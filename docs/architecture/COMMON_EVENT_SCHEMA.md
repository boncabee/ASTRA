# ASTRA Common Event Schema (CES)

Document ID: ASTRA-CES-001
Version: 1.0
Status: Approved

Related Documents:

* DATABASE_SCHEMA.md
* ARCHITECTURE.md
* ATTACK_KNOWLEDGE_MODEL.md

---

# Purpose

Define the canonical event format used internally.

All parsers must output CES.

---

# Event Schema

```json
{
  "event_id": "",
  "timestamp": "",
  "source_system": "",

  "host": "",
  "user": "",

  "source_ip": "",
  "destination_ip": "",

  "event_type": "",
  "action": "",

  "severity": "",

  "raw_message": "",

  "metadata": {}
}
```

---

# Required Fields

Mandatory:

* event_id
* timestamp
* source_system
* event_type

---

# Event Categories

Supported:

```text
authentication

network

process

file

registry

powershell

vpn

firewall

web

database
```

---

# Severity Levels

```text
informational

low

medium

high

critical
```

---

# Correlation Fields

High Priority:

```text
user

host

source_ip

destination_ip

timestamp
```

---

# Parser Contract

Parser Input:

```text
Raw Vendor Log
```

Parser Output:

```text
CES Event
```

Validation Required:

* schema validation
* timestamp validation
* field normalization

---

# Governance

No parser may bypass CES.

```
```
