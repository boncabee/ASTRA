from datetime import datetime
from typing import Any
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Enum as SQLEnum, Index, DateTime
from sqlalchemy.types import Uuid
from sqlalchemy.sql import func
from core.database import Base
from models.mixins import AuditMixin
from models.observation import ObservationStatus, PolicyAction

class Policy(AuditMixin, Base):
    __tablename__ = "policies"

    __table_args__ = (
        Index("ix_policies_priority", "priority"),
        Index("ix_policies_is_active", "is_active"),
    )

    id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    action: Mapped[Any | None] = mapped_column(SQLEnum(PolicyAction), nullable=False)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # Conditions
    condition_risk_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    condition_risk_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    condition_classification: Mapped[str | None] = mapped_column(String, nullable=True)
    condition_status: Mapped[Any | None] = mapped_column(SQLEnum(ObservationStatus), nullable=True)

class PolicyEvaluation(Base):
    __tablename__ = "policy_evaluations"

    id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    policy_id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), ForeignKey("policies.id"), nullable=True, index=True)
    observation_id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), ForeignKey("observations.id"), nullable=False, index=True)
    evaluation_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    decision_reason: Mapped[str] = mapped_column(String, nullable=False)
    action: Mapped[Any | None] = mapped_column(SQLEnum(PolicyAction), nullable=False)
