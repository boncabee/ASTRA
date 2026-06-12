# ASTRA Repository Structure

Document ID: ASTRA-REPO-001
Version: 1.0
Status: Approved

Related Documents:

* PROJECT_PLAN.md
* ARCHITECTURE.md
* TECH_STACK.md
* DEVELOPMENT_GUIDELINES.md

---

# Purpose

Define the official repository layout.

AI Agents and contributors must follow this structure.

---

# Repository Layout

```text
astra/

├── docs/
│
│   ├── PROJECT_PLAN.md
│   ├── GOVERNANCE.md
│   ├── ROADMAP.md
│   ├── PRD.md
│   ├── TRACEABILITY_MATRIX.md
│   ├── ARCHITECTURE.md
│   ├── API_SPEC.md
│   ├── DATABASE_SCHEMA.md
│   ├── COMMON_EVENT_SCHEMA.md
│   ├── ATTACK_KNOWLEDGE_MODEL.md
│   ├── INVESTIGATION_PLAYBOOK.md
│   ├── PROMPT_ENGINEERING.md
│   ├── SECURITY.md
│   ├── THREAT_MODEL.md
│   ├── TESTING_STRATEGY.md
│   ├── AUDIT.md
│   ├── DEPLOYMENT.md
│   ├── DECISIONS.md
│   └── AI_AGENT_INSTRUCTIONS.md
│
├── frontend/
│
│   ├── src/
│   ├── public/
│   ├── tests/
│   └── package.json
│
├── backend/
│
│   ├── app/
│   │
│   ├── api/
│   ├── services/
│   ├── parsers/
│   ├── correlation/
│   ├── ai/
│   ├── models/
│   ├── repositories/
│   ├── security/
│   ├── schemas/
│   └── workers/
│
│   ├── tests/
│   └── requirements.txt
│
├── prompts/
│
├── datasets/
│
│   ├── golden/
│   ├── sample/
│   └── synthetic/
│
├── infrastructure/
│
│   ├── docker/
│   ├── cloudrun/
│   └── postgres/
│
├── scripts/
│
├── .github/
│
│   ├── workflows/
│   └── templates/
│
├── .env.example
├── docker-compose.yml
└── README.md
```

---

# Ownership

frontend/

Frontend Team

backend/

Backend Team

prompts/

AI Team

docs/

Architecture Team

datasets/

QA Team

---

# Repository Rules

Forbidden:

* random folders
* undocumented modules
* duplicated services

Every new directory requires documentation update.

```
```
