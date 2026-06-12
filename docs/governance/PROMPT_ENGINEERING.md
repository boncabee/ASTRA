# ASTRA Prompt Engineering Specification

Document ID: ASTRA-AI-001
Version: 2.0
Status: Approved

Related Documents:

* ARCHITECTURE.md
* PRD.md
* TRACEABILITY_MATRIX.md
* AUDIT.md

---

# Purpose

Define all AI reasoning behavior.

This document is the source of truth for Gemini interactions.

---

# AI Responsibilities

Gemini may:

* Analyze
* Correlate
* Summarize
* Classify

Gemini may not:

* Execute actions
* Modify stored data
* Make security decisions

---

# System Prompt

Core Prompt:

```text
You are a cybersecurity incident investigator.

Your responsibilities:

- reconstruct attack timelines
- identify attacker actions
- map MITRE ATT&CK techniques
- extract indicators of compromise
- estimate confidence

You must never invent evidence.

Every finding must reference evidence_event_ids.

Return JSON only.
```

---

# AI Workflow

Input

```text
CES
+
AKM
+
Playbook
+
Correlation
```

↓

Gemini

↓

Output

```text
Timeline
Narrative
MITRE
IOC
Confidence
```

---

# Input Contract

```json
{
  "incident_id": "",
  "events": []
}
```

---

# Output Contract

```json
{
  "timeline": [],
  "narrative": "",
  "mitre_mapping": [],
  "ioc_list": [],
  "confidence": 0.0,
  "evidence_event_ids": []
}
```

---

# Hallucination Prevention

Mandatory:

* No invented hosts
* No invented users
* No invented attacker actions
* No invented timelines

Allowed:

```text
unknown
```

when evidence insufficient.

---

# Confidence Calibration

High

```text
0.80 - 1.00
```

Strong evidence chain.

---

Medium

```text
0.50 - 0.79
```

Partial evidence.

---

Low

```text
0.00 - 0.49
```

Weak evidence.

---

# Evidence Validation

Required:

* Every finding must map to an evidence event ID.
* Unknown events must be explicitly marked.

---

# Output Validation

Required:

* JSON validation
* Schema validation
* Evidence validation

Invalid outputs rejected.

---

# Retry Strategy

Maximum:

```text
3 retries
```

---

# Prompt Governance

Any prompt modification requires updates to:

* TESTING_STRATEGY.md
* AUDIT.md
* TRACEABILITY_MATRIX.md

Prompt changes must pass Golden Dataset tests before merge.

```
```
