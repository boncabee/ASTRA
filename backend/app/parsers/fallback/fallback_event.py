from enum import Enum

class ConfidenceLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

FALLBACK_EVENT_TYPE = "custom.unknown.detected"
