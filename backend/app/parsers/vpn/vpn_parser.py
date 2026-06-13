import json
import re
import uuid
from typing import Dict, Any, Optional
from datetime import datetime, timezone

from app.parsers.base.base_parser import BaseParser
from app.schemas.parser import RawLog
from app.schemas.ces import CESEvent, SourceType, Severity, Entity, Artifact, ArtifactType
from app.parsers.base.transformer_config import TransformerConfig
from app.parsers.vpn.config import vpn_transformer_config

# Regex for Cisco ASA Syslog
ASA_REGEX = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s+"
    r"ASA-\d+-(?P<event_code>\d+):\s+"
    r"AAA user authentication (?P<event_status>Successful|Rejected)\s*:\s*"
    r"(reason\s*=\s*(?P<reason>[^:]+)\s*:\s*)?"
    r"server\s*=\s*(?P<server>\S+)\s*:\s*"
    r"user\s*=\s*(?P<user>\S+)"
)

class VPNParser(BaseParser):
    def __init__(self, config: Optional[TransformerConfig] = None):
        self.config = config or vpn_transformer_config

    def _extract_data(self, raw_event: str) -> Dict[str, Any]:
        try:
            return json.loads(raw_event)
        except json.JSONDecodeError:
            pass
            
        match = ASA_REGEX.search(raw_event)
        if match:
            extracted = match.groupdict()
            return {
                "timestamp": extracted.get("timestamp"),
                "username": extracted.get("user"),
                "server_ip": extracted.get("server"),
                "event": extracted.get("event_status"),
                "reason": extracted.get("reason"),
                "hostname": "vpn.corp.global"
            }
            
        raise ValueError("Unsupported VPN log format: Neither JSON nor recognized ASA Syslog.")

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
                mapped_data[ces_key] = data[raw_key]

        actor_data = {}
        if "actor.username" in mapped_data:
            actor_data["username"] = mapped_data["actor.username"]
        if "actor.ip" in mapped_data:
            actor_data["ip"] = mapped_data["actor.ip"]
        actor = Entity(**actor_data) if actor_data else None

        target_data = {}
        if "target.ip" in mapped_data:
            target_data["ip"] = mapped_data["target.ip"]
        if "target.hostname" in mapped_data:
            target_data["hostname"] = mapped_data["target.hostname"]
        target = Entity(**target_data) if target_data else None

        raw_event_status = data.get("event")
        event_type = self.config.event_mappings.get(str(raw_event_status) if raw_event_status is not None else "", self.config.unknown_event_type)

        severity = Severity.info
        if event_type == "authentication.login.failure":
            severity = Severity.low

        artifacts = []
        if actor and actor.ip:
            artifacts.append(Artifact(type=ArtifactType.ip, value=actor.ip))
            
        metadata = {}
        if "reason" in data and data["reason"]:
            metadata["reason"] = data["reason"].strip()
        
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
