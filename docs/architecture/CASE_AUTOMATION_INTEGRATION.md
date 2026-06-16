# Case Automation Integration

**Phase:** 7
**Project:** ASTRA

## 1. Automation Capabilities
The Case Management module interfaces with the Phase 6 Automation Engine to provide seamless remediation without leaving the Case UI.

## 2. Supported Automated Workflows

### 2.1 Auto-Create Case
Driven by the Policy Engine. Automatically instantiates the Case aggregate root, sets severity based on Observation data, and places it in the `Open` queue.

### 2.2 Auto-Assign Case
Round-robin or load-balanced assignment of `Open` cases to available Analysts within the shift. Handled by an asynchronous worker polling the `Open` queue.

### 2.3 Auto-Escalate Case
If a Case remains in `Investigating` beyond its SLA threshold, a scheduled cron job (or delayed queue task) transitions the Case Priority to `Critical` and reassigns it to the Tier 3 Responder group, appending a Timeline event.

### 2.4 Auto-Close Case
*Strictly Restricted.* ASTRA mandates human-in-the-loop for Case Closure (to `Closed` state). However, a Case can be automatically transitioned to `Resolved` if an automated Threat Intel feed confirms a previously flagged IOC is a known false positive.

## 3. Human-in-the-Loop (Approval Checkpoints)
When an Analyst triggers an Automation Task (e.g., "Block IP on Firewall"):
1. The Automation Engine receives the payload.
2. If the payload is marked `REQUIRES_APPROVAL` (based on RBAC or risk level), the task remains `PENDING`.
3. A Tier 3 Responder or Manager must click "Approve" in the Case UI.
4. The Case Timeline records the Approval signature.
5. The Automation Engine executes the task.

## 4. Rollback and Recovery Strategy
- **Rollback:** Every Automation Task triggered from a Case must have an inverse action defined (e.g., "Unblock IP"). If a mitigation fails or causes an outage, an Analyst can trigger the Rollback task directly from the Case Timeline.
- **Recovery:** If the Automation Engine goes offline, the Case remains in the `Mitigating` state with a task status of `PENDING`. Once the engine recovers, it resumes the queue. Analysts can manually abort a `PENDING` task to revert the Case to `Investigating`.
