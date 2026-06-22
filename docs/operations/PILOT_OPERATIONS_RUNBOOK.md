# ASTRA Pilot Operations Runbook

**Document ID:** ASTRA-OPS-PILOT-001  
**Version:** 1.0  
**Audience:** On-call operators managing the ASTRA pilot deployment  

---

## Daily Health Check (run by 09:00 local time)

```bash
# 1. Container status
docker compose -f docker-compose.prod.yml ps

# 2. API health
curl -sk https://<DOMAIN>/api/v1/health | python3 -m json.tool

# 3. Disk usage — alert if > 70%
df -h /

# 4. Confirm last night's backup
ls -lh backups/ | tail -5

# 5. Error log spot-check (last 24h)
docker compose -f docker-compose.prod.yml logs --since 24h 2>&1 | grep -i "error\|critical" | head -20
```

---

## Stack Operations

```bash
# Start / redeploy
bash scripts/deploy.sh

# Graceful shutdown (data preserved)
docker compose -f docker-compose.prod.yml down

# Restart a single service
docker compose -f docker-compose.prod.yml restart <db|backend|frontend|proxy>

# Stream all logs
docker compose -f docker-compose.prod.yml logs -f

# Filter errors in backend
docker compose -f docker-compose.prod.yml logs backend | grep -i error
```

---

## Backup Operations

```bash
# Manual backup
bash scripts/backup.sh

# Verify backup integrity
gunzip -t backups/astra_backup_<timestamp>.sql.gz && echo "VALID" || echo "CORRUPT"

# List all backups
ls -lh backups/

# Clean up backups older than 30 days
find backups/ -name "*.sql.gz" -mtime +30 -delete
```

---

## TLS Certificate Operations

```bash
# Check certificate expiry
echo | openssl s_client -servername <DOMAIN> -connect <DOMAIN>:443 2>/dev/null \
  | openssl x509 -noout -dates

# Force renewal if automated renewal failed
docker compose -f docker-compose.prod.yml run --rm \
  --entrypoint "certbot renew --force-renewal" certbot
docker compose -f docker-compose.prod.yml exec proxy nginx -s reload
```

---

## Database Diagnostics

```bash
# Connect to database
docker compose -f docker-compose.prod.yml exec db psql -U astra_prod -d astra

# Useful queries
SELECT count(*) FROM users;
SELECT count(*) FROM observations WHERE created_at > NOW() - INTERVAL '7 days';
SELECT pg_size_pretty(pg_database_size('astra'));
SELECT count(*), state FROM pg_stat_activity GROUP BY state;
```

---

## Performance Monitoring

```bash
# Container resource usage
docker stats --no-stream

# Check connection pool
docker compose -f docker-compose.prod.yml exec db \
  psql -U astra_prod -d astra -c \
  "SELECT count(*), state FROM pg_stat_activity GROUP BY state;"
```

---

## Maintenance Window Procedure

**Window:** Tuesdays 22:00–23:00 UTC. Notify operators 24h in advance.

```bash
# Before changes: take a manual backup
bash scripts/backup.sh

# Pull latest code and redeploy
git pull origin main
bash scripts/deploy.sh

# Verify health post-deploy
docker compose -f docker-compose.prod.yml ps
curl -sk https://<DOMAIN>/api/v1/health
```

---

## Weekly Review Checklist

```
□ Review /var/log/astra-health.log for past week
□ Confirm 7 nightly backup files exist in backups/
□ Integrity check: gunzip -t backups/<latest>.sql.gz
□ Review open bugs in bug tracker
□ Check login failure rate in backend logs
□ docker stats --no-stream (memory/CPU trend)
□ Record availability % for the week
```

---

## Reference

| Document | Path |
|:---------|:-----|
| Operator Handoff | `docs/history/phase-reports/PHASE_10A_OPERATOR_HANDOFF.md` |
| Incident Response | `docs/operations/PILOT_INCIDENT_RESPONSE.md` |
| Backup Restore | `docs/operations/BACKUP_RESTORE_RUNBOOK.md` |
| Disaster Recovery | `docs/operations/DISASTER_RECOVERY_RUNBOOK.md` |
| Secret Management | `docs/operations/SECRET_MANAGEMENT.md` |
| Troubleshooting | `docs/operations/TROUBLESHOOTING_GUIDE.md` |
