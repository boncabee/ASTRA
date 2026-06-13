class BatchProcessingError(Exception):
    """Base exception for all batch processing errors."""
    pass

class BatchSizeExceededError(BatchProcessingError):
    """Raised when a batch exceeds the maximum allowed size."""
    pass

class InvalidBatchError(BatchProcessingError):
    """Raised when a batch is empty or contains invalid items."""
    pass

class PartialBatchFailureError(BatchProcessingError):
    """Raised when a batch completes but with partial failures that cannot be safely recovered."""
    pass
