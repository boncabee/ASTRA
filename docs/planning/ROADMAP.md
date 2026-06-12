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

# Phase 3 — Threat Intelligence

Target: v0.3

Features:

* IOC reputation
* Threat feed integration
* Campaign correlation

Dependencies:

* DATABASE_SCHEMA.md
* API_SPEC.md

---

# Phase 4 — SOC Copilot

Target: v0.4

Features:

Natural language investigation.

Examples:

```text
show suspicious powershell activity

show credential dumping activity

show lateral movement incidents
```

Dependencies:

* PROMPT_ENGINEERING.md

---

# Phase 5 — Real-Time Analysis

Target: v0.5

Features:

* Kafka
* Event streaming
* Real-time correlation

Dependencies:

* ARCHITECTURE.md

---

# Phase 6 — Enterprise

Target: v1.0

Features:

* Authentication
* RBAC
* Multi-tenancy
* Audit Logs
* API Keys

Dependencies:

* SECURITY.md
* THREAT_MODEL.md

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
