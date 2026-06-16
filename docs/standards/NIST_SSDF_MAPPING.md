# NIST SSDF Mapping

## Overview
This document evaluates the ASTRA platform against the **NIST Secure Software Development Framework (SSDF) V1.1 (SP 800-218)**.

## 1. Prepare the Organization (PO)
*Ensure that people, processes, and technology are prepared to perform secure software development.*

- **Current Alignment:** ASTRA has strong governance models in place, including formal Documentation Lifecycle, Planning Governance, and Architecture Review (ADR) processes.
- **Missing Areas:** Formal secure coding training for personnel is not documented as a strict requirement.
- **Recommended Actions:** Establish a requirement for annual secure development training (e.g., OWASP Top 10) for all core maintainers.

## 2. Protect the Software (PS)
*Protect all components of the software from tampering and unauthorized access.*

- **Current Alignment:** Git workflows enforce PR reviews. The `Evidence` repository design natively guarantees data immutability for critical security decisions.
- **Missing Areas:** Code signing and strict provenance (e.g., SLSA framework) are not implemented for release artifacts.
- **Recommended Actions:** Implement Sigstore or similar tooling to sign Docker images and releases, ensuring artifact integrity.

## 3. Produce Well-Secured Software (PW)
*Produce well-secured software with minimal security vulnerabilities.*

- **Current Alignment:** Code standards require strict type-hinting (Pyright) which eliminates many classes of runtime errors. 100% test coverage is mandated.
- **Missing Areas:** Automated Static Application Security Testing (SAST) and dependency vulnerability scanning are not fully integrated into the blocking CI path.
- **Recommended Actions:** Integrate tools like Bandit (for Python SAST) and Dependabot/Renovate into the GitHub Actions workflow, configured to block merges on High/Critical findings.

## 4. Respond to Vulnerabilities (RV)
*Identify residual vulnerabilities in software releases and respond appropriately.*

- **Current Alignment:** `SECURITY_REQUIREMENTS.md` and basic runbooks exist to guide incident response.
- **Missing Areas:** A formal Vulnerability Disclosure Program (VDP) and standardized SLA for patching reported flaws do not exist.
- **Recommended Actions:** Publish a `SECURITY.md` in the repository root detailing how external researchers can report vulnerabilities, and establish a 14-day SLA for critical patch deployment.
