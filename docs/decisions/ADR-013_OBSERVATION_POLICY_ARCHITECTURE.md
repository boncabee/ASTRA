# ADR-013: Observation & Policy Architecture

**Context:** The existing simplistic model (Correlation -> Alert) does not provide enough actionable nuance or policy flexibility.
**Decision:** Transition the platform model to: Correlation -> Observation -> Risk Scoring -> Policy Evaluation -> Action.
**Rationale:** This evidence-based recommendation architecture aligns with the goal of translating telemetry into explainable, policy-driven decisions without directly relying on user feedback to learn "truth".
**Status:** Accepted