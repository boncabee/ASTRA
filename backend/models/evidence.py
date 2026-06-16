from datetime import datetime
from typing import Any
from sqlalchemy.orm import Mapped, mapped_column
import uuid
import enum
from sqlalchemy import String, ForeignKey, Enum as SQLEnum, Index, DateTime, JSON
from sqlalchemy.types import Uuid
from sqlalchemy.sql import func
from core.database import Base

class EvidenceType(str, enum.Enum):
    CORRELATION_MATCH = "CORRELATION_MATCH"
    POLICY_EVALUATION = "POLICY_EVALUATION"
    SYSTEM_EVENT = "SYSTEM_EVENT"
    MANUAL_NOTE = "MANUAL_NOTE"

class Evidence(Base):
    __tablename__ = "evidence"

    __table_args__ = (
        Index("ix_evidence_observation_id", "observation_id"),
        Index("ix_evidence_created_at", "created_at"),
    )

    id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    observation_id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), ForeignKey("observations.id"), nullable=False)
    evidence_type: Mapped[Any | None] = mapped_column(SQLEnum(EvidenceType), nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=False)
    content_reference: Mapped[str] = mapped_column(String, nullable=False)
    hash_value: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by: Mapped[str] = mapped_column(String, nullable=False)

class AuditEvent(Base):
    __tablename__ = "audit_events"

    __table_args__ = (
        Index("ix_audit_events_entity", "entity_type", "entity_id"),
        Index("ix_audit_events_timestamp", "timestamp"),
    )

    id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    entity_type: Mapped[str] = mapped_column(String, nullable=False)
    entity_id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=False)
    action: Mapped[str] = mapped_column(String, nullable=False)
    actor: Mapped[str] = mapped_column(String, nullable=False)
    timestamp: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    old_value: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    new_value: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    reason: Mapped[str | None] = mapped_column(String, nullable=True)
