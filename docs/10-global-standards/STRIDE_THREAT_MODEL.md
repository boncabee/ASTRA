# STRIDE Threat Model

This document outlines the STRIDE threat model (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) across the core domains of the ASTRA platform.

| Domain | Threat Type | Description | Mitigation Strategy |
| --- | --- | --- | --- |
| **Identity** | Spoofing | Attacker forges a JWT to impersonate an Admin. | Cryptographic verification of JWT signatures using strong, rotating RS256 keys. |
| **Identity** | Elevation of Privilege | Analyst modifies API request to access Admin endpoints. | Strict FastAPI `Depends(require_role("admin"))` enforcement on all privileged routes. |
| **Correlation** | DoS | Massive influx of malformed CES events intended to exhaust correlation memory. | API rate limiting; batch processing with strict payload size limits; memory constraints on Redis workers. |
| **Observation** | Tampering | Attacker intercepts database connection to manually lower a Risk Score. | Enforce TLS 1.3 for all database connections; strict network segmentation preventing direct DB access. |
| **Policy** | Information Disclosure | Policy logic leaks sensitive network topology in its configuration. | Policies are strictly stored in the DB (not code) and restricted to `Tier 3` and `Admin` roles. |
| **Policy** | DoS | A poorly written regex in a Policy rule causes ReDoS, blocking the evaluation engine. | Restrict regex usage in policies; enforce evaluation timeouts (e.g., max 50ms per policy). |
| **Evidence** | Tampering | Internal actor deletes an Evidence record to hide an automated mistake. | Evidence repository is append-only at the ORM layer. Production DB user lacks `DELETE` permissions on the `evidence` table. |
| **Evidence** | Repudiation | Actor claims they did not manually trigger an automation. | All manual triggers require a JWT, and the `actor_id` is permanently bound to the Evidence record. |
| **Reporting** | Information Disclosure | A generated compliance report containing PII is accessed by unauthorized staff. | Reports are generated into secure, ephemeral storage requiring an authenticated, signed URL to download. |
| **Automation** | Elevation of Privilege | An automation worker executes a command beyond its intended scope (e.g., executing arbitrary shell commands). | Workers have strictly scoped, parameter-driven functions (e.g., `block_ip(ip)`). Arbitrary code execution features are explicitly prohibited. |
| **Automation** | Spoofing | Attacker injects a fake task into the Redis queue directly. | Queue access is restricted to the internal VPC network; Redis requires strong authentication. |
| **Case Mgmt (Future)** | Tampering | Attacker modifies the state of an open Case to `Closed` maliciously. | Implement strict state-machine validation and audit logging for all Case transitions. |
| **AI (Future)** | Information Disclosure | Sensitive evidence data is leaked to a public LLM provider during narrative generation. | Utilize private, dedicated AI endpoints (e.g., Azure OpenAI, self-hosted LLMs). Implement PII redaction before payload transmission. |
| **AI (Future)** | Elevation of Privilege | Prompt injection causes the AI to instruct the Automation engine to take destructive action. | **Critical Architecture Rule:** AI is strictly Read-Only and enhances observation narratives. AI is *never* granted authority to trigger Automations or alter Policies. |
