import pytest
import pytest_asyncio
import uuid
from httpx import AsyncClient

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
async def analyst_user(db_session):
    analyst = User(username="analyst_ev", email="ev@test.com", hashed_password="pw", role=UserRole.SOC_ANALYST)
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
async def test_get_evidence_list(override_get_db, client: AsyncClient, analyst_headers):
    # Just checking the route is active and allows read
    response = await client.get("/api/v1/evidence", headers=analyst_headers)
    assert response.status_code == 200
    assert "data" in response.json()
    assert isinstance(response.json()["data"], list)

@pytest.mark.asyncio
async def test_get_audit_list(override_get_db, client: AsyncClient, analyst_headers):
    response = await client.get("/api/v1/audit", headers=analyst_headers)
    assert response.status_code == 200
    assert "data" in response.json()
    assert isinstance(response.json()["data"], list)

@pytest.mark.asyncio
async def test_get_audit_by_entity(override_get_db, client: AsyncClient, analyst_headers):
    fake_id = str(uuid.uuid4())
    response = await client.get(f"/api/v1/audit/{fake_id}?entity_type=Observation", headers=analyst_headers)
    assert response.status_code == 200
    assert "data" in response.json()
    assert isinstance(response.json()["data"], list)

@pytest.mark.asyncio
async def test_get_provenance_not_found(override_get_db, client: AsyncClient, analyst_headers):
    fake_id = str(uuid.uuid4())
    response = await client.get(f"/api/v1/audit/provenance/{fake_id}", headers=analyst_headers)
    assert response.status_code == 404
    assert "not found" in response.json()["error"]
