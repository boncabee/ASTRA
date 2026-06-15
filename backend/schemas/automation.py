from typing import Optional, Dict, Any, List
from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime
from models.automation import AutomationAction, AutomationState

class AutomationExecutionBase(BaseModel):
    state: AutomationState
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result_metadata: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    audit_metadata: Optional[Dict[str, Any]] = None

class AutomationExecutionResponse(AutomationExecutionBase):
    id: UUID
    request_id: UUID
    model_config = ConfigDict(from_attributes=True)

class AutomationRequestCreate(BaseModel):
    policy_id: UUID
    action: AutomationAction
    parameters: Dict[str, Any] = Field(default_factory=dict)

class AutomationRequestBase(BaseModel):
    policy_id: UUID
    action: AutomationAction
    parameters: Dict[str, Any]
    state: AutomationState
    created_at: datetime
    created_by: str

class AutomationRequestResponse(AutomationRequestBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)

class AutomationRequestDetailResponse(AutomationRequestResponse):
    executions: List[AutomationExecutionResponse] = []
    model_config = ConfigDict(from_attributes=True)

class AutomationMetricsResponse(BaseModel):
    automation_requests: int
    automation_executions: int
    automation_failures: int
    average_execution_time_ms: float
    queue_depth: int
