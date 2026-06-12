from typing import Any, Optional

class TransformationError(Exception):
    """Base exception for all transformation errors."""
    def __init__(self, message: str, raw_event: Optional[Any] = None):
        super().__init__(message)
        self.raw_event = raw_event

class EventValidationError(TransformationError):
    """Raised when the transformed event fails CES validation."""
    pass

class ParsingError(TransformationError):
    """Raised when a transformer cannot structurally parse the raw event."""
    pass
