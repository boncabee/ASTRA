import logging
from typing import Dict, Any, Tuple

logger = logging.getLogger(__name__)

SUPPORTED_VERSIONS = ["1.0"]
DEPRECATED_FIELDS_BY_VERSION: Dict[str, Dict[str, str]] = {
    # Format: "version": {"field_name": "deprecation_message"}
    "1.0": {}
}

class SchemaVersionError(ValueError):
    pass

def validate_schema_version(version: str) -> bool:
    """Validate if the provided schema version is currently supported."""
    if version not in SUPPORTED_VERSIONS:
        # Prepare future support for CES v2.x
        if version.startswith("2."):
            raise SchemaVersionError(f"CES v{version} is not yet supported. Migration path will be required.")
        raise SchemaVersionError(f"Unsupported schema version: {version}. Supported versions: {SUPPORTED_VERSIONS}")
    return True

def check_deprecated_fields(event_dict: Dict[str, Any], version: str) -> None:
    """Check for deprecated fields and emit warnings."""
    if version in DEPRECATED_FIELDS_BY_VERSION:
        deprecated = DEPRECATED_FIELDS_BY_VERSION[version]
        for field, message in deprecated.items():
            if field in event_dict and event_dict[field] is not None:
                logger.warning(f"Deprecation Warning (v{version}): Field '{field}' is deprecated. {message}")

def migrate_to_latest(event_dict: Dict[str, Any], current_version: str) -> Tuple[Dict[str, Any], str]:
    """
    Compatibility utility to migrate older events to the latest supported schema.
    Returns the migrated event dictionary and the new version string.
    """
    # For now we only support 1.0, so validate it
    if current_version not in SUPPORTED_VERSIONS and not current_version.startswith("1."):
        # This is where future 1.x -> 2.x migration logic will be executed.
        # e.g., if current_version == "1.0": event_dict = _migrate_1_0_to_2_0(event_dict)
        pass
        
    return event_dict, current_version

def _migrate_1_0_to_2_0(event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Internal utility to migrate 1.0 events to 2.0 (stub for future use)."""
    # Example migration logic
    event_dict["schema_version"] = "2.0"
    return event_dict
