import time
import uuid
from typing import Callable, Awaitable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from core.logging import logger, correlation_id

class LogAndTraceMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        req_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        token = correlation_id.set(req_id)
        
        start_time = time.perf_counter()
        
        logger.info(
            f"Request Started {request.method} {request.url.path}",
            extra={
                "http.request.method": request.method,
                "http.request.url": str(request.url),
            }
        )
        
        try:
            response = await call_next(request)
            process_time = time.perf_counter() - start_time
            response.headers["X-Correlation-ID"] = req_id
            
            logger.info(
                f"Request Completed {request.method} {request.url.path} - {response.status_code}",
                extra={
                    "http.response.status_code": response.status_code,
                    "http.request.duration_seconds": process_time,
                }
            )
            return response
        except Exception as exc:
            process_time = time.perf_counter() - start_time
            logger.error(
                f"Request Failed {request.method} {request.url.path}",
                extra={
                    "error": str(exc),
                    "http.request.duration_seconds": process_time,
                },
                exc_info=True
            )
            raise
        finally:
            correlation_id.reset(token)
