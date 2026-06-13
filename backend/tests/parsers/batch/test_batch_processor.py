import pytest
from unittest.mock import patch, MagicMock

from app.schemas.parser import RawLog
from app.schemas.ces import CESEvent, SourceType, Severity
from app.parsers.base.base_parser import BaseParser
from app.parsers.registry.registry import registry
from app.parsers.batch.batch_processor import BatchProcessor
from app.parsers.batch.batch_result import BatchResult
from app.parsers.batch.exceptions import BatchSizeExceededError, InvalidBatchError
from app.parsers.fallback.fallback_event import FALLBACK_EVENT_TYPE

class MockParser(BaseParser):
    def parse(self, raw_log: RawLog) -> CESEvent:
        if raw_log.raw_event == "malformed":
            raise ValueError("Bad log")
        
        return CESEvent(
            schema_version="1.0",
            event_id="1234",
            timestamp="2026-01-01T12:00:00Z",
            source_type=SourceType.custom,
            event_type="custom.action.success",
            severity=Severity.info,
            raw_event=raw_log.raw_event,
            metadata={}
        )

@pytest.fixture(autouse=True)
def setup_registry():
    registry.clear()
    registry.register_parser("mock", MockParser)
    yield
    registry.clear()

def test_successful_batch_processing():
    processor = BatchProcessor()
    logs = [
        RawLog(raw_event="log 1", source_hint="mock"),
        RawLog(raw_event="log 2", source_hint="mock")
    ]
    
    result = processor.process(logs)
    
    assert result.total_logs == 2
    assert result.successful_events == 2
    assert result.failed_events == 0
    assert result.fallback_events == 0
    assert result.success_rate == 100.0
    assert result.failure_rate == 0.0
    assert result.fallback_rate == 0.0
    assert len(result.events) == 2
    assert result.events[0].raw_event == "log 1"  # type: ignore
    assert result.events[1].raw_event == "log 2"  # type: ignore
    assert result.events[0].event_type == "custom.action.success"  # type: ignore

def test_order_preservation_and_partial_failure():
    processor = BatchProcessor()
    logs = [
        RawLog(raw_event="log 1", source_hint="mock"),
        RawLog(raw_event="malformed", source_hint="mock"),
        RawLog(raw_event="log 3", source_hint="mock")
    ]
    
    result = processor.process(logs)
    
    assert result.total_logs == 3
    assert result.successful_events == 2
    assert result.fallback_events == 1
    assert result.failed_events == 0
    assert len(result.events) == 3
    assert result.events[0].raw_event == "log 1"  # type: ignore
    assert result.events[1].raw_event == "malformed"  # type: ignore
    assert result.events[1].event_type == "custom.parsing.failed" # Wait, BaseParser uses this  # type: ignore
    assert result.events[2].raw_event == "log 3"  # type: ignore

def test_fallback_integration():
    processor = BatchProcessor()
    logs = [
        RawLog(raw_event="unknown vendor log", source_hint="unknown_vendor"),
        RawLog(raw_event="no source hint log", source_hint=None)
    ]
    
    result = processor.process(logs)
    
    assert result.total_logs == 2
    assert result.successful_events == 0
    assert result.fallback_events == 2
    assert len(result.events) == 2
    assert result.events[0].event_type == FALLBACK_EVENT_TYPE  # type: ignore
    assert result.events[0].metadata["fallback_reason"] == "unknown_vendor"  # type: ignore
    assert result.events[1].event_type == FALLBACK_EVENT_TYPE  # type: ignore
    assert result.events[1].metadata["fallback_reason"] == "unknown_event"  # type: ignore

def test_invalid_batch_size():
    processor = BatchProcessor(max_batch_size=2)
    logs = [
        RawLog(raw_event="log 1"),  # type: ignore
        RawLog(raw_event="log 2"),  # type: ignore
        RawLog(raw_event="log 3")  # type: ignore
    ]
    
    with pytest.raises(BatchSizeExceededError):
        processor.process(logs)

def test_empty_batch():
    processor = BatchProcessor()
    
    with pytest.raises(InvalidBatchError):
        processor.process([])

def test_invalid_input_items():
    processor = BatchProcessor()
    logs = [
        RawLog(raw_event="valid"),  # type: ignore
        "invalid_string_instead_of_rawlog"
    ]
    
    result = processor.process(logs)
    
    assert result.total_logs == 2
    assert result.successful_events == 0
    assert result.fallback_events == 1
    assert result.failed_events == 1
    assert result.events[0].event_type == FALLBACK_EVENT_TYPE # No source hint  # type: ignore
    assert result.events[1] is None
    assert len(result.errors) == 1
    assert "Expected RawLog" in result.errors[0]["error"]

def test_batch_result_metrics_zero_logs():
    result = BatchResult()
    assert result.success_rate == 0.0
    assert result.failure_rate == 0.0
    assert result.fallback_rate == 0.0
