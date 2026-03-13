# Issue #623: Feedback System Gameplan

## Audit Summary

The feedback system is backend-focused but Issue #623 requires:
- "Feedback framed as Moment of connection"
- "Warm acknowledgment responses"
- "Passes experience test"

## Scope Decision

Create grammar infrastructure for feedback acknowledgments that:
1. Can be used when API responses are rendered to users
2. Can be called when conversation captures feedback
3. Follows established Response Context + Narrative Bridge pattern

## Implementation Plan

### Phase 1: Response Context (5 tests)
Create `services/feedback/response_context.py`:
- FeedbackResponseContext dataclass
- Captures: feedback_type, sentiment, is_first_feedback
- Factory from Feedback domain model

### Phase 2: Narrative Bridge (15 tests)
Create `services/feedback/narrative_bridge.py`:
- FeedbackNarrativeBridge class
- Type-aware acknowledgments (bug, feature, ux, general)
- Warm, connection-oriented language

### Phase 3: Helper Functions (8 tests)
Create `services/feedback/narrative_helpers.py`:
- acknowledge_feedback() - main acknowledgment
- narrate_feedback_type() - type explanation
- get_feedback_formality() - context-based formality

### Phase 4: Integration
Update `services/feedback/__init__.py` with exports

## Completion Matrix

| Phase | Component | Status |
|-------|-----------|--------|
| 1 | FeedbackResponseContext | Pending |
| 1 | Tests for context | Pending |
| 2 | FeedbackNarrativeBridge | Pending |
| 2 | Tests for bridge | Pending |
| 3 | narrative_helpers | Pending |
| 3 | Tests for helpers | Pending |
| 4 | __init__.py exports | Pending |

## Estimated Tests: ~28
