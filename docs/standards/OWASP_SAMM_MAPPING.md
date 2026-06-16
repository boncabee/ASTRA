# OWASP SAMM Mapping

## Overview
This document evaluates the ASTRA platform against the **OWASP Software Assurance Maturity Model (SAMM) v2.0**. It assesses maturity across five business functions: Governance, Design, Implementation, Verification, and Operations. Maturity is scored from 0 (Non-existent) to 3 (Optimized).

## 1. Governance
- **Strategy & Metrics (Score: 1):** Security is acknowledged, but no formal security metrics or KPIs are tracked.
- **Policy & Compliance (Score: 2):** Formal documentation standards and global engineering standards are established.
- **Education & Guidance (Score: 1):** Code standards exist, but no formal secure coding training is mandated for contributors.
- **Gap:** Lack of measurable security metrics.
- **Roadmap:** Implement tracking for MTTR (Mean Time to Remediate) vulnerabilities.

## 2. Design
- **Threat Assessment (Score: 2):** STRIDE threat modeling is performed for core architectural components.
- **Security Requirements (Score: 2):** `SECURITY_REQUIREMENTS.md` outlines foundational access controls and validation rules.
- **Security Architecture (Score: 2):** Modular monolith design enforces boundaries (e.g., Policy Engine isolated from Automation Workers).
- **Gap:** Missing automated threat modeling integrated into the CI pipeline.
- **Roadmap:** Adopt "Threat Modeling as Code" using tools like Threatspec.

## 3. Implementation
- **Secure Build (Score: 2):** CI pipeline builds Docker images automatically with predictable dependency manifests.
- **Secure Deployment (Score: 1):** Manual deployment steps still exist; infrastructure as code (IaC) is not fully mature.
- **Defect Management (Score: 1):** Technical debt is tracked, but security bugs lack a distinct, prioritized SLA workflow.
- **Gap:** Lack of fully automated IaC and strict bug SLAs.
- **Roadmap:** Migrate to Terraform/Pulumi for deployments and define security bug SLAs (e.g., 24h for Critical).

## 4. Verification
- **Architecture Assessment (Score: 2):** ADRs require review before implementation.
- **Requirements-driven Testing (Score: 2):** 100% unit test coverage rule is enforced; acceptance criteria are mapped to tests.
- **Security Testing (Score: 1):** Basic SAST may be present, but comprehensive DAST and manual penetration testing are absent.
- **Gap:** Missing dynamic security testing.
- **Roadmap:** Integrate OWASP ZAP into the staging pipeline.

## 5. Operations
- **Incident Management (Score: 1):** `RUNBOOKS.md` exist, but no formal incident response team is designated.
- **Environment Management (Score: 2):** Secrets are kept out of source code (via `.env` / secret managers).
- **Operational Management (Score: 1):** Basic logging is present, but SIEM integration and active alerting are missing.
- **Gap:** Lack of automated alerting for application security events.
- **Roadmap:** Implement Prometheus/Grafana alerting rules for excessive 403/500 errors.

## Overall Assessment
**Current SAMM Maturity Level: 1.5 (Defined/Managed)**
ASTRA has strong foundational documentation and architectural discipline, but lacks automated security verification and mature operational incident response capabilities. The immediate priority is advancing Verification and Operations to Level 2.
