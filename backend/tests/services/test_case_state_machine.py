"""Tests for the Case State Machine — transition validation, terminal states, role gating."""
import pytest
from models.case import CaseStatus
from services.case_state_machine import (
    validate_transition,
    get_allowed_transitions,
    is_terminal,
    can_close,
    can_cancel,
    TRANSITIONS,
    TERMINAL_STATES,
)


class TestTransitionMatrix:
    """Verify every valid transition from CASE_LIFECYCLE.md."""

    def test_draft_to_open(self):
        assert validate_transition(CaseStatus.DRAFT, CaseStatus.OPEN) is True

    def test_draft_to_cancelled(self):
        assert validate_transition(CaseStatus.DRAFT, CaseStatus.CANCELLED) is True

    def test_open_to_investigating(self):
        assert validate_transition(CaseStatus.OPEN, CaseStatus.INVESTIGATING) is True

    def test_open_to_cancelled(self):
        assert validate_transition(CaseStatus.OPEN, CaseStatus.CANCELLED) is True

    def test_investigating_to_mitigating(self):
        assert validate_transition(CaseStatus.INVESTIGATING, CaseStatus.MITIGATING) is True

    def test_investigating_to_resolved(self):
        assert validate_transition(CaseStatus.INVESTIGATING, CaseStatus.RESOLVED) is True

    def test_mitigating_to_monitoring(self):
        assert validate_transition(CaseStatus.MITIGATING, CaseStatus.MONITORING) is True

    def test_mitigating_to_investigating(self):
        assert validate_transition(CaseStatus.MITIGATING, CaseStatus.INVESTIGATING) is True

    def test_mitigating_to_resolved(self):
        assert validate_transition(CaseStatus.MITIGATING, CaseStatus.RESOLVED) is True

    def test_monitoring_to_resolved(self):
        assert validate_transition(CaseStatus.MONITORING, CaseStatus.RESOLVED) is True

    def test_monitoring_to_investigating(self):
        assert validate_transition(CaseStatus.MONITORING, CaseStatus.INVESTIGATING) is True

    def test_resolved_to_closed(self):
        assert validate_transition(CaseStatus.RESOLVED, CaseStatus.CLOSED) is True

    def test_resolved_to_investigating(self):
        assert validate_transition(CaseStatus.RESOLVED, CaseStatus.INVESTIGATING) is True


class TestForbiddenTransitions:
    """Verify forbidden transitions from CASE_LIFECYCLE.md §3."""

    def test_open_to_closed_forbidden(self):
        assert validate_transition(CaseStatus.OPEN, CaseStatus.CLOSED) is False

    def test_investigating_to_open_forbidden(self):
        assert validate_transition(CaseStatus.INVESTIGATING, CaseStatus.OPEN) is False

    def test_closed_to_anything_forbidden(self):
        for target in CaseStatus:
            assert validate_transition(CaseStatus.CLOSED, target) is False

    def test_cancelled_to_anything_forbidden(self):
        for target in CaseStatus:
            assert validate_transition(CaseStatus.CANCELLED, target) is False

    def test_draft_to_investigating_forbidden(self):
        assert validate_transition(CaseStatus.DRAFT, CaseStatus.INVESTIGATING) is False

    def test_draft_to_closed_forbidden(self):
        assert validate_transition(CaseStatus.DRAFT, CaseStatus.CLOSED) is False

    def test_open_to_resolved_forbidden(self):
        assert validate_transition(CaseStatus.OPEN, CaseStatus.RESOLVED) is False

    def test_monitoring_to_closed_forbidden(self):
        assert validate_transition(CaseStatus.MONITORING, CaseStatus.CLOSED) is False


class TestGetAllowedTransitions:
    def test_draft_transitions(self):
        allowed = get_allowed_transitions(CaseStatus.DRAFT)
        assert set(allowed) == {CaseStatus.OPEN, CaseStatus.CANCELLED}

    def test_terminal_has_no_transitions(self):
        assert get_allowed_transitions(CaseStatus.CLOSED) == []
        assert get_allowed_transitions(CaseStatus.CANCELLED) == []

    def test_resolved_transitions(self):
        allowed = get_allowed_transitions(CaseStatus.RESOLVED)
        assert set(allowed) == {CaseStatus.CLOSED, CaseStatus.INVESTIGATING}


class TestTerminalStates:
    def test_closed_is_terminal(self):
        assert is_terminal(CaseStatus.CLOSED) is True

    def test_cancelled_is_terminal(self):
        assert is_terminal(CaseStatus.CANCELLED) is True

    def test_non_terminal_states(self):
        non_terminal = [
            CaseStatus.DRAFT, CaseStatus.OPEN, CaseStatus.INVESTIGATING,
            CaseStatus.MITIGATING, CaseStatus.MONITORING, CaseStatus.RESOLVED,
        ]
        for s in non_terminal:
            assert is_terminal(s) is False


class TestRoleGating:
    """Verify RBAC enforcement for Close and Cancel transitions."""

    def test_can_close_administrator(self):
        assert can_close("Administrator") is True
        assert can_close("ADMINISTRATOR") is True

    def test_can_close_security_engineer(self):
        assert can_close("Security Engineer") is True
        assert can_close("SECURITY_ENGINEER") is True

    def test_cannot_close_soc_analyst(self):
        assert can_close("SOC Analyst") is False
        assert can_close("SOC_ANALYST") is False

    def test_cannot_close_incident_responder(self):
        assert can_close("Incident Responder") is False
        assert can_close("INCIDENT_RESPONDER") is False

    def test_can_cancel_administrator(self):
        assert can_cancel("Administrator") is True
        assert can_cancel("ADMINISTRATOR") is True

    def test_can_cancel_security_engineer(self):
        assert can_cancel("Security Engineer") is True
        assert can_cancel("SECURITY_ENGINEER") is True

    def test_can_cancel_incident_responder(self):
        assert can_cancel("Incident Responder") is True
        assert can_cancel("INCIDENT_RESPONDER") is True

    def test_cannot_cancel_soc_analyst(self):
        assert can_cancel("SOC Analyst") is False
        assert can_cancel("SOC_ANALYST") is False


class TestAllStatesHaveTransitions:
    """Ensure every CaseStatus is present in the transition matrix."""

    def test_all_states_covered(self):
        for status in CaseStatus:
            assert status in TRANSITIONS, f"{status} missing from transition matrix"

    def test_terminal_states_set(self):
        assert TERMINAL_STATES == {CaseStatus.CLOSED, CaseStatus.CANCELLED}
