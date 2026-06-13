import time
import logging
from typing import List

from app.schemas.parser import RawLog
from app.parsers.registry.registry import registry
from app.parsers.fallback.fallback_mapper import FallbackMapper
from app.parsers.batch.batch_result import BatchResult
from app.parsers.batch.exceptions import BatchSizeExceededError, InvalidBatchError

logger = logging.getLogger(__name__)

class BatchProcessor:
    """
    Standardized batch processing framework.
    Transforms multiple raw logs into validated CESEvents efficiently and consistently.
    """
    def __init__(self, max_batch_size: int = 10000):
        self.max_batch_size = max_batch_size

    def process(self, logs: List[RawLog]) -> BatchResult:
        """
        Processes a list of RawLogs into a BatchResult containing CESEvents.
        Preserves order deterministically.
        Handles partial failures seamlessly.
        """
        if not logs:
            raise InvalidBatchError("Batch cannot be empty.")
            
        if len(logs) > self.max_batch_size:
            raise BatchSizeExceededError(f"Batch size {len(logs)} exceeds maximum allowed {self.max_batch_size}.")

        start_time = time.time()
        
        result = BatchResult(total_logs=len(logs))
        
        for index, log in enumerate(logs):
            try:
                if not isinstance(log, RawLog):
                    raise ValueError(f"Invalid item in batch at index {index}. Expected RawLog.")

                source_hint = log.source_hint
                
                if not source_hint:
                    event = FallbackMapper.handle_unknown_event(log, original_source="unknown")
                    result.events.append(event)
                    result.fallback_events += 1
                    continue
                    
                if registry.has_parser(source_hint):
                    parser_class = registry.get_parser(source_hint)
                    parser = parser_class() # Instantiate parser
                    event = parser.parse_safe(log)
                    
                    if event.event_type == "custom.parsing.failed" or event.event_type == "custom.unknown.detected":
                        result.fallback_events += 1
                    else:
                        result.successful_events += 1
                        
                    result.events.append(event)
                else:
                    event = FallbackMapper.handle_unknown_vendor(log, vendor_name=source_hint)
                    result.events.append(event)
                    result.fallback_events += 1
                    
            except Exception as e:
                # Catastrophic failure for this specific log
                logger.error(f"Catastrophic failure processing log at index {index}: {str(e)}")
                result.failed_events += 1
                result.events.append(None) # Preserve order with None
                result.errors.append({
                    "index": index,
                    "error": str(e),
                    "raw_event_preview": log.raw_event[:100] if isinstance(log, RawLog) else "invalid type"
                })

        end_time = time.time()
        result.processing_time_ms = round((end_time - start_time) * 1000, 2)
        
        return result
