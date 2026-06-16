from typing import List, Optional, Tuple
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.sql.expression import func
from models.case import Case, CaseStatus, CasePriority, CaseSeverity, CaseEvidenceLink
from schemas.case import CaseCreate


class CaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: CaseCreate, created_by: str) -> Case:
        case = Case(
            title=data.title,
            description=data.description,
            priority=data.priority,
            severity=data.severity,
            status=CaseStatus.DRAFT,
            created_by=created_by,
        )
        self.session.add(case)
        await self.session.commit()
        await self.session.refresh(case)
        return case

    async def get_by_id(self, id: UUID) -> Optional[Case]:
        result = await self.session.execute(select(Case).where(Case.id == id))
        return result.scalars().first()

    async def list(
        self,
        skip: int = 0,
        limit: int = 50,
        status: Optional[CaseStatus] = None,
        priority: Optional[CasePriority] = None,
        severity: Optional[CaseSeverity] = None,
        assigned_to: Optional[str] = None,
    ) -> Tuple[List[Case], int]:
        query = select(Case)

        if status:
            query = query.where(Case.status == status)
        if priority:
            query = query.where(Case.priority == priority)
        if severity:
            query = query.where(Case.severity == severity)
        if assigned_to:
            query = query.where(Case.assigned_to == assigned_to)

        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.session.execute(count_query)
        total = total_result.scalar() or 0

        query = query.order_by(Case.created_at.desc()).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all()), total

    async def update(self, case: Case) -> Case:
        self.session.add(case)
        await self.session.commit()
        await self.session.refresh(case)
        return case

    async def assign(self, case: Case, assigned_user_id: str) -> Case:
        case.assigned_to = assigned_user_id
        self.session.add(case)
        await self.session.commit()
        await self.session.refresh(case)
        return case

    async def change_status(self, case: Case, new_status: CaseStatus) -> Case:
        case.status = new_status
        self.session.add(case)
        await self.session.commit()
        await self.session.refresh(case)
        return case

    async def link_evidence(self, case_id: UUID, evidence_id: UUID, created_by: str) -> CaseEvidenceLink:
        # Check if already linked and inactive
        query = select(CaseEvidenceLink).where(
            CaseEvidenceLink.case_id == case_id,
            CaseEvidenceLink.evidence_id == evidence_id
        )
        result = await self.session.execute(query)
        existing_link = result.scalars().first()

        if existing_link:
            if not existing_link.is_active:
                existing_link.is_active = True
                self.session.add(existing_link)
                await self.session.commit()
                await self.session.refresh(existing_link)
            return existing_link

        link = CaseEvidenceLink(
            case_id=case_id,
            evidence_id=evidence_id,
            created_by=created_by,
        )
        self.session.add(link)
        await self.session.commit()
        await self.session.refresh(link)
        return link

    async def get_evidence_links(self, case_id: UUID) -> List[CaseEvidenceLink]:
        query = select(CaseEvidenceLink).where(
            CaseEvidenceLink.case_id == case_id,
            CaseEvidenceLink.is_active.is_(True)
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def soft_unlink_evidence(self, link_id: UUID) -> Optional[CaseEvidenceLink]:
        result = await self.session.execute(select(CaseEvidenceLink).where(CaseEvidenceLink.id == link_id))
        link = result.scalars().first()
        if not link:
            return None
        
        link.is_active = False
        self.session.add(link)
        await self.session.commit()
        await self.session.refresh(link)
        return link

