import pytest
from pydantic import ValidationError
from typing import Dict, Any
from app.schemas.ces import CESEvent, Entity, Artifact, MAX_RAW_EVENT_SIZE, SourceType, Severity, ArtifactType

def get_valid_payload() -> Dict[str, Any]:
    return {
        "event_id": "uuid-1234",
        "timestamp": "2026-06-12T08:00:00Z",
        "source_type": SourceType.vpn,
        "event_type": "authentication.login.success",
        "severity": Severity.info,
        "actor": Entity(username="jsmith", ip="203.0.113.5"),
        "target": Entity(hostname="vpn.corp.local"),
        "artifacts": [Artifact(type=ArtifactType.ip, value="203.0.113.5")],
        "raw_event": "raw_log_string_here",
        "metadata": {"vpn_group": "Engineering"}
    }

def test_valid_ces_event():
    payload = get_valid_payload()
    event = CESEvent(**payload)
    assert event.event_id == "uuid-1234"
    assert event.timestamp == "2026-06-12T08:00:00Z"
    assert event.event_type == "authentication.login.success"
    assert event.severity == Severity.info
    assert event.actor is not None and event.actor.username == "jsmith"
    assert event.actor is not None and event.actor.ip == "203.0.113.5"
    assert event.artifacts[0].type == ArtifactType.ip

def test_missing_mandatory_fields():
    payload = get_valid_payload()
    del payload["event_id"]
    with pytest.raises(ValidationError) as exc_info:
        CESEvent(**payload)
    assert "event_id" in str(exc_info.value)

def test_invalid_timestamp():
    payload = get_valid_payload()
    payload["timestamp"] = "not-a-timestamp"
    with pytest.raises(ValidationError) as exc_info:
        CESEvent(**payload)
    assert "timestamp must be a valid ISO-8601 format string" in str(exc_info.value)

def test_invalid_event_taxonomy():
    payload = get_valid_payload()
    payload["event_type"] = "invalid_taxonomy"
    with pytest.raises(ValidationError) as exc_info:
        CESEvent(**payload)
    assert "event_type must follow category.action.outcome taxonomy" in str(exc_info.value)

def test_invalid_event_category():
    payload = get_valid_payload()
    payload["event_type"] = "nonsense.action.success"
    with pytest.raises(ValidationError) as exc_info:
        CESEvent(**payload)
    assert "event_type category 'nonsense' is invalid" in str(exc_info.value)

def test_invalid_severity():
    payload = get_valid_payload()
    payload["severity"] = "super-critical"
    with pytest.raises(ValidationError) as exc_info:
        CESEvent(**payload)
    assert "Input should be" in str(exc_info.value)

def test_missing_severity():
    payload = get_valid_payload()
    del payload["severity"]
    with pytest.raises(ValidationError) as exc_info:
        CESEvent(**payload)
    assert "severity\n  Field required" in str(exc_info.value)

def test_severity_case_insensitivity():
    payload = get_valid_payload()
    payload["severity"] = "HIGH"
    event = CESEvent(**payload)
    assert event.severity == Severity.high

def test_invalid_artifact_type():
    payload = get_valid_payload()
    payload["artifacts"] = [{"type": "bad_type", "value": "123"}]
    with pytest.raises(ValidationError) as exc_info:
        CESEvent(**payload)
    assert "Input should be" in str(exc_info.value)

def test_invalid_source_type():
    payload = get_valid_payload()
    payload["source_type"] = "nonsense_firewall"
    with pytest.raises(ValidationError) as exc_info:
        CESEvent(**payload)
    assert "Input should be" in str(exc_info.value)

def test_empty_entity():
    payload = get_valid_payload()
    payload["actor"] = {}
    with pytest.raises(ValidationError) as exc_info:
        CESEvent(**payload)
    assert "Entity must contain at least one identifying field" in str(exc_info.value)

def test_oversized_raw_event():
    payload = get_valid_payload()
    payload["raw_event"] = "a" * (MAX_RAW_EVENT_SIZE + 1)
    with pytest.raises(ValidationError) as exc_info:
        CESEvent(**payload)
    assert "String should have at most 65536 characters" in str(exc_info.value)
