# Case Management User Journeys

**Phase:** 7
**Project:** ASTRA

## 1. The Automated Triage Journey (Tier 1 Analyst)
**Trigger:** The Policy Engine evaluates a new Observation with a "Critical" risk score.
1. **Case Creation:** The system automatically creates a Case in the `Open` state. It links the Observation, the raw Correlation events, and the Policy Decision Evidence.
2. **Notification:** The Tier 1 Analyst sees a new Critical Case in their queue.
3. **Assignment:** The Analyst assigns the Case to themselves. The state transitions to `Investigating`. An Audit Event is written.
4. **Investigation:** The Analyst reviews the Evidence Tab. The data is pre-compiled, removing the need to query raw logs.
5. **Mitigation Trigger:** Finding the threat valid, the Analyst triggers an approved Automation task (e.g., "Isolate Host"). The state transitions to `Mitigating`.
6. **Resolution:** The Automation completes successfully. The Analyst marks the Case as `Resolved`, adding a resolution comment.
7. **Closure:** After a 24-hour monitoring period, a SOC Manager reviews the Case and transitions it to `Closed`.

## 2. The Manual Escalation Journey (Tier 2 Responder)
**Trigger:** A Tier 2 Responder is reviewing standard Correlations during a threat hunting exercise.
1. **Discovery:** The Responder notices a suspicious pattern that the Policy Engine flagged as "Low" risk, but their human intuition suggests a coordinated attack.
2. **Manual Creation:** The Responder manually creates a Case from the Correlation record.
3. **Evidence Linking:** The Responder manually queries the Evidence database and links related Audit Events to the Case to build the narrative.
4. **Collaboration:** The Responder @mentions a Tier 3 Engineer in a Case Comment.
5. **Execution:** The team decides to implement a custom block rule. They document the action in the Case Timeline.
6. **Post-Mortem:** Once `Resolved`, the Responder tags the Case with "Needs Rule Tuning" so the Policy Engine rules can be updated for future automated detection.

## 3. The Management Oversight Journey (SOC Manager)
**Trigger:** Daily or weekly operational review.
1. **Queue Review:** The Manager opens the ASTRA Dashboard and views the Case reporting metrics.
2. **SLA Monitoring:** The Manager notices a Case has been in the `Investigating` state for over 48 hours (breaching MTTR SLA).
3. **Intervention:** The Manager reassigns the Case to a senior Analyst and adds a High Priority flag. The Case Timeline immutable logs this reassignment.
4. **Executive Reporting:** At the end of the month, the Manager exports a Compliance Report directly from the Reporting Engine, which correlates Closed Cases with Evidence hashes to prove regulatory compliance.
