# Case State Machine Architecture

## Overview
The Case State Machine governs the lifecycle of a Case within the ASTRA platform. It is designed as a deterministic, role-gated state transition matrix that ensures cases follow a rigorous, auditable path from creation to resolution.

## States

| State | Description | Terminal |
|-------|-------------|----------|
| **DRAFT** | Initial state upon creation. The case is being populated with initial evidence and context. | No |
| **OPEN** | The case is formally open and awaiting assignment or initial triage. | No |
| **INVESTIGATING** | An analyst or responder is actively analyzing the case and associated evidence. | No |
| **MITIGATING** | Active countermeasures or remediation steps are being deployed. | No |
| **MONITORING** | Remediation is complete, and the system/user is monitoring for recurrence. | No |
| **RESOLVED** | The threat has been neutralized, and the case is awaiting final review and closure. | No |
| **CLOSED** | The case is permanently closed after final review. | **Yes** |
| **CANCELLED** | The case was deemed a false positive or duplicate and is permanently closed. | **Yes** |

## Transition Matrix

The following transitions are explicitly allowed by the `CaseStateMachine`:

| Current State | Allowed Next States |
|---------------|---------------------|
| DRAFT | OPEN, CANCELLED |
| OPEN | INVESTIGATING, CANCELLED |
| INVESTIGATING | MITIGATING, RESOLVED, CANCELLED |
| MITIGATING | MONITORING, RESOLVED |
| MONITORING | RESOLVED, INVESTIGATING |
| RESOLVED | CLOSED, INVESTIGATING |
| CLOSED | *None (Terminal)* |
| CANCELLED | *None (Terminal)* |

## Role-Based Access Control (RBAC) Gates

State transitions are not only governed by the matrix but also by the role of the user attempting the transition.

- **DRAFT → OPEN**: All Roles (SOC Analyst, Incident Responder, Security Engineer, Administrator)
- **OPEN → INVESTIGATING**: All Roles
- **INVESTIGATING → MITIGATING**: All Roles
- **MITIGATING → MONITORING**: All Roles
- **MONITORING → RESOLVED**: All Roles
- **RESOLVED → CLOSED**: **Gated** (Security Engineer, Administrator only)
- **Any → CANCELLED**: **Gated** (Incident Responder, Security Engineer, Administrator only)

*Note: SOC Analysts are explicitly prevented from transitioning a case to a terminal state (CLOSED or CANCELLED) to enforce a maker-checker (four-eyes) review principle.*

## Implementation Location
The state machine logic is strictly encapsulated within `backend/services/case_state_machine.py` and is invoked by the `CaseService` prior to any database mutation.
