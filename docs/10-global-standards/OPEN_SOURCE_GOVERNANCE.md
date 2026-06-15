# Open Source Governance

This document outlines the governance model for external contributions to the ASTRA platform, ensuring community engagement remains secure, high-quality, and aligned with the product vision.

## 1. Contributor Workflow
- **Fork & Clone:** Contributors must fork the repository and create feature branches.
- **DCO (Developer Certificate of Origin):** All commits must be signed-off (`git commit -s`) asserting that the contributor has the right to submit the code under the MIT License.
- **Draft PRs:** Contributors are encouraged to open Draft PRs early for architectural feedback.
- **Quality Gates:** External PRs must pass the same CI/CD pipelines (Lint, Test, SAST) as internal PRs.

## 2. Maintainer Workflow
- **Review SLA:** Core maintainers aim to provide initial feedback on external PRs within 3 business days.
- **Triage:** Maintainers are responsible for tagging incoming issues with appropriate labels (`bug`, `enhancement`, `good first issue`).
- **Merge Authority:** Only designated Core Maintainers have write access to the `main` branch.

## 3. Issue Lifecycle
1. **New:** Issue is submitted by a user.
2. **Triaged:** A maintainer assigns labels and adds it to the backlog (or closes it if invalid).
3. **Accepted:** The issue is mapped to an active Epic and prioritized for a future Sprint.
4. **In Progress:** A contributor or maintainer is actively working on the issue.
5. **Closed:** The PR resolving the issue is merged, or the issue is deemed won't-fix.

## 4. Security Disclosure Process
- **Private Reporting:** Vulnerabilities MUST NOT be reported via public GitHub Issues.
- **Contact:** Researchers must email `security@astra-platform.local` (or the designated security contact).
- **Embargo:** ASTRA requests a 90-day embargo period to patch the vulnerability before public disclosure.
- **Advisories:** Verified vulnerabilities will be patched, and a formal GitHub Security Advisory (GHSA) will be published alongside the fix.

## 5. Community Governance
- **Code of Conduct:** ASTRA adheres to the Contributor Covenant Code of Conduct. Harassment or abusive behavior will result in a permanent ban from the repository.
- **Decision Making:** Major architectural shifts are proposed via the RFC process. While community input is heavily weighed, final binding decisions are made by the Lead Architect.

## 6. Code Ownership
- **`CODEOWNERS`:** The repository utilizes a `CODEOWNERS` file to automatically request reviews from specific domain experts.
  - E.g., `src/api/* @astra-platform/api-team`
  - E.g., `docs/* @astra-platform/architecture-team`
- **Orphaned Code:** If a community-contributed feature becomes unmaintained and creates technical debt, the Core Team reserves the right to deprecate and remove it.
