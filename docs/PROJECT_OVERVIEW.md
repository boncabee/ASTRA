# Project Overview
**Project:** ASTRA (Adaptive Security Threat Response & Automation Platform)

## Executive Summary
ASTRA is an advanced, deterministic security event processing platform. Designed to sit at the core of a modern Security Operations Center (SOC), ASTRA bridges the gap between raw data ingestion and active threat mitigation. It provides high-throughput parsing, intelligent correlation, strict policy enforcement, and asynchronous automation execution—all while maintaining an immutable, cryptographically secure chain of evidence.

## Core Philosophy: Determinism Over AI Dependency
While ASTRA incorporates AI as a powerful enhancement tool for complex correlations and dynamic analysis, the core system is engineered to be **deterministic**. This means that if AI services become degraded or unavailable, ASTRA will continue to ingest events, evaluate rule-based policies, and execute critical automations without interruption.

## The ASTRA Lifecycle
1. **Ingest (Parser Framework):** Ingest raw telemetry from diverse sources (Firewalls, VPNs, Endpoints) and standardize it into the Common Event Schema (CES).
2. **Correlate (Observation Engine):** Group related CES events temporally and spatially to identify emerging threats, dynamically assigning an aggregate Risk Score.
3. **Decide (Policy Engine):** Evaluate Observations against user-defined, RBAC-protected policies to deterministically decide if action is required.
4. **Audit (Evidence Engine):** Persist a point-in-time, immutable snapshot of the entire decision context for future compliance and investigation.
5. **Act (Automation Engine):** Asynchronously dispatch response tasks (e.g., block an IP, suspend an account, open a ticket) to background workers.

## Target Audience
- **Tier 1/2 Analysts:** Utilize ASTRA to view pre-correlated, high-confidence observations rather than sifting through raw noise.
- **Tier 3 Engineers:** Build complex detection logic and wire up new automation integrations.
- **Operations & Compliance:** Rely on ASTRA's sub-500ms latency, high availability, and unalterable evidence logs.

## Navigation Guide
- **`01-product/`**: Roadmap, features, and user journeys.
- **`02-requirements/`**: System requirements (SRS), security, and compliance constraints.
- **`03-architecture/`**: Technical design (SDD), database schemas, APIs, and Architecture Decision Records (ADRs).
- **`04-ui-ux/`**: Design concepts, screen flows, and future dashboard mockups.
- **`05-engineering/`**: Coding standards, testing strategies, and contributor guidelines.
- **`06-operations/`**: Deployment guides and incident runbooks.
- **`07-governance/`**: Decision logs, risk registers, and documentation standards.
- **`08-history/`**: Immutable archive of past sprint plans, phase reports, and audits.
