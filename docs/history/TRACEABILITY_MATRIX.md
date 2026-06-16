# Traceability Matrix

This document maps high-level product requirements through software specification, design, implementation, and historical reporting.

| Feature / Capability | PRD Reference | SRS Reference | SDD Reference | Implementation (Code/Repo) | Phase Report (History) |
| --- | --- | --- | --- | --- | --- |
| **CES Event Ingestion** | Scope: Universal Ingestion | REQ-F01, REQ-F02 | Sec 2: API Layer, Sec 4: `CESEvent` | `backend/src/api/`, `backend/src/models/` | `PHASE_2_COMPLETION_REPORT.md` |
| **Observation Engine** | Scope: Risk Scoring & Threat Correlation | REQ-F04, REQ-F05 | Sec 4: `Correlation` -> `Observation` | `backend/src/services/observation_service.py` | `PHASE_3_COMPLETION_REPORT.md` |
| **Policy Engine** | Scope: Deterministic Policy Enforcement | REQ-F06 | Sec 2: Service Layer | `backend/src/services/policy_service.py` | `PHASE_4_COMPLETION_REPORT.md` |
| **Evidence Foundation** | Scope: Immutable Audit Trailing | REQ-F07, Validation Rule 1 | Sec 7: Evidence Architecture | `backend/src/repositories/evidence_repository.py`| `PHASE_4_5_COMPLETION_REPORT.md` |
| **Reporting & Compliance** | Scope: Compliance Reporting | COMP-01, COMP-02 | Sec 2: Service Layer | `backend/src/services/reporting_service.py` | `PHASE_5_COMPLETION_REPORT.md` |
| **Automation Engine** | Scope: Asynchronous Task Execution | REQ-F08, REQ-F09 | Sec 6: Queue & Worker Architecture | `backend/src/workers/automation_worker.py` | `PHASE_6_COMPLETION_REPORT.md` |
| **RBAC Framework** | Scope: Role-Based Access Control | Sec 4: Security & RBAC Rules | Sec 5: API Architecture | `backend/src/api/dependencies/auth.py` | `SPRINT_2_COMPLETION_REPORT.md` |
