# ADR-012: AI Provider Abstraction Layer

**Context:** ASTRA heavily leverages AI to assist in investigation. However, tying the platform to a single provider (e.g. OpenAI, Gemini) creates an unacceptable runtime dependency risk.
**Decision:** Implement an AI Gateway and AI Provider Abstraction Layer.
**Rationale:** Platform strategy dictates ASTRA is "AI Enhanced", NOT "AI Dependent". The core system must remain fully functional if AI services are unavailable.
**Status:** Accepted