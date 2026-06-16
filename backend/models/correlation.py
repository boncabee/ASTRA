from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from sqlalchemy import String, Boolean, Integer, JSON, ForeignKey, DateTime, Index
from sqlalchemy.types import Uuid
from core.database import Base
from models.mixins import AuditMixin

class CorrelationRule(AuditMixin, Base):
    __tablename__ = "correlation_rules"

    id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    event_types: Mapped[dict] = mapped_column(JSON, nullable=False) # List of strings e.g. ["authentication.failed.login"]
    conditions: Mapped[dict] = mapped_column(JSON, nullable=False) # {"threshold": 5, "actor.username": "admin"}
    time_window: Mapped[int] = mapped_column(Integer, nullable=False) # in seconds
    severity_weight: Mapped[int] = mapped_column(Integer, nullable=False, default=50)

class CorrelationMatch(AuditMixin, Base):
    __tablename__ = "correlation_matches"
    
    __table_args__ = (
        Index("ix_correlation_matches_created_at", "created_at"),
    )

    id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    rule_id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), ForeignKey("correlation_rules.id"), nullable=False, index=True)
    matched_events: Mapped[dict] = mapped_column(JSON, nullable=False) # List of CESEvent UUIDs
    event_count: Mapped[int] = mapped_column(Integer, nullable=False)
    match_timestamp: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    correlation_score: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    context: Mapped[dict | None] = mapped_column(JSON, nullable=True) # {"ips": [], "users": []}
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
