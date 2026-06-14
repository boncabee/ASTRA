# ASTRA Sprint 3 Task Backlog

## Pre-Requisite Architecture Task
### TASK-S3-ARCH-001: Observation Domain Model Definition
* **Title**: Define Observation Domain Model
* **Objective**: Establish the core architectural standards for Observations prior to engine implementation.
* **Deliverables**: Observation Status Enum, Risk Score Standard, Policy Action Enum, Audit Metadata Model.
* **Dependencies**: None
* **Acceptance Criteria**: Models are documented and approved by the lead architect.
* **Estimated Complexity**: Low
* **Risk Level**: Low

---

## Phase 1: Authentication & RBAC

### TASK-3001: User Schema
* **Title**: Implement User Database Schema
* **Objective**: Create the core database models required to store users, roles, and credentials.
* **Deliverables**: SQLAlchemy Models for Users and Roles, Alembic migrations.
* **Dependencies**: None
* **Acceptance Criteria**: Schema deployed to local DB, roles correctly mapped to the 4 ASTRA personas.
* **Estimated Complexity**: Low
* **Risk Level**: Low

### TASK-3002: Auth Service & JWT Authentication
* **Title**: Implement Authentication Service
* **Objective**: Provide secure login capabilities yielding JWTs.
* **Deliverables**: Login API endpoint, Password hashing utility, JWT generation and validation service.
* **Dependencies**: TASK-3001
* **Acceptance Criteria**: Valid credentials return a signed JWT; invalid credentials return 401.
* **Estimated Complexity**: Medium
* **Risk Level**: High (Security)

### TASK-3003: RBAC Middleware
* **Title**: Implement RBAC Middleware
* **Objective**: Intercept API requests and authorize them based on JWT role claims.
* **Deliverables**: FastAPI Dependency/Middleware for RBAC enforcement.
* **Dependencies**: TASK-3002
* **Acceptance Criteria**: SOC Analyst blocked from Admin routes; Responders can access Observation routes.
* **Estimated Complexity**: Medium
* **Risk Level**: High (Security)

### TASK-3004: User Management API
* **Title**: Implement User Management API
* **Objective**: Provide CRUD operations for Administrators to manage users.
* **Deliverables**: GET, POST, PUT, DELETE endpoints for users.
* **Dependencies**: TASK-3003
* **Acceptance Criteria**: Endpoints functional and strictly locked behind Administrator RBAC.
* **Estimated Complexity**: Low
* **Risk Level**: Medium

---

## Phase 2: Correlation Engine MVP

### TASK-3005: Correlation Domain Model
* **Title**: Implement Correlation Domain Model
* **Objective**: Define data structures representing incident candidates grouped from CES events.
* **Deliverables**: Pydantic models and SQLAlchemy schemas for Correlation entities.
* **Dependencies**: Sprint 1 CES Models
* **Acceptance Criteria**: Models successfully define relationships between multiple CES events.
* **Estimated Complexity**: Medium
* **Risk Level**: Low

### TASK-3006: Correlation Rule Engine
* **Title**: Implement Correlation Rule Engine MVP
* **Objective**: Process incoming CES events against static rules to group them.
* **Deliverables**: Static rule evaluator, grouping logic.
* **Dependencies**: TASK-3005
* **Acceptance Criteria**: Group of related CES events triggers the creation of a Correlation entity.
* **Estimated Complexity**: High
* **Risk Level**: Medium

### TASK-3007: Correlation Storage
* **Title**: Implement Correlation Storage Layer
* **Objective**: Persist generated Correlation entities to the database.
* **Deliverables**: Repository pattern implementation for Correlations.
* **Dependencies**: TASK-3006
* **Acceptance Criteria**: Engine can successfully save and retrieve Correlation objects.
* **Estimated Complexity**: Medium
* **Risk Level**: Low

### TASK-3008: Correlation API
* **Title**: Implement Correlation API
* **Objective**: Expose Correlation data to the frontend and internal services.
* **Deliverables**: REST endpoints to retrieve Correlation status.
* **Dependencies**: TASK-3007, TASK-3003
* **Acceptance Criteria**: Authorized users can query Correlations via API.
* **Estimated Complexity**: Low
* **Risk Level**: Low

### TASK-3009: Correlation Tests
* **Title**: Implement Correlation Test Suite
* **Objective**: Ensure absolute reliability of the Correlation grouping logic.
* **Deliverables**: Unit tests for the Rule Engine and Storage layer.
* **Dependencies**: TASK-3006, TASK-3007
* **Acceptance Criteria**: 90%+ test coverage on the Correlation Engine module.
* **Estimated Complexity**: Medium
* **Risk Level**: Low

---

## Phase 3: Observation Engine MVP

### TASK-3010: Observation Domain Model Implementation
* **Title**: Implement Observation Domain Model
* **Objective**: Translate TASK-S3-ARCH-001 into code.
* **Deliverables**: Pydantic and SQLAlchemy models for Observations.
* **Dependencies**: TASK-S3-ARCH-001, TASK-3005
* **Acceptance Criteria**: Schema correctly links to Correlations and tracks Status Enums.
* **Estimated Complexity**: Low
* **Risk Level**: Low

### TASK-3011: Observation Engine
* **Title**: Implement Observation Engine MVP
* **Objective**: Elevate Correlations into actionable Observations.
* **Deliverables**: Engine logic translating groups of events into a unified threat Observation.
* **Dependencies**: TASK-3008, TASK-3010
* **Acceptance Criteria**: Given a Correlation, the Engine outputs a well-formed Observation.
* **Estimated Complexity**: Medium
* **Risk Level**: Medium

### TASK-3012: Risk Scoring
* **Title**: Implement Risk Scoring Module
* **Objective**: Calculate an integer Risk Score for Observations.
* **Deliverables**: Risk calculation algorithm based on standard indicators.
* **Dependencies**: TASK-3011
* **Acceptance Criteria**: Observations are deterministically scored between 0-100.
* **Estimated Complexity**: High
* **Risk Level**: High (Logic Risk)

### TASK-3013: Observation Storage
* **Title**: Implement Observation Storage Layer
* **Objective**: Persist Observations and their assigned Risk Scores.
* **Deliverables**: Repository pattern for Observations.
* **Dependencies**: TASK-3012
* **Acceptance Criteria**: Risk Scores and Observations are successfully saved to the database.
* **Estimated Complexity**: Low
* **Risk Level**: Low

### TASK-3014: Observation API
* **Title**: Implement Observation API
* **Objective**: Provide CRUD endpoints for Observations.
* **Deliverables**: Endpoints to list, view, and update Observation statuses.
* **Dependencies**: TASK-3013, TASK-3003
* **Acceptance Criteria**: Authorized Responders can query and update Observations.
* **Estimated Complexity**: Low
* **Risk Level**: Low

### TASK-3015: Observation Tests
* **Title**: Implement Observation Test Suite
* **Objective**: Validate the engine and risk scoring algorithms.
* **Deliverables**: Unit and mock tests for the Observation layer.
* **Dependencies**: TASK-3011, TASK-3012
* **Acceptance Criteria**: 90%+ coverage ensuring Risk Scoring does not crash or yield invalid values.
* **Estimated Complexity**: Medium
* **Risk Level**: Low

---

## Phase 4: Policy Engine MVP

### TASK-3016: Policy Domain Model
* **Title**: Implement Policy Domain Model
* **Objective**: Define data structures for policy rules and evaluation outcomes.
* **Deliverables**: Policy schema including criteria and Recommended Action Enums.
* **Dependencies**: TASK-S3-ARCH-001
* **Acceptance Criteria**: Model supports "If Risk > X then Action = Y" structure.
* **Estimated Complexity**: Low
* **Risk Level**: Low

### TASK-3017: Policy Evaluation Logic
* **Title**: Implement Policy Evaluation Logic
* **Objective**: Process Observations against policies to determine next steps.
* **Deliverables**: Policy Evaluator function.
* **Dependencies**: TASK-3016, TASK-3014
* **Acceptance Criteria**: Evaluator correctly assigns actions like Observe, Notify, or Mitigate based on Risk Score.
* **Estimated Complexity**: High
* **Risk Level**: Medium

### TASK-3018: Policy Storage
* **Title**: Implement Policy Storage Layer
* **Objective**: Save configured policies and evaluation results.
* **Deliverables**: Database repository for policies.
* **Dependencies**: TASK-3016
* **Acceptance Criteria**: Policies can be persisted and loaded efficiently.
* **Estimated Complexity**: Low
* **Risk Level**: Low

### TASK-3019: Policy API
* **Title**: Implement Policy API
* **Objective**: Expose policies to the Security Engineer UI.
* **Deliverables**: CRUD REST endpoints for policy management.
* **Dependencies**: TASK-3018, TASK-3003
* **Acceptance Criteria**: Only Security Engineers and Administrators can modify policies.
* **Estimated Complexity**: Low
* **Risk Level**: Low

### TASK-3020: Policy Tests
* **Title**: Implement Policy Test Suite
* **Objective**: Ensure the logic does not yield incorrect actions.
* **Deliverables**: Unit tests covering edge cases in evaluation logic.
* **Dependencies**: TASK-3017
* **Acceptance Criteria**: Evaluator passes all permutations of static policies.
* **Estimated Complexity**: Medium
* **Risk Level**: Low

---

## Phase 5: Frontend MVP

### TASK-3021: Frontend Project Setup
* **Title**: Initialize Frontend Project
* **Objective**: Scaffold the SPA architecture.
* **Deliverables**: Base React/Vue project, router config, state management setup.
* **Dependencies**: None
* **Acceptance Criteria**: App builds and runs locally without errors.
* **Estimated Complexity**: Low
* **Risk Level**: Low

### TASK-3022: Authentication Screens
* **Title**: Implement Login Screen
* **Objective**: Allow users to authenticate against the backend.
* **Deliverables**: Login form, JWT storage mechanism.
* **Dependencies**: TASK-3021, TASK-3002
* **Acceptance Criteria**: User receives and stores token, redirecting to Dashboard.
* **Estimated Complexity**: Medium
* **Risk Level**: Low

### TASK-3023: Frontend RBAC
* **Title**: Implement Frontend RBAC
* **Objective**: Hide/Show UI elements based on user role.
* **Deliverables**: Router guards and conditional rendering wrappers.
* **Dependencies**: TASK-3022
* **Acceptance Criteria**: Unauthorized routes redirect to 403 pages; nav elements hide contextually.
* **Estimated Complexity**: Medium
* **Risk Level**: Medium

### TASK-3024: Dashboard
* **Title**: Implement Dashboard Screen
* **Objective**: Build the primary landing view displaying high-level metrics.
* **Deliverables**: Dashboard view with mock/real widgets.
* **Dependencies**: TASK-3022
* **Acceptance Criteria**: Screen loads cleanly without API errors.
* **Estimated Complexity**: Medium
* **Risk Level**: Low

### TASK-3025: Events Explorer
* **Title**: Implement Events Explorer Screen
* **Objective**: Build view for SOC Analysts to parse raw CES data.
* **Deliverables**: Data table with basic filtering/pagination.
* **Dependencies**: TASK-3023
* **Acceptance Criteria**: Displays CES events fetched from the backend.
* **Estimated Complexity**: High
* **Risk Level**: Low

### TASK-3026: Observations Screen
* **Title**: Implement Observations Screen
* **Objective**: List all active observations.
* **Deliverables**: List/Kanban view of Observations.
* **Dependencies**: TASK-3014, TASK-3023
* **Acceptance Criteria**: Displays real Observation data from API.
* **Estimated Complexity**: Medium
* **Risk Level**: Low

### TASK-3027: Observation Detail Screen
* **Title**: Implement Observation Detail Screen
* **Objective**: Deep-dive view of a single Observation, Risk Score, and Policy evaluation.
* **Deliverables**: Detailed view panel showing risk, recommended actions, and linked CES events.
* **Dependencies**: TASK-3026
* **Acceptance Criteria**: Displays full context of an Observation.
* **Estimated Complexity**: High
* **Risk Level**: High (UX Risk)

### TASK-3028: Users Screen
* **Title**: Implement Users Management Screen
* **Objective**: Administrator view to manage accounts.
* **Deliverables**: Data table for users, role assignment dropdowns.
* **Dependencies**: TASK-3004, TASK-3023
* **Acceptance Criteria**: Admins can view and change roles.
* **Estimated Complexity**: Medium
* **Risk Level**: Low

---

## Phase 6: Testing & Stabilization

### TASK-3029: Integration Tests
* **Title**: Finalize Integration Tests
* **Objective**: Ensure all APIs and Engines work together.
* **Deliverables**: Expanded test suite hitting the actual router endpoints.
* **Dependencies**: Phases 1-4 completed.
* **Acceptance Criteria**: 85%+ overall backend coverage.
* **Estimated Complexity**: Medium
* **Risk Level**: Low

### TASK-3030: E2E Tests
* **Title**: Implement End-to-End Tests
* **Objective**: Validate the full Telemetry → UI flow.
* **Deliverables**: Browser automation tests for core workflows.
* **Dependencies**: Phase 5 completed.
* **Acceptance Criteria**: Test scripts successfully inject an event and verify its appearance as an Observation in the UI.
* **Estimated Complexity**: High
* **Risk Level**: Medium

### TASK-3031: Performance & Security Validation
* **Title**: Execute Performance and Security Validation
* **Objective**: Ensure no OOM crashes and confirm RBAC integrity.
* **Deliverables**: Load testing results and vulnerability scan results.
* **Dependencies**: TASK-3030
* **Acceptance Criteria**: Platform sustains target ingestion rates; zero critical security flaws.
* **Estimated Complexity**: Medium
* **Risk Level**: Low
