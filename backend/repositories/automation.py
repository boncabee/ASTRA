from typing import List, Tuple, Optional, Dict, Any
from uuid import UUID
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.automation import AutomationRequest, AutomationExecution, AutomationState
from schemas.automation import AutomationRequestCreate

class AutomationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_request(self, data: AutomationRequestCreate, created_by: str) -> Tuple[AutomationRequest, AutomationExecution]:
        db_request = AutomationRequest(
            policy_id=data.policy_id,
            action=data.action,
            parameters=data.parameters,
            created_by=created_by,
            state=AutomationState.PENDING
        )
        self.session.add(db_request)
        await self.session.flush()
        
        # Create execution record
        db_execution = AutomationExecution(
            request_id=db_request.id,
            state=AutomationState.QUEUED
        )
        self.session.add(db_execution)
        await self.session.commit()
        await self.session.refresh(db_request)
        await self.session.refresh(db_execution)
        
        return db_request, db_execution

    async def get_request(self, request_id: UUID) -> Optional[AutomationRequest]:
        result = await self.session.execute(
            select(AutomationRequest)
            .options(selectinload(AutomationRequest.executions))
            .where(AutomationRequest.id == request_id)
        )
        return result.scalars().first()

    async def list_requests(self, skip: int = 0, limit: int = 50) -> Tuple[List[AutomationRequest], int]:
        count_result = await self.session.execute(select(func.count()).select_from(AutomationRequest))
        total = count_result.scalar() or 0

        result = await self.session.execute(
            select(AutomationRequest)
            .order_by(desc(AutomationRequest.created_at))
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all()), total

    async def get_history(self, skip: int = 0, limit: int = 50) -> Tuple[List[AutomationExecution], int]:
        count_result = await self.session.execute(select(func.count()).select_from(AutomationExecution))
        total = count_result.scalar() or 0

        result = await self.session.execute(
            select(AutomationExecution)
            .order_by(desc(AutomationExecution.started_at)) # nulls will be at the bottom but it's fine for simple list
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all()), total

    async def get_metrics(self) -> Dict[str, Any]:
        from core.queue import automation_queue
        
        requests_count = await self.session.scalar(select(func.count()).select_from(AutomationRequest))
        executions_count = await self.session.scalar(select(func.count()).select_from(AutomationExecution))
        failures_count = await self.session.scalar(
            select(func.count()).select_from(AutomationExecution).where(AutomationExecution.state == AutomationState.FAILED)
        )
        
        # Calculate average execution time
        result = await self.session.execute(
            select(AutomationExecution.started_at, AutomationExecution.completed_at)
            .where(AutomationExecution.completed_at.isnot(None))
            .where(AutomationExecution.started_at.isnot(None))
        )
        rows = result.all()
        
        total_time = 0
        valid_executions = 0
        for started, completed in rows:
            if started and completed:
                total_time += (completed - started).total_seconds() * 1000
                valid_executions += 1
                
        avg_time = (total_time / valid_executions) if valid_executions > 0 else 0.0
        
        return {
            "automation_requests": requests_count or 0,
            "automation_executions": executions_count or 0,
            "automation_failures": failures_count or 0,
            "average_execution_time_ms": avg_time,
            "queue_depth": automation_queue.qsize()
        }
