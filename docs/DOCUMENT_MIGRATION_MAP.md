# Document Migration Map

This document outlines the planned mapping from the current structure to the new target architecture.

## 01-product
| Original Path | Target Path | Action |
| --- | --- | --- |
| `docs/planning/PRD.md` | `docs/01-product/PRD.md` | Create new based on existing context |
| `N/A` | `docs/01-product/USER_PERSONAS.md` | Create new |
| `N/A` | `docs/01-product/USER_JOURNEYS.md` | Create new |
| `docs/planning/USER_FLOW.md` | `docs/01-product/USER_FLOW.md` | Extract/Create new |
| `N/A` | `docs/01-product/FEATURE_CATALOG.md` | Create new |
| `docs/planning/ROADMAP_V2.md` | `docs/01-product/ROADMAP.md` | Rename and Move |

## 02-requirements
| Original Path | Target Path | Action |
| --- | --- | --- |
| `N/A` | `docs/02-requirements/SRS.md` | Create new based on `CORRELATION_ENGINE_SPEC.md`, `PARSER_FRAMEWORK_SPEC.md` |
| `N/A` | `docs/02-requirements/BUSINESS_RULES.md` | Create new |
| `docs/security/THREAT_MODEL.md`<br>`docs/security/ATTACK_KNOWLEDGE_MODEL.md` | `docs/02-requirements/SECURITY_REQUIREMENTS.md` | Merge and Move |
| `N/A` | `docs/02-requirements/NON_FUNCTIONAL_REQUIREMENTS.md` | Create new |
| `N/A` | `docs/02-requirements/COMPLIANCE_REQUIREMENTS.md` | Create new |

## 03-architecture
| Original Path | Target Path | Action |
| --- | --- | --- |
| `docs/architecture/ARCHITECTURE.md` | `docs/03-architecture/ARCHITECTURE.md` | Move |
| `N/A` | `docs/03-architecture/SDD.md` | Create new |
| `docs/architecture/DATABASE_SCHEMA.md` | `docs/03-architecture/DATABASE_SCHEMA.md` | Move |
| `docs/architecture/API_SPEC.md` | `docs/03-architecture/API_SPEC.md` | Move |
| `docs/architecture/COMMON_EVENT_SCHEMA.md`<br>`docs/architecture/CES_IMPLEMENTATION_GUIDE.md` | `docs/03-architecture/COMMON_EVENT_SCHEMA.md` | Merge and Move |
| `docs/architecture/CORRELATION_DOMAIN_MODEL.md` | `docs/03-architecture/DOMAIN_MODELS/CORRELATION_DOMAIN_MODEL.md` | Move |
| `docs/architecture/OBSERVATION_DOMAIN_MODEL.md` | `docs/03-architecture/DOMAIN_MODELS/OBSERVATION_DOMAIN_MODEL.md` | Move |
| `docs/decisions/ADR-*.md` | `docs/03-architecture/ADR/` | Move all ADRs |

## 04-ui-ux
| Original Path | Target Path | Action |
| --- | --- | --- |
| `N/A` | `docs/04-ui-ux/UI_UX_FOUNDATION.md` | Create new |
| `N/A` | `docs/04-ui-ux/DESIGN_SYSTEM.md` | Create new |
| `N/A` | `docs/04-ui-ux/SCREEN_FLOWS.md` | Create new |
| `N/A` | `docs/04-ui-ux/WIREFRAMES.md` | Create new |

## 05-engineering
| Original Path | Target Path | Action |
| --- | --- | --- |
| `docs/governance/DEVELOPMENT_GUIDELINES.md`<br>`docs/governance/AI_AGENT_INSTRUCTIONS.md`<br>`docs/governance/PROMPT_ENGINEERING.md` | `docs/05-engineering/CODING_STANDARDS.md` | Merge and Move |
| `docs/governance/TESTING_STRATEGY.md` | `docs/05-engineering/TESTING_STRATEGY.md` | Move |
| `docs/governance/QUALITY_GATE.md` | `docs/05-engineering/RELEASE_PROCESS.md` | Rename and Move |
| `docs/governance/CONTRIBUTING.md` | `docs/05-engineering/CONTRIBUTING.md` | Move |

## 06-operations
| Original Path | Target Path | Action |
| --- | --- | --- |
| `docs/DEPLOYMENT.md` | `docs/06-operations/DEPLOYMENT.md` | Move |
| `docs/security/INVESTIGATION_PLAYBOOK.md` | `docs/06-operations/RUNBOOKS.md` | Rename and Move |
| `N/A` | `docs/06-operations/BACKUP_RECOVERY.md` | Create new |
| `N/A` | `docs/06-operations/MONITORING.md` | Create new |
| `N/A` | `docs/06-operations/INCIDENT_RESPONSE.md` | Create new |

## 07-governance
| Original Path | Target Path | Action |
| --- | --- | --- |
| `docs/planning/RISK_REGISTER_MASTER.md` | `docs/07-governance/RISK_REGISTER.md` | Rename and Move |
| `docs/planning/TECHNICAL_DEBT_REGISTER.md`<br>`docs/OPEN_FINDINGS.md` | `docs/07-governance/TECHNICAL_DEBT_REGISTER.md` | Merge and Move |
| `docs/decisions/DECISIONS.md` | `docs/07-governance/DECISION_LOG.md` | Rename and Move |
| `docs/governance/TRACEABILITY_MATRIX.md` | `docs/07-governance/TRACEABILITY_MATRIX.md` | Overwrite/Recreate |
| `docs/governance/GOVERNANCE.md`<br>`docs/governance/AGENT_TASK_EXECUTION_FRAMEWORK.md`<br>`docs/governance/SELF_IMPROVEMENT_POLICY.md` | `docs/07-governance/DOCUMENTATION_GOVERNANCE_STANDARD.md` | Merge and Move |

## 08-history
All historical sprint plans, phase reports, audit reports, architecture reviews, and legacy docs will be archived here without modification.
| Source Directory | Target Directory |
| --- | --- |
| `PHASE_6_COMPLETION_REPORT.md` | `docs/08-history/phase-reports/` |
| `docs/reports/` (all subdirs) | `docs/08-history/` (mapped to phase, sprint, task, audit, review reports) |
| `docs/planning/SPRINT_*` | `docs/08-history/sprint-reports/` |
| `docs/audits/` | `docs/08-history/audit-reports/` |
| `docs/architecture/ARCHITECTURE_REVIEW_REPORT.md` | `docs/08-history/review-reports/` |

## Root
| Original Path | Target Path | Action |
| --- | --- | --- |
| `README.md` | `README_V2.md` | Replace |
| `N/A` | `docs/PROJECT_OVERVIEW.md` | Create new |
