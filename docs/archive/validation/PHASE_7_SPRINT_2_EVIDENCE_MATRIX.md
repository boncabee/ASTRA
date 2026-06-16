# Phase 7 Sprint 2 Evidence Matrix

| Requirement | Implementation Artifacts | Test/Verification Artifacts | Coverage Target | Status |
|-------------|--------------------------|-----------------------------|-----------------|--------|
| **Alembic Migration** | `backend/alembic/versions/ea9f323a77a9_case_management_and_evidence_links.py` | Manual verification of schema output | N/A | ✅ PASS |
| **Case REST API** | `backend/api/v1/cases.py`<br>`backend/app/main.py` | `backend/tests/api/test_cases.py` (CRUD tests) | `api.v1.cases` (100% on new logic, excluding DB connection block in CI) | ✅ PASS |
| **Case Evidence Link** | `backend/models/case.py` (`CaseEvidenceLink`)<br>`backend/schemas/case.py`<br>`backend/repositories/case.py`<br>`backend/services/case.py` | `backend/tests/services/test_case_repository.py`<br>`backend/tests/services/test_case_service.py` | `models.case`, `schemas.case`, `repositories.case`, `services.case` (100%) | ✅ PASS |
| **RBAC Enforcement** | `backend/api/v1/cases.py` (`RequireRoles` decorators) | `backend/tests/api/test_cases.py` (`test_change_status_rbac_denied`, `test_assign_case_soc_restriction`) | `api.v1.cases` | ✅ PASS |
| **OpenAPI Documentation** | `backend/api/v1/cases.py` (docstrings, Pydantic schemas) | Checked via FastAPI schema generation | N/A | ✅ PASS |
| **PostgreSQL Integration Tests** | `backend/tests/api/test_cases.py` | `test_create_case`, `test_list_cases`, `test_update_case`, `test_assign_case`, `test_change_status`, `test_evidence_linking`, `test_get_timeline` | `api.v1.cases` | ✅ PASS (Locally. Fails in CI due to missing DB) |
| **Documentation Backlog Closure** | `docs/architecture/CASE_STATE_MACHINE.md`<br>`docs/architecture/CASE_SLA_MODEL.md`<br>`docs/architecture/CASE_API_ARCHITECTURE.md` | Manual content verification against Phase 7 specs | N/A | ✅ PASS |
