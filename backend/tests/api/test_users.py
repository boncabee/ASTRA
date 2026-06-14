import pytest
import pytest_asyncio
import uuid
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.main import app
from core.database import Base, get_db
from core.security import get_password_hash
from models.user import User, UserRole

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
async def users(db_session):
    admin = User(username="admin", email="admin@test.com", hashed_password=get_password_hash("pw"), role=UserRole.ADMINISTRATOR)
    sec_eng = User(username="sec", email="sec@test.com", hashed_password=get_password_hash("pw"), role=UserRole.SECURITY_ENGINEER)
    soc_ana = User(username="soc", email="soc@test.com", hashed_password=get_password_hash("pw"), role=UserRole.SOC_ANALYST)
    inc_res = User(username="inc", email="inc@test.com", hashed_password=get_password_hash("pw"), role=UserRole.INCIDENT_RESPONDER)
    
    db_session.add_all([admin, sec_eng, soc_ana, inc_res])
    await db_session.commit()
    await db_session.refresh(admin)
    
    from core.security import create_access_token
    tokens = {
        "admin": create_access_token(str(admin.id), admin.role),
        "sec": create_access_token(str(sec_eng.id), sec_eng.role),
        "admin_id": str(admin.id)
    }
    return tokens

@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_get_users(override_get_db, async_client, users):
    headers = {"Authorization": f"Bearer {users['sec']}"}
    res = await async_client.get("/api/v1/users", headers=headers)
    assert res.status_code == 200
    data = res.json()["data"]
    assert len(data) == 4
    assert "hashed_password" not in data[0]

@pytest.mark.asyncio
async def test_get_user(override_get_db, async_client, users):
    headers = {"Authorization": f"Bearer {users['sec']}"}
    res = await async_client.get(f"/api/v1/users/{users['admin_id']}", headers=headers)
    assert res.status_code == 200
    assert res.json()["data"]["username"] == "admin"

@pytest.mark.asyncio
async def test_create_user(override_get_db, async_client, users):
    headers = {"Authorization": f"Bearer {users['admin']}"}
    new_user = {
        "username": "newuser",
        "email": "new@test.com",
        "role": "SOC Analyst",
        "is_active": True,
        "password": "strongpassword"
    }
    res = await async_client.post("/api/v1/users", json=new_user, headers=headers)
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["username"] == "newuser"
    assert data["created_by"] == users["admin_id"]
    assert "hashed_password" not in data

@pytest.mark.asyncio
async def test_create_duplicate_user(override_get_db, async_client, users):
    headers = {"Authorization": f"Bearer {users['admin']}"}
    new_user = {
        "username": "admin",
        "email": "diff@test.com",
        "role": "SOC Analyst",
        "is_active": True,
        "password": "pw"
    }
    res = await async_client.post("/api/v1/users", json=new_user, headers=headers)
    assert res.status_code == 400
    assert res.json()["error"] == "Username or email already exists"

@pytest.mark.asyncio
async def test_create_user_unauthorized(override_get_db, async_client, users):
    headers = {"Authorization": f"Bearer {users['sec']}"}
    res = await async_client.post("/api/v1/users", json={"username":"fail","email":"f@a.c","password":"1","role":"SOC Analyst"}, headers=headers)
    assert res.status_code == 403

@pytest.mark.asyncio
async def test_update_user(override_get_db, async_client, users):
    headers = {"Authorization": f"Bearer {users['admin']}"}
    update_data = {"username": "admin_updated"}
    res = await async_client.put(f"/api/v1/users/{users['admin_id']}", json=update_data, headers=headers)
    assert res.status_code == 200
    assert res.json()["data"]["username"] == "admin_updated"

@pytest.mark.asyncio
async def test_update_status(override_get_db, async_client, users):
    headers = {"Authorization": f"Bearer {users['admin']}"}
    res = await async_client.patch(f"/api/v1/users/{users['admin_id']}/status", json={"is_active": False}, headers=headers)
    assert res.status_code == 200
    assert res.json()["data"]["is_active"] is False

@pytest.mark.asyncio
async def test_update_role(override_get_db, async_client, users):
    headers = {"Authorization": f"Bearer {users['admin']}"}
    res = await async_client.patch(f"/api/v1/users/{users['admin_id']}/role", json={"role": "Incident Responder"}, headers=headers)
    assert res.status_code == 200
    assert res.json()["data"]["role"] == "Incident Responder"

@pytest.mark.asyncio
async def test_user_not_found(override_get_db, async_client, users):
    headers = {"Authorization": f"Bearer {users['admin']}"}
    fake_id = str(uuid.uuid4())
    res = await async_client.get(f"/api/v1/users/{fake_id}", headers=headers)
    assert res.status_code == 404
