from typing import List, Optional, Tuple
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.sql.expression import func
from models.policy import Policy, PolicyEvaluation
from schemas.policy import PolicyCreate

class PolicyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: PolicyCreate, created_by: str) -> Policy:
        policy = Policy(
            **data.model_dump(),
            created_by=created_by,
            updated_by=created_by
        )
        self.session.add(policy)
        await self.session.commit()
        await self.session.refresh(policy)
        return policy

    async def get_by_id(self, id: UUID) -> Optional[Policy]:
        result = await self.session.execute(select(Policy).where(Policy.id == id))
        return result.scalars().first()

    async def get_by_name(self, name: str) -> Optional[Policy]:
        result = await self.session.execute(select(Policy).where(Policy.name == name))
        return result.scalars().first()

    async def update(self, policy: Policy) -> Policy:
        self.session.add(policy)
        await self.session.commit()
        await self.session.refresh(policy)
        return policy

    async def list(self, skip: int = 0, limit: int = 50) -> Tuple[List[Policy], int]:
        query = select(Policy)
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.session.execute(count_query)
        total = total_result.scalar() or 0

        # Apply pagination
        query = query.order_by(Policy.priority.desc(), Policy.id.asc()).offset(skip).limit(limit)
        result = await self.session.execute(query)
        
        return list(result.scalars().all()), total
        
    async def get_active_policies(self) -> List[Policy]:
        query = select(Policy).where(Policy.is_active.is_(True)).order_by(Policy.priority.desc(), Policy.id.asc())
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def record_evaluation(self, evaluation: PolicyEvaluation) -> PolicyEvaluation:
        self.session.add(evaluation)
        await self.session.commit()
        await self.session.refresh(evaluation)
        return evaluation

    async def list_evaluations(self, skip: int = 0, limit: int = 50) -> Tuple[List[PolicyEvaluation], int]:
        query = select(PolicyEvaluation)
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.session.execute(count_query)
        total = total_result.scalar() or 0

        # Apply pagination
        query = query.order_by(PolicyEvaluation.evaluation_time.desc()).offset(skip).limit(limit)
        result = await self.session.execute(query)
        
        return list(result.scalars().all()), total
