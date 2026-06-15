# Architecture Audit Report

## 1. Overview
The Architecture Audit reviews the ASTRA backend for compliance with Domain-Driven Design (DDD) boundaries, clean architecture principles, and future scalability.

## 2. Strengths
- **Modular Monolith Setup:** The architecture is designed as a modular monolith, which is highly appropriate for the current phase, avoiding premature microservice complexity.
- **Clear Domain Boundaries:** Distinct domains exist (Observation, Correlation, Policy, Evidence, Reporting, Automation) with dedicated models and schemas.
- **Repository Pattern:** The usage of the repository pattern abstracting database access is visible across all core domains.

## 3. Weaknesses
- **Layer Violations:** `backend/app/main.py` directly imports from root-level `api`, `core`, and `workers` directories, indicating that the `app` module is not the true root package. This creates a scattered architecture.
- **Domain Separation:** Domain models (`models/`), schemas (`schemas/`), and API routers (`api/`) are separated by technical concern rather than by domain context. This is MVC-style, not strict DDD.

## 4. Findings
- **Finding 1:** The project uses a layered architecture (MVC style: all models in one folder, all routers in another) rather than a pure DDD architecture (where everything related to `Policy` lives in a `policy/` module).
- **Finding 2:** Worker integrations (Celery/Redis queue) are tightly coupled with the FastAPI lifespan event in `main.py` rather than being abstracted behind an interface.

## 5. Risks
- **Scalability Risk:** As the platform grows, finding all components of a single domain (e.g., "Policy") requires opening 5 different directories, increasing cognitive load and merge conflicts.
- **Maintainability Risk:** The non-standard root packaging will confuse standard Python tooling (as seen with `pytest` and `mypy` path resolutions).

## 6. Technical Debt
- **High:** Re-architecting from MVC-style layered folders to true DDD domain folders (e.g., `app/domain/policy/`) will become significantly harder as more features are added.

## 7. Standards Violations
- Deviation from strict DDD bounded contexts as outlined in documentation.

## 8. Recommendations
| Priority | Recommendation |
|---|---|
| **High** | Re-organize the `backend` directory into a true Domain-Driven structure. Move all related routers, models, schemas, and services into self-contained domain packages (e.g., `backend/app/domain/observation/`). |
| **Medium** | Ensure the FastAPI application initialization in `main.py` uses proper dependency injection for workers to improve testability. |
