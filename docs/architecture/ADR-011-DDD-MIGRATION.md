# ADR 011: Domain-Driven Design (DDD) Architecture Migration

## Status
Proposed

## Context
ASTRA's current architecture uses a layered pattern (`api/`, `services/`, `repositories/`, `models/`), which has scaled decently for the MVP phases. However, as we approach Phase 7 (Case Management) and the integration of highly complex bounded contexts (Correlations, Policies, Automation, and Cases), the lack of strict domain boundaries causes tight coupling. Service classes are becoming God objects, and database models are bleeding directly into API responses. To ensure enterprise readiness, we must migrate to a Domain-Driven Design (DDD) architecture.

## Decision
We will migrate the ASTRA backend to a Modular Monolith architecture based on Domain-Driven Design principles.

### Key Architectural Shifts
1. **Bounded Contexts as Modules**: The `app/` directory will be restructured into distinct domains: `Identity`, `Ingestion`, `Observation`, `Policy`, `Correlation`, `Reporting`, and `CaseManagement`.
2. **Strict Layering within Domains**: Each domain will contain:
   - `domain/`: Pure business logic, Entities, Value Objects, Domain Events.
   - `application/`: Use cases, Service abstractions, DTOs.
   - `infrastructure/`: SQLAlchemy repositories, external API clients, message queue producers.
   - `presentation/`: FastAPI routers and dependency injection.
3. **Domain Events**: Inter-domain communication will occur exclusively via Domain Events or strictly defined Application Services to prevent database-level coupling.
4. **Repository Pattern Evolution**: Repositories will return Domain Entities, not SQLAlchemy Models.

## Consequences

### Positive
* **Decoupling**: Bounded contexts can be developed, tested, and potentially deployed independently.
* **Maintainability**: Clear separation of concerns prevents business logic from bleeding into FastAPI routers or SQLAlchemy models.
* **Testability**: Pure domain models can be tested instantly without database dependencies.

### Negative
* **Boilerplate**: DDD introduces additional layers of abstraction (DTOs to Entities to SQLAlchemy Models), increasing initial development time.
* **Migration Effort**: Refactoring the existing 6 phases into the new structure will require significant effort and a careful, phased approach.

## Implementation Plan (Phased Migration)
1. **Phase 1: Foundation (Sprint 1)**
   - Introduce the new directory structure alongside the existing one (`app/domains/`).
   - Implement base classes for Entities, Aggregate Roots, and Domain Events.
2. **Phase 2: Leaf Domains (Sprint 2)**
   - Migrate independent domains first: `Identity` (Auth/Users) and `Reporting`.
   - Update tests to validate the new boundaries.
3. **Phase 3: Core Domains (Sprint 3)**
   - Migrate complex domains: `Observation`, `Policy`, and `Correlation`.
   - Implement the Domain Event bus for inter-domain triggers.
4. **Phase 4: Decommissioning (Sprint 4)**
   - Delete the legacy `api/`, `services/`, `repositories/`, and `models/` directories.
   - Finalize CI/CD pipeline adjustments.
