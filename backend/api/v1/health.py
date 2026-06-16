from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import Annotated
from core.database import get_db
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class HealthCheck(BaseModel):
    status: str
    version: str
    database: str

@router.get("/health", response_model=HealthCheck, status_code=200)
async def health_check(db: Annotated[AsyncSession, Depends(get_db)]):
    try:
        await db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed"
        )
    return {"status": "ok", "version": "1.0.0", "database": db_status}
