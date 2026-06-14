import uuid
from typing import Annotated, Dict, Any
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.rbac import RequireRoles
from models.user import UserRole
from schemas.evidence import EvidenceResponse
from repositories.evidence import EvidenceRepository
from core.logging import logger

router = APIRouter()

def error_response(msg: str, code: int):
    return JSONResponse(status_code=code, content={"error": msg, "code": code})

# All roles have Read access
read_roles = [UserRole.ADMINISTRATOR, UserRole.SECURITY_ENGINEER, UserRole.INCIDENT_RESPONDER, UserRole.SOC_ANALYST]

@router.get("", response_model=Dict[str, Any], dependencies=[Depends(RequireRoles(read_roles))])
async def list_evidence(
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000)
):
    repo = EvidenceRepository(db)
    evidence_list, total = await repo.list_evidence(skip=skip, limit=limit)
    serialized = [EvidenceResponse.model_validate(e).model_dump() for e in evidence_list]
    return {"data": serialized, "total": total}

@router.get("/{evidence_id}", response_model=Dict[str, Any], dependencies=[Depends(RequireRoles(read_roles))])
async def get_evidence(evidence_id: uuid.UUID, db: Annotated[AsyncSession, Depends(get_db)]):
    repo = EvidenceRepository(db)
    evidence = await repo.get_evidence_by_id(evidence_id)
    if not evidence:
        return error_response("Evidence not found", 404)
    return {"data": EvidenceResponse.model_validate(evidence).model_dump()}
