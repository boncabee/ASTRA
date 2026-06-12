# ASTRA Traceability Matrix

Document ID: ASTRA-TRACE-001
Version: 2.0
Status: Approved

Related Documents:

* PROJECT_PLAN.md
* PRD.md
* ARCHITECTURE.md
* TASKS.md
* TESTING_STRATEGY.md

---

# Purpose

Provide complete traceability between:

```text
Requirement
↓
Architecture
↓
Implementation
↓
Database
↓
API
↓
Testing
↓
Audit
```

Every requirement must be traceable.

---

# Functional Traceability

| Requirement | Architecture       | API            | Database        | Tasks             | Tests            |
| ----------- | ------------------ | -------------- | --------------- | ----------------- | ---------------- |
| FR-001      | Upload Layer       | POST /analysis | uploaded_files  | TASK-001          | TEST-UPLOAD      |
| FR-002      | Parser Layer       | POST /analysis | incident_events | TASK-101,TASK-201 | TEST-PARSER      |
| FR-003      | Correlation Engine | Internal       | incidents       | TASK-301,TASK-302 | TEST-CORRELATION |
| FR-004      | AI Reasoner        | GET /result    | timelines       | TASK-501          | TEST-TIMELINE    |
| FR-005      | AI Reasoner        | GET /result    | incidents       | TASK-502          | TEST-NARRATIVE   |
| FR-006      | AI Reasoner        | GET /result    | mitre_mappings  | TASK-503          | TEST-MITRE       |
| FR-007      | AI Reasoner        | GET /result    | iocs            | TASK-504          | TEST-IOC         |
| FR-008      | AI Reasoner        | GET /result    | incidents       | TASK-505          | TEST-CONFIDENCE  |
| FR-009      | Persistence Layer  | Internal       | All Tables      | TASK-801          | TEST-STORAGE     |
| FR-010      | UI Layer           | GET /result    | Read Only       | TASK-701,TASK-703 | TEST-UI          |
| FR-011      | CES Layer          | Internal       | None            | Epic 10           | CES Tests        |
| FR-012      | AKM Layer          | Internal       | None            | Epic 11           | Knowledge Tests  |
| FR-013      | Investigation Layer| Internal       | None            | Epic 12           | Playbook Tests   |
| FR-014      | Self Improvement   | Internal       | None            | Epic 13           | Audit            |
| FR-015      | Validation Layer   | Internal       | None            | Epic 14           | Gate Tests       |

---

# Security Traceability

| Security Requirement | Source                | Validation    |
| -------------------- | --------------------- | ------------- |
| No Hardcoded Secrets | SECURITY.md           | Secret Scan   |
| Upload Validation    | SECURITY.md           | Upload Tests  |
| Prompt Validation    | PROMPT_ENGINEERING.md | AI Tests      |
| PII Protection       | SECURITY.md           | Privacy Tests |

---

# AI Traceability

| AI Capability | Prompt           | Output        |
| ------------- | ---------------- | ------------- |
| Timeline      | Timeline Prompt  | timeline      |
| Narrative     | Narrative Prompt | narrative     |
| MITRE         | MITRE Prompt     | mitre_mapping |
| IOC           | IOC Prompt       | ioc_list      |
| Confidence    | Confidence Rules | confidence    |

---

# Database Traceability

| Table           | Source Requirement |
| --------------- | ------------------ |
| analysis_jobs   | FR-001             |
| uploaded_files  | FR-001             |
| incidents       | FR-003             |
| timelines       | FR-004             |
| mitre_mappings  | FR-006             |
| iocs            | FR-007             |
| incident_events | FR-002             |

---

# Test Coverage Traceability

Required Mapping:

```text
Every FR
↓
At Least One Test
```

Forbidden:

```text
Requirement
↓
No Test
```

---

# Audit Requirements

AUDIT.md must verify:

* All FRs implemented
* All FRs tested
* All FRs traceable

Audit fails if:

* Missing traceability
* Missing tests
* Missing implementation

---

# Change Management

Whenever:

* PRD changes
* Architecture changes
* API changes
* Database changes

This document must be updated before merge.

```
```
