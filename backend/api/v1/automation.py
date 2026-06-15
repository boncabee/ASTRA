from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core.rbac import RequireRoles
from models.user import User, UserRole
from schemas.automation import (
    AutomationRequestCreate,
    AutomationRequestResponse,
    AutomationRequestDetailResponse,
    AutomationExecutionResponse,
    AutomationMetricsResponse
)
from repositories.automation import AutomationRepository
from services.automation import AutomationService
from api.deps import get_current_user

router = APIRouter(
    dependencies=[Depends(RequireRoles([
        UserRole.ADMINISTRATOR, 
        UserRole.SECURITY_ENGINEER, 
        UserRole.SOC_ANALYST, 
        UserRole.INCIDENT_RESPONDER
    ]))]
)

AdminOrEngineer = RequireRoles([UserRole.ADMINISTRATOR, UserRole.SECURITY_ENGINEER])

@router.post("", response_model=AutomationRequestResponse, status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(AdminOrEngineer)])
async def create_automation(
    request: AutomationRequestCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new automation request and queue it for execution.
    Access: Administrator, Security Engineer
    """
    service = AutomationService(db)
    new_request = await service.create_automation_request(request, user_id=str(current_user.id))
    return new_request

@router.get("/metrics", response_model=AutomationMetricsResponse)
async def get_metrics(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get metrics logging for automation.
    Access: Administrator, Security Engineer, SOC Analyst, Incident Responder
    """
    repo = AutomationRepository(db)
    metrics = await repo.get_metrics()
    return metrics

@router.get("/history", response_model=List[AutomationExecutionResponse])
async def get_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get execution history.
    Access: Administrator, Security Engineer, SOC Analyst, Incident Responder
    """
    repo = AutomationRepository(db)
    executions, _ = await repo.get_history(skip=skip, limit=limit)
    return executions

@router.get("/{id}", response_model=AutomationRequestDetailResponse)
async def get_request(
    id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific automation request by ID.
    Access: Administrator, Security Engineer, SOC Analyst, Incident Responder
    """
    repo = AutomationRepository(db)
    request = await repo.get_request(id)
    if not request:
        raise HTTPException(status_code=404, detail="Automation Request not found")
    return request

@router.get("", response_model=List[AutomationRequestResponse])
async def list_requests(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    List all automation requests.
    Access: Administrator, Security Engineer, SOC Analyst, Incident Responder
    """
    repo = AutomationRepository(db)
    requests, _ = await repo.list_requests(skip=skip, limit=limit)
    return requests
