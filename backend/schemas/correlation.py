from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID

class CorrelationRuleResponse(BaseModel):
    id: UUID
    name: str
    description: str
    enabled: bool
    event_types: List[str]
    conditions: Dict[str, Any]
    time_window: int
    severity_weight: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class CorrelationMatchResponse(BaseModel):
    id: UUID
    rule_id: UUID
    matched_events: List[UUID]
    event_count: int
    match_timestamp: datetime
    correlation_score: int
    context: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    expires_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
