# Mandatory Agentic Workflow

All agents MUST execute this workflow sequentially:

1. **Context Loading**
   - Gather inputs, requirements, and historical data.
2. **Repository Review**
   - Assess current state of relevant files and architecture.
3. **Risk Assessment**
   - Identify what could go wrong, especially regarding security and stability.
4. **Root Cause Analysis**
   - Required for bugs. Do not guess; prove the root cause.
5. **Implementation Plan**
   - Draft a plan of attack before making any modifications.
6. **Implementation**
   - Execute the planned changes.
7. **Validation**
   - Ensure the changes pass CI/CD (GitHub Actions).
8. **Documentation**
   - Update `README.md`, `docs/`, and any relevant standards.
9. **Reporting**
   - Generate required phase reports.
