# Documentation Lifecycle Standard

This standard governs how documentation is created, updated, approved, and retired within the ASTRA repository. It extends the foundational `DOCUMENTATION_GOVERNANCE_STANDARD.md` by defining the temporal lifecycle of docs.

## 1. Documentation Ownership
Every document must have an implicit owner based on its directory:
- `01-product/`: Product Owner
- `02-requirements/`: Product Owner & Lead Architect
- `03-architecture/`: Lead Architect
- `04-ui-ux/`: Design Lead
- `05-engineering/`: Engineering Manager
- `06-operations/`: DevOps Lead
- `07-governance/`: Architecture Board
- `10-global-standards/`: Global Standards Alignment Agent / Security Lead

## 2. Document Versioning
- Documentation is strictly versioned in lockstep with the source code via Git.
- We do not use explicit v1.0, v2.0 numbering inside the documents themselves (except for `README_V2.md` during transitions) because the Git SHA provides the exact version context.

## 3. RFC (Request for Comments) Process
For major changes to standards or architecture, an RFC process is utilized:
1. **Draft:** Author creates a PR with a new document marked as `[RFC]` in the title.
2. **Comment Period:** The PR remains open for a minimum of 3 days to allow cross-functional teams to comment.
3. **Resolution:** The author addresses comments. Once consensus is reached, the `[RFC]` tag is removed, and the PR is merged.

## 4. Review Cycle and Approval Process
- **Minor Updates:** Typo fixes or clarifying sentences require 1 peer review (standard PR process).
- **Major Updates:** Changes to PRD, SRS, SDD, or any Global Standard require explicit approval from the assigned Document Owner (see Section 1).
- **PR Blocking:** Pull Requests that modify system behavior but fail to update the corresponding documentation will be blocked by reviewers until the documentation is added to the same PR.

## 5. Retirement Process
Documents are never "deleted" if they contain historical value.
1. **Identification:** A document is identified as obsolete.
2. **Marking:** A GitHub Alert (`> [!WARNING] Obsolete: Superseded by X`) is added to the top of the file.
3. **Archiving:** The file is moved to the appropriate `docs/08-history/` subdirectory.
4. **Scrubbing:** Index files and READMEs are updated to remove references to the retired document.
