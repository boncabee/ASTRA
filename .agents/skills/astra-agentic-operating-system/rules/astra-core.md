# ASTRA Core Rules

These rules govern the fundamental behavior of any AI model operating within the ASTRA repository.

## 1. Architectural Rules
- **Target Architecture**: Enterprise-Grade Self-Hosted.
- **SaaS Deferral**: SaaS requirements are explicitly deferred unless requested.
- **Architecture Changes**: Require explicit justification.

## 2. Validation Rules
- **Source of Truth**: GitHub Actions is the ultimate source of truth. Local execution is not enough.
- **No Skipping**: Validation steps cannot be bypassed.

## 3. Implementation Rules
- **No Direct Implementation**: You must investigate first.
- **No Hardcoded Credentials**: Security is paramount.

## 4. Preservation Rules
You must always preserve:
- Security
- CI/CD
- Operations
- Documentation
