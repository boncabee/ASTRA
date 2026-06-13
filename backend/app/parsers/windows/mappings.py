from typing import Dict, Any

WINDOWS_FIELD_MAPPINGS: Dict[str, str] = {
    "TargetUserName": "actor.username",
    "TargetDomainName": "actor.domain",
    "IpAddress": "actor.ip",
    "Computer": "target.hostname"
}

WINDOWS_EVENT_MAPPINGS: Dict[str, str] = {
    "4624": "authentication.login.success",
    "4625": "authentication.login.failure",
    "4634": "authentication.logout.success",
    "4720": "custom.user.created",
    "4726": "custom.user.deleted"
}

WINDOWS_CONFIG_DICT: Dict[str, Any] = {
    "config_name": "windows_default",
    "config_version": "1.0",
    "description": "Default Windows Event transformation rules",
    "parser_name": "WindowsParser",
    "source_type": "windows",
    "enabled": True,
    "field_mappings": WINDOWS_FIELD_MAPPINGS,
    "event_mappings": WINDOWS_EVENT_MAPPINGS,
    "timezone": "UTC",
    "timestamp_field": "TimeCreated",
    "unknown_event_type": "custom.unknown.detected",
    "unknown_source_type": "windows"
}
