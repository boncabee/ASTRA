from core.config import settings
import pytest
import pytest_asyncio
import uuid
from httpx import AsyncClient, ASGITransport

from core.security import create_access_token
from core.database import Base, get_db
from models.user import User, UserRole
from models.observation import Observation, ObservationStatus
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
async def mock_observation(db_session):
    obs = Observation(
        title="Test Obs",
        description="Test Desc",
        correlation_id=uuid.uuid4(),
        classification="Anomaly",
        status=ObservationStatus.NEW,
        risk_score=75,
        evidence_count=5
    )
    db_session.add(obs)
    await db_session.commit()
    await db_session.refresh(obs)
    return obs

@pytest.mark.asyncio
async def test_get_observations(override_get_db, client: AsyncClient, admin_headers, mock_observation):
    response = await client.get("/api/v1/observations", headers=admin_headers)
    assert response.status_code == 200
    assert "data" in response.json()
    assert "total" in response.json()
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["id"] == str(mock_observation.id)

@pytest.mark.asyncio
async def test_get_observations_filters(override_get_db, client: AsyncClient, admin_headers, mock_observation):
    response = await client.get("/api/v1/observations?risk_category=HIGH", headers=admin_headers)
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1

    response = await client.get("/api/v1/observations?risk_category=LOW", headers=admin_headers)
    assert response.status_code == 200
    assert len(response.json()["data"]) == 0

@pytest.mark.asyncio
async def test_get_observation_by_id(override_get_db, client: AsyncClient, admin_headers, mock_observation):
    response = await client.get(f"/api/v1/observations/{mock_observation.id}", headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["data"]["id"] == str(mock_observation.id)

@pytest.mark.asyncio
async def test_update_observation_status_admin(override_get_db, client: AsyncClient, admin_headers, mock_observation):
    response = await client.put(
        f"/api/v1/observations/{mock_observation.id}",
        json={"status": "POLICY_EVALUATED"},
        headers=admin_headers
    )
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "POLICY_EVALUATED"

@pytest.mark.asyncio
async def test_update_observation_status_soc_denied(override_get_db, client: AsyncClient, soc_headers, mock_observation):
    # SOC Analyst cannot update status based on RequireRoles([ADMINISTRATOR, INCIDENT_RESPONDER])
    response = await client.put(
        f"/api/v1/observations/{mock_observation.id}",
        json={"status": "POLICY_EVALUATED"},
        headers=soc_headers
    )
    assert response.status_code == 403

