# PHASE 12A: STAGING STRATEGY DOCUMENTATION

**Date:** 2026-06-22  
**Agent:** ASTRA Production Launch Blocker Remediation Agent  
**Status:** COMPLETE  
**Scope:** Staging Environment and Code Promotion Strategy (LB-005)  

---

## 1. Overview

To resolve LB-005 (Staging Environment), we have defined a dual-environment configuration strategy. ASTRA now utilizes a staging environment that is structurally identical to the production environment but isolated at the network, database, and credential layers.

Staging serves as the final validation gate before code is promoted to the live production server. It is where automated and manual checks run to guarantee that updates do not degrade system stability or corrupt production databases.

---

## 2. Staging vs. Production Configuration

Both staging and production run the identical hardened compose stack (`docker-compose.prod.yml`) but use separate `.env` files for full environment isolation.

| Parameter | Staging Environment (`.env.staging`) | Production Environment (`.env`) |
|:----------|:------------------------------------|:--------------------------------|
| **Domain** | `staging.your-domain.com` | `your-domain.com` |
| **API URL** | `https://staging.your-domain.com/api/v1` | `https://your-domain.com/api/v1` |
| **ENVIRONMENT** | `prod` (keeps production security guards active) | `prod` |
| **Postgres User** | `astra_staging` | `astra_prod` |
| **Postgres Password** | Isolated, high-entropy password | Isolated, high-entropy password |
| **Postgres DB** | `astra_staging` | `astra` |
| **JWT Secret Key** | Unique 32-byte key | Unique 32-byte key |
| **Slack Webhook** | Staging channel | Production on-call channel |

> **Warning:** `.env.staging` has been explicitly added to `.gitignore`. Under no circumstances should staging credentials be committed to the repository.

---

## 3. Deployment Script: `deploy-staging.sh`

The newly added script `scripts/deploy-staging.sh` handles staging deployments cleanly:
1. **File Check:** Verifies that `.env.staging` is present.
2. **Environment Guard:** Confirms that `ENVIRONMENT=prod` is set in `.env.staging`.
3. **Isolation:** Runs `docker compose --env-file .env.staging -f docker-compose.prod.yml up -d --build`. This guarantees that staging containers boot using staging configuration variables only.

---

## 4. Promotion and Release Workflow

Changes are promoted through environments according to a strict lifecycle:

```text
  Local Development
        │
        ▼ (PR to main)
  GitHub Actions CI (Unit Tests, Lints, Security Scans)
        │
        ▼ (Merge to main)
  Automated Deployment to Staging (deploy-staging.sh)
        │
        ▼ (Validation Gates)
  1. Automated Health Check Passes
  2. manual QA / UAT Verification
  3. Nightly Security DAST Scans Pass
        │
        ▼ (Git Release Tag vX.Y.Z)
  Production Release Pipeline Triggered
        │
        ▼ (Docker Pull and Restart)
  Production Host Deployment (deploy.sh)
```

### Steps for Promoting to Production

1. **Staging Validation:** Ensure the staging server is stable. Run tests and review logs (`docker compose --env-file .env.staging -f docker-compose.prod.yml logs`).
2. **Tagging:** Create a release tag from the tested commit SHA:
   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin v1.0.0
   ```
3. **Release Pipeline:** The push triggers `.github/workflows/release.yml`, which runs CI, pushes images to GHCR, and attaches SBOM files to the GitHub Release.
4. **Production Update:** On the production host, update the `.env` file to reference the new release tags (if pulling pre-built images), pull, and run:
   ```bash
   bash scripts/deploy.sh
   ```
