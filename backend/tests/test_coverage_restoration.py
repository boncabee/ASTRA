"""
Phase 8.1.6 — Targeted coverage restoration tests.

Covers specific uncovered lines identified in the gap analysis:
- repositories/observation.py: create, get_by_correlation_id, list filters
- repositories/case_assignment.py: get_by_case_id
- repositories/report.py: get_compliance_mappings
- repositories/automation.py: avg execution time loop body
- services/case.py: status-is-None guard (line 151)
- app/core/versioning.py: migrate_to_latest pass branch, _migrate_1_0_to_2_0
- app/schemas/ces.py: non-string severity pass-through (line 133)
"""
import uuid
from datetime import datetime, timezone, timedelta
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from core.config import settings
from core.database import Base
from models.observation import ObservationStatus, PolicyAction
from models.correlation import CorrelationRule, CorrelationMatch
from models.case import Case, CaseStatus, CasePriority, CaseSeverity
from models.report import ReportType
from models.automation import AutomationRequest, AutomationExecution, AutomationState, AutomationAction
from models.policy import Policy
from schemas.observation import ObservationCreate
from schemas.report import ReportCreate, ComplianceMappingCreate
from repositories.observation import ObservationRepository
from repositories.case_assignment import CaseAssignmentRepository
from repositories.report import ReportRepository
from repositories.automation import AutomationRepository
from services.case import CaseService
from app.core.versioning import migrate_to_latest, _migrate_1_0_to_2_0
from app.schemas.ces import CESEvent, Severity


# ── DB session fixture ──────────────────────────────────────────────

@pytest_asyncio.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine(settings.TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with SessionLocal() as session:
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


# ── Helper: create prerequisite correlation match ────────────────────

async def _make_correlation_match(session) -> CorrelationMatch:
    rule = CorrelationRule(
        name=f"Rule-{uuid.uuid4()}",
        description="test",
        event_types=["test.event"],
        conditions={},
        time_window=60,
        severity_weight=50,
    )
    session.add(rule)
    await session.flush()

    match = CorrelationMatch(
        rule_id=rule.id,
        matched_events=["evt-1"],
        event_count=1,
        match_timestamp=datetime.now(timezone.utc),
        correlation_score=50,
        context={},
    )
    session.add(match)
    await session.flush()
    return match


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. repositories/observation.py — create, get_by_correlation_id, list
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestObservationRepository:
    @pytest.mark.asyncio
    async def test_create_observation(self, db_session):
        match = await _make_correlation_match(db_session)
        repo = ObservationRepository(db_session)
        data = ObservationCreate(
            title="Test Obs",
            description="Desc",
            correlation_id=match.id,
            classification="Auth",
            status=ObservationStatus.NEW,
            risk_score=42,
            evidence_count=1,
        )
        obs = await repo.create(data, created_by="test-user")
        assert obs.id is not None
        assert obs.title == "Test Obs"
        assert obs.created_by == "test-user"

    @pytest.mark.asyncio
    async def test_get_by_correlation_id(self, db_session):
        match = await _make_correlation_match(db_session)
        repo = ObservationRepository(db_session)
        data = ObservationCreate(
            title="Corr Obs",
            description="Desc",
            correlation_id=match.id,
            classification="Network",
            risk_score=60,
            evidence_count=1,
        )
        created = await repo.create(data, created_by="user")
        fetched = await repo.get_by_correlation_id(match.id)
        assert fetched is not None
        assert fetched.id == created.id

    @pytest.mark.asyncio
    async def test_list_filter_status(self, db_session):
        match = await _make_correlation_match(db_session)
        repo = ObservationRepository(db_session)
        data = ObservationCreate(
            title="Status Obs",
            description="d",
            correlation_id=match.id,
            classification="Auth",
            risk_score=50,
            evidence_count=1,
            status=ObservationStatus.NEW,
        )
        await repo.create(data, created_by="u")
        results, total = await repo.list(status=ObservationStatus.NEW)
        assert total >= 1

    @pytest.mark.asyncio
    async def test_list_filter_risk_categories(self, db_session):
        """Cover all risk category branches: INFORMATIONAL, LOW, MEDIUM, HIGH, CRITICAL."""
        repo = ObservationRepository(db_session)

        # Create observations at different risk scores, each with its own correlation
        for score in [5, 25, 50, 75, 95]:
            match = await _make_correlation_match(db_session)
            data = ObservationCreate(
                title=f"Risk-{score}",
                description="d",
                correlation_id=match.id,
                classification="Auth",
                risk_score=score,
                evidence_count=1,
            )
            await repo.create(data, created_by="u")

        # Exercise each risk_category branch
        for category in ["INFORMATIONAL", "LOW", "MEDIUM", "HIGH", "CRITICAL"]:
            results, total = await repo.list(risk_category=category)
            assert total >= 1, f"Expected at least 1 result for {category}"

    @pytest.mark.asyncio
    async def test_list_filter_classification(self, db_session):
        match = await _make_correlation_match(db_session)
        repo = ObservationRepository(db_session)
        data = ObservationCreate(
            title="Class Obs",
            description="d",
            correlation_id=match.id,
            classification="Malware",
            risk_score=70,
            evidence_count=1,
        )
        await repo.create(data, created_by="u")
        results, total = await repo.list(classification="Malware")
        assert total >= 1


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. repositories/case_assignment.py — get_by_case_id
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestCaseAssignmentRepository:
    @pytest.mark.asyncio
    async def test_get_by_case_id(self, db_session):
        # Create a case first
        case = Case(
            id=uuid.uuid4(),
            title="Assignment Test Case",
            status=CaseStatus.DRAFT,
            priority=CasePriority.MEDIUM,
            severity=CaseSeverity.MEDIUM,
            created_by="test-user",
        )
        db_session.add(case)
        await db_session.commit()
        await db_session.refresh(case)

        repo = CaseAssignmentRepository(db_session)
        await repo.create(
            case_id=case.id,
            assigned_user_id="analyst-1",
            assigned_by="manager-1",
        )
        history = await repo.get_by_case_id(case.id)
        assert len(history) >= 1
        assert history[0].assigned_user_id == "analyst-1"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. repositories/report.py — get_compliance_mappings
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestReportRepository:
    @pytest.mark.asyncio
    async def test_get_compliance_mappings(self, db_session):
        repo = ReportRepository(db_session)

        # Create a report with a compliance mapping
        report_data = ReportCreate(
            report_type=ReportType.AUDIT,
            scope={"period": "Q1-2026"},
            data_sources=["audit_events"],
            evidence_references=["evidence-1"],
            audit_references=["audit-1"],
            summary="Test compliance report",
            details={"findings": []},
            compliance_mappings=[
                ComplianceMappingCreate(
                    framework="SOC2",
                    control_id="CC6.1",
                    description="Logical access controls",
                )
            ],
        )
        report = await repo.create_report(report_data, created_by="auditor")

        mappings = await repo.get_compliance_mappings(report.id)
        assert len(mappings) >= 1
        assert mappings[0].framework == "SOC2"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. repositories/automation.py — avg execution time loop body
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestAutomationRepositoryMetrics:
    @pytest.mark.asyncio
    async def test_metrics_with_completed_execution(self, db_session):
        """Covers lines 89-91: the execution time aggregation loop body."""
        # Need a policy first (FK constraint)
        policy = Policy(
            name=f"Metric Policy {uuid.uuid4()}",
            description="for metrics test",
            action=PolicyAction.NOTIFY,
            priority=100,
            is_active=True,
            created_by="sys",
        )
        db_session.add(policy)
        await db_session.commit()
        await db_session.refresh(policy)

        # Create request + execution
        req = AutomationRequest(
            policy_id=policy.id,
            action=AutomationAction.NOTIFY_WEBHOOK,
            parameters={"url": "http://test.com"},
            created_by="test-user",
            state=AutomationState.SUCCESS,
        )
        db_session.add(req)
        await db_session.flush()

        now = datetime.now(timezone.utc)
        execution = AutomationExecution(
            request_id=req.id,
            state=AutomationState.SUCCESS,
            started_at=now - timedelta(seconds=2),
            completed_at=now,
        )
        db_session.add(execution)
        await db_session.commit()

        repo = AutomationRepository(db_session)
        metrics = await repo.get_metrics()

        assert metrics["automation_executions"] >= 1
        assert metrics["average_execution_time_ms"] > 0


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5. services/case.py — status-is-None guard (line 151)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestCaseServiceNullStatus:
    @pytest.mark.asyncio
    async def test_change_status_null_current_status(self):
        """Covers line 151: raises ValueError when case.status is None."""
        mock_session = AsyncMock()
        service = CaseService(mock_session)

        case_with_null_status = Case(
            id=uuid.uuid4(),
            title="Null Status Case",
            status=None,  # type: ignore[arg-type]
            created_by="user",
        )
        service.case_repo.get_by_id = AsyncMock(return_value=case_with_null_status)

        with pytest.raises(ValueError, match="has no status"):
            await service.change_status(
                case_with_null_status.id,
                CaseStatus.OPEN,
                actor="user",
                actor_role="SOC_ANALYST",
            )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 6. app/core/versioning.py — migrate_to_latest, _migrate_1_0_to_2_0
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestVersioningGaps:
    def test_migrate_to_latest_unsupported_non_1x(self):
        """Covers line 41: the pass branch for non-1.x unsupported versions."""
        event = {"event_id": "123", "schema_version": "3.0"}
        result, version = migrate_to_latest(event, "3.0")
        # Should pass through unchanged
        assert result == event
        assert version == "3.0"

    def test_migrate_1_0_to_2_0_stub(self):
        """Covers lines 48-49: the internal migration stub."""
        event = {"event_id": "123", "schema_version": "1.0"}
        migrated = _migrate_1_0_to_2_0(event)
        assert migrated["schema_version"] == "2.0"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 7. app/schemas/ces.py — non-string severity pass-through (line 133)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestCESSeverityPassthrough:
    def test_severity_enum_value_passthrough(self):
        """Covers line 133: when severity is already a Severity enum, not a string."""
        event = CESEvent(
            event_id="evt-001",
            timestamp="2024-01-01T00:00:00Z",
            source_type="vpn",
            event_type="authentication.login.success",
            severity=Severity.high,
            raw_event="raw log line",
        )
        assert event.severity == Severity.high
