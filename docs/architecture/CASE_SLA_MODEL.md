# Case SLA Model Architecture

## Overview
The Case SLA (Service Level Agreement) Model defines the expected timelines for acknowledging and resolving security cases within the ASTRA platform based on their Priority and Severity. 

> [!NOTE]
> This document outlines the architectural design and thresholds for the SLA Engine. The actual SLA Engine implementation, including automated escalations and timer enforcement, is deferred to a future phase and is **not** implemented in Phase 7.

## SLA Definitions

### 1. Response SLA
The maximum allowable time between Case Creation (state: `DRAFT` or `OPEN`) and the first active human interaction (state transition to `INVESTIGATING`).

### 2. Resolution SLA
The maximum allowable time between Case Creation and the neutralization of the threat (state transition to `RESOLVED` or terminal states `CLOSED`/`CANCELLED`).

## SLA Thresholds by Priority

| Priority | Response SLA | Resolution SLA | Escalation Threshold |
|----------|--------------|----------------|----------------------|
| **CRITICAL** | 15 Minutes | 4 Hours | 75% of SLA Elapsed |
| **HIGH** | 1 Hour | 24 Hours | 80% of SLA Elapsed |
| **MEDIUM** | 8 Hours | 3 Days | 85% of SLA Elapsed |
| **LOW** | 24 Hours | 7 Days | 90% of SLA Elapsed |

## Escalation Path
When an SLA crosses the **Escalation Threshold** (e.g., a CRITICAL case is in `OPEN` for 11.25 minutes without transitioning to `INVESTIGATING`), the future SLA Engine will:
1. Generate a high-priority system event.
2. Notify the on-call Incident Commander (via the Notification domain).
3. Automatically reassign or flag the case in the dashboard.

## Future Implementation Requirements
When the SLA Engine is implemented, it must:
- Run asynchronously via the `automation_worker`.
- Emit `TimelineEventType.SYSTEM_ACTION` events into the `case_timeline` when SLAs are breached.
- Be paused if a case transitions to `MONITORING` (time spent monitoring a mitigated threat does not count against Resolution SLA).
