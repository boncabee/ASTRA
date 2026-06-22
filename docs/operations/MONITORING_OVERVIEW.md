# Monitoring Overview

## Observability Stack
ASTRA ships with an embedded, enterprise-grade observability stack built on the Prometheus ecosystem. 

### 1. Metrics Collection (Prometheus)
- The FastAPI backend exposes an authenticated `/metrics` endpoint.
- Prometheus is configured via `monitoring/prometheus.yml` to scrape the backend and system metrics every 15 seconds.
- The metrics focus on RED indicators: Rate (requests/sec), Errors (5xx/4xx), and Duration (latency).

### 2. Visualization (Grafana)
- Grafana connects to Prometheus as a data source.
- Operators use the Executive Health Dashboard to monitor system stability.
- Dashboards are configured to display historical trends, allowing for post-mortem analysis of capacity and performance issues.

### 3. Alerting (Alertmanager)
- `monitoring/alertmanager.yml` defines the alert routing configuration.
- Critical alerts (e.g., `astra_backend_up == 0` or high 5xx error rates) trigger severity-based notifications.
- Notifications are routed to a Slack webhook or PagerDuty to page on-call operators.

## Logging
Application logs are output in structured JSON format via `python-json-logger`, ensuring correlation IDs tie together discrete events across the processing pipeline. Docker log rotation is enforced to prevent host disk exhaustion.
