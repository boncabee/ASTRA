from datetime import datetime
from typing import Any
from sqlalchemy.orm import Mapped, mapped_column
import uuid
import enum
from sqlalchemy import String, Text, ForeignKey, Enum as SQLEnum, Index, DateTime, JSON, UniqueConstraint, Boolean
from sqlalchemy.types import Uuid
from sqlalchemy.sql import func
from core.database import Base


# --- Enums ---

class CaseStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    OPEN = "OPEN"
    INVESTIGATING = "INVESTIGATING"
    MITIGATING = "MITIGATING"
    MONITORING = "MONITORING"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"
    CANCELLED = "CANCELLED"


class CasePriority(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class CaseSeverity(str, enum.Enum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class TimelineEventType(str, enum.Enum):
    STATUS_CHANGE = "STATUS_CHANGE"
    ASSIGNMENT = "ASSIGNMENT"
    CASE_CREATED = "CASE_CREATED"
    SYSTEM_ACTION = "SYSTEM_ACTION"


# --- Models ---

class Case(Base):
    """Case aggregate root — central entity for incident/case management."""
    __tablename__ = "cases"

    __table_args__ = (
        Index("ix_cases_status", "status"),
        Index("ix_cases_priority", "priority"),
        Index("ix_cases_severity", "severity"),
        Index("ix_cases_assigned_to", "assigned_to"),
        Index("ix_cases_created_at", "created_at"),
    )

    id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[Any | None] = mapped_column(SQLEnum(CaseStatus), nullable=False, default=CaseStatus.DRAFT)
    priority: Mapped[Any | None] = mapped_column(SQLEnum(CasePriority), nullable=False, default=CasePriority.MEDIUM)
    severity: Mapped[Any | None] = mapped_column(SQLEnum(CaseSeverity), nullable=False, default=CaseSeverity.MEDIUM)
    assigned_to: Mapped[str | None] = mapped_column(String, nullable=True)
    created_by: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class CaseTimeline(Base):
    """Immutable, append-only ledger of all case activity."""
    __tablename__ = "case_timeline"

    __table_args__ = (
        Index("ix_case_timeline_case_id", "case_id"),
        Index("ix_case_timeline_created_at", "created_at"),
    )

    id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    case_id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), ForeignKey("cases.id"), nullable=False)
    event_type: Mapped[Any | None] = mapped_column(SQLEnum(TimelineEventType), nullable=False)
    actor: Mapped[str] = mapped_column(String, nullable=False)
    event_metadata: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class CaseAssignment(Base):
    """Historical record of case assignments."""
    __tablename__ = "case_assignments"

    __table_args__ = (
        Index("ix_case_assignments_case_id", "case_id"),
    )

    id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    case_id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), ForeignKey("cases.id"), nullable=False)
    assigned_user_id: Mapped[str] = mapped_column(String, nullable=False)
    assigned_by: Mapped[str] = mapped_column(String, nullable=False)
    assigned_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class CaseEvidenceLink(Base):
    """Junction table linking Cases to Evidence with soft-unlink capability."""
    __tablename__ = "case_evidence_links"

    __table_args__ = (
        Index("ix_case_evidence_case_id", "case_id"),
        Index("ix_case_evidence_evidence_id", "evidence_id"),
        UniqueConstraint("case_id", "evidence_id", name="uq_case_evidence_link"),
    )

    id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    case_id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), ForeignKey("cases.id"), nullable=False)
    evidence_id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), ForeignKey("evidence.id"), nullable=False)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

