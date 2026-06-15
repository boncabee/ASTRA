from datetime import datetime
from typing import Any
from sqlalchemy.orm import Mapped, mapped_column
import uuid
import enum
from sqlalchemy import Column, String, ForeignKey, Enum as SQLEnum, Index, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.types import Uuid
from sqlalchemy.sql import func
from core.database import Base

class ReportType(str, enum.Enum):
    OBSERVATION = "Observation Report"
    INCIDENT = "Incident Report"
    EVIDENCE = "Evidence Report"
    AUDIT = "Audit Report"
    EXECUTIVE_SUMMARY = "Executive Summary Report"

class Report(Base):
    __tablename__ = "reports"

    __table_args__ = (
        Index("ix_reports_created_at", "created_at"),
        Index("ix_reports_type", "report_type"),
    )

    id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    report_type: Mapped[Any | None] = mapped_column(SQLEnum(ReportType), nullable=False)
    scope: Mapped[dict] = mapped_column(JSON, nullable=False) # E.g., time range, specific observation IDs
    data_sources: Mapped[dict] = mapped_column(JSON, nullable=False) # List of sources
    evidence_references: Mapped[dict] = mapped_column(JSON, nullable=False) # List of Evidence IDs or hashes
    audit_references: Mapped[dict] = mapped_column(JSON, nullable=False) # List of Audit Event IDs
    summary: Mapped[str] = mapped_column(String, nullable=False)
    details: Mapped[dict] = mapped_column(JSON, nullable=False)
    
    # Audit trail
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by: Mapped[str] = mapped_column(String, nullable=False)

    compliance_mappings = relationship("ComplianceMapping", back_populates="report", cascade="all, delete-orphan")

class ComplianceMapping(Base):
    __tablename__ = "compliance_mappings"

    __table_args__ = (
        Index("ix_compliance_mappings_report", "report_id"),
        Index("ix_compliance_mappings_framework", "framework"),
    )

    id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    report_id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), ForeignKey("reports.id", ondelete="CASCADE"), nullable=False)
    framework: Mapped[str] = mapped_column(String, nullable=False) # e.g., "ISO 27001", "NIST CSF", "MITRE ATT&CK"
    control_id: Mapped[str] = mapped_column(String, nullable=False) # e.g., "A.12.4.1", "PR.PT-1"
    description: Mapped[str] = mapped_column(String, nullable=False)
    
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    report = relationship("Report", back_populates="compliance_mappings")

