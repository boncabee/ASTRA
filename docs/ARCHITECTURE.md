# ASTRA System Architecture

Document ID: ASTRA-ARCH-001
Version: 2.0
Status: Approved

Related Documents:

* PROJECT_PLAN.md
* PRD.md
* GOVERNANCE.md
* API_SPEC.md
* DATABASE_SCHEMA.md
* PROMPT_ENGINEERING.md

---

# Purpose

Define the technical architecture of ASTRA.

This document answers:

```text
How does ASTRA work?
```

---

# Architectural Principles

## AP-001 Modular Architecture

All components must be independently testable.

---

## AP-002 AI-Assisted Architecture

AI is used for:

* Timeline generation
* Narrative generation
* MITRE mapping
* IOC extraction

AI must not:

* Execute actions
* Modify source data
* Make security decisions

---

## AP-003 Deterministic Pipeline

Pipeline stages before Gemini must be deterministic.

```text
Upload
↓
Parser
↓
CES
↓
Correlation
↓
AKM
↓
Playbooks
↓
Gemini
↓
Validation
↓
Database
```

---

## AP-004 Traceability

Every output must reference evidence.

Reference:

* PROMPT_ENGINEERING.md

---

# High-Level Architecture

```text
User

↓

Frontend

↓

API

↓

Upload Service

↓

Parser Layer

↓

CES Layer

↓

Correlation Engine

↓

AKM Layer

↓

Investigation Layer

↓

AI Reasoner

↓

Validation Layer

↓

Persistence Layer

↓

Frontend
```

---

# Components

## Frontend

Technology:

```text
Next.js
TypeScript
Tailwind
```

Responsibilities:

* Upload logs
* View incidents
* View timelines
* Download reports

---

## API Layer

Technology:

```text
FastAPI
```

Responsibilities:

* Upload handling
* Job creation
* Status retrieval
* Result retrieval

Reference:

* API_SPEC.md

---

## Upload Service

Responsibilities:

* File validation
* File hashing
* Job creation

Reference:

* SECURITY.md

---

## Parser Layer

Responsibilities:

Convert source logs into CES.

Supported MVP:

* Windows Logs
* Firewall Logs

Output:

CES Event

---

## CES Layer

Purpose:

Create common event representation.

Reference:

* DATABASE_SCHEMA.md

---

## AKM Layer

Purpose:

Represent attacker behaviors, perform MITRE mapping, confidence scoring, and attack chain reconstruction.

Reference:

* ATTACK_KNOWLEDGE_MODEL.md

---

## Investigation Layer

Purpose:

Standardize investigations using playbooks to guide reasoning and improve explainability.

Reference:

* INVESTIGATION_PLAYBOOK.md

---

## Validation Layer

Purpose:

Validate outputs and evidence before persistence.

Reference:

* QUALITY_GATE.md

---

## Correlation Engine

Purpose:

Group related events into incidents.

Correlation Factors:

* User
* Host
* IP
* Time Window

Output:

Incident Candidate

---

## AI Reasoner

Technology:

```text
Gemini API
```

Responsibilities:

* Timeline
* Narrative
* MITRE
* IOC
* Confidence

Reference:

* PROMPT_ENGINEERING.md

---

## Persistence Layer

Technology:

```text
PostgreSQL
```

Reference:

* DATABASE_SCHEMA.md

---

# Data Flow

Step 1

User uploads file.

---

Step 2

Upload Service validates file.

---

Step 3

Parser converts logs into CES.

---

Step 4

Correlation Engine creates incidents.

---

Step 5

AKM Layer enriches incidents with attack knowledge.

---

Step 6

Investigation Layer applies playbooks to the incident.

---

Step 7

AI Reasoner analyzes incidents.

---

Step 8

Validation Layer validates the analysis.

---

Step 9

Results stored.

---

Step 10

Results displayed.

---

# Cross-Document Dependencies

PRD

Defines:

```text
What to build
```

---

Architecture

Defines:

```text
How it works
```

---

API

Defines:

```text
How components communicate
```

---

Database

Defines:

```text
How data is stored
```

---

Prompt Engineering

Defines:

```text
How AI reasons
```

---

# Architecture Acceptance Criteria

Architecture is valid if:

* All PRD requirements supported
* All components traceable
* Security requirements respected
* Testability preserved

```
```
