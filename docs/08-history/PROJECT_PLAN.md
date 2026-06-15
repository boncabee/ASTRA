# ASTRA - Project Plan

Document ID: ASTRA-PLAN-001
Version: 2.0
Status: Approved
Owner: Project Team

---

# Purpose

This document is the highest-level project document for ASTRA.

It defines:

* Vision
* Mission
* Objectives
* Scope
* Constraints
* Success Criteria

All other project documents must align with this document.

---

# Document Hierarchy

The following hierarchy is mandatory:

```text
PROJECT_PLAN.md

    ↓

GOVERNANCE.md

    ↓

ROADMAP.md

    ↓

PRD.md

    ↓

TRACEABILITY_MATRIX.md

    ↓

REPOSITORY_STRUCTURE.md
TECH_STACK.md

    ↓

ARCHITECTURE.md

    ↓

COMMON_EVENT_SCHEMA.md

    ↓

ATTACK_KNOWLEDGE_MODEL.md

    ↓

INVESTIGATION_PLAYBOOK.md

    ↓

API_SPEC.md
DATABASE_SCHEMA.md
PROMPT_ENGINEERING.md

    ↓

TASKS.md

    ↓

Implementation

    ↓

TESTING_STRATEGY.md

    ↓

QUALITY_GATE.md

    ↓

AUDIT.md

    ↓

SELF_IMPROVEMENT_POLICY.md

    ↓

DEPLOYMENT.md

    ↓

DECISIONS.md
```

If conflicts occur:

Higher-level documents take precedence.

---

# Project Foundations

* Common Event Schema (CES)
* Attack Knowledge Model (AKM)
* Investigation Playbooks
* Quality Gates
* Continuous Self Improvement

---

# Vision

Enable security teams to transform large volumes of heterogeneous security logs into evidence-backed attack intelligence within minutes.

---

# Mission

Reduce investigation time by automating:

* Event normalization through Common Event Schema (CES)
* Event correlation
* Attack reconstruction
* Timeline generation
* MITRE ATT&CK mapping
* IOC extraction
* Incident reporting
* Continuous quality auditing
* Continuous self-improvement

using AI-assisted reasoning guided by attack knowledge and investigation playbooks.

---

# Product Definition

ASTRA is an Adaptive Security Threat Response & Automation Platform.

ASTRA is NOT:

* A SIEM replacement
* An AI chatbot
* An AI-first security platform
* A pure investigation platform

ASTRA IS:

* Adaptive Security Threat Response & Automation Platform

Additional Characteristics:

* Common Event Schema based
* Knowledge-driven investigation platform
* Playbook-driven reasoning platform
* Explainable AI investigation platform
* Self-auditing security analysis platform

---

# Core Principles

## Evidence First

Every conclusion must be traceable.

---

## Human Verifiable

Analysts must be able to validate every finding.

---

## AI Assisted

AI supports analysts.

AI does not replace analysts.

---

## Secure By Design

Security requirements are mandatory.

See:

* SECURITY.md
* THREAT_MODEL.md

---

## Open Source Friendly

No vendor lock-in.

No hardcoded credentials.

---

## Schema Driven

All event processing must use the Common Event Schema.

Reference:

* COMMON_EVENT_SCHEMA.md

---

## Knowledge Driven

All attack analysis must use the Attack Knowledge Model.

Reference:

* ATTACK_KNOWLEDGE_MODEL.md

---

## Playbook Driven

All investigations must follow approved investigation playbooks.

Reference:

* INVESTIGATION_PLAYBOOK.md

---

## Continuous Improvement

ASTRA continuously identifies weaknesses and creates improvement opportunities.

Reference:

* SELF_IMPROVEMENT_POLICY.md

---

# Strategic Objectives

## Objective 1

Reduce investigation time.

Target:

```text
2 hours
↓

5 minutes
```

---

## Objective 2

Standardize incident reporting.

---

## Objective 3

Increase investigation consistency.

---

## Objective 4

Provide explainable AI output.

---

## Objective 5

Establish a reusable investigation knowledge platform.

---

## Objective 6

Maintain investigation quality through quality gates.

---

## Objective 7

Continuously improve platform quality through audits.

---

# Scope

## In Scope

* Log ingestion
* Event normalization
* Common Event Schema conversion
* Correlation
* Attack knowledge modeling
* Investigation playbooks
* Timeline generation
* Narrative generation
* MITRE mapping
* IOC extraction
* Reporting
* Quality gates
* Continuous auditing
* Self-improvement recommendations

---

## Out of Scope

* Real-time response actions
* Endpoint isolation
* Automated remediation
* Full SIEM functionality

---

# Success Metrics

| Metric | Target |
|----------|----------|
| Timeline Generation | < 60 sec |
| MITRE Accuracy | >= 80% |
| Test Coverage | >= 70% |
| Hardcoded Secrets | 0 |
| Traceable Findings | 100% |
| Audit Score | >= 90 |
| CES Validation Success | 100% |
| Playbook Compliance | 100% |
| Knowledge Mapping Accuracy | >= 80% |
| Prompt Validation Success | >= 95% |

---

# Required Documents

Strategic:

* ROADMAP.md
* GOVERNANCE.md

Business:

* PRD.md
* TRACEABILITY_MATRIX.md

Foundation:

* REPOSITORY_STRUCTURE.md
* TECH_STACK.md

Technical:

* ARCHITECTURE.md
* COMMON_EVENT_SCHEMA.md
* ATTACK_KNOWLEDGE_MODEL.md
* INVESTIGATION_PLAYBOOK.md
* API_SPEC.md
* DATABASE_SCHEMA.md
* PROMPT_ENGINEERING.md

Execution:

* TASKS.md
* CONTRIBUTING.md
* DEVELOPMENT_GUIDELINES.md
* AGENT_TASK_EXECUTION_FRAMEWORK.md

Verification:

* TESTING_STRATEGY.md
* QUALITY_GATE.md
* AUDIT.md

Security:

* SECURITY.md
* THREAT_MODEL.md

Operations:

* DEPLOYMENT.md
* DECISIONS.md

Governance:

* AI_AGENT_INSTRUCTIONS.md
* SELF_IMPROVEMENT_POLICY.md

---

# Acceptance Criteria

This project is considered successful when:

* MVP requirements are delivered
* Common Event Schema fully implemented
* Attack Knowledge Model implemented
* Investigation Playbooks implemented
* Golden Dataset passes
* Security requirements pass
* Audit score >= 90
* Quality Gates pass
* Deployment process validated
* Documentation remains synchronized
* Self-improvement workflow operational