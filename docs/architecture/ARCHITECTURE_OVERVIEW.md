# Architecture Overview

## Design Philosophy
ASTRA uses a Domain-Driven Design (DDD) modular monolith architecture. The core principle is deterministic execution: identical inputs must always produce identical outputs, creating an auditable and mathematically verifiable security posture.

## Core Domains

1. **Ingestion & Parsing:** Receives disparate security telemetry and normalizes it into a Common Event Schema (CES).
2. **Observation Engine:** Correlates CES events based on entity attributes and timing to determine if a threshold is crossed, triggering an Observation.
3. **Policy Engine:** Evaluates Observations against user-defined, deterministic logic to decide if an action is warranted.
4. **Evidence Linker:** Cryptographically chains the Policy Decision back to the original Observation and CES Events, ensuring immutability.
5. **Automation Engine:** Queues actions prescribed by the Policy Engine for reliable background execution.
6. **Case Management:** Provides structured orchestration for human-in-the-loop review of escalated Observations and automated actions.

## Data Flow
The data flow is strictly unidirectional:
`Event -> Parser -> Observation -> Policy -> Decision -> Automation -> Action`

## Database Architecture
ASTRA uses PostgreSQL as the canonical source of truth. All domains map to strictly typed SQLAlchemy ORM models. The database relies on strong constraints, foreign keys, and unique indexes to guarantee data integrity at the lowest level.
