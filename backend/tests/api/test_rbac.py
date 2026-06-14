import pytest
import pytest_asyncio
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
    admin = User(username="admin", email="admin@test", hashed_password=get_password_hash("pw"), role=UserRole.ADMINISTRATOR)
    sec_eng = User(username="sec", email="sec@test", hashed_password=get_password_hash("pw"), role=UserRole.SECURITY_ENGINEER)
    soc_ana = User(username="soc", email="soc@test", hashed_password=get_password_hash("pw"), role=UserRole.SOC_ANALYST)
    inc_res = User(username="inc", email="inc@test", hashed_password=get_password_hash("pw"), role=UserRole.INCIDENT_RESPONDER)
    
    db_session.add_all([admin, sec_eng, soc_ana, inc_res])
    await db_session.commit()
    
    # generate tokens
    from core.security import create_access_token
    tokens = {
        "admin": create_access_token(str(admin.id), admin.role),
        "sec": create_access_token(str(sec_eng.id), sec_eng.role),
        "soc": create_access_token(str(soc_ana.id), soc_ana.role),
        "inc": create_access_token(str(inc_res.id), inc_res.role)
    }
    return tokens

@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_admin_access(override_get_db, async_client, users):
    headers = {"Authorization": f"Bearer {users['admin']}"}
    
    res1 = await async_client.get("/api/v1/admin/ping", headers=headers)
    assert res1.status_code == 200
    
    res2 = await async_client.get("/api/v1/security/ping", headers=headers)
    assert res2.status_code == 200
    
    res3 = await async_client.get("/api/v1/responders/ping", headers=headers)
    assert res3.status_code == 200

@pytest.mark.asyncio
async def test_security_engineer_access(override_get_db, async_client, users):
    headers = {"Authorization": f"Bearer {users['sec']}"}
    
    res1 = await async_client.get("/api/v1/admin/ping", headers=headers)
    assert res1.status_code == 403
    
    res2 = await async_client.get("/api/v1/security/ping", headers=headers)
    assert res2.status_code == 200
    
    res3 = await async_client.get("/api/v1/responders/ping", headers=headers)
    assert res3.status_code == 403

@pytest.mark.asyncio
async def test_incident_responder_access(override_get_db, async_client, users):
    headers = {"Authorization": f"Bearer {users['inc']}"}
    
    res1 = await async_client.get("/api/v1/admin/ping", headers=headers)
    assert res1.status_code == 403
    
    res2 = await async_client.get("/api/v1/security/ping", headers=headers)
    assert res2.status_code == 403
    
    res3 = await async_client.get("/api/v1/responders/ping", headers=headers)
    assert res3.status_code == 200

@pytest.mark.asyncio
async def test_soc_analyst_access(override_get_db, async_client, users):
    headers = {"Authorization": f"Bearer {users['soc']}"}
    
    # SOC Analyst has no access to any ping endpoints in this test setup
    for endpoint in ["/api/v1/admin/ping", "/api/v1/security/ping", "/api/v1/responders/ping"]:
        res = await async_client.get(endpoint, headers=headers)
        assert res.status_code == 403

@pytest.mark.asyncio
async def test_missing_and_invalid_token(async_client):
    res1 = await async_client.get("/api/v1/admin/ping")
    assert res1.status_code == 401
    
    res2 = await async_client.get("/api/v1/admin/ping", headers={"Authorization": "Bearer invalid"})
    assert res2.status_code == 401

@pytest.mark.asyncio
async def test_deny_by_default(async_client):
    # Dynamically inject an unprotected route into the running app
    @app.get("/api/v1/unprotected")
    async def unprotected():
        return {"msg": "Should not be reached"}
        
    res = await async_client.get("/api/v1/unprotected")
    assert res.status_code == 403
    assert res.json()["detail"] == "Access denied by default. Route is unprotected."

@pytest.mark.asyncio
async def test_rbac_logging(override_get_db, async_client, users, caplog):
    import logging
    caplog.set_level(logging.WARNING)
    
    headers = {"Authorization": f"Bearer {users['soc']}"}
    await async_client.get("/api/v1/admin/ping", headers=headers)
    
    # Check if a log was emitted
    log_records = [record for record in caplog.records if "Unauthorized access attempt" in record.message]
    assert len(log_records) > 0
