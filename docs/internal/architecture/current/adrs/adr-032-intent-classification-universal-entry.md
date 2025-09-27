# ADR-032: Intent Classification as Universal Entry Point

## Status
Accepted

## Context
Currently, users must learn specific commands and syntax to interact with Piper Morgan effectively. The May 28 vision proposed natural language as the primary interface, with intent classification routing all interactions. Recent advances in LLM capabilities make this vision more achievable now than at conception.

## Decision
We will implement intent classification as the universal entry point for all Piper Morgan interactions. Every user input, regardless of source (CLI, web, Slack), will first pass through intent classification before routing to appropriate handlers.

### Classification Layer Architecture
```
User Input → Intent Classifier → Router → Handler → Response
                     ↓
              Learning System
```

### Core Intent Types
- CREATE_ISSUE: User wants to create work items
- REVIEW_ISSUE: User wants to check/update status
- QUERY_KNOWLEDGE: User asking questions
- ANALYZE_DATA: User requesting analysis
- CLARIFY: User needs multi-turn conversation
- CHAT: General conversation

## Consequences

### Positive
- **Natural interaction**: No command memorization required
- **Universal interface**: Works identically across all entry points
- **Learning opportunity**: Every interaction improves classification
- **Progressive enhancement**: Can start simple, evolve to sophisticated
- **Reduced cognitive load**: Users think in intentions, not commands

### Negative
- **Initial accuracy issues**: Early classification will have errors
- **Latency addition**: Extra processing step for all interactions
- **Ambiguity handling**: Some inputs have multiple valid interpretations
- **Training data requirement**: Needs accumulated interactions to improve

### Neutral
- **Development complexity**: Adds abstraction layer to all interactions
- **Testing requirements**: Need comprehensive intent test coverage

## Implementation

### Phase 1: Basic Classifier (Week 1)
- Keyword-based classification
- Logging for training data
- Integration with existing router

### Phase 2: LLM Enhancement (Week 2)
- Use Claude for classification
- Fallback to keyword approach
- A/B testing for accuracy

### Phase 3: Learning Integration (Week 3)
- Store classifications with outcomes
- Build training dataset
- Implement feedback loop

## Code Location
- Implementation: `services/queries/intent_classifier.py`
- Tests: `tests/services/queries/test_intent_classifier.py`
- Integration: `services/queries/router.py` (modify existing)

## References
- Original vision: May 28, 2025
- Pattern-028: Intent Classification
- Issue #96: FEAT-INTENT
- Related: ADR-031 (MVP Redefinition)
