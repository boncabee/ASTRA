# Master Risk Register

## Overview
This document consolidates all identified risks across ASTRA's lifecycle from Phase 1 through Phase 5.

## Consolidated Risks

| Risk ID | Description | Likelihood | Impact | Mitigation | Status | Owner | Target Sprint |
|---|---|---|---|---|---|---|---|
| **RSK-101** | Schema evolution may break existing parsers during ingestion. | MEDIUM | HIGH | Enforce strict Pydantic versioning and schema validation at API ingress. | **MITIGATED** | Architecture | Sprint 2 |
| **RSK-201** | High latency in real-time correlation for thousands of events per second. | HIGH | CRITICAL | Implement asynchronous matching and batch DB inserts. | **OPEN** | Engineering | Sprint 6 |
| **RSK-301** | Risk scoring normalizations across diverse data sources may skew averages. | MEDIUM | MEDIUM | Define strict bounding rules (0-100) and normalization maps per source type. | **MITIGATED** | Product | Sprint 3 |
| **RSK-401** | Policy Evaluation loops might trigger circular actions if rules conflict. | LOW | HIGH | Implement strict Directed Acyclic Graph (DAG) constraints or recursion depth limits in the engine. | **OPEN** | Architecture | Sprint 7 |
| **RSK-451** | Audit Trail storage footprint will grow exponentially, potentially exhausting DB volume limits. | HIGH | MEDIUM | Implement a lifecycle policy to archive audit logs older than 90 days to cold storage. | **ACCEPTED** | DevOps | Sprint 9 |
| **RSK-501** | Querying 10,000 records dynamically causes DB latencies with standard offset pagination. | HIGH | MEDIUM | Chunked pagination implemented. Future: Keyset pagination or read-replica. | **MITIGATED** | Engineering | Sprint 6 |
| **RSK-502** | Evidence Reference counting may duplicate queries across large tables. | MEDIUM | MEDIUM | Utilize index-backed time-range queries instead of ORM instantiation. | **MITIGATED** | Engineering | Sprint 5 |
| **RSK-503** | Expanding Compliance Mapping lists (e.g., NIST, ISO) globally might drift from Report snapshots. | LOW | LOW | Mappings are instantiated as distinct entities scoped to the Report ID directly. | **MITIGATED** | Compliance | Sprint 5 |
| **RSK-504** | Missing front-end prevents any real user consumption of reports. | HIGH | MEDIUM | Output raw JSON endpoints only. Frontend integration is slated for a future phase. | **ACCEPTED** | Product | Sprint 8 |
| **RSK-505** | Scheduled reporting delivery is entirely absent. | HIGH | LOW | Build a cron-based trigger layer later using Celery or FastAPI Background Tasks. | **DEFERRED** | Engineering | Sprint 7 |
