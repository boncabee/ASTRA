import uuid
import enum
from sqlalchemy import Column, String, ForeignKey, Enum as SQLEnum, Index, DateTime, JSON
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

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    observation_id = Column(Uuid(as_uuid=True), ForeignKey("observations.id"), nullable=False)
    evidence_type = Column(SQLEnum(EvidenceType), nullable=False)
    source = Column(String, nullable=False)
    content_reference = Column(String, nullable=False)
    hash_value = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by = Column(String, nullable=False)

class AuditEvent(Base):
    __tablename__ = "audit_events"

    __table_args__ = (
        Index("ix_audit_events_entity", "entity_type", "entity_id"),
        Index("ix_audit_events_timestamp", "timestamp"),
    )

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    entity_type = Column(String, nullable=False)
    entity_id = Column(Uuid(as_uuid=True), nullable=False)
    action = Column(String, nullable=False)
    actor = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    old_value = Column(JSON, nullable=True)
    new_value = Column(JSON, nullable=True)
    reason = Column(String, nullable=True)
