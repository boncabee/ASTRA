# Deployment Overview

## Deployment Model
ASTRA utilizes an **Enterprise-Grade Self-Hosted** deployment model. We have intentionally deferred any SaaS multi-tenant evolution to prioritize data sovereignty, tenant isolation, and regulatory compliance for enterprise customers.

## Target Environment
The production stack is designed to run on a hardened Linux Virtual Machine (e.g., Ubuntu 24.04 LTS) utilizing Docker and Docker Compose. 

## Component Topology
The `docker-compose.prod.yml` defines the following isolated services:
1. **NGINX Reverse Proxy:** Handles TLS 1.3 termination, rate limiting, and request routing.
2. **FastAPI Backend:** The core Python 3.10+ application, running under Uvicorn and scaled via Gunicorn workers.
3. **PostgreSQL:** The primary relational database.
4. **Prometheus:** Scrapes `/metrics` from the backend and system endpoints.
5. **Grafana:** Visualizes metrics and provides operator dashboards.
6. **Alertmanager:** Routes critical infrastructure alerts to Slack/PagerDuty.

## Network Security
- Only ports 80 (redirect) and 443 (HTTPS) are exposed to the external network.
- Internal services (Postgres, Prometheus) communicate over isolated internal Docker bridge networks and are unreachable from the outside.
