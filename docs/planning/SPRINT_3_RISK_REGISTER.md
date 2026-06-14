# ASTRA Sprint 3 Risk Register

## Technical Risks
* **Risk**: Complexity of rule evaluation logic in the Correlation Engine MVP.
* **Impact**: Delayed feature delivery or engine bugs.
* **Mitigation**: Start with simple static rules for the MVP; defer the complex dynamic rule engine to Sprint 4.

## Architecture Risks
* **Risk**: Database contention between continuous ingestion (CES) and frequent polling (Frontend APIs/Correlation Engine).
* **Impact**: UI latency and slow correlation times.
* **Mitigation**: Implement strict separation of read/write patterns; utilize appropriate indexing on CES and Observation tables.

## Performance Risks
* **Risk**: High memory footprint when processing large event batches for correlation.
* **Impact**: Out Of Memory (OOM) crashes on backend containers.
* **Mitigation**: Implement pagination, batch chunking, and hard limits on the number of events processed in a single correlation loop.

## Security Risks
* **Risk**: RBAC vulnerabilities allowing Privilege Escalation (e.g., SOC Analyst gaining Administrator rights).
* **Impact**: Total compromise of system integrity.
* **Mitigation**: Implement rigorous unit testing for the RBAC middleware covering all endpoint/role combinations. Ensure default-deny logic on all routes.

## UX Risks
* **Risk**: Overwhelming the Incident Responder with raw event data on the Observation Detail screen.
* **Impact**: User fatigue and decreased response efficiency.
* **Mitigation**: Implement progressive disclosure; show a high-level observation summary initially and require user interaction to view raw CES events.

## Integration Risks
* **Risk**: Misalignment between Frontend API calls and Backend Route definitions.
* **Impact**: Broken UI screens and integration delays during Phase 5.
* **Mitigation**: Adopt a contract-first API development approach using OpenAPI/Swagger documentation before frontend development begins.
