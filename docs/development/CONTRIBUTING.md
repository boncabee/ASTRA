# Contributing to ASTRA

Document ID: ASTRA-CONTRIB-001
Version: 2.0
Status: Active

Related Documents:

* GOVERNANCE.md
* DEVELOPMENT_GUIDELINES.md
* SECURITY.md

---

# Purpose

Define contribution rules.

---

# Before Contributing

Read in order:

1. PROJECT_PLAN.md
2. GOVERNANCE.md
3. PRD.md
4. ARCHITECTURE.md
5. TASKS.md

---

# Branch Naming

Format:

```text
feature/*
bugfix/*
hotfix/*
docs/*
```

Examples:

```text id="zln36s"
feature/windows-parser

feature/gemini-reasoner

bugfix/timeline-order
```

---

# Commit Convention

Format:

```text
type(scope): description
```

Examples:

```text id="f9h7ns"
feat(parser): add windows parser

fix(api): handle invalid upload

docs(prd): update requirement
```

---

# Pull Request Requirements

Required:

* Linked task
* Linked requirement
* Tests
* Documentation updates
* Meet the formal Definition of Done
* GitHub Actions Pass (Local validation alone is insufficient)

---

# Pull Request Template

```markdown id="xv4ruw"
## Summary

## Related Task

## Related Requirement

## Test Evidence

## Documentation Updated
```

---

# Merge Requirements

Must pass:

* GitHub Actions (Source of Truth)
* Tests
* Secret scan
* Code review

---

# Security Reporting

Security issues must not be publicly disclosed.

Reference:

SECURITY.md

---

# Documentation Updates

Mandatory when changing:

* API
* Database
* Prompts
* Architecture

Failure to update documentation blocks merge.

---

# Contributor Responsibilities

Contributors must ensure:

* Code quality
* Security compliance
* Traceability preservation
* Documentation consistency

```
```
