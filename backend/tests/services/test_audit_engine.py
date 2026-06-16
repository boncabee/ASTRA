from core.config import settings
import pytest
import pytest_asyncio
import uuid
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from core.database import Base
from models.observation import Observation, ObservationStatus, PolicyAction
from models.policy import PolicyEvaluation
from models.evidence import Evidence, EvidenceType
from models.correlation import CorrelationRule, CorrelationMatch
from services.audit_engine import AuditEngineService

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

async def make_observation(db_session, risk_score=50, classification="Auth", status=ObservationStatus.NEW, action=PolicyAction.REVIEW_REQUIRED):
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
        policy_action=action,
        evidence_count=1
    )
    db_session.add(obs)
    await db_session.commit()
    await db_session.refresh(obs)
    return obs

@pytest.mark.asyncio
async def test_decision_provenance(db_session):
    obs = await make_observation(db_session, risk_score=85, classification="Malware", status=ObservationStatus.POLICY_EVALUATED, action=PolicyAction.REVIEW_REQUIRED)
    obs_id = obs.id
    pol_id = uuid.uuid4()
    
    from models.policy import Policy
    policy = Policy(
        id=pol_id,
        name="Test Policy",
        description="Desc",
        action=PolicyAction.REVIEW_REQUIRED,
        priority=100,
        is_active=True
    )
    db_session.add(policy)
    await db_session.flush()
    
    # 2. Setup Evaluation
    pe = PolicyEvaluation(
        policy_id=pol_id,
        observation_id=obs_id,
        decision_reason="Matched high risk policy",
        action=PolicyAction.REVIEW_REQUIRED
    )
    db_session.add(pe)
    
    # 3. Setup Evidence
    ev = Evidence(
        observation_id=obs_id,
        evidence_type=EvidenceType.SYSTEM_EVENT,
        source="Engine",
        content_reference="log_123",
        hash_value="abc",
        created_by="system"
    )
    db_session.add(ev)
    
    await db_session.commit()
    
    # 4. Run Provenance Engine
    svc = AuditEngineService(db_session)
    response = await svc.get_decision_provenance(obs_id)
    
    assert response is not None
    assert response.observation_id == obs_id
    assert response.risk_score == 85
    assert response.policy_action == "REVIEW_REQUIRED"
    assert len(response.evidence) == 1
    assert response.evidence[0].hash_value == "abc"
    assert len(response.evaluations) == 1
    assert response.evaluations[0]["decision_reason"] == "Matched high risk policy"

@pytest.mark.asyncio
async def test_decision_provenance_not_found(db_session):
    svc = AuditEngineService(db_session)
    response = await svc.get_decision_provenance(uuid.uuid4())
    assert response is None

