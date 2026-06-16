# Task Breakdown Guidelines

This document outlines the strict guidelines for defining, scoping, and accepting work within the ASTRA project.

## 1. Structural Standards

### 1.1 Epic
- **Format:** `EPIC-[ID]: [Name]`
- **Requirement:** Must map directly to a strategic business goal. Rarely "closed"; instead, acts as a container.
- **Example:** `EPIC-07: Automation`

### 1.2 Feature
- **Format:** `FEAT-[ID]: [Actionable Title]`
- **Requirement:** A distinct piece of functionality that provides end-user value.
- **Example:** `FEAT-071: Asynchronous Task Queuing`

### 1.3 User Story
- **Format:** `As a [persona], I want to [action] so that [value].`
- **Requirement:** Must fit within a single Sprint.
- **Example:** `As a System Administrator, I want the Automation Engine to process tasks asynchronously so that the core Policy Engine is not blocked.`

### 1.4 Task
- **Format:** `TASK-[ID]: [Technical Implementation]`
- **Requirement:** A specific engineering task assigned to one developer. Should take no more than 3 days to complete.
- **Example:** `TASK-3011: Implement Celery AutomationWorker`

### 1.5 Subtask
- **Format:** Checkbox list within a Task.
- **Requirement:** Granular implementation steps (e.g., "Define SQLAlchemy model", "Write Pytest unit test").

## 2. Dependencies
Tasks must explicitly list blocking dependencies before they can be moved to "In Progress".
- **Hard Dependency:** Task B cannot start until Task A is merged.
- **Soft Dependency:** Task B can start, but cannot be deployed until Task A is deployed.

## 3. Acceptance Criteria (AC)
Every User Story and Task must have clear, boolean Acceptance Criteria.
- AC must be testable.
- AC must define edge cases and error handling expectations.
- **Example:** "If the AutomationWorker fails to connect to Redis, it must log a CRITICAL error and retry 3 times with exponential backoff."

## 4. Definition of Done (DoD)
A Task or Story is only "Done" when it meets the global ASTRA DoD:
1. Code is fully implemented and peer-reviewed.
2. All Acceptance Criteria are met.
3. Code compiles and passes all CI/CD linters (MyPy, Pyright).
4. Testing Requirements (see below) are met.
5. Documentation Requirements (see below) are met.

## 5. Testing Requirements
1. **100% Coverage Rule:** All new Python code must be covered by unit tests.
2. **Integration Tests:** Any feature interacting with the database or external services must have an integration test.
3. **Golden Datasets:** Parsers and logic engines must be validated against standardized `.json` datasets to prevent regression.

## 6. Documentation Requirements
1. **API Changes:** Any change to a REST endpoint must update `docs/03-architecture/API_SPEC.md` and the FastAPI OpenAPI schema.
2. **Architectural Changes:** Must be preceded by an approved ADR in `docs/03-architecture/ADR/`.
3. **Traceability:** The pull request must reference the `TASK-[ID]`, linking it up the hierarchy to the relevant Epic.
