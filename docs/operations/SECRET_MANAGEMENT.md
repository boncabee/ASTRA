# ASTRA Secret Management Lifecycle
Document ID: ASTRA-SEC-001
Version: 1.0

## 1. Secret Generation Standards
All cryptographic secrets and database credentials must be generated using cryptographically secure random number generators (CSPRNG).
- **JWT_SECRET_KEY:** Must be a minimum of 256 bits (32 bytes) of entropy.
  - *Example:* `openssl rand -hex 32`
- **POSTGRES_PASSWORD:** Must be a minimum of 24 characters, high entropy.

## 2. Injection and Storage
- **No Hardcoding:** Secrets must never be hardcoded in application source code, `docker-compose` files, or Dockerfiles.
- **Environment Variables:** Secrets are passed to the ASTRA cluster exclusively via the root `.env` file (`chmod 600`).
- **CI/CD:** In automated pipelines (e.g., GitHub Actions), secrets must be managed using the platform's native encrypted secret store (GitHub Secrets).

## 3. Secret Rotation Procedure
Secrets must be rotated under two conditions: **Routine** (annually) or **Emergency** (suspected compromise).

### Routine Rotation Steps
1. **Generate New Secret:** Create the new secret value.
2. **Update `.env`:** Replace the old value in the production `.env` file.
3. **Restart Service:** Execute `docker compose -f docker-compose.prod.yml up -d` to restart the containers with the new environment variables.
   *Note: Rotating `JWT_SECRET_KEY` will immediately invalidate all active user sessions.*

## 4. Incident Response (Leakage)
If a secret is suspected of being exposed (e.g., accidentally committed to a repository or logged in plaintext):
1. **Declare Incident:** Notify the Security Engineering team immediately.
2. **Revoke and Rotate:** Immediately rotate the compromised secret in production following the Routine Rotation Steps.
3. **Audit Access:** Review ASTRA audit logs and database logs for any anomalous activity utilizing the compromised secret or associated accounts during the exposure window.
4. **Purge:** Ensure the leaked secret is purged from the repository history using tools like `git filter-repo` if applicable.
