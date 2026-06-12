from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.health import router as health_router
from core.config import settings

def create_app() -> FastAPI:
    app = FastAPI(
        title="ASTRA API",
        version="1.0.0",
        description="ASTRA Backend API",
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

    return app

app = create_app()
