# PHASE 12A: OBSERVABILITY STACK DOCUMENTATION

**Date:** 2026-06-22  
**Agent:** ASTRA Production Launch Blocker Remediation Agent  
**Status:** COMPLETE  
**Scope:** Production Monitoring Stack (LB-003) and Alerting Implementation (LB-004)  

---

## 1. Overview

To resolve LB-003 (Prometheus + Grafana) and LB-004 (Alerting), we have integrated a production-ready telemetry and alerting stack into the ASTRA Production Docker Compose architecture. This setup provides historical metric visualization, capacity planning data, and immediate on-call notifications without exposing monitoring telemetry to the public internet.

---

## 2. Telemetry Stack Architecture

The telemetry stack consists of three coordinated services running on isolated internal networks:

```text
  Public Internet
        │
        ▼ (Port 443)
┌────────────────┐
│  NGINX Proxy   │
└───────┬────────┘
        │
        ├──────────────────────┐ (Internal Proxy Network)
        ▼                      ▼
┌───────────────┐      ┌───────────────┐
│   Frontend    │      │    Grafana    │ (Visualization at /grafana/)
└───────────────┘      └───────┬───────┘
                               │ (Internal Monitoring Network)
                               ▼
                       ┌───────────────┐
                       │  Prometheus   │ ◄─── Scrapes ───► ┌───────────────┐
                       └───────┬───────┘                   │    Backend    │
                               │                           └───────────────┘
                               ▼
                       ┌───────────────┐
                       │ Alertmanager  │ ─── Notifications ───► Slack Webhook
                       └───────────────┘
```

### Stack Components

1. **Prometheus (v2.53.0):**
   - Configured with a 30-day time-series database retention (`--storage.tsdb.retention.time=30d`).
   - Scrapes the backend's `/metrics` endpoint every 15 seconds.
   - Evaluates alerting rules every 15 seconds.
   - Mounted to a persistent Docker volume (`prometheus_data`).

2. **Alertmanager (v0.27.0):**
   - Receives active alerts from Prometheus.
   - Groups alerts by category and severity to prevent alert fatigue.
   - Injects `SLACK_WEBHOOK_URL` from the host `.env` file at runtime.

3. **Grafana (v11.1.0):**
   - Provisioned automatically with Prometheus set as the default datasource.
   - Served at the `/grafana/` sub-path, routed securely behind the main NGINX proxy.
   - Local user sign-up is disabled (`GF_USERS_ALLOW_SIGN_UP=false`) to enforce security policies.

---

## 3. Production Alerting Rules

Alerts are defined in `monitoring/alerts.yml` and cover critical operational events:

### Rule 1: ASTRABackendDown (Critical)
- **Expression:** `up{job="astra-backend"} == 0`
- **Duration:** 1 minute (`for: 1m`)
- **Action:** Triggers immediate paging to the on-call channel.
- **Description:** Fired if the API container has crashed or is unreachable.

### Rule 2: ASTRAHigh5xxRate (Warning)
- **Expression:** `rate(http_requests_total{job="astra-backend",status=~"5.."}[5m]) / rate(http_requests_total{job="astra-backend"}[5m]) > 0.05`
- **Duration:** 5 minutes
- **Action:** Sends a warning alert to the Slack alerts channel.
- **Description:** Fired if more than 5% of incoming requests result in server errors.

### Rule 3: ASTRADiskUsageHigh (Warning)
- **Expression:** `(node_filesystem_size_bytes{mountpoint="/"} - node_filesystem_free_bytes{mountpoint="/"}) / node_filesystem_size_bytes{mountpoint="/"} > 0.80`
- **Duration:** 10 minutes
- **Action:** Sends a warning alert to the Slack alerts channel.
- **Description:** Fired if host disk utilization exceeds 80% capacity.

---

## 4. Alert Routing and Notification

Alertmanager routes alerts based on severity labels defined in the alerting rules:

- **Critical Severity:** Routed immediately to the `#astra-oncall` Slack channel. Repeat interval set to 1 hour to ensure resolution visibility.
- **Warning Severity:** Routed to the `#astra-alerts` Slack channel. Repeat interval set to 4 hours.
- **Slack Webhook Integration:** The Slack webhook URL is kept completely out of the code. It is defined in the operator's `.env` as `SLACK_WEBHOOK_URL` and passed dynamically into the Alertmanager container.

---

## 5. Security & Isolation

- **Network Isolation:** Prometheus and Alertmanager do not expose public ports. They reside on `app_network` and `monitoring_network` respectively.
- **No Direct Prometheus Access:** The Prometheus expression browser is not exposed to the public. It can only be reached via internal routing from Grafana.
- **Grafana Sub-path Routing:** Grafana is mapped behind NGINX. The proxy configuration handles routing requests to `https://<DOMAIN>/grafana/` safely to prevent open ports on `3000`.
