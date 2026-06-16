# ADR-014: Automation Engine Architecture

**Context:** A core strategy pivot demands that Automation is considered more important than pure Recommendation.
**Decision:** Implement an Automation Engine as a core platform component.
**Rationale:** Evolving the platform to "Detection -> Investigation -> Decision -> Automation" requires an engine that can natively execute the actions dictated by the Policy Engine.
**Status:** Accepted