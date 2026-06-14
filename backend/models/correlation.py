import uuid
from sqlalchemy import Column, String, Boolean, Integer, JSON, ForeignKey, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID as PGUUID # if postgres is targeted later, but we use string/UUID
from sqlalchemy.types import Uuid
from core.database import Base
from models.mixins import AuditMixin

class CorrelationRule(AuditMixin, Base):
    __tablename__ = "correlation_rules"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    enabled = Column(Boolean, default=True, nullable=False)
    event_types = Column(JSON, nullable=False) # List of strings e.g. ["authentication.failed.login"]
    conditions = Column(JSON, nullable=False) # {"threshold": 5, "actor.username": "admin"}
    time_window = Column(Integer, nullable=False) # in seconds
    severity_weight = Column(Integer, nullable=False, default=50)

class CorrelationMatch(AuditMixin, Base):
    __tablename__ = "correlation_matches"
    
    __table_args__ = (
        Index("ix_correlation_matches_created_at", "created_at"),
    )

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    rule_id = Column(Uuid(as_uuid=True), ForeignKey("correlation_rules.id"), nullable=False, index=True)
    matched_events = Column(JSON, nullable=False) # List of CESEvent UUIDs
    event_count = Column(Integer, nullable=False)
    match_timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    correlation_score = Column(Integer, nullable=False, index=True)
    context = Column(JSON, nullable=True) # {"ips": [], "users": []}
    expires_at = Column(DateTime(timezone=True), nullable=True, index=True)
