from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.case import CaseAssignment


class CaseAssignmentRepository:
    """Repository for case assignment history records."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        case_id: UUID,
        assigned_user_id: str,
        assigned_by: str,
    ) -> CaseAssignment:
        assignment = CaseAssignment(
            case_id=case_id,
            assigned_user_id=assigned_user_id,
            assigned_by=assigned_by,
        )
        self.session.add(assignment)
        await self.session.commit()
        await self.session.refresh(assignment)
        return assignment

    async def get_by_case_id(self, case_id: UUID) -> List[CaseAssignment]:
        query = (
            select(CaseAssignment)
            .where(CaseAssignment.case_id == case_id)
            .order_by(CaseAssignment.assigned_at.desc())
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())
