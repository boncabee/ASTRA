# API Governance Standard

This document establishes the design, versioning, and security standards for all RESTful interfaces exposed by the ASTRA platform.

## 1. REST API Design
- **Protocol:** HTTPS only. HTTP requests must be strictly redirected or rejected.
- **Format:** JSON payloads only (`application/json`).
- **Resource Naming:** Nouns, pluralized, and strictly `kebab-case` in URLs (e.g., `/api/v1/policy-decisions`).
- **HTTP Methods:**
  - `GET`: Retrieve a resource (Idempotent).
  - `POST`: Create a new resource.
  - `PUT`: Full replacement of a resource (Idempotent).
  - `PATCH`: Partial update of a resource.
  - `DELETE`: Remove a resource.

## 2. Versioning
- **URL Versioning:** All public endpoints must include the major version in the URL path (e.g., `/api/v1/...`).
- **Breaking Changes:** Any breaking change (removing a field, changing a type) requires a bump to the major version (`/api/v2/...`). Additive changes (adding an optional field) do not.

## 3. Pagination and Filtering
- **Pagination:** All collection responses (e.g., getting a list of Observations) MUST be paginated to prevent memory exhaustion and DoS.
- **Standard Params:** Use `?limit=100&offset=0` as the standard approach.
- **Filtering:** Use query parameters for exact matches (`?status=active`). Use explicit operators for ranges (`?risk_score_gt=80`).

## 4. Rate Limiting
- All public-facing API endpoints must implement rate limiting to protect against brute force and DoS attacks.
- Limits are scoped by the JWT `subject` (User ID) or IP address (for unauthenticated routes like login).

## 5. Security Standards
- **Authentication:** All routes (except `/health` and `/login`) must require a valid JWT Bearer token.
- **Authorization:** Enforced via FastAPI dependency injection based on the roles embedded in the JWT.
- **Error Responses:** 
  - Standardized JSON error schema: `{"error": "string", "details": "string", "code": int}`.
  - Never leak stack traces or internal DB IDs in error messages. 404s should obscure resource existence if the user lacks access.
