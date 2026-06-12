# ASTRA Governance Model

Document ID: ASTRA-GOV-001
Version: 2.0
Status: Approved

---

# Purpose

Ensure consistency between:

* Documentation
* Architecture
* Code
* Tests
* Deployment

This document defines decision authority and conflict resolution.

---

# Documentation Authority Chain

Level 1

```text
PROJECT_PLAN.md
```

Defines:

```text
Why ASTRA exists
```

---

Level 2

```text
ROADMAP.md
PRD.md
```

Define:

```text
What ASTRA must do
```

---

Level 3

```text
ARCHITECTURE.md
```

Defines:

```text
How ASTRA should work
```

---

Level 4

```text
API_SPEC.md
DATABASE_SCHEMA.md
PROMPT_ENGINEERING.md
```

Define:

```text
Technical implementation contracts
```

---

Level 5

```text
TASKS.md
```

Defines:

```text
Implementation work
```

---

Level 6

```text
Implementation
```

Defines:

```text
Actual source code
```

---

Level 7

```text
TESTING_STRATEGY.md
AUDIT.md
```

Verify:

```text
Whether implementation is correct
```

---

Level 8

```text
DEPLOYMENT.md
```

Defines:

```text
How ASTRA runs in production
```

---

# Conflict Resolution Rules

Rule 1

Code must not contradict TASKS.md.

---

Rule 2

TASKS.md must not contradict PRD.md.

---

Rule 3

PRD.md must not contradict PROJECT_PLAN.md.

---

Rule 4

Architecture must not contradict PRD.md.

---

Rule 5

Tests must validate requirements from PRD.md.

---

Rule 6

Audit findings override assumptions.

---

# Mandatory Traceability

Every requirement must be traceable.

Required flow:

```text
PROJECT_PLAN

↓

PRD

↓

ARCHITECTURE

↓

API / DATABASE / PROMPTS

↓

TASKS

↓

CODE

↓

TESTS

↓

AUDIT
```

---

# Documentation Update Rules

If API changes:

Update:

* API_SPEC.md
* TESTING_STRATEGY.md
* TRACEABILITY_MATRIX.md

---

If Database changes:

Update:

* DATABASE_SCHEMA.md
* ARCHITECTURE.md
* TRACEABILITY_MATRIX.md

---

If Prompt changes:

Update:

* PROMPT_ENGINEERING.md
* AUDIT.md
* TESTING_STRATEGY.md

---

# Governance Review Gates

Before Merge:

* CI passes
* Tests pass
* Security scan passes
* Documentation updated

Before Release:

* Audit score >= 90
* Security review complete
* Golden dataset passes

---

# AI Agent Rules

Before implementing any task:

Read in order:

1. PROJECT_PLAN.md
2. GOVERNANCE.md
3. PRD.md
4. ARCHITECTURE.md
5. TASKS.md

AI agents must not skip this sequence.

---

# Definition of Alignment

ASTRA is considered aligned when:

* Documentation agrees
* Architecture agrees
* Implementation agrees
* Tests agree
* Audit confirms agreement

Alignment Score Target:

```text
>= 95%
```
