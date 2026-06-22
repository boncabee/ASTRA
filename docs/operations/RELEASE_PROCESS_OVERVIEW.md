# Release Process Overview

## Continuous Integration
All code changes to ASTRA are gated by GitHub Actions. Before a branch can be merged to `main`, it must pass the `ci.yml` workflow, which enforces:
- 100% test coverage (`pytest --cov-fail-under=100`)
- Static type checking (`mypy`)
- Linting and formatting (`ruff`)
- Security scans (`bandit`, `pip-audit`, `gitleaks`)

## Continuous Delivery
ASTRA creates immutable release artifacts. The release process is defined in `.github/workflows/release.yml`:
1. **Tagging:** A developer pushes a semantic version tag (e.g., `v1.0.0`).
2. **Build:** GitHub Actions builds the Docker images for the Backend (and Frontend when active).
3. **SBOM Generation:** Syft is used to generate a CycloneDX JSON Software Bill of Materials.
4. **Publish:** The immutable Docker images are pushed to GitHub Container Registry (GHCR).
5. **Release Note:** A GitHub Release is drafted with the attached SBOM for supply chain auditing.

## Deployment to Production
ASTRA operators deploy releases to self-hosted environments by updating the image tag in their `docker-compose.prod.yml` and executing:
```bash
docker-compose pull
docker-compose up -d
```
All database schema migrations are executed automatically during the container startup sequence via Alembic.
