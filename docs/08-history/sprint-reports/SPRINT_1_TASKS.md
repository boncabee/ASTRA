# ASTRA Sprint 1 Tasks

**Version:** 3.1
**Date:** 2026-06-12
**Status:** Approved

---

## Epic 1.1 CES Core Models

### TASK-1001: Implement Core CES Pydantic Models
**Description:** Create the base Pydantic models for the Common Event Schema as defined in `COMMON_EVENT_SCHEMA.md` and `CES_IMPLEMENTATION_GUIDE.md`. This includes the core event fields (`event_id`, `timestamp`, `source_type`, `event_type`, `severity`, `raw_event`, `metadata`) and the nested objects (`actor`, `target`, `artifacts`).
**Dependencies:** None
**Deliverables:** `backend/app/schemas/ces.py` containing the Pydantic models.
**Acceptance Criteria:** Pydantic models successfully instantiate with valid data, enforce exact field definitions, and correctly type optional vs. required fields.
**Estimated Effort:** 2 hours

---

## Epic 1.2 Validation Engine

### TASK-1002: Implement CES Validation Rules
**Description:** Implement strict runtime validation using Pydantic validators. This must ensure `timestamp` successfully parses as a valid ISO-8601 format string, `event_type` follows the exact `category.action.outcome` taxonomy, and `severity` defaults to `info`.
**Dependencies:** TASK-1001
**Deliverables:** Validation methods and constraints within `backend/app/schemas/ces.py`.
**Acceptance Criteria:** Validation engine properly accepts valid payloads and explicitly rejects instances with missing mandatory fields, invalid timestamps, or incorrect taxonomies.
**Estimated Effort:** 2 hours

---

## Epic 1.3 Transformation Engine

### TASK-1003: Implement CES Transformation Interface
**Description:** Define the base interfaces and abstract classes for the transformation layer. This dictates how parsers will later implement the transformation of raw vendor logs into the validated CES models.
**Dependencies:** TASK-1002
**Deliverables:** `backend/app/services/transformation.py` with abstract base classes and transformation utilities.
**Acceptance Criteria:** A clear Python interface exists that enforces a standard contract (e.g., `transform(raw_log: dict) -> CESEvent`) ensuring no logs are dropped during conversion.
**Estimated Effort:** 2 hours

---

## Epic 1.4 Versioning Framework

### TASK-1004: Implement CES Schema Versioning
**Description:** Integrate schema versioning logic into the CES models. Establish the `schema_version` field set to `"1.0"` by default and prepare the structure for identifying and warning on deprecated fields for backward compatibility handling.
**Dependencies:** TASK-1001
**Deliverables:** Version control implementation in the CES Pydantic models.
**Acceptance Criteria:** All instantiated events include the `schema_version` set to `"1.0"`. The system has a standardized way to identify version mismatches or deprecated fields.
**Estimated Effort:** 1 hour

---

## Epic 1.5 CES Test Suite

### TASK-1005: Create CES Unit Tests
**Description:** Develop comprehensive unit tests verifying the validation engine and versioning constraints. Tests must explicitly assert that valid payloads are accepted and invalid payloads (missing mandatory fields, invalid dates, incorrect event taxonomies) are rejected. Include schema evolution tests if applicable.
**Dependencies:** TASK-1002, TASK-1004
**Deliverables:** `backend/tests/test_ces_validation.py` and `backend/tests/test_ces_versioning.py`.
**Acceptance Criteria:** All validation constraints are actively proven to work via unit tests without silent failures. Unit tests pass with >70% coverage for the `ces.py` module.
**Estimated Effort:** 3 hours

---

## Epic 1.6 Golden Dataset Foundation

### TASK-1006: Define Initial Golden Dataset for CES
**Description:** Create sample JSON files containing valid CES event examples (VPN Login, Windows Logon, Firewall Event, PowerShell Event) as defined in the examples of `CES_IMPLEMENTATION_GUIDE.md`. This forms the foundation for parser testing in Sprint 2.
**Dependencies:** TASK-1001
**Deliverables:** Golden dataset JSON files located in a new `datasets/golden/ces/` directory.
**Acceptance Criteria:** Golden dataset JSON files exist and perfectly match the schema validation rules defined in the implemented CES models.
**Estimated Effort:** 1 hour

---

## Sprint Exit Criteria
Sprint 1 is complete only if:
* All defined CES models (Epic 1.1) are fully implemented.
* The Validation Engine (Epic 1.2) successfully validates and rejects appropriate payloads.
* The Transformation Engine interface (Epic 1.3) is defined.
* Schema Versioning (Epic 1.4) is actively enforced.
* The CES Test Suite (Epic 1.5) passes 100% locally and via CI.
* The Golden Dataset Foundation (Epic 1.6) is populated with standard examples.

## Sprint Success Metrics
* 100% of Epic 1.1-1.6 tasks completed.
* 100% test coverage strictly for the CES schema and validation components.
* 100% schema validation success against the Golden Dataset instances.
* Zero integration of unapproved business logic (no Parsers, Correlation Engine, AKM, Playbooks, or Gemini logic implemented).

## Definition of Done
Every task is formally complete only if:
* Implementation is complete.
* Required tests pass (minimum 70% coverage).
* Required documentation is updated.
* Code passes all defined CI Quality Gates (Linting, Test, Security Scans).
