from core.config import settings
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from core.database import Base
from models.user import User, UserRole

@pytest_asyncio.fixture
async def async_session():
    engine = create_async_engine(settings.TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with SessionLocal() as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.mark.asyncio
async def test_create_user(async_session):
    user = User(
        username="test_admin",
        email="admin@astra.local",
        hashed_password="hashed_password",
        role=UserRole.ADMINISTRATOR
    )
    async_session.add(user)
    await async_session.commit()
    
    # Verify User creation
    stmt = select(User).where(User.username == "test_admin")
    result = await async_session.execute(stmt)
    db_user = result.scalar_one_or_none()
    
    assert db_user is not None
    assert db_user.email == "admin@astra.local"
    assert db_user.role == UserRole.ADMINISTRATOR
    assert db_user.is_active is True
    assert db_user.created_at is not None
    assert db_user.updated_at is not None

@pytest.mark.asyncio
async def test_unique_username_constraint(async_session):
    user1 = User(
        username="duplicate",
        email="dup1@astra.local",
        hashed_password="pw",
        role=UserRole.SOC_ANALYST
    )
    async_session.add(user1)
    await async_session.commit()
    
    user2 = User(
        username="duplicate",
        email="dup2@astra.local",
        hashed_password="pw",
        role=UserRole.SOC_ANALYST
    )
    async_session.add(user2)
    with pytest.raises(IntegrityError):
        await async_session.commit()

@pytest.mark.asyncio
async def test_unique_email_constraint(async_session):
    user1 = User(
        username="user1",
        email="duplicate@astra.local",
        hashed_password="pw",
        role=UserRole.SOC_ANALYST
    )
    async_session.add(user1)
    await async_session.commit()
    
    user2 = User(
        username="user2",
        email="duplicate@astra.local",
        hashed_password="pw",
        role=UserRole.SOC_ANALYST
    )
    async_session.add(user2)
    with pytest.raises(IntegrityError):
        await async_session.commit()

@pytest.mark.asyncio
async def test_role_enum_values(async_session):
    # Ensure role is mapped properly using the Enum
    user = User(
        username="sec_eng",
        email="eng@astra.local",
        hashed_password="pw",
        role=UserRole.SECURITY_ENGINEER
    )
    async_session.add(user)
    await async_session.commit()
    
    stmt = select(User).where(User.username == "sec_eng")
    result = await async_session.execute(stmt)
    db_user = result.scalar_one_or_none()
    
    assert db_user.role == "Security Engineer"

