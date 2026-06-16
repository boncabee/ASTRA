# Case Role-Based Access Control (RBAC) Model

**Phase:** 7
**Project:** ASTRA

## 1. Core Principles
The Case Management module integrates seamlessly with ASTRA's existing RBAC framework. Permissions are granted via JWT claims validated at the API Gateway layer before reaching the Case Service.

## 2. Role Definitions

| Role | Scope / Description |
| :--- | :--- |
| **Viewer** | Auditor or external stakeholder. Read-only access to specific, sanitized cases. |
| **Analyst** | Tier 1/2 operator. Triage, investigate, and resolve standard cases. |
| **Responder** | Tier 3 operator. Access to advanced mitigation and manual automation overrides. |
| **Manager** | SOC lead. Queue management, reassignment, QA, and final case closure. |
| **Administrator** | System admin. Global access, primarily for system configuration, not case handling. |

## 3. Permissions Matrix

The following actions define the exact permissions enforced by the API endpoints.

| Action | Viewer | Analyst | Responder | Manager | Admin |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **View Cases** | Self/Assigned | All | All | All | All |
| **Create Cases** | No | Yes | Yes | Yes | Yes |
| **Assign (Self)**| No | Yes | Yes | Yes | Yes |
| **Assign (Others)**| No | No | Yes | Yes | Yes |
| **Comment** | No | Yes | Yes | Yes | Yes |
| **Change Status**| No | Yes* | Yes* | Yes | Yes |
| **Close Case** | No | No | No | Yes | Yes |
| **Cancel Case** | No | No | Yes | Yes | Yes |
| **Trigger Auto.**| No | No | Yes | Yes | Yes |
| **Delete Case** | No | No | No | No | Yes** |
| **Export Case** | Yes | Yes | Yes | Yes | Yes |

*\*Analysts and Responders can change status up to `Resolved`. Only Managers/Admins can transition to `Closed`.*
*\*\*Deletion is inherently a "soft delete" or archival action. Hard deletions are forbidden to preserve the audit trail.*

## 4. Enforcement Layer
- **Endpoint Security:** Every FastAPI route in the Case Service must be decorated with the `RequiresRole()` dependency injected from the Identity Foundation (Phase 1).
- **Row-Level Security (RLS):** For multi-tenant or departmental configurations, PostgreSQL RLS will be utilized to ensure Users can only `View Cases` associated with their specific organizational unit or assigned scope.
