from typing import List, Optional, Tuple
from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.sql.expression import func
from models.observation import Observation, ObservationStatus
from schemas.observation import ObservationCreate

class ObservationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: ObservationCreate, created_by: str) -> Observation:
        observation = Observation(
            **data.model_dump(),
            created_by=created_by,
            updated_by=created_by
        )
        self.session.add(observation)
        await self.session.commit()
        await self.session.refresh(observation)
        return observation

    async def get_by_id(self, id: UUID) -> Optional[Observation]:
        result = await self.session.execute(select(Observation).where(Observation.id == id))
        return result.scalars().first()

    async def get_by_correlation_id(self, correlation_id: UUID) -> Optional[Observation]:
        result = await self.session.execute(select(Observation).where(Observation.correlation_id == correlation_id))
        return result.scalars().first()

    async def update(self, observation: Observation) -> Observation:
        self.session.add(observation)
        await self.session.commit()
        await self.session.refresh(observation)
        return observation

    async def list(
        self,
        skip: int = 0,
        limit: int = 50,
        status: Optional[ObservationStatus] = None,
        risk_category: Optional[str] = None,
        classification: Optional[str] = None,
        created_after: Optional[datetime] = None,
        created_before: Optional[datetime] = None
    ) -> Tuple[List[Observation], int]:
        
        query = select(Observation)
        
        if status:
            query = query.where(Observation.status == status)
        
        if risk_category:
            risk_category = risk_category.upper()
            if risk_category == "INFORMATIONAL":
                query = query.where(and_(Observation.risk_score >= 0, Observation.risk_score <= 19))
            elif risk_category == "LOW":
                query = query.where(and_(Observation.risk_score >= 20, Observation.risk_score <= 39))
            elif risk_category == "MEDIUM":
                query = query.where(and_(Observation.risk_score >= 40, Observation.risk_score <= 69))
            elif risk_category == "HIGH":
                query = query.where(and_(Observation.risk_score >= 70, Observation.risk_score <= 89))
            elif risk_category == "CRITICAL":
                query = query.where(and_(Observation.risk_score >= 90, Observation.risk_score <= 100))

        if classification:
            query = query.where(Observation.classification == classification)
            
        if created_after:
            query = query.where(Observation.created_at >= created_after)
            
        if created_before:
            query = query.where(Observation.created_at <= created_before)

        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.session.execute(count_query)
        total = total_result.scalar() or 0

        # Apply pagination
        query = query.order_by(Observation.created_at.desc()).offset(skip).limit(limit)
        result = await self.session.execute(query)
        
        return list(result.scalars().all()), total
