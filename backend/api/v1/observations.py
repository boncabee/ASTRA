import uuid
from typing import Dict, Any, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.rbac import RequireRoles
from models.user import UserRole, User
from models.observation import ObservationStatus
from schemas.observation import ObservationResponse, ObservationUpdate
from services.observation import ObservationService
from api.deps import get_current_user

router = APIRouter(
    dependencies=[Depends(RequireRoles([UserRole.ADMINISTRATOR, UserRole.SECURITY_ENGINEER, UserRole.SOC_ANALYST, UserRole.INCIDENT_RESPONDER]))]
)

def error_response(msg: str, code: int):
    return JSONResponse(status_code=code, content={"error": msg, "code": code})

@router.get("", response_model=Dict[str, Any])
async def list_observations(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000),
    status: Optional[ObservationStatus] = None,
    risk_category: Optional[str] = None,
    classification: Optional[str] = None,
    created_after: Optional[datetime] = None,
    created_before: Optional[datetime] = None,
    sort_by: str = Query("created_at", description="Field to sort by (created_at, risk_score, status, classification)"),
    sort_order: str = Query("desc", description="Sort order (asc or desc)"),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve Observations."""
    valid_sort_by = ["created_at", "risk_score", "status", "classification"]
    if sort_by not in valid_sort_by:
        return error_response(f"Invalid sort_by. Must be one of {valid_sort_by}", 400)
    
    if sort_order.lower() not in ["asc", "desc"]:
        return error_response("Invalid sort_order. Must be 'asc' or 'desc'", 400)

    service = ObservationService(db)
    observations, total = await service.repository.list(
        skip=skip,
        limit=limit,
        status=status,
        risk_category=risk_category,
        classification=classification,
        created_after=created_after,
        created_before=created_before,
        sort_by=sort_by,
        sort_order=sort_order
    )
    
    return {
        "data": [ObservationResponse.model_validate(o).model_dump() for o in observations],
        "total": total
    }

@router.get("/{id}", response_model=Dict[str, Any])
async def get_observation(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """Retrieve a specific Observation by ID."""
    service = ObservationService(db)
    observation = await service.repository.get_by_id(id)
    if not observation:
        return error_response("Observation not found", 404)
    return {"data": ObservationResponse.model_validate(observation).model_dump()}

@router.put("/{id}", response_model=Dict[str, Any], dependencies=[Depends(RequireRoles([UserRole.ADMINISTRATOR, UserRole.INCIDENT_RESPONDER]))])
async def update_observation_status(
    id: uuid.UUID,
    update_data: ObservationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update Observation status."""
    service = ObservationService(db)
    observation = await service.repository.get_by_id(id)
    if not observation:
        return error_response("Observation not found", 404)
    
    try:
        updated = await service.update_status(observation, update_data.status, updated_by=str(current_user.id))
        return {"data": ObservationResponse.model_validate(updated).model_dump()}
    except ValueError as e:
        return error_response(str(e), 400)
