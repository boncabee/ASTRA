from typing import List, Optional, Tuple
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.sql.expression import func
from models.evidence import Evidence, AuditEvent
from schemas.evidence import EvidenceCreate, AuditEventCreate

class EvidenceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_evidence(self, data: EvidenceCreate, created_by: str) -> Evidence:
        evidence = Evidence(
            **data.model_dump(),
            created_by=created_by
        )
        self.session.add(evidence)
        await self.session.commit()
        await self.session.refresh(evidence)
        return evidence

    async def get_evidence_by_id(self, id: UUID) -> Optional[Evidence]:
        result = await self.session.execute(select(Evidence).where(Evidence.id == id))
        return result.scalars().first()

    async def get_evidence_by_observation(self, observation_id: UUID) -> List[Evidence]:
        query = select(Evidence).where(Evidence.observation_id == observation_id).order_by(Evidence.created_at.desc())
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def list_evidence(self, skip: int = 0, limit: int = 50) -> Tuple[List[Evidence], int]:
        query = select(Evidence)
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.session.execute(count_query)
        total = total_result.scalar() or 0

        query = query.order_by(Evidence.created_at.desc()).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all()), total

class AuditRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_event(self, data: AuditEventCreate) -> AuditEvent:
        event = AuditEvent(**data.model_dump())
        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)
        return event

    async def get_events_by_entity(self, entity_type: str, entity_id: UUID) -> List[AuditEvent]:
        query = select(AuditEvent).where(
            AuditEvent.entity_type == entity_type,
            AuditEvent.entity_id == entity_id
        ).order_by(AuditEvent.timestamp.desc())
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def list_events(self, skip: int = 0, limit: int = 50) -> Tuple[List[AuditEvent], int]:
        query = select(AuditEvent)
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.session.execute(count_query)
        total = total_result.scalar() or 0

        query = query.order_by(AuditEvent.timestamp.desc()).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all()), total
