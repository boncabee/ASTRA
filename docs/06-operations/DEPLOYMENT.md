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

Load Balancer

↓

Frontend

↓

API

↓

Worker

↓

PostgreSQL
```

---

# Infrastructure Stack

Frontend:

```text id="59l6ci"
Vercel
```

or

```text id="91r43l"
Cloud Run
```

---

Backend:

```text id="sw18hm"
Cloud Run
```

---

Database:

```text id="m1w61j"
PostgreSQL
```

---

# Environment Variables

Required:

```env id="tntfns"
GEMINI_API_KEY=

DATABASE_URL=

PRIVACY_MODE=

LOG_LEVEL=
```

---

# Startup Procedure

Step 1

Run migrations.

```bash id="xwy52r"
alembic upgrade head
```

---

Step 2

Start services.

```bash id="m0j66s"
docker compose up
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
