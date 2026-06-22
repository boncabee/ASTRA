# Phase 16.1: Frontend Architecture Design

## 1. Overview
This document defines the technical architecture for the ASTRA frontend. Based on the Operator Experience Design (Phase 16), the frontend will serve as an Enterprise-Grade Self-Hosted security tool for Tier 1 SOC Analysts and Security Engineers. The architecture leverages the Next.js 16+ App Router, React 19, and Tailwind CSS v4, focusing on performance, scalability, and robust data fetching for high-volume security telemetry.

## 2. Directory Structure
The application follows a modular, feature-grouped directory structure within the `src` directory, adhering to Next.js App Router conventions.

```text
src/
├── app/                  # Next.js App Router (Routes, Layouts, Pages)
│   ├── (auth)/           # Authentication route group
│   ├── (dashboard)/      # Main operator dashboard route group
│   ├── globals.css       # Global styles and Tailwind v4 theme configuration
│   └── layout.tsx        # Root layout (Providers, Theme)
├── components/           # Reusable UI components
│   ├── ui/               # Base component library (e.g., shadcn/ui components)
│   ├── layout/           # Shared layout components (Sidebar, TopNav)
│   └── domain/           # Domain-specific components (e.g., CaseTimeline)
├── lib/                  # Utilities and core configuration
│   ├── api/              # API client and fetch wrappers
│   ├── utils.ts          # Helper functions (e.g., Tailwind merge)
│   └── constants.ts      # Global constants
├── hooks/                # Custom React hooks
├── types/                # TypeScript definitions (Models, API Responses)
└── store/                # Global client state (if applicable)
```

## 3. Route Structure
Routing is organized using Next.js Route Groups to separate authentication from the main application layout without affecting the URL paths.

*   `app/(auth)/login/page.tsx` -> `/login`
*   `app/(dashboard)/layout.tsx` -> Shared Sidebar Navigation
*   `app/(dashboard)/dashboard/page.tsx` -> `/dashboard`
*   `app/(dashboard)/cases/page.tsx` -> `/cases`
*   `app/(dashboard)/cases/[id]/page.tsx` -> `/cases/[id]`
*   `app/(dashboard)/alerts/page.tsx` -> `/alerts`
*   `app/(dashboard)/observations/page.tsx` -> `/observations`
*   `app/(dashboard)/policies/page.tsx` -> `/policies`
*   `app/(dashboard)/policies/[id]/page.tsx` -> `/policies/[id]`
*   `app/(dashboard)/automations/page.tsx` -> `/automations`
*   `app/(dashboard)/settings/page.tsx` -> `/settings`

## 4. Component Hierarchy
ASTRA utilizes a composition-based component hierarchy. Data fetching occurs as high up the tree as possible, passing data down to pure UI components.

1.  **Root Layout**: Injects global providers (Theme, Auth Context, Toast Toaster).
2.  **Route Layout**: The `(dashboard)/layout.tsx` maintains persistent state for the Navigation Sidebar and Top Header.
3.  **Page Components**: Default to React Server Components (RSC). Responsible for initial data fetching, SEO/metadata, and rendering `<Suspense>` boundaries.
4.  **Domain Components**: Client or Server components specific to a feature (e.g., `<CaseEvidenceTable />`, `<AlertQueue />`).
5.  **UI Components**: Pure presentation components (Buttons, Inputs, Cards), primarily built using `shadcn/ui` over Tailwind v4.

## 5. State Strategy
State management is segmented based on the data lifecycle to prevent unnecessary client-side bloat:

*   **URL State (Source of Truth for Navigation):** All pagination, filtering, search queries, and sorting parameters must be stored in the URL (e.g., `?page=2&severity=critical`). This ensures that complex Views, like the Observations Explorer, are deeply linkable and shareable among analysts.
*   **Server State (Data Fetching):** Handled natively by Next.js Server Components for initial loads. For client-side mutations (e.g., claiming a case, running an automation) and polling (e.g., refreshing the case queue), we will utilize Next.js Server Actions or a lightweight client fetcher hook.
*   **Client UI State:** Minimized. Used only for transient interactions (e.g., dropdowns, modal visibility, sidebar toggles) using standard React `useState`. Global UI state (like theme) will be managed via React Context.

## 6. API Client Strategy
The frontend communicates with the ASTRA FastAPI backend via a standardized, typed API client wrapper:

*   **Server-Side Fetching:** A custom `fetch` wrapper configured with standard headers (Auth) and base URLs. Leverages Next.js extended `fetch` for caching and revalidation logic.
*   **Authentication Injection:** JWT or Session tokens will be securely passed from Next.js Auth (or HTTP-only cookies) into the API headers for every request.
*   **Type Safety:** `types/` will closely mirror the backend OpenAPI schema to ensure full end-to-end type safety between FastAPI and React.

## 7. Error Handling Strategy
*   **API Level:** The API client intercepts standard HTTP errors (401 Unauthorized, 403 Forbidden, 500 Server Error) and standardizes the error payload.
*   **Application Level (Boundaries):** Next.js `error.tsx` files placed at critical route segments (e.g., `/cases/error.tsx`) to catch rendering and data-fetching failures without crashing the entire app.
*   **User Level:** User-facing validation errors and API mutation failures will trigger accessible Toast notifications (e.g., "Failed to block IP: Network timeout").

## 8. Performance Strategy
To handle the scale of security telemetry (e.g., thousands of observations):
*   **Streaming & Suspense:** Implement `loading.tsx` and `<Suspense>` boundaries. The page shell loads instantly, while slow data components (like historical case metrics) stream in progressively.
*   **Table Strategy:** Data tables will NEVER load full datasets. Tables will employ strictly controlled server-side pagination, sorting, and filtering.
*   **Pagination Strategy:** Cursor-based or standard offset pagination handled via the backend API. The frontend only stores the current page and limit in the URL search parameters.
*   **Bundle Optimization:** Strict adherence to Server Components by default. `'use client'` is only applied to leaf components that require interactivity (e.g., buttons, forms, charts).

## 9. MVP Build Order
To ensure a rapid and logical rollout, implementation will follow this sequence:

1.  **Sprint 1: Scaffold & Infrastructure**
    *   Initialize Next.js App Router, Tailwind v4, and base UI component library.
    *   Establish routing skeleton and persistent Dashboard layout (Sidebar).
    *   Implement API client wrapper and Auth routing (Login).
2.  **Sprint 2: Core Operational Views**
    *   Dashboard Page (Static layout and metrics cards).
    *   Cases List View (Table with Server-side Pagination).
    *   Case Detail View (Tabs, Timeline layout).
3.  **Sprint 3: Telemetry & Actions**
    *   Observations Explorer (Advanced filtering URL state, high-performance table).
    *   Case Actions (Client mutations for closing cases, triggering basic automations).
4.  **Sprint 4: Engineering Views**
    *   Alerts List.
    *   Policies List and basic Policy Editor View.
    *   Settings and user configuration.
