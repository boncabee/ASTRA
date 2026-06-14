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

def create_app() -> FastAPI:
    app = FastAPI(
        title="ASTRA API",
        version="1.0.0",
        description="ASTRA Backend API",
        dependencies=[Depends(enforce_deny_by_default)]
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

    return app

app = create_app()
