# OWASP ASVS Mapping

## Overview
This document maps the current ASTRA architecture against the **OWASP Application Security Verification Standard (ASVS) v4.0**. ASTRA targets ASVS Level 2 (Standard applications handling sensitive data).

## 1. Architecture, Design and Threat Modeling (V1)
- **Implemented:**
  - *V1.1 Secure Software Development Lifecycle:* ASTRA has formalized `SECURE_SDLC.md` and uses strict PR quality gates.
  - *V1.2 Authentication Design:* JWT-based stateless authentication is defined (`ADR-011`).
- **Partially Implemented:**
  - *V1.5 Input and Output Architecture:* CES parsing provides strict input validation via Pydantic, but output encoding requires review.
- **Missing:**
  - *V1.4 Access Control Architecture:* Deep resource-level authorization (ABAC) is not yet fully defined.
- **Priority:** High
- **Recommendations:** Formalize ABAC design for `Tenant_ID` isolation prior to SaaS transition.

## 2. Authentication Verification Requirements (V2)
- **Implemented:**
  - *V2.1 Password Security:* Delegated to external IdP via JWT.
  - *V2.7 Out of Band Authenticator:* N/A (handled by IdP).
- **Partially Implemented:**
  - *V2.3 Authenticator Lifecycle:* Tokens expire, but immediate revocation (blacklist) is not currently implemented in Redis.
- **Priority:** Medium
- **Recommendations:** Implement a Redis-based JWT denylist for explicit logouts.

## 3. Session Management Verification Requirements (V3)
- **Implemented:**
  - *V3.1 Fundamental Session Management:* Uses HTTP Bearer tokens.
- **Missing:**
  - *V3.3 Session Termination:* Lack of token revocation.
- **Priority:** Medium
- **Recommendations:** Tie token validation to Redis blacklist.

## 4. Access Control Verification Requirements (V4)
- **Implemented:**
  - *V4.1 General Access Control:* FastAPI dependencies enforce Role-Based Access Control (RBAC).
- **Partially Implemented:**
  - *V4.3 Other Access Control:* Missing horizontal privilege escalation checks (e.g., User A accessing User B's Correlation).
- **Priority:** Critical
- **Recommendations:** Add ownership/tenant filtering to all ORM queries.

## 5. Validation, Sanitization and Encoding (V5)
- **Implemented:**
  - *V5.1 Input Validation:* Pydantic V2 strictly validates all API inputs.
- **Priority:** Low
- **Recommendations:** Maintain strict Pydantic configurations.

## 6. Stored Cryptography Verification Requirements (V6)
- **Implemented:**
  - *V6.1 Data Classification:* Not fully applicable yet; database uses standard Postgres types.
  - *V6.2 Algorithms:* N/A (Using managed cloud DB encryption at rest).
- **Priority:** Low
- **Recommendations:** Ensure production Postgres instance enables AES-256 transparent data encryption (TDE).

## 7. Error Handling and Logging Verification Requirements (V7)
- **Implemented:**
  - *V7.1 Log Content:* Audit trail (Evidence) captures all automated decisions immutably.
- **Partially Implemented:**
  - *V7.3 Exception Handling:* Global exception handlers exist, but stack traces must be strictly suppressed in production.
- **Priority:** Medium
- **Recommendations:** Enforce structured JSON logging without sensitive fields.

## 8. Data Protection Verification Requirements (V8)
- **Partially Implemented:**
  - *V8.1 General Data Protection:* No PII is explicitly collected, but raw logs may contain sensitive IPs/Users.
- **Priority:** High
- **Recommendations:** Implement data masking/anonymization for raw logs stored in Observations.
