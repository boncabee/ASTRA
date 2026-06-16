from core.config import settings
import pytest
import pytest_asyncio
import uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import inspect, text

from core.database import Base
from models.policy import Policy, PolicyEvaluation
from models.observation import PolicyAction
from schemas.policy import PolicyCreate
from repositories.policy import PolicyRepository

@pytest_asyncio.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine(settings.TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with SessionLocal() as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.mark.asyncio
async def test_create_and_get_policy(db_session):
    repo = PolicyRepository(db_session)
    obj_in = PolicyCreate(
        name="Test Policy",
        description="Desc",
        action=PolicyAction.NOTIFY,
        priority=100,
        is_active=True,
        condition_risk_min=50
    )
    
    policy = await repo.create(obj_in, "system")
    assert policy.id is not None
    assert policy.name == "Test Policy"
    assert policy.created_at is not None
    assert policy.condition_risk_min == 50
    
    fetched = await repo.get_by_id(policy.id)
    assert fetched is not None
    assert fetched.name == "Test Policy"

@pytest.mark.asyncio
async def test_update_policy(db_session):
    repo = PolicyRepository(db_session)
    obj_in = PolicyCreate(
        name="Update Policy",
        description="Desc",
        action=PolicyAction.OBSERVE,
        priority=100,
        is_active=True
    )
    policy = await repo.create(obj_in, "system")
    
    policy.action = PolicyAction.REVIEW_REQUIRED
    policy.priority = 200
    
    updated = await repo.update(policy)
    assert updated.action == PolicyAction.REVIEW_REQUIRED
    assert updated.priority == 200

@pytest.mark.asyncio
async def test_get_active_policies(db_session):
    repo = PolicyRepository(db_session)
    
    await repo.create(PolicyCreate(name="P1", description="D", action=PolicyAction.OBSERVE, priority=10, is_active=True), "sys")
    await repo.create(PolicyCreate(name="P2", description="D", action=PolicyAction.OBSERVE, priority=20, is_active=True), "sys")
    await repo.create(PolicyCreate(name="P3", description="D", action=PolicyAction.OBSERVE, priority=30, is_active=False), "sys")
    
    active_policies = await repo.get_active_policies()
    assert len(active_policies) >= 2
    
    # Should be ordered by priority DESC
    names = [p.name for p in active_policies if p.name in ("P1", "P2", "P3")]
    assert names == ["P2", "P1"]

from models.observation import Observation, ObservationStatus
from models.correlation import CorrelationRule, CorrelationMatch

async def make_observation(db_session):
    rule = CorrelationRule(
        name=f"Rule {uuid.uuid4()}",
        description="Test Desc",
        event_types=["test.event"],
        conditions={},
        time_window=60,
        severity_weight=50
    )
    db_session.add(rule)
    await db_session.flush()

    match = CorrelationMatch(
        rule_id=rule.id,
        matched_events=["test-event-uuid"],
        event_count=1,
        match_timestamp=datetime.now(timezone.utc),
        correlation_score=50,
        context={}
    )
    db_session.add(match)
    await db_session.flush()

    obs = Observation(
        id=uuid.uuid4(),
        title="Test Obs",
        description="Desc",
        correlation_id=match.id,
        classification="Anomaly",
        status=ObservationStatus.NEW,
        risk_score=50,
        evidence_count=1
    )
    db_session.add(obs)
    await db_session.commit()
    await db_session.refresh(obs)
    return obs

@pytest.mark.asyncio
async def test_record_evaluation(db_session):
    repo = PolicyRepository(db_session)
    obs = await make_observation(db_session)
    
    eval_in = PolicyEvaluation(
        observation_id=obs.id,
        decision_reason="Test reason",
        action=PolicyAction.NOTIFY
    )
    
    record = await repo.record_evaluation(eval_in)
    assert record.id is not None
    assert record.evaluation_time is not None
    
    evals, total = await repo.list_evaluations()
    assert total >= 1
    assert any(e.id == record.id for e in evals)

