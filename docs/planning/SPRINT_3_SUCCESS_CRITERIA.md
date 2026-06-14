# ASTRA Sprint 3 Success Criteria

Sprint 3 is considered complete when the following measurable outcomes are met:

## 1. Authentication & Authorization
* **User can log in**: A user can successfully authenticate using valid credentials and receive a persona-based JWT.
* **User role restrictions enforced**: A SOC Analyst account attempting to access Administrator configuration endpoints is blocked with a 403 Forbidden error.

## 2. Core Pipeline (End-to-End Workflow)
* **Correlation creates observations**: A predefined set of mock CES events successfully triggers the Correlation Engine MVP to group them into an incident candidate.
* **Observations receive risk score**: The generated incident candidate is passed to the Observation Engine and successfully assigned a numeric Risk Score.
* **Policies evaluate observations**: The Policy Engine processes the Observation, evaluates the Risk Score, and assigns a valid "Recommended Action" (e.g., Observe, Notify).

## 3. User Interface Implementation
* **Observations visible in UI**: The output from the Policy Engine is queryable via API and renders successfully on the Observations Screen and Observation Detail Screen.
* **Events Explorer operational**: Users can view the parsed CES events that form the correlations in the UI.
* **User Management visible**: Administrators can view the Users Screen and see current RBAC assignments.

## 4. Delivery Metric
* The planning package must be detailed enough to immediately create Sprint 3 task breakdowns without further discovery work. (This criteria is satisfied by this planning package).
