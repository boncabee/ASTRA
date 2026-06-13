# ASTRA

Security Event Normalization, Correlation, and Threat Analysis Platform

---

## Overview

**Purpose**: To provide a unified, robust, and scalable platform for ingesting, normalizing, correlating, and analyzing disparate security events across diverse network architectures.

**Scope**: End-to-end security event management, from raw log ingestion and parsing via a Common Event Schema (CES) to advanced threat detection and response integration.

**Vision**: To empower Security Operations Centers (SOCs) with high-fidelity, actionable intelligence by seamlessly translating complex, multi-vendor telemetry into standardized, context-rich security narratives.

---

## Key Features

* **Common Event Schema (CES)**
* **Parser Framework**
* **VPN Parser**
* **Windows Parser**
* **Firewall Parser**
* **Parser Registry**
* **Batch Processing**
* **Fallback Mapping**

---

## Current Status

| Phase / Milestone | Status |
| :--- | :--- |
| **Sprint 1** | Complete |
| **Sprint 2** | Complete |
| **Sprint 3** | Planned |
| **Architecture Review** | Approved With Revisions |

---

## Architecture Overview

Raw Logs
↓
Parsers
↓
TransformerConfig
↓
CES
↓
Correlation Engine
↓
Detection Engine
↓
AKM

---

## Technology Stack

* **Frontend**: Next.js, React, TypeScript
* **Backend**: Python, FastAPI, Pydantic, SQLAlchemy
* **Database**: PostgreSQL
* **Testing**: Pytest (Backend), Vitest (Frontend)
* **Documentation**: Markdown

---

## Repository Structure

* `backend/` - FastAPI server, core business logic, parsers, and database models
* `frontend/` - Next.js web application and UI components
* `docs/` - Comprehensive architectural, planning, and governance documentation
* `datasets/` - Golden datasets and sample logs for testing and validation
* `infrastructure/` - Infrastructure as Code (IaC) and deployment manifests
* `docker/` - Containerization configurations
* `scripts/` - Automation, CI/CD, and utility scripts
* `tests/` - Standalone integration and end-to-end testing suites

---

## Quick Start

### Prerequisites
* Python 3.10+
* Node.js 18+
* PostgreSQL

### Environment Setup

#### Virtual Environment Setup (Backend)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

#### Dependency Installation
```bash
# Backend dependencies
cd backend
pip install -r requirements.txt

# Frontend dependencies
cd ../frontend
npm install
```

### Run Backend
```bash
cd backend
# Ensure your .venv is active
uvicorn app.main:app --reload
```

### Run Frontend
```bash
cd frontend
npm run dev
```

### Run Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm run test
```

---

## Documentation

* [Project Plan](docs/planning/PROJECT_PLAN.md)
* [Architecture](docs/architecture/ARCHITECTURE.md)
* [Roadmap](docs/planning/ROADMAP.md)
* [API Specification](docs/architecture/API_SPEC.md)
* [Database Schema](docs/architecture/DATABASE_SCHEMA.md)
* [Security Policy](docs/security/SECURITY.md)
* [Threat Model](docs/security/THREAT_MODEL.md)
* [Testing Strategy](docs/governance/TESTING_STRATEGY.md)
* [Deployment](docs/DEPLOYMENT.md)
* [Report Index](docs/REPORT_INDEX.md)
* [Open Findings](docs/OPEN_FINDINGS.md)

---

## Development Workflow

* **Branching**: Use task-based feature branches extending from `main`.
* **Pull Requests**: Require peer review and passing CI pipelines before merging.
* **Testing**: 100% test coverage mandated for core components (parsers, schema).
* **Code Quality**: Enforced via strict typing (Mypy, Pyright) and linting (ESLint, Prettier).
* **Type Safety**: Leverage Pydantic models in Python and strict TypeScript types in the frontend.

---

## Roadmap

* **Sprint 1**: Establish Common Event Schema (CES) foundation and repository structure. *(Complete)*
* **Sprint 2**: Implement core Parser Framework, Parser Registry, and parsers (VPN, Windows, Firewall). *(Complete)*
* **Sprint 3**: Develop Correlation Engine and baseline Detection Engine heuristics. *(Planned)*
* **Future**: Advanced threat detection, SOAR integrations, and cloud-native auto-scaling.

---

## Security

Please review our comprehensive security protocols and models:
* [Security Policy](docs/security/SECURITY.md)
* [Threat Model](docs/security/THREAT_MODEL.md)

---

## Contributing

We welcome contributions! Please adhere to our guidelines:
* [Contributing Guide](docs/governance/CONTRIBUTING.md)
* [Development Guidelines](docs/governance/DEVELOPMENT_GUIDELINES.md)

---

## License

License: TBD

---

## Acknowledgements

Special thanks to the open-source community and all early contributors to the ASTRA project.