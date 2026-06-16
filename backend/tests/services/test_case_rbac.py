"""Tests for Case RBAC enforcement — role-gated close/cancel in CaseService."""
import pytest
import uuid
from unittest.mock import AsyncMock
from models.case import Case, CaseStatus, CasePriority, CaseSeverity
from services.case import CaseService
from services.case_state_machine import can_close, can_cancel


@pytest.fixture
def mock_session():
    return AsyncMock()

@pytest.fixture
def service(mock_session):
    return CaseService(mock_session)

@pytest.fixture
def draft_case():
    return Case(id=uuid.uuid4(), title="Draft", status=CaseStatus.DRAFT, priority=CasePriority.MEDIUM, severity=CaseSeverity.MEDIUM, created_by="u")

@pytest.fixture
def resolved_case():
    return Case(id=uuid.uuid4(), title="Resolved", status=CaseStatus.RESOLVED, priority=CasePriority.MEDIUM, severity=CaseSeverity.MEDIUM, created_by="u", assigned_to="a")


class TestCloseRBAC:
    """Only Manager (Security Engineer) and Administrator can close cases."""

    @pytest.mark.asyncio
    async def test_admin_can_close(self, service, resolved_case, monkeypatch):
        monkeypatch.setattr(service.case_repo, "get_by_id", AsyncMock(return_value=resolved_case))
        monkeypatch.setattr(service.case_repo, "change_status", AsyncMock(return_value=resolved_case))
        monkeypatch.setattr(service.timeline_service, "record_event", AsyncMock())
        monkeypatch.setattr(service.audit_repo, "create_event", AsyncMock())
        await service.change_status(resolved_case.id, CaseStatus.CLOSED, "admin", "Administrator")
        service.case_repo.change_status.assert_called_once()

    @pytest.mark.asyncio
    async def test_sec_engineer_can_close(self, service, resolved_case, monkeypatch):
        monkeypatch.setattr(service.case_repo, "get_by_id", AsyncMock(return_value=resolved_case))
        monkeypatch.setattr(service.case_repo, "change_status", AsyncMock(return_value=resolved_case))
        monkeypatch.setattr(service.timeline_service, "record_event", AsyncMock())
        monkeypatch.setattr(service.audit_repo, "create_event", AsyncMock())
        await service.change_status(resolved_case.id, CaseStatus.CLOSED, "eng", "Security Engineer")
        service.case_repo.change_status.assert_called_once()

    @pytest.mark.asyncio
    async def test_soc_analyst_cannot_close(self, service, resolved_case, monkeypatch):
        monkeypatch.setattr(service.case_repo, "get_by_id", AsyncMock(return_value=resolved_case))
        with pytest.raises(PermissionError, match="not authorized to close"):
            await service.change_status(resolved_case.id, CaseStatus.CLOSED, "a", "SOC Analyst")

    @pytest.mark.asyncio
    async def test_responder_cannot_close(self, service, resolved_case, monkeypatch):
        monkeypatch.setattr(service.case_repo, "get_by_id", AsyncMock(return_value=resolved_case))
        with pytest.raises(PermissionError, match="not authorized to close"):
            await service.change_status(resolved_case.id, CaseStatus.CLOSED, "r", "Incident Responder")


class TestCancelRBAC:
    """Responder, Manager, and Administrator can cancel; SOC Analyst cannot."""

    @pytest.mark.asyncio
    async def test_admin_can_cancel(self, service, draft_case, monkeypatch):
        monkeypatch.setattr(service.case_repo, "get_by_id", AsyncMock(return_value=draft_case))
        monkeypatch.setattr(service.case_repo, "change_status", AsyncMock(return_value=draft_case))
        monkeypatch.setattr(service.timeline_service, "record_event", AsyncMock())
        monkeypatch.setattr(service.audit_repo, "create_event", AsyncMock())
        await service.change_status(draft_case.id, CaseStatus.CANCELLED, "admin", "Administrator")
        service.case_repo.change_status.assert_called_once()

    @pytest.mark.asyncio
    async def test_responder_can_cancel(self, service, draft_case, monkeypatch):
        monkeypatch.setattr(service.case_repo, "get_by_id", AsyncMock(return_value=draft_case))
        monkeypatch.setattr(service.case_repo, "change_status", AsyncMock(return_value=draft_case))
        monkeypatch.setattr(service.timeline_service, "record_event", AsyncMock())
        monkeypatch.setattr(service.audit_repo, "create_event", AsyncMock())
        await service.change_status(draft_case.id, CaseStatus.CANCELLED, "r", "Incident Responder")
        service.case_repo.change_status.assert_called_once()

    @pytest.mark.asyncio
    async def test_sec_engineer_can_cancel(self, service, draft_case, monkeypatch):
        monkeypatch.setattr(service.case_repo, "get_by_id", AsyncMock(return_value=draft_case))
        monkeypatch.setattr(service.case_repo, "change_status", AsyncMock(return_value=draft_case))
        monkeypatch.setattr(service.timeline_service, "record_event", AsyncMock())
        monkeypatch.setattr(service.audit_repo, "create_event", AsyncMock())
        await service.change_status(draft_case.id, CaseStatus.CANCELLED, "e", "Security Engineer")
        service.case_repo.change_status.assert_called_once()

    @pytest.mark.asyncio
    async def test_soc_analyst_cannot_cancel(self, service, draft_case, monkeypatch):
        monkeypatch.setattr(service.case_repo, "get_by_id", AsyncMock(return_value=draft_case))
        with pytest.raises(PermissionError, match="not authorized to cancel"):
            await service.change_status(draft_case.id, CaseStatus.CANCELLED, "a", "SOC Analyst")


class TestStateMachineRoleFunctions:
    """Direct tests of role-checking functions."""

    def test_can_close_values(self):
        assert can_close("Administrator") is True
        assert can_close("ADMINISTRATOR") is True
        assert can_close("Security Engineer") is True
        assert can_close("SECURITY_ENGINEER") is True
        assert can_close("SOC Analyst") is False
        assert can_close("SOC_ANALYST") is False
        assert can_close("Incident Responder") is False
        assert can_close("INCIDENT_RESPONDER") is False

    def test_can_cancel_values(self):
        assert can_cancel("Administrator") is True
        assert can_cancel("ADMINISTRATOR") is True
        assert can_cancel("Security Engineer") is True
        assert can_cancel("SECURITY_ENGINEER") is True
        assert can_cancel("Incident Responder") is True
        assert can_cancel("INCIDENT_RESPONDER") is True
        assert can_cancel("SOC Analyst") is False
        assert can_cancel("SOC_ANALYST") is False
