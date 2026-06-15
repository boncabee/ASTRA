# ASTRA Sprint 3 Architecture Baseline

## Sprint 3 Scope Freeze

**In Scope**
* Authentication
* RBAC
* User Management
* Correlation Engine MVP
* Observation Engine MVP
* Risk Scoring MVP
* Policy Engine MVP
* Observation APIs
* Correlation APIs
* RBAC Middleware
* Login Screen
* Dashboard
* Events Explorer
* Observations Screen
* Observation Detail Screen
* Users Screen

**Out of Scope**
* Automation Engine
* Recovery Engine
* Case Management
* AI Gateway
* AI Providers
* SOAR Integrations
* Report Engine
* Compliance Mapping
* Playbooks
* Executive Reporting

---

## Role Definitions

ASTRA implements a strict 4-persona hierarchy:

1. **Administrator**
   * **Purpose**: Maintain platform health and access.
   * **Responsibilities**: User provisioning, system configuration, integration management, audit review.
   * **Permissions**: Full administrative access to all configuration and audit routes.
   * **Restrictions**: Cannot execute incident mitigations or modify live cases.

2. **Security Engineer**
   * **Purpose**: Manage detection and response logic.
   * **Responsibilities**: Create/tune correlation rules, manage policies, configure automation definitions.
   * **Permissions**: Edit access for Rules, Policies, and Integrations. Read access to events and observations.
   * **Restrictions**: Cannot manage users or execute rollbacks.

3. **Incident Responder**
   * **Purpose**: Analyze and resolve verified threats.
   * **Responsibilities**: Review observations, approve mitigations, manage cases, execute recoveries.
   * **Permissions**: Write/Approve access to Observations, Cases, and Mitigations. Request AI Explanations.
   * **Restrictions**: Cannot edit system policies, correlation rules, or user accounts.

4. **SOC Analyst**
   * **Purpose**: Monitor telemetry and escalate anomalies.
   * **Responsibilities**: Review raw events, validate correlations, escalate observations.
   * **Permissions**: Read access to Events and Observations. Write access to escalate observations.
   * **Restrictions**: Cannot execute/approve mitigations, manage cases, edit policies, or manage users.

---

## RBAC Matrix

| Resource Domain | Administrator | Security Engineer | Incident Responder | SOC Analyst |
| :--- | :--- | :--- | :--- | :--- |
| **Users** | Admin | None | None | None |
| **Audit Logs** | Read | Read (System) | Read (Self) | Read (Self) |
| **Events** | Read | Read | Read | Read |
| **Correlations**| Read | Write | Read | Read |
| **Observations**| Read | Read | Write | Read/Escalate |
| **Policies** | Read | Write | Read | Read |
| **Integrations**| Admin | Write | Read | None |
| **Cases** | Read | Read | Write | Read |
| **Mitigations** | Read | Configure | Approve | None |

---

## Correlation Domain Standard

* **Minimum Required Fields**:
  * `id` (UUID)
  * `rule_id` (String)
  * `status` (Enum: DETECTED, ELEVATED, DISMISSED)
  * `event_ids` (List of UUIDs linking to CES Events)
  * `audit_metadata` (Embedded model)
* **Relationships**:
  * One-to-Many with CES Events.
  * One-to-One with Observation (if elevated).
* **Storage Expectations**:
  * Stored in the relational DB. Indexed by `rule_id` and `status` for fast querying.

---

## Observation Domain Standard

* **Official Observation Lifecycle Statuses**:
  * `NEW`
  * `UNDER_REVIEW`
  * `POLICY_EVALUATED`
  * `DISMISSED`
  * `RESOLVED`

* **Transitions**:
  * `NEW` → `POLICY_EVALUATED` (via Policy Engine)
  * `POLICY_EVALUATED` → `UNDER_REVIEW` (via Responder action)
  * `UNDER_REVIEW` → `RESOLVED` (via Mitigation/Case closure)
  * `NEW` / `POLICY_EVALUATED` / `UNDER_REVIEW` → `DISMISSED`
* **Invalid Transitions**:
  * `RESOLVED` → `NEW`
  * `DISMISSED` → `UNDER_REVIEW` (Requires a new Correlation instead)

* **Minimum Required Fields**:
  * `id` (UUID)
  * `correlation_id` (UUID)
  * `status` (ObservationStatus Enum)
  * `risk_score` (Integer 0-100)
  * `policy_action` (PolicyAction Enum)
  * `audit_metadata` (Embedded model)
* **Relationships**:
  * One-to-One with Correlation.
  * One-to-One with Case (future scope).
* **Storage Expectations**:
  * Relational DB. Indexed by `status`, `risk_score`, and `policy_action`.

---

## Risk Score Standard

* **Official Scale**: Integer `0-100`
* **Categories & Exact Ranges**:
  * **INFORMATIONAL**: 0 - 19
  * **LOW**: 20 - 39
  * **MEDIUM**: 40 - 69
  * **HIGH**: 70 - 89
  * **CRITICAL**: 90 - 100

---

## Policy Domain Standard

* **Minimum Required Fields**:
  * `id` (UUID)
  * `name` (String)
  * `condition` (JSON/String logic definition)
  * `action` (PolicyAction Enum)
  * `audit_metadata` (Embedded model)
* **Relationships**:
  * Independent configuration model. Applied dynamically to Observations.
* **Storage Expectations**:
  * Cached in-memory for the Policy Engine; persisted in the relational DB.

---

## Policy Action Standard

* **Official Enum**:
  * `OBSERVE`: No automated action. Retain for analyst visibility.
  * `NOTIFY`: Send alert to configured integration (e.g., Slack, Email) or escalate in UI.
  * `REVIEW_REQUIRED`: Mandates an Incident Responder to manually authorize the next step.
  * `FUTURE_MITIGATION`: Placeholder for automated containment/remediation (out of scope for Sprint 3).

---

## Audit Metadata Standard

* **Mandatory Fields**:
  * `created_at` (Datetime, UTC)
  * `updated_at` (Datetime, UTC)
  * `created_by` (String/UUID of User or System service)
  * `updated_by` (String/UUID of User or System service)
* **Applicability**:
  * Every persistable domain model (Users, Roles, Correlations, Observations, Policies) MUST embed this metadata standard.

---

## API Naming Standard

* **REST Naming**: Strict adherence to HTTP methods (GET, POST, PUT, DELETE). No verbs in URLs.
* **Pluralization**: Resource names MUST be plural nouns (e.g., `/users`, `/observations`).
* **Resource Naming**: Use kebab-case for multi-word resources (e.g., `/audit-logs`).
* **Versioning**: Prefix all API routes with `/api/v1/`.
* **Error Format**: Standard JSON response: `{"error": "message", "code": 4xx/5xx}`.
* **Pagination Format**: Query parameters `?skip=0&limit=50`. Response MUST wrap data: `{"data": [...], "total": X}`.

---

## Frontend Route Standard

* `/login` : Unauthenticated only.
* `/dashboard` : Accessible to all authenticated roles.
* `/events` : Accessible to all authenticated roles.
* `/observations` : Accessible to all authenticated roles.
* `/observations/{id}` : Accessible to all authenticated roles.
* `/policies` : Accessible to Security Engineer and Administrator.
* `/users` : Accessible to Administrator only.

---

## Performance Baseline

* **ADR-017 Principles**:
  * **Hot Path**: Event Ingestion & Parser (must be sub-millisecond per event).
  * **Warm Path**: Correlation Engine & Policy Engine (bulk processing, allowed up to 5 seconds latency).
  * **Cold Path**: UI API queries and historical data retrieval (allowed up to 2 seconds latency).
* **Responsibilities**:
  * Event ingestion must never block UI queries. Implement database indexing for Warm/Cold paths to ensure Hot path is unimpeded.

---

## Sprint 3 Non-Goals

The following components are explicitly **Out of Scope** for Sprint 3 and must NOT be implemented or mocked into the architecture:
* **Automation**: Any active mitigation/remediation execution.
* **Recovery**: Rollback execution logic.
* **AI Gateway**: No LLM prompt routing or endpoints.
* **Case Management**: No `/cases` API or domain models.
* **Report Engine**: No PDF/CSV automated reporting.
* **SOAR**: No external Playbook orchestration integrations.

---

## Architecture Freeze Decision

**State: APPROVED**

**Justification**: This architecture baseline fully addresses `TASK-S3-ARCH-000`. It comprehensively defines all data schemas, APIs, lifecycles, and access controls required for Sprint 3 execution without introducing implementation details. Developers can now implement these explicit contracts without requiring further architectural decisions or domain model discovery.
