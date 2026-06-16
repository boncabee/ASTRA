# Sprint Planning Standard

This document governs the execution cycle of ASTRA development sprints. ASTRA utilizes a 2-week Sprint cadence.

## 1. Sprint Inputs
Before a Sprint begins, the following inputs must be finalized:
- **Prioritized Backlog:** A ranked list of User Stories and Tasks.
- **Capacity Plan:** Availability of the engineering and architecture teams.
- **Refined Tasks:** All Tasks must meet the standards defined in `TASK_BREAKDOWN_GUIDELINES.md` (clear AC and DoD).

## 2. Sprint Goals
Every Sprint must have 1-3 distinct, measurable goals that deliver business value or architectural stabilization.
- *Example:* "Establish the core Automation Queue infrastructure" rather than "Complete 15 tickets."

## 3. Risk Assessment
During Sprint Planning, the team must identify and document immediate execution risks:
- Technical Dependencies (e.g., waiting on a specific external library update).
- Resource Bottlenecks.
- Risks are logged in `docs/07-governance/RISK_REGISTER.md` if they pose a threat to the broader Epic.

## 4. Sprint Outputs
At the conclusion of a Sprint, the expected outputs are:
- A shippable increment of the ASTRA platform.
- An updated `SPRINT_COMPLETION_REPORT.md` saved into `docs/08-history/sprint-reports/`.
- Updated documentation (Architecture, API specs, etc.).

## 5. Success Criteria
A Sprint is considered successful if:
1. The Sprint Goals are achieved.
2. All merged code adheres to the 100% test coverage rule.
3. No critical technical debt was introduced without being formally logged in the `TECHNICAL_DEBT_REGISTER.md`.

## 6. Review Process (Sprint Showcase)
At the end of the Sprint, the team will conduct a review:
- Demonstrate the completed Features to stakeholders (Product, Architecture).
- Validate that the implementation matches the `PRD.md` and `SRS.md`.
- Formally accept or reject User Stories.

## 7. Retrospective Process
Immediately following the Review, a Retrospective is held to focus on continuous improvement:
- **What went well?**
- **What needs improvement?**
- **Action Items:** Specific changes to processes or tooling to be implemented in the next Sprint.
