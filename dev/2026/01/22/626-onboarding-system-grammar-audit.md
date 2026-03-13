# Grammar Audit: #626 Onboarding System

## Current State Assessment

### Files Analyzed
- `services/onboarding/portfolio_handler.py` - Main conversation handler (459 lines)
- `services/onboarding/portfolio_manager.py` - State machine management
- `services/onboarding/first_meeting_detector.py` - Trigger detection (123 lines)
- `services/onboarding/__init__.py` - Module exports

### Grammar Compliance Matrix

| Element | Status | Evidence |
|---------|--------|----------|
| Entity | ⚠️ Partial | "I'm Piper Morgan" in start, but user not acknowledged as individual |
| Moment | ✅ Good | Onboarding treated as significant moment, state-aware |
| Place | ⚠️ Partial | No workspace atmosphere ("Welcome to your workspace...") |
| Lenses | ✅ Good | Progress/stage awareness through state machine |
| Situation | ✅ Good | Adapts to INITIATED, GATHERING, CONFIRMING, DECLINED states |

### Current User-Facing Messages

**start_onboarding()** (line 96-100):
```
"Hello! I'm Piper Morgan, your PM assistant. I notice we haven't
set up your project portfolio yet. Would you like to tell me about
the projects you're working on?"
```
- ✅ Introduces Piper
- ⚠️ "I notice" is somewhat mechanical
- ⚠️ No warmth or relationship establishment

**_handle_initiated() - declined** (line 166-169):
```
"No problem! Whenever you're ready to tell me about your projects,
just say 'set up my projects' and we can do this then.
What can I help you with today?"
```
- ✅ Respectful of user choice
- ✅ Offers path forward

**_handle_initiated() - accepted** (line 180):
```
"Great! What's the main project you're focused on right now?"
```
- ⚠️ Functional but not warm

**_handle_gathering() - no projects yet** (line 201-204):
```
"I'd love to know about at least one project you're working on.
What are you building or working on right now?"
```
- ✅ "I'd love to know" has warmth
- ⚠️ Could be warmer

**_handle_gathering() - project captured** (line 251-255):
```
f"Got it - {project_name}. Are there any other projects you'd like
me to know about, or is that your main focus?"
```
- ⚠️ Functional acknowledgment, could show more interest

**_handle_confirming() - confirmed** (line 279-282):
```
f"All set! I've added {project_list} to your portfolio.
I'll help you stay on track with development coordination,
issue tracking, and planning. What would you like to focus on today?"
```
- ✅ Lists capabilities
- ⚠️ No celebration of relationship established

**_handle_confirming() - declined** (line 308-312):
```
"No problem, I won't save those projects.
Let me know if you'd like to set up your portfolio later.
What can I help you with today?"
```
- ✅ Respectful

**Session lost error** (line 134-135):
```
"I'm sorry, I lost track of our conversation. Would you like to start over?"
```
- ✅ Honest about failure

### Grammar Deficits

1. **No Place Atmosphere**: Missing "Welcome to your workspace" framing
2. **Relationship Establishment Light**: User treated as task, not relationship
3. **Project Interest Mechanical**: "Got it" vs genuine curiosity
4. **Completion Celebration Missing**: No warmth when onboarding succeeds
5. **First Meeting Not Special**: Same tone as any other interaction

### Existing Patterns to Leverage

From previous GRAMMAR-TRANSFORM work:
- `services/personality/grammar_context.py` - SituationType enum
- `services/personality/grammar_bridge.py` - Formality-calibrated phrases
- Pattern-052: PersonalityBridge
- Pattern-053: WarmthCalibration

## Transformation Approach

### Phase 1: OnboardingGrammarContext (Dataclass)

Rich context capturing:
- `onboarding_stage`: GREETING, GATHERING, CONFIRMING, COMPLETE, DECLINED
- `is_first_meeting`: bool (always true for onboarding)
- `projects_captured`: int
- `user_seems_hesitant`: bool
- `warmth_level`: float (default higher for onboarding)

### Phase 2: OnboardingNarrativeBridge

Transform context into warm, relationship-establishing phrases:
- Stage-appropriate greetings
- Project acknowledgments with genuine interest
- Completion celebrations
- Respectful decline handling
- Place atmosphere phrases

### Phase 3: Narrative Helpers

Simple helpers for the handler:
- `get_welcome_message()` - First meeting welcome
- `acknowledge_project()` - Warm project acknowledgment
- `get_confirmation_prompt()` - Natural confirmation
- `celebrate_completion()` - Relationship established!
- `handle_decline_warmly()` - Respectful goodbye

### Phase 4: Integration

Update `__init__.py` with exports, run all tests.

## Files to Create

1. `services/onboarding/grammar_context.py`
2. `services/onboarding/narrative_bridge.py`
3. `services/onboarding/narrative_helpers.py`
4. `tests/unit/services/onboarding/test_grammar_context.py`
5. `tests/unit/services/onboarding/test_narrative_bridge.py`
6. `tests/unit/services/onboarding/test_narrative_helpers.py`

## Test Categories

- Context creation from onboarding state
- Stage-appropriate message generation
- Warmth calibration for onboarding
- Project acknowledgment phrasing
- Contractor Test compliance

## Acceptance Criteria Mapping

From issue #626:
- [ ] Onboarding framed as relationship establishment → Phase 2 welcome messages
- [ ] Warm, welcoming language throughout → All phases
- [ ] Place atmosphere present → Phase 2 atmosphere phrases
- [ ] Passes experience test → Phase 3 helpers + Contractor Tests
- [ ] PR review consciousness checklist passed → All phases
