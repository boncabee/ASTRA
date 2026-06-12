import pytest
import json
from pydantic import ValidationError

from app.parsers.base.transformer_config import (
    TransformerConfig,
    ConfigurationError,
    InvalidMappingError,
    InvalidSourceTypeError
)

@pytest.fixture
def valid_config_dict():
    return {
        "config_name": "Test Config",
        "config_version": "1.0",
        "description": "A test configuration",
        "parser_name": "TestParser",
        "source_type": "vpn",
        "enabled": True,
        "field_mappings": {
            "username": "user",
            "src_ip": "source_ip",
            "dest_ip": "destination_ip"
        },
        "event_mappings": {
            "LOGIN_SUCCESS": "authentication.login.success",
            "LOGIN_FAILED": "authentication.login.failure"
        },
        "timezone": "UTC",
        "timestamp_field": "time",
        "timestamp_format": "%Y-%m-%dT%H:%M:%S",
        "unknown_event_type": "custom.unknown",
        "unknown_source_type": "custom",
        "fallback_enabled": True,
        "strict_mode": False,
        "allow_unknown_fields": True,
        "batch_size": 1000,
        "max_event_size": 1048576
    }

def test_load_from_dict_valid(valid_config_dict):
    config = TransformerConfig.load_from_dict(valid_config_dict)
    assert config.config_name == "Test Config"
    assert config.source_type == "vpn"
    assert len(config.field_mappings) == 3
    assert config.field_mappings["username"] == "user"

def test_load_from_json_valid(valid_config_dict):
    json_str = json.dumps(valid_config_dict)
    config = TransformerConfig.load_from_json(json_str)
    assert config.config_name == "Test Config"
    assert config.source_type == "vpn"
    assert len(config.event_mappings) == 2

def test_missing_required_fields(valid_config_dict):
    del valid_config_dict["config_name"]
    with pytest.raises(ConfigurationError) as exc_info:
        TransformerConfig.load_from_dict(valid_config_dict)
    assert "config_name" in str(exc_info.value)

def test_invalid_json():
    with pytest.raises(ConfigurationError) as exc_info:
        TransformerConfig.load_from_json("{ invalid json ")
    assert "Invalid JSON" in str(exc_info.value)

def test_invalid_source_type(valid_config_dict):
    valid_config_dict["source_type"] = "invalid_source_123"
    with pytest.raises(InvalidSourceTypeError) as exc_info:
        TransformerConfig.load_from_dict(valid_config_dict)
    assert "invalid_source_123" in str(exc_info.value)

def test_invalid_field_mapping_empty_key(valid_config_dict):
    valid_config_dict["field_mappings"][""] = "value"
    with pytest.raises(InvalidMappingError) as exc_info:
        TransformerConfig.load_from_dict(valid_config_dict)
    assert "keys and values must not be empty" in str(exc_info.value)

def test_invalid_field_mapping_empty_value(valid_config_dict):
    valid_config_dict["field_mappings"]["key"] = "   "
    with pytest.raises(InvalidMappingError) as exc_info:
        TransformerConfig.load_from_dict(valid_config_dict)
    assert "keys and values must not be empty" in str(exc_info.value)

def test_invalid_event_mapping_empty_key(valid_config_dict):
    valid_config_dict["event_mappings"][""] = "value"
    with pytest.raises(InvalidMappingError) as exc_info:
        TransformerConfig.load_from_dict(valid_config_dict)
    assert "keys and values must not be empty" in str(exc_info.value)

def test_invalid_event_mapping_empty_value(valid_config_dict):
    valid_config_dict["event_mappings"]["key"] = "   "
    with pytest.raises(InvalidMappingError) as exc_info:
        TransformerConfig.load_from_dict(valid_config_dict)
    assert "keys and values must not be empty" in str(exc_info.value)

def test_defaults_applied(valid_config_dict):
    # Remove optional fields with defaults
    del valid_config_dict["timezone"]
    del valid_config_dict["fallback_enabled"]
    del valid_config_dict["strict_mode"]
    
    config = TransformerConfig.load_from_dict(valid_config_dict)
    assert config.timezone == "UTC"
    assert config.fallback_enabled is True
    assert config.strict_mode is False
    assert config.batch_size == 1000
    assert config.max_event_size == 1048576

def test_fallback_behavior_validation(valid_config_dict):
    valid_config_dict["fallback_enabled"] = False
    valid_config_dict["strict_mode"] = True
    config = TransformerConfig.load_from_dict(valid_config_dict)
    assert config.fallback_enabled is False
    assert config.strict_mode is True

