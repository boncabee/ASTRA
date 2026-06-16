# Work Breakdown Structure (WBS) Framework

This document defines the official hierarchical breakdown of work for the ASTRA platform. All planning, execution, and reporting must adhere to this structure to ensure traceability and governance.

## 1. Hierarchy Overview

1. **Vision:** The ultimate long-term product destination (e.g., "A fully autonomous deterministic security platform").
2. **Goals:** Measurable objectives that advance the vision (e.g., "Achieve 1,000 EPS ingestion with sub-500ms latency").
3. **Epics:** Major architectural or business workstreams that span multiple releases.
4. **Capabilities:** Broad sets of functionality within an Epic.
5. **Features:** Distinct, shippable increments of product value.
6. **User Stories:** Requirements defined from the perspective of an end-user or system actor.
7. **Tasks:** Engineering execution units assigned to developers.
8. **Subtasks:** Granular steps required to complete a Task.

## 2. Definitions

### 2.1 Strategic Level
- **Vision:** Defined in the `PRD.md`. It acts as the North Star for all architectural and product decisions.
- **Goals:** Documented in `ROADMAP.md` as Success Metrics for upcoming phases.

### 2.2 Planning Level
- **Epics:** Massive bodies of work (e.g., "Automation Engine", "Identity & Access"). Epics are persistent and rarely closed; instead, new Features are added to them over time.
- **Capabilities:** Logical groupings within an Epic. For example, within the "Automation Engine" Epic, "Webhook Integration" is a Capability.

### 2.3 Delivery Level
- **Features:** A deliverable that provides tangible value. E.g., "Jira Ticket Creation Automation". Features span multiple Sprints and consist of multiple User Stories.
- **User Stories:** Formatted as `As a [persona], I want to [action] so that [value]`. These are scoped to be completed within a single Sprint.

### 2.4 Execution Level
- **Tasks:** Technical implementations mapped to a User Story. E.g., `TASK-3011: Implement AutomationWorker class`.
- **Subtasks:** Breaking down the Task into manageable commits or checklist items.

## 3. Unit Types
Tasks are further classified by their nature to ensure comprehensive execution:

### 3.1 Implementation Units
Code changes that add or modify system behavior (e.g., writing the FastAPI router, updating SQLAlchemy models).

### 3.2 Testing Units
Code changes dedicated to validation (e.g., writing Pytest suites, integration tests, or manual test scripts). A Feature is not complete until its Testing Units are executed.

### 3.3 Documentation Units
Updates to the `docs/` hierarchy, including Phase Reports, ADRs, or API specification updates. Code cannot be merged without its associated Documentation Units.
