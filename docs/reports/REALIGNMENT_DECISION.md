# ASTRA Realignment Decision

**Date:** 2026-06-14
**Phase:** Pre-Sprint 3

## Strategic Changes
* Pivot from an "AI-first investigation platform" to an "Adaptive Security Threat Response & Automation Platform."
* AI is repositioned as an enhancement, not a core runtime dependency.

## Architectural Changes
* Introduction of the Observation Engine, Policy Engine, and Automation Engine.
* Introduction of the AI Gateway and AI Provider Abstraction Layer.

## Product Changes
* User persona priority shifted to: Incident Responder > SOC Analyst > Security Engineer > Administrator.
* Workflow emphasizes: Correlation -> Observation -> Risk Scoring -> Policy Evaluation -> Action.

## Risks
* Increased architectural complexity with the introduction of multiple new engines (Observation, Policy, Automation) simultaneously.
* The design of the Policy Engine requires rigorous logic to prevent automated destructive actions (e.g., unintended isolation).

## Open Questions
* None at this time. Architecture Review has resolved previous ambiguities regarding AI learning models.

## Sprint 3 Readiness
* All project plan, roadmap, PRD, and architecture documentation have been updated to reflect the new direction without contradictions.
* Sprint 3 objectives have been successfully adjusted to focus on RBAC, Correlation Engine, Observation Engine, and Policy Engine.

---

**Final Decision:** READY FOR USER_FLOW