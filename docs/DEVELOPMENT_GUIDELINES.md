# ASTRA Development Guidelines

Document ID: ASTRA-DEV-001
Version: 2.0
Status: Approved

Related Documents:

* GOVERNANCE.md
* SECURITY.md
* TESTING_STRATEGY.md

---

# Purpose

Define coding standards for developers and AI agents.

---

# Mandatory System Principles

* All parsers output CES.
* All findings reference AKM.
* All investigations use Playbooks.
* All AI outputs contain evidence references.

---

# Development Philosophy

Priority Order:

```text id="s0w4in"
Correctness

↓

Security

↓

Maintainability

↓

Performance

↓

Convenience
```

---

# Code Standards

---

## Function Length

Target:

```text id="1s4j6v"
< 50 lines
```

Maximum:

```text id="8l8grr"
100 lines
```

---

## File Length

Target:

```text id="7u4vzc"
< 500 lines
```

Maximum:

```text id="5hvv7e"
1000 lines
```

---

## Nesting

Maximum:

```text id="sfb9e6"
3 levels
```

---

## Comments

Required for:

* Complex logic
* Correlation logic
* AI orchestration

---

# Python Standards

Version:

```text id="wtzv0w"
Python 3.12+
```

---

## Type Hints

Mandatory.

Example:

```python id="6cx7j5"
def build_timeline(events: list[Event]) -> Timeline:
    ...
```

---

## Data Models

Mandatory:

```text id="a7m9sp"
Pydantic
```

---

## Database

Mandatory:

```text id="h4s9z5"
SQLAlchemy
Alembic
```

---

# API Standards

Reference:

API_SPEC.md

Requirements:

* JSON only
* Versioned endpoints
* Consistent error handling

---

# AI Standards

Reference:

PROMPT_ENGINEERING.md

Rules:

* Never trust AI output directly
* Always validate JSON
* Always validate schema

---

# Logging Standards

Required Fields:

```json id="3vl10y"
{
  "request_id": "",
  "job_id": "",
  "message": ""
}
```

---

# Security Standards

Reference:

SECURITY.md

Requirements:

* No hardcoded secrets
* Input validation
* Output validation

---

# Test Standards

Reference:

TESTING_STRATEGY.md

Required:

* Unit tests
* Integration tests
* Golden dataset tests

---

# Documentation Standards

Any code change affecting behavior must update:

* PRD
* Architecture
* API
* Database
* Prompts

when applicable.

---

# AI Agent Rules

Before coding:

Read:

```text id="if9zjm"
PROJECT_PLAN

↓

GOVERNANCE

↓

PRD

↓

ARCHITECTURE

↓

TASKS
```

---

# Forbidden Practices

Do not:

* Hardcode credentials
* Skip validation
* Bypass tests
* Bypass code review
* Ignore audit findings

---

# Definition of Quality

Code is considered production-ready when:

* Readable
* Tested
* Secure
* Traceable
* Documented

```
```
