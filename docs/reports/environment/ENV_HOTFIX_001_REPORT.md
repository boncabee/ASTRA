---
id: ENV-HOTFIX-001
type: environment-report
sprint: 2
status: PASS
---

# Executive Summary

The ASTRA platform development environment previously had a critical runtime drift between the CI/CD pipeline (Python 3.11) and the local development environment (Python 3.14.5). This drift has been successfully eliminated by upgrading the GitHub Actions workflows and the backend Dockerfile to use Python 3.14. The environment is now perfectly aligned, ensuring that all linting, static type checking, and unit tests execute consistently across both local and CI environments.

# Changes Applied

- Upgraded the Python runtime in the GitHub Actions continuous integration workflow from 3.11 to 3.14.
- Upgraded the Python base image in the backend Docker build file from `python:3.11-slim` to `python:3.14-slim`.
- Validated that `asyncpg 0.31.0` (previously updated during stabilization) functions correctly without build issues under Python 3.14.

# Files Modified

- `.github/workflows/ci.yml`: Updated `python-version: "3.11"` to `python-version: "3.14"` in the `setup-python` action.
- `backend/Dockerfile`: Updated the base image from `FROM python:3.11-slim` to `FROM python:3.14-slim`.

# Validation Results

- **Local Runtime Aligned with CI:** ✓ (Both are now Python 3.14)
- **Dependency Installation:** ✓ (Succeeds via pip without compilation errors for asyncpg 0.31.0)
- **Pytest:** ✓ (All 23 backend tests passed successfully)
- **Pyright:** ✓ (Static type checking passes with zero errors)
- **Mypy:** ✓ (Zero type issues found across 23 source files)

# Risks Identified

- None. The runtime environment is completely synced.

# Recommendations

- Moving forward, when updating the local Python version, ensure that `ci.yml` and `Dockerfile` are updated in tandem to prevent runtime drift from recurring. 

# Final Decision

PASS
