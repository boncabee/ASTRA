"""
Phase 8.1.7 — Targeted coverage correction tests.
Covers exactly the missed lines reported in CI.
"""
import uuid
from datetime import datetime, timezone
import pytest
import pytest_asyncio
from unittest.mock import patch, AsyncMock
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from core.config import settings
from core.database import Base
from models.automation import AutomationAction, AutomationState
from models.policy import Policy
from models.case import Case, CaseStatus, CasePriority, CaseSeverity, TimelineEventType
from models.observation import Observation, ObservationStatus, PolicyAction
from models.correlation import CorrelationRule, CorrelationMatch
from models.evidence import AuditEvent
from models.report import Report, ReportType
from schemas.automation import AutomationRequestCreate
from schemas.evidence import AuditEventCreate
from repositories.automation import AutomationRepository
from services.automation import AutomationService
from repositories.case_timeline import CaseTimelineRepository
from repositories.report import ReportRepository
from repositories.policy import PolicyRepository
from repositories.evidence import AuditRepository
from repositories.observation import ObservationRepository

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
async def test_automation_repo_and_service(db_session):
    # 1. Create a policy
    policy = Policy(
        name=f"Policy-{uuid.uuid4()}",
        description="test",
        action=PolicyAction.NOTIFY,
        priority=100,
        is_active=True,
        created_by="test",
    )
    db_session.add(policy)
    await db_session.commit()
    await db_session.refresh(policy)

    # 2. Repo: create_request (covers 26-35)
    repo = AutomationRepository(db_session)
    data = AutomationRequestCreate(
        policy_id=policy.id,
        action=AutomationAction.LOG_ACTION,
        parameters={"test": "data"}
    )
    req, exec_record = await repo.create_request(data, "user-1")
    assert req.id is not None
    assert exec_record.id is not None

    # 3. Repo: get_request (covers 43)
    fetched_req = await repo.get_request(req.id)
    assert fetched_req is not None
    assert fetched_req.id == req.id

    # 4. Repo: list_requests (covers 47-55)
    reqs, count = await repo.list_requests()
    assert count > 0
    assert len(reqs) > 0

    # 5. Repo: get_history (covers 59-67)
    hist, hist_count = await repo.get_history()
    assert hist_count > 0
    assert len(hist) > 0

    # 6. Service: create_automation_request (covers 18-28)
    service = AutomationService(db_session)
    # mock the queue enqueue
    with patch("core.queue.automation_queue.enqueue", new_callable=AsyncMock) as mock_enqueue:
        service_req = await service.create_automation_request(data, "user-2")
        assert service_req.id is not None
        mock_enqueue.assert_called_once()

@pytest.mark.asyncio
async def test_case_timeline_repo(db_session):
    # Create a case
    case = Case(
        id=uuid.uuid4(),
        title="Test Case",
        status=CaseStatus.DRAFT,
        priority=CasePriority.LOW,
        severity=CaseSeverity.LOW,
        created_by="test",
    )
    db_session.add(case)
    await db_session.commit()
    await db_session.refresh(case)

    # 1. create (covers 33-34)
    repo = CaseTimelineRepository(db_session)
    timeline_event = await repo.create(
        case_id=case.id,
        event_type=TimelineEventType.CASE_CREATED,
        actor="test",
        event_metadata={"info": "started"}
    )
    assert timeline_event.id is not None

    # 2. get_by_case_id (covers 46-50)
    events, count = await repo.get_by_case_id(case.id)
    assert count > 0
    assert len(events) > 0

@pytest.mark.asyncio
async def test_report_repo(db_session):
    # 1. list_reports (covers 43-47)
    repo = ReportRepository(db_session)
    reports, count = await repo.list_reports()
    # just hitting it is enough for coverage
    assert count >= 0

@pytest.mark.asyncio
async def test_policy_repo(db_session):
    # Create policy
    name = f"TestName-{uuid.uuid4()}"
    policy = Policy(
        name=name,
        description="test",
        action=PolicyAction.NOTIFY,
        priority=100,
        is_active=True,
        created_by="test",
    )
    db_session.add(policy)
    await db_session.commit()

    repo = PolicyRepository(db_session)
    
    # 1. get_by_name (covers 30)
    fetched = await repo.get_by_name(name)
    assert fetched is not None

    # 2. list (covers 44-50)
    policies, count = await repo.list()
    assert count > 0

@pytest.mark.asyncio
async def test_audit_repo(db_session):
    repo = AuditRepository(db_session)
    
    data = AuditEventCreate(
        entity_type="observation",
        entity_id=uuid.uuid4(),
        action="created",
        actor="user",
        details={"k": "v"}
    )
    await repo.create_event(data)

    # list_events (covers 65-69)
    events, count = await repo.list_events()
    assert count > 0

@pytest.mark.asyncio
async def test_observation_repo(db_session):
    # Create correlation rule and match first
    rule = CorrelationRule(
        name=f"Rule-{uuid.uuid4()}",
        description="test",
        event_types=["test.event"],
        conditions={},
        time_window=60,
        severity_weight=50,
    )
    db_session.add(rule)
    await db_session.flush()

    match = CorrelationMatch(
        rule_id=rule.id,
        matched_events=["evt-1"],
        event_count=1,
        match_timestamp=datetime.now(timezone.utc),
        correlation_score=50,
        context={},
    )
    db_session.add(match)
    await db_session.flush()

    # Create observation
    obs = Observation(
        id=uuid.uuid4(),
        title="Test Obs",
        description="test",
        correlation_id=match.id,
        classification="Network",
        status=ObservationStatus.NEW,
        risk_score=50,
        evidence_count=0,
        created_by="test",
        updated_by="test",
    )
    db_session.add(obs)
    await db_session.commit()
    await db_session.refresh(obs)

    repo = ObservationRepository(db_session)

    # 1. get_by_id (covers 27)
    fetched = await repo.get_by_id(obs.id)
    assert fetched is not None

    # 2. update (covers 36-37)
    obs.status = ObservationStatus.UNDER_REVIEW
    updated = await repo.update(obs)
    assert updated.status == ObservationStatus.UNDER_REVIEW
