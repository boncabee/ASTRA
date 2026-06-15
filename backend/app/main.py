from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from api.v1.health import router as health_router
from api.v1.auth import router as auth_router
from api.v1.users import router as users_router
from api.v1.admin import router as admin_router
from api.v1.security import router as security_router
from api.v1.responders import router as responders_router
from core.config import settings
from core.rbac import enforce_deny_by_default

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    from workers.automation_worker import automation_worker
    await automation_worker.start()
    yield
    await automation_worker.stop()

def create_app() -> FastAPI:
    app = FastAPI(
        title="ASTRA API",
        version="1.0.0",
        description="ASTRA Backend API",
        dependencies=[Depends(enforce_deny_by_default)],
        lifespan=lifespan
    )

    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(health_router, prefix="/api/v1")
    app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
    app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
    app.include_router(admin_router, prefix="/api/v1/admin", tags=["admin"])
    app.include_router(security_router, prefix="/api/v1/security", tags=["security"])
    app.include_router(responders_router, prefix="/api/v1/responders", tags=["responders"])
    
    from api.v1.correlations import router as correlations_router
    app.include_router(correlations_router, prefix="/api/v1/correlations", tags=["correlations"])

    from api.v1.observations import router as observations_router
    app.include_router(observations_router, prefix="/api/v1/observations", tags=["observations"])

    from api.v1.policies import router as policies_router
    app.include_router(policies_router, prefix="/api/v1/policies", tags=["policies"])

    from api.v1.evidence import router as evidence_router
    app.include_router(evidence_router, prefix="/api/v1/evidence", tags=["evidence"])

    from api.v1.audit import router as audit_router
    app.include_router(audit_router, prefix="/api/v1/audit", tags=["audit"])

    from api.v1.reports import router as reports_router
    app.include_router(reports_router, prefix="/api/v1/reports", tags=["reports"])

    from api.v1.automation import router as automation_router
    app.include_router(automation_router, prefix="/api/v1/automation", tags=["automation"])

    return app

app = create_app()
