# PHASE 16.9: Observations Capability Audit

## Objective
Assess the readiness of the backend API and database schemas to support the development of a fully featured Observations Explorer on the frontend, focusing on data manipulation, filtering, sorting, and pagination at scale.

## Review Findings

### 1. What observation APIs exist?
The `observations` router (`api/v1/observations.py`) provides three core endpoints:
- `GET /api/v1/observations`: List observations (with pagination, filters, and total count).
- `GET /api/v1/observations/{id}`: Retrieve a specific observation by its UUID.
- `PUT /api/v1/observations/{id}`: Update an observation's status.

### 2. What filters exist?
The `GET /api/v1/observations` endpoint supports a comprehensive set of filters:
- `status`: Filter by enum (e.g., NEW, TRIAGED).
- `risk_category`: A string mapping to score ranges (e.g., "HIGH" translates to `score >= 70 AND score <= 89`).
- `classification`: Exact match string filtering.
- `created_after` & `created_before`: Datetime bounds for time-range filtering.

### 3. What pagination model exists?
The backend uses standard **Offset/Limit** pagination (`skip` and `limit` query parameters). 
Crucially, the repository performs a `func.count()` query alongside the data query, meaning the endpoint returns both the `data` array and the `total` integer. This is required for building a standard table pagination UI.

### 4. What scale is supported?
- **Page Size**: Capped at 1000 items per request (`le=1000`).
- **Deep Pagination**: Because it relies on `OFFSET`, deep pagination (e.g., skipping 500,000 rows) will suffer from performance degradation as the database must scan and discard rows. 
- **Counting**: The `func.count()` operation over large, unfiltered datasets can become a bottleneck at the multi-million row scale, though indexing on commonly filtered columns (like `status` and `created_at`) can mitigate this.

### 5. Is the backend ready for an Observations Explorer?
**No. It is Partially Ready.**
While the filtering and pagination foundations are solid, the API **completely lacks dynamic sorting**. 
The repository hardcodes the sort order: `query.order_by(Observation.created_at.desc())`. An Observations Explorer fundamentally requires the ability to sort by severity (`risk_score`), classification, and status to allow analysts to prioritize their triage queue. Without exposing `sort_by` and `order` parameters, the frontend UI cannot offer clickable column headers.

## Decision

**PARTIALLY READY**

## Recommendations
Before frontend implementation begins, the backend API (`observations.py`) and repository (`ObservationRepository.list`) must be updated to accept and apply dynamic sorting parameters (e.g., `sort_by="risk_score"`, `sort_order="desc"`).
