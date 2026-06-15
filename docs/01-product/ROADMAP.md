# ASTRA Roadmap V2

## Executive Summary & Recommendation
Following the Phase 5.5 Architecture and Product Reviews, ASTRA has achieved a stable, highly-tested foundation capable of supporting advanced workflows.

**Recommendation:** **Proceed to Automation (Phase 6)**, but **Pause for Hardening** immediately afterward before tackling AI/SaaS features. 
The backend architecture is structurally sound for the Automation Engine, but the Technical Debt (specifically the lack of async workers, TD-003) must be resolved simultaneously or immediately following Phase 6 to prevent performance cascading failures.

---

## Phase 6: Automation Foundation (Next Up)
**Focus:** Converting Policy Evaluation outputs into actionable automated responses.
- Implement the `AutomationEngine` to execute actions (e.g., API calls, webhook dispatches).
- Implement basic `Integration` stubs for ticketing and firewall blocking.
- *Hardening Action:* Introduce an async task worker queue (e.g., Celery) to offload synchronous policy and automation execution.

## Phase 7: Recovery & Case Management
**Focus:** Human-in-the-loop workflows and incident tracking.
- Build the `Case` domain model, linking `Observations` and `Automations` to a human-assigned incident.
- Implement workflow states (Open, Investigating, Remediated, Closed).
- Expose endpoints for analysts to manually trigger recovery or rollback actions.

## Phase 8: Integrations Expansion
**Focus:** Broadening the ecosystem to connect with real-world enterprise tooling.
- Enterprise SSO (SAML/OIDC) Integration for Identity.
- Build native connectors for standard tools (Jira, Slack/Teams, SentinelOne, CrowdStrike).
- Create a visual or declarative playbook schema for custom integrations.

## Phase 9: AI Enablement (Adaptive Intelligence)
**Focus:** Introducing the "Adaptive Security" components.
- Integrate the AI Gateway to abstract provider dependencies (e.g., Gemini, OpenAI).
- Implement AI-driven timeline generation from raw `Evidence` payloads.
- Enable automated narrative drafting for `Reports`.
- *Constraint:* AI must remain an *enhancement*, not a structural dependency for rules or correlations to fire.

## Phase 10: Compliance & UI Deployment
**Focus:** Presenting the data and satisfying advanced GRC requirements.
- Build out the React/Next.js Frontend Dashboard.
- Provide interactive visualizations for Correlation graphs and Attack trees.
- Expand Compliance Mappings into an active evaluation engine (reporting drift against baselines).

## Phase 11: SaaS Readiness & Multi-Tenancy
**Focus:** Evolving from a single-tenant enterprise deployment to a cloud-native SaaS.
- Refactor the database schema to include `tenant_id` on all core models.
- Implement strict tenant data isolation at the ORM layer.
- Build billing and utilization metrics aggregation.
