# Documentation Governance Standard
**Project:** ASTRA (Adaptive Security Threat Response & Automation Platform)

## 1. Purpose
This document establishes the strict governance model for all documentation within the ASTRA repository. It ensures that documentation remains an accurate, high-quality representation of the system's architecture and product vision.

## 2. Naming Conventions
- **Markdown Files:** All documentation must use `UPPER_SNAKE_CASE.md` (e.g., `DOCUMENTATION_GOVERNANCE_STANDARD.md`, `API_SPEC.md`).
- **Exception:** The repository root `README_V2.md` and `docs/README.md` (if applicable) use standard naming.
- **Directories:** All directories inside `docs/` must use `kebab-case` and be prefixed with a two-digit ordering number if they are top-level sections (e.g., `01-product`, `02-requirements`).

## 3. Document Ownership
Every document must have a logical owner responsible for its accuracy:
- `01-product/`: Product Management Team
- `02-requirements/`: Product & Architecture Teams
- `03-architecture/`: Architecture Team
- `04-ui-ux/`: UI/UX & Frontend Teams
- `05-engineering/`: Engineering & QA Teams
- `06-operations/`: DevOps & Security Operations Teams
- `07-governance/`: Architecture Team
- `08-history/`: N/A (Immutable)

## 4. Versioning
- Documentation is versioned alongside the code in Git.
- Major structural changes require an explicit Pull Request and Architecture review.

## 5. Review Process
- Any Pull Request that modifies system behavior (e.g., changing an API, adding a new database table) MUST include the corresponding update to the documentation in the same PR.
- PRs without updated documentation will be rejected by the Quality Gate.

## 6. Change Approval Process
- Minor typo fixes: Self-approved or standard code-review.
- Structural changes to `01-product`, `02-requirements`, or `03-architecture`: Requires approval from a Lead Architect or Product Owner.

## 7. Retirement Process
If a document becomes obsolete:
1. Do NOT simply delete it if it contains valuable historical context. Move it to `08-history/` and append a `> [!WARNING] Obsolete` banner at the top.
2. If it is entirely superseded by a new document (e.g., old PRD -> new PRD), the old file can be safely deleted or overwritten, provided the history exists in Git.

## 8. Future ADR Creation (Architecture Decision Records)
When a significant technical decision is made:
1. Create a new file in `03-architecture/ADR/` named `ADR-XXX_SHORT_DESCRIPTION.md`.
2. Use the standard ADR template (Context, Decision, Consequences).
3. Log the decision in `07-governance/DECISION_LOG.md`.
