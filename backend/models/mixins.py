from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, String

class AuditMixin:
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    created_by = Column(String, nullable=True)
    updated_by = Column(String, nullable=True)
