# ASTRA Technology Stack

Document ID: ASTRA-STACK-001
Version: 1.0
Status: Approved

Related Documents:

* ARCHITECTURE.md
* DEPLOYMENT.md
* DEVELOPMENT_GUIDELINES.md

---

# Purpose

Define official technologies allowed in ASTRA.

---

# Frontend

Framework:

```text
Next.js 15
```

Language:

```text
TypeScript
```

UI:

```text
TailwindCSS
```

State Management:

```text
TanStack Query
```

Validation:

```text
Zod
```

---

# Backend

Framework:

```text
FastAPI
```

Language:

```text
Python 3.12+
```

Validation:

```text
Pydantic v2
```

ORM:

```text
SQLAlchemy 2
```

Migration:

```text
Alembic
```

---

# AI Layer

Provider:

```text
Gemini API
```

Model Strategy:

```text
Primary:
Gemini 2.5 Pro

Fallback:
Gemini 2.5 Flash
```

---

# Database

Primary:

```text
PostgreSQL
```

Future:

```text
pgvector
```

---

# Background Jobs

Framework:

```text
Celery
```

Broker:

```text
Redis
```

---

# Testing

Unit:

```text
pytest
```

Frontend:

```text
vitest
```

E2E:

```text
playwright
```

---

# Security

Tools:

```text
gitleaks

pip-audit

npm audit

bandit
```

---

# Deployment

Container:

```text
Docker
```

Hosting:

```text
Cloud Run
```

---

# Technology Governance

Replacing technologies requires:

* ADR update
* Architecture review
* Approval

```
```
