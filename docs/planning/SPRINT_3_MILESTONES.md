# ASTRA Sprint 3 Milestones & Readiness

## Milestones

### M1: Authentication Complete
* **Criteria**: User Schema, Auth Service, and RBAC Middleware are fully operational in the backend. 
* **Validation**: API tests prove secure issuance of JWTs and enforcement of role restrictions.

### M2: Correlation Complete
* **Criteria**: Correlation Engine MVP actively groups raw CES events into Correlation incident candidates.
* **Validation**: Database reflects correctly aggregated event correlations.

### M3: Observation Complete
* **Criteria**: `TASK-S3-ARCH-001` is defined; the Observation Engine elevates correlations and applies a distinct Risk Score.
* **Validation**: Observations APIs return scored and status-tracked entities.

### M4: Policy Complete
* **Criteria**: Policy Engine processes Observations and assigns a Recommended Action based on the Risk Score.
* **Validation**: API returns Observation records decorated with the Policy Engine's decision.

### M5: Frontend Integrated
* **Criteria**: The SPA is built and successfully authenticates users, displaying the Dashboard, Events Explorer, Observations list, and detailed Observation screens.
* **Validation**: Manual testing confirms all UI routes map correctly to the backend APIs.

### M6: Sprint Complete
* **Criteria**: All tasks are closed; E2E, Unit, and Performance tests are passing.
* **Validation**: The Definition of Done is fully satisfied.

---

## Definition of Done

Sprint 3 is complete ONLY when the following conditions are explicitly met:

1. **User can authenticate**: The frontend login form yields a valid, secure session.
2. **RBAC is enforced**: The frontend hides unauthorized routes, and the backend explicitly rejects unauthorized API calls.
3. **Correlation generates observations**: Raw telemetry is successfully aggregated by the engine.
4. **Observations receive risk score**: A deterministic algorithm assigns scores properly.
5. **Policies evaluate observations**: Action recommendations (e.g., Observe, Notify) are attached to observations based on score thresholds.
6. **Observations visible in UI**: The full end-to-end flow is demonstrable in the browser.
7. **All critical tests pass**: The test pipeline reports green for Unit, Integration, and E2E layers.

---

## Sprint Readiness Assessment

* **Execution Risk**: **Moderate**. The backend logic transitioning from CES to Correlation to Observation is computationally complex and requires strict adherence to the data contracts.
* **Schedule Risk**: **Moderate**. Implementing both the entire logic pipeline and a brand-new frontend SPA within one sprint is a heavy workload. Strict adherence to the MVP scope and out-of-scope boundaries is required.
* **Architecture Risk**: **Low**. The Architecture Realignment clearly defined the boundaries. Mandating `TASK-S3-ARCH-001` at the start of Phase 3 guarantees no structural misalignment during Observation Engine implementation.
* **Overall Sprint Confidence**: **HIGH**. The task backlog is highly granular, dependencies are linear, and out-of-scope items (Automation, SOAR, AI Gateway) have been firmly walled off. The team can execute these tasks autonomously immediately.
