# PHASE 9.1.1: RUNTIME COMPATIBILITY INVESTIGATION

**Date:** 2026-06-17  
**Status:** COMPLETE (NO-GO)  
**Target:** Backend Healthcheck 500 Errors  

## Executive Summary
During the Phase 9.1 Runtime Hardening sprint, it was discovered that the backend application was systematically returning `HTTP 500 Internal Server Error` for all incoming requests, including the `/api/v1/health` endpoint. The healthcheck was temporarily modified to tolerate these 500 errors to allow the container to report as "healthy." This investigation was launched to identify the root cause of these 500 errors, as a 500-tolerant healthcheck is unacceptable for a production deployment.

## Investigation Findings

### 1. Environment Versions
- **FastAPI Version:** `0.137.1`
- **Starlette Version:** `1.3.1`
- **Prometheus-FastAPI-Instrumentator Version:** `8.0.0`

### 2. Affected Endpoints
The issue is **global**. It affects **all endpoints** registered via `app.include_router()`. Testing multiple paths (e.g., `/api/v1/health`, `/api/v1/auth/login`) consistently yields a `500 Internal Server Error`.

### 3. Root Cause Analysis
The root cause is an **instrumentator bug** triggered by a **dependency incompatibility**. 

In previous phases, the project upgraded `starlette` to `1.3.1` (and `fastapi` to `0.137.1`) to remediate security vulnerabilities. In these newer versions of Starlette, the routing architecture was updated to use a new `_IncludedRouter` object when routers are mounted via `include_router()`. 

The `prometheus-fastapi-instrumentator==8.0.0` library attempts to resolve the current route name during every HTTP request to populate its metrics labels. It does this by iterating over the application's routes and attempting to read `route.path`. Because `_IncludedRouter` does not have a `path` attribute, the instrumentator raises an `AttributeError`, crashing the request pipeline before the business logic is ever executed.

Because the instrumentator is implemented as an ASGI middleware, it catches every request, thereby bringing down the entire API.

*(Note: This issue was masked in CI/CD pipelines because the `app/main.py` logic explicitly disables the instrumentator when `pytest` is running.)*

### 4. Stack Trace
```text
INFO:     127.0.0.1:43760 - "GET /api/v1/health HTTP/1.1" 500 Internal Server Error
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "/usr/local/lib/python3.14/site-packages/uvicorn/protocols/http/h11_impl.py", line 396, in run_asgi
    result = await app(self.scope, self.receive, self.send)
  File "/usr/local/lib/python3.14/site-packages/uvicorn/middleware/proxy_headers.py", line 70, in __call__
    return await self.app(scope, receive, send)
  File "/usr/local/lib/python3.14/site-packages/fastapi/applications.py", line 1162, in __call__
    await super().__call__(scope, receive, send)
  File "/usr/local/lib/python3.14/site-packages/starlette/applications.py", line 90, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/usr/local/lib/python3.14/site-packages/starlette/middleware/errors.py", line 186, in __call__
    raise exc
  File "/usr/local/lib/python3.14/site-packages/prometheus_fastapi_instrumentator/middleware.py", line 131, in __call__
    handler, is_templated = self._get_handler(request)
  File "/usr/local/lib/python3.14/site-packages/prometheus_fastapi_instrumentator/middleware.py", line 240, in _get_handler
    route_name = routing.get_route_name(request)
  File "/usr/local/lib/python3.14/site-packages/prometheus_fastapi_instrumentator/routing.py", line 75, in get_route_name
    route_name = _get_route_name(scope, routes)
  File "/usr/local/lib/python3.14/site-packages/prometheus_fastapi_instrumentator/routing.py", line 55, in _get_route_name
    route_name = route.path
AttributeError: '_IncludedRouter' object has no attribute 'path'
```

### 5. Reproduction Steps
1. Run the backend container using `docker compose up -d backend`.
2. Ensure the `pytest` module is not loaded (standard runtime behavior).
3. Execute `curl.exe -s -i http://localhost:8000/api/v1/health`.
4. Observe the `HTTP/1.1 500 Internal Server Error` response and the traceback in `docker compose logs backend`.

## Recommended Fix

There are two viable paths to remediate this issue, listed in order of preference:

1. **Option A: Replace the Instrumentator (Recommended)**
   - Disable or remove `prometheus-fastapi-instrumentator`.
   - Implement metrics manually using the official `prometheus_client` or migrate to a more actively maintained library like `starlette-prometheus`. This eliminates the dependency conflict while retaining observability.

2. **Option B: Patch the Instrumentator Locally**
   - Fork or monkey-patch `prometheus_fastapi_instrumentator.routing._get_route_name` during app startup to check if `hasattr(route, 'path')` before accessing it, safely ignoring `_IncludedRouter` instances.

*(Note: Downgrading Starlette/FastAPI is **not** recommended, as the recent upgrade was specifically performed to remediate known security vulnerabilities.)*

## Risk Assessment
- **Severity:** CRITICAL
- **Impact:** The entire API is inaccessible in production-like environments where tests are not running. All health checks and business operations will fail.
- **Resolution Risk:** Removing the instrumentator will temporarily blind the `/metrics` endpoint until an alternative is implemented, but this is preferable to a completely broken API.

## Final Determination

**NO-GO**

The platform is currently non-functional in a true runtime environment due to this middleware exception. The health checks cannot be restored to strict `200 OK` enforcement until the underlying middleware bug is remediated. Immediate engineering action is required to implement the recommended fix.
