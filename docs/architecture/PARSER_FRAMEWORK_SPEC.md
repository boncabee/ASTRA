# ASTRA Parser Framework Specification

**Version:** 3.1
**Date:** 2026-06-12
**Status:** Approved

---

## Purpose
The Parser Framework serves as the exclusive ingest layer for the ASTRA platform. Its purpose is to ingest heterogeneous, vendor-specific raw security logs and transform them into standardized Common Event Schema (CES) events. This decoupling allows downstream correlation and AI reasoning engines to operate on a uniform data model, entirely agnostic to the source log format.

---

## Design Goals
* **Absolute Normalization:** No parser may output any data structure other than a strict CES event.
* **Idempotency:** Parsing the exact same raw log multiple times must produce the exact same CES event (including deterministic UUID generation based on log hashes if applicable).
* **High Throughput:** The framework must process large batches of logs efficiently without blocking the event loop.
* **Resiliency:** A failure to parse a single malformed log must not crash the parsing pipeline or drop the log entirely.
* **Traceability:** Every outputted CES event must contain the pristine, unmodified `raw_event` string for evidence validation.

---

## Parser Architecture
The Parser Framework is built on an extensible abstract base class (or interface). The framework implements a Router that inspects the incoming log format or source hint, instantiates the appropriate concrete Parser class, executes the parsing logic, and returns a Pydantic-validated CES object.

---

## Parser Lifecycle
Every single log ingested by ASTRA strictly follows this lifecycle:

```text
Raw Event
↓
Parse      (Extract key fields based on vendor format)
↓
Normalize  (Map vendor fields to standard CES taxonomy)
↓
Validate   (Pass through Pydantic CES model)
↓
CES Event  (Output finalized object to Correlation Engine)
```

---

## Parser Interface Contract
All concrete parsers must implement the following strict interface:

* **Input:** A single `RawLog` object containing the unparsed log string and an optional `source_hint`.
* **Output:** A validated `CESEvent` object.
* **Rule:** If a log cannot be fully parsed due to missing data or an unknown format variant, the parser **must** wrap the string in a `Custom` CES event type and attach the `raw_event`. **Logs must never be silently dropped.**

---

## Supported Input Types
The framework must provide base utility functions to handle the unpacking of the following standard input types:
* **JSON:** Fully structured nested key-value pairs (e.g., AWS CloudTrail).
* **CSV:** Comma-separated values requiring strict header mapping.
* **Syslog:** Standard RFC 3164 / RFC 5424 formats requiring regex-based extraction.
* **Windows Events:** XML-formatted EventLog data.
* **Text Logs:** Unstructured text requiring custom regex or grok patterns (e.g., raw firewall streams).

---

## Error Handling
* **Parsing Failures:** If a critical extraction fails (e.g., regex mismatch), the parser catches the exception, logs an `ERROR` with the `request_id`, and outputs a fallback `CESEvent` categorized as `Custom` with the original `raw_event` intact.
* **Validation Failures:** If the resulting mapped data fails Pydantic CES validation (e.g., invalid ISO-8601 timestamp), it is treated as a Parsing Failure and fallback logic applies.
* **Fatal Errors:** Unhandled exceptions (e.g., memory exhaustion) must be caught by the framework runner, logged, and trigger an alert, bypassing the correlation engine for that batch.

---

## Validation Rules
* Parsers are solely responsible for mapping data; the validation engine (Pydantic) is responsible for enforcing the CES schema.
* Parsers must enforce UTC timezone normalization on all extracted timestamps before passing them to the validation engine.
* Parsers must ensure the original raw string is mapped verbatim to the `raw_event` field without any trimming or mutation.

---

## Performance Requirements
* **Throughput:** The parsing engine must process and validate raw logs at a minimum rate of 10,000 logs per second per CPU core.
* **Latency:** Parsing a single event must take less than 1 millisecond.
* **Resource Bounds:** Parsers must process streams or batches iteratively to prevent massive memory spikes when ingesting multi-gigabyte log files.

---

## Security Requirements
* **Input Sanitization:** Parsers must gracefully handle malformed or maliciously crafted log inputs (e.g., billion laughs attack on XML, excessive regex backtracking).
* **Secret Masking:** Parsers should NOT attempt to mask secrets in the `raw_event` to preserve forensic integrity, but must ensure any artifacts mapped to the CES model do not expose credentials (e.g., extracting passwords from command-line arguments).

---

## Testing Requirements
* **Unit Tests:** Every parser must have unit tests covering all known variants of its target log format.
* **Golden Datasets:** Parsers must be tested against a static golden dataset of raw logs, asserting that the output exactly matches a predefined JSON CES output.
* **Fuzzing:** Parsers must be subjected to fuzzed inputs to guarantee regex safety and prevent unhandled exceptions on garbage data.

---

## Example Implementations

### VPN Parser
**Target:** Cisco ASA Syslog
**Logic:** Uses regex to extract the timestamp, source IP, username, and connection outcome. Maps to `authentication.login.success` or `authentication.login.failed`. Extracts IP to the `artifacts` array.

### Firewall Parser
**Target:** Palo Alto CSV/JSON
**Logic:** Maps source/destination IP and port fields. Evaluates the `action` field to map to `network.connection.accepted` or `network.connection.blocked`.

### Windows Event Parser
**Target:** Windows Security XML
**Logic:** Parses EventID. Maps EventID `4624` to `authentication.login.success`, extracting `TargetUserName` as the actor. Maps EventID `4688` to `process.creation.success`, extracting `NewProcessName` and `CommandLine`.

---

## Acceptance Criteria
The Parser Framework is formally accepted only if:
* The abstract parser interface is defined and implemented.
* VPN, Firewall, and Windows Event parsers successfully implement the interface.
* All parsers strictly emit CES-compliant events and pass Pydantic validation.
* No parser silently drops a log under any condition (fallback to `Custom` category works).
* Test coverage for the framework and the three initial parsers exceeds 70%.
