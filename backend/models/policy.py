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

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    action = Column(SQLEnum(PolicyAction), nullable=False)
    priority = Column(Integer, nullable=False, default=100)
    is_active = Column(Boolean, nullable=False, default=True)

    # Conditions
    condition_risk_min = Column(Integer, nullable=True)
    condition_risk_max = Column(Integer, nullable=True)
    condition_classification = Column(String, nullable=True)
    condition_status = Column(SQLEnum(ObservationStatus), nullable=True)

class PolicyEvaluation(Base):
    __tablename__ = "policy_evaluations"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    policy_id = Column(Uuid(as_uuid=True), ForeignKey("policies.id"), nullable=True, index=True)
    observation_id = Column(Uuid(as_uuid=True), ForeignKey("observations.id"), nullable=False, index=True)
    evaluation_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    decision_reason = Column(String, nullable=False)
    action = Column(SQLEnum(PolicyAction), nullable=False)
