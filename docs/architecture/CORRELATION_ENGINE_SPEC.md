# ASTRA Correlation Engine Specification

**Version:** 3.1
**Date:** 2026-06-12
**Status:** Approved

---

## Purpose
The Correlation Engine is the critical analytical bridge between isolated data points and contextualized security incidents. Its purpose is to ingest normalized Common Event Schema (CES) events and intelligently group them into cohesive, high-fidelity investigation candidates. This ensures that the Attack Knowledge Model (AKM) and the Gemini AI reason over a unified narrative rather than fragmented alerts.

---

## Correlation Philosophy
* **Reduce Noise, Preserve Context:** Group thousands of related logs into a single narrative thread without deleting or mutating the underlying evidence.
* **Multi-Dimensional Linking:** Correlation is not strictly chronological; it must pivot simultaneously across users, hosts, IPs, and process lineages.
* **Deterministic Baseline:** The engine relies on strict, deterministic logic (rules, sliding windows, and graph traversal) rather than AI to build the initial clusters. This ensures absolute repeatability and prevents hallucination at the aggregation layer.

---

## Correlation Inputs
**Data Source:** `CES Events`
* The engine accepts strictly validated CES events outputted by the Parser Framework.
* Inputs may be streamed or processed in discrete batches bounded by logical time windows.
* The engine relies explicitly on the canonical `actor`, `target`, and `artifacts` fields for clustering, heavily penalizing reliance on unstructured `metadata`.

---

## Correlation Outputs
**Data Object:** `Correlated Event Groups` (Incident Candidates)
* A structured JSON object containing:
  * `incident_id`: A globally unique UUID representing the correlated group.
  * `root_entity`: The primary pivot point driving the cluster (e.g., User `jsmith`, or IP `10.0.0.5`).
  * `start_time` & `end_time`: The chronological boundaries encompassing the clustered events.
  * `event_count`: The total number of CES events bundled within the group.
  * `events`: An array of the underlying CES `event_id` references (or the full nested objects).

---

## Correlation Strategies
The engine applies the following strategies concurrently to build incident graphs:

* **User Correlation:** Links all events sharing the exact same actor identity (e.g., `actor.user` or `actor.email`). Essential for tracking lateral movement across multiple distinct hosts.
* **Host Correlation:** Links all events occurring on or targeting the same machine (e.g., `target.hostname`). Crucial for detecting local privilege escalation or malware execution chains.
* **IP Correlation:** Links events sharing source or destination IP addresses. Identifies external beaconing, port scanning, or data exfiltration.
* **Process Correlation:** Tracks process parent-child relationships (e.g., `cmd.exe` spawned by `winword.exe`) utilizing `actor.process` and mapping `metadata.parent_process_id`.
* **Time Correlation:** Clusters events occurring within unnaturally narrow time windows (e.g., a burst of 50 failed logins in 2 seconds). Serves primarily as an amplifier modifier to other correlation types.
* **Behavior Correlation:** Groups distinct events that match predefined tactical chains (e.g., a successful VPN login from a new IP followed immediately by an Active Directory group modification).

---

## Correlation Scoring
Each Correlated Event Group is assigned a preliminary severity score to assist in triage prioritization:
* **Event Density:** High frequency of suspicious events compressed into a short time window drastically increases the score.
* **Severity Aggregation:** The baseline presence of `high` or `critical` severity CES events within the cluster elevates the overall score.
* **Anomaly Weight:** Rare event types (e.g., `process.injection` or `authentication.mfa.bypassed`) inherently boost the score of the entire group.

---

## Confidence Scoring
The engine assigns an internal confidence score (0-100%) indicating the reliability of the clustered relationships:
* **Strong Ties (90-100%):** Events linked by exact session IDs, authentication tokens, or strict cryptographic process lineages.
* **Medium Ties (60-89%):** Events logically linked by IP and time proximities, but lacking definitive user or session context.
* **Weak Ties (<60%):** Loosely grouped events based only on broad time windows and generic subnet overlaps.

---

## Investigation Context Generation
Once a Correlated Event Group is formed and scored, the engine packages it into an `Investigation Context`.
* This context acts as the formal, final payload dispatched to the AKM mapping layer and the Gemini AI service.
* It must cleanly include the clustered CES events, the correlation rationale (exactly *why* they were grouped), and an aggregated artifacts list to facilitate immediate, context-rich AI prompt generation.

---

## Testing Requirements
* **Golden Graph Tests:** The engine must correctly assemble predefined, fragmented sets of CES events into exact, expected Correlated Event Groups without deviation.
* **Boundary Testing:** Ensure the engine cleanly separates independent events that fall just outside defined time or session sliding windows.
* **Scale Testing:** Validate that the engine can process and cluster 10,000 concurrent CES events representing interleaved, distinct attacks without cross-contamination.

---

## Performance Requirements
* **Throughput:** Must process and accurately cluster at least 5,000 CES events per second per CPU core.
* **Memory Management:** Must utilize sliding windows or stream processing state management to prevent Out-Of-Memory (OOM) crashes on large incident datasets.
* **Latency:** Batch correlation must complete in under 5 seconds for standard investigation payloads.

---

## Acceptance Criteria
The Correlation Engine specification is formally implemented only if:
* It exclusively ingests CES events and successfully outputs structured Correlated Event Groups.
* All specified correlation strategies (User, Host, IP, Process, Time, Behavior) are demonstrably functional via isolated unit tests.
* Confidence and Correlation scoring logic successfully assigns mathematical metrics to all outputted clusters.
* The system consistently meets the 5,000 EPS throughput requirement.
* It passes 100% of defined Golden Graph integration test scenarios without false linkages.
