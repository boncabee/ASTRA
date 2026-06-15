# Secure Software Development Life Cycle (SSDLC)

This document formalizes the integration of security at every phase of the ASTRA software development life cycle, shifting security "left".

## 1. Planning & Requirements
- **Action:** During the drafting of User Stories, security requirements must be explicitly defined.
- **Artifact:** Product Requirements Document (PRD) and Threat Models.
- **Security Check:** Are we exposing new PII? Are we changing RBAC boundaries? If yes, an Architecture Decision Record (ADR) is required.

## 2. Design & Architecture
- **Action:** Execute STRIDE threat modeling against any new component or major feature.
- **Artifact:** Architecture Design Document (SDD) and `STRIDE_THREAT_MODEL.md` updates.
- **Security Check:** Does the design adhere to the principle of least privilege and ASTRA's modular monolith constraints?

## 3. Development
- **Action:** Developers follow the `CODING_STANDARD_GLOBAL.md` to prevent common flaws (e.g., injection, ReDoS).
- **Artifact:** Code commits, Pull Requests.
- **Security Check:** Peer review explicitly checks for security flaws. Secrets scanning runs locally via pre-commit hooks.

## 4. Testing & Verification
- **Action:** Automated CI/CD pipelines execute SAST, DAST, and dependency scanning.
- **Artifact:** CI run logs, Test coverage reports.
- **Security Check:** Pipeline blocks deployment if High/Critical vulnerabilities are detected, or if test coverage drops below 100%.

## 5. Deployment & Release
- **Action:** Container images are built, scanned, and signed.
- **Artifact:** Docker Image, Software Bill of Materials (SBOM).
- **Security Check:** No critical OS-level vulnerabilities in the base image. Immutable infrastructure principles applied.

## 6. Operations & Monitoring
- **Action:** Continuous monitoring of API traffic, error rates, and system health.
- **Artifact:** Telemetry dashboards, Audit Logs.
- **Security Check:** Unhandled exceptions and massive spikes in 403 Forbidden errors trigger alerts to the SecOps team for immediate investigation.
