# Phase 8.1.6 Coverage Gap Analysis

## Executive Summary
This analysis identifies the exact coverage gaps responsible for the backend test suite falling below the 99% threshold in the GitHub Actions CI pipeline, and documents the root cause of the measurement discrepancy.

## Root Cause: Coverage Scope Mismatch

The CI pipeline originally ran:
```
pytest --cov=app --cov-fail-under=99 tests/
```

However, `pytest.ini` also specifies:
```ini
addopts = --cov=app --cov=models --cov=repositories --cov=services --cov-report=term-missing
```

When pytest merges these, the resulting coverage scope covers **four directories**: `app/`, `models/`, `repositories/`, and `services/`. The 99% gate was applied against the combined 1,908 statements, where repository and service modules had significant uncovered branches.

## Gap Inventory

| Module | Stmts | Miss | Cover | Missing Lines | Description |
|--------|-------|------|-------|---------------|-------------|
| `repositories/observation.py` | 56 | 13 | 77% | 15-23, 30-31, 53, 58, 62, 65-66, 69 | `create()`, `get_by_correlation_id()`, all risk category filter branches |
| `repositories/case_assignment.py` | 18 | 3 | 83% | 31-37 | `get_by_case_id()` query execution |
| `repositories/automation.py` | 48 | 3 | 94% | 89-91 | Execution time aggregation loop body in `get_metrics()` |
| `repositories/report.py` | 40 | 3 | 92% | 55-57 | `get_compliance_mappings()` query |
| `app/core/versioning.py` | 26 | 3 | 88% | 41, 48-49 | `migrate_to_latest()` pass branch, `_migrate_1_0_to_2_0()` stub |
| `app/schemas/ces.py` | 113 | 1 | 99% | 133 | Non-string severity validator return path |
| `services/case.py` | 114 | 1 | 99% | 151 | `current_status is None` guard clause |
| **TOTAL** | **1,908** | **27** | **98.58%** | | |

## Required Remediation
At 98.58% (27 missed lines of 1,908 total), the threshold requires covering at least **8 additional lines** to reach 99% (≤19 misses). The strategy focused on the largest gap first (`repositories/observation.py` at 13 lines) followed by the remaining modules.

## Priority Order
1. **P0**: `repositories/observation.py` — 13 lines, highest impact
2. **P1**: `repositories/case_assignment.py` — 3 lines
3. **P1**: `repositories/automation.py` — 3 lines
4. **P1**: `repositories/report.py` — 3 lines
5. **P2**: `app/core/versioning.py` — 3 lines
6. **P2**: `services/case.py` — 1 line
7. **P3**: `app/schemas/ces.py` — 1 line (difficult to exercise via tests)
