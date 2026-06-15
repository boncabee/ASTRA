import asyncio
import logging
from datetime import datetime, timezone
from sqlalchemy.future import select
from core.database import SessionLocal
from core.queue import automation_queue, AutomationJob
from models.automation import AutomationExecution, AutomationRequest, AutomationState
from integrations.providers import get_provider

logger = logging.getLogger(__name__)

class AutomationWorker:
    def __init__(self) -> None:
        self.is_running: bool = False
        self._task: asyncio.Task[None] | None = None

    async def start(self) -> None:
        if self.is_running:
            return
        self.is_running = True
        self._task = asyncio.create_task(self._run_loop())
        logger.info("AutomationWorker started.")

    async def stop(self) -> None:
        self.is_running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("AutomationWorker stopped.")

    async def _run_loop(self) -> None:
        while self.is_running:
            try:
                job: AutomationJob = await automation_queue.dequeue()
                await self._process_job(job)
                automation_queue.queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in AutomationWorker loop: {e}")

    async def _process_job(self, job: AutomationJob) -> None:
        logger.info(f"Processing automation job for execution {job.execution_id}")
        async with SessionLocal() as session:
            try:
                # Fetch execution and request
                result = await session.execute(
                    select(AutomationExecution).where(AutomationExecution.id == job.execution_id)
                )
                execution = result.scalars().first()
                
                if not execution:
                    logger.error(f"Execution {job.execution_id} not found.")
                    return

                request_result = await session.execute(
                    select(AutomationRequest).where(AutomationRequest.id == job.request_id)
                )
                request = request_result.scalars().first()

                if not request:
                    logger.error(f"Request {job.request_id} not found.")
                    return

                # Update state to RUNNING
                now = datetime.now(timezone.utc)
                execution.state = AutomationState.RUNNING
                execution.started_at = now
                request.state = AutomationState.RUNNING
                await session.commit()

                # Execute provider logic
                provider = get_provider(job.action)
                try:
                    success, result_metadata, error_message = await provider.execute(job.parameters)
                    
                    execution.completed_at = datetime.now(timezone.utc)
                    execution.result_metadata = result_metadata
                    
                    if success:
                        execution.state = AutomationState.SUCCESS
                        request.state = AutomationState.SUCCESS
                    else:
                        execution.state = AutomationState.FAILED
                        execution.error_message = error_message
                        request.state = AutomationState.FAILED
                        
                except Exception as provider_error:
                    logger.error(f"Provider execution failed: {provider_error}")
                    execution.completed_at = datetime.now(timezone.utc)
                    execution.state = AutomationState.FAILED
                    execution.error_message = str(provider_error)
                    request.state = AutomationState.FAILED

                await session.commit()
                logger.info(f"Execution {job.execution_id} completed with state {execution.state}")

            except Exception as db_error:
                logger.error(f"Database error during job processing: {db_error}")

automation_worker = AutomationWorker()
