from typing import Any
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from enum import Enum
from sqlalchemy import String, Boolean, Enum as SQLEnum, Uuid

from core.database import Base
from models.mixins import AuditMixin

class UserRole(str, Enum):
    ADMINISTRATOR = "Administrator"
    SECURITY_ENGINEER = "Security Engineer"
    INCIDENT_RESPONDER = "Incident Responder"
    SOC_ANALYST = "SOC Analyst"

class User(AuditMixin, Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[Any | None] = mapped_column(SQLEnum(UserRole), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
