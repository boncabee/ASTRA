import pytest
import uuid
from datetime import datetime, timezone, timedelta
import json
import logging

from app.schemas.ces import CESEvent, SourceType, Severity, Entity, EventCategory
from models.correlation import CorrelationRule, CorrelationMatch
from services.correlation import run_correlation_cycle

def create_mock_event(event_type: str, timestamp: str, actor_username: str | None = None) -> CESEvent:
    actor = None
    if actor_username:
        actor = Entity(username=actor_username)
    return CESEvent(
        schema_version="1.0",
        event_id=str(uuid.uuid4()),
        timestamp=timestamp,
        source_type=SourceType.custom,
        event_type=event_type,
        severity=Severity.info,
        actor=actor,
        raw_event="mock event"
    )

def test_run_correlation_cycle_match(caplog):
    caplog.set_level(logging.INFO)
    
    # Create rule
    rule = CorrelationRule(
        id=uuid.uuid4(),
        name="Failed Login Burst",
        description="5 failed logins in 5 minutes",
        enabled=True,
        event_types=["authentication.failed.login"],
        conditions={"threshold": 5, "actor.username": "admin"},
        time_window=300,
        severity_weight=50
    )
    
    # Create events (all within the same 300s window)
    base_time = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    events = []
    for i in range(5):
        t = (base_time + timedelta(seconds=i)).isoformat()
        events.append(create_mock_event("authentication.failed.login", t, "admin"))
        
    # Run cycle
    matches = run_correlation_cycle(events, [rule], str(uuid.uuid4()))
    
    assert len(matches) == 1
    match = matches[0]
    assert match.rule_id == rule.id
    assert match.event_count == 5
    assert len(match.matched_events) == 5
    assert match.correlation_score == 50 + (5 * 5) # 75
    assert "admin" in match.context["users"]
    
    # Verify metrics logged
    log_messages = [r.message for r in caplog.records if "correlation_cycle_metrics" in r.message]
    assert len(log_messages) == 1
    metrics = json.loads(log_messages[0])
    assert metrics["matches_generated"] == 1
    assert metrics["events_processed"] == 5

def test_run_correlation_cycle_no_match():
    rule = CorrelationRule(
        id=uuid.uuid4(),
        name="Failed Login Burst",
        description="5 failed logins in 5 minutes",
        enabled=True,
        event_types=["authentication.failed.login"],
        conditions={"threshold": 5, "actor.username": "admin"},
        time_window=300,
        severity_weight=50
    )
    
    # Only 4 events, below threshold of 5
    base_time = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    events = []
    for i in range(4):
        t = (base_time + timedelta(seconds=i)).isoformat()
        events.append(create_mock_event("authentication.failed.login", t, "admin"))
        
    matches = run_correlation_cycle(events, [rule], str(uuid.uuid4()))
    assert len(matches) == 0

def test_run_correlation_cycle_disabled_rule():
    rule = CorrelationRule(
        id=uuid.uuid4(),
        name="Disabled Rule",
        description="test",
        enabled=False,
        event_types=["test.event.trigger"],
        conditions={"threshold": 1},
        time_window=300,
        severity_weight=50
    )
    # create generic event bypasses pydantic EventCategory validation, need valid one.
    events = [create_mock_event("custom.event.trigger", datetime.now(timezone.utc).isoformat())]
    matches = run_correlation_cycle(events, [rule], str(uuid.uuid4()))
    assert len(matches) == 0

def test_correlation_performance_benchmark():
    # Target: 10,000 events/minute -> Process 10,000 events against 5 rules quickly.
    events = []
    base_time = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    for i in range(10000):
        t = (base_time + timedelta(seconds=i%300)).isoformat()
        events.append(create_mock_event("custom.connection.accepted", t, f"user_{i%100}"))
        
    rules = [
        CorrelationRule(
            id=uuid.uuid4(),
            name=f"Rule {i}",
            description="test",
            enabled=True,
            event_types=["custom.connection.accepted"],
            conditions={"threshold": 100},
            time_window=300,
            severity_weight=10
        ) for i in range(5)
    ]
    
    import time
    start = time.perf_counter()
    matches = run_correlation_cycle(events, rules, str(uuid.uuid4()))
    end = time.perf_counter()
    
    duration = end - start
    assert duration < 5.0 # Ensure MVP processing is reasonably fast
    assert len(matches) > 0
