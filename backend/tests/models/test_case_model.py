"""Tests for Case domain models — instantiation, enums, defaults."""
import pytest
import uuid
from models.case import (
    Case, CaseTimeline, CaseAssignment,
    CaseStatus, CasePriority, CaseSeverity, TimelineEventType,
)


# --- Enum Value Tests ---

class TestCaseStatusEnum:
    def test_all_values(self):
        expected = {"DRAFT", "OPEN", "INVESTIGATING", "MITIGATING", "MONITORING", "RESOLVED", "CLOSED", "CANCELLED"}
        actual = {s.value for s in CaseStatus}
        assert actual == expected

    def test_string_mixin(self):
        assert CaseStatus.DRAFT == "DRAFT"
        assert isinstance(CaseStatus.OPEN, str)


class TestCasePriorityEnum:
    def test_all_values(self):
        expected = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
        actual = {p.value for p in CasePriority}
        assert actual == expected


class TestCaseSeverityEnum:
    def test_all_values(self):
        expected = {"INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"}
        actual = {s.value for s in CaseSeverity}
        assert actual == expected


class TestTimelineEventTypeEnum:
    def test_all_values(self):
        expected = {"STATUS_CHANGE", "ASSIGNMENT", "CASE_CREATED", "SYSTEM_ACTION"}
        actual = {e.value for e in TimelineEventType}
        assert actual == expected


# --- Model Instantiation Tests ---

class TestCaseModel:
    def test_create_with_defaults(self):
        """When constructed with explicit defaults matching CaseRepository behavior."""
        case = Case(
            title="Test Case",
            created_by="user1",
            status=CaseStatus.DRAFT,
            priority=CasePriority.MEDIUM,
            severity=CaseSeverity.MEDIUM,
        )
        assert case.title == "Test Case"
        assert case.created_by == "user1"
        assert case.status == CaseStatus.DRAFT
        assert case.priority == CasePriority.MEDIUM
        assert case.severity == CaseSeverity.MEDIUM
        assert case.description is None
        assert case.assigned_to is None

    def test_column_defaults_configured(self):
        """Verify that column-level defaults are properly configured for DB INSERT."""
        status_col = Case.__table__.columns["status"]
        priority_col = Case.__table__.columns["priority"]
        severity_col = Case.__table__.columns["severity"]
        assert status_col.default is not None
        assert priority_col.default is not None
        assert severity_col.default is not None

    def test_create_with_all_fields(self):
        case_id = uuid.uuid4()
        case = Case(
            id=case_id,
            title="Critical Incident",
            description="A critical security incident",
            status=CaseStatus.INVESTIGATING,
            priority=CasePriority.CRITICAL,
            severity=CaseSeverity.HIGH,
            assigned_to="analyst-1",
            created_by="system",
        )
        assert case.id == case_id
        assert case.title == "Critical Incident"
        assert case.description == "A critical security incident"
        assert case.status == CaseStatus.INVESTIGATING
        assert case.priority == CasePriority.CRITICAL
        assert case.severity == CaseSeverity.HIGH
        assert case.assigned_to == "analyst-1"

    def test_tablename(self):
        assert Case.__tablename__ == "cases"


class TestCaseTimelineModel:
    def test_create(self):
        event = CaseTimeline(
            case_id=uuid.uuid4(),
            event_type=TimelineEventType.STATUS_CHANGE,
            actor="user1",
            event_metadata={"old": "DRAFT", "new": "OPEN"},
        )
        assert event.event_type == TimelineEventType.STATUS_CHANGE
        assert event.actor == "user1"
        assert event.event_metadata == {"old": "DRAFT", "new": "OPEN"}

    def test_nullable_metadata(self):
        event = CaseTimeline(
            case_id=uuid.uuid4(),
            event_type=TimelineEventType.SYSTEM_ACTION,
            actor="SYSTEM",
        )
        assert event.event_metadata is None

    def test_tablename(self):
        assert CaseTimeline.__tablename__ == "case_timeline"


class TestCaseAssignmentModel:
    def test_create(self):
        assignment = CaseAssignment(
            case_id=uuid.uuid4(),
            assigned_user_id="analyst-2",
            assigned_by="manager-1",
        )
        assert assignment.assigned_user_id == "analyst-2"
        assert assignment.assigned_by == "manager-1"

    def test_tablename(self):
        assert CaseAssignment.__tablename__ == "case_assignments"
