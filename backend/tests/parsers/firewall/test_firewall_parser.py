import pytest
import json
from app.schemas.parser import RawLog
from app.schemas.ces import Severity, ArtifactType
from app.parsers.firewall.firewall_parser import FirewallParser
from app.parsers.registry.registry import registry
from app.parsers.batch.batch_processor import BatchProcessor

@pytest.fixture(autouse=True)
def setup_registry():
    if not registry.has_parser("firewall"):
        registry.register_parser("firewall", FirewallParser)

def test_registry_integration():
    assert registry.has_parser("firewall")
    assert registry.get_parser("firewall") == FirewallParser

def test_allow_csv():
    raw_event = "10.0.5.15,203.0.113.88,50124,443,tcp,allow,Outbound_HTTPS"
    parser = FirewallParser()
    event = parser.parse(RawLog(raw_event=raw_event, source_hint="firewall"))
    
    assert event.event_type == "network.connection.allowed"
    assert event.severity == Severity.info
    assert event.actor.ip == "10.0.5.15"  # type: ignore
    assert event.actor.port == 50124  # type: ignore
    assert event.target.ip == "203.0.113.88"  # type: ignore
    assert event.target.port == 443  # type: ignore
    assert event.metadata["rule_name"] == "Outbound_HTTPS"
    assert event.metadata["protocol"] == "tcp"
    assert len(event.artifacts) == 1
    assert event.artifacts[0].type == ArtifactType.ip
    assert event.artifacts[0].value == "203.0.113.88"

def test_deny_json():
    raw_event = json.dumps({
        "timestamp": "2026-06-12T10:15:10Z",
        "src_ip": "10.0.5.15",
        "dst_ip": "198.51.100.99",
        "src_port": 50128,
        "dst_port": 22,
        "protocol": "tcp",
        "action": "DENY",
        "rule_name": "Block_Outbound_SSH"
    })
    parser = FirewallParser()
    event = parser.parse(RawLog(raw_event=raw_event, source_hint="firewall"))
    
    assert event.event_type == "network.connection.denied"
    assert event.severity == Severity.low
    assert event.timestamp == "2026-06-12T10:15:10Z"
    assert event.actor.ip == "10.0.5.15"  # type: ignore
    assert event.target.ip == "198.51.100.99"  # type: ignore
    assert event.metadata["rule_name"] == "Block_Outbound_SSH"

def test_drop():
    raw_event = "10.0.5.15,203.0.113.88,50124,443,udp,drop"
    parser = FirewallParser()
    event = parser.parse(RawLog(raw_event=raw_event, source_hint="firewall"))
    assert event.event_type == "network.connection.dropped"
    assert event.severity == Severity.low
    
def test_block():
    raw_event = "10.0.5.15,203.0.113.88,50124,443,icmp,block"
    parser = FirewallParser()
    event = parser.parse(RawLog(raw_event=raw_event, source_hint="firewall"))
    assert event.event_type == "network.connection.blocked"
    assert event.severity == Severity.low

def test_unknown_action():
    raw_event = "10.0.5.15,203.0.113.88,50124,443,tcp,QUARANTINE"
    parser = FirewallParser()
    event = parser.parse(RawLog(raw_event=raw_event, source_hint="firewall"))
    assert event.event_type == "custom.unknown.detected"

def test_malformed_event():
    raw_event = "this,is,not,enough,fields"
    parser = FirewallParser()
    with pytest.raises(ValueError) as exc:
        parser.parse(RawLog(raw_event=raw_event, source_hint="firewall"))
    assert "Unsupported Firewall log format" in str(exc.value)

def test_missing_ips():
    raw_event = json.dumps({
        "src_port": 123,
        "action": "allow"
    })
    parser = FirewallParser()
    event = parser.parse(RawLog(raw_event=raw_event, source_hint="firewall"))
    assert event.actor is None
    assert event.target is None

def test_invalid_ports():
    raw_event = json.dumps({
        "src_ip": "1.1.1.1",
        "dst_ip": "2.2.2.2",
        "src_port": "invalid",
        "dst_port": "invalid",
        "action": "allow"
    })
    parser = FirewallParser()
    event = parser.parse(RawLog(raw_event=raw_event, source_hint="firewall"))
    assert event.actor.port is None  # type: ignore
    assert event.target.port is None  # type: ignore

def test_missing_timestamp():
    raw_event = json.dumps({
        "src_ip": "1.1.1.1",
        "action": "allow"
    })
    parser = FirewallParser()
    event = parser.parse(RawLog(raw_event=raw_event, source_hint="firewall"))
    assert event.timestamp is not None

def test_invalid_timestamp():
    raw_event = json.dumps({
        "src_ip": "1.1.1.1",
        "action": "allow",
        "timestamp": "not-a-time"
    })
    parser = FirewallParser()
    event = parser.parse(RawLog(raw_event=raw_event, source_hint="firewall"))
    assert event.timestamp is not None
    assert "not-a-time" not in event.timestamp

def test_space_in_timestamp():
    raw_event = json.dumps({
        "src_ip": "1.1.1.1",
        "action": "allow",
        "timestamp": "2026-06-12 10:15:10"
    })
    parser = FirewallParser()
    event = parser.parse(RawLog(raw_event=raw_event, source_hint="firewall"))
    assert event.timestamp == "2026-06-12T10:15:10Z"

def test_batch_integration():
    logs = [
        RawLog(raw_event='{"action": "ALLOW", "src_ip": "1.1.1.1"}', source_hint="firewall"),
        RawLog(raw_event="malformed", source_hint="firewall")
    ]
    processor = BatchProcessor()
    result = processor.process(logs)
    
    assert result.total_logs == 2
    assert result.successful_events == 1
    assert result.fallback_events == 1
    assert result.events[0].actor.ip == "1.1.1.1"  # type: ignore
    assert result.events[1].event_type == "custom.parsing.failed"  # type: ignore

def test_fallback_integration():
    raw_event = "malformed"
    parser = FirewallParser()
    event = parser.parse_safe(RawLog(raw_event=raw_event, source_hint="firewall"))
    assert event.event_type == "custom.parsing.failed"
