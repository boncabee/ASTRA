from typing import Optional, Dict, Any
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from models.case import CaseStatus, CasePriority, CaseSeverity


class CaseCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: CasePriority = CasePriority.MEDIUM
    severity: CaseSeverity = CaseSeverity.MEDIUM


class CaseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[CasePriority] = None
    severity: Optional[CaseSeverity] = None


class CaseStatusChange(BaseModel):
    new_status: CaseStatus
    reason: Optional[str] = None


class CaseAssignRequest(BaseModel):
    assigned_user_id: str


class CaseResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    status: CaseStatus
    priority: CasePriority
    severity: CaseSeverity
    assigned_to: Optional[str] = None
    created_by: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CaseTimelineResponse(BaseModel):
    id: UUID
    case_id: UUID
    event_type: str
    actor: str
    event_metadata: Optional[Dict[str, Any]] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CaseAssignmentResponse(BaseModel):
    id: UUID
    case_id: UUID
    assigned_user_id: str
    assigned_by: str
    assigned_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CaseEvidenceLinkCreate(BaseModel):
    evidence_id: UUID


class CaseEvidenceLinkResponse(BaseModel):
    id: UUID
    case_id: UUID
    evidence_id: UUID
    created_at: datetime
    created_by: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

