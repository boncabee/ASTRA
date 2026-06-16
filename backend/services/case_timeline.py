"""
TimelineService — Strict append-only service for Case Timeline events.

This service enforces immutability: events can only be created and read.
No update or delete operations are exposed.
"""
from typing import List, Optional, Tuple
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from models.case import CaseTimeline, TimelineEventType
from repositories.case_timeline import CaseTimelineRepository
from core.logging import logger


class TimelineService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.timeline_repo = CaseTimelineRepository(session)

    async def record_event(
        self,
        case_id: UUID,
        event_type: TimelineEventType,
        actor: str,
        event_metadata: Optional[dict] = None,
    ) -> CaseTimeline:
        """
        Append a new immutable event to the case timeline.
        Every state transition, assignment, and system action is recorded here.
        """
        if not case_id:
            raise ValueError("case_id is required for timeline events")
        if not actor:
            raise ValueError("actor is required for timeline events")

        event = await self.timeline_repo.create(
            case_id=case_id,
            event_type=event_type,
            actor=actor,
            event_metadata=event_metadata,
        )

        logger.info("Timeline event recorded", extra={
            "event": "timeline_event_created",
            "case_id": str(case_id),
            "event_type": event_type.value,
            "actor": actor,
        })

        return event

    async def get_timeline(
        self,
        case_id: UUID,
        skip: int = 0,
        limit: int = 50,
    ) -> Tuple[List[CaseTimeline], int]:
        """Retrieve timeline events for a case in chronological order."""
        return await self.timeline_repo.get_by_case_id(case_id, skip=skip, limit=limit)

    # NOTE: No update method — timeline is immutable
    # NOTE: No delete method — timeline is immutable
