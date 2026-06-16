# Import all models here so Alembic can discover them via Base.metadata
from core.database import Base
from models.user import User
from models.correlation import CorrelationRule, CorrelationMatch
from models.observation import Observation
from models.policy import Policy, PolicyEvaluation
from models.evidence import Evidence, AuditEvent
from models.report import Report, ComplianceMapping
from models.automation import AutomationRequest, AutomationExecution
from models.case import Case, CaseTimeline, CaseAssignment, CaseEvidenceLink

__all__ = [
    "Base",
    "User",
    "CorrelationRule",
    "CorrelationMatch",
    "Observation",
    "Policy",
    "PolicyEvaluation",
    "Evidence",
    "AuditEvent",
    "Report",
    "ComplianceMapping",
    "AutomationRequest",
    "AutomationExecution",
    "Case",
    "CaseTimeline",
    "CaseAssignment",
    "CaseEvidenceLink",
]
