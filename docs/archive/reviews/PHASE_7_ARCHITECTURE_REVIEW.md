# Phase 7 Architecture Review: Case Management

**Date:** 2026-06-16
**Status:** Complete
**Reviewer:** ASTRA Solution Architect

## 1. Architecture Assessment
The Case Management architecture successfully decouples the human-triage workflow from the deterministic processing pipelines (Ingestion, Correlation, Policy). The domain is properly structured around the `Case` aggregate root, and the strictly enforced state machine guarantees linear, auditable resolution tracking.

## 2. Risk Assessment
- **Risk:** Rapid case generation by the Policy Engine could overwhelm Analysts (Alert Fatigue).
- **Mitigation:** Rely on Phase 2 Correlation and Phase 4 Policy Engines to pre-filter noise. Only high-confidence Observations trigger auto-creation.

## 3. Scalability Assessment
The schema design isolates immutable `Case Timeline` records and `Case Evidence Links` from the mutable `Case` entity. This ensures that querying open cases remains fast even as the timeline ledger grows to millions of rows. RDBMS partitioning by `created_at` on the Timeline table will ensure long-term stability.

## 4. Security Assessment
The design respects the overarching security tenets of ASTRA. The Case Service cannot mutate Evidence. It operates strictly within the boundaries of the API Gateway, which guarantees that all incoming requests possess a valid JWT.

## 5. RBAC Assessment
Roles are explicitly defined from `Viewer` to `Admin`. The architecture mandates `RequiresRole()` dependency injection on all routes. The distinction between `Analyst` (standard resolution) and `Responder` (override and escalation) provides adequate segregation of duties.

## 6. Automation Assessment
Integration with Phase 6 is seamless via the Message Bus. The enforcement of "Approval Checkpoints" guarantees that automated mitigations triggered from the Case UI adhere to the "human-in-the-loop" requirement for critical infrastructure changes.

## 7. Reporting Assessment
By generating metrics (MTTA, MTTR) from the immutable Timeline rather than mutable state columns, the Phase 5 Reporting Engine is guaranteed cryptographically accurate data for SLA compliance.

## 8. Future AI Assessment
The architecture clearly establishes the boundaries for AI integration (Phase 8+). The `TimelineService` and `CaseService` are strictly deterministic. The AI Reasoner will act as an async sidecar, reading data to provide recommendations, without the permission to close cases or override human input.

## 9. Implementation Risks
- Transitioning the Phase 6 webhook payload to cleanly map back to the Case Timeline requires careful JSON schema validation to avoid parsing errors.
- Implementing PostgreSQL Row-Level Security (RLS) for multi-tenant viewing may introduce query latency if not properly indexed by `assigned_to` and `status`.

## 10. Recommendations
- Proceed with Phase 7 Implementation.
- During Sprint 1, prioritize the Database Models and the Timeline Service to ensure the immutable foundation is flawless before building the FastAPI routers.

## 11. Final Decision
**GO FOR PHASE 7 IMPLEMENTATION.**
