# ASTRA AI Agent Operating Manual

Document ID: ASTRA-AIAGENT-001
Version: 2.0
Status: Approved

Related Documents:

* PROJECT_PLAN.md
* GOVERNANCE.md
* PRD.md
* ARCHITECTURE.md
* API_SPEC.md
* DATABASE_SCHEMA.md
* PROMPT_ENGINEERING.md
* TASKS.md
* TESTING_STRATEGY.md
* AUDIT.md
* SECURITY.md
* THREAT_MODEL.md
* DEPLOYMENT.md
* DECISIONS.md
* TRACEABILITY_MATRIX.md

---

# Purpose

This document defines how AI Agents must behave while developing ASTRA.

This document is mandatory for:

* Google Antigravity IDE
* Gemini CLI
* Claude Code
* Cursor Agent
* OpenAI Codex
* Any autonomous coding agent

This document acts as the operational layer above source code generation.

---

# Core Mission

The AI Agent's mission is:

```text id="mvjvw4"
Build ASTRA

Safely

Incrementally

Traceably

Repeatably
```

The AI Agent must prioritize:

```text id="rwjs2q"
Correctness

↓

Security

↓

Traceability

↓

Maintainability

↓

Performance
```

---

# Mandatory Reading Order

Before implementing any task, the AI Agent MUST read documents in the following order:

```text id="iygv8v"
1. PROJECT_PLAN.md

2. GOVERNANCE.md

3. ROADMAP.md

4. PRD.md

5. TRACEABILITY_MATRIX.md

6. REPOSITORY_STRUCTURE.md

7. TECH_STACK.md

8. ARCHITECTURE.md

9. COMMON_EVENT_SCHEMA.md

10. ATTACK_KNOWLEDGE_MODEL.md

11. INVESTIGATION_PLAYBOOK.md

12. API_SPEC.md

13. DATABASE_SCHEMA.md

14. PROMPT_ENGINEERING.md

15. SECURITY.md

16. THREAT_MODEL.md

17. TASKS.md

18. DEVELOPMENT_GUIDELINES.md

19. TESTING_STRATEGY.md

20. QUALITY_GATE.md

21. AUDIT.md

22. SELF_IMPROVEMENT_POLICY.md

23. DEPLOYMENT.md

24. DECISIONS.md
```

Skipping documents is forbidden.

---

# Source of Truth Hierarchy

When conflicts exist:

```text id="q29ehz"
PROJECT_PLAN

>

GOVERNANCE

>

ROADMAP

>

PRD

>

ARCHITECTURE

>

API_SPEC
DATABASE_SCHEMA
PROMPT_ENGINEERING

>

TASKS

>

CODE
```

The AI Agent must obey the higher-level document.

---

# Development Workflow

For every task:

```text id="msbxt4"
Read Requirement

↓

Read Architecture

↓

Read API Contract

↓

Read Database Contract

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

Do not skip steps.

---

# Task Execution Rules

Before starting:

Verify:

* Requirement exists
* Task exists
* Traceability exists

If missing:

STOP.

Create finding in AUDIT report.

---

# Incremental Development

The AI Agent must work in small increments.

Maximum scope per implementation cycle:

```text id="3dc5j8"
1 Task

OR

1 Feature
```

Forbidden:

```text id="s0ylsi"
Implement entire system at once.
```

---

# Code Generation Rules

Reference:

DEVELOPMENT_GUIDELINES.md

Requirements:

* Strong typing
* Small functions
* Modular design
* Dependency injection
* Testability

---

# Security Rules

Reference:

SECURITY.md

Mandatory:

* Validate all inputs
* Validate all outputs
* No hardcoded secrets
* No unsafe deserialization
* No hidden backdoors

Forbidden:

```python id="cqj3fa"
API_KEY = "secret"
```

---

# AI Integration Rules

Reference:

PROMPT_ENGINEERING.md

The AI Agent must:

* Treat Gemini output as untrusted
* Validate JSON
* Validate schema
* Validate evidence references

Never trust model output directly.

---

# Database Rules

Reference:

DATABASE_SCHEMA.md

The AI Agent may not:

* Create undocumented tables
* Create undocumented fields
* Modify schema without updating documentation

---

# API Rules

Reference:

API_SPEC.md

The AI Agent may not:

* Create undocumented endpoints
* Change response contracts
* Break compatibility

without updating documentation.

---

# Testing Rules

Reference:

TESTING_STRATEGY.md

Every implementation must include:

```text id="9oc7eg"
Unit Test

Integration Test
```

When applicable:

```text id="jlwm4f"
Golden Dataset Test
```

---

# Documentation Synchronization Rules

When code changes:

The AI Agent must determine whether updates are required.

---

## Update Required

If API changes:

Update:

```text id="fznn0s"
API_SPEC.md

TRACEABILITY_MATRIX.md

TESTING_STRATEGY.md
```

---

If Database changes:

Update:

```text id="3o7vga"
DATABASE_SCHEMA.md

ARCHITECTURE.md

TRACEABILITY_MATRIX.md
```

---

If Prompt changes:

Update:

```text id="xmmxvr"
PROMPT_ENGINEERING.md

AUDIT.md

TESTING_STRATEGY.md
```

---

If Requirements change:

Update:

```text id="kt3x8m"
PRD.md

TASKS.md

TRACEABILITY_MATRIX.md
```

---

# Traceability Enforcement

Every implementation must map:

```text id="lvg85h"
Requirement

↓

Task

↓

Code

↓

Test
```

Missing links are considered defects.

---

# Audit Integration

Reference:

AUDIT.md

After implementation:

Run audit checks.

Validate:

* Requirement Alignment
* Architecture Alignment
* Security Compliance
* Documentation Consistency

---

# Technical Debt Prevention

The AI Agent must continuously detect:

* Duplicate code
* Dead code
* Large files
* Large functions
* Circular dependencies

When found:

Create audit findings.

---

# Self-Review Protocol

Before creating a pull request:

The AI Agent must review:

---

## Requirement Review

Questions:

```text id="0e66kg"
Was the requirement implemented?
```

---

## Architecture Review

Questions:

```text id="0nmbhr"
Does implementation match architecture?
```

---

## Security Review

Questions:

```text id="4t34ow"
Did implementation introduce risk?
```

---

## Testing Review

Questions:

```text id="o0b6ru"
Are tests sufficient?
```

---

## Documentation Review

Questions:

```text id="t8v7kr"
Which documents require updates?
```

---

# Pull Request Checklist

Before merge:

```markdown id="ahwnmv"
- Requirement linked

- Task linked

- Tests added

- Documentation updated

- Security reviewed

- Audit passed
```

---

# Autonomous Audit Mode

The AI Agent should periodically perform:

```text id="qgzyo6"
Requirement Audit

Architecture Audit

Security Audit

Prompt Audit

Documentation Audit
```

Reference:

AUDIT.md

---

# Hallucination Prevention

The AI Agent must never assume:

* APIs exist
* Tables exist
* Requirements exist
* Tasks exist

Verification required.

---

# Error Handling Policy

If documentation conflicts:

```text id="v2uk5u"
Stop

↓

Report Conflict

↓

Request Resolution
```

Do not guess.

---

# Release Readiness Checklist

Before deployment:

Verify:

```text id="jlsnvc"
All Tests Pass

Audit Score >= 90

No Critical Findings

No Open Security Findings

Documentation Synced
```

---

# Definition of Success

The AI Agent succeeds when:

* Requirements are implemented
* Architecture remains aligned
* Security controls remain intact
* Documentation remains synchronized
* Audit score remains >= 90

---

# Final Rule

If uncertain:

```text id="eb6h52"
Do Not Assume

Read Documentation

Follow Governance

Preserve Traceability
```

This rule overrides all implementation shortcuts.
