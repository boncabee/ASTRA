from typing import Optional, List
import time
from sqlalchemy.ext.asyncio import AsyncSession
from models.observation import Observation, PolicyAction
from models.policy import Policy, PolicyEvaluation
from repositories.policy import PolicyRepository
from core.logging import logger

class PolicyEngineService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.policy_repo = PolicyRepository(session)

    async def evaluate_observation(self, observation: Observation) -> PolicyAction:
        start_time = time.time()
        
        # Fetch all active policies
        active_policies = await self.policy_repo.get_active_policies()
        
        matched_policies: List[Policy] = []
        
        # Evaluate each policy
        for policy in active_policies:
            if self._matches(policy, observation):
                matched_policies.append(policy)

        # Handle matches and conflicts
        decision_reason = "No matching policy found"
        final_action: PolicyAction = PolicyAction.OBSERVE  # type: ignore
        final_policy_id = None
        
        if len(matched_policies) > 0:
            # We already ordered by priority DESC, id ASC in the repository
            # So the highest priority is the first one.
            highest_priority = matched_policies[0].priority
            
            # Find how many matched at this highest priority level to detect conflicts
            conflicting_policies = [p for p in matched_policies if p.priority == highest_priority]
            
            chosen_policy = conflicting_policies[0]
            final_action = chosen_policy.action
            final_policy_id = chosen_policy.id
            decision_reason = f"Matched policy '{chosen_policy.name}' (Priority {chosen_policy.priority})"
            
            if len(conflicting_policies) > 1:
                decision_reason += f". Conflict resolved by ID order among {len(conflicting_policies)} policies at priority {highest_priority}."
                logger.warning(
                    "Policy conflict detected",
                    extra={
                        "observation_id": str(observation.id),
                        "conflicting_policies": [str(p.id) for p in conflicting_policies],
                        "chosen_policy": str(chosen_policy.id)
                    }
                )
                # Metric
                logger.info("metric", extra={"policy_conflicts": 1})
            
            # Metric
            logger.info("metric", extra={"policy_matches": 1})
        else:
            decision_reason = "Fallback to default action (OBSERVE)"
        
        # Create Evaluation Record
        evaluation = PolicyEvaluation(
            policy_id=final_policy_id,
            observation_id=observation.id,
            decision_reason=decision_reason,
            action=final_action
        )
        
        await self.policy_repo.record_evaluation(evaluation)
        
        # Log Metrics
        duration_ms = (time.time() - start_time) * 1000
        logger.info(
            "Policy Evaluation Complete",
            extra={
                "policies_evaluated": len(active_policies),
                "average_evaluation_time_ms": duration_ms, # Since it's a single evaluation, total time = avg
                "observation_id": str(observation.id),
                "final_action": final_action.value
            }
        )
        
        return final_action

    def _matches(self, policy: Policy, observation: Observation) -> bool:
        if policy.condition_risk_min is not None and observation.risk_score < policy.condition_risk_min:
            return False
        if policy.condition_risk_max is not None and observation.risk_score > policy.condition_risk_max:
            return False
        if policy.condition_classification is not None and observation.classification != policy.condition_classification:
            return False
        if policy.condition_status is not None and observation.status != policy.condition_status:
            return False
            
        return True
