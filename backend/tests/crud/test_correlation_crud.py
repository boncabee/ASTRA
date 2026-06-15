import pytest
import pytest_asyncio
import uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import inspect, text

from core.database import Base
from crud.crud_correlation import correlation_crud
from models.correlation import CorrelationRule, CorrelationMatch

@pytest_asyncio.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with SessionLocal() as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.mark.asyncio
async def test_create_and_get_rule(db_session):
    obj_in = {
        "name": "Test Rule",
        "description": "Desc",
        "enabled": True,
        "event_types": ["auth.failed"],
        "conditions": {"threshold": 5},
        "time_window": 300,
        "severity_weight": 50
    }
    
    rule = await correlation_crud.create_rule(db_session, obj_in=obj_in)
    assert rule.id is not None
    assert rule.name == "Test Rule"
    assert rule.created_at is not None
    
    fetched = await correlation_crud.get_rule(db_session, rule.id)
    assert fetched is not None
    assert fetched.name == "Test Rule"

@pytest.mark.asyncio
async def test_update_rule(db_session):
    obj_in = {
        "name": "Update Rule",
        "description": "Desc",
        "enabled": True,
        "event_types": ["auth.failed"],
        "conditions": {"threshold": 5},
        "time_window": 300,
        "severity_weight": 50
    }
    rule = await correlation_crud.create_rule(db_session, obj_in=obj_in)
    
    updated = await correlation_crud.update_rule(db_session, db_obj=rule, obj_in={"enabled": False, "severity_weight": 90})
    assert updated.enabled is False
    assert updated.severity_weight == 90

@pytest.mark.asyncio
async def test_create_and_get_matches(db_session):
    rule = await correlation_crud.create_rule(db_session, obj_in={
        "name": "Match Rule",
        "description": "Desc",
        "enabled": True,
        "event_types": ["auth.failed"],
        "conditions": {"threshold": 5},
        "time_window": 300,
        "severity_weight": 50
    })
    
    now = datetime.now(timezone.utc)
    match_in = {
        "rule_id": rule.id,
        "matched_events": [str(uuid.uuid4())],
        "event_count": 1,
        "match_timestamp": now,
        "correlation_score": 75,
        "context": {"user": "test"},
        "expires_at": now + timedelta(days=30)
    }
    match = await correlation_crud.create_match(db_session, obj_in=match_in)
    assert match.id is not None
    assert match.expires_at is not None
    
    # query matches
    matches = await correlation_crud.get_matches(db_session, rule_id=rule.id, min_score=70)
    assert len(matches) == 1
    assert matches[0].correlation_score == 75
    
    # check filters
    matches_empty = await correlation_crud.get_matches(db_session, rule_id=rule.id, min_score=80)
    assert len(matches_empty) == 0

@pytest.mark.asyncio
async def test_schema_indexes(db_session):
    # Verify indexes exist in sqlite metadata
    result = await db_session.execute(text("PRAGMA index_list('correlation_matches');"))
    indexes = result.fetchall()
    index_names = [i[1] for i in indexes]
    
    # SQLite creates indexes. Check for our explicitly named ones or standard ones
    assert any("ix_correlation_matches_correlation_score" in name for name in index_names)
    assert any("ix_correlation_matches_created_at" in name for name in index_names)
    assert any("ix_correlation_matches_match_timestamp" in name for name in index_names)
    assert any("ix_correlation_matches_rule_id" in name for name in index_names)

@pytest.mark.asyncio
async def test_performance_benchmark(db_session):
    rule = await correlation_crud.create_rule(db_session, obj_in={
        "name": "Perf Rule",
        "description": "Desc",
        "enabled": True,
        "event_types": ["auth.failed"],
        "conditions": {"threshold": 5},
        "time_window": 300,
        "severity_weight": 50
    })
    
    now = datetime.now(timezone.utc)
    # Insert 10,000 matches
    matches = []
    for i in range(10000):
        matches.append(CorrelationMatch(
            rule_id=rule.id,
            matched_events=[str(uuid.uuid4())],
            event_count=5,
            match_timestamp=now,
            correlation_score=50,
            context={}
        ))
    
    db_session.add_all(matches)
    await db_session.commit()
    
    import time
    start = time.perf_counter()
    # Find all matches for this rule
    res = await correlation_crud.get_matches(db_session, rule_id=rule.id, start_time=now - timedelta(days=1), limit=10000)
    end = time.perf_counter()
    
    assert len(res) == 10000
    assert (end - start) < 1.0 # Should be very fast with indexes
