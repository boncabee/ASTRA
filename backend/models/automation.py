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

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    policy_id = Column(Uuid(as_uuid=True), ForeignKey("policies.id"), nullable=False)
    action = Column(SQLEnum(AutomationAction), nullable=False)
    parameters = Column(JSON, nullable=False, default=dict)
    state = Column(SQLEnum(AutomationState), nullable=False, default=AutomationState.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by = Column(String, nullable=False)
    
    executions = relationship("AutomationExecution", back_populates="request", cascade="all, delete-orphan")

class AutomationExecution(Base):
    __tablename__ = "automation_executions"

    __table_args__ = (
        Index("ix_automation_executions_request_id", "request_id"),
        Index("ix_automation_executions_state", "state"),
        Index("ix_automation_executions_started_at", "started_at"),
    )

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    request_id = Column(Uuid(as_uuid=True), ForeignKey("automation_requests.id"), nullable=False)
    state = Column(SQLEnum(AutomationState), nullable=False, default=AutomationState.QUEUED)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    result_metadata = Column(JSON, nullable=True)
    error_message = Column(String, nullable=True)
    audit_metadata = Column(JSON, nullable=True)

    request = relationship("AutomationRequest", back_populates="executions")
