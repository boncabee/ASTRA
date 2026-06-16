from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core.rbac import RequireRoles
from models.user import User, UserRole
from schemas.report import (
    ReportResponse,
    ReportHistoryResponse,
    ReportGenerateRequest,
    ComplianceMappingResponse
)
from repositories.report import ReportRepository
from services.report import ReportService
from api.deps import get_current_user

router = APIRouter(
    dependencies=[Depends(RequireRoles([UserRole.ADMINISTRATOR, UserRole.SECURITY_ENGINEER, UserRole.SOC_ANALYST, UserRole.INCIDENT_RESPONDER]))]
)

# RBAC Definitions
AdminOrEngineer = RequireRoles([UserRole.ADMINISTRATOR, UserRole.SECURITY_ENGINEER])

@router.post("/generate", response_model=ReportResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(AdminOrEngineer)])
async def generate_report(
    request: ReportGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Generate a new standardized report.
    Access: Administrator, Security Engineer
    """
    service = ReportService(db)
    report = await service.generate_report(request, user_id=str(current_user.id))
    return report

@router.get("/history", response_model=List[ReportHistoryResponse])
async def get_report_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get the history of generated reports.
    Access: Administrator, Security Engineer, SOC Analyst, Incident Responder
    """
    repo = ReportRepository(db)
    reports, _ = await repo.get_history(skip=skip, limit=limit)
    return reports

@router.get("/compliance", response_model=List[ComplianceMappingResponse])
async def get_compliance_mappings(
    report_id: UUID = Query(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get compliance mapping lookup for a specific report.
    Access: Administrator, Security Engineer, SOC Analyst, Incident Responder
    """
    repo = ReportRepository(db)
    mappings = await repo.get_compliance_mappings(report_id=report_id)
    return mappings

@router.get("/{id}", response_model=ReportResponse)
async def get_report(
    id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific report by ID.
    Access: Administrator, Security Engineer, SOC Analyst, Incident Responder
    """
    repo = ReportRepository(db)
    report = await repo.get_report(id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@router.get("", response_model=List[ReportResponse])
async def list_reports(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    List all generated reports.
    Access: Administrator, Security Engineer, SOC Analyst, Incident Responder
    """
    repo = ReportRepository(db)
    reports, _ = await repo.list_reports(skip=skip, limit=limit)
    return reports
