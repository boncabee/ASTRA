# Case Foundation Implementation

**Phase:** 7 — Sprint 1  
**Project:** ASTRA  
**Date:** 2026-06-16  
**Status:** Complete

## 1. Overview

This document describes the implementation of the Case Management domain foundation in ASTRA Phase 7 Sprint 1. The implementation establishes the aggregate root, immutable timeline, assignment tracking, state machine, RBAC enforcement, and audit integration required to support future Case operations, automation, reporting, and AI without domain redesign.

## 2. Architecture

### 2.1 Layer Diagram

```
┌─────────────────────────────────────────────┐
│              CaseService                    │
│  - create_case()  - assign_case()           │
│  - change_status() - update_case()          │
│  - get_case()     - list_cases()            │
├─────────────┬───────────┬───────────────────┤
│ CaseRepo    │ Timeline  │ Assignment │ Audit │
│             │ Service   │ Repo       │ Repo  │
├─────────────┴───────────┴───────────────────┤
│              State Machine                  │
│  validate_transition() / can_close/cancel() │
├─────────────────────────────────────────────┤
│           SQLAlchemy 2.0 Models             │
│  Case │ CaseTimeline │ CaseAssignment       │
└─────────────────────────────────────────────┘
```

### 2.2 Component Responsibilities

| Component | Responsibility |
|-----------|---------------|
| `Case` model | Aggregate root with status, priority, severity |
| `CaseTimeline` model | Immutable, append-only activity ledger |
| `CaseAssignment` model | Historical assignment tracking |
| `CaseStateMachine` | Transition validation + role gating |
| `CaseRepository` | CRUD + filter/pagination for Cases |
| `CaseTimelineRepository` | Append-only persistence (no update/delete) |
| `CaseAssignmentRepository` | Assignment history persistence |
| `TimelineService` | Event recording with validation |
| `CaseService` | Business logic orchestration |

## 3. State Machine

Encodes the transition matrix from `CASE_LIFECYCLE.md`:

| Current | → Allowed Next |
|---------|---------------|
| DRAFT | OPEN, CANCELLED |
| OPEN | INVESTIGATING, CANCELLED |
| INVESTIGATING | MITIGATING, RESOLVED |
| MITIGATING | MONITORING, INVESTIGATING, RESOLVED |
| MONITORING | RESOLVED, INVESTIGATING |
| RESOLVED | CLOSED, INVESTIGATING |
| CLOSED | *(terminal)* |
| CANCELLED | *(terminal)* |

### Role-Gated Transitions
- **Close** → Security Engineer, Administrator only
- **Cancel** → Incident Responder, Security Engineer, Administrator only

## 4. RBAC Mapping

The Case RBAC model maps to existing `UserRole` values:

| RBAC Spec Role | UserRole | Permissions |
|---------------|----------|-------------|
| Analyst | SOC_ANALYST | Create, assign self, change status (not close/cancel) |
| Responder | INCIDENT_RESPONDER | + Cancel, assign others |
| Manager | SECURITY_ENGINEER | + Close cases |
| Administrator | ADMINISTRATOR | Full access |

## 5. Audit Integration

Every mutation generates an `AuditEvent` via the existing `AuditRepository`:
- **CREATED** — case creation with initial values
- **ASSIGNED** — old/new assignee captured
- **STATUS_CHANGED** — old/new status + optional reason
- **UPDATED** — field-level old/new value diffs

## 6. Timeline Immutability

Enforced at two layers:
1. **Repository** — `CaseTimelineRepository` has no `update()` or `delete()` methods
2. **Service** — `TimelineService` has no `update()` or `delete()` methods

Every state transition, assignment, and creation is permanently recorded.

## 7. Files Created

| File | Description |
|------|-------------|
| `models/case.py` | Enums + Case, CaseTimeline, CaseAssignment models |
| `schemas/case.py` | Pydantic schemas (Create, Update, Response) |
| `repositories/case.py` | CaseRepository |
| `repositories/case_timeline.py` | CaseTimelineRepository (append-only) |
| `repositories/case_assignment.py` | CaseAssignmentRepository |
| `services/case_state_machine.py` | Transition matrix + role gating |
| `services/case.py` | CaseService |
| `services/case_timeline.py` | TimelineService |

## 8. Files Modified

| File | Change |
|------|--------|
| `models/__init__.py` | Added Case model imports |
| `pytest.ini` | Extended coverage paths |

## 9. Design Decisions

1. **String for actor fields** — Consistent with all existing models (not UUID FK)
2. **Enums co-located with models** — Following `evidence.py` pattern
3. **No API endpoints** — Sprint 1 is domain-only; endpoints are Sprint 2
4. **No soft-delete** — Deferred; no existing project pattern exists
5. **Role mapping** — Maps `UserRole` to Case permissions without new enum values
