# Definition of Done

This standard outlines the formal Definition of Done (DoD) for all tasks, features, and pull requests within the ASTRA platform.

## 1. Source of Truth

**GitHub Actions is the absolute Source of Truth.** Local validation alone is insufficient and cannot be used as the sole evidence of completion.

## 2. Required Criteria

A task may only be marked **COMPLETE** when all the following conditions are met:

### Code Complete
- All required code is written and adheres to the ASTRA `CODING_STANDARD_GLOBAL.md`.
- No temporary debug code or bypassed security controls remain.

### Tests Complete
- Unit tests and integration tests are written and pass.
- 100% code coverage is maintained.

### Documentation Complete
- Relevant documentation (`ARCHITECTURE.md`, `PRD.md`, Phase Reports) is updated.
- Inline docstrings and type hints are accurate.

### GitHub Actions Pass
- Changes committed.
- Changes pushed to the repository.
- GitHub Actions executed.
- All required workflows passed successfully.
