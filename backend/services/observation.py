import logging
import json
import time
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from models.correlation import CorrelationMatch
from models.observation import Observation, ObservationStatus
from schemas.observation import ObservationCreate
from repositories.observation import ObservationRepository

logger = logging.getLogger("observation_engine")
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)

class ObservationService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = ObservationRepository(session)

    async def process_correlation_match(self, match: CorrelationMatch, run_by_user_id: str) -> Optional[Observation]:
        start_time = time.perf_counter()
        
        # Duplicate Prevention
        existing = await self.repository.get_by_correlation_id(match.id)  # type: ignore
        if existing:
            return existing

        # Mock asset criticality for MVP
        asset_criticality = 50
        event_volume = match.event_count

        # Deterministic Risk Score
        raw_score = match.correlation_score + event_volume + asset_criticality
        risk_score = min(raw_score, 100)

        # Create Observation
        data = ObservationCreate(
            title=f"Observation from Correlation {match.id}",
            description=f"Generated from rule {match.rule_id} with {event_volume} events.",
            correlation_id=match.id,  # type: ignore
            classification="Anomaly",
            status=ObservationStatus.NEW,
            risk_score=risk_score,
            evidence_count=event_volume
        )

        observation = await self.repository.create(data, created_by=run_by_user_id)

        # Logging metrics
        duration_ms = (time.perf_counter() - start_time) * 1000
        metrics = {
            "event": "observation_created",
            "observations_created": 1,
            "average_risk_score": risk_score,
            "processing_duration_ms": duration_ms,
            "correlation_id": str(match.id),
            "observation_id": str(observation.id)
        }
        logger.info(json.dumps(metrics))

        return observation

    async def update_status(self, observation: Observation, new_status: ObservationStatus, updated_by: str) -> Observation:
        start_time = time.perf_counter()
        
        # Validate Transition
        valid_transitions = {
            ObservationStatus.NEW: [ObservationStatus.POLICY_EVALUATED, ObservationStatus.DISMISSED],
            ObservationStatus.POLICY_EVALUATED: [ObservationStatus.UNDER_REVIEW, ObservationStatus.DISMISSED],
            ObservationStatus.UNDER_REVIEW: [ObservationStatus.RESOLVED, ObservationStatus.DISMISSED],
            ObservationStatus.DISMISSED: [],
            ObservationStatus.RESOLVED: []
        }

        if new_status not in valid_transitions.get(observation.status, []):  # type: ignore
            raise ValueError(f"Invalid transition from {observation.status} to {new_status}")

        observation.status = new_status
        observation.updated_by = updated_by
        
        updated = await self.repository.update(observation)

        duration_ms = (time.perf_counter() - start_time) * 1000
        metrics = {
            "event": "observation_updated",
            "observations_updated": 1,
            "processing_duration_ms": duration_ms,
            "observation_id": str(updated.id)
        }
        logger.info(json.dumps(metrics))

        return updated
