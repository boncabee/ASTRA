# Case Reporting Integration

**Phase:** 7
**Project:** ASTRA

## 1. Reporting Engine Interface
The Case Management module acts as a primary data source for the Phase 5 Reporting Engine. The Reporting Engine consumes the immutable `Case Timeline` records to generate operational metrics.

## 2. Core Case Metrics

### 2.1 Mean Time to Acknowledge (MTTA)
- **Definition:** The average time elapsed between Case creation and the first human assignment.
- **Calculation:** `Timeline.Timestamp (State: Investigating) - Timeline.Timestamp (State: Open)`.
- **Goal:** Drive down queue wait times.

### 2.2 Mean Time to Respond (MTTR)
- **Definition:** The average time elapsed between Case creation and resolution.
- **Calculation:** `Timeline.Timestamp (State: Resolved) - Timeline.Timestamp (State: Open)`.
- **Goal:** Measure Analyst efficiency and automation effectiveness.

### 2.3 Volume Metrics
- **Open Cases:** Current count of cases in `Draft`, `Open`, `Investigating`, `Mitigating`, and `Monitoring` states.
- **Resolved Cases:** Count of cases transitioned to `Resolved` or `Closed` within a specific time window.
- **Severity Distribution:** Pie chart metrics breaking down active and historical cases by Severity (Info, Low, Medium, High, Critical).

### 2.4 Case SLA Tracking
- Reports highlighting cases that have breached predefined SLA thresholds for MTTA or MTTR based on their Priority level.

## 3. Executive and Compliance Reporting
- **Executive Dashboards:** High-level aggregation of MTTR trends over the last 30/60/90 days, correlated with the number of automated mitigations vs. manual mitigations.
- **Compliance Reporting:** End-of-month generation of Case Manifests. A report detailing every `Critical` Case, its resolution status, the assigned Analyst, and a cryptographic hash of the compiled Evidence to satisfy regulatory audit requirements.
