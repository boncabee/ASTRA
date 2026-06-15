# UI/UX Foundation
**Project:** ASTRA (Adaptive Security Threat Response & Automation Platform)

## 1. Primary Screens
The ASTRA UI is composed of several primary views designed for high-density information display:
- **Global Dashboard:** High-level metrics, active threats, and system health.
- **Observations / Threat Feed:** A real-time, filterable list of active security observations and correlations.
- **Policy Management:** A rule-builder interface for defining threat detection and response policies.
- **Evidence Explorer:** A read-only audit log interface detailing automated decisions.
- **Reporting Hub:** Interface for generating compliance and metric reports.
- **Settings & Integrations:** Configuration for external services, webhooks, and parsers.

## 2. Navigation Model
- **Persistent Left Sidebar:** Contains icons/labels for the primary screens (Dashboard, Observations, Policies, Evidence, Reports, Settings).
- **Top Bar:** Contains the global search (Search by IP, Hash, User), current User Profile / RBAC context, and contextual actions (e.g., "Export to CSV" on list views).
- **Breadcrumbs:** Used within deep-dive views (e.g., `Observations > Obs-1234 > Related Events`).

## 3. Role-Based Experience
- **Tier 1 Analyst:** Defaults to the Observation Feed. Cannot see Policy creation buttons. Evidence views are visible but cannot trigger manual re-evaluations.
- **Tier 3 Engineer:** Defaults to the Dashboard. Full access to Policy Management and Integrations.
- **Administrator:** Full access, including the User Management sub-menu under Settings.

## 4. Dashboard Concepts
- **Metrics:** "Automations Executed (24h)", "High Risk Observations (Active)", "System Latency".
- **Visuals:** Time-series charts showing ingestion volume vs. automated blocks.

## 5. Workflows

### 5.1 Observation Workflows
- **Triage:** User clicks an Observation from the feed -> Opens a split-pane view (List on left, Details on right).
- **Details Pane:** Shows Risk Score, associated CES Events, and an action button (e.g., "Trigger Manual Block" if no automation fired).

### 5.2 Policy Workflows
- **Creation:** User clicks "New Policy" -> Enters a guided form -> Defines Condition (e.g., `risk_score > 80`) -> Defines Action (e.g., `Automation: Block_IP`) -> Saves Policy.

### 5.3 Evidence Workflows
- **Auditing:** User searches by `PolicyDecision ID` or date range -> Clicks a row -> Views a read-only JSON representation of the system state at the exact time the decision was made.

### 5.4 Reporting Workflows
- **Generation:** User selects "Compliance Template" -> Selects Date Range -> Clicks "Generate" -> System async generates the report and provides a download link.

## 6. Future Workflows
- **Case Management:** Transitioning an Observation into a long-lived "Case" with notes, assignee, and external ticket sync (Jira/ServiceNow).
- **Automation Playbook Builder:** A visual node-based editor for linking multiple automation actions (e.g., Block IP -> Disable AD Account -> Send Slack Alert).
