# CI/CD Validation Standard

This standard establishes the governance rules for Continuous Integration validation within the ASTRA platform.

## 1. The Source of Truth

**GitHub Actions is the Source of Truth.**

Under no circumstances is local execution of tests, linters, or coverage reports sufficient to mark a task as complete. Local environments are subject to discrepancies, uncommitted files, and missing dependencies. 

## 2. Validation Requirements

A task or feature may only be considered validated and marked **COMPLETE** when:
1. Changes are fully committed.
2. Changes are pushed to the remote repository.
3. GitHub Actions are triggered and executed.
4. All required workflows have passed successfully.

## 3. Reporting Standards

All future phase reports, validation reports, and pull request descriptions must contain explicitly linked evidence from CI. Reports must include:

- **Local Validation:** Summary of local execution (for context only).
- **CI Validation:** Confirmation that CI pipelines ran.
- **Workflow Run ID:** The unique identifier for the GitHub Actions run.
- **Commit SHA:** The specific git commit validated by CI.
- **GitHub Actions Results:** The outcome of the pipeline (e.g., PASSED).
- **Final Status:** The ultimate GO/NO-GO status based on CI results.

Future reports cannot claim a GO status without concrete CI evidence.
