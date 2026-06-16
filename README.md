# ASTRA (Adaptive Security Threat Response & Automation Platform)

[![CI](https://github.com/boncabee/ASTRA/actions/workflows/ci.yml/badge.svg)](https://github.com/boncabee/ASTRA/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## 1. Project Overview
ASTRA is an enterprise-grade, high-throughput security event processing and automation platform. It acts as the deterministic nervous system for a Security Operations Center (SOC), standardizing disparate telemetry, correlating threats, enforcing strict policies, and executing automated responses at scale.

## 2. Vision
Our vision is to empower security teams with a platform that guarantees deterministic automated responses backed by immutable evidence, significantly reducing Mean Time to Respond (MTTR) while eliminating raw log fatigue.

## 3. Product Purpose
Modern SOCs are overwhelmed by fragmented security alerts and rigid SIEMs that require massive manual effort to triage and respond. ASTRA standardizes ingestion, eliminates noise through correlation, and bridges the gap between detection and automated response.
*Read more in the [Product Requirements Document (PRD)](docs/product/PRD.md).*

## 4. Key Capabilities
- **Universal Event Parsing:** High-speed ingestion mapping raw logs to a Common Event Schema (CES).
- **Observation Engine:** Dynamic threat correlation and risk scoring.
- **Policy Engine:** Deterministic rule evaluation triggering defined actions.
- **Evidence Foundation:** Cryptographically verifiable, append-only audit trails for every automated decision.
- **Automation Foundation:** Asynchronous, non-blocking queue execution for external system integrations.
- **Case Management:** Structured orchestration of observations and evidence for human-in-the-loop review.

## 5. Architecture Overview
ASTRA follows a modular monolith architecture driven by Domain-Driven Design (DDD):
1. **Ingestion:** API receives data -> `Parser` converts to `CESEvent`.
2. **Correlation:** `Observation Engine` groups events -> updates Risk Score.
3. **Decision:** `Policy Engine` evaluates Observation -> creates `PolicyDecision` & saves `Evidence`.
4. **Action:** `Automation Engine` queues task -> Background Worker executes response.
*Explore the architecture in [System Design Document (SDD)](docs/architecture/CASE_FOUNDATION_IMPLEMENTATION.md) and [Architecture Directory](docs/architecture/).*

## 6. Technology Stack
- **Backend:** Python 3.10+, FastAPI, Pydantic V2
- **Database:** PostgreSQL (asyncpg), SQLAlchemy 2.0 ORM, Alembic
- **Testing:** Pytest (100% Coverage Enforced)
- **Environment:** Docker, WSL2, Windows local dev

## 7. Repository Structure
```
ASTRA/
├── backend/            # Core Python API and services
├── docs/               # Official Documentation
│   ├── archive/        # Deprecated and historical validation records
│   ├── architecture/   # Design, ADRs, and Domain Models
│   ├── development/    # Contributing guides and strategies
│   ├── history/        # Sprint completion and phase reports
│   ├── operations/     # Runbooks and environment setup guides
│   ├── product/        # PRDs, roadmaps, and requirements
│   └── standards/      # Global coding and security standards
├── frontend/           # Future UI dashboard
└── README.md           # This file
```

## 8. Quick Start
### Prerequisites
- Docker & Docker Desktop with WSL2 integration
- Python 3.10+

### Run via Docker
```bash
git clone https://github.com/boncabee/ASTRA.git
cd ASTRA
docker-compose up -d db
```

## 9. Local Development Setup
To ensure environment consistency, please follow the canonical [Local Development Setup Guide](docs/operations/LOCAL_DEVELOPMENT_SETUP.md).

```bash
cd backend/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 10. Testing Workflow
All testing is mandated to run from the `backend/` directory utilizing the `astra_test` database.
For complete instructions, refer to the [Testing Guide](docs/operations/TESTING_GUIDE.md).
```bash
cd backend/
pytest
```

## 11. Documentation Index
The central documentation hub is located at [docs/README.md](docs/README.md).
Key links:
- [Product & Roadmap](docs/product/)
- [Architecture](docs/architecture/)
- [Task Breakdown](docs/product/WORK_BREAKDOWN_STRUCTURE.md)
- [Operations Docs](docs/operations/)
- [Global Standards](docs/standards/)

## 12. Development Standards
All development must align with our [Global Development Standards](docs/standards/DEVELOPMENT_STANDARD_GLOBAL.md) and [Coding Standards](docs/standards/CODING_STANDARDS.md).

## 13. Branch Strategy
ASTRA utilizes trunk-based development with short-lived feature branches. All branches must pass the CI/CD pipeline quality gates before merging into `main`.

## 14. CI/CD Overview
Continuous Integration is enforced via GitHub Actions. Merges to `main` require:
- 100% Pytest Coverage
- Zero MyPy type-checking errors
- Zero Bandit security vulnerabilities
- Passing `pip-audit`

## 15. Security Notes
ASTRA is a security product; as such, security is baked into the SDLC. Please refer to our [Security Standards](docs/standards/DEVSECOPS_STANDARD.md) and the [Troubleshooting Guide](docs/operations/TROUBLESHOOTING_GUIDE.md) for connectivity or credential issues.

## 16. Roadmap Overview
Phase 8 focuses on Production Readiness and enterprise hardening. Check the [Roadmap](docs/product/ROADMAP.md) for future capabilities including UI integrations and advanced correlations.

## 17. Contribution Guide
Please review our [Contributing Guidelines](docs/development/CONTRIBUTING.md) and [Documentation Governance Standard](docs/standards/DOCUMENTATION_LIFECYCLE_STANDARD.md) prior to submitting pull requests.

## 18. License
ASTRA is released under the [MIT License](LICENSE).
