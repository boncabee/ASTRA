# ASTRA (Adaptive Security Threat Response & Automation Platform)

[![CI](https://github.com/boncabee/ASTRA/actions/workflows/ci.yml/badge.svg)](https://github.com/boncabee/ASTRA/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## What is ASTRA?
ASTRA is an enterprise-grade, high-throughput security event processing and automation platform. It acts as the deterministic nervous system for a Security Operations Center (SOC), standardizing disparate telemetry, correlating threats, enforcing strict policies, and executing automated responses at scale.

## What problem does ASTRA solve?
Modern SOCs are overwhelmed by fragmented security alerts and rigid SIEMs that require massive manual effort to triage and respond. ASTRA standardizes ingestion, eliminates noise through correlation, and guarantees deterministic automated responses backed by immutable evidence, significantly reducing Mean Time to Respond (MTTR).

## Who is ASTRA for?
- **Security Engineers (Tier 3):** To design deterministic threat policies, map complex correlations, and build reliable automation workflows.
- **Security Analysts (Tier 1/2):** To quickly triage high-risk observations enriched with deep context, bypassing raw log fatigue.
- **Incident Responders:** To rely on immutable, auditable evidence trails detailing exactly why an automated action was taken.

## Current Capabilities
- **Universal Event Parsing:** High-speed ingestion mapping raw logs to a Common Event Schema (CES).
- **Observation Engine:** Dynamic threat correlation and risk scoring.
- **Policy Engine:** Deterministic rule evaluation triggering defined actions.
- **Evidence Foundation:** Cryptographically verifiable, append-only audit trails for every automated decision.
- **Automation Foundation:** Asynchronous, non-blocking queue execution for external system integrations (webhooks, blocking IPs, ticketing).

## Current Limitations
- **Not a Cold Storage SIEM:** ASTRA processes active threats but is not designed for multi-year cold storage search of benign logs.
- **No GUI Yet:** Currently, all interactions are via REST API. The UI dashboard is slated for future phases.
- **Case Management:** Does not replace full-featured ticketing systems (e.g., Jira/ServiceNow) but integrates with them.

## Architecture Overview
ASTRA follows a modular monolith architecture driven by Domain-Driven Design (DDD):
1. **Ingestion:** API receives data -> `Parser` converts to `CESEvent`.
2. **Correlation:** `Observation Engine` groups events -> updates Risk Score.
3. **Decision:** `Policy Engine` evaluates Observation -> creates `PolicyDecision` & saves `Evidence`.
4. **Action:** `Automation Engine` queues task -> Background Worker executes response.

## Technology Stack
- **Backend:** Python 3.12+, FastAPI, Pydantic V2
- **Database:** PostgreSQL (asyncpg), SQLAlchemy ORM, Alembic
- **Queues/Workers:** Celery / Redis
- **Testing:** Pytest (100% Coverage Enforced)

## Quick Start Guide

### Prerequisites
- Docker & Docker Compose
- Python 3.12 (for local development without Docker)

### Run via Docker (Recommended)
```bash
git clone https://github.com/boncabee/ASTRA.git
cd ASTRA
docker-compose up --build
```
The API will be available at `http://localhost:8000`. API documentation (Swagger) is available at `http://localhost:8000/docs`.

## Development Setup
For local development and testing:
```bash
# Set up virtual environment
python -m venv .venv
source .venv/bin/activate  # Or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r backend/requirements.txt
pip install -r backend/requirements-dev.txt

# Run tests
pytest backend/tests/ -v --cov=backend/src
```

## Documentation Index
Comprehensive documentation is located in the `docs/` directory:
- [Product & Roadmap](docs/01-product/)
- [Requirements (SRS)](docs/02-requirements/)
- [Architecture & SDD](docs/03-architecture/)
- [UI/UX Concepts](docs/04-ui-ux/)
- [Engineering Standards](docs/05-engineering/)
- [Operations & Runbooks](docs/06-operations/)
- [Governance & Decisions](docs/07-governance/)
- [Historical Reports](docs/08-history/)

## Contribution Guide
Please review our [Contributing Guidelines](docs/05-engineering/CONTRIBUTING.md) and [Documentation Governance Standard](docs/07-governance/DOCUMENTATION_GOVERNANCE_STANDARD.md) before submitting pull requests.

## License
ASTRA is released under the [MIT License](LICENSE).
