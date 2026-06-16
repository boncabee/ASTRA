# CI/CD Governance Standard

This document defines the automated pipelines and deployment workflows for the ASTRA platform.

## 1. Build Pipeline Standards
- **Trigger:** Executes on every push to a branch and every Pull Request.
- **Actions:** 
  1. Code formatting check (Black).
  2. Static type checking (Pyright/Mypy).
  3. Linter execution (Ruff).
  4. Docker image build (to ensure the `Dockerfile` is valid).
- **Rule:** If the build pipeline fails, the PR cannot be merged.

## 2. Testing Pipeline Standards
- **Trigger:** Executes in parallel with or immediately following the Build Pipeline.
- **Actions:**
  1. Unit tests (`pytest`).
  2. Integration tests via Testcontainers.
  3. Coverage report generation (fails if < 100%).
  4. Security scans (Bandit, Secrets check).
- **Rule:** Flaky tests must be disabled, logged as Technical Debt, and fixed. They cannot be allowed to pass sporadically.

## 3. Release Pipeline Standards
- **Trigger:** Executes when a new Semantic Version tag (e.g., `v1.2.0`) is pushed to the `main` branch.
- **Actions:**
  1. Full execution of Build and Testing pipelines.
  2. Build production-optimized Docker image.
  3. Tag image with the version and `latest`.
  4. Generate SBOM.
  5. Push image to the container registry.
  6. Automatically generate GitHub Release Notes based on conventional commits.

## 4. Environment Promotion Strategy
ASTRA utilizes a three-tier environment architecture:
1. **Development (Local/Dev):** Developers run ASTRA locally via `docker-compose`. Experimental feature branches may be deployed to a shared Dev environment.
2. **Staging:** A production-like environment. The `main` branch is continuously deployed (CD) here. Performance and DAST testing occur here.
3. **Production:** Deployed only from official Release Tags. Requires manual approval from the Operations Team to promote the container from Staging to Production.

## 5. Rollback Standards
- **Stateless Services:** If the API or Worker containers fail health checks post-deployment, Kubernetes (or the orchestrator) automatically rolls back to the previous image tag.
- **Database Migrations:** Alembic schema migrations must always include a `downgrade()` method. If a migration fails or causes data corruption, the `downgrade` script is executed, followed by an image rollback.

## 6. Artifact Retention
- **Docker Images:** Production-tagged images are retained indefinitely. `main` branch (staging) images are retained for 30 days. Feature branch images are retained for 7 days.
- **Evidence Logs:** Retained in the database indefinitely per compliance requirements, rather than pipeline artifacts.
