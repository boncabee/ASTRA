import asyncio
from typing import Optional, Dict, Any

class AutomationJob:
    def __init__(self, execution_id: str, request_id: str, action: str, parameters: Dict[str, Any]):
        self.execution_id = execution_id
        self.request_id = request_id
        self.action = action
        self.parameters = parameters

class AutomationQueueManager:
    _instance: Optional['AutomationQueueManager'] = None
    
    def __init__(self) -> None:
        self.queue: asyncio.Queue[AutomationJob] = asyncio.Queue()
    
    @classmethod
    def get_instance(cls) -> 'AutomationQueueManager':
        if cls._instance is None:
            cls._instance = AutomationQueueManager()
        return cls._instance
    
    async def enqueue(self, job: AutomationJob) -> None:
        await self.queue.put(job)
        
    async def dequeue(self) -> AutomationJob:
        return await self.queue.get()
        
    def qsize(self) -> int:
        return self.queue.qsize()

automation_queue = AutomationQueueManager.get_instance()
