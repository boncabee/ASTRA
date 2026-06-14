import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.rbac import RequireRoles
from models.user import UserRole
from schemas.correlation import CorrelationMatchResponse, CorrelationRuleResponse
from crud.crud_correlation import correlation_crud

router = APIRouter(
    dependencies=[Depends(RequireRoles([UserRole.ADMINISTRATOR, UserRole.SECURITY_ENGINEER, UserRole.SOC_ANALYST, UserRole.INCIDENT_RESPONDER]))]
)

@router.get("/rules", response_model=Dict[str, Any])
async def get_correlation_rules(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve Correlation Rules."""
    rules = await correlation_crud.get_rules(db, skip=skip, limit=limit)
    # ASTRA standard wrapper {"data": [...]}
    return {"data": [CorrelationRuleResponse.model_validate(r).model_dump() for r in rules]}

@router.get("/matches", response_model=Dict[str, Any])
async def get_correlation_matches(
    rule_id: Optional[uuid.UUID] = None,
    min_score: Optional[int] = Query(None, ge=0, le=100),
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve Correlation Matches."""
    matches = await correlation_crud.get_matches(
        db, 
        rule_id=rule_id, 
        min_score=min_score, 
        start_time=start_time, 
        end_time=end_time, 
        skip=skip, 
        limit=limit
    )
    return {"data": [CorrelationMatchResponse.model_validate(m).model_dump() for m in matches]}

@router.get("", response_model=Dict[str, Any])
async def get_correlations(
    rule_id: Optional[uuid.UUID] = None,
    min_score: Optional[int] = Query(None, ge=0, le=100),
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """Alias for /matches."""
    return await get_correlation_matches(rule_id, min_score, start_time, end_time, skip, limit, db)

@router.get("/{id}", response_model=Dict[str, Any])
async def get_correlation_match(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """Retrieve a specific Correlation Match by ID."""
    match = await correlation_crud.get_match(db, id=id)
    if not match:
        return {"error": "Correlation match not found", "code": 404}
    return {"data": CorrelationMatchResponse.model_validate(match).model_dump()}
