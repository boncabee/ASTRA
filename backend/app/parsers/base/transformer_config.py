import json
from typing import Dict, Optional, Any
from pydantic import BaseModel, Field, model_validator

from app.schemas.ces import SourceType

class ConfigurationError(Exception):
    """Base exception for configuration errors."""
    pass

class InvalidMappingError(ConfigurationError):
    """Exception raised for invalid field or event mappings."""
    pass

class InvalidSourceTypeError(ConfigurationError):
    """Exception raised for invalid or unsupported source types."""
    pass


class TransformerConfig(BaseModel):
    """
    Standardized configuration framework for parsers.
    Allows loading mappings, transformation rules, and runtime settings
    without hardcoded values.
    """
    # 1. Metadata
    config_name: str = Field(..., description="Name of the configuration")
    config_version: str = Field(..., description="Version of the configuration")
    description: Optional[str] = Field(None, description="Optional description of the config")

    # 2. Parser Identification
    parser_name: str = Field(..., description="Name of the parser this config applies to")
    source_type: str = Field(..., description="The source type (e.g. vpn, windows)")
    enabled: bool = Field(True, description="Whether this parser/config is enabled")

    # 3. Field Mapping
    field_mappings: Dict[str, str] = Field(default_factory=dict, description="Maps raw log fields to CES fields")

    # 4. Event Mapping
    event_mappings: Dict[str, str] = Field(default_factory=dict, description="Maps raw events to CES taxonomy events")

    # 5. Time Handling
    timezone: str = Field("UTC", description="Default timezone if not present in the log")
    timestamp_field: Optional[str] = Field(None, description="Field containing the timestamp")
    timestamp_format: Optional[str] = Field(None, description="Format string to parse the timestamp")

    # 6. Fallback Strategy
    unknown_event_type: str = Field("custom.unknown", description="Default event type if mapping fails")
    unknown_source_type: str = Field("custom", description="Default source type if mapping fails")
    fallback_enabled: bool = Field(True, description="Whether to emit fallback events on failure")

    # 7. Validation Controls
    strict_mode: bool = Field(False, description="If True, missing mappings raise errors instead of falling back")
    allow_unknown_fields: bool = Field(True, description="If True, unmapped fields are included in extra/metadata")

    # 8. Runtime Controls
    batch_size: int = Field(1000, description="Number of events to process in a batch")
    max_event_size: int = Field(1048576, description="Maximum size of a raw event in bytes (default 1MB)")

    @model_validator(mode='after')
    def validate_mappings_and_types(self) -> 'TransformerConfig':
        # Validate SourceType
        try:
            SourceType(self.source_type)
        except ValueError:
            valid_sources = [st.value for st in SourceType]
            raise InvalidSourceTypeError(f"Invalid source_type: '{self.source_type}'. Must be one of {valid_sources}.")

        # Validate mappings
        for k, v in self.field_mappings.items():
            if not k.strip() or not v.strip():
                raise InvalidMappingError("Field mapping keys and values must not be empty.")

        for k, v in self.event_mappings.items():
            if not k.strip() or not v.strip():
                raise InvalidMappingError("Event mapping keys and values must not be empty.")

        return self

    @classmethod
    def load_from_dict(cls, data: Dict[str, Any]) -> "TransformerConfig":
        """
        Loads the configuration from a dictionary.
        """
        try:
            return cls(**data)
        except Exception as e:
            if isinstance(e, ConfigurationError):
                raise
            raise ConfigurationError(f"Failed to load configuration from dict: {str(e)}")

    @classmethod
    def load_from_json(cls, json_str: str) -> "TransformerConfig":
        """
        Loads the configuration from a JSON string.
        """
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Invalid JSON provided: {str(e)}")

        return cls.load_from_dict(data)

