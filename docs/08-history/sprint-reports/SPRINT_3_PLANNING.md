# ASTRA Sprint 3 Planning Package

## Sprint Goal
Deliver the first end-to-end operational ASTRA workflow:
Telemetry → CES → Correlation → Observation → Risk Scoring → Policy Evaluation → User Interface

## Scope Definition
**IN SCOPE**
* Authentication
* RBAC (Role-Based Access Control)
* User Management
* Correlation Engine MVP
* Observation Engine MVP
* Risk Scoring MVP
* Policy Engine MVP
* Observation APIs
* Correlation APIs
* RBAC Middleware
* UI: Login Screen, Dashboard, Events Explorer, Observations Screen, Observation Detail Screen, Users Screen

**OUT OF SCOPE**
* Automation Engine
* Recovery Engine
* Case Management
* AI Gateway & AI Providers
* SOAR Integrations
* Report Engine & Compliance Mapping
* Playbooks
* Executive Reporting

---

## Phase Execution Plan

### Phase 1: Authentication & RBAC
* **Objectives**: Secure access to the ASTRA platform based on the 4 defined personas.
* **Deliverables**: Auth Service, RBAC Middleware, User Management DB Schema.
* **Dependencies**: User DB Schema.
* **Risks**: High complexity in securing API endpoints.
* **Success Criteria**: System can validate users and issue persona-based JWTs. Middleware successfully blocks unauthorized endpoints.
* **Estimated Complexity**: Medium

### Phase 2: Correlation Engine (MVP)
* **Objectives**: Process CES events and group them into incident candidates based on rules.
* **Deliverables**: Correlation Engine, Correlation DB Schema, Basic static rule definitions.
* **Dependencies**: CES Schema (completed in Sprint 1), Event Pipeline.
* **Risks**: Performance bottlenecks querying large volumes of CES data.
* **Success Criteria**: Engine groups related CES events matching a sample correlation rule.
* **Estimated Complexity**: High

### Phase 3: Observation Engine & Risk Scoring (MVP)
* **Objectives**: Elevate grouped events into an actionable Observation and assign a risk score.
* **Deliverables**: Observation Engine, Risk Scoring module, Observation APIs.
* **Dependencies**: Phase 2 (Correlation Engine).
* **Risks**: Logic for risk score calculation might require extensive tuning.
* **Success Criteria**: Observations are generated from correlated events and assigned an accurate numeric Risk Score.
* **Estimated Complexity**: High

### Phase 4: Policy Engine (MVP)
* **Objectives**: Evaluate Observations and Risk Scores to recommend a required action.
* **Deliverables**: Policy Engine, basic static policy set (e.g., if risk > 80, recommend Notify).
* **Dependencies**: Phase 3 (Observation Engine).
* **Risks**: Policy syntax and storage design could become overly complex.
* **Success Criteria**: Policies consistently evaluate generated Observations and output the correct Recommended Action.
* **Estimated Complexity**: Medium

### Phase 5: Frontend Integration
* **Objectives**: Connect the backend pipeline to the user interfaces defined in USER_FLOW.md.
* **Deliverables**: Login Screen, Dashboard, Events Explorer, Observations Screen, Observation Detail Screen, Users Screen.
* **Dependencies**: Phases 1, 3, and 4 (Auth, Observation APIs).
* **Risks**: API contracts might shift, requiring rework in frontend components.
* **Success Criteria**: End users can log in and view their persona-specific dashboards and observations.
* **Estimated Complexity**: High

### Phase 6: Testing & Stabilization
* **Objectives**: Ensure the end-to-end flow is robust and performant.
* **Deliverables**: E2E tests, Unit test coverage updates, Performance benchmarks.
* **Dependencies**: Phases 1-5.
* **Risks**: Discovering architectural gaps during E2E testing.
* **Success Criteria**: A single piece of telemetry can be traced completely from ingestion through to display in the UI without error.
* **Estimated Complexity**: Medium

---

## Final Decision

**Is Sprint 3 ready to execute?**
**YES**

**Justification**: 
The core pipeline logic (Parser/CES) is solid from Sprints 1 and 2. The Product Realignment, Architecture Realignment, and User Flow are completely approved and documented. This provides absolute clarity on what the UI and API surfaces must deliver. There are no remaining ambiguity blockers to begin breaking down specific tasks for Auth, Correlation, Observation, and Frontend development.
