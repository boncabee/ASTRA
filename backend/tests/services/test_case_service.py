"""Tests for CaseService — create, assign, change_status, update with audit + timeline."""
import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock, patch
from models.case import Case, CaseStatus, CasePriority, CaseSeverity, TimelineEventType
from services.case import CaseService
from schemas.case import CaseCreate, CaseUpdate


@pytest.fixture
def mock_session():
    return AsyncMock()


@pytest.fixture
def service(mock_session):
    return CaseService(mock_session)


@pytest.fixture
def mock_case():
    return Case(
        id=uuid.uuid4(),
        title="Test Case",
        description="Desc",
        status=CaseStatus.DRAFT,
        priority=CasePriority.MEDIUM,
        severity=CaseSeverity.MEDIUM,
        created_by="user1",
        assigned_to=None,
    )


@pytest.fixture
def mock_open_case():
    return Case(
        id=uuid.uuid4(),
        title="Open Case",
        status=CaseStatus.OPEN,
        priority=CasePriority.HIGH,
        severity=CaseSeverity.HIGH,
        created_by="user1",
        assigned_to="analyst-1",
    )


@pytest.fixture
def mock_resolved_case():
    return Case(
        id=uuid.uuid4(),
        title="Resolved Case",
        status=CaseStatus.RESOLVED,
        priority=CasePriority.MEDIUM,
        severity=CaseSeverity.MEDIUM,
        created_by="user1",
        assigned_to="analyst-1",
    )


class TestCreateCase:
    @pytest.mark.asyncio
    async def test_create_case_success(self, service, monkeypatch):
        data = CaseCreate(title="New Case", priority=CasePriority.HIGH, severity=CaseSeverity.CRITICAL)
        created_case = Case(
            id=uuid.uuid4(), title="New Case", status=CaseStatus.DRAFT,
            priority=CasePriority.HIGH, severity=CaseSeverity.CRITICAL,
            created_by="user1",
        )

        monkeypatch.setattr(service.case_repo, "create", AsyncMock(return_value=created_case))
        monkeypatch.setattr(service.timeline_service, "record_event", AsyncMock())
        monkeypatch.setattr(service.audit_repo, "create_event", AsyncMock())

        result = await service.create_case(data, created_by="user1")

        assert result.title == "New Case"
        assert result.status == CaseStatus.DRAFT
        service.case_repo.create.assert_called_once()
        service.timeline_service.record_event.assert_called_once()
        service.audit_repo.create_event.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_case_timeline_event_type(self, service, monkeypatch):
        data = CaseCreate(title="Timeline Test")
        created_case = Case(id=uuid.uuid4(), title="Timeline Test", status=CaseStatus.DRAFT, created_by="user1")

        monkeypatch.setattr(service.case_repo, "create", AsyncMock(return_value=created_case))
        monkeypatch.setattr(service.timeline_service, "record_event", AsyncMock())
        monkeypatch.setattr(service.audit_repo, "create_event", AsyncMock())

        await service.create_case(data, created_by="user1")

        call_kwargs = service.timeline_service.record_event.call_args
        assert call_kwargs.kwargs["event_type"] == TimelineEventType.CASE_CREATED

    @pytest.mark.asyncio
    async def test_create_case_audit_action(self, service, monkeypatch):
        data = CaseCreate(title="Audit Test")
        created_case = Case(id=uuid.uuid4(), title="Audit Test", status=CaseStatus.DRAFT, created_by="user1")

        monkeypatch.setattr(service.case_repo, "create", AsyncMock(return_value=created_case))
        monkeypatch.setattr(service.timeline_service, "record_event", AsyncMock())
        monkeypatch.setattr(service.audit_repo, "create_event", AsyncMock())

        await service.create_case(data, created_by="user1")

        audit_call = service.audit_repo.create_event.call_args[0][0]
        assert audit_call.entity_type == "CASE"
        assert audit_call.action == "CREATED"
        assert audit_call.actor == "user1"


class TestAssignCase:
    @pytest.mark.asyncio
    async def test_assign_success(self, service, mock_case, monkeypatch):
        monkeypatch.setattr(service.case_repo, "get_by_id", AsyncMock(return_value=mock_case))
        monkeypatch.setattr(service.case_repo, "assign", AsyncMock(return_value=mock_case))
        monkeypatch.setattr(service.assignment_repo, "create", AsyncMock())
        monkeypatch.setattr(service.timeline_service, "record_event", AsyncMock())
        monkeypatch.setattr(service.audit_repo, "create_event", AsyncMock())

        result = await service.assign_case(mock_case.id, "analyst-1", "manager-1")

        service.case_repo.assign.assert_called_once()
        service.assignment_repo.create.assert_called_once()
        service.timeline_service.record_event.assert_called_once()
        service.audit_repo.create_event.assert_called_once()

    @pytest.mark.asyncio
    async def test_assign_records_timeline(self, service, mock_case, monkeypatch):
        monkeypatch.setattr(service.case_repo, "get_by_id", AsyncMock(return_value=mock_case))
        monkeypatch.setattr(service.case_repo, "assign", AsyncMock(return_value=mock_case))
        monkeypatch.setattr(service.assignment_repo, "create", AsyncMock())
        monkeypatch.setattr(service.timeline_service, "record_event", AsyncMock())
        monkeypatch.setattr(service.audit_repo, "create_event", AsyncMock())

        await service.assign_case(mock_case.id, "analyst-1", "manager-1")

        call_kwargs = service.timeline_service.record_event.call_args.kwargs
        assert call_kwargs["event_type"] == TimelineEventType.ASSIGNMENT

    @pytest.mark.asyncio
    async def test_assign_not_found(self, service, monkeypatch):
        monkeypatch.setattr(service.case_repo, "get_by_id", AsyncMock(return_value=None))

        with pytest.raises(ValueError, match="not found"):
            await service.assign_case(uuid.uuid4(), "analyst-1", "manager-1")

    @pytest.mark.asyncio
    async def test_assign_audit_records_old_and_new(self, service, mock_case, monkeypatch):
        mock_case.assigned_to = "old-analyst"
        monkeypatch.setattr(service.case_repo, "get_by_id", AsyncMock(return_value=mock_case))
        monkeypatch.setattr(service.case_repo, "assign", AsyncMock(return_value=mock_case))
        monkeypatch.setattr(service.assignment_repo, "create", AsyncMock())
        monkeypatch.setattr(service.timeline_service, "record_event", AsyncMock())
        monkeypatch.setattr(service.audit_repo, "create_event", AsyncMock())

        await service.assign_case(mock_case.id, "new-analyst", "manager-1")

        audit_call = service.audit_repo.create_event.call_args[0][0]
        assert audit_call.old_value == {"assigned_to": "old-analyst"}
        assert audit_call.new_value == {"assigned_to": "new-analyst"}


class TestChangeStatus:
    @pytest.mark.asyncio
    async def test_valid_transition(self, service, mock_case, monkeypatch):
        monkeypatch.setattr(service.case_repo, "get_by_id", AsyncMock(return_value=mock_case))
        monkeypatch.setattr(service.case_repo, "change_status", AsyncMock(return_value=mock_case))
        monkeypatch.setattr(service.timeline_service, "record_event", AsyncMock())
        monkeypatch.setattr(service.audit_repo, "create_event", AsyncMock())

        result = await service.change_status(
            mock_case.id, CaseStatus.OPEN, actor="user1", actor_role="SOC_ANALYST"
        )

        service.case_repo.change_status.assert_called_once()
        service.timeline_service.record_event.assert_called_once()
        service.audit_repo.create_event.assert_called_once()

    @pytest.mark.asyncio
    async def test_forbidden_transition_raises(self, service, mock_case, monkeypatch):
        monkeypatch.setattr(service.case_repo, "get_by_id", AsyncMock(return_value=mock_case))

        with pytest.raises(ValueError, match="Invalid transition"):
            await service.change_status(
                mock_case.id, CaseStatus.CLOSED, actor="user1", actor_role="SOC_ANALYST"
            )

    @pytest.mark.asyncio
    async def test_case_not_found(self, service, monkeypatch):
        monkeypatch.setattr(service.case_repo, "get_by_id", AsyncMock(return_value=None))

        with pytest.raises(ValueError, match="not found"):
            await service.change_status(
                uuid.uuid4(), CaseStatus.OPEN, actor="user1", actor_role="SOC_ANALYST"
            )

    @pytest.mark.asyncio
    async def test_close_requires_role(self, service, mock_resolved_case, monkeypatch):
        monkeypatch.setattr(service.case_repo, "get_by_id", AsyncMock(return_value=mock_resolved_case))

        with pytest.raises(PermissionError, match="not authorized to close"):
            await service.change_status(
                mock_resolved_case.id, CaseStatus.CLOSED,
                actor="analyst", actor_role="SOC_ANALYST",
            )

    @pytest.mark.asyncio
    async def test_close_allowed_for_manager(self, service, mock_resolved_case, monkeypatch):
        monkeypatch.setattr(service.case_repo, "get_by_id", AsyncMock(return_value=mock_resolved_case))
        monkeypatch.setattr(service.case_repo, "change_status", AsyncMock(return_value=mock_resolved_case))
        monkeypatch.setattr(service.timeline_service, "record_event", AsyncMock())
        monkeypatch.setattr(service.audit_repo, "create_event", AsyncMock())

        result = await service.change_status(
            mock_resolved_case.id, CaseStatus.CLOSED,
            actor="manager1", actor_role="Security Engineer",
        )

        service.case_repo.change_status.assert_called_once()

    @pytest.mark.asyncio
    async def test_cancel_requires_role(self, service, mock_case, monkeypatch):
        """SOC Analyst cannot cancel cases."""
        monkeypatch.setattr(service.case_repo, "get_by_id", AsyncMock(return_value=mock_case))

        with pytest.raises(PermissionError, match="not authorized to cancel"):
            await service.change_status(
                mock_case.id, CaseStatus.CANCELLED,
                actor="analyst", actor_role="SOC_ANALYST",
            )

    @pytest.mark.asyncio
    async def test_cancel_allowed_for_responder(self, service, mock_case, monkeypatch):
        monkeypatch.setattr(service.case_repo, "get_by_id", AsyncMock(return_value=mock_case))
        monkeypatch.setattr(service.case_repo, "change_status", AsyncMock(return_value=mock_case))
        monkeypatch.setattr(service.timeline_service, "record_event", AsyncMock())
        monkeypatch.setattr(service.audit_repo, "create_event", AsyncMock())

        result = await service.change_status(
            mock_case.id, CaseStatus.CANCELLED,
            actor="responder1", actor_role="Incident Responder",
        )

        service.case_repo.change_status.assert_called_once()

    @pytest.mark.asyncio
    async def test_status_change_with_reason(self, service, mock_case, monkeypatch):
        monkeypatch.setattr(service.case_repo, "get_by_id", AsyncMock(return_value=mock_case))
        monkeypatch.setattr(service.case_repo, "change_status", AsyncMock(return_value=mock_case))
        monkeypatch.setattr(service.timeline_service, "record_event", AsyncMock())
        monkeypatch.setattr(service.audit_repo, "create_event", AsyncMock())

        await service.change_status(
            mock_case.id, CaseStatus.OPEN,
            actor="user1", actor_role="SOC_ANALYST",
            reason="Promoting to open",
        )

        audit_call = service.audit_repo.create_event.call_args[0][0]
        assert audit_call.reason == "Promoting to open"

    @pytest.mark.asyncio
    async def test_status_change_timeline_metadata(self, service, mock_case, monkeypatch):
        monkeypatch.setattr(service.case_repo, "get_by_id", AsyncMock(return_value=mock_case))
        monkeypatch.setattr(service.case_repo, "change_status", AsyncMock(return_value=mock_case))
        monkeypatch.setattr(service.timeline_service, "record_event", AsyncMock())
        monkeypatch.setattr(service.audit_repo, "create_event", AsyncMock())

        await service.change_status(
            mock_case.id, CaseStatus.OPEN,
            actor="user1", actor_role="SOC_ANALYST",
        )

        call_kwargs = service.timeline_service.record_event.call_args.kwargs
        assert call_kwargs["event_type"] == TimelineEventType.STATUS_CHANGE
        assert "previous_status" in call_kwargs["event_metadata"]
        assert "new_status" in call_kwargs["event_metadata"]


class TestGetAndListCases:
    @pytest.mark.asyncio
    async def test_get_case(self, service, mock_case, monkeypatch):
        monkeypatch.setattr(service.case_repo, "get_by_id", AsyncMock(return_value=mock_case))
        result = await service.get_case(mock_case.id)
        assert result == mock_case

    @pytest.mark.asyncio
    async def test_list_cases(self, service, monkeypatch):
        monkeypatch.setattr(service.case_repo, "list", AsyncMock(return_value=([], 0)))
        cases, total = await service.list_cases()
        assert total == 0
        assert cases == []


class TestUpdateCase:
    @pytest.mark.asyncio
    async def test_update_title(self, service, mock_case, monkeypatch):
        monkeypatch.setattr(service.case_repo, "get_by_id", AsyncMock(return_value=mock_case))
        monkeypatch.setattr(service.case_repo, "update", AsyncMock(return_value=mock_case))
        monkeypatch.setattr(service.audit_repo, "create_event", AsyncMock())

        data = CaseUpdate(title="Updated Title")
        result = await service.update_case(mock_case.id, data, actor="user1")

        service.case_repo.update.assert_called_once()
        service.audit_repo.create_event.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_no_changes_skips_audit(self, service, mock_case, monkeypatch):
        monkeypatch.setattr(service.case_repo, "get_by_id", AsyncMock(return_value=mock_case))
        monkeypatch.setattr(service.case_repo, "update", AsyncMock(return_value=mock_case))
        monkeypatch.setattr(service.audit_repo, "create_event", AsyncMock())

        data = CaseUpdate()  # No fields set
        await service.update_case(mock_case.id, data, actor="user1")

        service.audit_repo.create_event.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_not_found(self, service, monkeypatch):
        monkeypatch.setattr(service.case_repo, "get_by_id", AsyncMock(return_value=None))

        with pytest.raises(ValueError, match="not found"):
            await service.update_case(uuid.uuid4(), CaseUpdate(title="New"), actor="user1")

    @pytest.mark.asyncio
    async def test_update_description(self, service, mock_case, monkeypatch):
        monkeypatch.setattr(service.case_repo, "get_by_id", AsyncMock(return_value=mock_case))
        monkeypatch.setattr(service.case_repo, "update", AsyncMock(return_value=mock_case))
        monkeypatch.setattr(service.audit_repo, "create_event", AsyncMock())

        data = CaseUpdate(description="New description")
        await service.update_case(mock_case.id, data, actor="user1")

        service.audit_repo.create_event.assert_called_once()
        audit_call = service.audit_repo.create_event.call_args[0][0]
        assert "description" in audit_call.new_value

    @pytest.mark.asyncio
    async def test_update_priority(self, service, mock_case, monkeypatch):
        monkeypatch.setattr(service.case_repo, "get_by_id", AsyncMock(return_value=mock_case))
        monkeypatch.setattr(service.case_repo, "update", AsyncMock(return_value=mock_case))
        monkeypatch.setattr(service.audit_repo, "create_event", AsyncMock())

        data = CaseUpdate(priority=CasePriority.CRITICAL)
        await service.update_case(mock_case.id, data, actor="user1")

        service.audit_repo.create_event.assert_called_once()
        audit_call = service.audit_repo.create_event.call_args[0][0]
        assert audit_call.new_value["priority"] == "CRITICAL"

    @pytest.mark.asyncio
    async def test_update_severity(self, service, mock_case, monkeypatch):
        monkeypatch.setattr(service.case_repo, "get_by_id", AsyncMock(return_value=mock_case))
        monkeypatch.setattr(service.case_repo, "update", AsyncMock(return_value=mock_case))
        monkeypatch.setattr(service.audit_repo, "create_event", AsyncMock())

        data = CaseUpdate(severity=CaseSeverity.CRITICAL)
        await service.update_case(mock_case.id, data, actor="user1")

        service.audit_repo.create_event.assert_called_once()
        audit_call = service.audit_repo.create_event.call_args[0][0]
        assert audit_call.new_value["severity"] == "CRITICAL"

    @pytest.mark.asyncio
    async def test_update_all_fields(self, service, mock_case, monkeypatch):
        monkeypatch.setattr(service.case_repo, "get_by_id", AsyncMock(return_value=mock_case))
        monkeypatch.setattr(service.case_repo, "update", AsyncMock(return_value=mock_case))
        monkeypatch.setattr(service.audit_repo, "create_event", AsyncMock())

        data = CaseUpdate(
            title="New Title",
            description="New Desc",
            priority=CasePriority.HIGH,
            severity=CaseSeverity.LOW,
        )
        await service.update_case(mock_case.id, data, actor="user1")

        audit_call = service.audit_repo.create_event.call_args[0][0]
        assert "title" in audit_call.new_value
        assert "description" in audit_call.new_value
        assert "priority" in audit_call.new_value
        assert "severity" in audit_call.new_value

