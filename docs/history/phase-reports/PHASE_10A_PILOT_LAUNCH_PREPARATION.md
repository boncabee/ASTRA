# PHASE 10A: PILOT LAUNCH PREPARATION

**Date:** 2026-06-22  
**Agent:** ASTRA Pilot Launch Preparation Agent  
**Status:** COMPLETE  
**Scope:** P1 review, triage, pilot blocker fixes, and final launch package assembly  

---

## Executive Summary

Following the P0 remediation sprint (commit `39969fa`), ASTRA had four remaining pilot blockers buried in the P1 category. This phase reviewed all P1, P2, and P3 findings, reclassified each, fixed the pilot blockers, and produced the final operator handoff package.

**Pilot Blocker fixes applied in this phase:**
- P1-001 (`BACKEND_CORS_ORIGINS` undocumented) — Fixed in `.env.example`, `docker-compose.prod.yml`, and `DEPLOYMENT.md`
- P1-004 (orphaned `backup_data` volume) — Removed from `docker-compose.prod.yml`
- P1-005 (`deploy.sh` targeting dev stack) — Rewritten with prod guards and confirmation prompt
- P2-002 (infinite entrypoint wait loop, reclassified as blocker) — Fixed with 60-second timeout and explicit error message

**Final determination: GO WITH CONDITIONS**

---

## P1 Review and Reclassification

| ID | Finding | Classification | Rationale |
|:---|:--------|:--------------:|:----------|
| P1-001 | `BACKEND_CORS_ORIGINS` undocumented | **Pilot Blocker** ✅ Fixed | Operators will get unexplained CORS failures. Blocks all browser-based use. |
| P1-002 | CSP allows `unsafe-inline` / `unsafe-eval` | **Pilot Risk** | Documented in Phase 9.3. Required by Next.js static hydration. Nonce-based CSP is a post-pilot improvement. |
| P1-003 | `release.yml` is a non-functional stub | **Post-Pilot Enhancement** | Pilot operators build from source. No registry required for initial pilot. |
| P1-004 | Orphaned `backup_data` volume declared | **Pilot Blocker** ✅ Fixed | Dead config causes operator confusion and wastes disk reservation. Simple removal. |
| P1-005 | `deploy.sh` targets dev compose file | **Pilot Blocker** ✅ Fixed | An operator using this script deploys the insecure development stack to production. |
| P1-006 | No Prometheus/Grafana in compose | **Pilot Risk** | Metrics endpoint exposed; a separate Prometheus stack can be connected. Operators must manually watch health endpoints during the pilot. |
| P1-007 | No alerting rules defined | **Post-Pilot Enhancement** | Requires a monitoring stack. Cannot be implemented without P1-006 first. |
| P1-008 | No staging environment documented | **Pilot Risk** | Pilot is by definition the staging environment. Document in handoff notes. |

**P2-002 Reclassification:**

P2-002 (infinite wait loop in `entrypoint.sh`) was reclassified from **P2** to **Pilot Blocker**. An infinite hang on a misconfigured `DATABASE_URL` produces no output and causes the container to appear stuck indefinitely, making it impossible for an operator to diagnose their configuration error. Fixed with a 60-second timeout.

---

## Remaining Risks

### Pilot Risks (Accept and Monitor)

| ID | Risk | Mitigation |
|:---|:-----|:-----------|
| P1-002 | CSP `unsafe-inline` permits XSS escalation | ASTRA is a self-hosted internal tool; risk surface is limited to internal trusted operators. Nonce-based CSP tracked as post-pilot. |
| P1-006 | No integrated Prometheus/Grafana | Operator must monitor `/api/v1/health` and Docker logs manually during pilot. A cron-based health check alert is documented in `OPERATOR_HANDOFF.md`. |
| P1-008 | No formal staging environment | The pilot _is_ the staging environment. DEPLOYMENT.md updated to clarify. |
| P2-001 | `init-letsencrypt.sh` has no `--staging` flag | Operators must not run the script repeatedly without DNS confirmed. Documented in handoff. |
| P2-003 | Loose dependency pins | Supply-chain risk exists but pip-audit in CI catches known CVEs. Acceptable for initial pilot. |
| P2-006 | SQLAlchemy default pool settings | Under low pilot load, defaults (5 connections, overflow 10) are acceptable. Monitor and tune if timeouts occur. |

### Post-Pilot Enhancements (Not Required for GO)

| ID | Enhancement |
|:---|:-----------|
| P1-003 | Implement GHCR image registry push in `release.yml` |
| P1-007 | Define Alertmanager rules for DB unavailability and error-rate thresholds |
| P2-004 | Add Docker log rotation driver config to compose services |
| P2-005 | Multi-stage frontend Dockerfile for smaller image |
| P2-007 | Document `GEMINI_API_KEY` graceful degradation behavior |
| P2-008 | Generate SBOM in CI (Syft/CycloneDX) |
| P3-001 | Kubernetes/Helm scale-out path |
| P3-002 | Account-level lockout (IP-based rate limiting currently in place) |
| P3-003 | JWT refresh token flow |
| P3-004 | Automated offsite backup synchronization |
| P3-005 | OpenTelemetry distributed tracing |
| P3-006 | Configure Dependabot/Renovate for dependency updates |

---

## Files Modified

| File | Change | Finding |
|:-----|:-------|:--------|
| `.env.example` | Added `BACKEND_CORS_ORIGINS`, `CERTBOT_EMAIL` with documentation | P1-001 |
| `docker-compose.prod.yml` | Added `BACKEND_CORS_ORIGINS` env var; removed orphaned `backup_data` volume | P1-001, P1-004 |
| `scripts/deploy.sh` | Rewritten to target `docker-compose.prod.yml` with prod guard and confirmation prompt | P1-005 |
| `backend/entrypoint.sh` | Added 60-second timeout with explicit error message to database wait loop | P2-002 (reclassified) |
| `docs/operations/DEPLOYMENT.md` | Added `ENVIRONMENT=prod`, `BACKEND_CORS_ORIGINS`, `CERTBOT_EMAIL` to required vars | P1-001 |

---

## Validation Results

| Gate | Result |
|:-----|:------:|
| `docker compose -f docker-compose.prod.yml config` | ✅ Valid |
| `ruff check .` (backend) | ✅ All checks passed |
| `entrypoint.sh` timeout logic | ✅ Correct bash arithmetic |
| `deploy.sh` ENVIRONMENT guard | ✅ Exits non-zero on missing/wrong value |

---

## GitHub Results

All changes submitted to `main`. GitHub Actions will execute:
- Ruff → MyPy → Pytest (≥99% coverage) → Gitleaks → pip-audit → Bandit → Docker Build

> Verify the CI badge in `README.md` is green before completing the operator handoff.

---

## Final Determination

> **GO WITH CONDITIONS**

**Conditions:**
1. GitHub Actions must be green on the latest commit to `main`.
2. Operator must complete `PHASE_10A_DEPLOYMENT_CHECKLIST.md` in full before placing real data on the system.
3. P1-006 (no Prometheus) is accepted as a pilot risk; operator must implement the manual health monitoring procedure described in `PHASE_10A_OPERATOR_HANDOFF.md`.
