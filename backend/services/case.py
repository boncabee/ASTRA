"""
CaseService — Core business logic for Case Management.

Orchestrates:
- Case creation with timeline + audit
- Assignment with history tracking + audit
- Status changes with state machine validation + RBAC + audit
- Read operations (get, list)
"""
from typing import List, Optional, Tuple
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from models.case import Case, CaseStatus, CasePriority, CaseSeverity, TimelineEventType, CaseEvidenceLink
from repositories.case import CaseRepository
from repositories.case_assignment import CaseAssignmentRepository
from repositories.evidence import AuditRepository, EvidenceRepository
from schemas.case import CaseCreate, CaseUpdate
from schemas.evidence import AuditEventCreate
from services.case_timeline import TimelineService
from services import case_state_machine
from core.logging import logger


class CaseService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.case_repo = CaseRepository(session)
        self.assignment_repo = CaseAssignmentRepository(session)
        self.timeline_service = TimelineService(session)
        self.audit_repo = AuditRepository(session)
        self.evidence_repo = EvidenceRepository(session)

    async def create_case(self, data: CaseCreate, created_by: str) -> Case:
        """
        Create a new case in DRAFT status.
        Records a CASE_CREATED timeline event and an audit event.
        """
        case = await self.case_repo.create(data, created_by=created_by)

        # Timeline: record creation event
        await self.timeline_service.record_event(
            case_id=case.id,  # type: ignore[arg-type]
            event_type=TimelineEventType.CASE_CREATED,
            actor=created_by,
            event_metadata={
                "title": data.title,
                "priority": data.priority.value,
                "severity": data.severity.value,
                "status": CaseStatus.DRAFT.value,
            },
        )

        # Audit: record creation
        await self.audit_repo.create_event(AuditEventCreate(
            entity_type="CASE",
            entity_id=case.id,  # type: ignore[arg-type]
            action="CREATED",
            actor=created_by,
            old_value=None,
            new_value={
                "title": data.title,
                "status": CaseStatus.DRAFT.value,
                "priority": data.priority.value,
                "severity": data.severity.value,
            },
        ))

        logger.info("Case created", extra={
            "event": "case_created",
            "case_id": str(case.id),
            "created_by": created_by,
        })

        return case

    async def assign_case(self, case_id: UUID, assigned_user_id: str, assigned_by: str) -> Case:
        """
        Assign a case to a user. Updates current assignee, records assignment
        history, creates a timeline event, and generates an audit record.
        """
        case = await self.case_repo.get_by_id(case_id)
        if not case:
            raise ValueError(f"Case {case_id} not found")

        previous_assignee = case.assigned_to

        # Update current assignee on case
        case = await self.case_repo.assign(case, assigned_user_id)

        # Record assignment history
        await self.assignment_repo.create(
            case_id=case_id,
            assigned_user_id=assigned_user_id,
            assigned_by=assigned_by,
        )

        # Timeline: record assignment event
        await self.timeline_service.record_event(
            case_id=case_id,
            event_type=TimelineEventType.ASSIGNMENT,
            actor=assigned_by,
            event_metadata={
                "previous_assignee": previous_assignee,
                "new_assignee": assigned_user_id,
            },
        )

        # Audit: record assignment
        await self.audit_repo.create_event(AuditEventCreate(
            entity_type="CASE",
            entity_id=case_id,
            action="ASSIGNED",
            actor=assigned_by,
            old_value={"assigned_to": previous_assignee},
            new_value={"assigned_to": assigned_user_id},
        ))

        logger.info("Case assigned", extra={
            "event": "case_assigned",
            "case_id": str(case_id),
            "assigned_to": assigned_user_id,
            "assigned_by": assigned_by,
        })

        return case

    async def change_status(
        self,
        case_id: UUID,
        new_status: CaseStatus,
        actor: str,
        actor_role: str,
        reason: Optional[str] = None,
    ) -> Case:
        """
        Change the status of a case. Validates against the state machine
        and enforces RBAC for Close/Cancel transitions.

        Raises ValueError for:
        - Case not found
        - Forbidden state transition
        - Insufficient role for Close/Cancel
        """
        case = await self.case_repo.get_by_id(case_id)
        if not case:
            raise ValueError(f"Case {case_id} not found")

        current_status = case.status
        if current_status is None:
            raise ValueError(f"Case {case_id} has no status")

        # Validate state machine transition
        if not case_state_machine.validate_transition(current_status, new_status):
            raise ValueError(
                f"Invalid transition from {current_status} to {new_status}. "
                f"Allowed: {case_state_machine.get_allowed_transitions(current_status)}"
            )

        # RBAC enforcement for restricted transitions
        if new_status == CaseStatus.CLOSED and not case_state_machine.can_close(actor_role):
            raise PermissionError(
                f"Role '{actor_role}' is not authorized to close cases. "
                f"Required: Manager or Administrator."
            )

        if new_status == CaseStatus.CANCELLED and not case_state_machine.can_cancel(actor_role):
            raise PermissionError(
                f"Role '{actor_role}' is not authorized to cancel cases. "
                f"Required: Responder, Manager, or Administrator."
            )

        # Update status
        case = await self.case_repo.change_status(case, new_status)

        # Timeline: record status change
        await self.timeline_service.record_event(
            case_id=case_id,
            event_type=TimelineEventType.STATUS_CHANGE,
            actor=actor,
            event_metadata={
                "previous_status": current_status.value if hasattr(current_status, 'value') else str(current_status),
                "new_status": new_status.value,
                "reason": reason,
            },
        )

        # Audit: record status change
        await self.audit_repo.create_event(AuditEventCreate(
            entity_type="CASE",
            entity_id=case_id,
            action="STATUS_CHANGED",
            actor=actor,
            old_value={"status": current_status.value if hasattr(current_status, 'value') else str(current_status)},
            new_value={"status": new_status.value},
            reason=reason,
        ))

        logger.info("Case status changed", extra={
            "event": "case_status_changed",
            "case_id": str(case_id),
            "from_status": str(current_status),
            "to_status": new_status.value,
            "actor": actor,
        })

        return case

    async def get_case(self, case_id: UUID) -> Optional[Case]:
        """Retrieve a single case by ID."""
        return await self.case_repo.get_by_id(case_id)

    async def list_cases(
        self,
        skip: int = 0,
        limit: int = 50,
        status: Optional[CaseStatus] = None,
        priority: Optional[CasePriority] = None,
        severity: Optional[CaseSeverity] = None,
        assigned_to: Optional[str] = None,
    ) -> Tuple[List[Case], int]:
        """List cases with optional filters and pagination."""
        return await self.case_repo.list(
            skip=skip,
            limit=limit,
            status=status,
            priority=priority,
            severity=severity,
            assigned_to=assigned_to,
        )

    async def update_case(self, case_id: UUID, data: CaseUpdate, actor: str) -> Case:
        """Update mutable case fields (title, description, priority, severity)."""
        case = await self.case_repo.get_by_id(case_id)
        if not case:
            raise ValueError(f"Case {case_id} not found")

        old_values: dict = {}
        new_values: dict = {}

        if data.title is not None:
            old_values["title"] = case.title
            case.title = data.title
            new_values["title"] = data.title

        if data.description is not None:
            old_values["description"] = case.description
            case.description = data.description
            new_values["description"] = data.description

        if data.priority is not None:
            priority = data.priority
            old_values["priority"] = getattr(case.priority, 'value', str(case.priority))
            case.priority = priority
            new_values["priority"] = getattr(priority, 'value', str(priority))

        if data.severity is not None:
            severity = data.severity
            old_values["severity"] = getattr(case.severity, 'value', str(case.severity))
            case.severity = severity
            new_values["severity"] = getattr(severity, 'value', str(severity))

        case = await self.case_repo.update(case)

        # Audit: record update
        if new_values:
            await self.audit_repo.create_event(AuditEventCreate(
                entity_type="CASE",
                entity_id=case_id,
                action="UPDATED",
                actor=actor,
                old_value=old_values,
                new_value=new_values,
            ))

        return case

    async def link_evidence(self, case_id: UUID, evidence_id: UUID, actor: str) -> CaseEvidenceLink:
        """Link evidence to a case."""
        case = await self.case_repo.get_by_id(case_id)
        if not case:
            raise ValueError(f"Case {case_id} not found")

        evidence = await self.evidence_repo.get_evidence_by_id(evidence_id)
        if not evidence:
            raise ValueError(f"Evidence {evidence_id} not found")

        link = await self.case_repo.link_evidence(case_id, evidence_id, actor)

        # Timeline: record evidence linking
        await self.timeline_service.record_event(
            case_id=case_id,
            event_type=TimelineEventType.SYSTEM_ACTION,
            actor=actor,
            event_metadata={
                "action": "evidence_linked",
                "evidence_id": str(evidence_id),
                "link_id": str(link.id),
            },
        )

        # Audit: record linking
        await self.audit_repo.create_event(AuditEventCreate(
            entity_type="CASE_EVIDENCE_LINK",
            entity_id=link.id,  # type: ignore[arg-type]
            action="CREATED",
            actor=actor,
            old_value=None,
            new_value={"case_id": str(case_id), "evidence_id": str(evidence_id)},
        ))

        logger.info("Evidence linked to case", extra={
            "event": "case_evidence_linked",
            "case_id": str(case_id),
            "evidence_id": str(evidence_id),
            "actor": actor,
        })

        return link

    async def get_evidence_links(self, case_id: UUID) -> List[CaseEvidenceLink]:
        """Retrieve all active evidence links for a case."""
        return await self.case_repo.get_evidence_links(case_id)

    async def soft_unlink_evidence(self, case_id: UUID, link_id: UUID, actor: str) -> Optional[CaseEvidenceLink]:
        """Soft unlink evidence from a case."""
        case = await self.case_repo.get_by_id(case_id)
        if not case:
            raise ValueError(f"Case {case_id} not found")

        link = await self.case_repo.soft_unlink_evidence(link_id)
        if not link:
            return None

        # Ensure the link belongs to the case
        if link.case_id != case_id:
            raise ValueError(f"Link {link_id} does not belong to Case {case_id}")

        # Timeline: record evidence unlinking
        await self.timeline_service.record_event(
            case_id=case_id,
            event_type=TimelineEventType.SYSTEM_ACTION,
            actor=actor,
            event_metadata={
                "action": "evidence_unlinked",
                "evidence_id": str(link.evidence_id),
                "link_id": str(link_id),
            },
        )

        # Audit: record unlinking
        await self.audit_repo.create_event(AuditEventCreate(
            entity_type="CASE_EVIDENCE_LINK",
            entity_id=link.id,  # type: ignore[arg-type]
            action="DELETED", # logical delete
            actor=actor,
            old_value={"is_active": True},
            new_value={"is_active": False},
        ))

        logger.info("Evidence unlinked from case", extra={
            "event": "case_evidence_unlinked",
            "case_id": str(case_id),
            "link_id": str(link_id),
            "actor": actor,
        })

        return link
