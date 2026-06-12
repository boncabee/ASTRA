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
