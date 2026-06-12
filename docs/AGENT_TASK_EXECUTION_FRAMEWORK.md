# ASTRA Agent Task Execution Framework

Document ID: ASTRA-AGENT-EXEC-001
Version: 1.0
Status: Approved

Related Documents:

* AI_AGENT_INSTRUCTIONS.md
* TASKS.md
* GOVERNANCE.md
* AUDIT.md

---

# Purpose

Define how AI Agents execute work.

---

# Execution Cycle

```text
Read

↓

Plan

↓

Implement

↓

Test

↓

Audit

↓

Document

↓

Review
```

---

# Step 1

Requirement Discovery

---

Agent must identify:

* Requirement ID
* Task ID
* Dependencies

Example:

```text
FR-002

↓

TASK-201

↓

TASK-202
```

---

# Step 2

Implementation Planning

Required Outputs:

* files affected
* tests required
* documentation updates

---

# Step 3

Implementation

Rules:

* smallest change possible
* no speculative features
* maintain traceability

---

# Step 4

Testing

Mandatory:

```text
Unit Test

Integration Test
```

Optional:

```text
Golden Dataset
```

---

# Step 5

Audit

Run:

* Requirement Audit
* Security Audit
* Documentation Audit

Reference:

AUDIT.md

---

# Step 6

Documentation

Update affected documents.

Examples:

API changes:

```text
API_SPEC

TRACEABILITY_MATRIX

TESTING_STRATEGY
```

---

# Step 7

Review

Agent must self-review:

* correctness
* security
* maintainability

---

# Work Unit Size

Maximum:

```text
1 task
```

per execution cycle.

---

# Forbidden Behaviors

Do not:

* skip tests
* skip documentation
* modify unrelated code
* create undocumented features

---

# Success Criteria

Task considered complete only if:

* code passes
* tests pass
* audit passes
* docs synchronized

```
```
