import pytest
import pytest_asyncio
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from core.database import Base
from models.evidence import EvidenceType
from schemas.evidence import EvidenceCreate, AuditEventCreate
from repositories.evidence import EvidenceRepository, AuditRepository

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

@pytest.mark.asyncio
async def test_create_and_get_evidence(db_session):
    repo = EvidenceRepository(db_session)
    obs_id = uuid.uuid4()
    
    obj_in = EvidenceCreate(
        observation_id=obs_id,
        evidence_type=EvidenceType.SYSTEM_EVENT,
        source="TestSystem",
        content_reference="s3://test/file.json",
        hash_value="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )
    
    evidence = await repo.create_evidence(obj_in, "sysadmin")
    assert evidence.id is not None
    assert evidence.created_at is not None
    assert evidence.evidence_type == EvidenceType.SYSTEM_EVENT
    
    fetched = await repo.get_evidence_by_id(evidence.id)
    assert fetched is not None
    assert fetched.hash_value == obj_in.hash_value
    
    list_obs = await repo.get_evidence_by_observation(obs_id)
    assert len(list_obs) == 1

@pytest.mark.asyncio
async def test_create_and_get_audit_event(db_session):
    repo = AuditRepository(db_session)
    ent_id = uuid.uuid4()
    
    obj_in = AuditEventCreate(
        entity_type="Observation",
        entity_id=ent_id,
        action="UPDATE_STATUS",
        actor="analyst1",
        old_value={"status": "NEW"},
        new_value={"status": "UNDER_REVIEW"},
        reason="Manual investigation started"
    )
    
    event = await repo.create_event(obj_in)
    assert event.id is not None
    assert event.timestamp is not None
    assert event.old_value["status"] == "NEW"
    
    events_list = await repo.get_events_by_entity("Observation", ent_id)
    assert len(events_list) == 1
    assert events_list[0].action == "UPDATE_STATUS"

@pytest.mark.asyncio
async def test_evidence_pagination(db_session):
    repo = EvidenceRepository(db_session)
    obs_id = uuid.uuid4()
    
    for i in range(15):
        await repo.create_evidence(
            EvidenceCreate(
                observation_id=obs_id,
                evidence_type=EvidenceType.MANUAL_NOTE,
                source="User",
                content_reference=f"note_{i}",
                hash_value="hash"
            ), "tester"
        )
        
    items, total = await repo.list_evidence(skip=0, limit=10)
    assert total >= 15
    assert len(items) == 10
    
    items_page2, _ = await repo.list_evidence(skip=10, limit=10)
    assert len(items_page2) >= 5
