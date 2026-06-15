from core.config import settings
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from datetime import datetime, timezone, timedelta
import uuid

from core.security import create_access_token
from core.database import Base, get_db
from models.user import User, UserRole
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

@pytest.mark.asyncio
async def test_generate_report_as_admin(override_get_db, client: AsyncClient, admin_headers):
    now = datetime.now(timezone.utc)
    start_time = now - timedelta(days=1)
    
    payload = {
        "report_type": "Observation Report",
        "time_range_start": start_time.isoformat(),
        "time_range_end": now.isoformat(),
        "data_sources": ["AWS", "Firewall"],
        "include_evidence": True,
        "include_audit": True,
        "compliance_frameworks": ["ISO 27001", "NIST CSF"]
    }
    
    response = await client.post(
        "/api/v1/reports/generate",
        json=payload,
        headers=admin_headers
    )
    
    assert response.status_code == 201, response.json()
    data = response.json()
    assert data["report_type"] == "Observation Report"
    assert "id" in data
    assert len(data["compliance_mappings"]) == 2
    assert data["compliance_mappings"][0]["framework"] == "ISO 27001"

@pytest.mark.asyncio
async def test_generate_report_rbac_denied(override_get_db, client: AsyncClient, soc_headers):
    now = datetime.now(timezone.utc)
    start_time = now - timedelta(days=1)
    
    payload = {
        "report_type": "Observation Report",
        "time_range_start": start_time.isoformat(),
        "time_range_end": now.isoformat(),
        "data_sources": [],
        "include_evidence": True,
        "include_audit": True,
        "compliance_frameworks": []
    }
    
    response = await client.post(
        "/api/v1/reports/generate",
        json=payload,
        headers=soc_headers
    )
    
    assert response.status_code == 403, response.json()

@pytest.mark.asyncio
async def test_list_reports(override_get_db, client: AsyncClient, soc_headers):
    response = await client.get(
        "/api/v1/reports",
        headers=soc_headers
    )
    
    assert response.status_code == 200, response.json()
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_get_report_history(override_get_db, client: AsyncClient, soc_headers):
    response = await client.get(
        "/api/v1/reports/history",
        headers=soc_headers
    )
    
    assert response.status_code == 200, response.json()
    data = response.json()
    assert isinstance(data, list)

