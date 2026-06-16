# Case Lifecycle Architecture

**Phase:** 7
**Project:** ASTRA

## 1. State Machine Definition

A Case within ASTRA follows a strict, directed state machine. Transitions outside of this matrix are rejected at the domain layer.

### Allowed States
1. **Draft:** Created manually but not yet formalized. (System-created cases bypass this).
2. **Open:** Formalized and awaiting assignment. SLA timers for MTTA begin here.
3. **Investigating:** Assigned to an Analyst. Active review of evidence is occurring. SLA timers for MTTR begin here.
4. **Mitigating:** Active response measures are being taken (either manual or via Automation Engine).
5. **Monitoring:** Mitigation applied; waiting to verify if the threat is neutralized.
6. **Resolved:** Threat neutralized or deemed false positive.
7. **Closed:** Final QA completed by a Manager. Immutable archive state.
8. **Cancelled:** Created in error or duplicate. (Requires reason).

## 2. Transition Matrix

| Current State | Allowed Next States | Trigger |
| :--- | :--- | :--- |
| **Draft** | Open, Cancelled | Manual Action |
| **Open** | Investigating, Cancelled | Assignment |
| **Investigating** | Mitigating, Resolved | Manual Action |
| **Mitigating** | Monitoring, Investigating, Resolved | Automation Callback or Manual |
| **Monitoring** | Resolved, Investigating | Time-based or Manual |
| **Resolved** | Closed, Investigating | Manager Review / Threat Recurrence |
| **Closed** | *None* (Terminal) | - |
| **Cancelled**| *None* (Terminal) | - |

## 3. Forbidden Transitions
- **Open → Closed:** A case must be investigated and resolved before closure.
- **Investigating → Open:** Reassignment within the Investigating state is allowed, but returning to the Open queue is forbidden to prevent SLA manipulation.
- **Closed → Anything:** Once closed, a Case is cryptographically sealed for compliance. If a new event occurs, a *new* Case must be opened and linked via `Case Relationship`.

## 4. Audit Requirements
Every state transition MUST generate a `Case Timeline` record containing:
- The previous state.
- The new state.
- The timestamp.
- The user (or system) executing the transition.
- An optional transition justification/comment.

## 5. Automation Triggers
- **On Enter `Open`:** Trigger Webhook to ticketing system integration (if configured) or alert SOC channels (Slack/Teams).
- **On Enter `Mitigating`:** Suspend SLA timers. Lock case from manual `Resolved` transition if an Automation Engine task is `RUNNING`.
- **On Enter `Resolved`:** Trigger Phase 5 Reporting Engine to recalculate MTTR metrics.
