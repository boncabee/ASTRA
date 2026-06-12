from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class HealthCheck(BaseModel):
    status: str
    version: str

@router.get("/health", response_model=HealthCheck, status_code=200)
async def health_check():
    return {"status": "ok", "version": "1.0.0"}
