# ASTRA Database Schema

Document ID: ASTRA-DB-001
Version: 2.0
Status: Approved

Related Documents:

* ARCHITECTURE.md
* API_SPEC.md
* TRACEABILITY_MATRIX.md

---

# Purpose

Define data storage contracts.

---

# Core Design Principles

## Single Source of Truth

Each data element stored once.

---

## Traceability

Every finding must map back to events.

---

## Auditability

All analyses must be reproducible.

---

# Tables

## analysis_jobs

Purpose:

Track analysis execution.

Source:

FR-001

---

## uploaded_files

Purpose:

Track uploads.

Source:

FR-001

---

## incidents

Purpose:

Store incident results.

Source:

FR-003

---

## timelines

Purpose:

Store timeline entries.

Source:

FR-004

---

## mitre_mappings

Purpose:

Store ATT&CK mappings.

Source:

FR-006

---

## iocs

Purpose:

Store indicators.

Source:

FR-007

---

## incident_events

Purpose:

Store normalized CES events.

Source:

FR-002

---

# CES Standard

All parsers must produce:

```json
{
  "event_id": "",
  "timestamp": "",
  "source": "",
  "host": "",
  "user": "",
  "ip": "",
  "event_type": "",
  "action": "",
  "raw_message": "",
  "metadata": {}
}
```

---

# Data Retention

Default:

```text
90 days
```

Configurable.

---

# Privacy Controls

Reference:

SECURITY.md

Supported:

* Hash usernames
* Hash IPs
* Remove raw events

---

# Database Governance

Any schema modification requires updates to:

* ARCHITECTURE.md
* TRACEABILITY_MATRIX.md
* TESTING_STRATEGY.md
* AUDIT.md

```
```
