# Software Requirements Specification (SRS)
**Project:** ASTRA (Adaptive Security Threat Response & Automation Platform)

## 1. Functional Requirements
### 1.1 Ingestion & Parsing
- **REQ-F01:** The system MUST accept incoming security logs via REST API.
- **REQ-F02:** The system MUST parse logs into the Common Event Schema (CES).
- **REQ-F03:** The system MUST gracefully reject malformed logs with a 400 Bad Request error.

### 1.2 Correlation & Observation
- **REQ-F04:** The system MUST group related CES events into a single `Correlation` entity based on configurable temporal and spatial rules.
- **REQ-F05:** The system MUST calculate an aggregate risk score for each Correlation, producing an `Observation`.

### 1.3 Policy & Evidence
- **REQ-F06:** The system MUST evaluate Observations against active Policies to generate a `PolicyDecision`.
- **REQ-F07:** The system MUST persist every PolicyDecision as an immutable `Evidence` record.

### 1.4 Automation
- **REQ-F08:** The system MUST queue `AutomationRequests` based on approved PolicyDecisions.
- **REQ-F09:** The system MUST execute automations asynchronously using background workers.

## 2. Validation & Business Rules
- **Rule 1 (Data Integrity):** No record in the `Evidence` table may be modified or deleted after creation.
- **Rule 2 (Risk Thresholds):** Risk scores must be calculated strictly between 0 and 100.
- **Rule 3 (Automation Guardrails):** Destructive automations (e.g., Firewall Block) REQUIRE a risk score > 80.

## 3. State Transitions
### 3.1 Automation Request State Machine
- `PENDING`: Request received and queued.
- `IN_PROGRESS`: Worker has picked up the request.
- `COMPLETED`: Execution succeeded.
- `FAILED`: Execution failed (terminal state).
- `RETRYING`: Execution failed but is eligible for retry.

## 4. Security & RBAC Rules
- **Admin:** Full read/write access to all endpoints, including user management.
- **Analyst:** Read-only access to Observations, Correlations, and Evidence. Can trigger manual automations.
- **System:** Internal service-to-service role. Bypasses standard UI rate limits but is restricted from destructive user management.
- **Rule 4:** All API endpoints MUST require a valid JWT bearer token.

## 5. Error Handling
- **500 Internal Server Error:** Must be caught globally, logged securely (without PII/secrets), and return a sanitized correlation ID to the client.
- **403 Forbidden:** Must be triggered immediately upon RBAC failure.
- **404 Not Found:** Must obscure whether a resource exists if the user lacks read permissions for that resource class.

## 6. Non-Functional & Performance Requirements
- **NFR-01 (Latency):** The core Policy Engine MUST evaluate a standard policy in under 200ms.
- **NFR-02 (Throughput):** The Event Ingestion API MUST handle 1,000 requests per second.
- **NFR-03 (Availability):** The system MUST be designed for 99.9% uptime (excluding planned maintenance).

## 7. Compliance Requirements
- **COMP-01:** The system MUST comply with basic GDPR data anonymization for generic log retention.
- **COMP-02:** The system MUST retain immutable Evidence logs for a minimum of 1 year to satisfy standard infosec audit requirements.
