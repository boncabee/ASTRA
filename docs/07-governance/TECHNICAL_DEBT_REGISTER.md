# Technical Debt Register

## Overview
This document consolidates all known technical debt accumulated during ASTRA Phases 1 through 5. Addressing these items is crucial before scaling ASTRA to a SaaS or high-volume enterprise deployment.

## Debt Items

| Debt ID | Category | Description | Impact | Priority | Suggested Sprint |
|---|---|---|---|---|---|
| **TD-001** | Database/Performance | `offset`/`limit` pagination becomes inefficient with millions of rows in `observations` and `reports`. Requires cursor-based pagination or keyset pagination. | Medium | Medium | Sprint 6 |
| **TD-002** | Testing | Test suite uses `sqlite+aiosqlite` in-memory. This masks PostgreSQL-specific syntax errors (e.g., JSONB querying differences). | High | High | Sprint 6 |
| **TD-003** | Architecture/Async | No dedicated background worker (e.g., Celery/Redis). Large report generations or policy evaluations currently run in the main FastAPI event loop context or simple await chains, risking timeout under heavy load. | Critical | High | Sprint 7 |
| **TD-004** | Security/RBAC | Global dependency overrides for `RequireRoles` proved brittle during Phase 5 testing. RBAC logic should be consolidated into a cleaner middleware or explicit route-level declarative model. | Medium | Medium | Sprint 7 |
| **TD-005** | UI/UX | Complete lack of frontend. All data consumption requires API interactions, severely limiting analyst usability. | Critical | Critical | Sprint 8 |
| **TD-006** | Database/Storage | Evidence and Audit models currently store JSON variants and hashes inline. As volume scales, `evidence` table will balloon, requiring partitioning strategies. | Medium | Low | Sprint 9 |
| **TD-007** | Integration | "Automation Engine" and external ticketing systems are completely stubbed out. No real webhook validation or API integration exists for mitigation actions. | High | High | Sprint 6 |


# Open Findings

| Finding ID | Description | Status | Target Sprint | Resolution Task | Notes |
|---|---|---|---|---|---|
| PF-001 | Batch Transformation | Open | 2 | | |
| PF-003 | Fallback Mapping | Open | 2 | | |
| PF-004 | Parser SDK Documentation | Open | 2 | | |
| PF-005 | Parser Registry Plugin Auto-discovery | Open | Future | | Consider dynamic parser auto-discovery |
\n| ARCH-001 | Realignment requires architecture updates | Closed | 3 | Realignment | |\n


