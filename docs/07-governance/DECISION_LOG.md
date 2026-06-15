# ASTRA Architecture Decision Records

Document ID: ASTRA-ADR-001
Version: 2.0
Status: Active

Related Documents:

* PROJECT_PLAN.md
* ARCHITECTURE.md
* GOVERNANCE.md

---

# Purpose

Record major architectural and engineering decisions.

All significant decisions must be documented.

---

# ADR-001

Title:

Use FastAPI

Status:

Accepted

---

## Context

Need:

* Type safety
* OpenAPI generation
* Async support

---

## Decision

Use FastAPI.

---

## Consequences

Pros:

* Strong typing
* Fast development

Cons:

* Async complexity

---

# ADR-002

Title:

Use Gemini API

Status:

Accepted

---

## Context

Need advanced reasoning.

---

## Decision

Use Gemini API.

---

## Consequences

Pros:

* Large context
* Strong reasoning

Cons:

* External dependency

---

# ADR-003

Title:

Use Common Event Schema (CES)

Status:

Accepted

---

## Context

Need parser independence.

---

## Decision

Normalize all events into CES.

---

## Consequences

Pros:

* Unified processing

Cons:

* Parser maintenance

---

# ADR-004

Title:

Evidence-Based Findings

Status:

Accepted

---

## Context

Hallucinations unacceptable.

---

## Decision

Every AI finding requires evidence references.

---

## Consequences

Pros:

* Explainability
* Auditability

Cons:

* More complex prompts

---

# ADR-005

Title:

JSON-Only AI Output

Status:

Accepted

---

## Context

Need deterministic integration.

---

## Decision

Structured output only.

---

## Consequences

Pros:

* Easier validation

Cons:

* Additional schema management

---

# ADR Lifecycle

Statuses:

```text id="m7v8lq"
Proposed

Accepted

Deprecated

Rejected
```

---

# ADR Change Process

Required when:

* Architecture changes
* AI workflow changes
* Database design changes
* Security design changes

---

# ADR Template

```markdown id="4cg9na"
# ADR-XXX

Title

Status

Context

Decision

Consequences
```

---

# Governance

No architectural decision may contradict:

* PROJECT_PLAN.md
* GOVERNANCE.md
* PRD.md

Higher-level documents take precedence.

```id="hjlwm0"
```
