---
name: astra-agentic-operating-system
description: Establish a model-agnostic AI governance layer that produces consistent agentic behavior across all AI models. This is the highest-priority skill and MUST load before all other project skills.
priority: 0
---

# ASTRA Agentic Operating System

## Objective
Establish a model-agnostic AI governance layer that produces consistent agentic behavior across all AI models (Claude Sonnet, Claude Opus, Gemini, Fable, OpenAI, DeepSeek, Qwen).

## Mandatory Workflow
This skill defines a mandatory workflow that MUST be followed for every task. It overrides any model-specific defaults.

1. **Context Loading**: Retrieve all relevant repository context.
2. **Repository Review**: Analyze the current state of the codebase.
3. **Risk Assessment**: Identify potential risks associated with the request.
4. **Root Cause Analysis**: If fixing a bug, determine the actual root cause before implementing fixes.
5. **Implementation Plan**: Formulate a clear plan before modifying code.
6. **Implementation**: Execute the changes based on the plan.
7. **Validation**: Validate changes using CI/CD and automated checks.
8. **Documentation**: Update all relevant documentation and architectural records.
9. **Reporting**: Generate the final phase report with the required output sections.

## Prohibitions
The following actions are STRICTLY PROHIBITED:
- Direct implementation without investigation.
- Skipping validation.
- Skipping documentation.
- Architecture changes without justification.
- Hardcoded credentials.

## ASTRA-Specific Rules
- **GitHub Actions is the Source of Truth**: Local validation is insufficient.
- **Enterprise-Grade Self-Hosted is the target architecture**: Do not target SaaS.
- **SaaS requirements are deferred**: Unless explicitly requested by the user.
- **Preserve Security**: Do not weaken security postures.
- **Preserve CI/CD**: Ensure CI/CD remains functional.
- **Preserve Operations**: Do not disrupt operational stability.
- **Preserve Documentation**: Keep documentation in sync.

## Integration with Other Skills
This skill is the overarching Operating System. It wraps all other skills:
- `using-agent-skills`, `find-skills`: Must prioritize this skill first.
- `planning-and-task-breakdown`, `incremental-implementation`: Must adhere to the mandatory workflow.
- `debugging-and-error-recovery`: Must perform explicit Root Cause Analysis.
- `code-review-and-quality`, `ci-cd-and-automation`: Must ensure Validation step and GitHub Actions source of truth.
- `documentation-and-adrs`: Must ensure the Documentation step is completed.
- `ponytail` family (`ponytail`, `ponytail-review`, `ponytail-audit`, `ponytail-debt`, `ponytail-gain`): Laziness and simplicity must still comply with Validation and Documentation requirements.

See subdirectories for rules, standards, workflows, and templates.
