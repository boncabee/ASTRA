import json
import re
import uuid
from typing import Dict, Any, Optional
from datetime import datetime, timezone

from app.parsers.base.base_parser import BaseParser
from app.schemas.parser import RawLog
from app.schemas.ces import CESEvent, SourceType, Severity, Entity, Artifact, ArtifactType
from app.parsers.base.transformer_config import TransformerConfig
from app.parsers.windows.config import windows_transformer_config

class WindowsParser(BaseParser):
    def __init__(self, config: Optional[TransformerConfig] = None):
        self.config = config or windows_transformer_config

    def _extract_data(self, raw_event: str) -> Dict[str, Any]:
        try:
            return json.loads(raw_event)
        except json.JSONDecodeError:
            pass
            
        data = {}
        parts = re.split(r',\s*', raw_event)
        for part in parts:
            if ':' in part:
                k, v = part.split(':', 1)
                data[k.strip()] = v.strip().rstrip('.')
        
        if not data or "EventID" not in data:
            raise ValueError("Unsupported Windows log format: Neither JSON nor Key-Value.")
            
        return data

    def parse(self, raw_log: RawLog) -> CESEvent:
        data = self._extract_data(raw_log.raw_event)
        
        raw_time = None
        if self.config.timestamp_field:
            raw_time_val = data.get(self.config.timestamp_field)
            if raw_time_val is not None:
                raw_time = str(raw_time_val)
                
        if raw_time:
            if " " in raw_time and "T" not in raw_time:
                raw_time = raw_time.replace(" ", "T") + "Z"
            timestamp = raw_time
        else:
            timestamp = datetime.now(timezone.utc).isoformat()
            
        try:
            datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except ValueError:
            timestamp = datetime.now(timezone.utc).isoformat()

        mapped_data = {}
        for raw_key, ces_key in self.config.field_mappings.items():
            if raw_key in data and data[raw_key] is not None:
                mapped_data[ces_key] = str(data[raw_key])

        actor_data = {}
        if "actor.username" in mapped_data:
            actor_data["username"] = mapped_data["actor.username"]
        if "actor.domain" in mapped_data:
            actor_data["domain"] = mapped_data["actor.domain"]
        actor = Entity(**actor_data) if actor_data else None

        target_data = {}
        if "target.hostname" in mapped_data:
            target_data["hostname"] = mapped_data["target.hostname"]
        target = Entity(**target_data) if target_data else None

        raw_event_id = data.get("EventID")
        event_type = self.config.event_mappings.get(str(raw_event_id) if raw_event_id is not None else "", self.config.unknown_event_type)

        severity = Severity.info
        if event_type in ["authentication.login.failure", "custom.user.deleted"]:
            severity = Severity.medium

        artifacts = []
        if "actor.ip" in mapped_data:
            artifacts.append(Artifact(type=ArtifactType.ip, value=mapped_data["actor.ip"]))
            
        metadata = {}
        if "EventID" in data:
            metadata["event_id"] = str(data["EventID"])
        if "LogonType" in data:
            metadata["logon_type"] = str(data["LogonType"])
        if "Status" in data:
            metadata["failure_reason"] = str(data["Status"])
        if "ProcessName" in data:
            metadata["process_name"] = str(data["ProcessName"])
        
        return CESEvent(
            schema_version="1.0",
            event_id=str(uuid.uuid4()),
            timestamp=timestamp,
            source_type=SourceType(self.config.source_type),
            event_type=event_type,
            severity=severity,
            actor=actor,
            target=target,
            artifacts=artifacts,
            raw_event=raw_log.raw_event,
            metadata=metadata
        )
