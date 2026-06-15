# Software Design Document (SDD)
**Project:** ASTRA (Adaptive Security Threat Response & Automation Platform)

## 1. System Architecture Overview
ASTRA is designed as a modular, API-first microservice monolith (modular monolith). It is built to run reliably under heavy load, separating high-throughput event ingestion from asynchronous backend processing tasks like automation.

## 2. Backend Architecture
The backend is structured using a Domain-Driven Design (DDD) approach.
- **API Layer:** FastAPI routers exposing RESTful endpoints.
- **Service Layer:** Business logic orchestration (e.g., CorrelationService, ObservationService, AutomationService).
- **Repository Layer:** Abstracted data access patterns using SQLAlchemy ORM.
- **Domain Layer:** Pydantic and SQLAlchemy models.

## 3. Database Architecture
- **Primary Datastore:** PostgreSQL.
- **ORM:** SQLAlchemy with asynchronous drivers (`asyncpg`).
- **Schema Management:** Alembic for automated migrations.
- **Key Constraints:** UUID primary keys, strict foreign key relationships, and indexed query paths for performance.

## 4. Domain Model Relationships
- `CESEvent` (Many) -> `Correlation` (One)
- `Correlation` (One) -> `Observation` (One)
- `Observation` (One) -> `PolicyDecision` (Many)
- `PolicyDecision` (One) -> `Evidence` (One)
- `PolicyDecision` (One) -> `AutomationRequest` (One or Many)

## 5. API Architecture
- **Framework:** FastAPI.
- **Protocol:** HTTP/REST.
- **Security:** OAuth2 with JWT Bearer tokens.
- **Design:** Versioned endpoints (e.g., `/api/v1/correlations`), strictly typed Pydantic request/response schemas.

## 6. Queue & Worker Architecture
- **Broker:** Redis (or RabbitMQ pending final deployment).
- **Worker Framework:** Celery (or native Python `asyncio` queues for MVP).
- **Flow:** API generates an `AutomationRequest` -> places it on Queue -> background Worker consumes Request -> executes external API call -> updates DB state.

## 7. Evidence Architecture
- **Immutability:** The `Evidence` repository implements append-only logic. Update and Delete operations raise a `NotImplementedError` or `PermissionError` at the ORM layer.
- **Provenance:** Every `Evidence` record strongly links to the `PolicyDecision` and the exact state of the `Observation` at the time of the decision.

## 8. Deployment Architecture
- **Containerization:** Docker & Docker Compose for local dev/testing.
- **Orchestration:** Kubernetes (Production target).
- **CI/CD:** GitHub Actions for automated linting, testing, and Docker image publishing.

## 9. Technology Decisions
- **Language:** Python 3.12+ (chosen for data science/AI ecosystem compatibility).
- **Web Framework:** FastAPI (chosen for performance and native async support).
- **Database:** PostgreSQL (chosen for ACID compliance and JSONB support).
- **Type Checking:** Pyright / Mypy (strict mode).
