# ASTRA User Flow

The following describes the new high-level user and system flow for ASTRA's Observation-based pipeline.

1. **Correlation**: The system correlates normalized events into incident candidates.
2. **Observation**: The Observation Engine translates incidents into evidence-backed observations.
3. **Risk Scoring**: Observations are assigned a risk score based on confidence and historical attack knowledge.
4. **Policy Evaluation**: The Policy Engine evaluates the observation and risk against defined security policies to determine an outcome (observe, notify, create case, automate response).
5. **Action**: The Automation Engine executes the appropriate response actions determined by the Policy Engine.