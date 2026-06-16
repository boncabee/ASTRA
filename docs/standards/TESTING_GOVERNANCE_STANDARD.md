# Testing Governance Standard

This document establishes the mandatory testing tiers and coverage rules to ensure the reliability and security of the ASTRA platform.

## 1. Unit Testing
- **Scope:** Testing individual functions, methods, and isolated classes.
- **Framework:** Pytest.
- **Rules:** 
  - External dependencies (DB, Redis, external APIs) MUST be mocked (e.g., via `unittest.mock` or `pytest-mock`).
  - Unit tests must execute in less than 50ms per test.

## 2. Integration Testing
- **Scope:** Testing the interaction between internal modules and datastores.
- **Framework:** Pytest + Testcontainers (or Docker Compose).
- **Rules:**
  - Real database instances (PostgreSQL) and message brokers (Redis) must be spun up ephemerally for the test suite.
  - Data must be rolled back or flushed between tests to prevent state leakage.

## 3. Performance Testing
- **Scope:** Validating the NFRs (e.g., 1000 EPS ingestion, <500ms latency).
- **Framework:** Locust or k6.
- **Rules:**
  - Executed on a dedicated staging environment mirroring production.
  - Required prior to cutting any formal Release Candidate.

## 4. Security Testing
- **Scope:** Validating RBAC boundaries and preventing regressions of known vulnerabilities.
- **Rules:**
  - Every API endpoint test must assert both successful access (200 OK) with the correct role, and rejected access (403 Forbidden) with an incorrect role.
  - Input fuzzing against parsing engines to validate Pydantic constraints.

## 5. Acceptance Testing
- **Scope:** Validating that a Feature meets the user requirements defined in the `PRD.md` and `SRS.md`.
- **Rules:**
  - Executed primarily via API integration testing (testing the entire lifecycle: Ingestion -> Correlation -> Policy -> Evidence).
  - Acts as the final quality gate before a PR is marked as "Done".

## 6. Coverage Requirements
- **Rule:** ASTRA enforces a strict **100% test coverage** rule for all new Python code (`backend/src`).
- **Enforcement:** The CI pipeline (GitHub Actions) runs `pytest --cov`. If coverage drops below 100%, the pipeline fails, and the PR is blocked from merging.
- **Exemptions:** Code that interacts with hardware or un-mockable 3rd party black-boxes may use `# pragma: no cover`, but this requires explicit Lead Architect approval.

## 7. Definition of Done (Testing)
A task's testing phase is complete when:
1. All unit and integration tests pass locally and in CI.
2. Code coverage remains at 100%.
3. The specific Acceptance Criteria for the User Story have been explicitly tested.
