# Operations Overview

## Philosophy
Operating ASTRA relies on a combination of automated health checks and deterministic runbooks. Because the system is "Enterprise-Grade Self-Hosted," operators have full control and responsibility over the infrastructure.

## Daily Operations
Operators should perform the following checks daily:
1. **Dashboard Review:** Check the Grafana Executive Dashboard for elevated Error rates (5xx) or anomalous latency.
2. **Alert Verification:** Ensure no unresolved firing alerts remain in Alertmanager.
3. **Backup Validation:** Verify that the nightly `pg_dump` succeeded and the resulting gzip file is intact on the host disk.

## Incident Management
If an alert fires or a system anomaly is detected, operators should consult the `PILOT_INCIDENT_RESPONSE.md` playbook. 
Standard steps include:
- Triage: Determine if the issue is Application (code bug), Database (connection pool exhaustion, disk space), or Network.
- Mitigation: If a bad deployment caused the issue, utilize the Rollback Runbook.
- Post-Mortem: All severity 1 and 2 incidents require a blameless post-mortem document.

## Maintenance Windows
As ASTRA currently runs on a single-node architecture, updates (such as updating the Docker image or running Alembic migrations) require brief downtime. Maintenance windows should be scheduled during off-peak hours and communicated to stakeholders.
