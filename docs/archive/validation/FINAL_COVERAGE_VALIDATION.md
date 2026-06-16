# Final Coverage Validation

## Verification Method
Executed `pytest --cov=app --cov-report=term-missing tests/` from `backend/` using the project virtual environment.

## Command Executed
```
.\.venv\Scripts\pytest --cov=app --cov-report=term-missing tests/
```

## Coverage Tooling
- **pytest-cov** 5.0.0: Present in `requirements-dev.txt` and installed.
- **pytest.ini** `addopts`: `--cov=app --cov-report=term-missing` — coverage is automatically enabled on every test run.

## Coverage Gate
- **CI enforcement**: `.github/workflows/ci.yml` line 45: `pytest --cov=app --cov-fail-under=100 tests/`
- **Local enforcement**: `pytest.ini` does NOT include `--cov-fail-under`. Gate is CI-only.

## Actual Results

| Metric | Value |
|--------|-------|
| Total Tests Collected | 215 |
| Tests Passed | 132 |
| Tests Failed | 0 |
| Tests Errored | 83 |
| Total Statements | 787 |
| Statements Missed | 4 |
| Coverage Reported | 99% |
| Error Cause | `ConnectionRefusedError` — PostgreSQL not running locally |

### Detailed Error Analysis
All 83 errors are `ConnectionRefusedError: [WinError 10061]` — the test suite attempts to connect to `postgresql+asyncpg://postgres:postgres@localhost:5432/astra_test` but no PostgreSQL instance is running on this machine. These are **not test failures**; they are **infrastructure errors** caused by the VR-004 migration to PostgreSQL without a local database available.

### Passing Tests Breakdown
The 132 tests that passed are unit tests that do not require a database connection (parsers, transformers, CES validation, versioning, correlation service logic, policy engine `_matches`, automation worker cancel, RBAC middleware, API deps, main lifespan).

### Coverage Gap Detail
- `app/schemas/ces.py` line 134: 1 uncovered line (Pydantic validator fallback path)
- `app/main.py` lines 16-19: 3 uncovered lines (startup import block, only hit in full application context)

## Assessment

| Check | Result |
|-------|--------|
| Coverage tooling exists | PASS |
| Coverage gate exists in CI | PASS |
| Coverage gate enforced locally | FAIL — `pytest.ini` lacks `--cov-fail-under` |
| Coverage result is 100% | NOT VERIFIED — 83 tests errored due to missing PostgreSQL |
| All tests pass | NOT VERIFIED — 83 connection errors |

## Status
**NOT VERIFIED** — Cannot confirm 100% coverage or full test pass because the local environment lacks a running PostgreSQL instance. The CI pipeline enforces `--cov-fail-under=100` with a PostgreSQL service container, so **CI-level enforcement is correctly configured**. Local verification requires a running database.
