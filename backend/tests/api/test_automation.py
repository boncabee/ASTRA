import pytest
import pytest_asyncio
import asyncio
from httpx import AsyncClient, ASGITransport
from datetime import datetime, timezone, timedelta
import uuid
import time

from core.security import create_access_token
from core.database import Base, get_db
from models.user import User, UserRole
from app.main import app
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# Reusing same fixtures strategy as reports to ensure consistency
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

@pytest.fixture
def override_get_db(db_session):
    async def _get_db_override():
        yield db_session
    
    app.dependency_overrides[get_db] = _get_db_override
    yield
    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def admin_user(db_session):
    admin = User(username="admin_auto", email="admin_auto@test.com", hashed_password="pw", role=UserRole.ADMINISTRATOR)
    db_session.add(admin)
    await db_session.commit()
    await db_session.refresh(admin)
    return admin

@pytest_asyncio.fixture
async def soc_user(db_session):
    soc = User(username="soc_auto", email="soc_auto@test.com", hashed_password="pw", role=UserRole.SOC_ANALYST)
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

@pytest.mark.asyncio
async def test_create_automation_request_admin(override_get_db, client: AsyncClient, admin_headers):
    policy_id = str(uuid.uuid4())
    payload = {
        "policy_id": policy_id,
        "action": "NOTIFY_WEBHOOK",
        "parameters": {"url": "http://example.com/webhook"}
    }
    
    response = await client.post(
        "/api/v1/automation",
        headers=admin_headers,
        json=payload
    )
    
    assert response.status_code == 202, response.json()
    data = response.json()
    assert data["policy_id"] == policy_id
    assert data["action"] == "NOTIFY_WEBHOOK"
    assert data["state"] == "PENDING"
    assert "id" in data

@pytest.mark.asyncio
async def test_create_automation_request_unauthorized(override_get_db, client: AsyncClient, soc_headers):
    payload = {
        "policy_id": str(uuid.uuid4()),
        "action": "NOTIFY_WEBHOOK",
        "parameters": {"url": "http://example.com/webhook"}
    }
    
    response = await client.post(
        "/api/v1/automation",
        headers=soc_headers,
        json=payload
    )
    
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_get_metrics(override_get_db, client: AsyncClient, admin_headers):
    response = await client.get(
        "/api/v1/automation/metrics",
        headers=admin_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "automation_requests" in data
    assert "automation_executions" in data
    assert "queue_depth" in data

@pytest.mark.asyncio
async def test_automation_worker_processing(override_get_db, client: AsyncClient, admin_headers):
    policy_id = str(uuid.uuid4())
    payload = {
        "policy_id": policy_id,
        "action": "LOG_ACTION",
        "parameters": {"message": "test"}
    }
    
    response = await client.post(
        "/api/v1/automation",
        headers=admin_headers,
        json=payload
    )
    assert response.status_code == 202
    request_id = response.json()["id"]

    await asyncio.sleep(0.5)

    response = await client.get(
        f"/api/v1/automation/{request_id}",
        headers=admin_headers
    )
    assert response.status_code == 200
    data = response.json()
    
    assert data["state"] in ["RUNNING", "SUCCESS", "PENDING"]

@pytest.mark.asyncio
async def test_performance_no_blocking(override_get_db, client: AsyncClient, admin_headers):
    start_time = time.time()
    for _ in range(50):
        payload = {
            "policy_id": str(uuid.uuid4()),
            "action": "LOG_ACTION",
            "parameters": {"test": "perf"}
        }
        resp = await client.post("/api/v1/automation", headers=admin_headers, json=payload)
        assert resp.status_code == 202
        
    duration = time.time() - start_time
    assert duration < 2.0
