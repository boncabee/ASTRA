# PHASE 16.7: Backend Authentication Audit

## Objective
Determine the current authentication and authorization capabilities of ASTRA prior to implementing frontend authentication integrations.

## Review Scope
- FastAPI routers
- Auth modules
- Security modules
- JWT handling
- RBAC implementation
- Middleware
- Dependencies

## Findings

### 1. What authentication mechanisms exist?
ASTRA implements an **OAuth2 Password Bearer** flow using **JWT (JSON Web Tokens)**. Passwords are hashed using `bcrypt` (`core/security.py`).

### 2. What login endpoints exist?
- `POST /api/v1/auth/login`
  Accepts an `OAuth2PasswordRequestForm` (username/password) and returns a JSON response containing an `access_token` (JWT) and `token_type` (bearer). Rate limited to 5 requests per minute.

### 3. What refresh token endpoints exist?
**None**. There are no endpoints for refreshing expired access tokens, meaning sessions will forcefully expire based on `ACCESS_TOKEN_EXPIRE_MINUTES`.

### 4. What logout endpoints exist?
**None**. JWTs are stateless and there is no token revocation list (blocklist) or session state maintained on the backend to invalidate tokens prior to expiration.

### 5. What user profile endpoints exist?
- `GET /api/v1/auth/me`
  Returns the currently authenticated user's profile information (id, username, email, role, is_active).

### 6. What RBAC capabilities exist?
- **Role-Based Access Control** is implemented via a `RequireRoles` FastAPI dependency (`core/rbac.py`).
- It extracts the `UserRole` from the `current_user` and validates it against a permitted list of roles per route.
- A **Deny-by-Default Middleware** (`enforce_deny_by_default`) automatically rejects requests to `/api/*` that do not explicitly apply the `RequireRoles` dependency (with exceptions for `/health` and `/login`).

### 7. What frontend authentication flow is supported today?
**None.** The frontend authentication flow is bypassed and entirely simulated for development:
- The login page (`src/app/(auth)/login/page.tsx`) is a static placeholder with a direct `<Link>` to the dashboard.
- The API client (`src/lib/api/client.ts`) automatically injects a `NEXT_PUBLIC_DEV_TOKEN` from the environment if present.
- There is no session management, React Context for Auth, or secure token storage implemented.

### 8. What gaps remain?
- **Backend:** 
  - Missing token refresh mechanisms (Refresh Tokens endpoint).
  - Missing token revocation/logout mechanism.
  - Potential security improvement: Shift from returning tokens in the JSON payload to setting `HttpOnly` secure cookies to prevent XSS.
- **Frontend:** 
  - No functional login form (missing API integration and state management).
  - No auth state provider or route guards.
  - No mechanism to handle expired tokens.

## Decision
**PARTIALLY READY**

The backend enforces strict authentication and RBAC by default, establishing a secure baseline. However, the lack of refresh tokens and logout capabilities, combined with a completely non-functional frontend auth layer, means significant integration work remains before user authentication is considered production-ready.
