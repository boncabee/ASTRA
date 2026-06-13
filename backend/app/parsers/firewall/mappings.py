from typing import Dict, Any

FIREWALL_FIELD_MAPPINGS: Dict[str, str] = {
    "src_ip": "source.ip",
    "dst_ip": "target.ip",
    "src_port": "source.port",
    "dst_port": "target.port",
    "protocol": "network.protocol"
}

FIREWALL_EVENT_MAPPINGS: Dict[str, str] = {
    "allow": "network.connection.allowed",
    "deny": "network.connection.denied",
    "drop": "network.connection.dropped",
    "block": "network.connection.blocked"
}

FIREWALL_CONFIG_DICT: Dict[str, Any] = {
    "config_name": "firewall_default",
    "config_version": "1.0",
    "description": "Default Firewall Event transformation rules",
    "parser_name": "FirewallParser",
    "source_type": "firewall",
    "enabled": True,
    "field_mappings": FIREWALL_FIELD_MAPPINGS,
    "event_mappings": FIREWALL_EVENT_MAPPINGS,
    "timezone": "UTC",
    "timestamp_field": "timestamp",
    "unknown_event_type": "custom.unknown.detected",
    "unknown_source_type": "firewall"
}
