import pytest
import pytest_asyncio
import jwt
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.main import app
from core.database import Base, get_db
from core.config import settings
from core.security import get_password_hash
from models.user import User, UserRole

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
async def test_user(db_session):
    user = User(
        username="test_auth_user",
        email="auth@astra.local",
        hashed_password=get_password_hash("secure_password"),
        role=UserRole.INCIDENT_RESPONDER,
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest_asyncio.fixture
async def inactive_user(db_session):
    user = User(
        username="inactive_user",
        email="inactive@astra.local",
        hashed_password=get_password_hash("secure_password"),
        role=UserRole.SOC_ANALYST,
        is_active=False
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_valid_login(override_get_db, async_client, test_user):
    response = await async_client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "test_auth_user", "password": "secure_password"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] > 0
    
    # Verify JWT claims
    token = data["access_token"]
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    assert payload["sub"] == str(test_user.id)
    assert payload["role"] == "Incident Responder"
    assert "exp" in payload
    assert "iat" in payload
    assert "password" not in payload
    assert "hashed_password" not in payload

@pytest.mark.asyncio
async def test_invalid_password(override_get_db, async_client, test_user):
    response = await async_client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "test_auth_user", "password": "wrong_password"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

@pytest.mark.asyncio
async def test_inactive_user_login(override_get_db, async_client, inactive_user):
    response = await async_client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "inactive_user", "password": "secure_password"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Inactive user"

@pytest.mark.asyncio
async def test_get_me_valid_token(override_get_db, async_client, test_user):
    # First login
    login_response = await async_client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "test_auth_user", "password": "secure_password"}
    )
    token = login_response.json()["access_token"]
    
    # Then get /me
    me_response = await async_client.get(
        f"{settings.API_V1_STR}/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert me_response.status_code == 200
    data = me_response.json()
    assert data["id"] == str(test_user.id)
    assert data["username"] == "test_auth_user"
    assert data["role"] == "Incident Responder"

@pytest.mark.asyncio
async def test_get_me_invalid_token(override_get_db, async_client):
    me_response = await async_client.get(
        f"{settings.API_V1_STR}/auth/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert me_response.status_code == 401

@pytest.mark.asyncio
async def test_get_me_expired_token(override_get_db, async_client, test_user):
    from core.security import create_access_token
    from datetime import timedelta
    
    # Create expired token
    token = create_access_token(str(test_user.id), test_user.role, expires_delta=timedelta(minutes=-1))
    
    me_response = await async_client.get(
        f"{settings.API_V1_STR}/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert me_response.status_code == 401

