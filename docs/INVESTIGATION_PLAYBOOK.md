# ASTRA Investigation Playbook

Document ID: ASTRA-PLAYBOOK-001
Version: 1.0
Status: Approved

Related Documents:

* ATTACK_KNOWLEDGE_MODEL.md
* COMMON_EVENT_SCHEMA.md
* PROMPT_ENGINEERING.md
* PRD.md

---

# Purpose

Define standardized investigation procedures.

This document answers:

```text
How should ASTRA investigate security events?
```

---

# Investigation Workflow

```text
Ingest

↓

Normalize

↓

Correlate

↓

Classify

↓

Analyze

↓

Generate Timeline

↓

Generate Findings

↓

Generate Report
```

---

# PLAYBOOK-001

VPN Suspicious Login

---

## Trigger

Examples:

* Multiple failed logins
* Impossible travel
* New country login
* New device login

---

## Required Evidence

* username
* source_ip
* geolocation
* timestamp

---

## Investigation Steps

1. Identify account
2. Review login history
3. Compare geolocation
4. Compare device information
5. Assess anomaly

---

## Expected Outputs

* timeline
* confidence score
* IOC list

---

# PLAYBOOK-002

PowerShell Investigation

---

## Trigger

Examples:

```text
EncodedCommand

DownloadString

Invoke-WebRequest

Invoke-Expression
```

---

## Investigation Steps

1. Identify process parent
2. Extract command
3. Identify downloaded content
4. Map MITRE technique
5. Evaluate impact

---

## Expected Outputs

* execution chain
* technique mapping
* confidence score

---

# PLAYBOOK-003

Credential Dumping

---

## Trigger

Examples:

```text
lsass

procdump

mimikatz

comsvcs.dll
```

---

## Investigation Steps

1. Identify process creator
2. Identify target process
3. Review privileges
4. Build attack chain

---

## Expected MITRE

```text
T1003
```

---

# PLAYBOOK-004

Lateral Movement

---

## Trigger

Examples:

```text
RDP

SMB

PsExec

WMI
```

---

## Investigation Steps

1. Identify source host
2. Identify destination host
3. Identify account used
4. Correlate sequence

---

## Outputs

* attack path
* affected assets

---

# PLAYBOOK-005

Data Exfiltration

---

## Trigger

Examples:

* abnormal outbound traffic
* archive creation
* cloud upload activity

---

## Investigation Steps

1. Identify source asset
2. Estimate volume
3. Identify destination
4. Assess sensitivity

---

## Outputs

* exfiltration path
* confidence score
* IOC list

---

# Governance

New attack scenarios require:

* Playbook
* Golden Dataset
* Tests
* MITRE Mapping

```
```
