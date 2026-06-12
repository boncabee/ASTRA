from typing import Optional
from pydantic import BaseModel, Field

class RawLog(BaseModel):
    raw_event: str = Field(..., description="The unparsed log string")
    source_hint: Optional[str] = Field(None, description="Optional hint about the source type")
