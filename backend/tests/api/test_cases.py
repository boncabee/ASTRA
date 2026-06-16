from core.config import settings
import pytest
import pytest_asyncio
import uuid
from httpx import AsyncClient, ASGITransport

from core.security import create_access_token
from core.database import Base, get_db
from models.user import User, UserRole
from models.case import Case, CaseStatus, CasePriority, CaseSeverity, CaseEvidenceLink
from models.evidence import Evidence, EvidenceType
from app.main import app
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

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
    admin = User(username="admin", email="admin@test.com", hashed_password="pw", role=UserRole.ADMINISTRATOR)
    db_session.add(admin)
    await db_session.commit()
    await db_session.refresh(admin)
    return admin

@pytest_asyncio.fixture
async def soc_user(db_session):
    soc = User(username="soc", email="soc@test.com", hashed_password="pw", role=UserRole.SOC_ANALYST)
    db_session.add(soc)
    await db_session.commit()
    await db_session.refresh(soc)
    return soc

@pytest.fixture
def admin_headers(admin_user):
    token = create_access_token(str(admin_user.id), admin_user.role)
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def soc_headers(soc_user):
    token = create_access_token(str(soc_user.id), soc_user.role)
    return {"Authorization": f"Bearer {token}"}

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest_asyncio.fixture
async def mock_case(db_session):
    case = Case(
        title="Test Case",
        description="Test Desc",
        status=CaseStatus.DRAFT,
        priority=CasePriority.MEDIUM,
        severity=CaseSeverity.MEDIUM,
        created_by="system",
    )
    db_session.add(case)
    await db_session.commit()
    await db_session.refresh(case)
    return case

@pytest_asyncio.fixture
async def mock_evidence(db_session):
    from datetime import datetime, timezone
    from models.correlation import CorrelationRule, CorrelationMatch
    from models.observation import Observation, ObservationStatus

    rule = CorrelationRule(
        name="Test Rule",
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
        title="Test Obs",
        description="Test Desc",
        correlation_id=match.id,
        classification="Anomaly",
        status=ObservationStatus.NEW,
        risk_score=75,
        evidence_count=0
    )
    db_session.add(obs)
    await db_session.commit()
    await db_session.refresh(obs)

    ev = Evidence(
        observation_id=obs.id,
        evidence_type=EvidenceType.SYSTEM_EVENT,
        source="system",
        content_reference="ref",
        hash_value="hash",
        created_by="system"
    )
    db_session.add(ev)
    await db_session.commit()
    await db_session.refresh(ev)
    return ev


@pytest.mark.asyncio
async def test_create_case(override_get_db, client: AsyncClient, admin_headers):
    response = await client.post(
        "/api/v1/cases",
        json={"title": "New API Case", "priority": "HIGH", "severity": "HIGH"},
        headers=admin_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New API Case"
    assert data["status"] == "DRAFT"

@pytest.mark.asyncio
async def test_list_cases(override_get_db, client: AsyncClient, admin_headers, mock_case):
    response = await client.get("/api/v1/cases", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any(c["id"] == str(mock_case.id) for c in data)

@pytest.mark.asyncio
async def test_get_case(override_get_db, client: AsyncClient, admin_headers, mock_case):
    response = await client.get(f"/api/v1/cases/{mock_case.id}", headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["id"] == str(mock_case.id)

@pytest.mark.asyncio
async def test_update_case(override_get_db, client: AsyncClient, admin_headers, mock_case):
    response = await client.patch(
        f"/api/v1/cases/{mock_case.id}",
        json={"title": "Updated API Case"},
        headers=admin_headers
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated API Case"

@pytest.mark.asyncio
async def test_assign_case(override_get_db, client: AsyncClient, admin_headers, mock_case):
    response = await client.post(
        f"/api/v1/cases/{mock_case.id}/assign",
        json={"assigned_user_id": "admin"},
        headers=admin_headers
    )
    assert response.status_code == 200
    assert response.json()["assigned_to"] == "admin"

@pytest.mark.asyncio
async def test_assign_case_soc_restriction(override_get_db, client: AsyncClient, soc_headers, soc_user, mock_case):
    # SOC cannot assign to someone else
    response = await client.post(
        f"/api/v1/cases/{mock_case.id}/assign",
        json={"assigned_user_id": "admin"},
        headers=soc_headers
    )
    assert response.status_code == 403

    # SOC can assign to self
    response = await client.post(
        f"/api/v1/cases/{mock_case.id}/assign",
        json={"assigned_user_id": soc_user.username},
        headers=soc_headers
    )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_change_status(override_get_db, client: AsyncClient, admin_headers, mock_case):
    response = await client.post(
        f"/api/v1/cases/{mock_case.id}/status",
        json={"new_status": "OPEN", "reason": "Testing API"},
        headers=admin_headers
    )
    assert response.status_code == 200
    assert response.json()["status"] == "OPEN"

@pytest.mark.asyncio
async def test_change_status_rbac_denied(override_get_db, client: AsyncClient, soc_headers, mock_case):
    # Assume mock_case is somehow RESOLVED, so SOC Analyst can't close it.
    # Since mock_case is DRAFT, let's open -> close.
    # This might require multiple transitions or direct DB manipulation.
    # For now, just test we can get a 403 for CLOSE via SOC
    # Open -> Investigating -> Resolved -> Closed
    await client.post(f"/api/v1/cases/{mock_case.id}/status", json={"new_status": "OPEN"}, headers=soc_headers)
    await client.post(f"/api/v1/cases/{mock_case.id}/status", json={"new_status": "INVESTIGATING"}, headers=soc_headers)
    await client.post(f"/api/v1/cases/{mock_case.id}/status", json={"new_status": "RESOLVED"}, headers=soc_headers)
    
    response = await client.post(f"/api/v1/cases/{mock_case.id}/status", json={"new_status": "CLOSED"}, headers=soc_headers)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_evidence_linking(override_get_db, client: AsyncClient, admin_headers, mock_case, mock_evidence):
    # Link
    response = await client.post(
        f"/api/v1/cases/{mock_case.id}/evidence",
        json={"evidence_id": str(mock_evidence.id)},
        headers=admin_headers
    )
    assert response.status_code == 201
    link_id = response.json()["id"]

    # List
    response = await client.get(f"/api/v1/cases/{mock_case.id}/evidence", headers=admin_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1

    # Soft Unlink
    response = await client.delete(f"/api/v1/cases/{mock_case.id}/evidence/{link_id}", headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["is_active"] is False

    # List again (should be 0 active)
    response = await client.get(f"/api/v1/cases/{mock_case.id}/evidence", headers=admin_headers)
    assert response.status_code == 200
    assert len(response.json()) == 0

@pytest.mark.asyncio
async def test_get_timeline(override_get_db, client: AsyncClient, admin_headers, mock_case):
    # A DRAFT case will have a CASE_CREATED event if created via API.
    # Since mock_case was direct DB, we should generate an event via API.
    await client.post(
        f"/api/v1/cases/{mock_case.id}/status",
        json={"new_status": "OPEN"},
        headers=admin_headers
    )

    response = await client.get(f"/api/v1/cases/{mock_case.id}/timeline", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["event_type"] == "STATUS_CHANGE"
