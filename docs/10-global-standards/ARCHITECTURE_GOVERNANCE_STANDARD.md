# Architecture Governance Standard

This document defines how architectural decisions are made, documented, and enforced within the ASTRA platform.

## 1. Architecture Decision Criteria
A formal Architecture Decision Record (ADR) is REQUIRED when a proposed change:
1. Alters the system's external interfaces or public APIs significantly.
2. Introduces a new programming language, database, or core infrastructure component.
3. Crosses established domain boundaries (e.g., Policy Engine directly accessing the Evidence database).
4. Modifies the global security model or RBAC definitions.
5. Impacts the non-functional requirements (NFRs) established in the `SRS.md` (e.g., introducing a component that degrades latency above 500ms).

## 2. ADR Lifecycle
1. **Draft:** An engineer creates a new markdown file in `docs/03-architecture/ADR/` following the ADR template (Context, Decision, Consequences).
2. **Review:** The PR containing the ADR is reviewed by the Architecture Team.
3. **Approved/Rejected:** The Lead Architect approves or rejects the PR.
4. **Implementation:** Once approved, engineering execution may begin.
5. **Deprecated:** If a later ADR supersedes an existing one, the old ADR is marked `[DEPRECATED]` but is NEVER deleted.

## 3. Architecture Review Process
The Architecture Team holds a formal review at the conclusion of every Sprint:
- **Scope:** Review all merged ADRs, assess technical debt logs, and evaluate any deviations from the `SDD.md`.
- **Output:** Identifies necessary refactoring tasks to be scheduled in the upcoming Sprint.

## 4. Dependency Rules (The "Modular Monolith" Constraint)
ASTRA enforces strict Domain-Driven Design boundaries:
- **Rule 1 (Downstream Isolation):** Domains may only communicate via established Service Layer interfaces or explicit internal events.
- **Rule 2 (Database Isolation):** Repositories must never perform cross-domain JOINs. If the Policy Engine needs Observation data, it must query the `ObservationService`, not the `observations` table directly.
- **Rule 3 (External Abstraction):** External SaaS providers (e.g., OpenAI, Jira) must be wrapped in an Abstraction Layer. Direct SDK usage deep in the business logic is prohibited.

## 5. Domain Ownership
Clear ownership prevents architectural drift.
- **Core Platform (Ingestion/Correlation):** Platform Engineering Team.
- **Security Logic (Policy/Evidence):** Security Engineering Team.
- **Execution (Automation):** Backend Automation Team.
- *Any cross-domain changes require approval from both owning teams.*

## 6. Deprecation Policy
When a feature, API endpoint, or internal service is slated for removal:
1. **Notice:** Mark the component as `@deprecated` in the code and document it in the upcoming Release Notes.
2. **Grace Period:** The component must remain fully functional for at least one full Minor version cycle (e.g., deprecated in v1.2, removed in v1.3).
3. **Removal:** Safely delete the code and update all related documentation and Open API specs.
