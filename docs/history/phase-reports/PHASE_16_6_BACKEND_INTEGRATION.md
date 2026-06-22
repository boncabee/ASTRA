# Phase 16.6 Report: Backend Integration

## 1. Findings
The frontend shell and UX components developed in previous sprints were isolated from the live backend, relying entirely on static mock data. To validate the full operational capability of the platform, the frontend must interface with the existing FastAPI endpoints defined in Phase 7.

## 2. Root Cause
N/A - This phase was a planned transition from static prototyping to live system integration.

## 3. Plan
1. Establish a central API client configured to hit `http://localhost:8000/api/v1`.
2. Map the Next.js `searchParams` for pagination and filtering directly to the backend's query parameters (e.g., `skip`, `limit`, `case_status`).
3. Update the frontend TypeScript interfaces to strictly match the Pydantic schemas defined in `backend/schemas/case.py` (e.g., matching standard UUID formats and date strings).
4. Refactor the Server Components (`CasesPage`, `CaseDetailPage`) to await `fetch` calls.
5. Refactor the Client Components (`CaseActions`) to perform true `POST` actions to modify state.
6. Remove all traces of `mock-data.ts`.

## 4. Changes
- **API Client Layer**:
  - `src/lib/api/client.ts`: Developed a custom wrapper handling dynamic base URLs and standardized JSON request formatting.
  - **Dev Token Injection**: In order to bypass the backend's strict RBAC implementation without implementing a full Auth flow on the frontend, the client looks for a `NEXT_PUBLIC_DEV_TOKEN` environment variable and injects it as a Bearer Token.
- **Data Definitions**:
  - `src/types/index.ts`: Rewritten to perfectly align with the backend Models (`CaseResponse`, `CaseTimelineResponse`).
- **Pages**:
  - `Cases Queue`: Fetches data dynamically using `getCases({ skip, limit, status })`. Converted to `force-dynamic`.
  - `Case Detail`: Parallels fetches for the main case and its timeline events. Implements explicit `notFound()` handling if the API returns a 404.
- **Cleanup**: Deleted `src/lib/mock-data.ts` to ensure zero stale mock leakage.

## 5. Validation
- **TypeScript Strict Mode**: Zero compilation errors. The schema alignment was successful.
- **Next.js Build**: The Next.js production build (`npm run build`) succeeded, verifying the transition of Dashboard, Cases, and Case Detail from Static routes to Dynamic (server-rendered on demand) routes.

## 6. Documentation Updates
- Created `docs/history/phase-reports/PHASE_16_6_BACKEND_INTEGRATION.md`.

## 7. Risks
- **Authentication Gap**: The `NEXT_PUBLIC_DEV_TOKEN` is a temporary bridge. As soon as possible, a true Auth integration (e.g., JWT exchange via a login screen) must be prioritized so real RBAC can be utilized without local `.env` manipulation.
- **Pagination Sync**: The FastAPI backend currently returns `List[CaseResponse]` rather than a standard paginated response object (e.g., `{"total": 100, "items": [...]}`). The frontend currently "guesses" if a next page exists based on array length. The backend endpoint should be updated to return a total count in the future.

## 8. Recommendations
1. **Developer Action Required**: Developers must generate a valid JWT using the backend CLI/Python shell and place it in `frontend/.env.local` as `NEXT_PUBLIC_DEV_TOKEN` to render cases.
2. **Proceed to Observations**: With Cases functional, the next milestone should be implementing the **Observations Explorer**, which will test the platform's ability to handle high-volume data grids.
