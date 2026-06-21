# PHASE 10: PILOT DEPLOYMENT READINESS ASSESSMENT

**Date:** 2026-06-21  
**Assessor:** ASTRA Pilot Deployment Readiness Agent  
**Status:** FINAL  
**Scope:** Full-stack pilot deployment readiness across all operational dimensions  

---

## Executive Summary

ASTRA has completed a substantial and well-documented journey through Phases 6–9, culminating in a hardened Docker Compose production stack with TLS termination, rate limiting, structured observability, non-root containers, backup automation, and immutable audit trails. The engineering quality gates enforced by GitHub Actions (Ruff, Bandit, pip-audit, Gitleaks, 99% test coverage) represent a strong software supply-chain posture.

However, this assessment has uncovered **four Critical (P0) findings** that must be remediated before a real pilot deployment can proceed safely. The most severe is a **broken production safety guard**: `ENVIRONMENT=prod` is never injected into the production compose stack, meaning the `config.py` validator that prevents insecure defaults from booting is silently inert. A pilot operator who copies `.env.example` without changing `JWT_SECRET_KEY` will boot a production instance using the well-known default key `supersecretkey_please_override_in_env` with **no warning and no crash**. This is a cryptographic security failure that invalidates the core security design.

The remaining P0 findings address a broken backup format, a missing MyPy gate in CI despite it being listed as a mandatory quality gate, and an incompatible Dockerfile base image. These issues, taken together, constitute a **NO-GO** on the current codebase state.

The project is architecturally mature and close to ready. All P0 findings are remediable within one focused sprint. The recommended disposition is **GO WITH CONDITIONS** once all P0 items are resolved and verified by a passing GitHub Actions run.

---

## Readiness Assessment

| Dimension | Status | Summary |
|:---|:---:|:---|
| Production Architecture | ⚠️ Conditional | Sound design; broken ENVIRONMENT gate undermines all security guarantees |
| Deployment Process | ⚠️ Conditional | Functional but deploy.sh targets dev stack; release pipeline is a stub |
| Runtime Operations | ✅ Pass | Idempotent startup, health checks, restart policies all functional |
| Security Posture | ❌ Fail | Production guard bypassed; CSP weak; CORS wildcard; backup format bug |
| Observability | ⚠️ Conditional | Metrics exposed; no Prometheus/Grafana stack; no alerting rules |
| Backup & Recovery | ❌ Fail | `pg_dump -F c` piped through `gzip` produces a corrupt archive |
| Secrets Management | ⚠️ Conditional | Good lifecycle doc; `ENVIRONMENT=prod` never set; guard is dead letter |
| Abuse Protection | ✅ Pass | Rate limiting operational; IP spoofing risk noted and documented |
| Documentation Quality | ✅ Pass | Comprehensive suite; minor deployment guide gaps |
| Operator Experience | ⚠️ Conditional | TLS bootstrap script present; no staging flag; rollback script is minimal |

---

## P0 Findings — Pilot Blockers

These findings must be resolved before any real users or real data are placed on ASTRA. Each represents a condition where the system will silently fail to enforce its own security contract.

---

### P0-001 — Production Safety Guard Is a Dead Letter

**Dimension:** Security / Secrets Management  
**Files:** `docker-compose.prod.yml`, `.env.example`, `backend/core/config.py`

**Finding:**  
`backend/core/config.py` contains a `model_validator` that refuses to start if `JWT_SECRET_KEY` equals the insecure default `supersecretkey_please_override_in_env` — but only when `ENVIRONMENT == "prod"`. Neither `docker-compose.prod.yml` nor `.env.example` sets `ENVIRONMENT=prod`. The default value in `config.py` is `ENVIRONMENT: str = "dev"`.

**Impact:**  
Any pilot operator who copies `.env.example` and forgets to change `JWT_SECRET_KEY` (a common mistake) will boot a production instance with the well-known default key. The validator that is supposed to catch this will never fire because the application sees `ENVIRONMENT=dev`. All JWTs issued under this key are trivially forgeable by anyone who has read the source code.

**Evidence:**
```python
# core/config.py line 8
ENVIRONMENT: str = "dev"

# core/config.py line 30
if self.ENVIRONMENT == "prod":   # Never true without explicit injection
    if self.JWT_SECRET_KEY == "supersecretkey_please_override_in_env":
        raise ValueError(...)
```
```yaml
# docker-compose.prod.yml — backend environment section (lines 53-58)
environment:
  - DATABASE_URL=${DATABASE_URL}
  - JWT_SECRET_KEY=${JWT_SECRET_KEY}
  - GEMINI_API_KEY=${GEMINI_API_KEY}
  - LOG_LEVEL=${LOG_LEVEL:-INFO}
  - PRIVACY_MODE=${PRIVACY_MODE:-true}
  # ENVIRONMENT is not set — application defaults to "dev"
```

**Remediation:**  
Add `ENVIRONMENT=prod` to both `docker-compose.prod.yml` and `.env.example`. Validate in CI that the gate fires correctly.

---

### P0-002 — Backup Script Produces Corrupt Archives

**Dimension:** Backup & Recovery  
**File:** `scripts/backup.sh`

**Finding:**  
`backup.sh` invokes `pg_dump -F c` (custom binary format) then pipes the output through `gzip`. The PostgreSQL custom format (`-F c`) is already a compressed binary format. Piping it through `gzip` wraps binary data in a second, incompatible compression layer. The resulting `.sql.gz` file cannot be restored with `pg_restore` or `gunzip | psql`. Every automated backup being produced is unrestorable.

**Evidence:**
```bash
# scripts/backup.sh line 20
docker compose exec -T db pg_dump -U "$DB_USER" -d "$DB_NAME" -F c | gzip > "$BACKUP_FILE"
# -F c = custom binary format (already compressed internally)
# piping to gzip = double-wrapped, incompatible with pg_restore
```

**Impact:**  
The backup automation is silently broken. A DR event requiring a restore from these archives will fail at the worst possible moment. RPO/RTO commitments documented in `DISASTER_RECOVERY_RUNBOOK.md` cannot be met.

**Remediation:**  
Either use plain SQL format (`-F p`) with gzip compression, or use custom format without gzip:
- Option A: `pg_dump -U "$DB_USER" -d "$DB_NAME" | gzip > "$BACKUP_FILE"` (plain SQL + gzip)
- Option B: `pg_dump -U "$DB_USER" -d "$DB_NAME" -F c -f "/tmp/backup.dump"` then copy out (no gzip)
  
Verify the restore script is aligned with whichever format is chosen.

---

### P0-003 — MyPy Is Absent from CI Despite Being a Mandatory Gate

**Dimension:** Deployment Process / CI  
**File:** `.github/workflows/ci.yml`

**Finding:**  
`README.md` section 14 explicitly lists "Zero MyPy type-checking errors" as a required merge gate. `PHASE_8_5_BACKUP_DISASTER_RECOVERY_REPORT.md` and multiple other phase reports list MyPy as a validated gate. However, the actual `ci.yml` workflow does not contain a MyPy step. The quality gate is not enforced in any CI job.

**Evidence:**
```yaml
# .github/workflows/ci.yml — no mypy step present
# Actual gates enforced: ruff, pytest --cov, bandit, pip-audit, gitleaks, docker build
```
```markdown
# README.md line 107
- Zero MyPy type-checking errors
```

**Impact:**  
Type errors introduced by contributors are not caught before merge. The compliance posture described in governance documents (NIST SSDF, OWASP SAMM mappings) claims type safety enforcement that does not exist at the CI layer. Phase reports citing "MyPy: PASSED" were validated locally, not by GitHub Actions (the Source of Truth per project standards).

**Remediation:**  
Add a MyPy step to `ci.yml` under the `lint-and-test-backend` job:
```yaml
- name: Type check with mypy
  working-directory: ./backend
  run: |
    pip install mypy
    mypy .
```
Ensure `mypy.ini` at the repo root is properly scoped and that the step passes on the current codebase before merging.

---

### P0-004 — Backend Dockerfile Uses Pre-Release Python Base Image

**Dimension:** Production Architecture  
**File:** `backend/Dockerfile`

**Finding:**  
`backend/Dockerfile` uses `FROM python:3.14-slim`. Python 3.14 is in alpha/beta development phase and is **not a stable release**. Pre-release Python images receive no security patches, may have undocumented behavioral changes, and are not supported by most security scanning tools (Trivy, Snyk). This means the Docker security scan step in CI is operating against an image that cannot be properly assessed for CVEs.

**Evidence:**
```dockerfile
# backend/Dockerfile line 1
FROM python:3.14-slim
```

**Impact:**  
Production containers are built on an unsupported, unpatched base image. The `devsecops_standard.md` states: "Base images must be kept up to date (e.g., `python:3.12-slim`). Images with Critical OS-level vulnerabilities cannot be deployed to production." This deployment violates the project's own standard.

**Remediation:**  
Pin to the current stable release: `FROM python:3.12-slim`. Verify all tests pass after the downgrade, as 3.14 alpha features could have been inadvertently relied upon.

---

## P1 Findings — Must Fix Before Public Deployment

### P1-001 — CORS Configuration Allows Wildcard in Development; No Production Override Mechanism

**Dimension:** Security  
**File:** `backend/core/config.py`

**Finding:**  
`BACKEND_CORS_ORIGINS` defaults to `["http://localhost:3000"]`. There is no documented method in `.env.example` or `DEPLOYMENT.md` for operators to override this value to their actual production domain. While the default is not a wildcard, operators running a production server at `https://my-soc.company.com` will have CORS blocked entirely unless they know to manually set this variable. The deployment guide does not mention it.

**Remediation:**  
Add `BACKEND_CORS_ORIGINS=https://${DOMAIN}` to `.env.example` and document it in `DEPLOYMENT.md`.

---

### P1-002 — Content-Security-Policy Allows `unsafe-inline` and `unsafe-eval`

**Dimension:** Security  
**File:** `nginx/default.conf.template`

**Finding:**  
The CSP header (noted as a known risk in Phase 9.3) permits `'unsafe-inline'` and `'unsafe-eval'` across script-src. For a security platform processing sensitive SOC data, this significantly weakens XSS defenses. A stored XSS vulnerability in any frontend component would have full scope.

**Remediation:**  
Implement nonce-based CSP for the Next.js frontend. This requires a Next.js `nonce` middleware to generate per-request nonces and inject them into the CSP header dynamically.

---

### P1-003 — `release.yml` Is a Non-Functional Stub

**Dimension:** Deployment Process  
**File:** `.github/workflows/release.yml`

**Finding:**  
The release workflow builds Docker images but the "Push to Registry" step executes `echo "Manual approval required to push"` — it does not push anything. There is no container registry configured. ASTRA has no formal release artifact. Deploying a new version requires operators to re-clone and rebuild from source, creating reproducibility and rollback risks.

**Remediation:**  
Implement a complete release pipeline: push tagged images to GitHub Container Registry (GHCR) and update `DEPLOYMENT.md` to allow operators to pull pre-built images instead of building from source.

---

### P1-004 — `backup_data` Volume Declared But Never Mounted

**Dimension:** Backup & Recovery  
**File:** `docker-compose.prod.yml`

**Finding:**  
`docker-compose.prod.yml` declares a `backup_data` volume in the `volumes:` section (line 90) but this volume is not mounted to any service. The comment in Phase 9.2 report notes "a dedicated `backup_data` volume inside compose is unnecessary" — but the orphaned volume declaration adds confusion and waste.

**Remediation:**  
Remove the `backup_data` volume declaration from `docker-compose.prod.yml` to eliminate dead configuration.

---

### P1-005 — `scripts/deploy.sh` Targets the Development Compose File

**Dimension:** Deployment Process  
**File:** `scripts/deploy.sh`

**Finding:**  
`scripts/deploy.sh` executes `docker compose -f docker-compose.yml up -d`, pointing to the development compose file, not `docker-compose.prod.yml`. An operator running this script against a production server would deploy the insecure development stack.

**Remediation:**  
Update `deploy.sh` to use `docker-compose.prod.yml` and add a guard requiring the operator to confirm the production context.

---

### P1-006 — No Prometheus/Grafana Scraping Stack in Production Compose

**Dimension:** Observability  
**File:** `docker-compose.prod.yml`

**Finding:**  
ASTRA exposes `/metrics` for Prometheus scraping, but no Prometheus or Grafana service is included in `docker-compose.prod.yml`. The `OBSERVABILITY_STANDARD.md` mandates dashboards for Executive Health, Ingestion Pipeline, and Automation Health. Without a scraper, the metrics endpoint is instrumented but silent.

**Impact:**  
Operators have no visibility into ASTRA's runtime health, latency, error rates, or queue depth during the pilot. Incidents will only be discovered reactively through user reports.

**Remediation:**  
Add a minimal `prometheus` + `grafana` service pair to `docker-compose.prod.yml` with a pre-configured `prometheus.yml` scrape config and a base Grafana datasource. This is a pilot-grade observability minimum.

---

### P1-007 — No Alerting Rules Defined

**Dimension:** Observability  
**File:** N/A (gap)

**Finding:**  
The `OBSERVABILITY_STANDARD.md` specifies PagerDuty/OpsGenie for critical alerts and Slack for warnings. No alert rules, alertmanager configuration, or Slack webhook integration exists in the codebase. During a pilot, a database crash or ingestion queue overflow would go unnoticed unless someone is actively watching dashboards.

**Remediation:**  
Define a minimal alertmanager ruleset covering: database unavailability, backend health-check failure, and >10% error rate on critical endpoints. Document the webhook integration process in the operations runbook.

---

### P1-008 — No Staging Environment Defined or Documented

**Dimension:** Deployment Process  
**File:** `docs/operations/DEPLOYMENT.md`

**Finding:**  
`DEPLOYMENT.md` lists "Staging" as a deployment environment but provides no content beyond the word "Validation". There is no staging compose file, no staging CI job, and no instructions for provisioning a staging instance. The DEVSECOPS standard references nightly DAST scans against staging — these cannot run without a staging environment.

**Remediation:**  
For a controlled pilot, at minimum document that staging runs on the same `docker-compose.prod.yml` with staging-specific `.env` values. Add a `ci-staging.yml` workflow or reference the manual staging validation procedure.

---

## P2 Findings — Recommended Improvements

### P2-001 — `init-letsencrypt.sh` Has No `--staging` Flag for Let's Encrypt

**Finding:** The TLS bootstrap script uses Let's Encrypt production endpoints. Repeated failed runs (e.g., during DNS troubleshooting) will hit Let's Encrypt rate limits (5 certificate failures per hour). A `--staging` flag to use the Let's Encrypt staging ACME endpoint would protect operators during setup without consuming production certificate quotas.

---

### P2-002 — `entrypoint.sh` Has an Infinite Wait Loop With No Timeout

**Finding:** The backend `entrypoint.sh` loops indefinitely with `while ! alembic current ...`. If the database never becomes available (e.g., misconfigured `DATABASE_URL`), the container spins forever and emits no clear error. A configurable timeout (e.g., 60 seconds) with an explicit failure message would surface misconfigurations faster.

---

### P2-003 — Loose Dependency Pinning in `requirements.txt`

**Finding:** `bcrypt>=4.0.0`, `PyJWT>=2.8.0`, `python-multipart>=0.0.9`, and `email-validator>=2.1.0` use minimum version pins. This was flagged in the Phase 8.2 audit and remains unresolved. Loose pins create non-reproducible builds and supply-chain risk. All dependencies should be pinned to exact versions (`==`) and managed with a lock file or `pip-compile`.

---

### P2-004 — Docker Log Rotation Not Configured in Production Compose

**Finding:** Phase 9.0 reference architecture explicitly noted: "The Host VM should be configured to rotate Docker JSON logs to prevent disk exhaustion (`max-size: '10m'`, `max-file: '3'`)." No `logging:` driver configuration exists in `docker-compose.prod.yml`. On a busy pilot instance, unrotated container logs will eventually fill the host disk.

**Remediation:** Add to each service in `docker-compose.prod.yml`:
```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

---

### P2-005 — Frontend Is Not a Multi-Stage Docker Build

**Finding:** `frontend/Dockerfile` is a single-stage build that installs dev dependencies (`npm ci` installs everything in `package.json` including devDependencies) and builds within the same layer. A multi-stage build (`builder` → `runner`) would produce a significantly smaller, more secure image by excluding build tooling from the final artifact.

---

### P2-006 — No Database Connection Pool Configuration

**Finding:** Phase 8.2 flagged this: "PostgreSQL connections lack explicit pooling configuration (relies on SQLAlchemy defaults)." Under pilot load, default pool settings (5 connections, overflow 10) may be insufficient and will cause request timeouts rather than graceful queue behavior. Document recommended pool settings in `.env.example`.

---

### P2-007 — `GEMINI_API_KEY` Is Optional But Undocumented in Context

**Finding:** `.env.example` comments: "Required for observability engine / AI insights" — but the application appears to start without it. It is unclear which features are degraded without this key. Document the graceful degradation behavior and whether a pilot deployment without AI insights is a valid configuration.

---

### P2-008 — No SBOM Generated in CI

**Finding:** `DEVSECOPS_STANDARD.md` section 6 mandates SBOM generation for every formal release using Syft or CycloneDX. The `release.yml` workflow builds images but generates no SBOM. This is required for supply-chain transparency and regulatory traceability.

---

## P3 Findings — Future Enhancements

### P3-001 — No Kubernetes / Helm Chart for Scale-Out

**Finding:** The Small Team architecture is appropriate for pilots. However, there is no documented migration path from Docker Compose to Kubernetes for organizations that outgrow the single-VM model. A Helm chart or `kustomize` overlay would provide a clear scale-out trajectory.

---

### P3-002 — No Account-Level Lockout Policy

**Finding:** Rate limiting is IP-based (5 req/min). A distributed credential stuffing attack with rotating IPs bypasses this. An account-level lockout (e.g., lock after 10 global failed attempts regardless of IP) would provide defense-in-depth. Documented as a future enhancement in Phase 9.4.

---

### P3-003 — No Token Refresh Flow

**Finding:** JWT tokens expire after 30 minutes with no refresh mechanism. Users are forced to re-authenticate, which may cause friction during long investigation sessions in a SOC context. A refresh token flow would improve operator experience.

---

### P3-004 — No Automated Offsite Backup Synchronization

**Finding:** Backup scripts deposit `.sql.gz` files to the local `backups/` directory. The runbook documents that operators "must configure an external synchronization mechanism." There is no automation for this. An S3/GCS sync could be integrated into `backup.sh` as an optional step.

---

### P3-005 — OpenTelemetry Distributed Tracing Not Implemented

**Finding:** `OBSERVABILITY_STANDARD.md` mandates W3C `traceparent` propagation. A custom `correlation_id` is implemented, but not OpenTelemetry-compatible tracing. For multi-service or future async worker debugging, OTel would be a significant improvement.

---

### P3-006 — No Dependency Automation (Dependabot / Renovate)

**Finding:** `DEVSECOPS_STANDARD.md` section 3 mandates Dependabot or Renovate. Neither is configured. CVE patches require manual identification and PRs. This is a supply-chain hygiene gap.

---

## Recommended Remediations

Ordered by priority for a focused remediation sprint:

| # | Finding | Action | Owner | Effort |
|:--|:--------|:-------|:------|:-------|
| 1 | P0-001 | Set `ENVIRONMENT=prod` in `docker-compose.prod.yml` and `.env.example` | DevOps | 30 min |
| 2 | P0-002 | Fix `backup.sh` format: use plain SQL or remove gzip from custom format | DevOps | 1 hr |
| 3 | P0-003 | Add `mypy` step to `ci.yml` and ensure it passes | Backend | 1-2 hr |
| 4 | P0-004 | Change `FROM python:3.14-slim` → `FROM python:3.12-slim` in backend Dockerfile | Backend | 1 hr |
| 5 | P1-005 | Fix `deploy.sh` to reference `docker-compose.prod.yml` | DevOps | 15 min |
| 6 | P1-004 | Remove orphaned `backup_data` volume from `docker-compose.prod.yml` | DevOps | 5 min |
| 7 | P1-001 | Document `BACKEND_CORS_ORIGINS` in `.env.example` and `DEPLOYMENT.md` | Backend | 30 min |
| 8 | P2-004 | Add log rotation driver config to all services in `docker-compose.prod.yml` | DevOps | 30 min |
| 9 | P1-006 | Add minimal Prometheus + Grafana to `docker-compose.prod.yml` | DevOps | 2-3 hr |
| 10 | P2-002 | Add 60-second timeout to `entrypoint.sh` wait loop | Backend | 30 min |

---

## Pilot Deployment Checklist

This checklist must be completed and verified by a passing GitHub Actions run **before any pilot deployment.**

### Pre-Deployment (Code & CI)
- [ ] `P0-001` resolved: `ENVIRONMENT=prod` present in `docker-compose.prod.yml` and `.env.example`
- [ ] `P0-002` resolved: `backup.sh` format corrected; test restore validated on a local instance
- [ ] `P0-003` resolved: MyPy step added to `ci.yml`; pipeline passes with zero type errors
- [ ] `P0-004` resolved: `FROM python:3.12-slim` in `backend/Dockerfile`; CI build passes
- [ ] `P1-005` resolved: `deploy.sh` targets `docker-compose.prod.yml`
- [ ] `P1-004` resolved: orphaned `backup_data` volume removed
- [ ] All four quality gates green in GitHub Actions: Ruff, MyPy, Pytest (≥99%), Bandit, pip-audit, Gitleaks, Docker Build

### Pilot Environment (Infrastructure)
- [ ] Domain name configured with DNS A record pointing to the pilot host
- [ ] `.env` file created from `.env.example` with all `CHANGE_ME_*` values replaced
- [ ] `ENVIRONMENT=prod` explicitly set in `.env`
- [ ] `JWT_SECRET_KEY` generated with `openssl rand -hex 32` (not the default)
- [ ] `POSTGRES_PASSWORD` generated with minimum 24-character high-entropy string
- [ ] `.env` permissions set to `chmod 600`
- [ ] `init-letsencrypt.sh` executed successfully; TLS certificates provisioned
- [ ] `docker compose -f docker-compose.prod.yml up -d --build` completes without errors
- [ ] All containers show `healthy` status in `docker compose ps`
- [ ] `GET /api/v1/health` returns HTTP 200 via `https://[DOMAIN]/api/v1/health`
- [ ] Login endpoint rate-limiting verified (5 req/min per IP returns HTTP 429)
- [ ] HTTPS redirect from HTTP verified (301 response)
- [ ] Security headers verified (HSTS, X-Frame-Options, CSP) via browser devtools or curl

### Backup & Recovery Validation
- [ ] `backup.sh` executed manually; output file is non-zero and readable
- [ ] Restore test completed on a local or staging instance (not production data)
- [ ] Cron job configured on the host for automated daily backup
- [ ] Offsite backup synchronization configured (manual or automated)

### Operator Readiness
- [ ] At least one operator has read `DEPLOYMENT.md`, `BACKUP_RESTORE_RUNBOOK.md`, and `DISASTER_RECOVERY_RUNBOOK.md`
- [ ] An incident response contact is designated
- [ ] Docker logs are confirmed rotating (check `docker inspect` log config)
- [ ] A rollback plan is documented: known-good commit SHA + restore procedure identified

---

## Final Determination

> **NO-GO** (on current main branch codebase)
>
> **GO WITH CONDITIONS** (upon remediation of all P0 findings and CI validation)

**Rationale:**

The current state of the `main` branch contains four pilot-blocking defects:

1. The production JWT security guard is unreachable (`ENVIRONMENT=prod` never set), meaning a misconfigured deployment will silently use the insecure default key — this is the most severe finding.
2. All automated backups produce corrupt archives that cannot be restored.
3. MyPy is not enforced in CI despite being a documented mandatory gate.
4. The backend runs on an alpha Python release that receives no security patches.

These are not theoretical risks — they are concrete operational failures that would manifest during a real pilot. The architecture is sound and the remediation effort is low (estimated one focused engineering day). Upon completion of all P0 items and a clean GitHub Actions run validating the fixes, this assessment should be re-evaluated and the determination is expected to change to **GO**.

The P1 findings, particularly the missing Prometheus/Grafana stack and the non-functional release pipeline, should be addressed before expanding the pilot beyond initial internal users.

---

*This report was produced as part of ASTRA Phase 10 Pilot Deployment Readiness. All findings are based on direct evidence from the repository at the time of assessment (2026-06-21). No source code changes were made as part of this assessment.*
