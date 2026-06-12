import pytest
from pydantic import ValidationError
from unittest.mock import patch
from typing import Dict, Any
from app.schemas.ces import CESEvent, SourceType, Severity, Entity
from app.core.versioning import SchemaVersionError, migrate_to_latest, DEPRECATED_FIELDS_BY_VERSION

def get_base_payload() -> Dict[str, Any]:
    return {
        "event_id": "uuid-1234",
        "timestamp": "2026-06-12T08:00:00Z",
        "source_type": SourceType.vpn,
        "event_type": "authentication.login.success",
        "severity": Severity.info,
        "actor": Entity(username="jroberts"),
        "raw_event": "raw_log_string_here"
    }

def test_default_schema_version():
    payload = get_base_payload()
    event = CESEvent(**payload)
    assert event.schema_version == "1.0"

def test_valid_schema_version():
    payload = get_base_payload()
    payload["schema_version"] = "1.0"
    event = CESEvent(**payload)
    assert event.schema_version == "1.0"

def test_unsupported_schema_version():
    payload = get_base_payload()
    payload["schema_version"] = "9.9"
    with pytest.raises(ValidationError) as exc_info:
        CESEvent(**payload)
    assert "Unsupported schema version" in str(exc_info.value)

def test_future_schema_version():
    payload = get_base_payload()
    payload["schema_version"] = "2.0"
    with pytest.raises(ValidationError) as exc_info:
        CESEvent(**payload)
    assert "is not yet supported" in str(exc_info.value)

@patch("app.core.versioning.logger")
def test_deprecation_warnings(mock_logger):
    # Temporarily add a deprecated field for testing
    DEPRECATED_FIELDS_BY_VERSION["1.0"] = {"old_field": "Use new_field instead."}
    
    payload = get_base_payload()
    payload["old_field"] = "some_value"
    
    # Validation should pass but logger should be called
    event = CESEvent(**payload)
    assert event.event_id == "uuid-1234"
    mock_logger.warning.assert_called_once()
    assert "old_field" in mock_logger.warning.call_args[0][0]
    
    # Cleanup
    DEPRECATED_FIELDS_BY_VERSION["1.0"] = {}

def test_migrate_to_latest():
    payload = get_base_payload()
    payload["schema_version"] = "1.0"
    
    migrated_payload, new_version = migrate_to_latest(payload, "1.0")
    
    assert new_version == "1.0"
    assert migrated_payload["event_id"] == "uuid-1234"
