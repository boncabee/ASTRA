from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from uuid import UUID
from models.observation import ObservationStatus, PolicyAction

class PolicyBase(BaseModel):
    name: str = Field(..., description="Unique name of the policy")
    description: str
    action: PolicyAction
    priority: int = Field(default=100, description="Higher number means higher priority")
    is_active: bool = True
    
    # Conditions
    condition_risk_min: Optional[int] = Field(None, ge=0, le=100)
    condition_risk_max: Optional[int] = Field(None, ge=0, le=100)
    condition_classification: Optional[str] = None
    condition_status: Optional[ObservationStatus] = None

class PolicyCreate(PolicyBase):
    pass

class PolicyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    action: Optional[PolicyAction] = None
    priority: Optional[int] = None
    is_active: Optional[bool] = None
    condition_risk_min: Optional[int] = Field(None, ge=0, le=100)
    condition_risk_max: Optional[int] = Field(None, ge=0, le=100)
    condition_classification: Optional[str] = None
    condition_status: Optional[ObservationStatus] = None

class PolicyResponse(PolicyBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class PolicyEvaluationResponse(BaseModel):
    id: UUID
    policy_id: Optional[UUID] = None
    observation_id: UUID
    evaluation_time: datetime
    decision_reason: str
    action: PolicyAction
    
    model_config = ConfigDict(from_attributes=True)
