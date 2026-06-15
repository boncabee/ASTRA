# Document Retirement List

The following documents have been identified as obsolete, entirely superseded by new deliverables, or conceptually broken given the new architectural vision. These will be securely deleted (or fully overridden without keeping the original name).

| Document Path | Reason for Retirement | Superseding Document | Action |
| --- | --- | --- | --- |
| `README.md` | Outdated, unstructured, replaced by V2. | `README_V2.md` | Delete / Override |
| `docs/REPORT_INDEX.md` | Redundant. History will naturally live in `08-history` folder. | N/A | Delete |
| `docs/architecture/REPOSITORY_BOOTSTRAP_SPEC.md` | Obsolete. Original setup instructions are no longer relevant. | N/A | Delete |
| `docs/architecture/REPOSITORY_STRUCTURE.md` | File structure completely changing during this refactor. | `DOCUMENTATION_GOVERNANCE_STANDARD.md` | Delete |
| `docs/governance/GOVERNANCE.md` | Fragmented governance. Replaced by a comprehensive standard. | `DOCUMENTATION_GOVERNANCE_STANDARD.md` | Delete |
| `docs/governance/AGENT_TASK_EXECUTION_FRAMEWORK.md` | Concept merged into Governance Standard and Engineering Guidelines. | `DOCUMENTATION_GOVERNANCE_STANDARD.md` | Delete / Merge |
| `docs/planning/PRD.md` | Stale planning document. Needs complete rewrite. | `docs/01-product/PRD.md` | Delete / Override |
| `docs/planning/ROADMAP.md` | Superseded by `ROADMAP_V2.md`. | `docs/01-product/ROADMAP.md` | Delete |
| `docs/planning/USER_FLOW.md` | Stale and out of context with new Automation features. | `docs/01-product/USER_FLOW.md` | Delete / Override |
| `docs/security/SECURITY.md` | Redundant to other security documentation. | `docs/02-requirements/SECURITY_REQUIREMENTS.md` | Delete / Merge |

> [!NOTE]
> No historical phase, sprint, or audit reports will be deleted. They are preserved in `docs/08-history/` for traceability and context.
