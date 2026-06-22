# PHASE 10A: OPERATOR HANDOFF

**Document:** ASTRA Pilot Operator Handoff  
**Date:** 2026-06-22  
**Version:** 1.0  

This document is the primary reference for operators managing the ASTRA pilot deployment. It supplements the detailed runbooks in `docs/operations/` and covers daily operations, health monitoring, rollback, and escalation.

---

## System Overview

ASTRA is deployed as a Hardened Docker Compose stack on a single host VM. The components are:

| Container | Role | Health Check |
|:----------|:-----|:-------------|
| `astra-db-1` | PostgreSQL 15 database | `pg_isready` |
| `astra-backend-1` | FastAPI API (port 8000 internal) | `GET /api/v1/health` |
| `astra-frontend-1` | Next.js frontend (port 3000 internal) | HTTP 200 on `/` |
| `astra-proxy-1` | NGINX reverse proxy (ports 80, 443) | Process running |
| `astra-certbot-1` | Let's Encrypt renewal daemon | Process running |

Networks: `proxy_network` (public-facing), `app_network` (internal, database-only access)

---

## Runbook Summary

### Daily Health Check

Run this manually or add to cron for automated alerting:

```bash
#!/bin/bash
# Save as /usr/local/bin/astra-health-check.sh and chmod +x

DOMAIN="your-domain.com"
HEALTH_URL="https://${DOMAIN}/api/v1/health"

STATUS=$(curl -sk -o /dev/null -w "%{http_code}" "$HEALTH_URL")
if [ "$STATUS" != "200" ]; then
  echo "[$(date)] ALERT: ASTRA health check failed — HTTP ${STATUS}" | \
    tee -a /var/log/astra-health.log
  # Add Slack webhook or email notification here:
  # curl -s -X POST https://hooks.slack.com/services/... -d '{"text":"ASTRA is DOWN"}'
else
  echo "[$(date)] OK: ASTRA health check passed — HTTP ${STATUS}" >> /var/log/astra-health.log
fi
```

Add to cron (every 5 minutes):
```
*/5 * * * * /usr/local/bin/astra-health-check.sh
```

### View Logs

```bash
# All services
docker compose -f docker-compose.prod.yml logs -f

# Specific service
docker compose -f docker-compose.prod.yml logs -f backend
docker compose -f docker-compose.prod.yml logs -f proxy
docker compose -f docker-compose.prod.yml logs -f db
```

### Restart a Service

```bash
docker compose -f docker-compose.prod.yml restart backend
docker compose -f docker-compose.prod.yml restart proxy
```

### Full Stack Restart (no data loss)

```bash
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d
```

### Check Container Status

```bash
docker compose -f docker-compose.prod.yml ps
```

---

## Backup & Restore

### Manual Backup

```bash
bash scripts/backup.sh
# Output: backups/astra_backup_YYYYMMDD_HHMMSS.sql.gz
```

### Verify Backup Integrity

```bash
gunzip -t backups/astra_backup_*.sql.gz && echo "VALID" || echo "CORRUPT"
```

### Restore from Backup

> **Warning:** This overwrites all current data. Confirm the correct backup file.

```bash
# Stop the backend first to prevent new writes
docker compose -f docker-compose.prod.yml stop backend frontend proxy

# Restore
gunzip -c backups/astra_backup_<timestamp>.sql.gz | \
  docker compose -f docker-compose.prod.yml exec -T db \
  psql -U astra_prod -d astra

# Restart
docker compose -f docker-compose.prod.yml up -d
```

---

## Rollback Procedure

If a deployment introduces a regression:

### Step 1 — Identify the Last Known Good Commit

```bash
git log --oneline -10
# Find the commit SHA before the broken deployment
```

### Step 2 — Revert to Previous Version

```bash
# On the pilot host:
git fetch origin
git checkout <last-known-good-sha>
```

### Step 3 — Rebuild and Redeploy

```bash
bash scripts/deploy.sh
```

### Step 4 — Verify Health

```bash
curl -k https://<DOMAIN>/api/v1/health
docker compose -f docker-compose.prod.yml ps
```

### Step 5 — Document the Incident

Create an incident report documenting:
- Which commit caused the regression
- How it was identified
- Actions taken
- Preventive measures for the future

---

## Secret Rotation

If a secret is suspected to be compromised, rotate immediately:

### JWT Secret Key

```bash
# 1. Generate new key
NEW_KEY=$(openssl rand -hex 32)

# 2. Update .env
sed -i "s/^JWT_SECRET_KEY=.*/JWT_SECRET_KEY=${NEW_KEY}/" .env

# 3. Restart backend (invalidates all active sessions)
docker compose -f docker-compose.prod.yml restart backend
```

> All active user sessions will be invalidated. Users must re-login.

### Database Password

```bash
# 1. Generate new password
NEW_PASS=$(openssl rand -base64 32)

# 2. Update password in PostgreSQL
docker compose -f docker-compose.prod.yml exec db \
  psql -U astra_prod -d astra \
  -c "ALTER USER astra_prod PASSWORD '${NEW_PASS}';"

# 3. Update .env
sed -i "s/^POSTGRES_PASSWORD=.*/POSTGRES_PASSWORD=${NEW_PASS}/" .env
# Update DATABASE_URL accordingly

# 4. Restart backend
docker compose -f docker-compose.prod.yml restart backend
```

Refer to `docs/operations/SECRET_MANAGEMENT.md` for the full lifecycle procedure.

---

## TLS Certificate Renewal

Certbot renews automatically every 12 hours. If renewal fails:

```bash
# Check certbot logs
docker compose -f docker-compose.prod.yml logs certbot

# Force manual renewal
docker compose -f docker-compose.prod.yml run --rm certbot certbot renew

# Reload NGINX after renewal
docker compose -f docker-compose.prod.yml exec proxy nginx -s reload
```

---

## Known Pilot Risks and Mitigations

| Risk | Impact | Mitigation |
|:-----|:-------|:-----------|
| No Prometheus/Grafana | Reduced visibility | Use daily health-check cron and `docker stats` |
| CSP `unsafe-inline` | XSS escalation potential | Internal tool; trusted operator base; tracked for post-pilot |
| IP-based rate limiting only | Distributed credential stuffing | Monitor login failure logs; add account lockout post-pilot |
| Loose dep pins (`bcrypt>=`, etc.) | Supply-chain risk | pip-audit in CI catches known CVEs |
| `init-letsencrypt.sh` no staging flag | Let's Encrypt rate limits | Confirm DNS before running; do not run repeatedly |

---

## Support Escalation Path

| Tier | Condition | Contact |
|:-----|:----------|:--------|
| Self-service | Container not healthy | Check logs → restart service → see TROUBLESHOOTING_GUIDE.md |
| On-call operator | All containers down / data inaccessible | Primary operator contacts Security Engineering team |
| Emergency | Active breach / secret compromised | Immediately rotate secrets → notify Security Engineering → create incident report |

---

## Useful Commands Reference

```bash
# Check all service health
docker compose -f docker-compose.prod.yml ps

# Stream all logs
docker compose -f docker-compose.prod.yml logs -f

# Execute a database query
docker compose -f docker-compose.prod.yml exec db \
  psql -U astra_prod -d astra -c "SELECT count(*) FROM users;"

# Check disk usage
df -h && du -sh backups/

# Check resource usage
docker stats --no-stream
```
