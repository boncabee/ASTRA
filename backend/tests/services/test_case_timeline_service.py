"""Tests for TimelineService — append-only, immutability enforcement."""
import pytest
import uuid
from unittest.mock import AsyncMock
from models.case import CaseTimeline, TimelineEventType
from services.case_timeline import TimelineService


@pytest.fixture
def mock_session():
    return AsyncMock()

@pytest.fixture
def service(mock_session):
    return TimelineService(mock_session)


class TestRecordEvent:
    @pytest.mark.asyncio
    async def test_record_status_change(self, service, monkeypatch):
        case_id = uuid.uuid4()
        expected = CaseTimeline(id=uuid.uuid4(), case_id=case_id, event_type=TimelineEventType.STATUS_CHANGE, actor="user1", event_metadata={"old": "DRAFT", "new": "OPEN"})
        monkeypatch.setattr(service.timeline_repo, "create", AsyncMock(return_value=expected))
        result = await service.record_event(case_id=case_id, event_type=TimelineEventType.STATUS_CHANGE, actor="user1", event_metadata={"old": "DRAFT", "new": "OPEN"})
        assert result.event_type == TimelineEventType.STATUS_CHANGE
        service.timeline_repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_record_assignment(self, service, monkeypatch):
        case_id = uuid.uuid4()
        expected = CaseTimeline(id=uuid.uuid4(), case_id=case_id, event_type=TimelineEventType.ASSIGNMENT, actor="mgr")
        monkeypatch.setattr(service.timeline_repo, "create", AsyncMock(return_value=expected))
        result = await service.record_event(case_id=case_id, event_type=TimelineEventType.ASSIGNMENT, actor="mgr")
        assert result.event_type == TimelineEventType.ASSIGNMENT

    @pytest.mark.asyncio
    async def test_record_case_created(self, service, monkeypatch):
        case_id = uuid.uuid4()
        expected = CaseTimeline(id=uuid.uuid4(), case_id=case_id, event_type=TimelineEventType.CASE_CREATED, actor="sys")
        monkeypatch.setattr(service.timeline_repo, "create", AsyncMock(return_value=expected))
        result = await service.record_event(case_id=case_id, event_type=TimelineEventType.CASE_CREATED, actor="sys")
        assert result.event_type == TimelineEventType.CASE_CREATED

    @pytest.mark.asyncio
    async def test_record_system_action(self, service, monkeypatch):
        case_id = uuid.uuid4()
        expected = CaseTimeline(id=uuid.uuid4(), case_id=case_id, event_type=TimelineEventType.SYSTEM_ACTION, actor="SYSTEM")
        monkeypatch.setattr(service.timeline_repo, "create", AsyncMock(return_value=expected))
        result = await service.record_event(case_id=case_id, event_type=TimelineEventType.SYSTEM_ACTION, actor="SYSTEM")
        assert result.event_type == TimelineEventType.SYSTEM_ACTION

    @pytest.mark.asyncio
    async def test_validates_case_id(self, service):
        with pytest.raises(ValueError, match="case_id is required"):
            await service.record_event(case_id=None, event_type=TimelineEventType.STATUS_CHANGE, actor="u")

    @pytest.mark.asyncio
    async def test_validates_actor(self, service):
        with pytest.raises(ValueError, match="actor is required"):
            await service.record_event(case_id=uuid.uuid4(), event_type=TimelineEventType.STATUS_CHANGE, actor="")


class TestGetTimeline:
    @pytest.mark.asyncio
    async def test_get_timeline(self, service, monkeypatch):
        case_id = uuid.uuid4()
        events = [CaseTimeline(id=uuid.uuid4(), case_id=case_id, event_type=TimelineEventType.CASE_CREATED, actor="u")]
        monkeypatch.setattr(service.timeline_repo, "get_by_case_id", AsyncMock(return_value=(events, 1)))
        result, total = await service.get_timeline(case_id)
        assert total == 1
        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_get_timeline_empty(self, service, monkeypatch):
        monkeypatch.setattr(service.timeline_repo, "get_by_case_id", AsyncMock(return_value=([], 0)))
        result, total = await service.get_timeline(uuid.uuid4())
        assert total == 0


class TestImmutability:
    def test_no_update_method(self, service):
        assert not hasattr(service, "update_event")
        assert not hasattr(service, "update")

    def test_no_delete_method(self, service):
        assert not hasattr(service, "delete_event")
        assert not hasattr(service, "delete")

    def test_no_update_on_repo(self, service):
        assert not hasattr(service.timeline_repo, "update")

    def test_no_delete_on_repo(self, service):
        assert not hasattr(service.timeline_repo, "delete")
