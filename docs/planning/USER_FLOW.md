# ASTRA User Flow Document

## Executive Summary
This document defines the comprehensive user and system flow for the **Adaptive Security Threat Response & Automation (ASTRA) Platform**. ASTRA operates on the principle of AI-enhanced, observation-based threat response. The platform does not generate alerts directly; instead, it processes telemetry through a rigorous pipeline: Telemetry → Parser → CES (Common Event Schema) → Correlation → Observation → Risk Scoring → Policy Evaluation → Action. All actions prioritize recovery, and AI serves strictly in an advisory capacity (explaining, summarizing, recommending, and analyzing) without execution authority. This document serves as the foundation for frontend design, backend API planning, and Sprint 3 execution.

## Role Definitions
ASTRA serves four primary personas, listed in order of workflow priority:
1. **Incident Responder**: Handles high-fidelity observations, executes mitigations, and manages incident cases.
2. **SOC Analyst**: Reviews raw events, analyzes correlations, and escalates observations.
3. **Security Engineer**: Configures rules, policies, and automation playbooks.
4. **Administrator**: Manages the platform, integrations, system health, and user access.

---

## Incident Responder Journey
**Goal**: Swiftly resolve verified threats through observation analysis, mitigation, and case management.

**Start**: Observation Created  
**End**: Case Closed

### Daily Workflow & Step-by-Step Flow
1. **Observation Review**: The Responder receives a new Observation with a pre-calculated Risk Score. They review the context, timeline, and correlated CES events.
2. **AI Explanation Usage**: The Responder requests an AI summary of the observation to understand complex attack patterns. The AI explains the threat but does not execute actions.
3. **Risk Review**: The Responder validates the Risk Score against the organization's current threat landscape.
4. **Mitigation Review**: The platform proposes an automated or manual mitigation based on Policy Evaluation.
5. **Approval Workflow**: If the recommended remediation requires approval, the Responder reviews the action details and authorizes the execution.
6. **Execution & Case Creation**: The action is executed. A Case is created to track the incident.
7. **Recovery Workflow**: The Responder monitors the mitigation. If an error is detected or the mitigation causes operational disruption, the Responder initiates a rollback/recovery action.
8. **Case Closure**: The Responder documents findings, updates the case, and closes it.

---

## SOC Analyst Journey
**Goal**: Monitor the environment, validate correlations, and escalate true positive observations.

### Daily Workflow
1. **Event Review**: The Analyst monitors parsed CES events for anomalies that have not yet formed correlations.
2. **Correlation Review**: The Analyst investigates emerging correlations to determine if they indicate a coordinated attack.
3. **Observation Analysis**: Once an Observation is generated, the Analyst performs a preliminary investigation into the evidence.
4. **Escalation Path**: If the Observation is deemed a high-risk threat, the Analyst escalates it to an Incident Responder or tags it for automated policy evaluation.

---

## Security Engineer Journey
**Goal**: Maintain the detection and automated response capabilities of the platform.

### Daily Workflow
1. **Correlation Rule Management**: The Engineer creates, tests, and tunes correlation rules to ensure high-fidelity observations.
2. **Policy Management**: The Engineer defines the Policy Evaluation logic that dictates when an Observation should trigger an Observe, Notify, Create Case, Mitigate, or Remediate action.
3. **Automation Configuration**: The Engineer configures the Automation Engine, defining the specific API calls and scripts used for mitigation.
4. **Playbook Management (Future)**: The Engineer designs complex, multi-step playbooks for orchestrated response.

---

## Administrator Journey
**Goal**: Ensure platform availability, security, and integration health.

### Daily Workflow
1. **User Management & RBAC**: The Administrator provisions accounts and assigns roles based on the Permission Matrix.
2. **AI Provider Configuration**: The Administrator configures connections to external AI gateways, sets rate limits, and monitors AI token usage.
3. **Integration Management**: The Administrator manages API keys and connections to firewalls, EDRs, and other telemetry sources.
4. **System Health**: The Administrator monitors parser throughput, database performance, and pipeline latency.
5. **Audit Review**: The Administrator reviews system audit logs to ensure compliance and track recovery actions.

---

## Screen Inventory

### Core Platform
* **Login**: SSO and MFA entry point.
* **Dashboard**: High-level metrics, active cases, recent observations, and system health.
* **Events Explorer**: Search and filter raw CES events.
* **Observations**: Kanban or list view of active, pending, and resolved observations.
* **Observation Detail**: Deep-dive into a specific observation, including AI explanations, evidence graph, and mitigation options.
* **Cases**: Incident management workspace.
* **Case Detail**: Notes, timeline, evidence attachments, and closure options.

### Configuration & Management
* **Policies**: Rule and policy builder for the Policy Engine.
* **Correlations**: Interface for defining event correlation logic.
* **Integrations**: Telemetry and response integration management.
* **AI Providers**: Configuration for AI models and prompts.
* **Settings**: Global platform configurations.
* **Users**: User and RBAC management.
* **System Health**: Infrastructure monitoring dashboard.
* **Audit Logs**: Immutable log of user and system actions.

---

## Navigation Model

### Main Navigation
* Dashboard
* Observations
* Cases
* Events Explorer

### Secondary Navigation
* Policies & Correlations
* Integrations
* Users
* System Health
* Audit Logs
* Settings (includes AI Providers)

### Role-Based Navigation
* **Incident Responder**: Primary focus on Observations and Cases.
* **SOC Analyst**: Primary focus on Dashboard and Events Explorer.
* **Security Engineer**: Primary focus on Policies, Correlations, and Integrations.
* **Administrator**: Primary focus on Users, System Health, Audit Logs, and Settings.

---

## Observation Workflow

`Observation Created`
↓
`Risk Score Generated`
↓
`Policy Evaluated`
↓
`Recommended Action`
↓
`Mitigation` (Automatic or Manual)
↓
`Approval` (If required for Remediation)
↓
`Remediation` Executed
↓
`Recovery` (If needed)

---

## Case Workflow

`Case Created` (From Observation or Manual)
↓
`Investigation` (Reviewing linked events and AI summaries)
↓
`Evidence Collection` (Tagging related logs)
↓
`Decision` (Mitigate, Remediate, or Dismiss)
↓
`Closure` (Documenting outcome)

---

## Recovery Workflow

`Action Executed` (e.g., Block IP)
↓
`Error Detected` (e.g., Critical service blocked)
↓
`Rollback Available` (System checks for recovery steps)
↓
`Recovery Executed` (e.g., Unblock IP)
↓
`Audit Recorded` (Logged in immutable Audit Logs)

---

## AI Interaction Workflow

`User` (e.g., Incident Responder)
↓
`Request Explanation` (Action initiated in UI)
↓
`AI Gateway` (Internal routing and prompt formatting)
↓
`Provider` (External LLM)
↓
`Response` (Summary/Recommendation displayed)

*Note: AI is advisory only. It cannot approve, authorize, remediate, or execute actions.*

---

## Permission Matrix

| Feature / Action | Incident Responder | SOC Analyst | Security Engineer | Administrator |
| :--- | :--- | :--- | :--- | :--- |
| **View Events** | Yes | Yes | Yes | Yes |
| **View Observations**| Yes | Yes | Yes | Yes |
| **Escalate Obs.** | Yes | Yes | Yes | No |
| **Execute Mitigation**| Yes | No | Yes | No |
| **Approve Remediation**| Yes | No | Yes | No |
| **Manage Cases** | Yes | View Only | View Only | View Only |
| **Execute Recovery** | Yes | No | Yes | Yes |
| **Request AI Expl.** | Yes | Yes | Yes | Yes |
| **Edit Policies** | No | No | Yes | No |
| **Edit Integrations**| No | No | Yes | Yes |
| **Manage Users** | No | No | No | Yes |
| **View Audit Logs** | View Personal | View Personal | View System | Full Access |

---

## UX Risks

1. **Complexity Risks**: Displaying too much raw event data on the Observation Detail screen may overwhelm Responders. *Mitigation: Use progressive disclosure and AI summaries.*
2. **Approval Bottlenecks**: Remediation approvals may delay critical responses. *Mitigation: Clearly highlight pending approvals and offer bulk approval for related observations.*
3. **Automation Risks**: Users may mistrust automated mitigations. *Mitigation: Clearly define the Policy Evaluation logic that triggered the automation.*
4. **Recovery Risks**: Rollback actions may fail, leaving the system in an inconsistent state. *Mitigation: Ensure the UI clearly indicates recovery status and offers manual fallback instructions.*
5. **AI Misuse Risks**: Users may over-rely on AI summaries and skip verifying evidence. *Mitigation: Always present the raw evidence alongside the AI summary, clearly marking AI output as "Advisory."*

---

## Product Gaps

Based on the current architecture and this flow, the following are not yet implemented:
1. **Frontend Repository**: No React/Vue application exists yet.
2. **API Layer**: The backend API routes for the Screen Inventory are not defined.
3. **RBAC Service**: The authorization middleware to enforce the Permission Matrix is missing.
4. **AI Gateway integration**: The connection to external AI providers is conceptual.
5. **Recovery Engine**: The technical mechanism to execute rollbacks is undefined.

---

## Recommendations

### Immediate (Pre-Sprint 3)
* Finalize the API specifications required to support the Main Navigation and Observation Workflow.
* Select a frontend framework and initialize the repository.

### Sprint 3
* Develop the core Observation and Case views.
* Implement the RBAC middleware and User Management screens.
* Build the Events Explorer for the SOC Analyst.

### Sprint 4+
* Integrate the AI Gateway for the AI Interaction Workflow.
* Implement the Recovery Workflow and Rollback UI.
* Develop the Policy and Correlation rule builders for the Security Engineer.

---

## Final Decision

**Is ASTRA user experience ready for Sprint 3?**

**PASS**

The user flow is clearly defined, aligns with the newly approved architecture, and provides sufficient detail to drive frontend design, API planning, and RBAC implementation without requiring further user-flow discovery.