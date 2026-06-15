from datetime import datetime
from typing import Any
from sqlalchemy.orm import Mapped, mapped_column
import uuid
import enum
from sqlalchemy import Column, String, ForeignKey, Enum as SQLEnum, Index, DateTime, JSON
from sqlalchemy.types import Uuid
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base

class AutomationAction(str, enum.Enum):
    NOTIFY_WEBHOOK = "NOTIFY_WEBHOOK"
    CREATE_TICKET = "CREATE_TICKET"
    SEND_EMAIL = "SEND_EMAIL"
    LOG_ACTION = "LOG_ACTION"

class AutomationState(str, enum.Enum):
    PENDING = "PENDING"
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class AutomationRequest(Base):
    __tablename__ = "automation_requests"

    __table_args__ = (
        Index("ix_automation_requests_policy_id", "policy_id"),
        Index("ix_automation_requests_state", "state"),
        Index("ix_automation_requests_created_at", "created_at"),
    )

    id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    policy_id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), ForeignKey("policies.id"), nullable=False)
    action: Mapped[Any | None] = mapped_column(SQLEnum(AutomationAction), nullable=False)
    parameters: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    state: Mapped[Any | None] = mapped_column(SQLEnum(AutomationState), nullable=False, default=AutomationState.PENDING)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by: Mapped[str] = mapped_column(String, nullable=False)
    
    executions = relationship("AutomationExecution", back_populates="request", cascade="all, delete-orphan")

class AutomationExecution(Base):
    __tablename__ = "automation_executions"

    __table_args__ = (
        Index("ix_automation_executions_request_id", "request_id"),
        Index("ix_automation_executions_state", "state"),
        Index("ix_automation_executions_started_at", "started_at"),
    )

    id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    request_id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), ForeignKey("automation_requests.id"), nullable=False)
    state: Mapped[Any | None] = mapped_column(SQLEnum(AutomationState), nullable=False, default=AutomationState.QUEUED)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    result_metadata: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    error_message: Mapped[str | None] = mapped_column(String, nullable=True)
    audit_metadata: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    request = relationship("AutomationRequest", back_populates="executions")
