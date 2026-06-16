from core.config import settings
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
async def users(db_session):
    sec_eng = User(username="sec", email="sec@test.com", hashed_password="pw", role=UserRole.SECURITY_ENGINEER)
    db_session.add(sec_eng)
    await db_session.commit()
    await db_session.refresh(sec_eng)
    
    token = create_access_token(str(sec_eng.id), sec_eng.role)
    return {"Authorization": f"Bearer {token}"}

@pytest_asyncio.fixture
async def client():
    # Use httpx.ASGITransport directly if needed, but app=app works in this version, or override if needed.
    # To match test_users exactly:
    from httpx import ASGITransport
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def auth_headers(users):
    return users

@pytest.fixture
def unauth_headers():
    # Helper to generate a valid JWT token for an UNAUTHORIZED role (wait, all active roles are authorized in prompt, so let's test missing token)
    return {}

@pytest.mark.asyncio
async def test_get_rules_unauthorized(override_get_db, client: AsyncClient, unauth_headers):
    response = await client.get("/api/v1/correlations/rules", headers=unauth_headers)
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_rules(override_get_db, client: AsyncClient, auth_headers):
    response = await client.get("/api/v1/correlations/rules", headers=auth_headers)
    assert response.status_code == 200
    assert "data" in response.json()
    assert isinstance(response.json()["data"], list)

@pytest.mark.asyncio
async def test_get_matches(override_get_db, client: AsyncClient, auth_headers):
    response = await client.get("/api/v1/correlations/matches", headers=auth_headers)
    assert response.status_code == 200
    assert "data" in response.json()
    assert isinstance(response.json()["data"], list)

@pytest.mark.asyncio
async def test_get_correlations_alias(override_get_db, client: AsyncClient, auth_headers):
    response = await client.get("/api/v1/correlations", headers=auth_headers)
    assert response.status_code == 200
    assert "data" in response.json()

@pytest.mark.asyncio
async def test_get_match_not_found(override_get_db, client: AsyncClient, auth_headers):
    fake_id = str(uuid.uuid4())
    response = await client.get(f"/api/v1/correlations/{fake_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["error"] == "Correlation match not found"

@pytest.mark.asyncio
async def test_matches_filtering(override_get_db, client: AsyncClient, auth_headers):
    response = await client.get("/api/v1/correlations/matches?min_score=50&limit=10", headers=auth_headers)
    assert response.status_code == 200
    assert "data" in response.json()

