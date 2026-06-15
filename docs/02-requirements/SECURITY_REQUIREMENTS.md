# ASTRA Threat Model

Document ID: ASTRA-THREAT-001
Version: 2.0
Status: Approved

Related Documents:

* SECURITY.md
* ARCHITECTURE.md
* AUDIT.md

Methodology:

```text
STRIDE
```

---

# Purpose

Identify and mitigate threats against ASTRA.

---

# Scope

Protected Components:

* Frontend
* API
* Upload Service
* Parser Layer
* AI Reasoner
* Database

---

# Assets

Critical Assets:

1. Uploaded Logs
2. Incident Results
3. Gemini API Key
4. Database Records
5. Prompt Templates

---

# Trust Boundaries

```text id="8xjlwm"
Internet

↓

Frontend

↓

API

↓

AI Layer

↓

Database
```

---

# STRIDE Analysis

---

## Spoofing

Threat:

Attacker impersonates user.

Mitigation:

* Future Authentication
* JWT
* Session Validation

Risk:

Medium

---

## Tampering

Threat:

Log manipulation.

Mitigation:

* File Hashing
* Immutable Upload Records

Risk:

High

---

## Repudiation

Threat:

Action denial.

Mitigation:

* Audit Logs
* Request IDs

Risk:

Medium

---

## Information Disclosure

Threat:

Sensitive data leakage.

Mitigation:

* Privacy Mode
* PII Hashing
* Restricted Logging

Risk:

Critical

---

## Denial of Service

Threat:

Massive uploads.

Mitigation:

* Upload limits
* Rate limiting
* Queue controls

Risk:

High

---

## Elevation of Privilege

Threat:

Unauthorized access escalation.

Mitigation:

* Least Privilege
* Container Isolation

Risk:

High

---

# AI-Specific Threats

---

## Prompt Injection

Threat:

Malicious instructions inside uploaded logs.

Mitigation:

* Prompt Isolation
* Output Validation

Reference:

PROMPT_ENGINEERING.md

Risk:

Critical

---

## Hallucination

Threat:

AI invents evidence.

Mitigation:

* Evidence references
* Confidence scoring
* Golden dataset validation

Risk:

Critical

---

## Data Leakage

Threat:

Sensitive logs exposed externally.

Mitigation:

* Privacy Mode
* Data minimization

Risk:

Critical

---

# Risk Matrix

| Threat           | Likelihood | Impact   |
| ---------------- | ---------- | -------- |
| Prompt Injection | High       | Critical |
| Hallucination    | High       | Critical |
| Data Leakage     | Medium     | Critical |
| DoS              | Medium     | High     |
| Tampering        | Medium     | High     |

---

# Threat Review Triggers

Review required when:

* New parser added
* New AI workflow added
* New external integration added
* Database schema changes

---

# Threat Model Acceptance

System considered secure when:

* No Critical unmitigated threats
* Security tests pass
* Audit score >= 90

```id="5rft8a"
```


# ASTRA Attack Knowledge Model

Document ID: ASTRA-AKM-001
Version: 1.0
Status: Approved

Related Documents:

* COMMON_EVENT_SCHEMA.md
* INVESTIGATION_PLAYBOOK.md
* PROMPT_ENGINEERING.md

---

# Purpose

Define how ASTRA understands attacks.

This document becomes the reasoning foundation for Gemini.

---

# Attack Lifecycle

```text
Initial Access

↓

Execution

↓

Persistence

↓

Privilege Escalation

↓

Defense Evasion

↓

Credential Access

↓

Discovery

↓

Lateral Movement

↓

Collection

↓

Exfiltration
```

---

# Core Investigation Objects

## Actor

Examples:

* user
* attacker
* service account

---

## Asset

Examples:

* workstation
* server
* VPN gateway

---

## Event

Examples:

* login
* process creation
* firewall allow

---

## Indicator

Examples:

* IP
* hash
* domain

---

# Confidence Model

High Confidence

Requirements:

* multiple corroborating events
* consistent timeline

Score:

```text
0.80 - 1.00
```

---

Medium Confidence

Requirements:

* partial evidence

Score:

```text
0.50 - 0.79
```

---

Low Confidence

Requirements:

* weak evidence

Score:

```text
0.00 - 0.49
```

---

# MITRE Mapping Rules

Every detection should map:

```text
Behavior

↓

Technique

↓

Evidence
```

Never:

```text
Technique

↓

Guess Evidence
```

---

# Reasoning Rules

Gemini must:

* prioritize evidence
* avoid assumptions
* reference event IDs
* preserve chronology

If evidence is insufficient:

```text
unknown
```

must be returned.

```
```



