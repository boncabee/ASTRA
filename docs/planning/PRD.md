# ASTRA Product Requirements Document

Document ID: ASTRA-PRD-001
Version: 2.0
Status: Approved

Related Documents:

* PROJECT_PLAN.md
* ROADMAP.md
* GOVERNANCE.md
* TRACEABILITY_MATRIX.md

---

# Purpose

Define all business and functional requirements for ASTRA.

This document answers:

```text
What must ASTRA do?
```

---

# Product Summary

ASTRA is an Adaptive Security Threat Response & Automation Platform that transforms security telemetry into explainable, auditable, policy-driven security decisions and automated response actions.

The system helps incident responders and security teams:

* Transform raw telemetry into actionable observations
* Automate decision-making via a configurable Policy Engine
* Execute automated response actions
* Leverage AI as an enhancement, not a core dependency

---

# User Personas

## Incident Responder

Goals:

* Determine root cause
* Understand attack chain
* Automate responses based on policy

Pain Points:

* Incomplete visibility
* Evidence scattered across systems
* Slow response actions

---

## SOC Analyst

Goals:

* Investigate observations
* Build attack timelines
* Identify attacker behavior

Pain Points:

* Too many logs
* Slow investigations
* Manual reporting

---

## Security Engineer

Goals:

* Improve security posture
* Analyze attack patterns
* Manage detection policies

Pain Points:

* Repetitive analysis work
* Difficult policy management

---

## Administrator

Goals:

* Manage platform health
* Oversee access and RBAC
* Ensure AI availability and reliability

Pain Points:

* Complex user management
* Dependency on single AI providers

---

# Functional Requirements

---

## FR-001 Log Upload

Description:

Allow users to upload security logs.

Priority:

Critical

Acceptance Criteria:

* Supports JSON
* Supports JSONL
* Supports CSV
* Upload validation enforced

Traceability:

* TASK-001
* TASK-002

---

## FR-002 Log Normalization

Description:

Convert uploaded logs into CES.

Priority:

Critical

Acceptance Criteria:

* Every parser outputs CES
* Validation enforced

Traceability:

* TASK-101
* TASK-201
* TASK-203

---

## FR-003 Event Correlation

Description:

Group related events into incidents.

Priority:

Critical

Acceptance Criteria:

* Correlation based on:

  * User
  * Host
  * IP
  * Time Window

Traceability:

* TASK-301
* TASK-302

---

## FR-004 Timeline Generation

Description:

Generate attack timeline.

Priority:

Critical

Acceptance Criteria:

* Chronological ordering
* Evidence references included

Traceability:

* TASK-501

---

## FR-005 Narrative Generation

Description:

Generate incident narrative.

Priority:

Critical

Acceptance Criteria:

* Human readable
* Evidence backed

Traceability:

* TASK-502

---

## FR-006 MITRE ATT&CK Mapping

Description:

Map attacker behavior to ATT&CK techniques.

Priority:

Critical

Acceptance Criteria:

* Technique ID
* Technique Name
* Confidence Score

Traceability:

* TASK-503

---

## FR-007 IOC Extraction

Description:

Extract indicators of compromise.

Priority:

Critical

Acceptance Criteria:

Supported:

* IP
* Domain
* URL
* Hash
* Hostname
* Username

Traceability:

* TASK-504

---

## FR-008 Confidence Scoring

Description:

Assign confidence score.

Priority:

High

Acceptance Criteria:

Range:

```text
0.00 - 1.00
```

Traceability:

* TASK-505

---

## FR-009 Result Storage

Description:

Store generated analysis.

Priority:

Critical

Acceptance Criteria:

* Incident persistence
* Timeline persistence
* IOC persistence

Traceability:

* TASK-801
* TASK-802
* TASK-803

---

## FR-010 Result Visualization

Description:

Display analysis results.

Priority:

Critical

Acceptance Criteria:

* Timeline visible
* Narrative visible
* IOC visible
* MITRE visible

Traceability:

* TASK-701
* TASK-703

---

## FR-011 CES Normalization

All events must be normalized into CES.

---

## FR-012 Knowledge-Based Analysis

ASTRA shall use Attack Knowledge Model.

---

## FR-013 Playbook-Based Investigation

ASTRA shall follow investigation playbooks.

---

## FR-014 Continuous Self-Improvement

ASTRA shall create findings from audits.

---

## FR-015 Quality Gate Enforcement

ASTRA shall block releases failing quality gates.

---


## FR-016 Observation Generation
Description: Generate actionable observations from correlated events.
Priority: Critical

## FR-017 Policy Engine Evaluation
Description: Evaluate observations against defined security policies.
Priority: Critical

## FR-018 Automated Response Actions
Description: Execute automated response actions based on policy decisions.
Priority: High

## FR-019 AI Provider Abstraction
Description: Abstract AI capabilities to support multiple providers (OpenAI, Gemini, Claude, Ollama) and ensure platform functions when AI is unavailable.
Priority: Critical

# Non-Functional Requirements

---

## NFR-001 Performance

Requirement:

10,000 events processed in under 60 seconds.

---

## NFR-002 Reliability

Requirement:

99% successful analysis completion.

---

## NFR-003 Security

Requirement:

No hardcoded secrets.

Reference:

* SECURITY.md

---

## NFR-004 Maintainability

Requirement:

Minimum 70% coverage.

Reference:

* TESTING_STRATEGY.md

---

## NFR-005 Traceability

Requirement:

100% findings traceable to evidence.

Reference:

* PROMPT_ENGINEERING.md

---

# Out of Scope

Not included in MVP:

* SOAR
* Automated remediation
* Endpoint isolation
* SIEM replacement

---

# MVP Definition

MVP is complete when:

* FR-001 through FR-010 complete
* Golden dataset passes
* Audit score >= 90
* Deployment validated

```
```
