import uuid
from enum import Enum
from sqlalchemy import Column, String, Boolean, Enum as SQLEnum, Uuid

from core.database import Base
from models.mixins import AuditMixin

class UserRole(str, Enum):
    ADMINISTRATOR = "Administrator"
    SECURITY_ENGINEER = "Security Engineer"
    INCIDENT_RESPONDER = "Incident Responder"
    SOC_ANALYST = "SOC Analyst"

class User(AuditMixin, Base):
    __tablename__ = "users"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
