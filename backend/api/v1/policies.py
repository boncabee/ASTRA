import uuid
from typing import Annotated, Dict, Any
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.rbac import RequireRoles
from models.user import User, UserRole
from schemas.policy import (
    PolicyCreate, PolicyUpdate, PolicyResponse, PolicyEvaluationResponse
)
from api.deps import get_current_user
from repositories.policy import PolicyRepository

router = APIRouter()

def error_response(msg: str, code: int):
    return JSONResponse(status_code=code, content={"error": msg, "code": code})

# Roles configured from architectural matrix
read_roles = [UserRole.ADMINISTRATOR, UserRole.SECURITY_ENGINEER, UserRole.INCIDENT_RESPONDER, UserRole.SOC_ANALYST]
write_roles = [UserRole.ADMINISTRATOR, UserRole.SECURITY_ENGINEER]

@router.get("", response_model=Dict[str, Any], dependencies=[Depends(RequireRoles(read_roles))])
async def list_policies(
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000)
):
    repo = PolicyRepository(db)
    policies, total = await repo.list(skip=skip, limit=limit)
    # Serialize with Pydantic
    serialized_policies = [PolicyResponse.model_validate(p).model_dump() for p in policies]
    return {"data": serialized_policies, "total": total}

@router.get("/evaluations", response_model=Dict[str, Any], dependencies=[Depends(RequireRoles(read_roles))])
async def list_evaluations(
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000)
):
    repo = PolicyRepository(db)
    evals, total = await repo.list_evaluations(skip=skip, limit=limit)
    serialized_evals = [PolicyEvaluationResponse.model_validate(e).model_dump() for e in evals]
    return {"data": serialized_evals, "total": total}

@router.get("/{policy_id}", response_model=Dict[str, Any], dependencies=[Depends(RequireRoles(read_roles))])
async def get_policy(policy_id: uuid.UUID, db: Annotated[AsyncSession, Depends(get_db)]):
    repo = PolicyRepository(db)
    policy = await repo.get_by_id(policy_id)
    if not policy:
        return error_response("Policy not found", 404)
    return {"data": PolicyResponse.model_validate(policy).model_dump()}

@router.post("", response_model=Dict[str, Any], dependencies=[Depends(RequireRoles(write_roles))])
async def create_policy(
    policy_in: PolicyCreate, 
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    repo = PolicyRepository(db)
    existing = await repo.get_by_name(policy_in.name)
    if existing:
        return error_response("Policy with this name already exists", 400)
        
    policy = await repo.create(policy_in, str(current_user.id))
    return {"data": PolicyResponse.model_validate(policy).model_dump()}

@router.put("/{policy_id}", response_model=Dict[str, Any], dependencies=[Depends(RequireRoles(write_roles))])
async def update_policy(
    policy_id: uuid.UUID,
    policy_in: PolicyUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    repo = PolicyRepository(db)
    policy = await repo.get_by_id(policy_id)
    if not policy:
        return error_response("Policy not found", 404)
        
    if policy_in.name and policy_in.name != policy.name:
        existing = await repo.get_by_name(policy_in.name)
        if existing:
            return error_response("Policy with this name already exists", 400)
        policy.name = policy_in.name
        
    if policy_in.description is not None:
        policy.description = policy_in.description
    if policy_in.action is not None:
        policy.action = policy_in.action
    if policy_in.priority is not None:
        policy.priority = policy_in.priority
    if policy_in.is_active is not None:
        policy.is_active = policy_in.is_active

    if policy_in.condition_risk_min is not None:
        policy.condition_risk_min = policy_in.condition_risk_min
    if policy_in.condition_risk_max is not None:
        policy.condition_risk_max = policy_in.condition_risk_max
    if policy_in.condition_classification is not None:
        policy.condition_classification = policy_in.condition_classification
    if policy_in.condition_status is not None:
        policy.condition_status = policy_in.condition_status

    policy.updated_by = str(current_user.id)
    updated_policy = await repo.update(policy)
    
    return {"data": PolicyResponse.model_validate(updated_policy).model_dump()}
