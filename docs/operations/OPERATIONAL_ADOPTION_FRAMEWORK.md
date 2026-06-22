# Operational Adoption Framework

## Adoption Strategy
ASTRA is an Enterprise-Grade Self-Hosted platform currently configured for personal operations. The core strategy for adoption is to create a deterministic, lightweight routine that extracts value without excessive administrative overhead. Because SaaS requirements are deferred, the framework focuses strictly on single-tenant reliability, observability, and iterative improvement based on real-world usage data.

## Daily Operations
The daily operational workflow is designed to be minimal but effective, ensuring the platform is healthy before any active use:
- **System Health Check**: Verify core containers (API, DB, Worker, Observability) are running.
- **Queue Inspection**: Ensure the automation queue has no stuck or dead-lettered tasks.
- **Alert Triage**: Review any alerts fired in the past 24 hours in the Grafana/Alertmanager dashboard.
- **Friction Logging**: Note down any usability issues or false positives encountered during the day.

## Weekly Operations
The weekly workflow focuses on maintenance and short-term trends:
- **Log Review**: Scan application logs for non-fatal errors or warnings that aren't triggering alerts.
- **Metric Baseline Check**: Review the past 7 days of CPU, Memory, and Storage utilization against baseline expectations.
- **Feedback Consolidation**: Collect daily friction logs and categorize them into actionable items (Feature Requests vs. Bug Fixes).
- **Security Check**: Review rate-limiting metrics to identify potential brute-force or abuse attempts.

## Monthly Operations
The monthly workflow focuses on strategic platform health, data integrity, and compliance:
- **Backup Verification**: Perform a dry-run restoration of a recent PostgreSQL backup in an isolated container to prove data integrity.
- **Capacity Planning**: Review storage growth and plan for volume expansions if necessary.
- **Incident Retrospective**: Review all `INC-XXXX.md` files from the month to identify systemic issues and prevention effectiveness.
- **Prioritization Review**: Assess the categorized feedback backlog and prioritize improvements for the next development cycle.

## Metrics
To measure the success of ASTRA's operation, the following metrics must be tracked continuously:
- **Uptime Tracking**: Percentage of time the core API and worker are successfully processing requests (Target: 99.9%).
- **Backup Success Tracking**: Success rate of daily automated database snapshots.
- **Restore Validation Tracking**: Monthly verification of restore times and data consistency.
- **Incident Tracking**: Frequency and severity of system failures resulting in degraded service.
- **Resource Utilization Tracking**: CPU, RAM, and Disk I/O consumption relative to the host's capacity.

## Incident Process
When an unexpected failure or degradation occurs, it must be tracked systematically.
- **Location**: Store incident reports in the `docs/incidents/` directory.
- **Naming Convention**: `INC-XXXX.md` (e.g., `INC-0001.md`).
- **Template**: Use the canonical [Incident Template](./INCIDENT_TEMPLATE.md).
- **Workflow**:
  1. **Identify & Mitigate**: Stop the bleeding immediately.
  2. **Document**: Open an `INC-XXXX` file.
  3. **Root Cause**: Perform the mandatory 5-Whys root cause analysis.
  4. **Resolve**: Deploy the fix through standard CI/CD channels.
  5. **Prevent**: Define actionable steps to ensure this specific failure never happens again.

## Feedback Process
To continuously improve ASTRA without speculative architecture work, a structured feedback loop is required:
1. **Friction Logging**: Users log pain points immediately as they occur, capturing context (e.g., "The case search took 4 seconds").
2. **Categorization**: Feedback is categorized into:
   - Feature Requests (missing functionality)
   - Usability Issues (clunky UX/API)
   - False Positives (incorrect rule triggers)
   - Operational Pain Points (difficult maintenance)
3. **Synthesis**: Weekly, these logs are synthesized into distinct, actionable backlog items.

## Prioritization Model
All backlog items, including incident preventions and synthesized feedback, are ranked using the following strict model:
- **P0 Critical**: System is down, data is lost, or security is breached. Must be fixed immediately.
- **P1 Important**: Core functionality is broken but workarounds exist, or significant friction prevents daily adoption. Scheduled for the current/next sprint.
- **P2 Improvement**: Quality of life upgrades, optimizations, and minor feature additions. Scheduled as bandwidth permits.
- **P3 Future**: 'Nice-to-have' ideas or deferred SaaS concepts. Not scheduled.

## Success Criteria
- ASTRA can continuously improve through operational usage without requiring new, speculative architecture work.
- The system is demonstrably stable, proven by documented uptime and verified backups.
- Every system failure results in an `INC` report and a corresponding prevention mechanism.
