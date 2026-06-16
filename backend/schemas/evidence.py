from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from models.evidence import EvidenceType

class EvidenceBase(BaseModel):
    observation_id: UUID
    evidence_type: EvidenceType
    source: str
    content_reference: str
    hash_value: str

class EvidenceCreate(EvidenceBase):
    pass

class EvidenceResponse(EvidenceBase):
    id: UUID
    created_at: datetime
    created_by: str
    
    model_config = ConfigDict(from_attributes=True)

class AuditEventBase(BaseModel):
    entity_type: str
    entity_id: UUID
    action: str
    actor: str
    old_value: Optional[Union[Dict[str, Any], List[Any], str]] = None
    new_value: Optional[Union[Dict[str, Any], List[Any], str]] = None
    reason: Optional[str] = None

class AuditEventCreate(AuditEventBase):
    pass

class AuditEventResponse(AuditEventBase):
    id: UUID
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)

# For provenance engine
class DecisionProvenanceResponse(BaseModel):
    observation_id: UUID
    status: str
    risk_score: int
    classification: str
    policy_action: Optional[str] = None
    evidence: List[EvidenceResponse] = []
    evaluations: List[Dict[str, Any]] = [] # Will contain policy evaluations mapped to dicts
