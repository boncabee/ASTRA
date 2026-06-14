# Architecture Decision Records

## ADR-001 Project Architecture Style
**Context:** ASTRA is an AI-powered security investigation platform currently in its MVP phase. The system requires simple deployment and minimal operational overhead.
**Decision:** Monolithic Modular Architecture
**Rationale:** Suitable for MVP complexity. Reduces operational overhead. Simplifies deployment.
**Consequences:** 
- **Positive:** Faster development, lower infrastructure cost.
- **Negative:** Future service extraction may be required as the application scales.
**Reference:** ARCHITECTURE.md, PROJECT_PLAN.md
**Status:** Accepted

---

## ADR-002 Backend Framework
**Context:** The API layer needs to handle asynchronous operations such as file uploads and background AI processing.
**Decision:** FastAPI
**Rationale:** 
- Async support
- Type-safe APIs
- Strong OpenAPI generation
**Consequences:**
- **Positive:** High performance, automatic API documentation, robust validation natively integrated with Pydantic.
- **Negative:** Requires strong adherence to Python type hinting ecosystem.
**Reference:** TECH_STACK.md, API_SPEC.md
**Status:** Accepted

---

## ADR-003 Frontend Framework
**Context:** A responsive and maintainable user interface is required for log upload and timeline visualization.
**Decision:** React + TypeScript (via Next.js)
**Rationale:** Provides a robust component-based architecture with strong typing. Next.js offers optimized performance and routing out of the box.
**Consequences:**
- **Positive:** Rich ecosystem, high developer productivity, strict type safety.
- **Negative:** Learning curve associated with Next.js app router paradigm.
**Reference:** TECH_STACK.md, ARCHITECTURE.md
**Status:** Accepted

---

## ADR-004 Database
**Context:** The persistence layer needs to reliably store incidents, timelines, extracted IOCs, and MITRE mappings.
**Decision:** PostgreSQL
**Rationale:** Strong relational integrity, JSONB support for flexible event schemas, and future compatibility with `pgvector` for AI embeddings.
**Consequences:**
- **Positive:** Proven reliability, highly flexible schemas for structured and semi-structured data.
- **Negative:** Requires strict database migration management (Alembic).
**Reference:** TECH_STACK.md, DATABASE_SCHEMA.md
**Status:** Accepted

---

## ADR-005 AI Provider
**Context:** ASTRA relies on a Large Language Model for timeline generation, narrative creation, and IOC extraction without modifying source data.
**Decision:** Google Gemini API
**Rationale:** Strong reasoning capabilities, high performance, and ability to handle large context windows necessary for analyzing security logs.
**Consequences:**
- **Positive:** Accelerated incident timeline generation, consistent correlation performance.
- **Negative:** Vendor dependency on Google Cloud / Gemini APIs.
**Reference:** TECH_STACK.md, PROMPT_ENGINEERING.md
**Status:** Accepted

---

## ADR-006 Event Processing Standard
**Context:** ASTRA must ingest heterogeneous security logs (Windows, Firewall, etc.) and analyze them uniformly.
**Decision:** Common Event Schema (CES)
**Rationale:** Normalizes all log sources into a vendor-independent event model, dramatically improving correlation quality.
**Consequences:**
- **Positive:** Unified pipeline logic, decoupled parser development from the core correlation engine.
- **Negative:** All parsers must strictly adhere to and maintain the CES schema.
**Reference:** COMMON_EVENT_SCHEMA.md, PRD.md
**Status:** Accepted

---

## ADR-007 Investigation Methodology
**Context:** AI reasoning must be consistent, explainable, and aligned with standard security operations.
**Decision:** Playbook Driven Investigation
**Rationale:** Standardizes investigations and guides the AI's reasoning, ensuring repeatable and explainable outputs.
**Consequences:**
- **Positive:** Higher analyst trust, consistent and traceable investigation results.
- **Negative:** Requires active maintenance and updates to investigation playbooks.
**Reference:** INVESTIGATION_PLAYBOOK.md, ARCHITECTURE.md
**Status:** Accepted

---

## ADR-008 Attack Reasoning Model
**Context:** Findings must be rooted in recognized attacker behaviors and tactics.
**Decision:** Attack Knowledge Model (AKM)
**Rationale:** Accurately represents attacker behaviors, maps directly to MITRE ATT&CK, and supports attack chain reconstruction with confidence scoring.
**Consequences:**
- **Positive:** Standardized security taxonomy, absolute traceability to established frameworks.
- **Negative:** Ongoing overhead in maintaining and expanding the attack knowledge graph.
**Reference:** ATTACK_KNOWLEDGE_MODEL.md
**Status:** Accepted

---

## ADR-009 API Design Style
**Context:** The frontend and external services require a standard, predictable way to interact with the ASTRA backend.
**Decision:** REST API
**Rationale:** Industry standard protocol, natively well-supported by FastAPI, and easily consumable by the Next.js frontend ecosystem.
**Consequences:**
- **Positive:** Simple integration, utilization of standard HTTP methods and status codes.
- **Negative:** Less flexible data fetching capabilities compared to GraphQL.
**Reference:** API_SPEC.md, DEVELOPMENT_GUIDELINES.md
**Status:** Accepted

---

## ADR-010 Authentication Strategy
**Context:** ASTRA handles sensitive security incident data and requires secure user authentication.
**Decision:** OIDC/OAuth2 Compatible Architecture
**Rationale:** Industry standard for delegated authorization. Provides secure, token-based authentication without handling passwords directly.
**Consequences:**
- **Positive:** Enhanced security posture, ability to integrate seamlessly with enterprise Identity Providers (IdP).
- **Negative:** Increased initial integration complexity.
**Reference:** SECURITY.md
**Status:** Accepted

---

## ADR-011 Secrets Management
**Context:** Hardcoded credentials present a critical security vulnerability and violate project principles.
**Decision:** Environment Variables Only
**Rationale:** Ensures secrets are isolated from the source code and configuration files.
**Forbidden:**
- Hardcoded credentials
- Hardcoded API keys
**Consequences:**
- **Positive:** Eliminates credential leakage in version control, strictly complies with security protocols.
- **Negative:** Requires secure environment injection mechanisms during deployment.
**Reference:** SECURITY.md, DEPLOYMENT.md
**Status:** Accepted

---

## ADR-012 Deployment Strategy
**Context:** The application needs to run consistently across local, staging, and production environments.
**Decision:** Docker-Based Deployment
**Rationale:** Containerization guarantees environment parity, simplifies CI/CD pipelines, and natively supports Cloud Run hosting.
**Consequences:**
- **Positive:** Highly portable artifacts, easily scalable via modern container orchestrators.
- **Negative:** Requires maintenance of the Docker toolchain and container registries.
**Reference:** DEPLOYMENT.md, TECH_STACK.md
**Status:** Accepted

---

## ADR-013 Testing Strategy
**Context:** ASTRA must prove correctness, reliability, and security without incurring excessive manual regression overhead.
**Decision:** Test Pyramid
**Rationale:** Balances fast feedback cycles with end-to-end workflow confidence.
- Unit Tests (70%)
- Integration Tests (20%)
- E2E Tests (10%)
**Consequences:**
- **Positive:** High confidence in code changes, actively prevents regressions.
- **Negative:** Continual development overhead to write and maintain extensive test suites.
**Reference:** TESTING_STRATEGY.md
**Status:** Accepted

---

## ADR-014 Quality Enforcement
**Context:** The platform must not release code that degrades the quality, security, or traceability of investigations.
**Decision:** Mandatory Quality Gates
**Rationale:** Strictly enforces testing, security scanning, and audit requirements before merging or deploying. Failed Gate = Blocked Release.
**Consequences:**
- **Positive:** Prevents low-quality releases and guarantees continuous audit compliance.
- **Negative:** May temporarily impede development velocity if test pipelines are flaky.
**Reference:** QUALITY_GATE.md, AUDIT.md
**Status:** Accepted

---

## ADR-015 Self Improvement Strategy
**Context:** The AI platform needs a systemic mechanism to detect its own weaknesses and optimize its accuracy over time.
**Decision:** Audit-Driven Continuous Improvement
**Rationale:** Automatically generates findings from audits and testing to create actionable improvement opportunities.
**Consequences:**
- **Positive:** Continuous optimization of prompts, knowledge mappings, and playbooks.
- **Negative:** Generates an ongoing stream of technical tasks that require human triage.
**Reference:** SELF_IMPROVEMENT_POLICY.md
**Status:** Accepted

---


---

## ADR-016 Product Delivery Model
**Context:** The platform deployment strategy must be defined.
**Decision:** Self-Hosted Web Application (Primary), SaaS Edition (Future).
**Rationale:** Keeps the architecture cloud-agnostic.
**Status:** Accepted

---

## ADR-017 Authentication & RBAC
**Context:** Multi-persona support required.
**Decision:** Implement robust RBAC supporting Incident Responder, SOC Analyst, Security Engineer, and Administrator.
**Status:** Accepted

---

## ADR-018 AI Provider Abstraction Layer
**Context:** The platform must not have a core runtime dependency on any single AI provider.
**Decision:** Implement an AI Gateway and Provider Abstraction Layer.
**Rationale:** Core platform remains functional if AI providers are unavailable.
**Status:** Accepted

---

## ADR-019 Observation & Policy Architecture
**Context:** Simplistic Correlation -> Alert models are insufficient.
**Decision:** Adopt Correlation -> Observation -> Risk Scoring -> Policy Evaluation -> Action.
**Rationale:** Provides evidence-based and policy-driven security decisions.
**Status:** Accepted

---

## ADR-020 Automation Engine Architecture
**Context:** Automation is a higher priority than mere recommendation.
**Decision:** Build an Automation Engine to execute actions from the Policy Engine.
**Status:** Accepted
\n# Architecture Freeze Summary

**Accepted Decisions:**
- ADR-001 through ADR-015 are officially approved and frozen for the MVP lifecycle. All implementation agents must adhere to these directives.

**Deferred Decisions:**
- Real-time response actions and active SOAR capabilities (Explicitly defined as Out of Scope for MVP).
- Adoption of `pgvector` for advanced AI embeddings (Deferred to future iterations).

**Open Decisions:**
- Specific Enterprise Identity Provider (IdP) integration standards for OIDC implementation.

**Risks:**
- High operational dependency on Google Gemini API uptime and latency.
- Maintaining the strict 70% test coverage requirement as prompt engineering iterates rapidly.

**Future Revisit Candidates:**
- Transition from a Monolithic Modular Architecture to Microservices if scalability bottlenecks arise.
- Migration to specialized graph databases (e.g., Neo4j) if Attack Knowledge Model (AKM) complexity outgrows PostgreSQL capabilities.
