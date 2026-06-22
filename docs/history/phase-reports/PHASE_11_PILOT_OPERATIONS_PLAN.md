# PHASE 11: PILOT OPERATIONS PLAN

**Date:** 2026-06-22  
**Agent:** ASTRA Pilot Operations Agent  
**Status:** FINAL  
**Phase:** Pilot Operations  

---

## Executive Summary

ASTRA has completed all pre-pilot engineering phases (P0 remediation, pilot blocker fixes, operator handoff package). This document establishes the operational framework governing the pilot period: what success looks like, how the system is monitored, how incidents are handled, and what criteria must be met before transitioning to production.

**Pilot Decision: READY**

All code blockers have been resolved. The operational processes defined here are actionable using the current toolset and documentation suite without any additional code changes.

---

## Pilot Scope

### What Is Being Piloted

| Dimension | Scope |
|:----------|:------|
| Users | Internal security operations team (≤ 10 operators) |
| Duration | 4–8 weeks from first user onboarding |
| Environment | Single self-hosted VM (Small Team Hardened Docker Compose) |
| Data | Real SOC observation data; no external customer data |
| Features | Full feature set as deployed: Observations, Policies, Evidence, Cases, Automation, Reporting |
| Excluded | Kubernetes, multi-node, external alerting integrations (post-pilot) |

### What Is Not Being Piloted

- Automated offsite backup synchronization (manual process required)
- Prometheus/Grafana integrated stack (manual health monitoring in place)
- JWT refresh token flow (users re-authenticate on expiry)
- Account-level lockout beyond IP-based rate limiting

---

## Success Criteria

The pilot is considered **successful** if ALL of the following are true at pilot exit:

| # | Criterion | Measurement Method |
|:--|:---------|:------------------|
| S1 | System available ≥ 95% of pilot calendar time | Health check cron logs |
| S2 | Zero P0 security incidents (no credential compromise, no data exfiltration) | Incident log |
| S3 | Zero unrecoverable data loss events | Backup verification log |
| S4 | ≥ 80% of pilot users can complete core workflows without operator intervention | User feedback survey |
| S5 | All critical bugs (Sev-1) resolved within SLA defined below | Bug triage log |
| S6 | At least one full backup/restore cycle completed and verified | Backup log |
| S7 | GitHub Actions remains green throughout the pilot | CI badge |

---

## Availability Targets

| Tier | Target | Measurement Window | Acceptable Downtime |
|:-----|:------:|:------------------|:-------------------|
| Pilot SLO | 95% | Per pilot week | ≤ 8.4 hours/week |
| Health Check | Every 5 minutes | Continuous | N/A |
| Backup Window | Daily 02:00 UTC | Per day | < 10 min backup duration |

> **Note:** 95% is appropriate for an internal pilot with a small operator group. This will be raised to ≥ 99.5% for public production deployment.

**Planned Maintenance Windows:** Tuesdays 22:00–23:00 UTC. Notify all operators 24 hours in advance via the primary communication channel.

---

## Monitoring Procedure

### Automated Health Checks

The health check cron from `PHASE_10A_OPERATOR_HANDOFF.md` must be deployed on the pilot host:

```bash
# Cron: every 5 minutes
*/5 * * * * /usr/local/bin/astra-health-check.sh
```

The script logs to `/var/log/astra-health.log` and must be extended with a notification (Slack webhook, email, or equivalent) before pilot user onboarding.

### Daily Operator Checklist

Each business day, the on-call operator must verify:

```
□ All containers healthy: docker compose -f docker-compose.prod.yml ps
□ No ERROR-level logs in last 24h: docker compose -f docker-compose.prod.yml logs --since 24h | grep -i error
□ Disk not above 70%: df -h
□ Backup from previous night exists and is non-zero: ls -lh backups/ | tail -5
□ Health endpoint responds: curl -sk https://<DOMAIN>/api/v1/health
```

Log each daily check in the pilot operations log (shared document or ticketing system).

### Weekly Operator Review

Every Monday, the operator team reviews:
- Health log summary (total downtime, if any)
- Backup log (all nightly backups present and valid)
- Login failure rate (potential brute force indicators)
- Docker resource usage trends: `docker stats --no-stream`
- Any open Sev-2 or Sev-3 bugs from the previous week

---

## Incident Severity Levels

| Level | Name | Definition | Response Time | Resolution SLA |
|:------|:-----|:-----------|:-------------|:--------------|
| **Sev-1** | Critical | System completely down OR active security breach OR data loss | 15 minutes | 4 hours |
| **Sev-2** | High | Core feature broken for all users OR significant performance degradation | 1 hour | 24 hours |
| **Sev-3** | Medium | Non-critical feature broken OR degraded for subset of users | 4 hours | 72 hours |
| **Sev-4** | Low | Minor UX issue, cosmetic bug, documentation gap | Next business day | Next sprint |

### Sev-1 Triggers (Immediate Action Required)

- `astra-backend-1` is unhealthy and not recovering within 5 minutes
- `astra-db-1` is unhealthy and not recovering within 5 minutes
- JWT secret or database password suspected compromised
- Unauthorized access detected in audit logs
- All backups from last 72 hours are corrupt or missing

---

## Escalation Path

```
┌─────────────────────────────────────────────────────────────┐
│                     Incident Detected                        │
│           (health check alert / user report)                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  Tier 1: On-Call Operator (Self-Service)                    │
│  • Check docker compose ps and logs                         │
│  • Attempt restart: docker compose restart <service>        │
│  • Reference TROUBLESHOOTING_GUIDE.md                       │
│  Escalate if: not resolved within 30 minutes                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  Tier 2: Security Engineering Team                          │
│  • Sev-1 and Sev-2 incidents                                │
│  • Infrastructure failures requiring elevated access        │
│  • All security-related incidents                           │
│  Escalate if: active breach OR data loss confirmed          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  Tier 3: Engineering Leadership                             │
│  • Confirmed P0-equivalent production incident              │
│  • Decision to initiate full rollback                       │
│  • Data loss impacting pilot users                          │
└─────────────────────────────────────────────────────────────┘
```

---

## Backup Verification Schedule

| Cadence | Action | Owner |
|:--------|:-------|:------|
| **Daily (automated)** | Cron runs `backup.sh` at 02:00 UTC; output logged | System |
| **Daily (operator)** | Verify backup file created and non-zero: `ls -lh backups/` | On-call operator |
| **Weekly (Monday)** | Integrity check: `gunzip -t backups/astra_backup_<latest>.sql.gz` | On-call operator |
| **Week 2 of pilot** | Full restore drill: restore latest backup to a local/test instance | Operator team |
| **Pilot exit** | Final restore verification on a clean environment | Operator team |

Backup logs must be retained for the full pilot duration plus 30 days.

---

## Feedback Collection Process

### Collection Channels

1. **In-session feedback form** — A shared link (Google Form or equivalent) provided to all pilot users. Fields: feature used, issue encountered (if any), severity (1–5), and free-text comments.
2. **Weekly structured interview** — 15-minute async or sync review with each pilot user group in weeks 2 and 4.
3. **Bug reports** — Submitted directly to the bug tracker (GitHub Issues or equivalent) using the Sev-3/Sev-4 template.

### Feedback Review Cadence

| Cadence | Action |
|:--------|:-------|
| Daily | Operator scans for new Sev-1/Sev-2 bug reports |
| Weekly (Monday) | Team reviews all feedback, triages new bugs, identifies trends |
| Pilot midpoint (week 4) | Interim feedback synthesis; assess whether any post-pilot enhancements should be pulled forward |
| Pilot exit | Full feedback synthesis for exit report |

---

## Bug Triage Process

### Submission Template

```
Title: [Sev-N] Short description of the issue
Severity: Sev-1 / Sev-2 / Sev-3 / Sev-4
Component: Backend / Frontend / Proxy / Database / Backup / Docs
Steps to reproduce:
  1. ...
  2. ...
Expected result:
Actual result:
Logs/screenshots attached: Yes / No
```

### Triage Workflow

```
Bug reported
    │
    ▼
Operator assigns preliminary severity (within 1 business day)
    │
    ├─ Sev-1 → Escalate immediately to Security Engineering
    │
    ├─ Sev-2 → Assign to next available engineer; target 24h resolution
    │
    ├─ Sev-3 → Add to sprint backlog; target 72h resolution
    │
    └─ Sev-4 → Log in post-pilot enhancement backlog
```

**No unresolved Sev-1 or Sev-2 bugs may exist at pilot exit.**

### Pilot vs. Post-Pilot Classification

A bug is a **pilot bug** (must fix before pilot exit) if it:
- Prevents a core workflow from completing
- Results in data loss or corruption
- Represents a security regression

A bug is a **post-pilot enhancement** if it:
- Affects non-critical UX
- Has an acceptable workaround documented
- Is architectural in nature (e.g., requires Kubernetes, OTel)

---

## Deployment Review Process

### Minor Updates During Pilot (hotfixes, doc fixes)

1. Create a branch from `main`
2. Implement change; ensure CI passes
3. Merge to `main` (peer review required)
4. Deploy using `bash scripts/deploy.sh` during the next maintenance window
5. Verify health post-deploy: `docker compose -f docker-compose.prod.yml ps`

### Sev-1 Emergency Patches

1. Fix applied directly to `main` with Security Engineering approval
2. CI must pass before deployment (no bypassing GitHub Actions)
3. Deployed immediately outside of maintenance window with operator notification
4. Incident report created and linked to the commit

### Deployment Verification (Post-Every-Deploy)

```bash
# 1. Confirm all containers healthy
docker compose -f docker-compose.prod.yml ps

# 2. Health check
curl -sk https://<DOMAIN>/api/v1/health

# 3. Spot check login
curl -sk -X POST https://<DOMAIN>/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=<test_user>&password=<test_pass>"
```

---

## Pilot Exit Criteria

The pilot may be declared **complete and successful** when ALL of the following are met:

| # | Criterion |
|:--|:---------|
| E1 | Pilot duration ≥ 4 weeks |
| E2 | Availability target (≥ 95%) met across all pilot weeks |
| E3 | Zero unresolved Sev-1 or Sev-2 incidents at exit |
| E4 | At least one successful backup/restore drill completed |
| E5 | All success criteria (S1–S7) met |
| E6 | Pilot user feedback collected and reviewed |
| E7 | Post-pilot enhancement backlog prioritized and documented |
| E8 | Phase 12 (Production Readiness) initiated with post-pilot findings incorporated |

**Pilot exit report:** `PHASE_11_PILOT_EXIT_REPORT.md` to be authored at pilot close.

---

## Final Determination

> **READY**

All operational processes are documented. No code changes are required to begin pilot operations. The operator team has a complete runbook suite covering daily operations, incident response, backup verification, feedback collection, bug triage, and deployment review.

**Prerequisites before first user onboarding:**
1. `PHASE_10A_DEPLOYMENT_CHECKLIST.md` completed in full (GitHub Actions green confirmed)
2. Health check cron deployed and notification integration configured
3. All pilot operators have read this plan and signed the readiness acknowledgment in `PHASE_10A_DEPLOYMENT_CHECKLIST.md`
