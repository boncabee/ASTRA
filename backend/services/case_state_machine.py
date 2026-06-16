"""
Case State Machine

Encodes the transition matrix from CASE_LIFECYCLE.md.
All transitions are validated at the domain level before any persistence.
"""
from typing import List, Set
from models.case import CaseStatus


# Transition matrix: current_state -> list of allowed next states
TRANSITIONS: dict[CaseStatus, List[CaseStatus]] = {
    CaseStatus.DRAFT:         [CaseStatus.OPEN, CaseStatus.CANCELLED],
    CaseStatus.OPEN:          [CaseStatus.INVESTIGATING, CaseStatus.CANCELLED],
    CaseStatus.INVESTIGATING: [CaseStatus.MITIGATING, CaseStatus.RESOLVED],
    CaseStatus.MITIGATING:    [CaseStatus.MONITORING, CaseStatus.INVESTIGATING, CaseStatus.RESOLVED],
    CaseStatus.MONITORING:    [CaseStatus.RESOLVED, CaseStatus.INVESTIGATING],
    CaseStatus.RESOLVED:      [CaseStatus.CLOSED, CaseStatus.INVESTIGATING],
    CaseStatus.CLOSED:        [],  # Terminal state
    CaseStatus.CANCELLED:     [],  # Terminal state
}

TERMINAL_STATES: Set[CaseStatus] = {CaseStatus.CLOSED, CaseStatus.CANCELLED}

# Roles allowed to close a case (Manager + Admin in RBAC spec)
CLOSE_ROLES: Set[str] = {"SECURITY_ENGINEER", "ADMINISTRATOR", "Security Engineer", "Administrator"}

# Roles allowed to cancel a case (Responder + Manager + Admin in RBAC spec)
CANCEL_ROLES: Set[str] = {
    "INCIDENT_RESPONDER", "SECURITY_ENGINEER", "ADMINISTRATOR",
    "Incident Responder", "Security Engineer", "Administrator",
}


def validate_transition(current: CaseStatus, target: CaseStatus) -> bool:
    """Return True if transitioning from current to target is allowed."""
    allowed = TRANSITIONS.get(current, [])
    return target in allowed


def get_allowed_transitions(current: CaseStatus) -> List[CaseStatus]:
    """Return the list of states reachable from current."""
    return list(TRANSITIONS.get(current, []))


def is_terminal(status: CaseStatus) -> bool:
    """Return True if the given status is a terminal (irreversible) state."""
    return status in TERMINAL_STATES


def can_close(role: str) -> bool:
    """Return True if the given role is allowed to close a case."""
    return role in CLOSE_ROLES


def can_cancel(role: str) -> bool:
    """Return True if the given role is allowed to cancel a case."""
    return role in CANCEL_ROLES
