# PHASE 8.2: SELF-HOSTED READINESS ASSESSMENT

**Date:** 2026-06-16  
**Status:** COMPLETE (WITH CONDITIONS)  
**GitHub Actions Run ID:** 27633570893  
**Commit SHA:** 034249842c61d8d7eb8c9527f177830279bb5b88

## Executive Summary

The Self-Hosted Readiness Assessment evaluates ASTRA's capability to be deployed reliably and securely by end-users or small teams within their own infrastructure. The assessment examines deployment simplicity, configuration safety, and operational documentation.

## Readiness by Deployment Tier

### 1. Single-Node Deployment (Developer / Sandbox)
**Status: READY**

- **Findings:** ASTRA can be spun up quickly using the provided `docker-compose.yml` and `docker-compose.dev.yml` files. The inclusion of the PostgreSQL database within the compose network allows for a seamless "one-click" startup.
- **Gaps:** The user still has to manually run `alembic upgrade head` after the containers start, which creates friction.
- **Recommendation:** Add an `entrypoint.sh` script to the backend container to automate database migrations before starting `uvicorn`.

### 2. Small Team Deployment (Internal Production)
**Status: NOT READY**

- **Findings:** Deploying for a small team requires secure configuration management, which ASTRA currently lacks out-of-the-box. The `docker-compose.yml` hardcodes database credentials (`postgres:postgres`) and lacks a secure `.env` mapping strategy for production.
- **Gaps:** 
  - The application allows startup with an insecure default `JWT_SECRET_KEY`.
  - Database queries are logged to stdout (`echo=True`), leaking sensitive internal data to team logs.
  - No automated database backup solutions or Cron jobs are provided in the compose stack.
- **Recommendation:** Provide a dedicated `docker-compose.prod.yml` that forces variables to be read from a locked-down `.env` file, removes default credentials, and disables debug logging.

### 3. Production Pilot Deployment (Enterprise Beta)
**Status: NOT READY**

- **Findings:** Enterprise pilots demand high observability, strict security, and disaster recovery procedures. 
- **Gaps:**
  - **Security:** Containers run as `root`. Authentication lacks rate-limiting. Token management relies entirely on local storage rather than `httpOnly` cookies.
  - **Observability:** Missing APM tracing and correlation IDs in logs prevent effective incident response.
  - **Operations:** The `DEPLOYMENT.md` specifies a backup policy but provides no scripts, runbooks, or tested restore procedures for PostgreSQL.
- **Recommendation:** Implement non-root Docker users, introduce structured logging with correlation IDs, provide robust disaster recovery runbooks, and harden the authentication layer.

## Self-Hosted Readiness Findings Summary

While ASTRA is structurally sound, it is too immature in its configuration management to be safely handed to end-users for production use. The "out-of-the-box" experience prioritizes developer convenience over secure defaults.

## Final Determination

**GO WITH CONDITIONS**

ASTRA is approved for local sandbox and development environments. It is a **NO-GO** for Small Team or Production Pilot deployments until the production-grade Docker compose configurations, secure default enforcements, and automated migration routines are implemented.
