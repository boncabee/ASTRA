from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db
from core.rbac import RequireRoles
from models.user import User, UserRole
from models.case import CaseStatus, CasePriority, CaseSeverity
from schemas.case import (
    CaseCreate,
    CaseUpdate,
    CaseResponse,
    CaseStatusChange,
    CaseAssignRequest,
    CaseTimelineResponse,
    CaseEvidenceLinkCreate,
    CaseEvidenceLinkResponse,
)
from services.case import CaseService

router = APIRouter()

# RBAC groupings
ALL_ROLES = [UserRole.SOC_ANALYST, UserRole.INCIDENT_RESPONDER, UserRole.SECURITY_ENGINEER, UserRole.ADMINISTRATOR]
RESPONDER_PLUS = [UserRole.INCIDENT_RESPONDER, UserRole.SECURITY_ENGINEER, UserRole.ADMINISTRATOR]
MANAGER_PLUS = [UserRole.SECURITY_ENGINEER, UserRole.ADMINISTRATOR]


@router.post("", response_model=CaseResponse, status_code=status.HTTP_201_CREATED)
async def create_case(
    data: CaseCreate,
    current_user: User = Depends(RequireRoles(ALL_ROLES)),
    db: AsyncSession = Depends(get_db)
):
    """Create a new case."""
    service = CaseService(db)
    return await service.create_case(data, created_by=current_user.username)


@router.get("", response_model=List[CaseResponse])
async def list_cases(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    case_status: Optional[CaseStatus] = None,
    priority: Optional[CasePriority] = None,
    severity: Optional[CaseSeverity] = None,
    assigned_to: Optional[str] = None,
    current_user: User = Depends(RequireRoles(ALL_ROLES)),
    db: AsyncSession = Depends(get_db)
):
    """List cases with optional filtering and pagination."""
    service = CaseService(db)
    cases, _ = await service.list_cases(
        skip=skip,
        limit=limit,
        status=case_status,
        priority=priority,
        severity=severity,
        assigned_to=assigned_to,
    )
    return cases


@router.get("/{case_id}", response_model=CaseResponse)
async def get_case(
    case_id: UUID,
    current_user: User = Depends(RequireRoles(ALL_ROLES)),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve a single case by ID."""
    service = CaseService(db)
    case = await service.get_case(case_id)
    if not case:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found")
    return case


@router.patch("/{case_id}", response_model=CaseResponse)
async def update_case(
    case_id: UUID,
    data: CaseUpdate,
    current_user: User = Depends(RequireRoles(ALL_ROLES)),
    db: AsyncSession = Depends(get_db)
):
    """Update a case's mutable fields."""
    service = CaseService(db)
    try:
        return await service.update_case(case_id, data, actor=current_user.username)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{case_id}/assign", response_model=CaseResponse)
async def assign_case(
    case_id: UUID,
    data: CaseAssignRequest,
    current_user: User = Depends(RequireRoles(ALL_ROLES)),
    db: AsyncSession = Depends(get_db)
):
    """Assign a case to a user."""
    # SOC Analysts can only assign to themselves
    if current_user.role == UserRole.SOC_ANALYST and data.assigned_user_id != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="SOC Analysts can only assign cases to themselves")

    service = CaseService(db)
    try:
        return await service.assign_case(case_id, data.assigned_user_id, assigned_by=current_user.username)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{case_id}/status", response_model=CaseResponse)
async def change_status(
    case_id: UUID,
    data: CaseStatusChange,
    current_user: User = Depends(RequireRoles(ALL_ROLES)),
    db: AsyncSession = Depends(get_db)
):
    """Change the status of a case."""
    service = CaseService(db)
    assert current_user.role is not None, "User role cannot be None"
    try:
        return await service.change_status(
            case_id, 
            data.new_status, 
            actor=current_user.username, 
            actor_role=current_user.role.value, 
            reason=data.reason
        )
    except ValueError as e:
        # Invalid state transition or not found
        if "not found" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except PermissionError as e:
        # Role gating rejected the transition (e.g., Close/Cancel)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.get("/{case_id}/timeline", response_model=List[CaseTimelineResponse])
async def get_case_timeline(
    case_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(RequireRoles(ALL_ROLES)),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve the timeline of events for a case."""
    service = CaseService(db)
    timeline, _ = await service.timeline_service.get_timeline(case_id, skip=skip, limit=limit)
    return timeline


@router.post("/{case_id}/evidence", response_model=CaseEvidenceLinkResponse, status_code=status.HTTP_201_CREATED)
async def link_evidence(
    case_id: UUID,
    data: CaseEvidenceLinkCreate,
    current_user: User = Depends(RequireRoles(ALL_ROLES)),
    db: AsyncSession = Depends(get_db)
):
    """Link evidence to a case."""
    service = CaseService(db)
    try:
        return await service.link_evidence(case_id, data.evidence_id, actor=current_user.username)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{case_id}/evidence", response_model=List[CaseEvidenceLinkResponse])
async def get_evidence_links(
    case_id: UUID,
    current_user: User = Depends(RequireRoles(ALL_ROLES)),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve all active evidence links for a case."""
    service = CaseService(db)
    return await service.get_evidence_links(case_id)


@router.delete("/{case_id}/evidence/{link_id}", response_model=CaseEvidenceLinkResponse)
async def unlink_evidence(
    case_id: UUID,
    link_id: UUID,
    current_user: User = Depends(RequireRoles(RESPONDER_PLUS)),
    db: AsyncSession = Depends(get_db)
):
    """Soft-unlink evidence from a case."""
    service = CaseService(db)
    try:
        link = await service.soft_unlink_evidence(case_id, link_id, actor=current_user.username)
        if not link:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Link {link_id} not found")
        return link
    except ValueError as e:
        if "does not belong" in str(e).lower() or "not found" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
