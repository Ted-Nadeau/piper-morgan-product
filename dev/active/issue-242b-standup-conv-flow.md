# STANDUP-CONV-FLOW: Multi-Turn Conversation Flow

**Priority**: P0
**Labels**: `enhancement`, `component: ai`, `standup`
**Milestone**: MVP
**Epic**: #242 (CONV-MCP-STANDUP-INTERACTIVE)
**Related**: #242-A (dependency)

---

## Problem Statement

### Current State
With state management in place (#242-A), we need the conversation logic that drives multi-turn interactions. Currently, standup is single-turn: user requests → Piper generates → done.

### Impact
- **Blocks**: Interactive standup experience (core #242 value)
- **User Impact**: Cannot refine standup output or guide generation
- **Technical Debt**: No reusable multi-turn conversation patterns

### Strategic Context
This implements the actual conversation flow that transforms standup from generator to assistant. Builds directly on #242-A state foundation.

---

## Goal

**Primary Objective**: Implement multi-turn conversation logic that guides users through standup refinement.

**Example User Experience**:
```
User: "standup"
Piper: "Good morning! Ready for your standup? I see 3 commits yesterday
       on piper-morgan. Include documentation updates?"
User: "Just the feature work"
Piper: "Perfect! Here's your standup focusing on features:
       [generated standup]
       Any blockers I should mention?"
User: "Add waiting for chat infrastructure"
Piper: "Updated! [shows revised standup] Anything else?"
User: "Looks good"
Piper: "Great! Would you like me to share this or save preferences?"
```

**Not In Scope** (explicitly):
- ❌ Chat widget UI (see #242-C)
- ❌ Preference persistence across sessions (see #242-D)
- ❌ Performance optimization (see #242-E)
- ❌ State management infrastructure (done in #242-A)

---

## What Already Exists

### Infrastructure ✅ (from #242-A)
- `ConversationState` enum
- `StandupConversation` dataclass
- `StandupConversationManager` service
- Session-scoped state persistence

### Current Standup ✅
- `StandupGenerator` with 4 modes
- Integration with GitHub, calendar, etc.
- Multi-format output (CLI, API, Web, Slack)

### What's Missing ❌
- Turn handler that routes based on conversation state
- Context-aware follow-up question generation
- Refinement logic (modify generated standup based on feedback)
- Graceful fallback to static generation

---

## Requirements

### Phase 0: Investigation & Setup
- [ ] Review #242-A implementation (state management)
- [ ] Review existing intent handling patterns
- [ ] Identify integration points with StandupGenerator

### Phase 1: Turn Handler
**Objective**: Create conversation turn handler

**Tasks**:
- [ ] Create `StandupConversationHandler` in `services/standup/`
- [ ] Implement state-based routing
- [ ] Handle each conversation state appropriately

**Deliverables**:
- `handle_turn(conversation, user_message)` → response + state transition

### Phase 2: Follow-up Questions
**Objective**: Generate context-aware questions

**Tasks**:
- [ ] Implement preference gathering questions
- [ ] Implement refinement prompts
- [ ] Implement finalization options

**Deliverables**:
- Questions adapt based on available data (GitHub activity, calendar)
- Natural conversation flow

### Phase 3: Refinement Logic
**Objective**: Modify standup based on user feedback

**Tasks**:
- [ ] Parse refinement requests (add/remove/modify)
- [ ] Apply modifications to generated standup
- [ ] Maintain standup coherence

**Deliverables**:
- "Add blocker X" → blocker added
- "Remove the documentation items" → filtered out
- "Focus on project Y" → regenerate with filter

### Phase 4: Graceful Fallback
**Objective**: Fallback to static generation when needed

**Tasks**:
- [ ] Detect when conversation isn't progressing
- [ ] Implement timeout/fallback logic
- [ ] Preserve user experience on fallback

### Phase 5: Tests

**Tasks**:
- [ ] Unit tests for turn handling
- [ ] Integration tests for full conversation flows
- [ ] Fallback scenario tests

### Phase Z: Completion & Handoff
- [ ] All acceptance criteria met
- [ ] Evidence provided
- [ ] GitHub issue updated

---

## Acceptance Criteria

### Conversation Capability
- [ ] Multi-turn standup conversations functional
- [ ] Conversation state maintained across turns
- [ ] Context-aware follow-up questions working
- [ ] Graceful fallback to static generation (<5% of interactions)
- [ ] Response time <500ms per turn

### Refinement
- [ ] "Add blocker" requests handled
- [ ] "Focus on X" filtering works
- [ ] "Remove Y" modifications work

### Testing
- [ ] Unit tests for turn handler
- [ ] Integration tests for conversation flows
- [ ] Fallback tests

---

## Completion Matrix

| Component | Status | Evidence |
|-----------|--------|----------|
| `StandupConversationHandler` | ⏸️ | |
| State-based routing | ⏸️ | |
| Preference gathering | ⏸️ | |
| Refinement logic | ⏸️ | |
| Graceful fallback | ⏸️ | |
| Turn handler tests | ⏸️ | |
| Conversation flow tests | ⏸️ | |

---

## Testing Strategy

### Unit Tests
```python
# test_standup_conversation_handler.py
def test_handle_turn_initiated_state()
def test_handle_turn_gathering_preferences()
def test_refinement_add_blocker()
def test_refinement_filter_by_project()
def test_fallback_on_timeout()
```

### Integration Tests
```python
# test_standup_conversation_integration.py
async def test_full_conversation_flow()
async def test_conversation_with_refinements()
```

---

## STOP Conditions

Stop immediately and escalate if:
- [ ] #242-A state management not complete
- [ ] StandupGenerator API has changed
- [ ] Performance exceeds 500ms per turn
- [ ] Tests fail for any reason

---

## Effort Estimate

**Overall Size**: Medium (2-3 days)

**Breakdown**:
- Phase 0: Small
- Phase 1: Medium (turn handler)
- Phase 2: Small (follow-ups)
- Phase 3: Medium (refinement)
- Phase 4: Small (fallback)
- Phase 5: Small (tests)

---

## Dependencies

### Required
- [ ] #242-A (State Management) - MUST be complete

### Enables
- #242-C (Chat Widget) - can start after this
- #242-D (Learning) - can start after this

---

_Issue created: 2026-01-07_
