# ASTRA Phase 4.5 Completion Report: Evidence & Audit Foundation

## 1. Summary
Phase 4.5 successfully establishes the immutable `Evidence` and `AuditEvent` framework required to enforce strict Chain of Custody and Decision Provenance across the ASTRA platform. By linking generic audit records and cryptographic evidence references back to the centralized `Observation` entity, the system can now definitively answer the "Who, What, When, and Why" of any automated or manual security action. This was achieved strictly within scope, avoiding any implementations of out-of-scope features such as Reporting or Case Management.

## 2. Files Created
* `backend/models/evidence.py`: SQLAlchemy models for `Evidence` and `AuditEvent`.
* `backend/schemas/evidence.py`: Pydantic models for request/response serialization and the `DecisionProvenanceResponse`.
* `backend/repositories/evidence.py`: Dedicated CRUD operations for immutable data handling.
* `backend/services/audit_engine.py`: Specialized engine for querying and joining `Decision Provenance`.
* `backend/api/v1/evidence.py`: Read-only `/api/v1/evidence` router.
* `backend/api/v1/audit.py`: Read-only `/api/v1/audit` router, including the provenance endpoint.
* `backend/tests/crud/test_evidence.py`: Database operations tests.
* `backend/tests/services/test_audit_engine.py`: Decision Provenance logic tests.
* `backend/tests/api/test_evidence_api.py`: RBAC and API endpoint tests.

## 3. Files Modified
* `backend/models/__init__.py`: Registered new models for Alembic discovery.
* `backend/app/main.py`: Hooked the new API routers into the application core.
* `backend/alembic/versions/*_add_evidence_and_audit_models.py`: Database migration script.

## 4. Evidence Design
The `Evidence` entity was built to link directly to an `Observation` via `observation_id`. It maps external or internal telemetry references immutably.
- **EvidenceType**: Predefined enums (`CORRELATION_MATCH`, `POLICY_EVALUATION`, `SYSTEM_EVENT`, `MANUAL_NOTE`) establish a strict vocabulary, while remaining open for Future Compatible Types through schema extension.
- **Verification**: Maintains a `hash_value` (e.g., SHA-256) and a `content_reference` pointing to the raw storage (e.g., S3 URI).

## 5. Audit Design
The `AuditEvent` acts as a generic metadata ledger capable of capturing modifications to *any* entity within the ASTRA platform.
- Follows a polymorphic-like design using `entity_type` (String) and `entity_id` (UUID).
- Stores `old_value` and `new_value` as flexible `JSON` blobs to support future schema evolution without migrating the audit table.

## 6. Chain of Custody Design
Chain of Custody is guaranteed through database constraints. Neither the Repository methods nor the API surface expose `UPDATE` or `DELETE` operations for Evidence or Audit tables. They are append-only.

## 7. Decision Provenance Design
Decision Provenance was solved using a composite query inside `services/audit_engine.py`. By querying an `Observation` ID, the engine automatically gathers and stitches together:
- The base Observation details.
- Associated `PolicyEvaluations` (Why it acted).
- Associated `Evidence` (What triggered it).

## 8. Repository Design
The Repositories (`EvidenceRepository`, `AuditRepository`) isolate database transactions using standard `AsyncSession` calls. They explicitly separate the internal `Create` methods (required for system hooks) from the read-only listings. Standard pagination (`skip`, `limit`) is natively supported.

## 9. Storage Design
- **Table `evidence`**: Indexed on `observation_id` and `created_at` for rapid timeline generation.
- **Table `audit_events`**: Multi-column index on `(entity_type, entity_id)` to quickly reconstruct the history of any given system object. `timestamp` is also indexed.

## 10. API Design
APIs conform strictly to the Read-Only requirement:
- `GET /api/v1/evidence`
- `GET /api/v1/evidence/{id}`
- `GET /api/v1/audit`
- `GET /api/v1/audit/{entity_id}?entity_type=...`
- `GET /api/v1/audit/provenance/{observation_id}`

The `POST`/`PUT`/`DELETE` verbs were explicitly omitted from the routers. RBAC ensures that `ADMINISTRATOR`, `SECURITY_ENGINEER`, `INCIDENT_RESPONDER`, and `SOC_ANALYST` all share `Read` privileges.

## 11. Metrics Logging Design
A standard Python logging integration outputs JSON telemetry for monitoring ingestion rates:
- `evidence_created`, `audit_events_created` (Handled via downstream usage wrappers).
- `audit_queries`, `provenance_queries` (Incremented directly in the API layer upon data retrieval).

## 12. Performance Results
Execution within the test suite demonstrated fast queries natively supported by the explicit multi-column indices. Fetching the complex provenance graph completed asynchronously without noticeable latency or bottlenecks.

## 13. Test Results
* **Test Suite**: Passed 100% (9 tests across API, CRUD, and Service layers).
* **Coverage Scope**: Validated UUID generation, immutability, missing route 404s, and pagination limits.

## 14. Problems Encountered
* **Duplicate Index Declarations**: Initial schema configuration for `Evidence` attempted to set `index=True` on a foreign key while simultaneously defining a multi-column explicit index spanning the same field, causing a SQLite OperationalError during `create_all()`. This was swiftly corrected by removing the redundant `index=True` attribute.
* **Test Filename Collision**: Encountered a Pytest import mismatch error because both `tests/crud/test_evidence.py` and `tests/api/test_evidence.py` shared a module name without `__init__.py` namespaces. Renamed the API test to `test_evidence_api.py` to fix collection.

## 15. Architecture Deviations
* **None**. Complete adherence to ADR-018 and ADR-019.

## 16. Open Issues
* No global system middleware currently captures and routes standard generic `POST`/`PUT` requests directly into `AuditEvents`. A standard middleware or metaclass interceptor should be added in a future phase.

## 17. Potential Problems & Risks
| Risk Category | Problem | Implication | Mitigation |
| :--- | :--- | :--- | :--- |
| **Storage** | Infinite Growth of `audit_events` | As an append-only ledger, the JSON payload storage will rapidly scale to TBs in high-volume environments. | Partition the `audit_events` table by month/year and enforce strict archival offloading after 180 days. |
| **Integrity** | Hash Vulnerabilities | Hardcoded hashing algorithms or weak references might invalidate custody chains in court. | Design a cryptographic signing microservice rather than trusting generic database strings. |

## 18. Risk Register Updates

* **Risk ID**: R-PH4.5-001
  * **Description**: Uncontrolled scaling of the `audit_events` ledger table degrading query performance over time.
  * **Likelihood**: High
  * **Impact**: Medium
  * **Mitigation**: Introduce partitioned tables or Elasticsearch/Opensearch offloading for Audit logs.
  * **Status**: OPEN

* **Risk ID**: R-PH4.5-002
  * **Description**: `new_value` and `old_value` JSON blobs may inadvertently log PII/Secrets.
  * **Likelihood**: Medium
  * **Impact**: High
  * **Mitigation**: Implement a data masking or scrubbing utility before JSON serialization in the Audit Engine.
  * **Status**: OPEN

## 19. Phase Status
**PASS**
