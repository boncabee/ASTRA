# ADR-011: Authentication & RBAC

**Context:** The system must support multiple personas with varying levels of access and priorities.
**Decision:** Implement robust RBAC supporting the following priority order: Incident Responder, SOC Analyst, Security Engineer, and Administrator.
**Rationale:** Incident Response workflows are the primary design driver, requiring dedicated access control logic.
**Status:** Accepted