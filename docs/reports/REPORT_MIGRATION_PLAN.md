# Report Migration Plan

This document outlines the step-by-step execution plan for consolidating reports in the ASTRA repository to ensure compliance with the new DOCS-HOTFIX-002 storage standards.

## 1. Directory Creation
The following directories will be created (if they do not already exist) to establish the Target Structure:
- `docs/audits/`
- `docs/reviews/`
- `docs/reports/`
- `docs/validation/`
- `docs/governance/`
- `docs/history/`
- `docs/phase-reports/`
- `docs/sprint-reports/`
- `docs/task-reports/`

## 2. File Relocation
Files currently violating the root-level storage prohibition will be moved using standard `mv` (or Powershell `Move-Item`) commands:

### Audits
- Move `API_AUDIT_REPORT.md` -> `docs/audits/`
- Move `ARCHITECTURE_AUDIT_REPORT.md` -> `docs/audits/`
- Move `CODE_QUALITY_AUDIT_REPORT.md` -> `docs/audits/`
- Move `DATABASE_AUDIT_REPORT.md` -> `docs/audits/`
- Move `DEPENDENCY_AUDIT_REPORT.md` -> `docs/audits/`
- Move `REPOSITORY_AUDIT_REPORT.md` -> `docs/audits/`
- Move `SECURITY_AUDIT_REPORT.md` -> `docs/audits/`
- Move `TESTING_AUDIT_REPORT.md` -> `docs/audits/`

### Validation
- Move `ENTERPRISE_READINESS_REPORT.md` -> `docs/validation/`
- Move `PROJECT_READINESS_REPORT.md` -> `docs/validation/`

### Phase Reports
- Move `PHASE_6_5_COMPLETION_REPORT.md` -> `docs/phase-reports/`

### Uncategorized Docs
- Move `docs/DOCUMENTATION_REFACTOR_REPORT.md` -> `docs/reports/`
- Move `docs/PLANNING_GOVERNANCE_REPORT.md` -> `docs/governance/`
- Move `docs/README_REVIEW.md` -> `docs/reviews/`

## 3. Reference Updates
After the files are relocated, a global search and replace will be executed to update relative links within `README.md` and any index files in `docs/` that referenced the old root locations.

## 4. Governance Enforcement
Generate `docs/governance/REPORT_STORAGE_STANDARD.md` to formally document the absolute prohibition of placing future reports in the repository root.
