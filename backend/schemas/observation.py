from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from uuid import UUID
from models.observation import ObservationStatus, PolicyAction

class ObservationBase(BaseModel):
    title: str
    description: str
    correlation_id: UUID
    classification: str
    status: ObservationStatus = ObservationStatus.NEW
    risk_score: int = Field(ge=0, le=100)
    policy_action: Optional[PolicyAction] = None
    evidence_count: int

class ObservationCreate(ObservationBase):
    pass

class ObservationUpdate(BaseModel):
    status: ObservationStatus

class ObservationResponse(ObservationBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
