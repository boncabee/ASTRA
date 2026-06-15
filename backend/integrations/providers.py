import logging
import asyncio
from typing import Dict, Any, Tuple

logger = logging.getLogger(__name__)

class AutomationProvider:
    async def execute(self, parameters: Dict[str, Any]) -> Tuple[bool, Dict[str, Any], str]:
        """
        Executes the automation action.
        Returns a tuple of (success, result_metadata, error_message)
        """
        raise NotImplementedError

class WebhookProvider(AutomationProvider):
    async def execute(self, parameters: Dict[str, Any]) -> Tuple[bool, Dict[str, Any], str]:
        logger.info(f"Mock Webhook execution with params: {parameters}")
        await asyncio.sleep(0.1) # Simulate network latency
        return True, {"status": "delivered", "provider": "WebhookProvider"}, ""

class TicketProvider(AutomationProvider):
    async def execute(self, parameters: Dict[str, Any]) -> Tuple[bool, Dict[str, Any], str]:
        logger.info(f"Mock Ticket creation with params: {parameters}")
        await asyncio.sleep(0.1)
        return True, {"ticket_id": "TKT-1234", "provider": "TicketProvider"}, ""

class EmailProvider(AutomationProvider):
    async def execute(self, parameters: Dict[str, Any]) -> Tuple[bool, Dict[str, Any], str]:
        logger.info(f"Mock Email sending with params: {parameters}")
        await asyncio.sleep(0.1)
        return True, {"status": "sent", "provider": "EmailProvider"}, ""

class LogProvider(AutomationProvider):
    async def execute(self, parameters: Dict[str, Any]) -> Tuple[bool, Dict[str, Any], str]:
        logger.info(f"Mock Log execution with params: {parameters}")
        return True, {"status": "logged", "provider": "LogProvider"}, ""

def get_provider(action: str) -> AutomationProvider:
    providers = {
        "NOTIFY_WEBHOOK": WebhookProvider(),
        "CREATE_TICKET": TicketProvider(),
        "SEND_EMAIL": EmailProvider(),
        "LOG_ACTION": LogProvider()
    }
    return providers.get(action, LogProvider())
