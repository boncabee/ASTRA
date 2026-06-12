# ASTRA Repository Bootstrap Specification

**Version:** 3.1
**Date:** 2026-06-12
**Status:** Approved

---

## Executive Summary
This document provides the definitive blueprint for initializing the ASTRA v3.1 monorepo (Sprint 0). It defines the exact directory layouts, naming conventions, tooling baselines, and governance standards that must be implemented. This specification serves as the absolute source of truth for autonomous AI agents and human developers bootstrapping the environment. **No business logic (CES, AKM, Playbooks, or AI integration) is to be developed under this spec.**

---

## Repository Layout
The root of the monorepo must strictly adhere to the following structure:

```text
/
├── frontend/         # Next.js React UI application
├── backend/          # FastAPI Python backend application
├── docs/             # Authoritative project documentation
├── prompts/          # AI system prompts (empty scaffolding for future sprints)
├── tests/            # Global/E2E test suites and integration tests
├── datasets/         # Golden datasets for testing (empty scaffolding)
├── infrastructure/   # IaC, deployment scripts, Kubernetes/Cloud Run configs
├── scripts/          # Local development scripts (bootstrap, db migration)
├── .github/          # CI/CD workflows and GitHub Actions
├── docker/           # Shared Dockerfile templates or compose networks
└── README.md         # Developer onboarding guide
```

---

## Backend Structure
The `backend/` directory operates on a clean, modular architecture using FastAPI.

```text
backend/
├── app/              # Application entry points (main.py, lifespan events)
├── api/              # API routers and versioning (e.g., v1/endpoints)
├── services/         # Business logic layer separating logic from transport
├── models/           # SQLAlchemy ORM definitions mapping to tables
├── repositories/     # Data access layer for database queries
├── schemas/          # Pydantic models for validation and serialization
├── core/             # Cross-cutting concerns (config, logging, security)
├── integrations/     # External API clients (empty scaffolding for future sprints)
└── tests/            # Unit tests localized to the backend module
```

**Responsibilities:**
* **`api/`:** Handles only HTTP routing, request parsing, and response formatting. Defers logic to `services/`.
* **`services/`:** Orchestrates logic. Contains zero HTTP knowledge.
* **`repositories/`:** Handles all raw database interactions.
* **`core/`:** Centralizes environment loading and application middleware.

---

## Frontend Structure
The `frontend/` directory operates on Next.js 15 utilizing the App Router architecture.

```text
frontend/
├── src/              # Root source directory
│   ├── app/          # Next.js App Router definitions, pages, and layouts
│   ├── components/   # Reusable UI React components (buttons, modals)
│   ├── services/     # API integration methods (fetch wrappers, API hooks)
│   ├── hooks/        # Custom React hooks for local state management
│   ├── layouts/      # Application wrappers and persistent navigational shells
│   ├── styles/       # Tailwind CSS overrides and global stylesheets
└── tests/            # Vitest/Jest unit and component tests
```

**Responsibilities:**
* **`app/`:** Governs URL routing and server-side components.
* **`components/`:** Pure, presentation-focused UI elements.
* **`services/`:** Isolates all network requests to the ASTRA Backend API.

---

## Naming Conventions
All source code must adhere strictly to these conventions:
* **Files:** `snake_case.py` (Python), `kebab-case.ts`/`kebab-case.tsx` (TypeScript/React).
* **Classes:** `PascalCase` (Python & TypeScript).
* **Functions:** `snake_case` (Python), `camelCase` (TypeScript).
* **Variables:** `snake_case` (Python), `camelCase` (TypeScript).
* **Environment Variables:** `UPPER_SNAKE_CASE` (e.g., `DATABASE_URL`).
* **Database Objects:** Tables and Columns must be `snake_case`. Table names must be plural nouns (e.g., `incidents`).
* **API Endpoints:** Kebab-case, plural nouns (e.g., `/api/v1/investigation-jobs`).

---

## Dependency Management
* **Backend:** Tracked via `requirements.txt` or `pyproject.toml` using `pip`. All versions must be explicitly pinned.
* **Frontend:** Tracked via `package.json` utilizing `npm` or `pnpm` with `package-lock.json` committed.
* **Versioning policy:** Semantic Versioning (SemVer) strictly enforced.
* **Upgrade policy:** Dependencies can only be upgraded via dedicated, isolated pull requests passing CI security scans.

---

## Configuration Standards
* **Environment variables only:** All configuration must be loaded via `.env` at runtime (parsed via strict Pydantic `BaseSettings` in the backend).
* **No hardcoded secrets:** Connection strings, keys, salts, or passwords are strictly prohibited in the codebase.
* **Reference:** `SECURITY.md`

---

## Logging Standards
* **Required Levels:**
  * `INFO`: Standard lifecycle events (e.g., application startup).
  * `WARN`: Recoverable errors, retries, or unexpected edge cases.
  * `ERROR`: Critical failures requiring human intervention.
  * `AUDIT`: Highly structured logs tracing security decisions, login attempts, and model outputs.
* **Format Requirements:** All logs must be emitted as strictly structured JSON.
* **Required Fields:** Every log must contain `timestamp`, `level`, `request_id`, and `message`.

---

## Testing Standards
**Reference:** `TESTING_STRATEGY.md`
* **Coverage targets:** Minimum >= 70% branch and line coverage required globally.
* **Folder locations:** Placed in dedicated `/tests` folders mirroring the source code structure.
* **Naming standards:** `test_*.py` for Python, `*.test.ts` or `*.spec.ts` for frontend components.

---

## Documentation Standards
**References:** 
* `DEVELOPMENT_GUIDELINES.md`
* `AI_AGENT_INSTRUCTIONS.md`
* `AGENT_TASK_EXECUTION_FRAMEWORK.md`

Code changes without corresponding documentation updates are considered defective.

---

## Security Requirements
**References:** 
* `SECURITY.md`
* `THREAT_MODEL.md`

**Required implementations for Sprint 0:**
* **Secret scanning:** e.g., `gitleaks` integrated into GitHub Actions blocking PRs.
* **Dependency scanning:** e.g., `pip-audit` and `npm audit` blocking vulnerable dependencies.
* **Audit logging:** Base middleware constructed to capture API transactions with a `request_id`.

---

## CI/CD Requirements
**References:** 
* `IMPLEMENTATION_STRATEGY.md`
* `DEPLOYMENT.md`
* `RELEASE_PLAN.md`

Sprint 0 mandates an automated pipeline guaranteeing that builds, tests, linters, and security checks all pass prior to merging any pull request.

---

## Bootstrap Deliverables
By the end of Sprint 0, the following core files and artifacts must exist and function:
* `.github/workflows/ci.yml` (The active CI pipeline)
* `docker-compose.yml` (The local orchestration stack)
* `backend/Dockerfile`, `backend/requirements.txt`, `backend/app/main.py`
* `frontend/Dockerfile`, `frontend/package.json`, `frontend/src/app/layout.tsx`
* `backend/core/config.py` (The environment variable validation engine)
* `backend/alembic.ini` and `backend/alembic/env.py` (The migration skeleton)
* Empty, functioning scaffolding for test suites across both modules.

---

## Bootstrap Acceptance Criteria
The Sprint 0 Repository is formally accepted **only if**:
* It builds successfully natively and via CI.
* Tests execute locally and via CI (passing with coverage metrics).
* Docker starts (`docker compose up` brings up all services and networks cleanly).
* Backend starts (FastAPI successfully responds on `/health`).
* Frontend starts (Next.js development server successfully renders the layout).
* CI passes (All GitHub Actions status checks report green).
* Security checks pass (Zero secrets detected, zero high-severity dependencies).
