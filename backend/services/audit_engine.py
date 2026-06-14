import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.observation import Observation
from models.policy import PolicyEvaluation
from models.evidence import Evidence
from schemas.evidence import DecisionProvenanceResponse, EvidenceResponse
from core.logging import logger

class AuditEngineService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_decision_provenance(self, observation_id: uuid.UUID) -> Optional[DecisionProvenanceResponse]:
        """
        Retrieves the complete decision provenance for a given observation.
        Answers: Which Observation? Which Policy? Which Evaluation? Which Evidence? Resulting Action?
        """
        # 1. Fetch Observation
        obs_query = select(Observation).where(Observation.id == observation_id)
        obs_result = await self.session.execute(obs_query)
        observation = obs_result.scalars().first()
        
        if not observation:
            return None

        # 2. Fetch Policy Evaluations
        eval_query = select(PolicyEvaluation).where(PolicyEvaluation.observation_id == observation_id).order_by(PolicyEvaluation.evaluation_time.asc())
        eval_result = await self.session.execute(eval_query)
        evaluations = list(eval_result.scalars().all())

        # 3. Fetch Evidence
        evidence_query = select(Evidence).where(Evidence.observation_id == observation_id).order_by(Evidence.created_at.asc())
        evidence_result = await self.session.execute(evidence_query)
        evidence_list = list(evidence_result.scalars().all())

        # Serialize Evidence
        serialized_evidence = [EvidenceResponse.model_validate(e) for e in evidence_list]

        # Serialize Evaluations (we can just dump them to dicts)
        serialized_evaluations = [
            {
                "id": str(ev.id),
                "policy_id": str(ev.policy_id) if ev.policy_id else None,
                "evaluation_time": ev.evaluation_time.isoformat() if ev.evaluation_time else None,
                "decision_reason": ev.decision_reason,
                "action": ev.action.value
            } for ev in evaluations
        ]

        # 4. Construct Response
        response = DecisionProvenanceResponse(
            observation_id=observation.id,
            status=observation.status.value,
            risk_score=observation.risk_score,
            classification=observation.classification,
            policy_action=observation.policy_action.value if observation.policy_action else None,
            evidence=serialized_evidence,
            evaluations=serialized_evaluations
        )

        # Log metric
        logger.info("metric", extra={"provenance_queries": 1})

        return response
