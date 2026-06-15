from core.config import settings
import pytest
import pytest_asyncio
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from core.database import Base
from models.observation import Observation, ObservationStatus, PolicyAction
from models.policy import PolicyEvaluation
from models.evidence import Evidence, EvidenceType
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

@pytest.mark.asyncio
async def test_decision_provenance(db_session):
    obs_id = uuid.uuid4()
    pol_id = uuid.uuid4()
    
    # 1. Setup Observation
    obs = Observation(
        id=obs_id,
        title="Test Obs",
        description="Desc",
        correlation_id=uuid.uuid4(),
        classification="Malware",
        status=ObservationStatus.POLICY_EVALUATED,
        risk_score=85,
        policy_action=PolicyAction.REVIEW_REQUIRED,
        evidence_count=1
    )
    db_session.add(obs)
    
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

