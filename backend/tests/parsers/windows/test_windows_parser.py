import pytest
import json
from app.schemas.parser import RawLog
from app.schemas.ces import Severity, ArtifactType
from app.parsers.windows.windows_parser import WindowsParser
from app.parsers.registry.registry import registry
from app.parsers.batch.batch_processor import BatchProcessor

@pytest.fixture(autouse=True)
def setup_registry():
    if not registry.has_parser("windows"):
        registry.register_parser("windows", WindowsParser)

def test_registry_integration():
    assert registry.has_parser("windows")
    assert registry.get_parser("windows") == WindowsParser

def test_4624_success_regex():
    raw_event = "EventID: 4624, LogonType: 3, TargetUserName: msmith, TargetDomainName: CORP_AD, Computer: WS-INT-04, ProcessName: advapi, IpAddress: 10.1.1.5"
    parser = WindowsParser()
    event = parser.parse(RawLog(raw_event=raw_event, source_hint="windows"))
    
    assert event.event_type == "authentication.login.success"
    assert event.severity == Severity.info
    assert event.actor.username == "msmith"  # type: ignore
    assert event.actor.domain == "CORP_AD"  # type: ignore
    assert event.target.hostname == "WS-INT-04"  # type: ignore
    assert event.metadata["event_id"] == "4624"
    assert event.metadata["process_name"] == "advapi"
    assert len(event.artifacts) == 1
    assert event.artifacts[0].type == ArtifactType.ip
    assert event.artifacts[0].value == "10.1.1.5"

def test_4625_failure_json():
    raw_event = json.dumps({
        "EventID": 4625,
        "TargetUserName": "admin_service",
        "TargetDomainName": "CORP_AD",
        "Computer": "SRV-DB-01",
        "Status": "0xC000006D",
        "TimeCreated": "2026-06-12T09:02:45Z"
    })
    parser = WindowsParser()
    event = parser.parse(RawLog(raw_event=raw_event, source_hint="windows"))
    
    assert event.event_type == "authentication.login.failure"
    assert event.severity == Severity.medium
    assert event.timestamp == "2026-06-12T09:02:45Z"
    assert event.actor.username == "admin_service"  # type: ignore
    assert event.metadata["failure_reason"] == "0xC000006D"

def test_4634_logout():
    raw_event = "EventID: 4634, TargetUserName: msmith"
    parser = WindowsParser()
    event = parser.parse(RawLog(raw_event=raw_event, source_hint="windows"))
    assert event.event_type == "authentication.logout.success"
    
def test_4720_create_user():
    raw_event = "EventID: 4720, TargetUserName: newuser"
    parser = WindowsParser()
    event = parser.parse(RawLog(raw_event=raw_event, source_hint="windows"))
    assert event.event_type == "custom.user.created"
    
def test_4726_delete_user():
    raw_event = "EventID: 4726, TargetUserName: olduser"
    parser = WindowsParser()
    event = parser.parse(RawLog(raw_event=raw_event, source_hint="windows"))
    assert event.event_type == "custom.user.deleted"
    assert event.severity == Severity.medium

def test_unknown_event_id():
    raw_event = json.dumps({
        "EventID": 9999,
        "TimeCreated": "2026-06-12T09:02:45Z"
    })
    parser = WindowsParser()
    event = parser.parse(RawLog(raw_event=raw_event, source_hint="windows"))
    assert event.event_type == "custom.unknown.detected"

def test_malformed_event():
    raw_event = "this is not valid"
    parser = WindowsParser()
    with pytest.raises(ValueError) as exc:
        parser.parse(RawLog(raw_event=raw_event, source_hint="windows"))
    assert "Unsupported Windows log format" in str(exc.value)

def test_missing_username():
    raw_event = json.dumps({
        "EventID": 4624,
        "TimeCreated": "2026-06-12T08:15:30Z"
    })
    parser = WindowsParser()
    event = parser.parse(RawLog(raw_event=raw_event, source_hint="windows"))
    assert event.actor is None

def test_missing_timestamp():
    raw_event = json.dumps({
        "EventID": 4624,
        "TargetUserName": "jdoe"
    })
    parser = WindowsParser()
    event = parser.parse(RawLog(raw_event=raw_event, source_hint="windows"))
    assert event.timestamp is not None
    assert "T" in event.timestamp
    
def test_invalid_timestamp():
    raw_event = json.dumps({
        "EventID": 4624,
        "TimeCreated": "not a real time"
    })
    parser = WindowsParser()
    event = parser.parse(RawLog(raw_event=raw_event, source_hint="windows"))
    assert event.timestamp is not None
    assert "not a real time" not in event.timestamp
    assert "T" in event.timestamp

def test_batch_integration():
    logs = [
        RawLog(raw_event='{"EventID": 4624, "TargetUserName": "u1"}', source_hint="windows"),
        RawLog(raw_event="malformed", source_hint="windows")
    ]
    processor = BatchProcessor()
    result = processor.process(logs)
    
    assert result.total_logs == 2
    assert result.successful_events == 1
    assert result.fallback_events == 1
    assert result.events[0].actor.username == "u1"  # type: ignore
    assert result.events[1].event_type == "custom.parsing.failed"  # type: ignore

def test_fallback_integration():
    raw_event = "malformed"
    parser = WindowsParser()
    event = parser.parse_safe(RawLog(raw_event=raw_event, source_hint="windows"))
    assert event.event_type == "custom.parsing.failed"
