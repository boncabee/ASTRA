import json
import uuid
from typing import Dict, Any, Optional
from datetime import datetime, timezone

from app.parsers.base.base_parser import BaseParser
from app.schemas.parser import RawLog
from app.schemas.ces import CESEvent, SourceType, Severity, Entity, Artifact, ArtifactType
from app.parsers.base.transformer_config import TransformerConfig
from app.parsers.firewall.config import firewall_transformer_config

class FirewallParser(BaseParser):
    def __init__(self, config: Optional[TransformerConfig] = None):
        self.config = config or firewall_transformer_config

    def _extract_data(self, raw_event: str) -> Dict[str, Any]:
        try:
            return json.loads(raw_event)
        except json.JSONDecodeError:
            pass
            
        data = {}
        parts = raw_event.split(",")
        if len(parts) >= 6:
            data["src_ip"] = parts[0].strip()
            data["dst_ip"] = parts[1].strip()
            data["src_port"] = parts[2].strip()
            data["dst_port"] = parts[3].strip()
            data["protocol"] = parts[4].strip()
            data["action"] = parts[5].strip()
            if len(parts) > 6:
                data["rule_name"] = parts[6].strip()
            return data
            
        raise ValueError("Unsupported Firewall log format: Neither JSON nor CSV.")

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
        if "source.ip" in mapped_data:
            actor_data["ip"] = mapped_data["source.ip"]
        if "source.port" in mapped_data:
            try:
                actor_data["port"] = int(mapped_data["source.port"])
            except ValueError:
                pass
        if actor_data and any(k in actor_data for k in ["id", "name", "username", "hostname", "ip"]):
            actor = Entity(**actor_data)
        else:
            actor = None

        target_data = {}
        if "target.ip" in mapped_data:
            target_data["ip"] = mapped_data["target.ip"]
        if "target.port" in mapped_data:
            try:
                target_data["port"] = int(mapped_data["target.port"])
            except ValueError:
                pass
        if target_data and any(k in target_data for k in ["id", "name", "username", "hostname", "ip"]):
            target = Entity(**target_data)
        else:
            target = None

        raw_action = data.get("action", "")
        action_lower = str(raw_action).lower()
        event_type = self.config.event_mappings.get(action_lower, self.config.unknown_event_type)

        severity = Severity.info
        if event_type in ["network.connection.denied", "network.connection.dropped", "network.connection.blocked"]:
            severity = Severity.low

        artifacts = []
        if target and target.ip:
            artifacts.append(Artifact(type=ArtifactType.ip, value=target.ip))
            
        metadata = {}
        if "rule_name" in data:
            metadata["rule_name"] = str(data["rule_name"])
        if "network.protocol" in mapped_data:
            metadata["protocol"] = mapped_data["network.protocol"]
            
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
