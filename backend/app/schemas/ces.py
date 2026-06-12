from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from app.core.versioning import validate_schema_version, check_deprecated_fields
from datetime import datetime
import re
from uuid import UUID
from enum import Enum

MAX_RAW_EVENT_SIZE = 65536

class EventCategory(str, Enum):
    authentication = "authentication"
    network = "network"
    process = "process"
    file = "file"
    endpoint = "endpoint"
    cloud = "cloud"
    application = "application"
    custom = "custom"

class ArtifactType(str, Enum):
    ip = "ip"
    hash = "hash"
    domain = "domain"
    url = "url"
    file = "file"
    process = "process"
    user = "user"
    host = "host"
    email = "email"
    registry = "registry"
    certificate = "certificate"

class SourceType(str, Enum):
    vpn = "vpn"
    windows = "windows"
    firewall = "firewall"
    powershell = "powershell"
    cloudtrail = "cloudtrail"
    application = "application"
    custom = "custom"

class Severity(str, Enum):
    info = "info"
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"
    informational = "informational"

class Artifact(BaseModel):
    type: ArtifactType
    value: str

class Entity(BaseModel):
    model_config = ConfigDict(extra="allow")
    
    id: Optional[str] = None
    name: Optional[str] = None
    username: Optional[str] = None
    hostname: Optional[str] = None
    ip: Optional[str] = None
    
    # Additional common fields
    port: Optional[int] = None
    domain: Optional[str] = None
    process: Optional[str] = None
    command_line: Optional[str] = None

    @model_validator(mode='after')
    def check_identity_fields(self):
        if not any([self.id, self.name, self.username, self.hostname, self.ip]):
            raise ValueError("Entity must contain at least one identifying field (id, name, username, hostname, ip)")
        return self

class CESEvent(BaseModel):
    schema_version: str = Field(default="1.0", description="CES schema version")
    event_id: str = Field(..., description="Globally unique identifier")
    timestamp: str = Field(..., description="Exact time the event occurred in UTC, ISO-8601")
    source_type: SourceType = Field(..., description="System or vendor originating the raw log")
    event_type: str = Field(..., description="Normalized action (category.action.outcome)")
    severity: Severity = Field(..., description="Normalized severity level")
    actor: Optional[Entity] = Field(default=None, description="Entity initiating the action")
    target: Optional[Entity] = Field(default=None, description="Entity being acted upon")
    artifacts: List[Artifact] = Field(default_factory=list, description="Extracted Indicators of Compromise")
    raw_event: str = Field(..., max_length=MAX_RAW_EVENT_SIZE, description="Original, unmodified source log string")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Parser-specific context")
    model_config = ConfigDict(extra="ignore")

    @field_validator('schema_version')
    @classmethod
    def validate_version(cls, v: str) -> str:
        validate_schema_version(v)
        return v

    @model_validator(mode='before')
    @classmethod
    def check_deprecations(cls, data: Any) -> Any:
        if isinstance(data, dict):
            version = data.get('schema_version', '1.0')
            check_deprecated_fields(data, version)
        return data

    @field_validator('timestamp')
    @classmethod
    def validate_timestamp(cls, v: str) -> str:
        try:
            parsed = v.replace('Z', '+00:00')
            datetime.fromisoformat(parsed)
        except ValueError:
            raise ValueError('timestamp must be a valid ISO-8601 format string')
        return v

    @field_validator('event_type')
    @classmethod
    def validate_event_type(cls, v: str) -> str:
        match = re.match(r'^([\w-]+)\.([\w-]+)\.([\w-]+)$', v)
        if not match:
            raise ValueError('event_type must follow category.action.outcome taxonomy')
        
        category = match.group(1)
        try:
            EventCategory(category)
        except ValueError:
            allowed = [e.value for e in EventCategory]
            raise ValueError(f"event_type category '{category}' is invalid. Allowed categories: {allowed}")
        return v

    @field_validator('severity', mode='before')
    @classmethod
    def validate_severity(cls, v: Any) -> Any:
        if isinstance(v, str):
            return v.lower()
        return v
