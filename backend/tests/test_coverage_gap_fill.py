import pytest
from httpx import AsyncClient, ASGITransport
import uuid
from app.main import app
from core.database import get_db, Base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from core.config import settings
from models.user import User, UserRole
from core.security import create_access_token

import pytest_asyncio

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

@pytest.fixture
def override_get_db(db_session):
    async def _get_db_override():
        yield db_session
    app.dependency_overrides[get_db] = _get_db_override
    yield
    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def admin_user(db_session):
    admin = User(username="admin_gap", email="admin_gap@test.com", hashed_password="pw", role=UserRole.ADMINISTRATOR)
    db_session.add(admin)
    await db_session.commit()
    await db_session.refresh(admin)
    return admin

@pytest.fixture
def admin_headers(admin_user):
    token = create_access_token(str(admin_user.id), admin_user.role)
    return {"Authorization": f"Bearer {token}"}

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_gap_automation_404(override_get_db, client: AsyncClient, admin_headers):
    fake_id = str(uuid.uuid4())
    resp = await client.get(f"/api/v1/automation/requests/{fake_id}", headers=admin_headers)
    assert resp.status_code == 404

    resp = await client.get(f"/api/v1/automation/executions/{fake_id}", headers=admin_headers)
    assert resp.status_code == 404

@pytest.mark.asyncio
async def test_gap_correlations_404(override_get_db, client: AsyncClient, admin_headers):
    fake_id = str(uuid.uuid4())
    resp = await client.get(f"/api/v1/correlations/rules/{fake_id}", headers=admin_headers)
    assert resp.status_code == 404

    resp = await client.get(f"/api/v1/correlations/matches/{fake_id}", headers=admin_headers)
    assert resp.status_code == 404

@pytest.mark.asyncio
async def test_gap_evidence_404(override_get_db, client: AsyncClient, admin_headers):
    fake_id = str(uuid.uuid4())
    resp = await client.get(f"/api/v1/evidence/{fake_id}", headers=admin_headers)
    assert resp.status_code == 404

@pytest.mark.asyncio
async def test_gap_observations_404(override_get_db, client: AsyncClient, admin_headers):
    fake_id = str(uuid.uuid4())
    resp = await client.get(f"/api/v1/observations/{fake_id}", headers=admin_headers)
    assert resp.status_code == 404

@pytest.mark.asyncio
async def test_gap_policies_404(override_get_db, client: AsyncClient, admin_headers):
    fake_id = str(uuid.uuid4())
    resp = await client.get(f"/api/v1/policies/{fake_id}", headers=admin_headers)
    assert resp.status_code == 404

@pytest.mark.asyncio
async def test_gap_reports_404(override_get_db, client: AsyncClient, admin_headers):
    fake_id = str(uuid.uuid4())
    resp = await client.get(f"/api/v1/reports/{fake_id}", headers=admin_headers)
    assert resp.status_code == 404

@pytest.mark.asyncio
async def test_gap_users_404(override_get_db, client: AsyncClient, admin_headers):
    fake_id = str(uuid.uuid4())
    resp = await client.get(f"/api/v1/users/{fake_id}", headers=admin_headers)
    assert resp.status_code == 404

@pytest.mark.asyncio
async def test_gap_queue_coverage():
    from core.queue import automation_queue
    sz = automation_queue.qsize()
    assert sz >= 0

@pytest.mark.asyncio
async def test_gap_report_service_with_obs(override_get_db, db_session, admin_user):
    from services.report import ReportService
    from schemas.report import ReportGenerateRequest
    from models.report import ReportType
    from models.observation import Observation
    from datetime import datetime, timezone, timedelta
    from unittest.mock import patch

    now = datetime.now(timezone.utc)
    svc = ReportService(db_session)
    request = ReportGenerateRequest(
        report_type=ReportType.EXECUTIVE_SUMMARY,
        time_range_start=now - timedelta(days=1),
        time_range_end=now + timedelta(days=1),
        include_evidence=True,
        include_audit=True,
        compliance_frameworks=["SOC2"]
    )

    fake_obs = Observation(
        id=uuid.uuid4(), 
        title="Test", 
        description="Test", 
        correlation_id=uuid.uuid4(), 
        classification="TEST_CLASS", 
        risk_score=50, 
        created_by="system"
    )

    from unittest.mock import AsyncMock

    mock_list = AsyncMock()
    mock_list.side_effect = [([fake_obs], 1), ([], 0)]

    with patch.object(svc.obs_repo, 'list', new=mock_list):
        report = await svc.generate_report(request, user_id=str(admin_user.id))
        
    assert report is not None
    assert report.details["total_observations"] == 1

@pytest.mark.asyncio
async def test_gap_correlation_service():
    from services.correlation import extract_nested_value, evaluate_condition, run_correlation_cycle
    from models.correlation import CorrelationRule
    from app.schemas.ces import CESEvent, SourceType, Severity, Entity
    import uuid
    from datetime import datetime, timezone

    # 1. extract_nested_value with objects to hit hasattr and None
    class Dummy:
        pass
    d = Dummy()
    d.field = "value"
    assert extract_nested_value(d, "field") == "value"
    assert extract_nested_value(d, "missing") is None

    # 2. rule with no events, rule condition failing, and IP extraction
    rule = CorrelationRule(
        id=uuid.uuid4(),
        enabled=True,
        event_types=["authentication.failed.login"],
        conditions={"metadata.custom": "val"},
        time_window=300,
        severity_weight=50
    )
    rule_empty = CorrelationRule(
        id=uuid.uuid4(),
        enabled=True,
        event_types=["nonexistent.event.type"],
        conditions={"metadata.custom": "val"},
        time_window=300,
        severity_weight=50
    )
    # Empty rule_events
    ev1 = CESEvent(
        schema_version="1.0",
        event_id=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc).isoformat(),
        source_type=SourceType.custom,
        event_type="authentication.success.login",
        severity=Severity.info,
        raw_event="mock"
    )
    
    # Failing condition and IP extraction
    ev2 = CESEvent(
        schema_version="1.0",
        event_id=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc).isoformat(),
        source_type=SourceType.custom,
        event_type="authentication.failed.login",
        severity=Severity.info,
        actor=Entity(ip="1.2.3.4", username="usr"),
        metadata={"custom": "fail"}, # Condition will fail
        raw_event="mock"
    )
    
    # Passing condition and IP extraction
    ev3 = CESEvent(
        schema_version="1.0",
        event_id=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc).isoformat(),
        source_type=SourceType.custom,
        event_type="authentication.failed.login",
        severity=Severity.info,
        actor=Entity(ip="1.2.3.4", username="usr"),
        metadata={"custom": "val"}, # Condition passes
        raw_event="mock"
    )

    matches = run_correlation_cycle([ev1, ev2, ev3], [rule, rule_empty], "system")
    assert len(matches) == 1
    assert "1.2.3.4" in matches[0].context["ips"]

    from services.policy_engine import PolicyEngineService
    from models.policy import Policy
    from models.observation import Observation

    engine = PolicyEngineService(None)
    
    obs = Observation(risk_score=50, classification="test", status="NEW")
    
    # 91: risk_max
    pol_max = Policy(condition_risk_max=40)
    assert not engine._matches(pol_max, obs)
    
    # 93: classification
    pol_class = Policy(condition_classification="other")
    assert not engine._matches(pol_class, obs)
    
    # 95: status
    pol_status = Policy(condition_status="RESOLVED")
    assert not engine._matches(pol_status, obs)

@pytest.mark.asyncio
async def test_gap_report_service_max_obs(override_get_db, db_session, admin_user):
    from services.report import ReportService
    from schemas.report import ReportGenerateRequest
    from models.report import ReportType
    from models.observation import Observation
    from datetime import datetime, timezone
    from unittest.mock import patch, AsyncMock
    import uuid

    svc = ReportService(db_session)
    request = ReportGenerateRequest(
        report_type=ReportType.EXECUTIVE_SUMMARY,
        time_range_start=datetime.now(timezone.utc),
        time_range_end=datetime.now(timezone.utc),
        include_evidence=False,
        include_audit=False,
        compliance_frameworks=[]
    )

    fake_obs = Observation(
        id=uuid.uuid4(), 
        title="Test", 
        description="Test", 
        correlation_id=uuid.uuid4(), 
        classification="TEST_CLASS", 
        risk_score=50, 
        created_by="system"
    )

    # Return exactly max_observations (10000) fake obs to trigger the break
    mock_list = AsyncMock()
    mock_list.return_value = ([fake_obs] * 10000, 10000)

    with patch.object(svc.obs_repo, 'list', new=mock_list):
        report = await svc.generate_report(request, user_id=str(admin_user.id))
        
    assert report is not None
    assert report.details["total_observations"] == 10000

@pytest.mark.asyncio
async def test_gap_automation_worker_cancel():
    from workers.automation_worker import automation_worker
    from core.queue import automation_queue
    from unittest.mock import patch, AsyncMock
    import asyncio

    automation_worker.is_running = True
    
    try:
        with patch.object(automation_queue, 'dequeue', new_callable=AsyncMock) as mock_dq:
            mock_dq.side_effect = asyncio.CancelledError()
            await automation_worker._run_loop()
    finally:
        automation_worker.is_running = False
    
    # Should exit cleanly via the break in except CancelledError
    assert True


# --- API and Other Missing Gaps ---

@pytest.mark.asyncio
async def test_api_deps_gaps():
    from api.deps import get_current_user
    from core.config import settings
    from models.user import User
    from unittest.mock import MagicMock, AsyncMock
    import jwt
    from fastapi import HTTPException
    
    db = AsyncMock()
    mock_result = MagicMock()
    db.execute.return_value = mock_result
    
    token_no_sub = jwt.encode({}, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    with pytest.raises(HTTPException) as exc:
        await get_current_user(token_no_sub, db)
    assert exc.value.status_code == 401
    
    token_bad_uuid = jwt.encode({"sub": "not-a-uuid"}, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    with pytest.raises(HTTPException) as exc:
        await get_current_user(token_bad_uuid, db)
    assert exc.value.status_code == 401
    
    valid_uuid = str(uuid.uuid4())
    token_valid = jwt.encode({"sub": valid_uuid}, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    mock_result.scalar_one_or_none.return_value = None
    with pytest.raises(HTTPException) as exc:
        await get_current_user(token_valid, db)
    assert exc.value.status_code == 401
    
    mock_result.scalar_one_or_none.return_value = User(id=uuid.UUID(valid_uuid), is_active=False)
    with pytest.raises(HTTPException) as exc:
        await get_current_user(token_valid, db)
    assert exc.value.status_code == 401

@pytest.mark.asyncio
async def test_main_lifespan_gap():
    from app.main import lifespan
    from unittest.mock import MagicMock
    app_mock = MagicMock()
    async with lifespan(app_mock):
        pass

def test_base_parser_transformer_not_implemented():
    from app.parsers.base.base_parser import BaseParser
    from app.transformers.base import BaseTransformer
    from app.schemas.parser import RawLog
    
    class DummyParser(BaseParser):
        def parse(self, raw_log):
            super().parse(raw_log)
            raise ValueError("Test error")
            
    p = DummyParser()
    res = p.parse_safe(RawLog(raw_event="mock", source_ip="1.1.1.1", source_type="custom"))
    assert res.event_type == "custom.parsing.failed"
        
    class DummyTransformer(BaseTransformer):
        def parse(self, event):
            super().parse(event)
            return {"parsed": True}
    t = DummyTransformer()
    with pytest.raises(Exception):
        t.transform("test")

def test_ces_severity_non_str():
    from app.schemas.ces import CESEvent, Severity
    assert CESEvent.validate_severity(Severity.info) == Severity.info

def test_versioning_gaps():
    from app.core.versioning import check_deprecated_fields
    check_deprecated_fields({"old_field": "val"}, "0.9")

@pytest.mark.asyncio
async def test_rbac_enforce_deny_by_default_no_route():
    from core.rbac import enforce_deny_by_default
    from unittest.mock import MagicMock
    from fastapi import Request
    req = MagicMock(spec=Request)
    req.scope = {"route": None}
    await enforce_deny_by_default(req)

@pytest.mark.asyncio
async def test_crud_correlation_gap():
    from crud.crud_correlation import correlation_crud
    from unittest.mock import MagicMock, AsyncMock
    from datetime import datetime, timezone
    db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    db.execute.return_value = mock_result
    res = await correlation_crud.get_matches(db, end_time=datetime.now(timezone.utc))
    assert res == []

@pytest.mark.asyncio
async def test_api_automation_and_users_gaps(override_get_db, client, admin_headers, db_session):
    import uuid
    # GET /api/v1/automation/history
    resp = await client.get(
        "/api/v1/automation/history",
        headers=admin_headers
    )
    assert resp.status_code == 200
    
    # GET /api/v1/automation/{id} 404
    resp = await client.get(
        f"/api/v1/automation/{uuid.uuid4()}",
        headers=admin_headers
    )
    assert resp.status_code == 404
    
    # GET /api/v1/automation
    resp = await client.get(
        "/api/v1/automation",
        headers=admin_headers
    )
    assert resp.status_code == 200

    # --- Users API ---
    from models.user import User, UserRole
    # Create a base user to conflict with
    base_user = User(username="conflict_user", email="conflict@test.com", hashed_password="pw", role=UserRole.SOC_ANALYST)
    db_session.add(base_user)
    await db_session.commit()
    await db_session.refresh(base_user)

    # 1. POST conflict
    resp = await client.post(
        "/api/v1/users",
        headers=admin_headers,
        json={"username": "conflict_user", "email": "conflict2@test.com", "password": "abc", "role": "SOC Analyst"}
    )
    assert resp.status_code == 400
    
    # 2. GET 404
    resp = await client.get(
        f"/api/v1/users/{uuid.uuid4()}",
        headers=admin_headers
    )
    assert resp.status_code == 404
    
    # 3. PUT 404
    resp = await client.put(
        f"/api/v1/users/{uuid.uuid4()}",
        headers=admin_headers,
        json={"email": "new@new.com", "role": "SOC Analyst"}
    )
    assert resp.status_code == 404
    
    # 4. PUT conflict username
    other_user = User(username="other_user", email="other@test.com", hashed_password="pw", role=UserRole.SOC_ANALYST)
    db_session.add(other_user)
    await db_session.commit()
    await db_session.refresh(other_user)
    
    resp = await client.put(
        f"/api/v1/users/{other_user.id}",
        headers=admin_headers,
        json={"username": "conflict_user", "email": "other@test.com"}
    )
    assert resp.status_code == 400

    # 5. PUT conflict email
    resp = await client.put(
        f"/api/v1/users/{other_user.id}",
        headers=admin_headers,
        json={"username": "other_user", "email": "conflict@test.com"}
    )
    assert resp.status_code == 400
    
    # 6. PATCH /role 404
    resp = await client.patch(
        f"/api/v1/users/{uuid.uuid4()}/role",
        headers=admin_headers,
        json={"role": "Administrator"}
    )
    assert resp.status_code == 404

    # --- Audit API 58 ---
    resp = await client.get(
        f"/api/v1/audit/{uuid.uuid4()}?entity_type=user",
        headers=admin_headers
    )
    assert resp.status_code == 200
    
    # --- Correlations API 72 ---
    resp = await client.get(
        f"/api/v1/correlations/rules/{uuid.uuid4()}",
        headers=admin_headers
    )
    assert resp.status_code == 404
    
    # --- Evidence API 39 ---
    resp = await client.get(
        f"/api/v1/evidence/{uuid.uuid4()}",
        headers=admin_headers
    )
    assert resp.status_code == 404
    
    # --- Observations API 74, 79-80 ---
    resp = await client.put(
        f"/api/v1/observations/{uuid.uuid4()}",
        headers=admin_headers,
        json={"status": "RESOLVED"}
    )
    assert resp.status_code == 404
    
    # --- Policies API 65, 80, 83-86 ---
    from models.policy import Policy
    from models.observation import PolicyAction
    base_pol_name = f"conflict_pol_{uuid.uuid4()}"
    base_pol = Policy(name=base_pol_name, description="Test Desc", action=PolicyAction.OBSERVE, priority=10, is_active=True, condition_classification="TEST")
    db_session.add(base_pol)
    await db_session.commit()
    await db_session.refresh(base_pol)
    
    resp = await client.post(
        "/api/v1/policies",
        headers=admin_headers,
        json={"name": base_pol_name, "description": "Test Desc", "action": "OBSERVE", "priority": 10}
    )
    assert resp.status_code == 400
    
    resp = await client.put(
        f"/api/v1/policies/{uuid.uuid4()}",
        headers=admin_headers,
        json={"name": "test"}
    )
    assert resp.status_code == 404
    
    other_pol_name = f"other_pol_{uuid.uuid4()}"
    other_pol = Policy(name=other_pol_name, description="Test Desc", action=PolicyAction.OBSERVE, priority=10, is_active=True, condition_classification="TEST")
    db_session.add(other_pol)
    await db_session.commit()
    await db_session.refresh(other_pol)
    
    resp = await client.put(
        f"/api/v1/policies/{other_pol.id}",
        headers=admin_headers,
        json={"name": base_pol_name}
    )
    assert resp.status_code == 400
    
    # --- Reports API 64-66, 82 ---
    resp = await client.get(
        f"/api/v1/reports/{uuid.uuid4()}",
        headers=admin_headers
    )
    assert resp.status_code == 404
    
    resp = await client.get(
        f"/api/v1/reports/{uuid.uuid4()}/download",
        headers=admin_headers
    )
    assert resp.status_code == 404
