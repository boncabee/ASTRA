import pytest
from app.transformers.base import BaseTransformer
from app.transformers.exceptions import TransformationError, EventValidationError
from app.schemas.ces import SourceType, Severity, ArtifactType, Entity, Artifact

class ValidDummyTransformer(BaseTransformer):
    def parse(self, raw_event):
        return {
            "event_id": "uuid-1234",
            "timestamp": "2026-06-12T08:00:00Z",
            "source_type": SourceType.vpn,
            "event_type": "authentication.login.success",
            "severity": Severity.info,
            "actor": Entity(username="jroberts"),
            "raw_event": str(raw_event)
        }

class InvalidDummyTransformer(BaseTransformer):
    def parse(self, raw_event):
        return {
            "event_id": "uuid-1234",
            "timestamp": "bad-date",
            "source_type": SourceType.vpn,
            "event_type": "nonsense",
            "severity": Severity.info,
            "actor": Entity(username="jroberts"),
            "raw_event": str(raw_event)
        }

class CrashingTransformer(BaseTransformer):
    def parse(self, raw_event):
        raise ValueError("Unexpected parsing issue")

class ExplicitErrorTransformer(BaseTransformer):
    def parse(self, raw_event):
        raise TransformationError("Explicit error", raw_event=raw_event)

def test_valid_transform():
    t = ValidDummyTransformer()
    event = t.transform("some_raw_log")
    assert event.event_id == "uuid-1234"
    assert event.raw_event == "some_raw_log"

def test_invalid_transform():
    t = InvalidDummyTransformer()
    with pytest.raises(EventValidationError):
        t.transform("some_raw_log")

def test_crashing_transform():
    t = CrashingTransformer()
    with pytest.raises(TransformationError) as exc:
        t.transform("some_raw_log")
    assert "Unexpected parsing issue" in str(exc.value)

def test_explicit_error_transform():
    t = ExplicitErrorTransformer()
    with pytest.raises(TransformationError) as exc:
        t.transform("some_raw_log")
    assert "Explicit error" in str(exc.value)
