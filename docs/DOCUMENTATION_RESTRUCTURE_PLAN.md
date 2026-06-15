# Documentation Restructure Plan

## Objective
To restructure the ASTRA project's documentation into an enterprise-grade framework suitable for Self-Hosted Enterprise, Future SaaS, Open Source Contributors, Security Engineers, and Product teams.

## Principles
1. **Source of Truth**: Single authoritative document for each major architectural or product concept.
2. **Traceability**: Clear line of sight from PRD -> SRS -> SDD -> Implementation -> Phase Reports.
3. **Preservation of History**: No historical sprint reports, phase reports, or audits will be destroyed. They are archived in `08-history`.
4. **Governance**: All future documentation must adhere to the standardized `DOCUMENTATION_GOVERNANCE_STANDARD.md`.

## Target Architecture

```text
docs/
├── README.md (Primary Entry Point)
├── PROJECT_OVERVIEW.md
├── 01-product/
│   ├── PRD.md
│   ├── USER_PERSONAS.md
│   ├── USER_JOURNEYS.md
│   ├── USER_FLOW.md
│   ├── FEATURE_CATALOG.md
│   └── ROADMAP.md
├── 02-requirements/
│   ├── SRS.md
│   ├── BUSINESS_RULES.md
│   ├── SECURITY_REQUIREMENTS.md
│   ├── NON_FUNCTIONAL_REQUIREMENTS.md
│   └── COMPLIANCE_REQUIREMENTS.md
├── 03-architecture/
│   ├── ARCHITECTURE.md
│   ├── SDD.md
│   ├── DATABASE_SCHEMA.md
│   ├── API_SPEC.md
│   ├── COMMON_EVENT_SCHEMA.md
│   ├── DOMAIN_MODELS/
│   └── ADR/
├── 04-ui-ux/
│   ├── UI_UX_FOUNDATION.md
│   ├── DESIGN_SYSTEM.md
│   ├── SCREEN_FLOWS.md
│   └── WIREFRAMES.md
├── 05-engineering/
│   ├── CODING_STANDARDS.md
│   ├── TESTING_STRATEGY.md
│   ├── RELEASE_PROCESS.md
│   └── CONTRIBUTING.md
├── 06-operations/
│   ├── DEPLOYMENT.md
│   ├── RUNBOOKS.md
│   ├── BACKUP_RECOVERY.md
│   ├── MONITORING.md
│   └── INCIDENT_RESPONSE.md
├── 07-governance/
│   ├── RISK_REGISTER.md
│   ├── TECHNICAL_DEBT_REGISTER.md
│   ├── DECISION_LOG.md
│   ├── TRACEABILITY_MATRIX.md
│   └── DOCUMENTATION_GOVERNANCE_STANDARD.md
└── 08-history/
    ├── phase-reports/
    ├── sprint-reports/
    ├── task-reports/
    ├── audit-reports/
    └── review-reports/
```

## Execution Steps

### Phase 1: Directory Setup
Create all target directories (`01-product` through `08-history`).

### Phase 2: Foundational Document Drafting
Extract context from existing documentation to draft:
- `PRD.md`
- `SRS.md`
- `SDD.md`
- `UI_UX_FOUNDATION.md`
- `README_V2.md`
- `DOCUMENTATION_GOVERNANCE_STANDARD.md`
- `TRACEABILITY_MATRIX.md`

### Phase 3: Migration and Archiving
Move existing authoritative documents into their appropriate directories based on the `DOCUMENT_MIGRATION_MAP.md`.
Move all sprint/phase/audit reports into `08-history/`.
Delete or securely archive obsolete documents as outlined in `DOCUMENT_RETIREMENT_LIST.md`.

### Phase 4: Verification
Confirm there are no orphaned files in `docs/` or the root directory. Ensure that all deliverables have been successfully generated and match the target architecture.
