# ASTRA Product Roadmap

Document ID: ASTRA-RM-001
Version: 2.0
Status: Active

Related Documents:

* PROJECT_PLAN.md
* PRD.md
* TASKS.md

---

# Purpose

Define long-term product evolution.

This document answers:

```text
What will ASTRA become?
```

---

# Phase 1 — MVP

Target: v0.1

Objectives:

* Upload logs
* Normalize logs
* Correlate events
* Generate timelines
* Generate narratives
* Generate MITRE mappings
* Generate IOC extraction

Deliverables:

* FastAPI Backend
* Next.js Frontend
* PostgreSQL
* Gemini Integration

Dependencies:

* PRD.md
* ARCHITECTURE.md
* TASKS.md

Success Criteria:

* Golden dataset passes
* End-to-end workflow operational

---

# Phase 2 — Investigation Enhancement

Target: v0.2

Features:

* VPN parser
* Syslog parser
* EDR parser
* Timeline filtering
* IOC explorer
* Entity graph

Success Criteria:

* Support 5+ log sources

---

# Phase 3 — Sprint 3 (Realignment)

Target: v0.3

Features:

* RBAC
* Correlation Engine
* Observation Engine
* Policy Engine

Dependencies:

* DATABASE_SCHEMA.md
* API_SPEC.md

---

# Phase 4 — Sprint 4

Target: v0.4

Features:

* Case Management
* Automation Engine
* AI Gateway

---

# Phase 5 — Sprint 5

Target: v0.5

Features:

* SOAR Integrations
* Playbook Engine
* Recommendation Engine

---

# Roadmap Governance

New roadmap items must:

1. Align with PROJECT_PLAN.md
2. Be represented in PRD.md
3. Be mapped into TASKS.md
4. Be testable via TESTING_STRATEGY.md

Otherwise roadmap items are invalid.

```
```
