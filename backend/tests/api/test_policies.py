from core.config import settings
import pytest
import pytest_asyncio
from httpx import AsyncClient

from core.security import create_access_token
from core.database import Base, get_db
from models.user import User, UserRole
from app.main import app
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from models.observation import PolicyAction

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
async def sec_user(db_session):
    sec = User(username="secpol", email="secpol@test.com", hashed_password="pw", role=UserRole.SECURITY_ENGINEER)
    db_session.add(sec)
    await db_session.commit()
    await db_session.refresh(sec)
    return sec

@pytest_asyncio.fixture
async def sec_headers(sec_user):
    token = create_access_token(str(sec_user.id), sec_user.role)
    return {"Authorization": f"Bearer {token}"}

@pytest_asyncio.fixture
async def analyst_user(db_session):
    analyst = User(username="analystpol", email="analystpol@test.com", hashed_password="pw", role=UserRole.SOC_ANALYST)
    db_session.add(analyst)
    await db_session.commit()
    await db_session.refresh(analyst)
    return analyst

@pytest_asyncio.fixture
async def analyst_headers(analyst_user):
    token = create_access_token(str(analyst_user.id), analyst_user.role)
    return {"Authorization": f"Bearer {token}"}

@pytest_asyncio.fixture
async def client():
    from httpx import ASGITransport
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_create_policy_success(override_get_db, client: AsyncClient, sec_headers):
    payload = {
        "name": "API Test Policy",
        "description": "Desc",
        "action": PolicyAction.NOTIFY,
        "priority": 100,
        "is_active": True,
        "condition_risk_min": 70
    }
    response = await client.post("/api/v1/policies", headers=sec_headers, json=payload)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == "API Test Policy"

@pytest.mark.asyncio
async def test_create_policy_forbidden(override_get_db, client: AsyncClient, analyst_headers):
    payload = {
        "name": "API Test Policy Analyst",
        "description": "Desc",
        "action": PolicyAction.NOTIFY,
        "priority": 100
    }
    response = await client.post("/api/v1/policies", headers=analyst_headers, json=payload)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_list_policies(override_get_db, client: AsyncClient, sec_headers):
    response = await client.get("/api/v1/policies", headers=sec_headers)
    assert response.status_code == 200
    assert "data" in response.json()
    assert isinstance(response.json()["data"], list)

@pytest.mark.asyncio
async def test_update_policy(override_get_db, client: AsyncClient, sec_headers):
    payload = {
        "name": "API Test Policy 2",
        "description": "Desc",
        "action": PolicyAction.OBSERVE,
        "priority": 50
    }
    res = await client.post("/api/v1/policies", headers=sec_headers, json=payload)
    policy_id = res.json()["data"]["id"]
    
    update_payload = {"action": PolicyAction.REVIEW_REQUIRED}
    res_update = await client.put(f"/api/v1/policies/{policy_id}", headers=sec_headers, json=update_payload)
    assert res_update.status_code == 200
    assert res_update.json()["data"]["action"] == PolicyAction.REVIEW_REQUIRED

@pytest.mark.asyncio
async def test_get_policy(override_get_db, client: AsyncClient, sec_headers):
    payload = {
        "name": "API Test Policy 3",
        "description": "Desc",
        "action": PolicyAction.OBSERVE,
        "priority": 50
    }
    res = await client.post("/api/v1/policies", headers=sec_headers, json=payload)
    policy_id = res.json()["data"]["id"]
    
    res_get = await client.get(f"/api/v1/policies/{policy_id}", headers=sec_headers)
    assert res_get.status_code == 200
    assert res_get.json()["data"]["name"] == "API Test Policy 3"

@pytest.mark.asyncio
async def test_list_evaluations(override_get_db, client: AsyncClient, analyst_headers):
    res = await client.get("/api/v1/policies/evaluations", headers=analyst_headers)
    assert res.status_code == 200
    assert "data" in res.json()
    assert isinstance(res.json()["data"], list)

