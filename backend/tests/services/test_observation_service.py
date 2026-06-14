import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock
from models.correlation import CorrelationMatch
from models.observation import Observation, ObservationStatus
from services.observation import ObservationService
from schemas.observation import ObservationCreate

@pytest.fixture
def mock_session():
    return AsyncMock()

@pytest.fixture
def mock_repo():
    repo = MagicMock()
    repo.get_by_correlation_id = AsyncMock(return_value=None)
    repo.create = AsyncMock()
    repo.update = AsyncMock()
    return repo

@pytest.mark.asyncio
async def test_process_correlation_match(mock_session, mock_repo, monkeypatch):
    service = ObservationService(mock_session)
    monkeypatch.setattr(service, "repository", mock_repo)
    
    match_id = uuid.uuid4()
    match = CorrelationMatch(
        id=match_id,
        rule_id=uuid.uuid4(),
        event_count=5,
        correlation_score=20
    )
    
    # Mock create to return the created observation
    async def mock_create(data: ObservationCreate, created_by: str):
        return Observation(**data.model_dump(), id=uuid.uuid4())
    mock_repo.create.side_effect = mock_create
    
    obs = await service.process_correlation_match(match, run_by_user_id="system")
    
    assert obs is not None
    assert obs.correlation_id == match_id
    assert obs.status == ObservationStatus.NEW
    # score = 20 (score) + 5 (events) + 50 (asset) = 75
    assert obs.risk_score == 75
    mock_repo.create.assert_called_once()

@pytest.mark.asyncio
async def test_process_correlation_match_duplicate(mock_session, mock_repo, monkeypatch):
    service = ObservationService(mock_session)
    monkeypatch.setattr(service, "repository", mock_repo)
    
    existing_obs = Observation(id=uuid.uuid4())
    mock_repo.get_by_correlation_id = AsyncMock(return_value=existing_obs)
    
    match = CorrelationMatch(id=uuid.uuid4())
    obs = await service.process_correlation_match(match, "system")
    
    assert obs == existing_obs
    mock_repo.create.assert_not_called()

@pytest.mark.asyncio
async def test_update_status_valid(mock_session, mock_repo, monkeypatch):
    service = ObservationService(mock_session)
    monkeypatch.setattr(service, "repository", mock_repo)
    
    obs = Observation(id=uuid.uuid4(), status=ObservationStatus.NEW)
    
    async def mock_update(o: Observation):
        return o
    mock_repo.update.side_effect = mock_update
    
    updated = await service.update_status(obs, ObservationStatus.POLICY_EVALUATED, "user1")
    
    assert updated.status == ObservationStatus.POLICY_EVALUATED
    assert updated.updated_by == "user1"
    mock_repo.update.assert_called_once()

@pytest.mark.asyncio
async def test_update_status_invalid(mock_session, mock_repo, monkeypatch):
    service = ObservationService(mock_session)
    monkeypatch.setattr(service, "repository", mock_repo)
    
    obs = Observation(id=uuid.uuid4(), status=ObservationStatus.NEW)
    
    with pytest.raises(ValueError, match="Invalid transition"):
        await service.update_status(obs, ObservationStatus.RESOLVED, "user1")
