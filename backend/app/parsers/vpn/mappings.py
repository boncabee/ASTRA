from typing import Dict, Any

VPN_FIELD_MAPPINGS: Dict[str, str] = {
    "username": "actor.username",
    "src_ip": "actor.ip",
    "server_ip": "target.ip",
    "hostname": "target.hostname"
}

VPN_EVENT_MAPPINGS: Dict[str, str] = {
    "LOGIN_SUCCESS": "authentication.login.success",
    "LOGIN_FAILURE": "authentication.login.failure",
    "Successful": "authentication.login.success",
    "Rejected": "authentication.login.failure"
}

VPN_CONFIG_DICT: Dict[str, Any] = {
    "config_name": "vpn_default",
    "config_version": "1.0",
    "description": "Default VPN transformation rules",
    "parser_name": "VPNParser",
    "source_type": "vpn",
    "enabled": True,
    "field_mappings": VPN_FIELD_MAPPINGS,
    "event_mappings": VPN_EVENT_MAPPINGS,
    "timezone": "UTC",
    "timestamp_field": "timestamp",
    "unknown_event_type": "custom.unknown.detected",
    "unknown_source_type": "vpn"
}
