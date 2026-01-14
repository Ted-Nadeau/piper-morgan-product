# FTUX-PORTFOLIO: Project Portfolio Onboarding - Multi-Layer User Project Setup

**Priority**: P0 (Alpha Critical for Layer 2)
**Labels**: `epic`, `ftux`, `alpha-critical`
**Milestone**: MVP
**Epic**: Yes (parent of child issues)
**Related**: #488 (Discovery Architecture), #487 (Intent Classification), #402 (MUX-INTERACT parent)

---

## Problem Statement

### Current State
- PIPER.user.md can store project info, but users must manually edit it
- Piper asks "Would you like me to help you set up your project portfolio?" but **no workflow fulfills this promise**
- Messages like "Would you like me to help..." appear in canonical_handlers.py 3+ times but lead nowhere
- No onboarding flow captures user's work context
- No learning mechanism detects project changes over time

### Impact
- **Blocks**: Personalized recommendations, priority guidance, standup context
- **User Impact**: Alpha testers don't understand what Piper can help with; generic responses feel hollow
- **Technical Debt**: Dead-end prompts create trust erosion

### Strategic Context
This is P0 for Alpha because first impressions matter. When users first interact with Piper and have no projects, we need a smooth conversational flow (like standup) to onboard them - not redirect them to a settings page.

---

## Goal

**Primary Objective**: When a user with no projects says "Hi Piper", Piper proactively guides them through project setup via natural conversation.

**Example User Experience**:
```
User: "Hi Piper"
Piper: "Hello! I'm Piper Morgan, your PM assistant. I notice we haven't
       set up your project portfolio yet. Would you like to tell me about
       the projects you're working on?"

User: "Sure"
Piper: "Great! What's the main project you're focused on right now?"

User: "I'm building a mobile app called HealthTrack"
Piper: "Got it - HealthTrack, a mobile app. What's the primary goal
       of this project?"

User: "It's a fitness tracking app for personal trainers"
Piper: "Perfect. Are there any other projects you'd like me to know about,
       or is HealthTrack your main focus?"

User: "That's the main one for now"
Piper: "All set! I've added HealthTrack to your portfolio. I'll help you
       stay on track with development coordination, issue tracking, and
       planning. What would you like to focus on today?"
```

**Not In Scope** (explicitly):
- ❌ Layer 1 (Manual Settings UI) - deferred to P2
- ❌ Layer 3 (Learning pattern detection) - deferred to P2, post-alpha
- ❌ Cross-channel sync (Slack ↔ Web ↔ CLI portfolio sync)
- ❌ GitHub repo auto-discovery

---

## What Already Exists

### Infrastructure ✅

| Component | Location | Status |
|-----------|----------|--------|
| Project domain model | `services/domain/models.py:194-252` | ✅ Full class with CRUD |
| ProjectRepository | `services/database/repositories.py:173-491` | ✅ Including `count_active_projects()` |
| GUIDANCE intent | `services/shared_types.py` | ✅ IntentCategory.GUIDANCE exists |
| Setup detection | `canonical_handlers.py:_detect_setup_request()` | ✅ Detects "help me set up my projects" |
| Conversation pattern | `services/standup/` | ✅ Template for state machine |
| Portfolio messages | `canonical_handlers.py` | ⚠️ Messages exist but lead nowhere |

### What's Missing ❌

- No `PortfolioOnboardingManager` (state machine for project setup flow)
- No first-meeting trigger when `count_active_projects() == 0`
- No entity extraction for project names from conversation
- The "Would you like to set up..." prompts have no follow-through

---

## Requirements

### Phase 1: First-Meeting Detection
**Objective**: Detect when user has no projects and should be offered onboarding

**Tasks**:
- [ ] Create `FirstMeetingDetector` using `ProjectRepository.count_active_projects()`
- [ ] Hook into greeting/hello handling in canonical_handlers.py
- [ ] Return onboarding prompt instead of generic greeting when projects empty
- [ ] Add bypass for users who decline ("no thanks")

**Deliverables**:
- `services/onboarding/first_meeting_detector.py`
- Tests in `tests/unit/services/onboarding/test_first_meeting_detector.py`
- Modified greeting handler in canonical_handlers.py

### Phase 2: Conversational Onboarding Handler
**Objective**: Multi-turn conversation to gather project info (follow standup pattern)

**Tasks**:
- [ ] Create `PortfolioOnboardingManager` with states:
  - INITIATED: User greeted, awaiting response to "want to set up?"
  - GATHERING_PROJECTS: Asking about projects
  - CONFIRMING: Confirming captured info
  - COMPLETE: Done, projects saved
  - DECLINED: User said no thanks
- [ ] Create `PortfolioOnboardingHandler` for turn-by-turn processing
- [ ] Implement project name/description extraction from natural language
- [ ] Handle graceful fallback if user declines

**Deliverables**:
- `services/onboarding/portfolio_manager.py`
- `services/onboarding/portfolio_handler.py`
- Tests in `tests/unit/services/onboarding/test_portfolio_onboarding.py`

### Phase 3: Project Persistence
**Objective**: Save extracted projects using existing repository

**Tasks**:
- [ ] Connect handler to `ProjectRepository.create()`
- [ ] Store project name, description from conversation
- [ ] Confirmation message with project summary
- [ ] Transition to normal conversation flow

**Deliverables**:
- Integration with existing ProjectRepository
- End-to-end test of full onboarding flow

### Phase Z: Completion & Handoff
- [ ] All acceptance criteria met (checked below)
- [ ] Evidence provided for each criterion
- [ ] Documentation updated (ALPHA_TESTING_GUIDE.md)
- [ ] GitHub issue fully updated with evidence
- [ ] Session log completed

---

## Acceptance Criteria

### Functionality
- [ ] User with 0 projects receives onboarding prompt on first greeting
- [ ] Multi-turn conversation captures at least 1 project name + description
- [ ] "No thanks" gracefully exits onboarding, allows normal interaction
- [ ] Project saved to database via ProjectRepository
- [ ] Subsequent greetings do NOT trigger onboarding (projects exist)

### Testing
- [ ] Unit tests for FirstMeetingDetector
- [ ] Unit tests for PortfolioOnboardingManager (state transitions)
- [ ] Unit tests for PortfolioOnboardingHandler (turn handling)
- [ ] Integration test: full conversation flow from greeting to saved project
- [ ] All tests passing: `pytest tests/unit/services/onboarding/ -v`

### Quality
- [ ] No regressions in existing greeting/GUIDANCE handling
- [ ] Performance: Onboarding turns respond in <500ms (match standup target)
- [ ] Error handling for malformed user input
- [ ] Logging for onboarding events

### Documentation
- [ ] User-facing docs updated (ALPHA_TESTING_GUIDE.md mentions onboarding)
- [ ] Code has docstrings explaining state machine
- [ ] Session log completed

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| FirstMeetingDetector | ❌ | - |
| PortfolioOnboardingManager | ❌ | - |
| PortfolioOnboardingHandler | ❌ | - |
| Handler integration | ❌ | - |
| Unit tests (detection) | ❌ | - |
| Unit tests (manager) | ❌ | - |
| Unit tests (handler) | ❌ | - |
| Integration test | ❌ | - |
| Documentation | ❌ | - |

**Legend**:
- ✅ = Complete with evidence
- ⏸️ = In progress
- ❌ = Not started / Blocked

---

## Testing Strategy

### Unit Tests
```python
# test_first_meeting_detector.py
- test_detects_empty_projects_state
- test_skips_when_projects_exist
- test_handles_database_error_gracefully

# test_portfolio_onboarding.py
- test_state_transitions_initiated_to_gathering
- test_state_transitions_gathering_to_confirming
- test_project_extraction_from_message
- test_decline_flow
- test_graceful_fallback_on_malformed_input
```

### Integration Tests
```python
# test_portfolio_onboarding_e2e.py
- test_full_onboarding_conversation_creates_project
- test_onboarding_not_triggered_when_projects_exist
```

### Manual Testing Checklist
**Scenario 1**: New user onboarding
1. [ ] Create new user with no projects
2. [ ] Say "Hi Piper" in chat
3. [ ] Receive onboarding prompt
4. [ ] Complete multi-turn conversation
5. [ ] Verify project created in database

**Scenario 2**: Decline onboarding
1. [ ] New user says "Hi Piper"
2. [ ] Receives onboarding prompt
3. [ ] Says "no thanks"
4. [ ] Piper gracefully continues with normal greeting
5. [ ] Future greetings don't re-trigger onboarding (respects decline)

---

## Success Metrics

### Quantitative
- Alpha user can complete project setup in <2 minutes
- 80%+ of alpha users have at least 1 project configured after first session
- Zero 422/500 errors during onboarding flow
- Response time <500ms per turn

### Qualitative
- Conversation feels natural, not robotic
- Users understand what happened (project saved, Piper knows context now)

---

## STOP Conditions

**STOP immediately and escalate if**:
- Infrastructure doesn't match assumptions (Project model changed)
- Tests fail for any reason
- State machine pattern from standup doesn't apply
- Entity extraction too complex for scope
- User data at risk
- Completion bias detected

**When stopped**: Document the issue, provide options, wait for PM decision.

---

## Effort Estimate

**Overall Size**: Medium

**Breakdown by Phase**:
- Phase 1 (Detection): Small (2-3 hours)
- Phase 2 (Handler): Medium (4-6 hours) - follows standup pattern
- Phase 3 (Persistence): Small (1-2 hours) - uses existing repo
- Testing: Medium (3-4 hours)
- Documentation: Small (1 hour)

**Complexity Notes**:
- Pattern already established by standup conversation handler
- Existing ProjectRepository means no schema changes
- Main complexity is entity extraction from natural language

---

## Dependencies

### Required (Must be complete first)
- [x] Project domain model and repository ✅ Already exists
- [x] GUIDANCE intent category ✅ Already exists
- [x] Conversation pattern from standup ✅ Available as template

### Optional (Nice to have)
- [ ] #488 Discovery Architecture (helpful but not blocking)

---

## Related Documentation

- **Architecture**: `services/standup/` - conversation pattern template
- **Domain Model**: `services/domain/models.py:194-252` - Project class
- **Repository**: `services/database/repositories.py:173-491` - ProjectRepository
- **Handlers**: `services/intent_service/canonical_handlers.py` - where to integrate

---

## Children (to be created)

Since this is an epic, consider splitting into:
- [ ] Issue: First-meeting detection and onboarding trigger
- [ ] Issue: Conversational project setup handler (state machine)
- [ ] Issue: Project persistence integration
- [ ] Issue: Tests and documentation

Or implement as single issue given Medium size and clear phases.

---

## Notes for Implementation

**Key Insight**: The standup conversation handler (`services/standup/`) is the template. Follow the same patterns:
- `StandupConversationManager` → `PortfolioOnboardingManager`
- `StandupConversationHandler` → `PortfolioOnboardingHandler`
- `StandupConversationState` enum → `PortfolioOnboardingState` enum

**Integration Point**: The greeting handler in `canonical_handlers.py` currently returns generic responses. Add hook to check `FirstMeetingDetector` before returning.

---

_Issue created: 2025-11-XX (original)_
_Last updated: 2026-01-09 (template compliance update)_
