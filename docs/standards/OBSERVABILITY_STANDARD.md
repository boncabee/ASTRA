# Observability Standard

This document defines the telemetry, monitoring, and alerting requirements to ensure ASTRA remains highly available and strictly auditable.

## 1. Logging Standards
- **Format:** All application logs MUST be written to `stdout`/`stderr` in structured JSON format. Multi-line string logs are prohibited.
- **Context:** Every log entry must include a unique `request_id` or `correlation_id` injected at the middleware layer.
- **Sanitization:** Passwords, API keys, full JWTs, and PII must be scrubbed or masked before the log is emitted.

## 2. Metrics Standards
- **Exposition:** ASTRA exposes a `/metrics` endpoint formatted for Prometheus scraping.
- **RED Method:** The system must track Rate (requests per second), Errors (4xx/5xx count), and Duration (latency histograms) for all HTTP endpoints.
- **Business Metrics:** Custom metrics must be emitted for Core Domain events (e.g., `astra_events_ingested_total`, `astra_automations_executed_total`).

## 3. Tracing Standards
- **Distributed Tracing:** OpenTelemetry (OTel) is used to track requests across microservice boundaries (e.g., from the API to the Celery Worker).
- **Propagation:** W3C Trace Context headers (`traceparent`, `tracestate`) must be propagated in all external HTTP requests and message queue payloads.

## 4. Audit Logging Standards
- **System Audit:** Standard logs (Section 1) capture system health.
- **Security Audit (Evidence):** All business-logic decisions (e.g., Policy triggered, Automation fired) are strictly logged to the immutable Postgres `evidence` table, not just standard output.
- **Admin Actions:** Any modification to user roles, policies, or system configurations by an Admin must generate a distinct `AuditLog` entry detailing the `actor_id`, `action`, `timestamp`, and `previous_state`.

## 5. Alerting Standards
- **Actionability:** Alerts must only be configured for actionable events. "CPU is at 80%" is a metric, not an alert. "API latency exceeded 500ms for 5 minutes" is an alert.
- **Routing:** 
  - **Critical:** PagerDuty/OpsGenie (e.g., Database down, Ingestion queue overflowing).
  - **Warning:** Slack channel (e.g., High rate of 401 Unauthorized errors).

## 6. Monitoring Standards
- **Dashboards:** Grafana is the standard visualization tool.
- **Core Dashboards:**
  1. **Executive Health:** High-level RED metrics and Uptime.
  2. **Ingestion Pipeline:** EPS (Events Per Second), Queue depth, Parser error rates.
  3. **Automation Health:** Worker active count, task failure rates.
