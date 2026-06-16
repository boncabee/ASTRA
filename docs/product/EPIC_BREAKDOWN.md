# Epic Breakdown

This document maps the ASTRA Roadmap into persistent, high-level Epics. These Epics serve as the highest organizational layer for tracking features and capabilities over time.

## Active Epics

### EPIC-01: Identity & Access (RBAC)
**Scope:** Authentication, Role-Based Access Control, session management, and enterprise SSO integrations (SAML/OIDC).
**Current State:** Basic JWT and local RBAC implemented.
**Future Work:** Multi-factor authentication, granular resource-level permissions, Azure AD / Okta integrations.

### EPIC-02: Correlation Engine
**Scope:** Ingestion of CES Events, spatial and temporal grouping, and relationship mapping.
**Current State:** Foundational correlation logic implemented.
**Future Work:** Graph-based correlation, cross-tenant correlation (for SaaS), advanced temporal windowing.

### EPIC-03: Observation Engine
**Scope:** Threat intelligence mapping, risk scoring, and dynamic observation lifecycle management.
**Current State:** MVP Risk Scoring and REST APIs implemented.
**Future Work:** Dynamic risk decay, integration with external threat feeds (e.g., MISP, VirusTotal).

### EPIC-04: Policy Engine
**Scope:** Deterministic rule evaluation, condition mapping, and triggering automated or manual actions.
**Current State:** Foundational evaluation implemented.
**Future Work:** UI-based policy builder, complex boolean logic (AND/OR trees), scheduled policy execution.

### EPIC-05: Evidence & Audit
**Scope:** Immutable persistence of system decisions, audit logging, and cryptographic chain-of-custody.
**Current State:** Append-only evidence repository implemented.
**Future Work:** Blockchain/DLT anchoring, export for legal hold.

### EPIC-06: Reporting & Compliance
**Scope:** Data aggregation, compliance framework mapping (e.g., SOC2, GDPR), and metric generation.
**Current State:** Basic reporting API implemented.
**Future Work:** PDF/CSV export, real-time compliance drift dashboards.

### EPIC-07: Automation
**Scope:** Asynchronous task queues, background workers, and execution of deterministic actions.
**Current State:** Task queue foundation implemented.
**Future Work:** Advanced retry mechanics, circuit breakers, visual playbook builder.

### EPIC-08: Case Management
**Scope:** Human-in-the-loop incident response, ticket tracking, and analyst workflows.
**Current State:** Not started.
**Future Work:** Incident states, collaborative notes, SLA tracking.

### EPIC-09: Integrations
**Scope:** Adapters and connectors to external enterprise tools (e.g., Firewalls, EDRs, SIEMs).
**Current State:** Mock integrations for webhooks and tickets.
**Future Work:** SentinelOne, CrowdStrike, Jira, Slack, Palo Alto native plugins.

### EPIC-10: AI Enablement
**Scope:** Utilizing LLMs and ML models for advanced threat detection and narrative generation, strictly as an enhancement layer.
**Current State:** Not started.
**Future Work:** AI Gateway abstraction, narrative generation for Evidence, anomaly detection models.

### EPIC-11: SaaS Readiness
**Scope:** Multi-tenancy, data isolation, billing, and horizontal scalability.
**Current State:** Architecture designed for single-tenant enterprise.
**Future Work:** Tenant-aware ORM filtering, usage metering, specialized deployment topologies.
