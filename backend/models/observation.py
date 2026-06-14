import uuid
import enum
from sqlalchemy import Column, String, Integer, ForeignKey, Enum as SQLEnum, Index
from sqlalchemy.types import Uuid
from core.database import Base
from models.mixins import AuditMixin

class ObservationStatus(str, enum.Enum):
    NEW = "NEW"
    UNDER_REVIEW = "UNDER_REVIEW"
    POLICY_EVALUATED = "POLICY_EVALUATED"
    DISMISSED = "DISMISSED"
    RESOLVED = "RESOLVED"

class PolicyAction(str, enum.Enum):
    OBSERVE = "OBSERVE"
    NOTIFY = "NOTIFY"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    FUTURE_MITIGATION = "FUTURE_MITIGATION"

class Observation(AuditMixin, Base):
    __tablename__ = "observations"

    __table_args__ = (
        Index("ix_observations_status", "status"),
        Index("ix_observations_risk_score", "risk_score"),
        Index("ix_observations_created_at", "created_at"),
    )

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    correlation_id = Column(Uuid(as_uuid=True), ForeignKey("correlation_matches.id"), nullable=False, unique=True, index=True)
    classification = Column(String, nullable=False)
    status = Column(SQLEnum(ObservationStatus), nullable=False, default=ObservationStatus.NEW)
    risk_score = Column(Integer, nullable=False)
    policy_action = Column(SQLEnum(PolicyAction), nullable=True)
    evidence_count = Column(Integer, nullable=False, default=0)
