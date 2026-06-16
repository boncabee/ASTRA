# PHASE 9.0: SELF-HOSTED ARCHITECTURE ASSESSMENT

**Date:** 2026-06-17  
**Status:** DRAFT / ASSESSMENT STAGE  

## Executive Summary
This document provides a comprehensive architecture assessment for the ASTRA v1 Self-Hosted deployment. The objective is to evaluate the current architectural state of ASTRA based on Phase 8 deliverables and analyze potential deployment topologies to identify the optimal official v1 self-hosted architecture.

## Current State
Based on the Phase 8 Production Readiness Gate Review and Readiness Assessments:
1.  **Docker Architecture:** Currently relies on `docker-compose.yml` and `docker-compose.dev.yml` optimized for local development. Production configurations (e.g., non-root users, hardened network mapping) are not yet implemented. Database migrations require manual intervention.
2.  **Observability:** ASTRA is "Production Operable." It implements `correlation_id` request tracing, structured JSON logging with performance metrics, and a Prometheus `/metrics` endpoint via `prometheus-fastapi-instrumentator`.
3.  **Backup & Recovery:** ASTRA is "Production Recoverable" for single-node deployments. Bash scripts (`backup.sh`, `restore.sh`) provide point-in-time `.sql.gz` logical backups with defined RPO (1-4 hours) and RTO (4 hours). Offsite synchronization is a manual operational requirement.
4.  **Secrets & Configuration:** Defaults prioritize developer convenience over security (e.g., default `JWT_SECRET_KEY`, root database user).
5.  **Infrastructure:** No reverse proxy or TLS termination exists. The Next.js frontend and FastAPI backend expose ports directly.

## Deployment Options

We evaluated three primary deployment models for ASTRA v1:

### 1. Single Node (Developer / Sandbox)
- **Description:** All services (Frontend, Backend, DB) run on a single host using the current development `docker-compose.yml`.
- **Pros:** Zero operational overhead; one-click start.
- **Cons:** No TLS, no secrets management, unhardened containers, high security risk if exposed to the internet.

### 2. Small Team (Hardened Docker Compose)
- **Description:** A production-grade Docker Compose stack running on a single, well-provisioned VM. Incorporates a reverse proxy (e.g., NGINX/Traefik) for TLS termination, strict `.env` secrets management, externalized backups, and non-root containers.
- **Pros:** Low operational complexity, strong security posture, easily reproducible, fits the established backup/restore runbooks.
- **Cons:** Limited horizontal scaling (vertical scaling required), manual offsite backup synchronization.

### 3. Kubernetes (Enterprise Scale)
- **Description:** A Helm-chart driven deployment targeting a managed K8s cluster (EKS/GKE/AKS).
- **Pros:** High availability, automated horizontal scaling, declarative infrastructure, advanced secret management (e.g., External Secrets Operator).
- **Cons:** Massive operational complexity for self-hosted users, steep learning curve, requires dedicated DevOps expertise, over-engineered for v1 initial release.

## Operational Tradeoffs

| Feature | Single Node | Small Team | Kubernetes |
| :--- | :--- | :--- | :--- |
| **Complexity** | Very Low | Low-Medium | Very High |
| **Security** | Poor | High | Very High |
| **Maintenance** | Low | Low | High |
| **Scaling** | None | Vertical Only | Horizontal & Vertical |
| **Skill Required**| Basic Docker | Intermediate Linux/Docker | Advanced DevOps |

## Security Considerations
- **TLS Requirements:** Any official deployment must enforce HTTPS. Exposing raw HTTP ports is unacceptable.
- **Secrets Management:** Relying on default secrets is a critical risk. The architecture must enforce the injection of strong, generated secrets via a `.env` file that is never committed to version control.
- **Least Privilege:** Docker containers must be hardened to run as non-root users to limit the blast radius of potential container escapes.

## Monitoring Considerations
- The selected architecture must provide an easy path to scrape the existing Prometheus `/metrics` endpoints. 
- Log aggregation will initially rely on Docker's native logging drivers (e.g., `json-file` or `journald`), but the architecture should not prohibit the integration of a Promtail/Loki or FluentBit sidecar in the future.

## Backup Considerations
- The architecture must ensure the `db_data` volume is persistent and isolated.
- The existing `backup.sh` scripts are perfectly tailored for a Single Node or Small Team deployment where they can be executed via a simple host-level cron job.
- Moving to Kubernetes would invalidate these scripts, requiring a completely new backup strategy (e.g., Velero or cloud-native snapshots).

## Scaling Considerations
- ASTRA's current architecture (stateless frontend, stateless backend, stateful Postgres) scales vertically very well.
- For a v1 self-hosted product, horizontal scaling (requiring load balancing across multiple backend nodes and connection pooling for Postgres) introduces premature complexity. Vertical scaling of a Small Team VM is sufficient for early adoption.

## Conclusion of Assessment
The current architecture has strong foundations in observability and data recoverability, but lacks the infrastructure wrapping (Reverse Proxy, TLS, Secrets) needed for safe public internet exposure. Kubernetes introduces too much friction for a v1 self-hosted product. The **Small Team** model is the most logical target.
