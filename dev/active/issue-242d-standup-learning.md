# STANDUP-LEARNING: User Preference Learning

**Priority**: P1
**Labels**: `enhancement`, `component: ai`, `standup`
**Milestone**: MVP
**Epic**: #242 (CONV-MCP-STANDUP-INTERACTIVE)
**Related**: #242-A (dependency), #242-B (dependency)

---

## Problem Statement

### Current State
Each standup conversation starts fresh. User preferences expressed in one session ("focus on GitHub work", "skip documentation updates") are lost and must be re-stated.

### Impact
- **Blocks**: "Piper learns about me" experience
- **User Impact**: Repetitive preference expression, not feeling "understood"
- **Technical Debt**: No foundation for personalization

### Strategic Context
This transforms standup from functional tool to personalized assistant. Key differentiator for user experience quality.

---

## Goal

**Primary Objective**: Learn and apply user preferences from standup conversations automatically.

**Example User Experience**:
```
Session 1:
User: "Focus on GitHub, skip docs"
Piper: [applies filter, remembers preference]

Session 2:
Piper: "Good morning! I'll focus on your GitHub work as usual.
       Any changes today?"
User: "Same as always"
Piper: [generates standup with learned preferences applied]
```

**Not In Scope** (explicitly):
- ❌ State management (done in #242-A)
- ❌ Conversation flow (done in #242-B)
- ❌ Chat widget (done in #242-C)
- ❌ ML-based preference prediction (future enhancement)

---

## What Already Exists

### Infrastructure ✅
- User model with preferences field (verify)
- `data/learning/` directory for patterns
- Session context preservation

### What's Missing ❌
- Preference extraction from conversation
- Preference storage per user
- Preference application in standup generation
- Preference feedback loop (user corrections)

---

## Requirements

### Phase 0: Investigation & Setup
- [ ] Review User model for preference storage
- [ ] Review existing learning patterns in `data/learning/`
- [ ] Identify preference categories (content filters, format, timing)

### Phase 1: Preference Extraction
**Objective**: Extract preferences from conversation turns

**Tasks**:
- [ ] Create preference extraction logic
- [ ] Define preference schema
- [ ] Handle implicit vs explicit preferences

**Deliverables**:
- Extract "focus on X" → content filter preference
- Extract "skip Y" → exclusion preference
- Extract "shorter/longer" → format preference

### Phase 2: Preference Storage
**Objective**: Persist preferences per user

**Tasks**:
- [ ] Add preference storage to user context
- [ ] Implement preference versioning (track changes)
- [ ] Handle preference conflicts/updates

**Deliverables**:
- Preferences persist across sessions
- History of preference changes available
- Graceful handling of conflicting preferences

### Phase 3: Preference Application
**Objective**: Apply learned preferences automatically

**Tasks**:
- [ ] Integrate preferences into standup generation
- [ ] Show user what preferences are being applied
- [ ] Allow override for single session

**Deliverables**:
- "Using your preferences: GitHub focus, skip docs"
- "Any changes for today?" prompt
- One-time overrides don't change stored preferences

### Phase 4: Feedback Loop
**Objective**: Learn from corrections

**Tasks**:
- [ ] Detect when user corrects applied preference
- [ ] Update stored preference on correction
- [ ] Confidence scoring for preferences

**Deliverables**:
- User says "actually include docs today" → temporary override
- User says "always include docs now" → preference update
- Preferences with low confidence prompt for confirmation

### Phase 5: Tests

**Tasks**:
- [ ] Unit tests for preference extraction
- [ ] Unit tests for preference application
- [ ] Integration tests for learning loop

### Phase Z: Completion & Handoff
- [ ] All acceptance criteria met
- [ ] Evidence provided
- [ ] GitHub issue updated

---

## Acceptance Criteria

### Learning & Adaptation
- [ ] User preferences learned and applied automatically
- [ ] Preference learning accuracy >70%
- [ ] Conversation patterns optimize based on user behavior
- [ ] Personalization visible to users
- [ ] Feedback loop functional (user corrections → learning)

### Testing
- [ ] Unit tests for preference extraction
- [ ] Unit tests for preference application
- [ ] Learning accuracy measurable

---

## Completion Matrix

| Component | Status | Evidence |
|-----------|--------|----------|
| Preference extraction | ⏸️ | |
| Preference schema | ⏸️ | |
| Preference storage | ⏸️ | |
| Preference application | ⏸️ | |
| Feedback loop | ⏸️ | |
| Tests | ⏸️ | |

---

## Testing Strategy

### Unit Tests
```python
# test_standup_preference_learning.py
def test_extract_focus_preference()
def test_extract_exclusion_preference()
def test_apply_preferences_to_generation()
def test_correction_updates_preference()
def test_temporary_override_preserves_stored()
```

---

## Success Metrics

- Preference learning accuracy >70%
- User satisfaction with personalization >85%
- Reduced preference re-statement across sessions

---

## STOP Conditions

Stop immediately and escalate if:
- [ ] User model doesn't support preference storage
- [ ] #242-A or #242-B not complete
- [ ] Preference extraction accuracy <50%
- [ ] Tests fail for any reason

---

## Effort Estimate

**Overall Size**: Medium (2-3 days)

**Breakdown**:
- Phase 0: Small
- Phase 1: Medium (extraction)
- Phase 2: Small (storage)
- Phase 3: Medium (application)
- Phase 4: Small (feedback)
- Phase 5: Small (tests)

---

## Dependencies

### Required
- [ ] #242-A (State Management) - conversation context
- [ ] #242-B (Conversation Flow) - preference expressions happen in conversation

### Can Parallelize With
- #242-C (Chat Widget) - independent backend vs frontend work

---

_Issue created: 2026-01-07_
