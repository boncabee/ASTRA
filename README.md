# ASTRA (Adaptive Security Threat Response & Automation Platform)

[![CI](https://github.com/boncabee/ASTRA/actions/workflows/ci.yml/badge.svg)](https://github.com/boncabee/ASTRA/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## 1. Project Overview
ASTRA is an enterprise-grade, high-throughput security event processing and automation platform. It acts as the deterministic nervous system for a Security Operations Center (SOC), standardizing disparate telemetry, correlating threats, enforcing strict policies, and executing automated responses at scale.

## 2. Production Status
**Current Status: Production Launch Authorized**
ASTRA has completed its pilot phase and is fully authorized for production workloads. The platform meets stringent CI/CD quality gates, strict security controls, and high-availability operational requirements.

## 3. Key Features
- **Universal Event Parsing:** High-speed ingestion mapping raw logs to a Common Event Schema (CES).
- **Observation Engine:** Dynamic threat correlation and risk scoring.
- **Policy Engine:** Deterministic rule evaluation triggering defined actions.
- **Evidence Foundation:** Cryptographically verifiable, append-only audit trails for every automated decision.
- **Automation Foundation:** Asynchronous, non-blocking queue execution for external system integrations.
- **Case Management:** Structured orchestration of observations and evidence for human-in-the-loop review.

## 4. Architecture Summary
ASTRA follows a modular monolith architecture driven by Domain-Driven Design (DDD). The data flows deterministically:
1. **Ingestion:** API receives data -> `Parser` converts to `CESEvent`.
2. **Correlation:** `Observation Engine` groups events -> updates Risk Score.
3. **Decision:** `Policy Engine` evaluates Observation -> creates `PolicyDecision` & saves `Evidence`.
4. **Action:** `Automation Engine` queues task -> Background Worker executes response.

For a deep dive, see the [Architecture Overview](docs/architecture/ARCHITECTURE_OVERVIEW.md).

## 5. Deployment Model
**Enterprise-Grade Self-Hosted**
ASTRA is designed exclusively for self-hosted deployment on enterprise infrastructure. It utilizes a hardened Docker Compose stack containing the application, database, and observability layers. Note: A multi-tenant SaaS evolution has been intentionally deferred to focus entirely on self-hosted data sovereignty and isolation. 
For more details, see the [Deployment Overview](docs/operations/DEPLOYMENT_OVERVIEW.md).

## 6. Technology Stack
- **Backend:** Python 3.10+, FastAPI, Pydantic V2
- **Database:** PostgreSQL (asyncpg), SQLAlchemy 2.0 ORM, Alembic
- **Testing:** Pytest (100% Coverage Enforced)
- **Deployment:** Docker, NGINX

## 7. Security Features
Security is foundational to ASTRA:
- **Zero-Trust Defaults:** All routes require authentication by default.
- **TLS & Encryption:** Mandatory TLS 1.3 termination via NGINX with HSTS.
- **Immutable Evidence:** Cryptographic auditing of automated decisions.
- **Rate Limiting:** Global IP-based rate limiting to prevent abuse.
- **Container Hardening:** Non-root execution and minimal surface area images.

## 8. Monitoring Stack
ASTRA ships with an embedded observability stack:
- **Metrics:** Prometheus endpoints embedded in all services.
- **Dashboards:** Grafana visualizing the RED (Rate, Errors, Duration) metrics.
- **Alerting:** Alertmanager routing critical failures to Slack/PagerDuty.
For detailed runbooks, see the [Monitoring Overview](docs/operations/MONITORING_OVERVIEW.md).

## 9. Backup & Recovery
Automated daily PostgreSQL logical backups (SQL dump + gzip) are configured on the host. Offsite synchronization and tested disaster recovery drills ensure strict Recovery Point Objectives (RPO) and Recovery Time Objectives (RTO).
See the [Backup & Recovery Overview](docs/operations/BACKUP_RECOVERY_OVERVIEW.md).

## 10. CI/CD Pipeline
Continuous Integration is enforced via GitHub Actions. Merges to `main` and production releases require:
- 100% Pytest Coverage
- Zero MyPy type-checking errors
- Zero Ruff lint violations
- Zero Bandit security vulnerabilities
- Passing `pip-audit` for supply chain security
- Automated SBOM (Software Bill of Materials) generation

For release procedures, see the [Release Process Overview](docs/operations/RELEASE_PROCESS_OVERVIEW.md).

## 11. Quick Start
### Prerequisites
- Docker & Docker Desktop with WSL2 integration (Windows) or native Linux/macOS.
- Python 3.10+ (for local development)

### Run via Docker
```bash
git clone https://github.com/boncabee/ASTRA.git
cd ASTRA
docker-compose -f docker-compose.prod.yml up -d
```

## 12. Documentation Index
The central documentation map is located at [docs/README.md](docs/README.md).

## 13. Roadmap
Having achieved Production Launch Authorization, future roadmap items focus on horizontal scalability, advanced SIEM integrations, and the development of the frontend React dashboard. See [Roadmap](docs/product/ROADMAP.md) for specifics.

## 14. License
ASTRA is released under the [MIT License](LICENSE).
