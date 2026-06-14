# ASTRA Sprint 3 Execution Order

This document defines the strict, dependency-mapped execution sequence for Sprint 3 tasks. Tasks must be executed in order from top to bottom.

## Execution Sequence Map

```mermaid
graph TD
    %% Phase 1
    T1[TASK-3001: User Schema] --> T2[TASK-3002: Auth Service]
    T2 --> T3[TASK-3003: RBAC Middleware]
    T3 --> T4[TASK-3004: User Management API]
    
    %% Phase 2
    T4 --> T5[TASK-3005: Correlation Domain Model]
    T5 --> T6[TASK-3006: Correlation Rule Engine]
    T6 --> T7[TASK-3007: Correlation Storage]
    T7 --> T8[TASK-3008: Correlation API]
    T8 --> T9[TASK-3009: Correlation Tests]
    
    %% Pre-req for Phase 3
    T9 --> TArch[TASK-S3-ARCH-001: Obs Domain Model Def]
    
    %% Phase 3
    TArch --> T10[TASK-3010: Observation Domain Model]
    T10 --> T11[TASK-3011: Observation Engine]
    T11 --> T12[TASK-3012: Risk Scoring]
    T12 --> T13[TASK-3013: Observation Storage]
    T13 --> T14[TASK-3014: Observation API]
    T14 --> T15[TASK-3015: Observation Tests]

    %% Phase 4
    T15 --> T16[TASK-3016: Policy Domain Model]
    T16 --> T17[TASK-3017: Policy Evaluation Logic]
    T17 --> T18[TASK-3018: Policy Storage]
    T18 --> T19[TASK-3019: Policy API]
    T19 --> T20[TASK-3020: Policy Tests]
    
    %% Phase 5
    T20 --> T21[TASK-3021: Frontend Project Setup]
    T21 --> T22[TASK-3022: Authentication Screens]
    T22 --> T23[TASK-3023: Frontend RBAC]
    T23 --> T24[TASK-3024: Dashboard]
    T23 --> T25[TASK-3025: Events Explorer]
    T23 --> T26[TASK-3026: Observations Screen]
    T26 --> T27[TASK-3027: Observation Detail Screen]
    T23 --> T28[TASK-3028: Users Screen]
    
    %% Phase 6
    T24 --> T29[TASK-3029: Integration Tests]
    T25 --> T29
    T27 --> T29
    T28 --> T29
    T29 --> T30[TASK-3030: E2E Tests]
    T30 --> T31[TASK-3031: Performance & Security Validation]
```

## Linear Execution Path

* **1.** `TASK-3001` User Schema
* **2.** `TASK-3002` Auth Service
* **3.** `TASK-3003` RBAC Middleware
* **4.** `TASK-3004` User Management API
* **5.** `TASK-3005` Correlation Domain Model
* **6.** `TASK-3006` Correlation Rule Engine
* **7.** `TASK-3007` Correlation Storage
* **8.** `TASK-3008` Correlation API
* **9.** `TASK-3009` Correlation Tests
* **10.** `TASK-S3-ARCH-001` Observation Domain Model Definition
* **11.** `TASK-3010` Observation Domain Model Implementation
* **12.** `TASK-3011` Observation Engine MVP
* **13.** `TASK-3012` Risk Scoring Module
* **14.** `TASK-3013` Observation Storage
* **15.** `TASK-3014` Observation API
* **16.** `TASK-3015` Observation Tests
* **17.** `TASK-3016` Policy Domain Model
* **18.** `TASK-3017` Policy Evaluation Logic
* **19.** `TASK-3018` Policy Storage
* **20.** `TASK-3019` Policy API
* **21.** `TASK-3020` Policy Tests
* **22.** `TASK-3021` Frontend Project Setup
* **23.** `TASK-3022` Authentication Screens
* **24.** `TASK-3023` Frontend RBAC
* **25.** `TASK-3024` Dashboard Screen
* **26.** `TASK-3025` Events Explorer
* **27.** `TASK-3026` Observations Screen
* **28.** `TASK-3027` Observation Detail Screen
* **29.** `TASK-3028` Users Screen
* **30.** `TASK-3029` Integration Tests
* **31.** `TASK-3030` E2E Tests
* **32.** `TASK-3031` Performance & Security Validation
