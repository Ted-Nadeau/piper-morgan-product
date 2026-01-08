# STANDUP-CONV-STATE: Conversation State Management

**Priority**: P0
**Labels**: `enhancement`, `component: ai`, `standup`
**Milestone**: MVP
**Epic**: #242 (CONV-MCP-STANDUP-INTERACTIVE)
**Related**: #160 (merged), #178 (merged)

---

## Problem Statement

### Current State
Standup generation is currently stateless - each `/standup` command generates a complete standup without any conversation context. Users cannot refine, adjust, or iterate on the output.

### Impact
- **Blocks**: Interactive standup refinement (#242 parent epic)
- **User Impact**: Users must accept generated standup as-is or start over entirely
- **Technical Debt**: No foundation for multi-turn AI interactions in standup domain

### Strategic Context
This is the foundational building block for interactive standup. All other #242 children depend on this state management infrastructure.

---

## Goal

**Primary Objective**: Implement conversation state management infrastructure that tracks standup conversations across multiple turns.

**Example User Experience**:
```
Turn 1: User says "standup" → State: INITIATED
Turn 2: Piper asks "Focus on GitHub work?" → State: GATHERING_PREFERENCES
Turn 3: User says "Yes" → State: GENERATING
Turn 4: Piper shows standup → State: REFINING (awaiting feedback)
Turn 5: User says "Add a blocker" → State: REFINING
Turn 6: Piper shows updated → State: FINALIZING
```

**Not In Scope** (explicitly):
- ❌ Chat widget UI integration (see #554)
- ❌ User preference learning/persistence (see #555)
- ❌ Performance optimization (see #556)
- ❌ Multi-turn conversation flow logic (see #553)

---

## What Already Exists

### Infrastructure ✅
- `services/session/session_manager.py` - Basic session management
- `services/domain/models.py` - Domain model patterns
- `services/shared_types.py` - Enum patterns
- `services/standup/standup_generator.py` - Static standup generation

### What's Missing ❌
- `StandupConversation` dataclass for tracking conversation state
- `ConversationState` enum for state machine
- `StandupConversationManager` service for state transitions
- State persistence (session-scoped initially)

---

## Requirements

### Phase 0: Investigation & Setup
- [ ] Verify SessionManager API and patterns
- [ ] Review existing conversation state patterns (if any)
- [ ] Confirm domain model conventions

### Phase 1: Domain Models
**Objective**: Create conversation state domain models

**Tasks**:
- [ ] Add `ConversationState` enum to `services/shared_types.py`
- [ ] Create `StandupConversation` dataclass in domain models
- [ ] Create `ConversationTurn` dataclass for history tracking

**Deliverables**:
- Enum with states: INITIATED, GATHERING_PREFERENCES, GENERATING, REFINING, FINALIZING, COMPLETE
- Dataclass with: session_id, user_id, state, context, preferences, history

### Phase 2: State Management Service
**Objective**: Create service for managing conversation state

**Tasks**:
- [ ] Create `StandupConversationManager` in `services/standup/`
- [ ] Implement state transition methods
- [ ] Implement session-scoped persistence
- [ ] Add validation for state transitions

**Deliverables**:
- `create_conversation()` - Initialize new standup conversation
- `get_conversation()` - Retrieve by session_id
- `transition_state()` - Move between states with validation
- `add_turn()` - Record conversation turn

### Phase 3: Tests
**Objective**: Comprehensive test coverage

**Tasks**:
- [ ] Unit tests for state transitions
- [ ] Unit tests for conversation lifecycle
- [ ] Edge case tests (invalid transitions, missing data)

### Phase Z: Completion & Handoff
- [ ] All acceptance criteria met
- [ ] Evidence provided for each criterion
- [ ] Documentation updated
- [ ] GitHub issue fully updated

---

## Acceptance Criteria

### Functionality
- [ ] `ConversationState` enum exists with 6 states
- [ ] `StandupConversation` dataclass tracks all required fields
- [ ] State transitions validate allowed paths
- [ ] Conversation history preserved across turns
- [ ] Session-scoped persistence working

### Testing
- [ ] Unit tests for all state transitions
- [ ] Unit tests for conversation lifecycle
- [ ] Edge cases covered (invalid transitions)

### Quality
- [ ] No regressions in existing standup functionality
- [ ] Follows existing domain model patterns
- [ ] Type hints complete

---

## Completion Matrix

| Component | Status | Evidence |
|-----------|--------|----------|
| `ConversationState` enum | ⏸️ | |
| `StandupConversation` dataclass | ⏸️ | |
| `ConversationTurn` dataclass | ⏸️ | |
| `StandupConversationManager` | ⏸️ | |
| State transition tests | ⏸️ | |
| Lifecycle tests | ⏸️ | |

---

## Testing Strategy

### Unit Tests
```python
# test_standup_conversation_state.py
def test_state_transition_initiated_to_gathering()
def test_state_transition_invalid_raises_error()
def test_conversation_history_preserved()
def test_conversation_lifecycle_complete()
```

---

## Success Metrics

- State transition validation: 100% of invalid transitions rejected
- Test coverage: >90% for new code
- No regressions in existing `/standup` functionality
- All 6 conversation states reachable and testable

---

## STOP Conditions

Stop immediately and escalate if:
- [ ] SessionManager API has changed significantly
- [ ] Existing conversation patterns conflict with design
- [ ] Domain model conventions unclear
- [ ] Tests fail for any reason

---

## Effort Estimate

**Overall Size**: Medium (1-2 days)

**Breakdown**:
- Phase 0: Small (investigation)
- Phase 1: Small (domain models)
- Phase 2: Medium (service implementation)
- Phase 3: Small (tests)

---

## Dependencies

### Required
- [ ] SessionManager operational
- [ ] Domain model patterns understood

### Enables
- #553 (Conversation Flow) - depends on this
- #554 (Chat Widget) - depends on this
- #555 (Learning) - depends on this

---

## Related Documentation

- **Architecture**: ADR for conversation state (if exists)
- **Patterns**: Domain model patterns in `docs/internal/architecture/`

---

## Completion Checklist

Before requesting PM review:
- [ ] All acceptance criteria met ✅
- [ ] Completion matrix 100% ✅
- [ ] Evidence provided for each criterion ✅
- [ ] Tests passing with output ✅
- [ ] No regressions confirmed ✅
- [ ] STOP conditions all clear ✅

**Status**: Not Started

---

_Issue created: 2026-01-07_
