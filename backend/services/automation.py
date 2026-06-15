from sqlalchemy.ext.asyncio import AsyncSession
from repositories.automation import AutomationRepository
from schemas.automation import AutomationRequestCreate
from core.queue import automation_queue, AutomationJob
import logging

logger = logging.getLogger(__name__)

class AutomationService:
    def __init__(self, db: AsyncSession):
        self.repo = AutomationRepository(db)

    async def create_automation_request(self, request_data: AutomationRequestCreate, user_id: str):
        # Create request and execution DB records
        request, execution = await self.repo.create_request(request_data, user_id)
        
        # Enqueue the job for background processing
        job = AutomationJob(
            execution_id=str(execution.id),
            request_id=str(request.id),
            action=request.action.value,
            parameters=request.parameters
        )
        
        await automation_queue.enqueue(job)
        logger.info(f"Enqueued automation job for execution {execution.id}")
        
        return request
