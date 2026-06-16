from typing import Any
from sqlalchemy.orm import Mapped, mapped_column
import uuid
import enum
from sqlalchemy import String, Integer, ForeignKey, Enum as SQLEnum, Index
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

    id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    correlation_id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), ForeignKey("correlation_matches.id"), nullable=False, unique=True, index=True)
    classification: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[Any | None] = mapped_column(SQLEnum(ObservationStatus), nullable=False, default=ObservationStatus.NEW)
    risk_score: Mapped[int] = mapped_column(Integer, nullable=False)
    policy_action: Mapped[Any | None] = mapped_column(SQLEnum(PolicyAction), nullable=True)
    evidence_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
