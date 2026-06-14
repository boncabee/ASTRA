# ASTRA Sprint 3 Dependency Map

The following map illustrates the architectural dependencies between core components required for Sprint 3. Components point towards the systems they depend on.

## Core Component Dependencies

* **Frontend UI Layer**
  * Depends on: Authentication Service, RBAC Middleware, Observation APIs, Correlation APIs

* **Authentication (Auth)**
  * Depends on: Database (User Schema)

* **RBAC (Role-Based Access Control)**
  * Depends on: Authentication, Database (Roles Schema)

* **Policy Engine**
  * Depends on: Observation Engine, Risk Scoring Module, Database (Policy Rules)

* **Risk Scoring Module**
  * Depends on: Observation Engine

* **Observation Engine**
  * Depends on: Correlation Engine, Database (Observation Schema)

* **Correlation Engine**
  * Depends on: CES Schema (from Sprint 1/2), Event Ingestion Pipeline, Database (CES Events)

* **Database Layer**
  * Independent. Must be established prior to other systems building upon it.

## Execution Flow Dependency Chain

`Database` → `Authentication & RBAC` → `Correlation Engine` → `Observation Engine` → `Risk Scoring` → `Policy Engine` → `Frontend UI`
