from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from app.schemas.ces import CESEvent

class BatchResult(BaseModel):
    """
    Standardized result for batch transformation.
    """
    total_logs: int = Field(default=0, description="Total number of logs in the batch")
    successful_events: int = Field(default=0, description="Number of logs successfully parsed without fallback")
    failed_events: int = Field(default=0, description="Number of logs that completely failed parsing/fallback")
    fallback_events: int = Field(default=0, description="Number of logs processed via fallback mapping")
    processing_time_ms: float = Field(default=0.0, description="Time taken to process the batch in milliseconds")
    
    events: List[Optional[CESEvent]] = Field(default_factory=list, description="Output events, order preserved")
    errors: List[Dict[str, Any]] = Field(default_factory=list, description="List of catastrophic failures per log index")

    @property
    def success_rate(self) -> float:
        if self.total_logs == 0:
            return 0.0
        return round((self.successful_events / self.total_logs) * 100, 2)

    @property
    def failure_rate(self) -> float:
        if self.total_logs == 0:
            return 0.0
        return round((self.failed_events / self.total_logs) * 100, 2)

    @property
    def fallback_rate(self) -> float:
        if self.total_logs == 0:
            return 0.0
        return round((self.fallback_events / self.total_logs) * 100, 2)
