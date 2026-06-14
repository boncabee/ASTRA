# Architecture Realignment Report

This document introduces the new components introduced as part of the architecture realignment.

## New Core Components

1. **Observation Engine**: Replaces simplistic correlation -> alert models by generating rich observations.
2. **Policy Engine**: Determines actions based on observations, evidence, confidence, risk, and policy.
3. **Automation Engine**: Executes actions defined by the Policy Engine (Automation > Recommendation).
4. **AI Gateway**: Centralized management for AI provider interactions.
5. **AI Provider Abstraction Layer**: Ensures ASTRA has no core runtime dependency on any single AI provider (OpenAI, Gemini, Claude, Ollama), allowing the platform to remain functional if AI is unavailable.

## Paradigm Shift

From:
Detection -> Recommendation only

To:
Detection -> Investigation -> Decision -> Automation