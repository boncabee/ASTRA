import uuid
from typing import Annotated, Dict, Any
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.rbac import RequireRoles
from models.user import UserRole
from schemas.evidence import AuditEventResponse, DecisionProvenanceResponse
from repositories.evidence import AuditRepository
from services.audit_engine import AuditEngineService
from core.logging import logger

router = APIRouter()

def error_response(msg: str, code: int):
    return JSONResponse(status_code=code, content={"error": msg, "code": code})

read_roles = [UserRole.ADMINISTRATOR, UserRole.SECURITY_ENGINEER, UserRole.INCIDENT_RESPONDER, UserRole.SOC_ANALYST]

@router.get("", response_model=Dict[str, Any], dependencies=[Depends(RequireRoles(read_roles))])
async def list_audit_events(
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000)
):
    repo = AuditRepository(db)
    events, total = await repo.list_events(skip=skip, limit=limit)
    serialized = [AuditEventResponse.model_validate(e).model_dump() for e in events]
    
    # Log metric
    logger.info("metric", extra={"audit_queries": 1})
    
    return {"data": serialized, "total": total}

@router.get("/{entity_id}", response_model=Dict[str, Any], dependencies=[Depends(RequireRoles(read_roles))])
async def get_audit_by_entity(
    entity_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    entity_type: str = Query(..., description="The type of entity to fetch audit events for")
):
    repo = AuditRepository(db)
    events = await repo.get_events_by_entity(entity_type, entity_id)
    serialized = [AuditEventResponse.model_validate(e).model_dump() for e in events]
    
    logger.info("metric", extra={"audit_queries": 1})
    
    return {"data": serialized}

@router.get("/provenance/{observation_id}", response_model=Dict[str, Any], dependencies=[Depends(RequireRoles(read_roles))])
async def get_decision_provenance(observation_id: uuid.UUID, db: Annotated[AsyncSession, Depends(get_db)]):
    svc = AuditEngineService(db)
    provenance = await svc.get_decision_provenance(observation_id)
    if not provenance:
        return error_response("Observation not found for provenance", 404)
        
    return {"data": provenance.model_dump()}
