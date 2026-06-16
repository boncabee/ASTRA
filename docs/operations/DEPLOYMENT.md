# ASTRA Deployment Guide

Document ID: ASTRA-DEPLOY-001
Version: 2.0
Status: Approved

Related Documents:

* ARCHITECTURE.md
* SECURITY.md
* AUDIT.md
* DECISIONS.md

---

# Purpose

Define deployment and operational procedures.

This document answers:

```text id="nwtk9m"
How do we run ASTRA?
```

---

# Deployment Environments

## Local

Purpose:

Development

---

## Staging

Purpose:

Validation

---

## Production

Purpose:

Live operations

---

# Recommended Architecture

```text id="sjd4n9"
Internet
↓
NGINX Reverse Proxy (TLS Termination)
↓
├── Frontend (Next.js)
└── Backend (FastAPI)
      ↓
    PostgreSQL (Internal Network)
```

---

# Infrastructure Stack

ASTRA v1 is standardized on a **Small Team (Hardened Docker Compose)** deployment model.

**Proxy Layer:** NGINX with Certbot for automated Let's Encrypt TLS.
**Frontend:** Next.js (Node.js Alpine Container)
**Backend:** FastAPI (Python Slim Container)
**Database:** PostgreSQL 15 (Persistent Volume)
**Orchestrator:** Docker Compose

---

# Environment Variables

Production deployments require a `.env` file at the repository root. Do not commit this file.

Required:

```env id="tntfns"
DOMAIN=example.com
NEXT_PUBLIC_API_URL=https://example.com/api/v1
POSTGRES_USER=astra_prod
POSTGRES_PASSWORD=secure_password
POSTGRES_DB=astra
DATABASE_URL=postgresql+asyncpg://astra_prod:secure_password@db:5432/astra
JWT_SECRET_KEY=secure_32_char_string
GEMINI_API_KEY=
LOG_LEVEL=INFO
PRIVACY_MODE=true
```

---

# Startup Procedure

Step 1

Clone the repository and configure the environment variables:
```bash id="envsetup"
cp .env.example .env
chmod 600 .env
nano .env
```

---

Step 2

Start the production stack. The backend `entrypoint.sh` will automatically run `alembic upgrade head`.

```bash id="m0j66s"
docker compose -f docker-compose.prod.yml up -d --build
```

---

Step 3

Verify health endpoint.

```http id="b9kcd0"
GET /health
```

Expected:

```json id="7sfg3f"
{
  "status": "healthy"
}
```

---

# Monitoring

Metrics:

* Request Count
* Analysis Duration
* Error Rate
* Gemini Failures

Tools:

```text id="4o0nsn"
Prometheus

Grafana
```

---

# Backup Policy

Frequency:

```text id="7jntae"
Daily
```

Retention:

```text id="8gtg7x"
30 Days
```

---

# Rollback Procedure

1. Stop rollout
2. Restore previous image
3. Verify health checks
4. Review logs
5. Create incident report

---

# Deployment Acceptance

Release approved only if:

* Tests pass
* Security passes
* Audit score >= 90
* Golden dataset passes

```id="u2mjlwm"
```
