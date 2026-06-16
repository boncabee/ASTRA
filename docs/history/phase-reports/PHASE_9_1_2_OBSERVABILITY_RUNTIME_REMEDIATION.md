# PHASE 9.1.2: OBSERVABILITY RUNTIME REMEDIATION

**Date:** 2026-06-17  
**Status:** COMPLETE  

## Executive Summary
This phase successfully remediated the critical runtime `HTTP 500` errors affecting all API endpoints without reverting any prior security upgrades (i.e., retaining FastAPI 0.137.1 and Starlette 1.3.1). The observability stack was stabilized by replacing the broken `prometheus-fastapi-instrumentator` with a native `PrometheusMiddleware` implementation using the official `prometheus_client`.

## Root Cause Summary
The `prometheus-fastapi-instrumentator==8.0.0` library contains a known bug when parsing the `_IncludedRouter` objects introduced in recent Starlette updates. Because it operates as an ASGI middleware, its failure to resolve `route.path` caused a catastrophic `AttributeError` on every incoming HTTP request, resulting in a `500 Internal Server Error`.

## Alternative Solutions Evaluated
1. **Option A1: `starlette-prometheus`**
   - *Result:* REJECTED. The library has not seen recent maintenance and introduces unnecessary third-party risks.
2. **Option A2: Custom Middleware with `prometheus_client`**
   - *Result:* SELECTED. This provides the lowest maintenance burden, uses the official Prometheus library, and bypasses the `_IncludedRouter` bug by safely resolving `request.scope.get("route")`.
3. **Option B: Monkey-Patching**
   - *Result:* REJECTED. Violates development standards and introduces fragile dependencies on third-party internal routing logic.

## Chosen Solution
Replaced `prometheus-fastapi-instrumentator` with a custom `PrometheusMiddleware` utilizing the official `prometheus_client` library. The middleware natively tracks `http_requests_total` and `http_request_duration_seconds`.

## Dependency Changes
**Removed:**
- `prometheus-fastapi-instrumentator==8.0.0`

**Added:**
- `prometheus-client>=0.20.0`

## Files Modified
- `backend/requirements.txt`
- `backend/app/main.py`
- `backend/api/middleware/metrics.py` (NEW)
- `backend/Dockerfile`

## Risks
- **Metrics Dashboard Compatibility:** The exposed metric names might slightly differ from the previous auto-generated ones. Any existing Grafana dashboards may need their queries updated to use `http_requests_total` and `http_request_duration_seconds`.

## Final Determination
**GO**

The application is fully functional in a production runtime environment with native metrics and strict health checks.
