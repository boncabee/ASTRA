import pytest
from unittest.mock import patch
from datetime import datetime, timezone
from app.parsers.fallback.fallback_mapper import FallbackMapper
from app.parsers.fallback.fallback_event import ConfidenceLevel, FALLBACK_EVENT_TYPE
from app.parsers.fallback.exceptions import RecoveryFailureError
from app.schemas.ces import SourceType, Severity
from app.schemas.parser import RawLog

def test_handle_unknown_event():
    raw_log = RawLog(raw_event="some random text log", source_hint="windows")
    event = FallbackMapper.handle_unknown_event(raw_log, original_source="windows")
    
    assert event.schema_version == "1.0"
    assert event.source_type == SourceType.windows
    assert event.event_type == FALLBACK_EVENT_TYPE
    assert event.severity == Severity.low
    assert event.raw_event == "some random text log"
    assert event.metadata["fallback_reason"] == "unknown_event"  # type: ignore
    assert event.metadata["confidence_score"] == ConfidenceLevel.LOW.value  # type: ignore
    assert event.metadata["original_source_type"] == "windows"  # type: ignore

def test_handle_unknown_vendor():
    raw_log = RawLog(raw_event="alien vendor log")  # type: ignore
    event = FallbackMapper.handle_unknown_vendor(raw_log, vendor_name="alien_vendor")
    
    assert event.source_type == SourceType.custom
    assert event.event_type == FALLBACK_EVENT_TYPE
    assert event.metadata["fallback_reason"] == "unknown_vendor"  # type: ignore
    assert event.metadata["original_source_type"] == "alien_vendor"  # type: ignore
    assert event.metadata["confidence_score"] == ConfidenceLevel.LOW.value  # type: ignore

def test_handle_parser_failure():
    raw_log = RawLog(raw_event="malformed firewall log")  # type: ignore
    ex = ValueError("regex mismatch")
    event = FallbackMapper.handle_parser_failure(raw_log, exception=ex, original_source="firewall")
    
    assert event.source_type == SourceType.firewall
    assert event.metadata["fallback_reason"] == "parser_failure"  # type: ignore
    assert event.metadata["partial_data"]["error_message"] == "regex mismatch"  # type: ignore
    assert event.metadata["confidence_score"] == ConfidenceLevel.LOW.value  # type: ignore

def test_handle_partial_recovery():
    raw_log = RawLog(raw_event="valid json with missing user")  # type: ignore
    ts = "2026-01-01T12:00:00Z"
    event = FallbackMapper.handle_partial_recovery(
        raw_log, 
        partial_data={"src_ip": "1.1.1.1"}, 
        original_source="vpn", 
        timestamp=ts
    )
    
    assert event.source_type == SourceType.vpn
    assert event.timestamp == ts
    assert event.metadata["fallback_reason"] == "partial_mapping"  # type: ignore
    assert event.metadata["partial_data"]["src_ip"] == "1.1.1.1"  # type: ignore
    assert event.metadata["confidence_score"] == ConfidenceLevel.MEDIUM.value  # type: ignore

def test_invalid_timestamp_fallback():
    raw_log = RawLog(raw_event="log")  # type: ignore
    # Provide an invalid timestamp string
    event = FallbackMapper.handle_partial_recovery(
        raw_log,
        partial_data={},
        original_source="custom",
        timestamp="invalid-time"
    )
    
    # Should fallback to current time, so we just verify it's a valid ISO format
    assert "T" in event.timestamp
    # Should be valid
    try:
        datetime.fromisoformat(event.timestamp.replace("Z", "+00:00"))
        is_valid = True
    except ValueError:
        is_valid = False
    assert is_valid

@patch("app.parsers.fallback.fallback_mapper.uuid.uuid4")
def test_critical_failure_raises_recovery_error(mock_uuid):
    # Make uuid4 raise an exception to simulate a critical error
    mock_uuid.side_effect = Exception("Out of memory")
    raw_log = RawLog(raw_event="log")  # type: ignore
    
    with pytest.raises(RecoveryFailureError) as exc_info:
        FallbackMapper.handle_unknown_event(raw_log, "windows")
    
    assert "Failed to create fallback event" in str(exc_info.value)
    assert "Out of memory" in str(exc_info.value)
