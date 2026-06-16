"""Tests for CaseRepository — CRUD, filtering, assignment, status changes."""
import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock, patch
from models.case import Case, CaseStatus, CasePriority, CaseSeverity
from repositories.case import CaseRepository
from schemas.case import CaseCreate


@pytest.fixture
def mock_session():
    session = AsyncMock()
    session.add = MagicMock()
    return session


@pytest.fixture
def repo(mock_session):
    return CaseRepository(mock_session)


@pytest.mark.asyncio
async def test_create(repo, mock_session):
    data = CaseCreate(title="Test Case", description="Desc", priority=CasePriority.HIGH, severity=CaseSeverity.CRITICAL)

    async def refresh_side_effect(obj):
        obj.id = uuid.uuid4()
    mock_session.refresh.side_effect = refresh_side_effect

    case = await repo.create(data, created_by="user1")

    assert case.title == "Test Case"
    assert case.description == "Desc"
    assert case.priority == CasePriority.HIGH
    assert case.severity == CaseSeverity.CRITICAL
    assert case.status == CaseStatus.DRAFT
    assert case.created_by == "user1"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_get_by_id(repo, mock_session):
    case_id = uuid.uuid4()
    expected = Case(id=case_id, title="Found")

    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = expected
    mock_session.execute.return_value = mock_result

    result = await repo.get_by_id(case_id)
    assert result == expected
    mock_session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_by_id_not_found(repo, mock_session):
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_session.execute.return_value = mock_result

    result = await repo.get_by_id(uuid.uuid4())
    assert result is None


@pytest.mark.asyncio
async def test_list_no_filters(repo, mock_session):
    case1 = Case(id=uuid.uuid4(), title="Case 1")
    case2 = Case(id=uuid.uuid4(), title="Case 2")

    # First call returns total count, second returns results
    count_result = MagicMock()
    count_result.scalar.return_value = 2

    list_result = MagicMock()
    list_result.scalars.return_value.all.return_value = [case1, case2]

    mock_session.execute.side_effect = [count_result, list_result]

    cases, total = await repo.list(skip=0, limit=50)
    assert total == 2
    assert len(cases) == 2


@pytest.mark.asyncio
async def test_list_with_status_filter(repo, mock_session):
    count_result = MagicMock()
    count_result.scalar.return_value = 1

    list_result = MagicMock()
    list_result.scalars.return_value.all.return_value = [Case(id=uuid.uuid4(), title="Open Case")]

    mock_session.execute.side_effect = [count_result, list_result]

    cases, total = await repo.list(status=CaseStatus.OPEN)
    assert total == 1
    assert len(cases) == 1


@pytest.mark.asyncio
async def test_list_with_all_filters(repo, mock_session):
    count_result = MagicMock()
    count_result.scalar.return_value = 0

    list_result = MagicMock()
    list_result.scalars.return_value.all.return_value = []

    mock_session.execute.side_effect = [count_result, list_result]

    cases, total = await repo.list(
        status=CaseStatus.INVESTIGATING,
        priority=CasePriority.CRITICAL,
        severity=CaseSeverity.HIGH,
        assigned_to="analyst-1",
    )
    assert total == 0
    assert len(cases) == 0


@pytest.mark.asyncio
async def test_update(repo, mock_session):
    case = Case(id=uuid.uuid4(), title="Updated")
    result = await repo.update(case)
    mock_session.add.assert_called_once_with(case)
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(case)


@pytest.mark.asyncio
async def test_assign(repo, mock_session):
    case = Case(id=uuid.uuid4(), title="Assign Test", assigned_to=None)
    result = await repo.assign(case, "analyst-1")
    assert case.assigned_to == "analyst-1"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_change_status(repo, mock_session):
    case = Case(id=uuid.uuid4(), title="Status Test", status=CaseStatus.DRAFT)
    result = await repo.change_status(case, CaseStatus.OPEN)
    assert case.status == CaseStatus.OPEN
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
