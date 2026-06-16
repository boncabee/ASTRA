# Architecture Review Report

## Executive Summary
This report summarizes the architectural state of the ASTRA platform at the conclusion of Phase 5. ASTRA has successfully implemented a monolithic, modular Python API using FastAPI and SQLAlchemy to support a robust pipeline from raw events (Correlation) to finalized outputs (Reporting). 

**Go / No-Go Recommendation for Phase 6 (Automation Foundation):** 
**GO, with reservations.**
ASTRA's backend architecture is stable, well-tested, and correctly enforces immutable logging and RBAC. However, before executing Phase 6 (Automation), the team must address the synchronous execution model (Technical Debt TD-003) to prevent API blocking when executing automated tasks.

---

## Domain Evaluations

### 1. Identity Domain
- **Strengths:** Robust, standard-based implementation using UUIDs and specific Enum roles (Administrator, Security Engineer, SOC Analyst, Incident Responder).
- **Weaknesses:** RBAC relies on a heavy `enforce_deny_by_default` global middleware pattern which proved brittle during testing, requiring route-level dependency overrides.
- **Gaps:** No integration with external enterprise Identity Providers (IdP) like Azure AD or Okta (ADR-010 is partially unmet).
- **Recommendations:** Refactor RBAC into standard FastAPI dependency injection patterns without relying heavily on `request.scope.route.dependencies` inspection.

### 2. Correlation Domain
- **Strengths:** Excellent separation of concerns. The schema enforcement ensures all downstream domains receive clean `CorrelationMatch` data.
- **Weaknesses:** Highly reliant on the PostgreSQL backend. No streaming or message queue (e.g., Kafka) sits in front of the engine, limiting high-throughput scaling.
- **Gaps:** Real-time stream processing is missing.
- **Recommendations:** Introduce a message broker (Redis Pub/Sub or RabbitMQ) for ingesting massive event volumes before they hit the database.

### 3. Observation Domain
- **Strengths:** Acts as the central anchor for the system. Risk scoring effectively normalizes disparate correlation findings into actionable intelligence.
- **Weaknesses:** The `list` querying currently handles filtering and pagination, but heavy offset usage could degrade performance as the table grows.
- **Gaps:** Missing geospatial or enriched metadata hooks out of the box.
- **Recommendations:** Implement keyset pagination for API retrieval of Observations.

### 4. Policy Domain
- **Strengths:** Clear abstraction between `Policy` definition and `PolicyEvaluation` results. Allows for complex logic targeting specific `Observation` states.
- **Weaknesses:** Execution is synchronous. A slow policy evaluation locks the API thread.
- **Gaps:** No visual builder or complex DAG constraint mechanism for conflicting policies.
- **Recommendations:** Introduce an async task queue (e.g., Celery) to evaluate policies in the background.

### 5. Evidence Domain
- **Strengths:** Strong enforcement of decision provenance. Evidence and Audit records are strictly immutable, storing content references and hash values natively.
- **Weaknesses:** Storing JSON blobs in relational columns could bloat the primary database.
- **Gaps:** No external object storage (e.g., S3) linked for raw payload archiving.
- **Recommendations:** Migrate heavy payload references to an S3-compatible backend, storing only the metadata in PostgreSQL.

### 6. Reporting Domain
- **Strengths:** Efficiently aggregates up to 10,000 observations into a lightweight, structural JSON snapshot containing relevant evidence and audit linkages. Includes native compliance mapping tags.
- **Weaknesses:** "Report" is merely a JSON data payload, not a human-readable format like PDF.
- **Gaps:** Scheduled reporting and PDF rendering are entirely absent.
- **Recommendations:** Build an asynchronous report rendering service utilizing headless Chromium or LaTeX generators.

---

## Architectural Review Criteria

- **Scalability:** **Medium.** The monolithic API handles thousands of records efficiently, but lacks the message queues needed for millions of events per second.
- **Security:** **High.** Role-Based Access Control and strict Secret Management (ADR-011) are thoroughly enforced. 
- **Performance:** **Medium-High.** Queries are optimized, but synchronous execution bottlenecks remain.
- **Compliance Readiness:** **High.** Complete audit trailing and evidence preservation satisfy strict frameworks (ISO 27001, NIST).
- **Maintainability:** **High.** The modular nature of the FastAPI layout ensures strong testability (100% pass rates across critical domains).
- **Extensibility:** **High.** New domains (like Automation) can easily attach to the existing Observation/Policy hooks.
- **Operational Readiness:** **Medium.** Missing core operational tooling (e.g., Prometheus metrics scraping, health probe sidecars, robust CD pipelines).
