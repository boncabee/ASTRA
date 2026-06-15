# Document Inventory

| File | Classification | Owner | Purpose | Replacement Document (If any) | Recommended Action |
| --- | --- | --- | --- | --- | --- |
| `PHASE_6_COMPLETION_REPORT.md` | HISTORICAL | Engineering Team | Phase 6 closure report | N/A | ARCHIVE (`08-history/phase-reports/`) |
| `README.md` | OBSOLETE | Architecture Team | Project overview | `README_V2.md` | MERGE / DELETE |
| `docs/DEPLOYMENT.md` | AUTHORITATIVE | Operations Team | Deployment guidelines | N/A | KEEP (Move to `06-operations/`) |
| `docs/IMPLEMENTATION_HISTORY.md` | HISTORICAL | Architecture Team | High-level execution log | N/A | ARCHIVE (`08-history/`) |
| `docs/OPEN_FINDINGS.md` | SUPPORTING | Security Team | Open audit findings | `TECHNICAL_DEBT_REGISTER.md` | MERGE |
| `docs/REPORT_INDEX.md` | OBSOLETE | Architecture Team | Index of historical reports | N/A | DELETE |
| `docs/architecture/API_SPEC.md` | AUTHORITATIVE | Architecture Team | API definitions | N/A | KEEP (Move to `03-architecture/`) |
| `docs/architecture/ARCHITECTURE.md` | AUTHORITATIVE | Architecture Team | System architecture overview | `SDD.md` | MERGE |
| `docs/architecture/ARCHITECTURE_DECISION_RECORD.md` | HISTORICAL | Architecture Team | Old ADR template / log | `DECISION_LOG.md` | ARCHIVE |
| `docs/architecture/ARCHITECTURE_REVIEW_REPORT.md` | HISTORICAL | Architecture Team | Sprint 2 architecture review | N/A | ARCHIVE (`08-history/review-reports/`) |
| `docs/architecture/CES_IMPLEMENTATION_GUIDE.md` | AUTHORITATIVE | Engineering Team | CES events implementation | `COMMON_EVENT_SCHEMA.md` | KEEP / MERGE |
| `docs/architecture/COMMON_EVENT_SCHEMA.md` | AUTHORITATIVE | Architecture Team | CES event definitions | N/A | KEEP (Move to `03-architecture/`) |
| `docs/architecture/CORRELATION_DOMAIN_MODEL.md` | AUTHORITATIVE | Architecture Team | Correlation domain mapping | N/A | KEEP (Move to `03-architecture/DOMAIN_MODELS/`) |
| `docs/architecture/CORRELATION_ENGINE_SPEC.md` | SUPPORTING | Architecture Team | Correlation logic details | `SRS.md` / `SDD.md` | MERGE |
| `docs/architecture/DATABASE_SCHEMA.md` | AUTHORITATIVE | Data Engineering | Database schema | N/A | KEEP (Move to `03-architecture/`) |
| `docs/architecture/OBSERVATION_DOMAIN_MODEL.md` | AUTHORITATIVE | Architecture Team | Observation domain mapping | N/A | KEEP (Move to `03-architecture/DOMAIN_MODELS/`) |
| `docs/architecture/PARSER_FRAMEWORK_SPEC.md` | SUPPORTING | Architecture Team | Parser framework logic | `SDD.md` | MERGE |
| `docs/architecture/REPOSITORY_BOOTSTRAP_SPEC.md` | OBSOLETE | Architecture Team | Initial repo setup | N/A | DELETE |
| `docs/architecture/REPOSITORY_STRUCTURE.md` | OBSOLETE | Architecture Team | Repo file structure | `DOCUMENTATION_GOVERNANCE_STANDARD.md` | DELETE |
| `docs/architecture/SPRINT_3_ARCHITECTURE_BASELINE.md` | HISTORICAL | Architecture Team | Sprint 3 baseline | N/A | ARCHIVE (`08-history/phase-reports/`) |
| `docs/architecture/TECH_STACK.md` | SUPPORTING | Architecture Team | Technology stack listing | `SDD.md` | MERGE |
| `docs/audits/AUDIT.md` | HISTORICAL | Security Team | General audit | N/A | ARCHIVE (`08-history/audit-reports/`) |
| `docs/audits/PRE_IMPLEMENTATION_AUDIT.md` | HISTORICAL | Architecture Team | Initial pre-implementation check | N/A | ARCHIVE (`08-history/audit-reports/`) |
| `docs/decisions/ADR-010_PRODUCT_DELIVERY_MODEL.md` | AUTHORITATIVE | Architecture Team | Delivery model decision | N/A | KEEP (Move to `03-architecture/ADR/`) |
| `docs/decisions/ADR-011_AUTHENTICATION_RBAC.md` | AUTHORITATIVE | Security Team | RBAC decision | N/A | KEEP (Move to `03-architecture/ADR/`) |
| `docs/decisions/ADR-012_AI_PROVIDER_ABSTRACTION_LAYER.md` | AUTHORITATIVE | Architecture Team | AI provider architecture | N/A | KEEP (Move to `03-architecture/ADR/`) |
| `docs/decisions/ADR-013_OBSERVATION_POLICY_ARCHITECTURE.md` | AUTHORITATIVE | Architecture Team | Policy engine decision | N/A | KEEP (Move to `03-architecture/ADR/`) |
| `docs/decisions/ADR-014_AUTOMATION_ENGINE_ARCHITECTURE.md` | AUTHORITATIVE | Architecture Team | Automation architecture | N/A | KEEP (Move to `03-architecture/ADR/`) |
| `docs/decisions/DECISIONS.md` | AUTHORITATIVE | Architecture Team | Main decision log | `DECISION_LOG.md` | KEEP (Move to `07-governance/`) |
| `docs/governance/AGENT_TASK_EXECUTION_FRAMEWORK.md` | SUPPORTING | Engineering Team | Execution workflows | `DOCUMENTATION_GOVERNANCE_STANDARD.md` | MERGE / DELETE |
| `docs/governance/AI_AGENT_INSTRUCTIONS.md` | SUPPORTING | Engineering Team | Rules for AI agents | `CODING_STANDARDS.md` | MERGE |
| `docs/governance/CONTRIBUTING.md` | AUTHORITATIVE | Engineering Team | Contributor guide | N/A | KEEP (Move to `05-engineering/`) |
| `docs/governance/DEVELOPMENT_GUIDELINES.md` | SUPPORTING | Engineering Team | Code style guide | `CODING_STANDARDS.md` | MERGE |
| `docs/governance/GOVERNANCE.md` | OBSOLETE | Architecture Team | Previous governance doc | `DOCUMENTATION_GOVERNANCE_STANDARD.md`| DELETE |
| `docs/governance/PROMPT_ENGINEERING.md` | SUPPORTING | Data Science Team | Prompt best practices | `CODING_STANDARDS.md` | MERGE |
| `docs/governance/QUALITY_GATE.md` | SUPPORTING | QA Team | Quality constraints | `RELEASE_PROCESS.md` | MERGE |
| `docs/governance/SELF_IMPROVEMENT_POLICY.md` | SUPPORTING | Operations Team | Improvement policy | `DOCUMENTATION_GOVERNANCE_STANDARD.md`| MERGE |
| `docs/governance/TESTING_STRATEGY.md` | AUTHORITATIVE | QA Team | Testing approaches | N/A | KEEP (Move to `05-engineering/`) |
| `docs/governance/TRACEABILITY_MATRIX.md` | OBSOLETE | Architecture Team | Requirement mapping | `TRACEABILITY_MATRIX.md` | MERGE / DELETE |
| `docs/planning/IMPLEMENTATION_STRATEGY.md` | HISTORICAL | Product Team | Outdated strategy doc | N/A | ARCHIVE (`08-history/`) |
| `docs/planning/PRD.md` | OBSOLETE | Product Team | Outdated PRD | `PRD.md` (New) | MERGE |
| `docs/planning/PROJECT_PLAN.md` | HISTORICAL | Project Management| Old project plan | N/A | ARCHIVE (`08-history/`) |
| `docs/planning/RELEASE_PLAN.md` | SUPPORTING | Project Management| Release phases | `ROADMAP.md` | MERGE |
| `docs/planning/RISK_REGISTER_MASTER.md` | AUTHORITATIVE | Security Team | Risk tracking | `RISK_REGISTER.md` | KEEP (Move to `07-governance/`) |
| `docs/planning/ROADMAP.md` | OBSOLETE | Product Team | V1 Roadmap | `ROADMAP.md` (New) | DELETE |
| `docs/planning/ROADMAP_V2.md` | AUTHORITATIVE | Product Team | Current roadmap | `ROADMAP.md` | KEEP (Move to `01-product/`) |
| `docs/planning/SPRINT_*_TASKS.md` | HISTORICAL | Project Management| Sprint backlogs | N/A | ARCHIVE (`08-history/sprint-reports/`) |
| `docs/planning/SPRINT_3_*.md` | HISTORICAL | Project Management| Sprint 3 artifacts | N/A | ARCHIVE (`08-history/sprint-reports/`) |
| `docs/planning/TASKS.md` | HISTORICAL | Project Management| Unsorted tasks | N/A | ARCHIVE (`08-history/`) |
| `docs/planning/TECHNICAL_DEBT_REGISTER.md` | AUTHORITATIVE | Engineering Team | Tech debt tracking | N/A | KEEP (Move to `07-governance/`) |
| `docs/planning/USER_FLOW.md` | OBSOLETE | UX Team | Old user flows | `USER_FLOW.md` | MERGE / DELETE |
| `docs/reports/*` | HISTORICAL | Varied | Phase/Sprint/Task reports| N/A | ARCHIVE (`08-history/...`) |
| `docs/security/ATTACK_KNOWLEDGE_MODEL.md` | AUTHORITATIVE | Security Team | Threat mapping | `SECURITY_REQUIREMENTS.md` | MERGE / KEEP |
| `docs/security/INVESTIGATION_PLAYBOOK.md` | AUTHORITATIVE | Security Team | Incident runbooks | `RUNBOOKS.md` | MERGE / KEEP |
| `docs/security/SECURITY.md` | OBSOLETE | Security Team | Old security doc | `SECURITY_REQUIREMENTS.md` | DELETE |
| `docs/security/THREAT_MODEL.md` | AUTHORITATIVE | Security Team | Threat modeling | `SECURITY_REQUIREMENTS.md` | MERGE / KEEP |
