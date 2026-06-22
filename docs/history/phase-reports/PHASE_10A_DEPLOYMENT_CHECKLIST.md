# PHASE 10A: DEPLOYMENT CHECKLIST

**Date:** 2026-06-22  
**Status:** READY FOR OPERATOR EXECUTION  

This checklist must be completed in order. Every item must be verified before the pilot accepts real users or real data.

---

## Phase 1 — Code & CI Readiness

- [ ] GitHub Actions CI is **green** on the latest commit to `main`
  - Gates: Ruff ✅ | MyPy ✅ | Pytest ≥99% ✅ | Gitleaks ✅ | pip-audit ✅ | Bandit ✅ | Docker Build ✅
- [ ] All four P0 findings confirmed resolved (see `PHASE_10_P0_REMEDIATION.md`)
- [ ] All four Pilot Blocker items from Phase 10A confirmed resolved (this phase)

---

## Phase 2 — Infrastructure Provisioning

- [ ] Ubuntu 22.04 LTS host provisioned (minimum: 2 vCPU / 4 GB RAM / 40 GB disk)
- [ ] Docker Engine ≥ 24.x and Docker Compose Plugin ≥ 2.x installed
- [ ] DNS A record for `DOMAIN` pointing to the host's public IP — confirmed with `nslookup`
- [ ] Ports 80 and 443 open in the host firewall
- [ ] Repository cloned to the host: `git clone <repo_url> && cd ASTRA`

---

## Phase 3 — Environment Configuration

- [ ] `.env` created from template: `cp .env.example .env && chmod 600 .env`
- [ ] `DOMAIN` set to the actual pilot domain (not `example.com`)
- [ ] `NEXT_PUBLIC_API_URL` set to `https://<DOMAIN>/api/v1`
- [ ] `BACKEND_CORS_ORIGINS` set to `["https://<DOMAIN>"]`
- [ ] `ENVIRONMENT` is `prod` (must not be changed)
- [ ] `CERTBOT_EMAIL` set to a real admin email for Let's Encrypt notifications
- [ ] `POSTGRES_USER` set (default `astra_prod` is acceptable)
- [ ] `POSTGRES_PASSWORD` generated: `openssl rand -base64 32` — minimum 24 chars
- [ ] `JWT_SECRET_KEY` generated: `openssl rand -hex 32` — must not be the default value
- [ ] `GEMINI_API_KEY` set if AI insights are required (leave empty to disable)
- [ ] All `CHANGE_ME_*` values replaced — none remain

---

## Phase 4 — TLS Certificate Bootstrap

- [ ] `init-letsencrypt.sh` executed: `bash init-letsencrypt.sh`
  - Script reads `DOMAIN` and `CERTBOT_EMAIL` from `.env`
  - Script generates a dummy cert → boots NGINX → issues real Let's Encrypt cert → reloads NGINX
- [ ] `curl -I http://<DOMAIN>` returns `301 Moved Permanently` to HTTPS
- [ ] `curl -I https://<DOMAIN>/api/v1/health` returns `200 OK`
- [ ] Security headers present in response: `Strict-Transport-Security`, `X-Frame-Options`, `X-Content-Type-Options`

---

## Phase 5 — Stack Boot & Runtime Verification

- [ ] `bash scripts/deploy.sh` completes without errors
- [ ] All containers show `healthy` or `running` in `docker compose -f docker-compose.prod.yml ps`
  - `astra-db-1`: `healthy`
  - `astra-backend-1`: `healthy`
  - `astra-frontend-1`: `healthy`
  - `astra-proxy-1`: `running` (no restart loops)
- [ ] `GET https://<DOMAIN>/api/v1/health` → `{"status": "healthy"}`
- [ ] Frontend loads in browser at `https://<DOMAIN>/`
- [ ] Login with a test account succeeds via the frontend

---

## Phase 6 — Rate Limiting Verification

- [ ] Run 6 rapid login attempts to confirm `HTTP 429` on the 6th:
  ```bash
  for i in $(seq 1 6); do
    curl -s -o /dev/null -w "%{http_code}\n" -X POST https://<DOMAIN>/api/v1/auth/login \
      -H "Content-Type: application/x-www-form-urlencoded" \
      -d "username=test&password=test"
  done
  ```
  Expected output: `401 401 401 401 401 429`

---

## Phase 7 — Backup & Recovery Verification

- [ ] Manual backup test: `bash scripts/backup.sh`
  - Output file `backups/astra_backup_<timestamp>.sql.gz` is created and non-zero
- [ ] Verify backup is readable: `gunzip -t backups/astra_backup_*.sql.gz` (exit 0 = valid)
- [ ] Cron job configured for daily backups at 02:00 UTC:
  ```bash
  0 2 * * * cd /path/to/ASTRA && bash scripts/backup.sh >> /var/log/astra-backup.log 2>&1
  ```
- [ ] Offsite backup synchronization configured (manual S3/GCS sync or equivalent)

---

## Phase 8 — Operator Readiness

- [ ] Primary operator has read: `DEPLOYMENT.md`, `BACKUP_RESTORE_RUNBOOK.md`, `DISASTER_RECOVERY_RUNBOOK.md`, `PHASE_10A_OPERATOR_HANDOFF.md`
- [ ] Security incident contact designated and documented
- [ ] Rollback plan identified: known-good git commit SHA recorded, restore procedure understood
- [ ] Health check script deployed (see `PHASE_10A_OPERATOR_HANDOFF.md` for cron template)

---

## Sign-Off

| Check | Operator | Date |
|:------|:---------|:-----|
| All Phase 1–8 items verified | | |
| GitHub Actions green confirmed | | |
| TLS certificate valid for pilot domain | | |
| Backup test passed | | |

**Deployment approved by:** ________________________________  
**Date:** ________________________________
