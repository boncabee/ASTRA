# Agent Skill Governance Standard

## 1. Purpose
This document establishes the formal governance framework for AI agent skills utilized within the ASTRA platform. It defines the standards for skill selection, management, and usage to ensure that all agent-driven development aligns with ASTRA's architectural principles, quality gates, and enterprise standards.

## 2. Skill Governance Principles
- **Repository Authority:** The ASTRA repository is the ultimate source of truth for all agent skills. Local project configurations override global workstation settings.
- **Standardized Execution:** Agents must rely on approved, version-controlled skills to ensure deterministic and compliant development outcomes.
- **Continuous Alignment:** Agent skills must align with ASTRA's Definition of Done, CI/CD validations, and global development standards.
- **Auditable Workflows:** The usage, addition, and deprecation of agent skills must be tracked, reviewed, and audited like any other codebase dependency.

## 3. Repository Source of Truth
Project skills must be loaded strictly from the local repository directory:
`.agents/skills/`

All installed skills are tracked and versioned through the lockfile:
`skills-lock.json`

**Rule:** Repository-managed skills explicitly take precedence over any global workstation skills installed on the developer's machine.

## 4. Skill Classification

### Mandatory Skills
These skills must be active and adhered to during relevant development tasks. They enforce core ASTRA architectural and quality standards.
- `api-and-interface-design`
- `ci-cd-and-automation`
- `code-review-and-quality`
- `documentation-and-adrs`
- `postgresql-table-design`
- `python-testing-patterns`
- `security-and-hardening`
- `spec-driven-development`
- `test-driven-development`

### Recommended Skills
These skills represent highly effective workflows and best practices within the ASTRA ecosystem.
- `context-engineering`
- `debugging-and-error-recovery`
- `git-workflow-and-versioning`
- `incremental-implementation`
- `planning-and-task-breakdown`
- `nextjs-app-router-patterns`
- `vercel-react-best-practices`
- `frontend-ui-engineering`

### Optional Skills
These skills may be used at the agent's or developer's discretion for supplementary tasks.
- `code-simplification`
- `deprecation-and-migration`
- `performance-optimization`
- `shipping-and-launch`
- `idea-refine`
- `interview-me`
- `doubt-driven-development`
- `find-skills`
- `using-agent-skills`

## 5. Skill Selection Rules
1. **Mandatory Enforcement:** Agents must leverage Mandatory Skills for any code generation, testing, or architectural task.
2. **Contextual Application:** Recommended and Optional Skills should be loaded dynamically based on the specific domain of the task (e.g., using `nextjs-app-router-patterns` only when modifying the frontend).
3. **No Unapproved Skills:** Agents are prohibited from using or installing skills that are not documented in this standard or tracked in `skills-lock.json` without formal architectural review.

## 6. Agent Startup Procedure
Before commencing any implementation, an AI agent operating within the ASTRA repository must execute the following startup procedure:

1. Read `docs/standards/DEFINITION_OF_DONE.md`
2. Read `docs/standards/CI_CD_VALIDATION_STANDARD.md`
3. Read `docs/standards/DEVELOPMENT_STANDARD_GLOBAL.md`
4. Load applicable skills from `.agents/skills/` based on the task requirements.
5. Execute task following the loaded skill protocols.
6. Validate via GitHub Actions (ensure local validation is not treated as final).

## 7. CI/CD Source of Truth Integration
Agent operations and skill-driven code modifications are subject to the same rigorous validation as human-authored code. 
- Local test execution and validation are insufficient for task completion.
- The GitHub Actions CI/CD pipeline is the definitive source of truth for all validations.
- Agents must rely on CI pipeline execution for final validation of test coverage, security scans, and code quality.

## 8. Skill Lifecycle Management
The lifecycle of an agent skill is managed through standard repository pull request processes.
- New skills must be proposed via a PR, evaluated against ASTRA's security and architecture requirements, and approved by a core maintainer.
- Upon approval, the skill is added to `.agents/skills/` and `skills-lock.json` is updated.

## 9. Skill Update Process
- Skill updates must be executed via the designated package manager (`npx skills update` or equivalent).
- Updates must be committed in an isolated PR.
- The PR must pass all CI/CD quality gates to ensure the updated skill does not introduce regressions or misaligned code generation patterns.

## 10. Skill Deprecation Process
- If a skill is deemed obsolete or replaced by a superior standard, it must be formally deprecated.
- The skill must be removed from `.agents/skills/` and `skills-lock.json`.
- The `AGENT_SKILL_STANDARD.md` (this document) must be updated to reflect the removal.
- A phase report or ADR must be generated documenting the rationale for the skill's removal.
