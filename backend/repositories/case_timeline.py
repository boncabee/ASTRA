from typing import List, Optional, Tuple
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.sql.expression import func
from models.case import CaseTimeline, TimelineEventType


class CaseTimelineRepository:
    """
    Append-only repository for Case Timeline events.
    No update or delete operations — immutability enforced at repository level.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        case_id: UUID,
        event_type: TimelineEventType,
        actor: str,
        event_metadata: Optional[dict] = None,
    ) -> CaseTimeline:
        event = CaseTimeline(
            case_id=case_id,
            event_type=event_type,
            actor=actor,
            event_metadata=event_metadata,
        )
        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)
        return event

    async def get_by_case_id(
        self,
        case_id: UUID,
        skip: int = 0,
        limit: int = 50,
    ) -> Tuple[List[CaseTimeline], int]:
        query = select(CaseTimeline).where(CaseTimeline.case_id == case_id)

        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.session.execute(count_query)
        total = total_result.scalar() or 0

        query = query.order_by(CaseTimeline.created_at.asc()).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all()), total

    # NOTE: No update() method — timeline is immutable
    # NOTE: No delete() method — timeline is immutable
