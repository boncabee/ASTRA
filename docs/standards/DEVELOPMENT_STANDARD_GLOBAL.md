# Global Development Standard

This document governs the collaborative development lifecycle, branching strategy, and release mechanics for the ASTRA platform.

## 1. Branching Strategy
ASTRA utilizes a streamlined Trunk-Based Development model.
- **`main`:** The primary integration branch. Code in `main` is considered stable and deployable to staging.
- **`feature/*`:** For new features (e.g., `feature/TASK-3011-celery-worker`).
- **`bugfix/*`:** For resolving defects.
- **`hotfix/*`:** For urgent production fixes branching directly from a release tag.

## 2. Git Workflow
1. Developer creates a branch from the latest `main`.
2. Developer commits atomic, logically grouped changes.
3. Developer pushes the branch and opens a Pull Request (PR) against `main`.
4. CI pipeline runs automatically (Lint, Test, SAST).
5. Code is reviewed. Once approved and CI passes, it is Squash-Merged into `main`.

## 3. Commit Message Convention
ASTRA enforces the **Conventional Commits** specification to enable automated changelog generation.
- **Format:** `<type>(<scope>): <description>`
- **Types:**
  - `feat`: A new feature.
  - `fix`: A bug fix.
  - `docs`: Documentation only changes.
  - `style`: Formatting changes (Black/Ruff).
  - `refactor`: Code change that neither fixes a bug nor adds a feature.
  - `test`: Adding missing tests.
  - `chore`: Maintenance tasks (e.g., dependency updates).
- **Example:** `feat(automation): add redis connection retry logic`

## 4. Pull Request Standards
A Pull Request must:
- Reference an active `TASK-[ID]`.
- Be reasonably sized (ideally < 500 lines of code changed, excluding generated lock files).
- Include an updated test suite proving the code works (or fails correctly).
- Pass all automated Quality Gates.

## 5. Review Standards
- **Mandatory Approvals:** Every PR requires at least 1 approval from a peer engineer. Architectural changes require an approval from a Lead Architect.
- **Reviewer Responsibilities:** Reviewers must check for logic errors, adherence to `CODING_STANDARD_GLOBAL.md`, security vulnerabilities, and sufficient test coverage.
- **Tone:** Code reviews must be respectful, objective, and focused on the code, not the developer.

## 6. Versioning Standards
ASTRA adheres to **Semantic Versioning (SemVer 2.0.0)**.
- **Format:** `MAJOR.MINOR.PATCH`
- **MAJOR:** Incompatible API changes or massive architectural shifts.
- **MINOR:** New functionality added in a backwards-compatible manner.
- **PATCH:** Backwards-compatible bug fixes.

## 7. Release Standards
- Releases are tagged in Git using the SemVer format (e.g., `v1.2.0`).
- A GitHub Release is created automatically, pulling the changelog from the Conventional Commits since the last tag.
- Deployment artifacts (Docker images) are built, tagged identically (`boncabee/astra:v1.2.0`), and published to the container registry.
