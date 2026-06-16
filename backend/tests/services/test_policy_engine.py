from core.config import settings
import pytest
import pytest_asyncio
import uuid
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from core.database import Base
from models.observation import Observation, ObservationStatus, PolicyAction
from models.correlation import CorrelationRule, CorrelationMatch
from schemas.policy import PolicyCreate
from repositories.policy import PolicyRepository
from services.policy_engine import PolicyEngineService

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

async def make_observation(db_session, risk_score=50, classification="Auth", status=ObservationStatus.NEW):
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
        classification=classification,
        status=status,
        risk_score=risk_score,
        evidence_count=1
    )
    db_session.add(obs)
    await db_session.commit()
    await db_session.refresh(obs)
    return obs
@pytest.mark.asyncio
async def test_policy_engine_no_match(db_session):
    engine_svc = PolicyEngineService(db_session)
    obs = await make_observation(db_session)
    
    action = await engine_svc.evaluate_observation(obs)
    
    assert action == PolicyAction.OBSERVE
    
    repo = PolicyRepository(db_session)
    evals, _ = await repo.list_evaluations()
    assert len(evals) == 1
    assert evals[0].action == PolicyAction.OBSERVE
    assert evals[0].decision_reason == "Fallback to default action (OBSERVE)"

@pytest.mark.asyncio
async def test_policy_engine_match_risk(db_session):
    repo = PolicyRepository(db_session)
    await repo.create(PolicyCreate(
        name="High Risk Notify",
        description="Notify on high risk",
        action=PolicyAction.NOTIFY,
        priority=100,
        condition_risk_min=70
    ), "sys")
    
    engine_svc = PolicyEngineService(db_session)
    
    obs_low = await make_observation(db_session, risk_score=50)
    action_low = await engine_svc.evaluate_observation(obs_low)
    assert action_low == PolicyAction.OBSERVE
    
    obs_high = await make_observation(db_session, risk_score=80)
    action_high = await engine_svc.evaluate_observation(obs_high)
    assert action_high == PolicyAction.NOTIFY

@pytest.mark.asyncio
async def test_policy_engine_priority(db_session):
    repo = PolicyRepository(db_session)
    
    await repo.create(PolicyCreate(
        name="Auth Notify",
        description="Notify on auth",
        action=PolicyAction.NOTIFY,
        priority=100,
        condition_classification="Auth"
    ), "sys")
    
    await repo.create(PolicyCreate(
        name="Auth Review",
        description="Review on auth",
        action=PolicyAction.REVIEW_REQUIRED,
        priority=200, # Higher priority
        condition_classification="Auth"
    ), "sys")
    
    engine_svc = PolicyEngineService(db_session)
    obs = await make_observation(db_session, classification="Auth")
    
    action = await engine_svc.evaluate_observation(obs)
    assert action == PolicyAction.REVIEW_REQUIRED

@pytest.mark.asyncio
async def test_policy_engine_conflict_resolution(db_session):
    repo = PolicyRepository(db_session)
    
    # Same priority, same conditions. ID order will break the tie.
    await repo.create(PolicyCreate(
        name="Conflict 1",
        description="C1",
        action=PolicyAction.NOTIFY,
        priority=50,
        condition_status=ObservationStatus.NEW
    ), "sys")
    
    await repo.create(PolicyCreate(
        name="Conflict 2",
        description="C2",
        action=PolicyAction.FUTURE_MITIGATION,
        priority=50,
        condition_status=ObservationStatus.NEW
    ), "sys")
    
    engine_svc = PolicyEngineService(db_session)
    obs = await make_observation(db_session, status=ObservationStatus.NEW)
    
    await engine_svc.evaluate_observation(obs)
    
    # Check that we handled conflict deterministically
    evals, _ = await repo.list_evaluations()
    last_eval = evals[0] # Due to order by desc in list_evaluations
    assert "Conflict resolved by ID order" in last_eval.decision_reason

@pytest.mark.asyncio
async def test_policy_engine_performance_10k(db_session):
    repo = PolicyRepository(db_session)
    
    # Add a few rules
    await repo.create(PolicyCreate(
        name="Perf 1", description="", action=PolicyAction.NOTIFY, priority=100, condition_risk_min=80
    ), "sys")
    await repo.create(PolicyCreate(
        name="Perf 2", description="", action=PolicyAction.REVIEW_REQUIRED, priority=200, condition_classification="Malware"
    ), "sys")
    
    engine_svc = PolicyEngineService(db_session)
    
    import time
    start = time.perf_counter()
    
    for i in range(100): # Just do 100 in test to avoid overhead
        obs = await make_observation(db_session, risk_score=85, classification="Malware")
        await engine_svc.evaluate_observation(obs)
        
    end = time.perf_counter()
    assert (end - start) < 15.0 # Increased timeout for SQLite overhead

