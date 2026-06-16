# Correlation Domain Model

## Executive Summary
**Correlation** is the central analytical engine of ASTRA. Its primary purpose is to identify meaningful patterns across massive volumes of raw, normalized `CES Events`. It transforms disjointed data points into cohesive, actionable contexts.

Correlation exists because singular events rarely provide enough context to declare a security incident. The Correlation Engine aggregates these events based on predefined logic over time.

**Relationships:**
* **Event**: The raw, normalized input (CES Event).
* **Correlation**: The logic and resulting aggregation of Events.
* **Observation**: If a Correlation Match meets specific thresholds, it is elevated into a single Observation.
* **Policy**: Rules applied to Observations to determine the necessary Action.
* **Action**: The automated or manual response triggered by a Policy.

---

## Correlation Domain Definition

* **Correlation Rule**: A formal definition of logic (event types, conditions, and time constraints) used to identify a pattern.
* **Correlation Match**: A specific instance where incoming events have successfully triggered a Correlation Rule.
* **Correlation Window**: The timeframe within which events must occur to satisfy the rule's conditions.
* **Correlation Result**: The evaluated outcome of a Match, dictating whether the pattern warrants escalation to an Observation.
* **Correlation Context**: The aggregated metadata and correlated entities (e.g., source IPs, user IDs) extracted from the matched events.

**Relationships:**
A single `Correlation Rule` evaluates many `Events` within a `Correlation Window`. When conditions are met, a `Correlation Match` is generated containing the `Correlation Context`. This match is evaluated to produce a `Correlation Result`.

---

## Correlation Lifecycle

1. **RULE_REGISTERED**: A rule is created but not actively processing events.
2. **RULE_ACTIVE**: The rule is actively analyzing the incoming event stream.
3. **MATCH_DETECTED**: The engine identifies a pattern of events satisfying the active rule.
4. **OBSERVATION_CREATED**: The match exceeds the necessary risk or severity threshold and is elevated to an Observation.
5. **RULE_DISABLED**: The rule is deactivated and ceases processing.

**Transitions:**
* *Valid*: REGISTERED -> ACTIVE -> MATCH_DETECTED -> OBSERVATION_CREATED. ACTIVE -> DISABLED -> ACTIVE.
* *Invalid*: MATCH_DETECTED -> RULE_REGISTERED.

**Ownership:**
* *System Ownership*: MATCH_DETECTED, OBSERVATION_CREATED (generated automatically by the engine).
* *User Ownership*: RULE_REGISTERED, RULE_ACTIVE, RULE_DISABLED (managed by Security Engineers/Administrators).

---

## Correlation Rule Schema

| Field | Data Type | Required | Description |
|---|---|---|---|
| `id` | UUID | Yes | Unique identifier for the rule. |
| `name` | String | Yes | Human-readable name of the correlation. |
| `description` | Text | Yes | Detailed explanation of what the rule detects. |
| `enabled` | Boolean | Yes | Operational status of the rule. |
| `event_types` | Array[Enum] | Yes | List of CES Event Types monitored by this rule. |
| `conditions` | JSON/Dict | Yes | The logical expression/DSL defining the match criteria. |
| `time_window` | Integer | Yes | The window duration in seconds. |
| `severity_weight` | Integer | Yes | The base weight (0-100) applied to matches. |
| `created_at` | DateTime | Yes | Rule creation timestamp. |
| `updated_at` | DateTime | Yes | Last modification timestamp. |
| `created_by` | UUID | Yes | User who created the rule. |
| `updated_by` | UUID | Yes | User who last updated the rule. |

---

## Correlation Match Schema

| Field | Data Type | Required | Description |
|---|---|---|---|
| `id` | UUID | Yes | Unique identifier for the match. |
| `rule_id` | UUID | Yes | Foreign key to the Correlation Rule. |
| `matched_events` | Array[UUID] | Yes | List of CES Event IDs that triggered the match. |
| `event_count` | Integer | Yes | Total number of events aggregated. |
| `match_timestamp` | DateTime | Yes | The exact time the match criteria was satisfied. |
| `correlation_score` | Integer | Yes | The computed severity of this specific match instance. |
| `context` | JSON | No | Extracted entities (IPs, Users, Hosts) for quick reference. |

---

## Correlation Classification

1. **Authentication**: Anomalous login patterns (e.g., brute force, impossible travel).
2. **Privilege Escalation**: Unexpected elevation of user or process rights.
3. **Network Activity**: Port scans, beaconing, or data exfiltration signatures.
4. **Malware**: Execution of known malicious payloads or ransomware-like file operations.
5. **Policy Violation**: Internal compliance breaches (e.g., unauthorized data access).
6. **Anomaly Detection**: Statistical deviations from established baselines (AI/ML driven).

*Rationale*: Standardizing classifications aligns Correlation output directly with MITRE ATT&CK mapping and simplifies triage for SOC Analysts.

---

## Correlation Window Model

* **Sliding Window**: Evaluates events over a continuous, moving timeframe (e.g., 5 failed logins within *any* 5-minute span).
* **Fixed Window**: Evaluates events within rigid time blocks (e.g., 5 failed logins between 12:00 and 12:05).

**Supported MVP Approach**: 
* **Fixed Windows (Tumbling)** will be utilized for the MVP to minimize computational overhead and state management complexity.

**Future Approaches**:
* **Sliding Windows** will be introduced in subsequent phases leveraging a stream processing framework (e.g., Flink/Kafka Streams) when sub-second accuracy is required.

---

## Correlation Scoring Model

* **Correlation Score**: An integer (0-100) representing the severity and confidence of the matched pattern.
* **Relationship to Risk Score**: The Correlation Score acts as an *input* to the Observation Risk Score. 
* **Scoring Inputs**: Rule `severity_weight`, total `event_count`, and asset criticality.
* **Scoring Constraints**: The score is capped at 100.

**Important Distinction:**
`Correlation Score` ≠ `Observation Risk Score`. 
The Correlation Score evaluates the technical certainty and severity of the pattern itself. The Observation Risk Score evaluates the holistic business impact, factoring in asset value and historical context.

---

## Observation Creation Rules

* **When Created**: Automatically generated when a Correlation Match's `correlation_score` exceeds a configured threshold (e.g., > 50).
* **When NOT Created**: If the pattern matches but the score is below the threshold, the match is logged for future context but does not trigger an Observation.
* **Duplicate Prevention Strategy**: The engine checks the `context` (e.g., Source IP + Target Host) against active Observations within the last X hours. If a match exists, the new Correlation Match is *appended* to the existing Observation rather than creating a new one.
* **Explosion Prevention**: A rate limiter restricts the creation of Observations originating from a single rule to a maximum of N per hour.
* **Threshold Rules**: Configurable on a per-rule basis, allowing high-fidelity rules to bypass threshold checks.

---

## Correlation API Contract

* **`GET /api/v1/correlations`**: List all Correlation Matches.
* **`GET /api/v1/correlations/{id}`**: Retrieve specific match details and context.
* **`GET /api/v1/correlations/rules`**: List active Correlation Rules.
* **`GET /api/v1/correlations/matches`**: Filterable endpoint for match history.

**Supported Filters**: `rule_id`, `start_time`, `end_time`, `min_score`, `classification`.
**Pagination**: Offset/Limit based.
**Sorting**: `match_timestamp` (DESC default), `correlation_score`.

**Response Structure**:
```json
{
  "data": [ ... ],
  "meta": { "total": 100, "page": 1 }
}
```
**Error Structure**:
```json
{
  "error": "Message",
  "code": 400
}
```

---

## Correlation UI Requirements

* **Correlation Rule List**: Grid displaying Rule Name, Classification, Status, and Event Types.
* **Correlation Match List**: Feed displaying Timestamp, Rule Triggered, Event Count, and Score.
* **Correlation Detail**: Deep dive showing the matched rule logic, extracted context (IPs/Users), and a chronological list of the `matched_events`.

**Role Restrictions**:
* *Security Engineer / Administrator*: Full Read/Write access to Rules.
* *SOC Analyst / Incident Responder*: Read-only access to Rules and Matches.

---

## Performance Requirements

* **Expected Events per Minute**: 100,000+ (Aligned with ADR-017 ingestion rates).
* **Expected Matching Latency**: < 5 seconds from event ingestion to match detection.
* **Storage Expectations**: High volume. Matches stored in primary DB for 30 days.
* **Retention Expectations**: Rules retained indefinitely; Matches archived after 30 days.
* **Indexing Recommendations**: Heavy indexing on `rule_id`, `match_timestamp`, and JSON `context` keys for rapid correlation lookups.

---

## Future Compatibility

* **Observation Engine**: Feeds directly into Observation generation via explicit triggers.
* **Policy Engine**: Policies can evaluate Correlation Scores natively.
* **Automation Engine**: Can trigger immediate mitigations based on high-fidelity Correlation Rules before an Observation is manually triaged.
* **Case Management**: Correlation Matches can be linked as evidence to Case files.
* **Report Engine**: Match volumes and classifications feed into SOC metric reporting.

---

## Open Risks

* **False Correlations**: Poorly tuned rules may trigger constantly.
* **Correlation Explosion**: A single compromised host could trigger thousands of matches.
* **Storage Growth**: Retaining `matched_events` arrays for high-volume rules could bloat the database.
* **Duplicate Observations**: Complex, overlapping rules might generate redundant observations for the same incident.
* **Performance Degradation**: Complex JSON condition evaluation may slow down the batch processor.

---

## Recommendations

* **Immediate**: Implement strict validation on Rule DSL (conditions) to prevent unoptimized queries.
* **Sprint 3**: Implement the Fixed Window correlation strategy synchronously within the Batch Processor.
* **Sprint 4+**: Offload Correlation evaluation to an asynchronous worker queue or stream processor to guarantee ingestion latency.

---

## Architecture Decision

**Correlation Domain Model: APPROVED**
*Justification*: The model provides a robust, scalable foundation that cleanly separates pattern detection (Correlation) from incident management (Observation), aligning perfectly with the ASTRA realigned architecture and Sprint 3 goals.
