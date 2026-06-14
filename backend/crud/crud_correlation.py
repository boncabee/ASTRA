import uuid
from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from models.correlation import CorrelationRule, CorrelationMatch

class CRUDCorrelation:
    async def create_rule(self, db: AsyncSession, *, obj_in: dict) -> CorrelationRule:
        db_obj = CorrelationRule(**obj_in)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_rule(self, db: AsyncSession, id: uuid.UUID) -> Optional[CorrelationRule]:
        return await db.get(CorrelationRule, id)

    async def update_rule(self, db: AsyncSession, *, db_obj: CorrelationRule, obj_in: dict) -> CorrelationRule:
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_rules(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[CorrelationRule]:
        query = select(CorrelationRule).offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())

    async def get_match(self, db: AsyncSession, id: uuid.UUID) -> Optional[CorrelationMatch]:
        return await db.get(CorrelationMatch, id)

    async def create_match(self, db: AsyncSession, *, obj_in: dict) -> CorrelationMatch:
        db_obj = CorrelationMatch(**obj_in)
        # Default retention to None per MVP (expires_at is nullable)
        # We can implement a policy here later if needed
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_matches(
        self, 
        db: AsyncSession, 
        *, 
        rule_id: Optional[uuid.UUID] = None, 
        min_score: Optional[int] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[CorrelationMatch]:
        query = select(CorrelationMatch)
        filters = []
        if rule_id:
            filters.append(CorrelationMatch.rule_id == rule_id)
        if min_score is not None:
            filters.append(CorrelationMatch.correlation_score >= min_score)
        if start_time:
            filters.append(CorrelationMatch.match_timestamp >= start_time)
        if end_time:
            filters.append(CorrelationMatch.match_timestamp <= end_time)
            
        if filters:
            query = query.where(and_(*filters))
            
        query = query.order_by(CorrelationMatch.match_timestamp.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())

correlation_crud = CRUDCorrelation()
