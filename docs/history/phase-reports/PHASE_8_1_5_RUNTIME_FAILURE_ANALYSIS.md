# Phase 8.1.5 Runtime Failure Analysis

## Incident Summary
During the final GitHub Actions pipeline execution, the CI workflows experienced two distinct runtime failures preventing the successful execution of `lint-and-test-backend` and `security-scan` jobs. This analysis isolates the root causes of both issues using explicit CI logs and simulated fresh environments.

## Failure A: Pytest Collection Errors (Backend)

**Symptoms:**
- `12 collection errors` reported in `pytest`.
- Coverage metrics dropped unexpectedly from 99% to 46.86%.

**Investigation:**
1. A fresh `.venv` was created locally mimicking the strict CI installation path: `pip install -r requirements.txt -r requirements-dev.txt`.
2. Running `pytest --collect-only` in the fresh environment explicitly recreated the 12 collection errors.
3. The root cause traceback was identified in `tests/api/test_auth.py`: 
   ```
   ImportError: email-validator is not installed, run `pip install 'pydantic[email]'`
   ```
4. **Root Cause:** ASTRA models utilize Pydantic's `EmailStr` field type. Pydantic requires the `email-validator` package to validate these fields. However, `email-validator` was missing from `requirements.txt`. Previous local validation passed because developers naturally accumulated `email-validator` in their local `.venv` installations over time.

**Resolution:**
Appended `email-validator>=2.1.0` to `backend/requirements.txt` to guarantee it is installed during the CI dependency step.

---

## Failure B: Security Scan 404 Error (Gitleaks)

**Symptoms:**
- The `security-scan` workflow failed during the `Secret Scanning (gitleaks)` step.
- `curl` returned a `404 Not Found` error.

**Investigation:**
1. The CI step utilized the following command:
   `curl -sSfL https://github.com/gitleaks/gitleaks/releases/latest/download/gitleaks_8.24.3_linux_x64.tar.gz`
2. **Root Cause:** The `latest/download/` URL endpoint in GitHub redirects to the newest release's assets. However, if the latest release increments the version (e.g., `8.25.0`), the explicit hardcoded filename `gitleaks_8.24.3_linux_x64.tar.gz` will return a 404 because it does not exist in the *latest* release assets.

**Resolution:**
Updated `.github/workflows/ci.yml` to target the explicit, immutable release tag `download/v8.24.3/` instead of `latest/download/`. Added `sudo` to the extraction command to ensure reliable unpacking into `/usr/local/bin`.

## Validation Proof
- Re-running `pytest --collect-only` in a fresh environment post-fix successfully collected all 345 tests with 0 collection errors.
- The `v8.24.3` endpoint was verified to actively serve the correct tarball payload.
