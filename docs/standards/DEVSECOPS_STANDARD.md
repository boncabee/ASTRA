# DevSecOps Standard

This document outlines the security automation and vulnerability management practices integrated into the ASTRA CI/CD pipeline.

## 1. Static Application Security Testing (SAST)
- **Tooling:** Bandit (Python) and Semgrep.
- **Integration:** Runs on every Pull Request.
- **Policy:** Any finding with a severity of "High" or "Critical" immediately fails the CI pipeline. "Medium" findings require explicit reviewer sign-off to merge.

## 2. Dynamic Application Security Testing (DAST)
- **Tooling:** OWASP ZAP.
- **Integration:** Runs nightly against the staging environment.
- **Policy:** Scans the active REST APIs for runtime vulnerabilities (e.g., misconfigured CORS, lack of rate limiting). Findings trigger automated Jira tickets.

## 3. Dependency Scanning
- **Tooling:** Dependabot and/or Renovate.
- **Integration:** Continuous scanning of `requirements.txt`.
- **Policy:** Automated PRs are generated for known CVEs in upstream dependencies. Critical CVEs must be merged and deployed within 48 hours.

## 4. Secrets Scanning
- **Tooling:** GitLeaks or GitHub Advanced Security.
- **Integration:** Runs as a pre-commit hook and in the CI pipeline.
- **Policy:** Pushing secrets (API keys, passwords, JWT secrets) is strictly prohibited. If a secret is committed, it must be considered compromised and rotated immediately, followed by a Git history rewrite if the repository is private.

## 5. Container Scanning
- **Tooling:** Trivy or Docker Scout.
- **Integration:** Runs on the finalized Docker image before it is pushed to the container registry.
- **Policy:** Base images must be kept up to date (e.g., `python:3.12-slim`). Images with Critical OS-level vulnerabilities cannot be deployed to production.

## 6. SBOM and Supply Chain Security
- **Tooling:** Syft or CycloneDX.
- **Integration:** A Software Bill of Materials (SBOM) is generated at the end of the build phase for every formal release.
- **Policy:** The SBOM provides cryptographic assurance of all included dependencies and is attached to the GitHub Release as an artifact.

## 7. Vulnerability Management
- **Tracking:** All security findings from SAST, DAST, and manual audits are logged in the `TECHNICAL_DEBT_REGISTER.md` (or an equivalent issue tracker).
- **SLAs:** 
  - **Critical:** Mitigated within 24 hours.
  - **High:** Mitigated within 7 days.
  - **Medium:** Mitigated within 30 days.
  - **Low:** Accepted risk or addressed during regular refactoring.
