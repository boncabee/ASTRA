from typing import List, Dict, Any
from datetime import datetime, timezone
import time
import json
import logging

from app.schemas.ces import CESEvent
from models.correlation import CorrelationRule, CorrelationMatch
from core.config import settings

# Setup standard logger
logger = logging.getLogger("correlation_engine")
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)

def extract_nested_value(obj: Dict[str, Any], path: str) -> Any:
    parts = path.split('.')
    current = obj
    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        elif hasattr(current, part):
            current = getattr(current, part)
        else:
            return None
    return current

def evaluate_condition(event: CESEvent, condition_key: str, expected_val: Any) -> bool:
    event_dict = event.model_dump()
    val = extract_nested_value(event_dict, condition_key)
    return val == expected_val

def run_correlation_cycle(events: List[CESEvent], rules: List[CorrelationRule], run_by_user_id: str) -> List[CorrelationMatch]:
    start_time = time.perf_counter()
    matches_generated = []
    
    for rule in rules:
        if not rule.enabled:
            continue
            
        rule_events = [e for e in events if e.event_type in rule.event_types]
        if not rule_events:
            continue
            
        # Tumbling window bucketing
        buckets: Dict[int, List[CESEvent]] = {}
        for event in rule_events:
            dt = datetime.fromisoformat(event.timestamp.replace('Z', '+00:00'))
            epoch = int(dt.timestamp())
            bucket_id = epoch // rule.time_window
            if bucket_id not in buckets:
                buckets[bucket_id] = []
            buckets[bucket_id].append(event)
            
        threshold = rule.conditions.get("threshold", 1)
        
        for bucket_id, bucket_events in buckets.items():
            valid_events = []
            for event in bucket_events:
                match_all = True
                for k, v in rule.conditions.items():
                    if k == "threshold":
                        continue
                    if not evaluate_condition(event, k, v):
                        match_all = False
                        break
                if match_all:
                    valid_events.append(event)
            
            if len(valid_events) >= threshold:
                ips = set()
                users = set()
                for e in valid_events:
                    if e.actor and getattr(e.actor, 'ip', None):
                        ips.add(e.actor.ip)
                    if e.actor and getattr(e.actor, 'username', None):
                        users.add(e.actor.username)
                        
                context = {"ips": list(ips), "users": list(users)}
                
                # Deterministic Scoring
                score = rule.severity_weight + (len(valid_events) * settings.CORRELATION_SCORE_MULTIPLIER)
                score = min(score, settings.CORRELATION_SCORE_MAX)
                
                bucket_timestamp = datetime.fromtimestamp(bucket_id * rule.time_window, tz=timezone.utc)
                
                match = CorrelationMatch(
                    rule_id=rule.id,
                    matched_events=[e.event_id for e in valid_events],
                    event_count=len(valid_events),
                    match_timestamp=bucket_timestamp,
                    correlation_score=score,
                    context=context,
                    created_by=run_by_user_id,
                    updated_by=run_by_user_id
                )
                matches_generated.append(match)
                
    end_time = time.perf_counter()
    duration_ms = (end_time - start_time) * 1000
    
    metrics = {
        "event": "correlation_cycle_metrics",
        "events_processed": len(events),
        "rules_evaluated": len(rules),
        "matches_generated": len(matches_generated),
        "evaluation_duration_ms": duration_ms
    }
    logger.info(json.dumps(metrics))
    
    return matches_generated
