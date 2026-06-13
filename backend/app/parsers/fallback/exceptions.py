class FallbackMappingError(Exception):
    """Base exception for all fallback mapping errors."""
    pass

class UnknownVendorError(FallbackMappingError):
    """Raised when the vendor is not registered or recognized."""
    pass

class UnsupportedEventError(FallbackMappingError):
    """Raised when the event format is unsupported."""
    pass

class RecoveryFailureError(FallbackMappingError):
    """Raised when fallback mapping fails to recover the event safely."""
    pass
