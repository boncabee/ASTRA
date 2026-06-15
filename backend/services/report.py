from typing import List, Dict, Any, Optional
import time
from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.evidence import Evidence, AuditEvent
from repositories.report import ReportRepository
from repositories.observation import ObservationRepository
from schemas.report import ReportGenerateRequest, ReportCreate, ComplianceMappingCreate
from models.report import Report, ReportType
from core.logging import logger

class ReportService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.report_repo = ReportRepository(session)
        self.obs_repo = ObservationRepository(session)

    async def generate_report(self, request: ReportGenerateRequest, user_id: str) -> Report:
        start_time = time.time()
        
        # 1. Fetch observations (up to 10,000 for performance boundaries)
        max_observations = 10000
        limit = 1000
        skip = 0
        total_fetched = 0
        
        observation_ids = []
        classifications: Dict[str, int] = {}
        risk_scores = []
        
        while total_fetched < max_observations:
            obs_list, total = await self.obs_repo.list(
                skip=skip,
                limit=limit,
                created_after=request.time_range_start,
                created_before=request.time_range_end
            )
            
            if not obs_list:
                break
                
            for obs in obs_list:
                observation_ids.append(str(obs.id))
                risk_scores.append(obs.risk_score)
                class_name = obs.classification or "Unclassified"
                classifications[class_name] = classifications.get(class_name, 0) + 1
                
                total_fetched += 1
                if total_fetched >= max_observations:
                    break
                    
            skip += limit

        evidence_refs = []
        audit_refs = []
        
        # 2. Gather Evidence References without duplicating raw evidence
        if request.include_evidence and observation_ids:
            # We can fetch evidence IDs matching the time range
            ev_query = select(Evidence.id).where(
                Evidence.created_at >= request.time_range_start,
                Evidence.created_at <= request.time_range_end
            )
            ev_result = await self.session.execute(ev_query)
            evidence_refs = [str(e_id) for e_id in ev_result.scalars().all()]

        # 3. Gather Audit References
        if request.include_audit and observation_ids:
            # Fetch audit event IDs for the time range
            audit_query = select(AuditEvent.id).where(
                AuditEvent.timestamp >= request.time_range_start,
                AuditEvent.timestamp <= request.time_range_end
            )
            audit_result = await self.session.execute(audit_query)
            audit_refs = [str(a_id) for a_id in audit_result.scalars().all()]

        # 4. Generate Summary and Details
        avg_risk = sum(risk_scores) / len(risk_scores) if risk_scores else 0
        summary = f"Generated {request.report_type.value} based on {total_fetched} observations."
        
        details = {
            "total_observations": total_fetched,
            "average_risk_score": round(avg_risk, 2),
            "classifications": classifications,
            "evidence_count": len(evidence_refs),
            "audit_events_count": len(audit_refs)
        }

        # 5. Handle Compliance Framework Mapping
        compliance_mappings = []
        if request.compliance_frameworks:
            for framework in request.compliance_frameworks:
                compliance_mappings.append(
                    ComplianceMappingCreate(
                        framework=framework,
                        control_id=f"{framework}-GENERIC",
                        description=f"Automated compliance tagging for {framework}"
                    )
                )

        report_data = ReportCreate(
            report_type=request.report_type,
            scope={
                "time_range_start": request.time_range_start.isoformat(),
                "time_range_end": request.time_range_end.isoformat(),
                "max_observations_processed": total_fetched
            },
            data_sources=request.data_sources or [],
            evidence_references=evidence_refs,
            audit_references=audit_refs,
            summary=summary,
            details=details,
            compliance_mappings=compliance_mappings
        )

        # 6. Save Report
        report = await self.report_repo.create_report(report_data, created_by=user_id)
        
        # 7. Metrics Logging
        generation_time_ms = int((time.time() - start_time) * 1000)
        logger.info("Report generated successfully", extra={
            "event": "report_generation",
            "reports_generated": 1,
            "report_generation_time_ms": generation_time_ms,
            "evidence_references_count": len(evidence_refs),
            "compliance_mappings_used": len(compliance_mappings),
            "report_id": str(report.id)
        })

        return report
