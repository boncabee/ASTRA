# Phase 16 Report: Operator Experience Design

## 1. Findings
ASTRA's backend is fully Production Ready, but the frontend currently exists only as a scaffold (`Phase UI UX Readiness Assessment: NOT USABLE`). To transition ASTRA from a headless API-driven platform to a usable Enterprise-Grade Self-Hosted security tool, a complete operator experience must be designed. Building frontend components without a formalized UX plan leads to inconsistent navigation, poor information architecture, and wasted engineering effort.

## 2. Root Cause
N/A - This phase represents a proactive design step preceding frontend implementation (Phase 10 / Phase 16).

## 3. Plan (Operator Experience Design)

### 3.1. Personas
The primary user of ASTRA is the **Security Operator**. We define two distinct sub-personas for the Enterprise-Grade Self-Hosted environment:
1. **Tier 1 SOC Analyst**: Focuses on the "Cases" and "Alerts" queues. Their goal is speed—quickly triaging incoming observations, confirming or dismissing them, and executing predefined automations.
2. **Security Engineer (Admin)**: Focuses on "Policies", "Automations", "Monitoring", and "Settings". Their goal is systemic stability—tuning rules to reduce false positives, creating integrations, and managing system health.

### 3.2. Daily Workflow
1. **Login**: Operator authenticates via local credentials or SSO (future).
2. **Dashboard Overview**: Reviews system health, active critical cases, and unassigned alerts.
3. **Case Triage**: Operator navigates to the "Cases" queue, claims an unassigned case, and begins investigation.
4. **Evidence Review**: Operator drills down into the "Observations" linked to the case to understand the timeline.
5. **Action/Resolution**: Operator executes manual "Automations" (e.g., Block IP) and transitions the Case state to "Closed".

### 3.3. Dashboard Design
The global dashboard is the landing page (`/dashboard`), split into two domains:
- **Top Row (Operational Health)**: API Uptime, Automation Queue length, System Error count.
- **Main View (Security Posture)**: Open Cases by Severity (P0, P1), Unassigned Alerts count, and a sparkline of ingestion volume over the last 24 hours.

### 3.4. Navigation Structure
A vertical left-hand sidebar layout provides persistent access to core domains:
- **Dashboards**: Global overview and metrics.
- **Operations**:
  - **Cases**: Grouped investigations.
  - **Alerts**: Policy breaches pending case assignment.
  - **Observations**: Raw, correlated telemetry data.
- **Engineering**:
  - **Policies**: Rule definitions and logic editors.
  - **Automations**: Webhooks, integrations, and action logs.
- **System**:
  - **Monitoring**: Links to Grafana/Prometheus views or embedded metrics.
  - **Settings**: User management, system configuration, RBAC.

### 3.5. Screen Inventory
1. **Authentication** (`/login`)
2. **Dashboard** (`/dashboard`)
3. **Cases List** (`/cases`)
4. **Case Detail** (`/cases/[id]`) - Includes Timeline, Evidence, and Action pane.
5. **Alerts List** (`/alerts`)
6. **Observations Explorer** (`/observations`) - Table view with robust filtering.
7. **Policies List** (`/policies`)
8. **Policy Editor** (`/policies/[id]`)
9. **Automations List** (`/automations`)
10. **Settings** (`/settings`)

### 3.6. User Flows (Critical Journeys)
- **Journey 1: Triage to Closure**
  `Dashboard` -> clicks "3 Critical Cases" -> `Cases List` -> clicks Case 101 -> `Case Detail` -> reviews timeline -> clicks "Block IP" -> clicks "Close Case" -> returns to `Cases List`.
- **Journey 2: Policy Tuning**
  `Alerts List` -> notices False Positive spam -> clicks related Policy -> `Policy Editor` -> adjusts regex/threshold -> saves -> returns to `Alerts List`.

### 3.7. Implementation Roadmap
Frontend development will be sequenced logically based on API dependencies.
- **MVP Screens (Sprint 1-2)**: Authentication, Dashboard (Static/Basic Metrics), Cases List, Case Detail, Observations Explorer. These screens unlock the Tier 1 Analyst workflow.
- **Post-MVP Screens (Sprint 3-4)**: Policy Editor, Automations configuration, advanced Monitoring embeds, Settings. These unlock the Security Engineer workflow.

## 4. Changes
- **Created**: `docs/history/phase-reports/PHASE_16_OPERATOR_EXPERIENCE_DESIGN.md` establishing the UX foundation prior to writing any React code.

## 5. Validation
- The design strictly aligns with the existing ASTRA backend entities (Cases, Observations, Policies, Automations).
- It adheres to the Enterprise-Grade Self-Hosted constraint (focusing on local operations, omitting multi-tenant SaaS elements).
- No UI code was implemented; the design phase is completely isolated.

## 6. Documentation Updates
- `docs/history/phase-reports/PHASE_16_OPERATOR_EXPERIENCE_DESIGN.md`

## 7. Risks (UX Risks)
- **Data Overload**: Observations can reach thousands per minute. If the `Observations Explorer` does not implement robust server-side pagination and filtering immediately, the browser will crash.
- **State Strikethrough**: If multiple operators view the same case, real-time status updates (WebSockets) are required to prevent duplicate effort. For the MVP, manual refresh or simple polling must be used, which carries a risk of race conditions.

## 8. Recommendations
1. **Proceed to Implementation**: The frontend engineering team should select a component library (e.g., shadcn/ui) and begin executing the **MVP Screens** defined in the implementation roadmap.
2. **Mock First**: Build the Case Detail view with static mock data first to validate the layout before hooking it up to the live `fastapi` backend.
