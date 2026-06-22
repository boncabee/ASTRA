# ASTRA Pilot Incident Response

**Document ID:** ASTRA-OPS-INCIDENT-001  
**Version:** 1.0  
**Audience:** On-call operators and Security Engineering team  

---

## Incident Severity Reference

| Level | Name | Definition | Response Time | Resolution SLA |
|:------|:-----|:-----------|:-------------|:--------------|
| **Sev-1** | Critical | System down OR active breach OR data loss | 15 min | 4 hours |
| **Sev-2** | High | Core feature broken for all users | 1 hour | 24 hours |
| **Sev-3** | Medium | Non-critical feature broken / partial degradation | 4 hours | 72 hours |
| **Sev-4** | Low | Minor bug / cosmetic issue | Next business day | Next sprint |

---

## Sev-1: System Completely Down

**Triggers:** All containers unhealthy, `GET /api/v1/health` returns non-200 or times out.

```bash
# Step 1: Assess state
docker compose -f docker-compose.prod.yml ps
docker compose -f docker-compose.prod.yml logs --tail 50

# Step 2: Attempt full restart
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d

# Step 3: Verify recovery
sleep 30
docker compose -f docker-compose.prod.yml ps
curl -sk https://<DOMAIN>/api/v1/health

# Step 4: If not recovered — escalate to Security Engineering
# Collect logs before restarting again:
docker compose -f docker-compose.prod.yml logs > /tmp/astra-incident-$(date +%Y%m%d%H%M%S).log
```

**Escalate to:** Security Engineering if not recovered within 30 minutes.

---

## Sev-1: Active Security Breach (Credential Compromise)

**Triggers:** Unauthorized access detected in audit logs, suspected secret leakage.

```bash
# Step 1: Immediately rotate JWT secret (invalidates ALL sessions)
NEW_KEY=$(openssl rand -hex 32)
sed -i "s/^JWT_SECRET_KEY=.*/JWT_SECRET_KEY=${NEW_KEY}/" .env
docker compose -f docker-compose.prod.yml restart backend

# Step 2: Rotate database password if implicated
NEW_PASS=$(openssl rand -base64 32)
docker compose -f docker-compose.prod.yml exec db \
  psql -U astra_prod -d astra \
  -c "ALTER USER astra_prod PASSWORD '${NEW_PASS}';"
# Update DATABASE_URL in .env then restart backend

# Step 3: Notify Security Engineering IMMEDIATELY
# Step 4: Preserve evidence — do NOT wipe logs before Security Engineering review
# Step 5: Create incident report (see template below)
```

---

## Sev-1: Database Unavailable

**Triggers:** `astra-db-1` shows `unhealthy` or `exited`.

```bash
# Step 1: Check DB logs
docker compose -f docker-compose.prod.yml logs db --tail 50

# Step 2: Restart DB container
docker compose -f docker-compose.prod.yml restart db

# Step 3: Wait for healthy status (up to 60 seconds)
for i in $(seq 1 12); do
  STATUS=$(docker compose -f docker-compose.prod.yml ps db --format "{{.Status}}")
  echo "DB status: $STATUS"
  [[ "$STATUS" == *"healthy"* ]] && break
  sleep 5
done

# Step 4: If volume corruption suspected — do NOT restart without backup
# Consult DISASTER_RECOVERY_RUNBOOK.md before proceeding
```

---

## Sev-1: Data Loss / Corrupt Database

**Triggers:** Postgres errors indicating table corruption, migration failure, or missing data.

> **Stop all write traffic before restoring.** Shut down backend and frontend first.

```bash
# Step 1: Stop write services
docker compose -f docker-compose.prod.yml stop frontend backend

# Step 2: Identify the latest valid backup
ls -lt backups/ | head -10
gunzip -t backups/astra_backup_<timestamp>.sql.gz

# Step 3: Restore (see BACKUP_RESTORE_RUNBOOK.md for full procedure)
gunzip -c backups/astra_backup_<timestamp>.sql.gz | \
  docker compose -f docker-compose.prod.yml exec -T db \
  psql -U astra_prod -d astra

# Step 4: Restart all services
docker compose -f docker-compose.prod.yml up -d

# Step 5: Verify data integrity
docker compose -f docker-compose.prod.yml exec db \
  psql -U astra_prod -d astra -c "SELECT count(*) FROM users;"
```

---

## Sev-2: Core Feature Broken

**Triggers:** Login fails for all users, policy evaluation fails, case creation fails.

```bash
# Step 1: Check backend for application errors
docker compose -f docker-compose.prod.yml logs backend --tail 100 | grep -i "error\|traceback\|exception"

# Step 2: Check if recent deployment caused the regression
git log --oneline -5

# Step 3: Roll back if deployment-related (see ROLLBACK PROCEDURE below)

# Step 4: If not deployment-related — file Sev-2 bug, assign to engineer
```

---

## Rollback Procedure

```bash
# Step 1: Identify last known good commit
git log --oneline -10

# Step 2: Checkout the known good commit
git checkout <good-commit-sha>

# Step 3: Rebuild and redeploy
bash scripts/deploy.sh

# Step 4: Verify health
docker compose -f docker-compose.prod.yml ps
curl -sk https://<DOMAIN>/api/v1/health

# Step 5: Return to main when fix is merged
git checkout main
git pull origin main
bash scripts/deploy.sh
```

---

## NGINX / Proxy Issues

```bash
# Test NGINX config syntax
docker compose -f docker-compose.prod.yml exec proxy nginx -t

# Reload NGINX without restarting
docker compose -f docker-compose.prod.yml exec proxy nginx -s reload

# Check proxy logs for 502/503
docker compose -f docker-compose.prod.yml logs proxy | grep " 50[23] "
```

**Common cause of 502:** Backend container not healthy when proxy tries to reach it.  
**Fix:** Wait for backend to become healthy, then reload proxy.

---

## Incident Report Template

Create a file named `incidents/INCIDENT-<YYYYMMDD>-<short-title>.md`:

```markdown
# Incident Report: <Short Title>

**Date:** YYYY-MM-DD  
**Severity:** Sev-N  
**Duration:** HH:MM – HH:MM UTC  
**Reported by:**  
**Resolved by:**  

## Timeline

| Time (UTC) | Event |
|:-----------|:------|
| HH:MM | Incident detected via <health check / user report> |
| HH:MM | Operator began investigation |
| HH:MM | Root cause identified |
| HH:MM | Fix applied |
| HH:MM | System verified healthy |

## Root Cause

<Describe the root cause in 2–3 sentences.>

## Impact

- Users affected: N
- Data affected: Yes / No
- Duration: N minutes

## Fix Applied

<Describe the fix.>

## Preventive Measures

<What change or process will prevent this from recurring?>

## Lessons Learned

<What did we learn?>
```

---

## Escalation Contacts

| Tier | Role | When to Contact |
|:-----|:-----|:---------------|
| On-call operator | Primary contact | First responder for all incidents |
| Security Engineering | Escalation | Sev-1 not resolved in 30 min; any security incident |
| Engineering Leadership | Executive escalation | Confirmed data loss; decision to halt pilot |

> Fill in actual contact details (name, Slack handle, phone) before pilot user onboarding.

---

## Reference

| Document | Path |
|:---------|:-----|
| Operations Runbook | `docs/operations/PILOT_OPERATIONS_RUNBOOK.md` |
| Backup Restore | `docs/operations/BACKUP_RESTORE_RUNBOOK.md` |
| Disaster Recovery | `docs/operations/DISASTER_RECOVERY_RUNBOOK.md` |
| Secret Management | `docs/operations/SECRET_MANAGEMENT.md` |
| Troubleshooting | `docs/operations/TROUBLESHOOTING_GUIDE.md` |
| Operator Handoff | `docs/history/phase-reports/PHASE_10A_OPERATOR_HANDOFF.md` |
