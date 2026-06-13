---
id: ARCH-REVIEW-SPRINT-2
type: architecture-review
sprint: 2
status: APPROVED WITH REVISIONS
---

# ASTRA Architecture Review Report

## Executive Summary
This document serves as the authoritative post-Sprint 2 checkpoint from the ASTRA Architecture Review Board. The purpose is to evaluate the viability of the ASTRA platform architecture based on empirical evidence gathered during the implementation of the Parser Framework and production parsers (VPN, Windows, Firewall).

The architectural decisions made in Sprint 1 (CES implementation, modular decoupling, fallback layers) were severely tested in Sprint 2. The evidence confirms that the object-oriented abstractions and declarative transformation pipelines are robust, accurate, and extensible. However, critical scalability bottlenecks and schema taxonomy gaps were discovered that must be remediated before entering high-volume ingestion phases. 

**Final Decision:** **APPROVED WITH REVISIONS**

---

## Architecture Areas To Review

| Area | Evaluation |
|---|---|
| **1. Common Event Schema (CES)** | Proven highly effective for standardizing vastly different logs, though missing strict enumerations (e.g., `identity`). |
| **2. Parser SDK** | Excellent abstraction; the `BaseParser` effectively hides validation complexity from parser developers. |
| **3. TransformerConfig** | Highly successful at decoupling vendor-specific mappings from python code. |
| **4. Parser Registry** | Validated as a seamless, plug-and-play dynamic discovery mechanism. |
| **5. Batch Processing** | Functional for small loads, but synchronous looping and uncapped memory pose severe scale risks. |
| **6. Fallback Processing** | Proven to prevent data loss, though extremely large payloads risk validation crashes without a DLQ. |
| **7. Parser Architecture** | Solid object-oriented structure; regex-coupling to vendor versions remains a fragility point. |
| **8. Ingestion Architecture** | Incomplete. Currently lacks asynchronous IO streaming and horizontal scaling. |
| **9. Event Taxonomy** | Mostly accurate, but `authentication.login.success` and missing user-management tags require expansion. |
| **10. Entity Model** | Strong, but mapping `TargetUserName` vs `SubjectUserName` (Windows) creates correlation ambiguity. |
| **11. Artifact Model** | Unidirectional artifact extraction (e.g., Firewall IPs) must evolve to bidirectional. |
| **12. Future Correlation Engine Compatibility** | High. Normalized data will cleanly feed correlation rules. |
| **13. Future Rule Engine Compatibility** | High. Standardized schemas enable simplified YAML-based detection rules. |
| **14. Future AKM Compatibility** | Moderate. Fallback logs (`custom.unknown`) might introduce graph noise if not filtered. |
| **15. Future Observability Compatibility** | Moderate. Telemetry exists, but Dead Letter Queues (DLQs) are missing for fatal failures. |

---

## Required Analysis

### What worked well
* **Decoupling via TransformerConfig:** Moving field mappings to configuration objects prevented the parser code from becoming unmaintainable nested dictionaries.
* **Schema Validation:** Pydantic's strict typing immediately caught format mismatches, preventing bad data from entering the database pipeline.

### What failed
* **Taxonomy Rigidity:** Pydantic strictness natively rejected Windows User Management events because the `identity` Event Category was not anticipated in Sprint 1.
* **Synchronous Batching:** The `BatchProcessor` loops block the event loop, proving unsuitable for modern async-first web frameworks (FastAPI).

### What is missing
* **Asynchronous IO / Streaming Engine:** Capable of chunking logs without blowing up memory.
* **Dead Letter Queue (DLQ):** To catch `RecoveryFailureError` instances when even the fallback mapper fails.

### What should change
* The `BatchProcessor` must cache parser instantiations instead of calling the registry factory inside tight loops.
* The CES Event Category Enum must be expanded to include new security domains (`identity`, `network.nat`).

### What should remain unchanged
* The `ParserRegistry` pattern.
* The `CESEvent` structural payload (Entities, Artifacts, Metadata).

---

## Architecture Decisions Review

| Decision Area | Status | Justification |
|---|---|---|
| **CES Normalization First** | **Validated** | It successfully normalized Cisco, Windows, and Firewall logs. |
| **JSON/Dict Driven Transformers** | **Validated** | Rapidly accelerated parser development. |
| **Synchronous Batching** | **Invalidated** | Will cause production blockages; requires async refactor. |
| **Strict Enum Schema Types** | **Partially Validated** | Secure, but requires iterative expansion (needs revision to add `identity`). |
| **Centralized Fallback Handling** | **Validated** | Consistently catches parsing anomalies. |

---

## Specific Topics Review

| Topic | Description | Recommendation | Evaluation Outcome |
|---|---|---|---|
| **ARCH-001 Identity EventCategory Gap** | Missing `identity` taxonomy in CES schema. | Update Pydantic Enum. | **Architecture Change** (Sprint 3 Task) |
| **PF-011 Windows LogonType Ambiguity** | Event 4624 maps machine accounts (noise) and users identically. | Filter/Enrich pre-processing step. | **Sprint 3 Task** |
| **PF-016 NAT Visibility** | Firewall parser lacks Pre/Post NAT translation correlation. | Expand CES network metadata. | **Sprint 4 Task** |
| **PF-017 Bidirectional IOC Extraction** | Firewall only extracts target IP as Artifact, missing malicious source IPs. | Modify `firewall_parser.py` logic. | **Sprint 3 Task** |
| **PF-018 Batch Memory Risks** | Max batch sizes of ~64KB payloads cause memory spikes. | Implement chunked iterators. | **Architecture Change** (Sprint 4 Task) |
| **PF-020 Async Processing Need** | Batch processor blocks FastAPI event loops. | `async def process()` migration. | **Architecture Change** (Sprint 3 Task) |
| **PF-008 Dead Letter Queue Requirement** | Fatal fallback generation failures drop data. | Implement DLQ on ingestion router. | **Sprint 3 Task** |

---

## Future Architecture Readiness

| Subsystem | Readiness | Notes |
|---|---|---|
| **Correlation Engine** | High | Standardized `CESEvent` outputs are highly predictable. |
| **Rule Engine** | High | Uniform fields allow for easy Sigma-rule or custom YAML rule translations. |
| **AKM (Attack Knowledge Model)** | Moderate | Bidirectional IP extraction and better Identity tracking is needed before generating Graph edges. |
| **Case Management** | High | Fallback events ensure all logs, even unparsed, can be attached to an investigation. |
| **Threat Intelligence** | Moderate | Needs automated tagging of internal (RFC-1918) vs external IPs to avoid querying TI for local networks. |
| **Detection Engineering** | High | Analysts have a clear, documented SDK to build custom parsers. |
| **SOC Workflow Automation** | Moderate | High volume of `custom.unknown` fallback events may fatigue automated triage if not filtered. |

---

## Required Scores

* **CES Score:** 85/100 *(Strictness is good, but taxonomy needs immediate expansion).*
* **Parser Framework Score:** 95/100 *(Object-oriented abstractions proved highly successful).*
* **Scalability Score:** 70/100 *(Synchronous processing and memory handling are critical flaws).*
* **Maintainability Score:** 90/100 *(TransformerConfig heavily reduces code bloat).*
* **Extensibility Score:** 95/100 *(Registry pattern is flawless).*
* **Observability Score:** 80/100 *(Good telemetry, but missing fatal-failure DLQ).*
* **Overall Architecture Score:** **86/100**

---

## Required Outputs

* **Architecture Strengths:** Unmatched data consistency; highly modular; prevents silent parser failures; rapid extensibility.
* **Architecture Weaknesses:** Synchronous IO bottlenecks; strict schema prevents ingesting novel categories without code changes; naive memory management.
* **Architecture Risks:** Vendor log format changes (e.g., Cisco ASA to FTD) will break regexes silently triggering high volumes of fallback events.
* **Architecture Opportunities:** The `TransformerConfig` can be exposed via a UI, allowing SOC analysts to map new logs without writing Python code.
* **Architecture Constraints:** Must operate within FastAPI's async paradigms; cannot afford to hold large batches in RAM.

---

## Generate Recommendations

### Immediate (Pre-Sprint 3)
1. **Schema Patch:** Update the `EventCategory` Enum in `app/schemas/ces.py` to include `identity` to unblock native Windows user-management parsing.

### Sprint 3
1. **Async Batch Engine:** Refactor `BatchProcessor` to utilize `async/await` to align with the core FastAPI architecture.
2. **Dead Letter Queue (DLQ):** Introduce a final safety net for `RecoveryFailureError` instances.
3. **Bidirectional Artifacts:** Update Firewall and VPN parsers to extract both Source and Target IPs into the `Artifact` array.
4. **Pre-Processing Filters:** Implement `LogonType` filtering for the Windows Parser to drastically reduce noise.

### Sprint 4+
1. **Memory Chunking:** Re-architect the batching mechanism to stream payload chunks, enforcing a strict RAM ceiling.
2. **NAT Tracking:** Expand CES schema to cleanly handle Pre-NAT and Post-NAT firewall mappings.
3. **Threat Intelligence Scaffolding:** Implement RFC-1918 internal IP tagging.

### Long-Term
1. **UI-Driven Parsers:** Expose `TransformerConfig` schemas to a front-end dashboard to eliminate the need for developer intervention for basic log mapping.
2. **Dynamic Taxonomy:** Evaluate replacing static Python Enums with database-driven taxonomies that can evolve dynamically at runtime.

---

## Architecture Roadmap

* **Sprint 3 (Pipeline Scaling & Correlation Prep):** Fix asynchronous ingestion bottlenecks, implement DLQ, expand schema taxonomies, and enhance IP Artifact extraction.
* **Sprint 4 (Advanced Telemetry & Rule Engine):** Implement memory chunking, integrate NAT network visibility, and begin routing CESEvents into a formalized Rule Engine.
* **Sprint 5 (Threat Intel & AKM):** Introduce automated Threat Intelligence lookups on extracted Artifacts and begin constructing the Attack Knowledge Model (graph DB edges).

---

## Final Decision

**APPROVED WITH REVISIONS**

**Justification:** The architecture fundamentally works and achieves its primary goal of standardizing heterogeneous security telemetry. However, it must undergo targeted async and scalability revisions in Sprint 3 to safely support high-throughput, production-grade log ingestion before moving into advanced correlation phases.
