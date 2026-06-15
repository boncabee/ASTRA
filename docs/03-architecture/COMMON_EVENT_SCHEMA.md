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


# Common Event Schema (CES) Implementation Guide

**Version:** 3.1
**Date:** 2026-06-12
**Status:** Approved

---

## Purpose
The Common Event Schema (CES) is the foundational data model for ASTRA v3.1. This implementation guide details how to build, validate, and integrate the CES layer, effectively decoupling vendor-specific raw log formats from ASTRA's Correlation Engine and AI reasoning models.

---

## Design Goals
The CES implementation must strictly adhere to the following architectural requirements:
* **Vendor Agnostic:** The schema must represent security activities generically without relying on specific vendor nomenclature (e.g., Splunk, CrowdStrike, Palo Alto).
* **Extensible:** The schema must cleanly accommodate new event categories and highly customized artifacts without breaking existing correlations.
* **Versioned:** Changes to the schema structure must be explicitly version-controlled to avoid breaking downstream investigation playbooks.
* **Traceable:** Every instantiated CES event must maintain a pristine, unmodified copy of the `raw_event` to guarantee absolute evidence validation.
* **AI Friendly:** The schema must be structured cleanly in JSON to optimize LLM token consumption and eliminate context hallucinations within the Gemini integration.

---

## Canonical Event Structure
Every CES event must be instantiated from a strict validation model (e.g., Pydantic) enforcing the following fields:

* `event_id` *(String, UUID)*: A globally unique identifier for the normalized event.
* `timestamp` *(String, ISO-8601)*: The exact time the event occurred in UTC.
* `source_type` *(String)*: The system or vendor originating the raw log (e.g., `windows_event_log`, `cisco_asa`).
* `event_type` *(String)*: The normalized, standardized action that occurred (e.g., `authentication.login.success`).
* `severity` *(String)*: Normalized severity level (`info`, `low`, `medium`, `high`, `critical`).
* `actor` *(Object)*: The primary entity initiating the action (e.g., user, originating process, source IP).
* `target` *(Object)*: The entity being acted upon (e.g., destination file, target host, destination port).
* `artifacts` *(Array)*: Extracted Indicators of Compromise (e.g., IPs, Domains, File Hashes).
* `raw_event` *(String)*: The original, completely unmodified source log string.
* `metadata` *(Object)*: Key-value pairs for parser-specific context that does not fit natively into the canonical model.

---

## Event Categories
To standardize downstream correlation, `event_type` must explicitly map to one of the following root categories:
* **Authentication:** Login, logout, privilege escalation, MFA failures.
* **Network:** Connections, DNS queries, firewall blocks, byte transfers.
* **Endpoint:** Registry modifications, service creations, scheduled tasks.
* **Process:** Process creation, process termination, code injection.
* **File:** File creation, deletion, modification, permission changes.
* **Cloud:** API calls, IAM role assumptions, storage bucket accesses.
* **Application:** Web server logs, custom business logic events.
* **Custom:** A temporary catch-all category for uncategorized alerts pending formal mapping updates.

---

## Event Validation Rules
Runtime validation must be enforced immediately upon parser output.
* **Required fields:** `event_id`, `timestamp`, `source_type`, `event_type`, `raw_event`.
* **Optional fields:** `severity` (defaults to `info`), `actor`, `target`, `artifacts`, `metadata`.
* **Field constraints:**
  * `timestamp` must successfully parse as a valid ISO-8601 format string.
  * `event_type` must follow the exact taxonomy format: `category.action.outcome`.
  * `artifacts` must be an array of strongly typed objects (e.g., `{"type": "ip", "value": "1.1.1.1"}`).

---

## Event Versioning Strategy
* **CES v1:** The initial foundational schema designed during Sprint 1. Marked via a mandatory `schema_version` field set to `"1.0"`.
* **Future versions:** Will increment semantically (e.g., `"1.1"` for additive, non-destructive fields; `"2.0"` for breaking structural changes).
* **Backward compatibility rules:** Deprecated fields must remain in the validation models as `Optional` and emit backend warnings for at least one major version cycle prior to complete removal.

---

## Parser Integration Contract
The Parser Framework serves as the absolute entry point for the CES layer.
* **Input:** Raw Logs (JSON, CSV, Syslog).
* **Output:** Validated CES Events.
* **Constraint:** Parsers must never drop logs. If a log cannot be fully normalized due to missing vendor data, it must be mapped to the `Custom` category with the `raw_event` left fully intact for manual analysis.

---

## Correlation Integration Contract
The Correlation Engine groups isolated logs into chronological incidents.
* **Input:** CES Events.
* **Output:** Correlated Events (Incident Candidates).
* **Constraint:** Correlation rules must explicitly reference the canonical `actor`, `target`, and `artifacts` fields rather than relying on deep, variable `metadata` keys.

---

## AI Integration Contract
The Gemini API analyzes the correlated data payload.
* **Input:** CES Events (bundled as a structured Incident Candidate).
* **Output:** Investigation Context (Timelines, Narratives, MITRE mappings, IOC extraction).
* **Constraint:** AI models must reference the specific CES `event_id` when generating evidence-backed findings to maintain 100% traceability.

---

## Examples

### 1. VPN Login Event
```json
{
  "schema_version": "1.0",
  "event_id": "uuid-1234",
  "timestamp": "2026-06-12T08:00:00Z",
  "source_type": "cisco_asa",
  "event_type": "authentication.login.success",
  "severity": "info",
  "actor": {"user": "jsmith", "ip": "203.0.113.5"},
  "target": {"hostname": "vpn.corp.local"},
  "artifacts": [{"type": "ip", "value": "203.0.113.5"}],
  "raw_event": "...",
  "metadata": {"vpn_group": "Engineering"}
}
```

### 2. Windows Logon Event
```json
{
  "schema_version": "1.0",
  "event_id": "uuid-5678",
  "timestamp": "2026-06-12T08:05:00Z",
  "source_type": "windows_event_log",
  "event_type": "authentication.login.success",
  "severity": "info",
  "actor": {"user": "jsmith", "domain": "CORP"},
  "target": {"hostname": "WS-0123"},
  "artifacts": [],
  "raw_event": "...",
  "metadata": {"event_id": "4624", "logon_type": "3"}
}
```

### 3. Firewall Event
```json
{
  "schema_version": "1.0",
  "event_id": "uuid-9012",
  "timestamp": "2026-06-12T08:10:00Z",
  "source_type": "palo_alto",
  "event_type": "network.connection.blocked",
  "severity": "low",
  "actor": {"ip": "10.0.0.5", "port": 54321},
  "target": {"ip": "198.51.100.10", "port": 22},
  "artifacts": [{"type": "ip", "value": "198.51.100.10"}],
  "raw_event": "...",
  "metadata": {"rule_name": "Block_Outbound_SSH"}
}
```

### 4. PowerShell Event
```json
{
  "schema_version": "1.0",
  "event_id": "uuid-3456",
  "timestamp": "2026-06-12T08:15:00Z",
  "source_type": "windows_event_log",
  "event_type": "process.creation.success",
  "severity": "high",
  "actor": {"user": "jsmith", "process": "powershell.exe"},
  "target": {"command_line": "powershell.exe -ExecutionPolicy Bypass -enc JABz..."},
  "artifacts": [],
  "raw_event": "...",
  "metadata": {"event_id": "4104", "script_block_id": "..."}
}
```

---

## Testing Requirements
* **Validation Tests:** Unit tests verifying that the validation engine (e.g., Pydantic) properly accepts valid payloads and explicitly rejects instances with missing mandatory fields or invalid ISO-8601 timestamps.
* **Parser Compatibility Tests:** Integration tests feeding raw vendor logs into parsers and asserting the output perfectly matches a verified CES golden dataset.
* **Schema Evolution Tests:** Tests guaranteeing that V1.0 schema payloads process without error if the downstream system upgrades to V1.1.

---

## Acceptance Criteria
The CES implementation (Sprint 1) is formally accepted only if:
* All instantiated events validate perfectly without silent failure.
* All created parsers (VPN, Windows, Firewall) output the exact standard CES format.
* Schema versioning constraints are actively proven to work via unit tests.
* Unit and Integration tests pass with >70% coverage.



