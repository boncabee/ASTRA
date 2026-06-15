# Dependency Audit Report

## 1. Overview
The Dependency Audit reviews the external packages and libraries used by the ASTRA project for modernization, security, and stability.

## 2. Strengths
- **Modern Python Ecosystem:** The backend utilizes the latest industry standards: FastAPI (0.111.0), SQLAlchemy 2.0+, and Pydantic V2.
- **Pinned Dependencies:** All core backend dependencies in `requirements.txt` are strictly pinned, preventing accidental breaking changes during deployment.

## 3. Weaknesses
- **Development vs. Production Separation:** `pytest` and `pytest-cov` are included directly in the main `requirements.txt` rather than isolated to a `requirements-dev.txt` or `pyproject.toml` `[dev-dependencies]` section.
- **Frontend Dependencies:** Next.js is installed, but testing and linting toolchains in the frontend `package.json` are incomplete or misconfigured.

## 4. Findings
- **Finding 1:** Testing libraries (pytest, pytest-asyncio, pytest-cov) are mixed into production dependencies.
- **Finding 2:** Strong reliance on asynchronous drivers (`asyncpg`).

## 5. Risks
- **Bloat Risk:** Deploying test runners to production containers increases the image size and potential attack surface.

## 6. Technical Debt
- **Medium:** Lack of a modern dependency manager (like Poetry or uv) makes managing transitive dependencies difficult.

## 7. Standards Violations
- Testing tools mixed with production dependencies.

## 8. Recommendations
| Priority | Recommendation |
|---|---|
| **High** | Split `requirements.txt` into `requirements.txt` (production) and `requirements-dev.txt` (development/testing), or migrate to `pyproject.toml` with Poetry/uv. |
| **Medium** | Finalize frontend `package.json` testing and linting scripts. |
