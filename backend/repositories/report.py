from typing import List, Optional, Tuple
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.expression import func
from models.report import Report, ComplianceMapping
from schemas.report import ReportCreate

class ReportRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_report(self, data: ReportCreate, created_by: str) -> Report:
        report_data = data.model_dump(exclude={"compliance_mappings"})
        report = Report(
            **report_data,
            created_by=created_by
        )
        self.session.add(report)
        await self.session.flush()

        if data.compliance_mappings:
            for mapping in data.compliance_mappings:
                compliance = ComplianceMapping(
                    report_id=report.id,
                    **mapping.model_dump()
                )
                self.session.add(compliance)
        
        await self.session.commit()
        return await self.get_report(report.id)

    async def get_report(self, report_id: UUID) -> Optional[Report]:
        query = select(Report).options(selectinload(Report.compliance_mappings)).where(Report.id == report_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def list_reports(self, skip: int = 0, limit: int = 100) -> Tuple[List[Report], int]:
        query = select(Report).options(selectinload(Report.compliance_mappings))
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.session.execute(count_query)
        total = total_result.scalar() or 0

        query = query.order_by(Report.created_at.desc()).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all()), total

    async def get_history(self, skip: int = 0, limit: int = 100) -> Tuple[List[Report], int]:
        # Identical to list_reports but could exclude details if we optimized query
        # For MVP, reuse list_reports
        return await self.list_reports(skip=skip, limit=limit)

    async def get_compliance_mappings(self, report_id: UUID) -> List[ComplianceMapping]:
        query = select(ComplianceMapping).where(ComplianceMapping.report_id == report_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())
