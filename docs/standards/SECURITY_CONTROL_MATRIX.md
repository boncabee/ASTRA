# Security Control Matrix

This matrix maps ASTRA's implemented and planned security controls against globally recognized frameworks.

| Control Area | Framework Mapping | Current Coverage | Identified Gap | Priority | Owner |
| --- | --- | --- | --- | --- | --- |
| **Authentication & Identity** | ASVS V2, ISO 27001 A.9, NIST PS.1 | JWT validation; Role-Based Access Control (RBAC) active. | Missing JWT explicit revocation (denylist); missing automated secret rotation. | High | Architecture Team |
| **Authorization** | ASVS V4, ISO 27001 A.9 | Endpoint-level roles (`Depends(require_role)`). | Missing Tenant/Resource-level isolation (Horizontal privilege limits). | Critical | Security Engineering |
| **Audit Logging (Evidence)** | ASVS V7, NIST PS.2, ISO 27001 A.12.4 | Immutable Evidence repository. Cryptographic chain-of-custody. | Logs not currently shipped to a distinct external SIEM for off-site backup. | Medium | DevOps |
| **Secure SDLC** | SAMM Governance, NIST PO.1 | Strict PR reviews, 100% test coverage, comprehensive documentation standard. | Lack of automated SAST/DAST in the CI/CD pipeline. | High | Engineering Team |
| **Data Protection** | ASVS V8, ISO 27001 A.8.2 | Managed DB encryption at rest (TLS in transit). | No internal application-layer encryption for PII or sensitive keys. | Low | Data Engineering |
| **Incident Response** | SAMM Operations, ISO 27001 A.16 | Basic runbooks defined. | No formal Incident Response Plan (IRP) or SLA tracking. | High | SecOps |
| **Threat Modeling** | SAMM Design, NIST PW.1 | STRIDE model documented for core domains. | Not integrated as a continuous, automated "as-code" check during PRs. | Medium | Architecture Team |
| **Supply Chain Security** | NIST PS.3 | Fixed dependency versions in `requirements.txt`. | Missing SBOM generation and automated dependency vulnerability scanning (e.g., Dependabot). | High | DevOps |
| **Execution Prevention** | MITRE ATT&CK (TA0002) | Strict Pydantic parsing prevents payload injection. Automation workers scoped to explicit functions. | ReDoS (Regex Denial of Service) potential in Policy Engine rules. | Medium | Security Engineering |
| **Defense Evasion** | MITRE ATT&CK (TA0005) | Tamper-proof Evidence logs prevent actors from hiding their tracks. | Database superuser account currently possesses deletion rights. | Critical | Data Engineering |
