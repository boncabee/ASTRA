# Phase 16.9B: Observations Explorer Design

## Objective
Design a high-performance, dense, and intuitive Observations Explorer for ASTRA. This module will serve as the primary hunting and triage interface for Tier 1 SOC Analysts to process raw security observations before they are correlated into Cases.

## 1. User Workflow
The primary workflow for a Tier 1 SOC Analyst using the Observations Explorer is:
1. **Discover**: Analyst opens the explorer and views the default queue (typically sorted by `created_at` DESC or `risk_score` DESC).
2. **Filter & Hunt**: Analyst applies filters (e.g., `status=NEW`, `risk_category=CRITICAL`) to narrow down a massive dataset of 10,000+ records to a manageable subset.
3. **Investigate**: Analyst clicks on a specific observation to view its raw JSON metadata, correlation matches, and evidence.
4. **Action**: Analyst updates the status of the observation (e.g., dismissing it as a false positive by marking it `CLOSED`, or escalating it to a Case).

## 2. Information Architecture
The Observations Explorer will exist as a primary route: `/observations`.
- **Top Bar**: Global page title, aggregate counts (e.g., "120 Critical Observations"), and a "Create Observation" manual entry stub.
- **Filter Bar**: A horizontally scrolling or collapsible bar containing specialized dropdowns and date-pickers.
- **Data Grid**: The core table.
- **Detail Pane**: A slide-out drawer (Sheet) or expandable row (Accordion) for viewing record details without losing context of the main table.

## 3. Table Design
**Density**: "Compact" by default. Tier 1 analysts need to see as many rows as possible on a standard 1080p monitor.
**Columns**:
1. `Checkbox` (For bulk actions)
2. `ID` (Truncated UUID, monospace)
3. `Risk` (Visual indicator/badge based on `risk_score` 0-100)
4. `Status` (Badge: NEW, TRIAGED, ESCALATED, CLOSED)
5. `Classification` (e.g., "Malware", "Phishing")
6. `Created At` (Formatted timestamp)

**Sorting**: Columns `Risk`, `Status`, `Classification`, and `Created At` will have clickable headers to trigger `sort_by` and `sort_order` URL mutations.

## 4. Filter Design
Filters will be driven entirely by the URL `searchParams` to ensure link-sharing works seamlessly between analysts.
- **Status Filter**: Multi-select dropdown (mapped to `status`).
- **Risk Category Filter**: Dropdown mapping to score bands (e.g., CRITICAL, HIGH).
- **Classification Filter**: Select menu populated by known classifications.
- **Time Range Filter**: Date picker for `created_after` and `created_before`.

## 5. Detail View Design
Clicking a row will open a **Side Drawer (Sheet)** overlay from the right side of the screen.
- **Header**: Observation ID, Title, and Risk Badge.
- **Body**: 
  - Description string.
  - Formatted JSON tree view for `metadata` / raw event data.
  - Correlation ID (with a link to the correlated Case if applicable).
- **Footer**: Action buttons (Update Status, Escalate, Dismiss).

## 6. Performance Strategy
Supporting scales of 100,000+ records requires careful architectural decisions:
- **Server-Side Rendering (SSR)**: All data fetching occurs on the server to prevent sending massive JSON payloads to the browser.
- **URL-Driven State**: React state (`useState`) will *not* be used for table data. The URL is the single source of truth.
- **Pagination Strategy**: Standard Offset/Limit pagination (50 items per page). 
- **Deep Pagination Mitigation**: At 100,000+ records, `OFFSET 99950` becomes extremely slow on PostgreSQL. The UI will prominently encourage analysts to use Time Range and Risk filters to narrow the dataset rather than clicking "Next Page" 2,000 times.
- **Concurrent UI**: Utilizing Next.js `useTransition()` and `Suspense` boundaries to show loading skeletons instantly while the server fetches new data.

## 7. MVP Scope
The immediate implementation (Phase 16.10) will include:
- The `/observations` route.
- The Data Table with 50-item offset pagination.
- URL-driven sorting (Clickable headers).
- URL-driven filtering (Status and Risk Category dropdowns).
- Basic Side Drawer for viewing the Observation detail.
- Ability to update a single observation's status via the API.

## 8. Post-MVP Scope
Future enhancements (Not included in MVP):
- **Bulk Actions**: Selecting multiple rows to update status simultaneously.
- **Websockets/SSE**: Live updating the table as new observations stream in.
- **Advanced Query Language**: A search bar supporting Lucene-style syntax (e.g., `metadata.ip_address:"192.168.1.1"`).
- **Keyset Pagination**: Upgrading the backend from Offset/Limit to cursor-based pagination for infinite scroll on massive datasets.
