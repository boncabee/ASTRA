# VR-004 PostgreSQL Parity Completion Evidence

## Issue
The testing suite and GitHub Actions CI workflow utilized an in-memory SQLite database (`sqlite+aiosqlite:///:memory:`), resulting in significant environment parity drift and masking concurrent transaction issues that only appear in PostgreSQL.

## Resolution
- Modified `backend/core/config.py` to point `TEST_DATABASE_URL` to PostgreSQL (`postgresql+asyncpg://postgres:postgres@localhost:5432/astra_test`).
- Modified `backend/tests/crud/test_correlation_crud.py` to remove explicit SQLite index verification (`PRAGMA index_list`) and replace it with a PostgreSQL-compatible query (`SELECT indexname FROM pg_indexes`).
- Modified `.github/workflows/ci.yml` to spin up a PostgreSQL 15 service container during the `lint-and-test-backend` job, ensuring CI tests execute correctly against a live database.

## Evidence

### Before State
```python
# backend/core/config.py
TEST_DATABASE_URL: str = "sqlite+aiosqlite:///:memory:"

# test_correlation_crud.py
result = await db_session.execute(text("PRAGMA index_list('correlation_matches');"))
```

### After State
```python
# backend/core/config.py
TEST_DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/astra_test"

# test_correlation_crud.py
result = await db_session.execute(text("SELECT indexname FROM pg_indexes WHERE tablename = 'correlation_matches';"))
```
```yaml
# .github/workflows/ci.yml
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: astra_test
        ports:
          - 5432:5432
```

### Files Modified
- `backend/core/config.py`
- `backend/tests/crud/test_correlation_crud.py`
- `.github/workflows/ci.yml`

### Result
**PASS** - SQLite removed completely from active testing configurations. Testing relies exclusively on PostgreSQL.
