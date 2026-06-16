from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from models.report import ReportType

class ComplianceMappingBase(BaseModel):
    framework: str
    control_id: str
    description: str

class ComplianceMappingCreate(ComplianceMappingBase):
    pass

class ComplianceMappingResponse(ComplianceMappingBase):
    id: UUID
    report_id: UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ReportBase(BaseModel):
    report_type: ReportType
    scope: Dict[str, Any]
    data_sources: List[str]
    evidence_references: List[str]
    audit_references: List[str]
    summary: str
    details: Dict[str, Any]

class ReportCreate(ReportBase):
    compliance_mappings: List[ComplianceMappingCreate] = []

class ReportResponse(ReportBase):
    id: UUID
    created_at: datetime
    created_by: str
    compliance_mappings: List[ComplianceMappingResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

class ReportHistoryResponse(BaseModel):
    id: UUID
    report_type: ReportType
    scope: Dict[str, Any]
    summary: str
    created_at: datetime
    created_by: str
    
    model_config = ConfigDict(from_attributes=True)

class ReportGenerateRequest(BaseModel):
    report_type: ReportType
    time_range_start: datetime
    time_range_end: datetime
    data_sources: Optional[List[str]] = None
    include_evidence: bool = True
    include_audit: bool = True
    compliance_frameworks: Optional[List[str]] = None
