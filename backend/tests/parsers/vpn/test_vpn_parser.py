import pytest
import json
from app.schemas.parser import RawLog
from app.schemas.ces import SourceType, Severity, ArtifactType
from app.parsers.vpn.vpn_parser import VPNParser
import app.parsers.vpn  # ensures the parser is registered in __init__.py
from app.parsers.registry.registry import registry
from app.parsers.batch.batch_processor import BatchProcessor

@pytest.fixture(autouse=True)
def setup_registry():
    if not registry.has_parser("vpn"):
        registry.register_parser("vpn", VPNParser)

def test_registry_integration():
    assert registry.has_parser("vpn")
    assert registry.get_parser("vpn") == VPNParser

def test_login_success_regex():
    raw_event = "2026-06-12 08:15:30 ASA-6-113004: AAA user authentication Successful : server =  10.1.2.3 : user = jroberts"
    parser = VPNParser()
    event = parser.parse(RawLog(raw_event=raw_event, source_hint="vpn"))
    
    assert event.event_type == "authentication.login.success"
    assert event.severity == Severity.info
    assert event.timestamp == "2026-06-12T08:15:30Z"
    assert event.actor.username == "jroberts"  # type: ignore
    assert event.target.ip == "10.1.2.3"  # type: ignore
    assert event.target.hostname == "vpn.corp.global"  # type: ignore

def test_login_failure_regex():
    raw_event = "2026-06-12 08:16:01 ASA-6-113005: AAA user authentication Rejected : reason = AAA failure : server = 10.1.2.3 : user = jroberts"
    parser = VPNParser()
    event = parser.parse(RawLog(raw_event=raw_event, source_hint="vpn"))
    
    assert event.event_type == "authentication.login.failure"
    assert event.severity == Severity.low
    assert event.timestamp == "2026-06-12T08:16:01Z"
    assert event.actor.username == "jroberts"  # type: ignore
    assert event.target.ip == "10.1.2.3"  # type: ignore
    assert event.metadata["reason"] == "AAA failure"  # type: ignore

def test_login_success_json():
    raw_event = json.dumps({
        "timestamp": "2026-06-12T08:15:30Z",
        "username": "jdoe",
        "src_ip": "10.1.1.5",
        "event": "LOGIN_SUCCESS"
    })
    parser = VPNParser()
    event = parser.parse(RawLog(raw_event=raw_event, source_hint="vpn"))
    
    assert event.event_type == "authentication.login.success"
    assert event.actor.username == "jdoe"  # type: ignore
    assert event.actor.ip == "10.1.1.5"  # type: ignore
    assert len(event.artifacts) == 1
    assert event.artifacts[0].type == ArtifactType.ip
    assert event.artifacts[0].value == "10.1.1.5"

def test_unknown_event():
    raw_event = json.dumps({
        "timestamp": "2026-06-12T08:15:30Z",
        "event": "WEIRD_EVENT"
    })
    parser = VPNParser()
    event = parser.parse(RawLog(raw_event=raw_event, source_hint="vpn"))
    
    assert event.event_type == "custom.unknown.detected"

def test_malformed_input():
    raw_event = "this is not json and not regex"
    parser = VPNParser()
    with pytest.raises(ValueError) as exc:
        parser.parse(RawLog(raw_event=raw_event, source_hint="vpn"))
    assert "Unsupported VPN log format" in str(exc.value)

def test_missing_timestamp():
    raw_event = json.dumps({
        "username": "jdoe",
        "event": "LOGIN_SUCCESS"
    })
    parser = VPNParser()
    event = parser.parse(RawLog(raw_event=raw_event, source_hint="vpn"))
    
    assert event.timestamp is not None
    assert "T" in event.timestamp

def test_fallback_integration():
    raw_event = "malformed"
    parser = VPNParser()
    # parse_safe should catch the ValueError and return a fallback event
    event = parser.parse_safe(RawLog(raw_event=raw_event, source_hint="vpn"))
    assert event.event_type == "custom.parsing.failed"

def test_batch_integration():
    logs = [
        RawLog(raw_event='{"timestamp": "2026-06-12T08:15:30Z", "event": "LOGIN_SUCCESS", "username": "u1", "src_ip": "10.1.1.1"}', source_hint="vpn"),
        RawLog(raw_event="malformed", source_hint="vpn")
    ]
    processor = BatchProcessor()
    result = processor.process(logs)
    
    assert result.total_logs == 2
    assert result.successful_events == 1
    assert result.fallback_events == 1
    assert result.events[0].actor.username == "u1"  # type: ignore
    assert result.events[1].event_type == "custom.parsing.failed"  # type: ignore

def test_invalid_timestamp_parsing():
    raw_event = json.dumps({
        "timestamp": "this_is_not_a_time",
        "username": "jdoe",
        "event": "LOGIN_SUCCESS"
    })
    parser = VPNParser()
    event = parser.parse(RawLog(raw_event=raw_event, source_hint="vpn"))
    
    assert event.timestamp is not None
    assert "this_is_not_a_time" not in event.timestamp
    assert "T" in event.timestamp
