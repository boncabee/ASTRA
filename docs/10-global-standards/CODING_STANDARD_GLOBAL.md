# Global Coding Standard

This document establishes the mandatory coding guidelines for the ASTRA platform. Consistency in our codebase reduces technical debt, improves security, and accelerates onboarding.

## 1. Python Style Guide
- **Formatter:** ASTRA uses `Black` with a line length of 120 characters.
- **Linter:** `Ruff` is used for rapid linting and PEP8 compliance enforcement.
- **Imports:** `isort` is used to organize imports (Standard library, Third-party, Local).

## 2. Type Hinting Policy
- **Strict Mode:** ASTRA enforces `strict` mode in Pyright.
- **Rule:** Every function, method, and variable (where ambiguous) MUST be type-hinted.
- **Generics:** Use standard collections `list[str]`, `dict[str, Any]` (Python 3.9+ syntax).
- **Return Types:** Functions that do not return a value must explicitly return `-> None`.

## 3. Naming Conventions
- **Classes:** `PascalCase` (e.g., `ObservationEngine`, `CESEvent`).
- **Functions/Methods:** `snake_case` (e.g., `calculate_risk_score`, `fetch_correlation`).
- **Variables:** `snake_case`. Private class attributes must be prefixed with a single underscore (e.g., `_internal_state`).
- **Constants:** `UPPER_SNAKE_CASE` (e.g., `MAX_RETRY_ATTEMPTS = 3`).

## 4. Error Handling Standards
- **Fail Fast:** Validate inputs at the boundary (via Pydantic). Fail immediately if constraints are violated.
- **Custom Exceptions:** Domain logic should raise custom exceptions (e.g., `PolicyEvaluationError`) rather than generic `ValueError` or `Exception`.
- **API Boundaries:** The FastAPI layer must catch domain exceptions and translate them into standardized HTTP responses (e.g., 400 Bad Request) using a unified JSON schema. Stack traces MUST NEVER leak to the client.

## 5. Logging Standards
- **Structured Logging:** All logs must be structured JSON. Avoid string interpolation in log payloads.
- **Contextual Awareness:** Logs must include a `correlation_id` (not to be confused with ASTRA's Threat Correlations) to trace a request through the system.
- **Levels:**
  - `DEBUG`: Tracing logic, variables (disabled in prod).
  - `INFO`: Business milestones (e.g., "Policy evaluated", "Automation triggered").
  - `WARNING`: Recoverable errors (e.g., "Retrying webhook connection").
  - `ERROR`: Unrecoverable failures (e.g., "Database connection lost").
- **Security:** NEVER log raw passwords, Bearer tokens, or PII.

## 6. Repository Structure Standards
- `src/api/`: FastAPI routers and dependency injection.
- `src/core/`: Application settings, logging configuration, and global security utilities.
- `src/models/`: SQLAlchemy ORM definitions and Pydantic schemas.
- `src/repositories/`: Abstracted database interaction logic.
- `src/services/`: Core business logic (Observation, Correlation, Policy).
- `src/workers/`: Celery/Redis asynchronous task definitions.
- `tests/`: Replicating the `src` structure exactly (e.g., `tests/services/`).

## 7. Documentation Standards in Code
- **Docstrings:** All public classes and functions must include a Google-style docstring detailing arguments, return types, and exceptions raised.
- **Inline Comments:** Use sparingly. Code should be self-documenting. Use inline comments only to explain *why* a counter-intuitive decision was made, never *what* the code is doing.

## 8. Dependency Management Standards
- **Tooling:** ASTRA uses `pip` with strict `requirements.txt` locking.
- **Locking:** Explicit versions must be defined (e.g., `fastapi==0.111.0`).
- **Vulnerability Scanning:** No package may be added without passing a vulnerability scan.
