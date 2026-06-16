# Testing Guide

## Purpose
This document establishes the canonical procedures for executing the ASTRA testing suite. It ensures consistency in test execution, tooling usage, and quality assurance workflows.

## Scope
This guide covers unit tests, integration tests, static analysis, code coverage, and vulnerability scanning for the backend application.

## Procedure

### Required Working Directory
**CRITICAL:** All tests and static analysis tools MUST be executed from the `backend/` directory, **NOT** the repository root.

```bash
cd backend/
```

### 1. Canonical Test Execution Procedure (pytest)
To execute the complete test suite (both unit and integration tests):
```bash
pytest
```
To run tests with verbose output and print standard output:
```bash
pytest -v -s
```

### 2. Integration Testing Workflow
Integration tests validate the interaction between the application and the PostgreSQL database.
Ensure your `TEST_DATABASE_URL` is correctly configured in your `backend/.env` file and the database container is running.
```bash
pytest tests/integration/
```

### 3. Code Coverage Usage (coverage)
To measure code coverage during test execution:
```bash
pytest --cov=app --cov-report=term-missing
```
For an HTML report:
```bash
pytest --cov=app --cov-report=html
```

### 4. Type Checking (mypy)
To execute static type checking:
```bash
mypy app/
```

### 5. Security Vulnerability Scanning (bandit)
To scan the application code for common security vulnerabilities:
```bash
bandit -r app/
```

### 6. Dependency Auditing (pip-audit)
To scan installed dependencies for known vulnerabilities:
```bash
pip-audit
```

## Verification

### Expected Success Outputs
- **pytest:** Shows all tests passing (e.g., `345 passed in 12.34s`) with no failures or errors.
- **coverage:** Shows the required line coverage (e.g., `TOTAL 99%`).
- **mypy:** Outputs `Success: no issues found in X source files`.
- **bandit:** Reports `No issues identified`.
- **pip-audit:** Reports `No known vulnerabilities found`.

## Troubleshooting
- **pytest collection failures:** Ensure you are in the `backend/` directory and your virtual environment is active.
- **Integration test connection errors:** Verify `astra_test` database exists and `TEST_DATABASE_URL` is valid.
Refer to the [Troubleshooting Guide](./TROUBLESHOOTING_GUIDE.md) for more details.

## References
- [pytest documentation](https://docs.pytest.org/)
- [mypy documentation](https://mypy.readthedocs.io/)
