import time
from typing import Callable, Awaitable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status_code"]
)

REQUEST_TIME = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "path"]
)

class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        start_time = time.time()
        method = request.method
        
        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception:
            status_code = 500
            raise
        finally:
            process_time = time.time() - start_time
            
            # Use matched route path if available to prevent cardinality explosion (e.g. /users/{id})
            route = request.scope.get("route")
            path = route.path if route else request.url.path

            REQUEST_COUNT.labels(method=method, path=path, status_code=status_code).inc()
            REQUEST_TIME.labels(method=method, path=path).observe(process_time)

        return response
