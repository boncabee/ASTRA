# Report Storage Standard

This document enforces the strict governance policies regarding the generation, categorization, and storage of all reports and audits within the ASTRA repository.

## 1. Mandatory Storage Rule
> [!CAUTION]
> **ABSOLUTE RULE:** No report, audit, review, or dynamically generated output file of any kind may be placed in the repository root (`/`). All future agents and contributors MUST place generated reports under the appropriate subdirectory within `docs/`. Failure to comply violates ASTRA governance.

## 2. Allowed Locations & Categories
Reports must be classified and stored in one of the following exact directories:
- `docs/audits/`: Formal technical, security, and repository audits.
- `docs/reviews/`: Code, architecture, or documentation review readouts.
- `docs/reports/`: General assessments, migration plans, and gap analyses.
- `docs/validation/`: Go/No-Go readiness checks (e.g., Enterprise Readiness, Release Readiness).
- `docs/governance/`: Standards alignment readouts and policy enforcement reports.
- `docs/phase-reports/`: High-level completion reports for major roadmap phases.
- `docs/sprint-reports/`: Agile sprint planning, retrospective, and completion reports.
- `docs/task-reports/`: Granular readouts for specific Jira/GitHub tasks.

## 3. Naming Conventions
- **Format:** `UPPER_SNAKE_CASE.md`
- **Suffix:** All reports must end with `_REPORT.md`, `_PLAN.md`, or `_MATRIX.md`.
- **Prefix (Temporal):** When applicable, prefix with the scope (e.g., `PHASE_6_5_COMPLETION_REPORT.md` or `SPRINT_3_RETROSPECTIVE_REPORT.md`).

## 4. Archiving Process
Active reports belong in the directories listed in Section 2. When a report is superseded or the phase it documents is formally closed:
1. It is moved to `docs/history/[category]/`.
2. A GitHub Alert (`> [!WARNING] Archived`) is prepended to the top of the file to prevent it from being treated as current context.

## 5. Historical Retention Process
- **Immutable History:** Reports detailing architectural decisions, audits, and phase completions are permanent historical artifacts. They are never deleted, only archived.
- **De-duplication:** If an agent generates an updated version of a report with the identical filename, the previous version MUST be overwritten. Do not create `_v2`, `_final`, or `_new` suffixes.

## 6. Future Report Generation Requirements
When an automated agent or human contributor is tasked with generating a report, they must first:
1. Determine the category based on Section 2.
2. Ensure the target directory exists within `docs/`.
3. Use `write_to_file` targeting the explicit `docs/[category]/` path.
