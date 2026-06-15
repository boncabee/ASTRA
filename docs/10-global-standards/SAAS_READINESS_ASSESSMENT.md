# SaaS Readiness Assessment

This document evaluates ASTRA's capability to evolve from a single-tenant enterprise deployment into a multi-tenant, cloud-native Software-as-a-Service (SaaS) platform (Phase 11 Roadmap).

## 1. Multi-Tenant Support (Score: 1/5)
- **Current State:** ASTRA is designed for single-tenant execution. There is no concept of a `Tenant` entity in the core domain models.
- **Action:** A major architectural refactoring is required to introduce a `Tenant` model and inject `tenant_id` into the request context of all APIs.

## 2. Tenant Isolation (Score: 1/5)
- **Current State:** Because there is no `tenant_id`, there is no data isolation. 
- **Action:** The ORM (SQLAlchemy) must be updated to implement automatic, mandatory filtering by `tenant_id` on every query to prevent cross-tenant data spillage (Horizontal Privilege Escalation). Alternatively, a database-per-tenant topology must be explored.

## 3. Data Isolation (Score: 1/5)
- **Current State:** All CES Events, Observations, and Evidence are stored globally.
- **Action:** For strict compliance (e.g., European data residency), the SaaS architecture may need to support geographic data pinning per tenant, significantly complicating the DB routing logic.

## 4. Organization Model (Score: 2/5)
- **Current State:** Users exist globally with a single Role (e.g., Admin, Analyst).
- **Action:** The RBAC system must be upgraded to support User-to-Tenant relationships, where a User can be an Admin in Tenant A but an Analyst in Tenant B.

## 5. Billing & Subscription Readiness (Score: 0/5)
- **Current State:** No billing metrics are collected.
- **Action:** The system must start emitting aggregate usage metrics (e.g., Events Processed Per Month, Automations Executed) per `tenant_id` to a billing provider like Stripe.

## 6. Cloud Readiness (Score: 4/5)
- **Current State:** The system is stateless (excluding DB/Redis), containerized, and horizontally scalable. It utilizes 12-factor app principles (e.g., environment variables for config).
- **Action:** Native cloud managed services (e.g., AWS RDS, ElastiCache, SQS instead of local Redis/Celery) should be validated to ensure seamless managed deployments.

## Overall SaaS Maturity Score: 1.5 / 5 (Not Ready)
ASTRA currently relies on physical/network isolation (deploying an entire ASTRA instance per customer) rather than logical multi-tenancy. Achieving true SaaS readiness (Phase 11) will require a massive, fundamental refactor of the database schemas, ORM layers, and API authentication flows to enforce strict `tenant_id` isolation.
