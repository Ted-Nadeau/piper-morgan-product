# Gameplan: #766 GLUE-MAINPROJ — Fix "Is that your main project?" repeated question

**Issue**: https://github.com/mediajunkie/piper-morgan-product/issues/766
**Epic**: #762 GLUE Conversational Glue Implementation
**Branch**: `claude/m0-conversational-glue`
**Effort Estimate**: 1-2 days
**Author**: Lead Developer
**Date**: 2026-02-16

---

## Phase -1: Infrastructure Verification ✅ COMPLETE

Completed during pre-sprint verification:
- Branch created: `claude/m0-conversational-glue`
- Migration chain clean (single head)
- All relevant models verified
- Onboarding module fully traced

**Worktree Assessment**: SKIP WORKTREE
- Single agent, sequential work
- Small fix, tightly coupled files
- Estimated <1 day implementation

---

## Phase 0: Investigation ✅ COMPLETE

### Root Cause

The bug has **two components**:

**Component 1: Hard-coded question repeats on every project**

In [portfolio_handler.py:249-255](services/onboarding/portfolio_handler.py#L249-L255), after every project extraction:
```python
response_message = (
    f"Got it - {project_name}. "
    f"Are there any other projects you'd like me to know about, "
    f"or is that your main focus?"
)
```
This repeats identically for project 1, 2, 3, ..., N.

**Component 2: Initial question contradicts subsequent questions**

In [portfolio_handler.py:180](services/onboarding/portfolio_handler.py#L180), the FIRST question asks:
```python
response_message = "Great! What's the main project you're focused on right now?"
```
This explicitly solicits the "main" project, then every subsequent question asks "or is that your main focus?" — a logical contradiction. You can't have multiple "main" projects.

### Existing Infrastructure (75% Complete Pattern)

A proper narrative system was built but **never wired into the handler**:

| Component | File | Status |
|-----------|------|--------|
| `OnboardingNarrativeBridge` | [narrative_bridge.py](services/onboarding/narrative_bridge.py) | ✅ Built, tested, not used by handler |
| `OnboardingGrammarContext` | [grammar_context.py](services/onboarding/grammar_context.py) | ✅ Built, tested, tracks `projects_captured` |
| `narrative_helpers` | [narrative_helpers.py](services/onboarding/narrative_helpers.py) | ✅ Built, tested, exported, not called |
| `PortfolioOnboardingHandler` | [portfolio_handler.py](services/onboarding/portfolio_handler.py) | ❌ Uses hard-coded strings |
| `is_default` field | [models.py](services/domain/models.py#L352) | ✅ Field exists, never set during onboarding |

### What's Actually Broken (Comprehensive)

1. **_handle_initiated** (line 180): Asks "What's the main project...?" — frames first project as main
2. **_handle_gathering** (lines 249-255): Asks "or is that your main focus?" — repeats per project
3. **narrative_bridge MORE_PROJECTS_PROMPTS "conversational" variant**: Also says "main focus" — template has same bug
4. **`is_default` never set**: After onboarding, ALL projects get `is_default=False`, making the "main" question pointless
5. **_handle_confirming** (lines 272-274): Has leftover debug `print()` statements from #731

---

## Phase 0.6: Data Flow Verification ✅ COMPLETE

Already traced during investigation:

| Layer | Needs user_id? | Needs session_id? | Source |
|-------|----------------|-------------------|--------|
| ConversationHandler | ✅ | ✅ | HTTP session + auth |
| PortfolioOnboardingHandler | ❌ | ✅ (session.id) | Manager lookup |
| PortfolioOnboardingManager | ❌ | ✅ | In-memory dict key |
| Project persistence | ✅ | ❌ | From user context at save time |

**Key**: `is_default` is set at persistence time (`_persist_onboarding_projects`), not during gathering. We'll need to pass the user's choice through to persistence.

---

## Phase 0.7: Conversation Design (CRITICAL for this issue)

### Current Flow (Broken)

```
Turn 1 (INITIATED → GATHERING):
  User: "Sure, let's do it"
  Piper: "Great! What's the main project you're focused on right now?"
  Problems: Frames first project as "main" before knowing total

Turn 2 (GATHERING):
  User: "Project Alpha"
  Piper: "Got it - Project Alpha. Are there any other projects you'd like me to know about, or is that your main focus?"
  Problems: Asks "main focus" — contradicts if user adds more

Turn 3 (GATHERING):
  User: "Project Beta"
  Piper: "Got it - Project Beta. Are there any other projects you'd like me to know about, or is that your main focus?"
  Problems: Identical to Turn 2 — robotic parrotry

Turn 4 (GATHERING → CONFIRMING):
  User: "That's all"
  Piper: "I have Project Alpha, Project Beta noted. Should I save these to your portfolio?"
  Problems: Never actually captures which is "main"
```

### Designed Flow (Fixed)

**Single project scenario:**
```
Turn 1 (INITIATED → GATHERING):
  User: "Sure, let's do it"
  Piper: "What are you working on right now?"
  Change: No "main" framing — just ask what they're working on

Turn 2 (GATHERING → CONFIRMING):
  User: "Project Alpha"
  Piper: "Project Alpha — nice! Should I save that to your portfolio?"
  Change: Acknowledge warmly via narrative_bridge, transition to confirm
  Note: Single project → automatically is_default=True (no need to ask)
```

**Multiple project scenario:**
```
Turn 1 (INITIATED → GATHERING):
  User: "Sure, let's do it"
  Piper: "What are you working on right now?"

Turn 2 (GATHERING):
  User: "Project Alpha"
  Piper: "Project Alpha — that sounds like a great project! Are there any other projects you'd like me to know about?"
  Change: Use narrative_bridge acknowledgment + more_projects_prompt (no "main focus")

Turn 3 (GATHERING):
  User: "Also working on Project Beta"
  Piper: "Got it — I'll keep track of that one too. Any others?"
  Change: Use ADDITIONAL_PROJECT_ACKNOWLEDGMENTS + varied follow-up

Turn 4 (GATHERING → CONFIRMING):
  User: "That's all"
  Piper: "I have Project Alpha and Project Beta. Which would you call your main focus right now? (Or I can just save them both without a primary.)"
  Change: Ask "which is main" ONCE, at the END, with an easy opt-out

Turn 5 (CONFIRMING → COMPLETE):
  User: "Alpha is my main one"
  Piper: "All set! I've added Project Alpha and Project Beta to your portfolio, with Alpha as your primary. What would you like to focus on today?"
  Change: Confirm what was saved, mention primary designation
```

### Edge Cases

| User Input | State | Expected Behavior |
|------------|-------|-------------------|
| "Project Alpha" (only project, then "done") | GATHERING→CONFIRMING | Auto-set as default, don't ask |
| "Neither is my main one" / "just save them" | CONFIRMING (main question) | Save both as is_default=False, no problem |
| User adds 5+ projects | GATHERING | Still only ask "which is main?" once at end |
| "Alpha is main" during gathering | GATHERING | Accept designation, note it, keep gathering |
| User changes mind about main later | Post-onboarding | Needs to be possible (acceptance criteria) — separate concern, not this issue |

---

## Phase 0.8: Post-Completion Integration

### Completion Side-Effects

| Side Effect | Table/Field | Current | After Fix |
|-------------|-------------|---------|-----------|
| Main project designated | projects.is_default | Always False | True for designated project |
| Other projects | projects.is_default | All False | Remain False |

### Downstream Behavior Changes

| Feature | Before Fix | After Fix |
|---------|-----------|-----------|
| "What project?" questions | May ask every time | Can default to is_default project |
| Project switching | No default | Pre-selected default |

---

## Phase 1: Wire Narrative System into Handler

### Objective
Replace hard-coded strings in `portfolio_handler.py` with calls to the existing `narrative_helpers` module.

### Tasks

- [ ] Import `narrative_helpers` functions into `portfolio_handler.py`
- [ ] Create `OnboardingGrammarContext.from_session()` calls at each handler method entry
- [ ] Replace hard-coded string in `_handle_initiated` (line 180) with `narrative_helpers` call
- [ ] Replace hard-coded string in `_handle_gathering` (lines 249-255) with `narrative_bridge` acknowledgment + more_projects_prompt
- [ ] Replace hard-coded strings in `_handle_confirming` with `narrative_bridge` equivalents
- [ ] Remove debug `print()` statements in `_handle_confirming` (leftover from #731)

### Not changing
- Pattern matching logic (DONE_PATTERNS, CONFIRM_PATTERNS, DECLINE_PATTERNS)
- State machine transitions
- Project extraction logic

---

## Phase 2: Fix Question Content and Logic

### Objective
Eliminate repeated "main focus" question, add single contextual designation question.

### Tasks

- [ ] Fix `_handle_initiated` response: Remove "main" framing → "What are you working on right now?"
- [ ] Fix `narrative_bridge.MORE_PROJECTS_PROMPTS["conversational"]`: Remove "or is that your main focus?" → "Any other projects you're working on?"
- [ ] Add project-count-aware response variation in `_handle_gathering`:
  - First project: `FIRST_PROJECT_ACKNOWLEDGMENTS` + `MORE_PROJECTS_PROMPTS`
  - Subsequent: `ADDITIONAL_PROJECT_ACKNOWLEDGMENTS` + varied follow-up
- [ ] Add "which is your main focus?" question to `_transition_to_confirming()`:
  - Only when `len(captured_projects) > 1`
  - Include easy opt-out: "Or I can just save them all without a primary."
  - Single project: skip question, auto-set as default
- [ ] Add response handling in `_handle_confirming` for the main-project designation answer

---

## Phase 3: Integrate is_default Persistence

### Objective
Actually set `is_default=True` on the designated project when persisting onboarding results.

### Tasks

- [ ] Track the user's main project designation in session state (add field to session or captured_projects)
- [ ] Pass designation through to `_persist_onboarding_projects()` (in `conversation_handler.py`)
- [ ] Set `is_default=True` on designated project during persistence
- [ ] If single project, auto-set `is_default=True`
- [ ] If user declines to designate, leave all `is_default=False`

### Data flow for designation

```
User says "Alpha is my main one"
  → _handle_confirming() stores designation in session
  → session.captured_projects[0]["is_default"] = True (or similar)
  → _persist_onboarding_projects() reads and applies
  → ProjectDB created with is_default=True
```

---

## Phase 4: Testing

### Unit Tests

- [ ] Test `_handle_initiated` no longer says "main project"
- [ ] Test `_handle_gathering` response varies by project count (1st vs 2nd vs 3rd)
- [ ] Test "main focus" question NOT asked for single project
- [ ] Test "which is your main focus?" asked once for multiple projects
- [ ] Test user can decline to designate a main project
- [ ] Test `is_default` set correctly after full flow (single project = auto-default)
- [ ] Test `is_default` set correctly when user designates (multi-project)
- [ ] Test `is_default` all-false when user declines to designate

### Wiring Integration Tests

- [ ] Test full onboarding flow: INITIATED → GATHERING (3 projects) → CONFIRMING → COMPLETE
  - Verify "main" question asked exactly once
  - Verify no repeated question text across turns
  - Verify `is_default` persistence

### Colleague Test Scenarios

- [ ] Single project flow: Does it feel natural?
- [ ] Three project flow: Is the "main focus" question well-timed?
- [ ] Declining main designation: Is it comfortable to say "no primary"?
- [ ] Response variety: Do the acknowledgments feel varied, not templated?

---

## Phase Z: Handoff

### Acceptance Criteria Mapping

| Acceptance Criterion | Phase | Evidence |
|---------------------|-------|---------|
| "Main project" asked max once per session | Phase 2 | Unit test + integration test |
| Question timing contextually appropriate | Phase 2 | Colleague test documented |
| User can designate/change main anytime | Phase 3 | Unit test for designation |
| No repeated templated questions in any workflow | Phase 1+2 | Integration test across full flow |
| Passes Colleague Test | Phase 4 | Manual verification documented |

### Sprint Gate Checks (#779)

- [ ] **Gate 1 - Persistence**: is_default DB write verified with test
- [ ] **Gate 2 - Anti-Flattening**: Implementation matches conversation design above, zero parrot confirmations
- [ ] **Gate 3 - Multi-Tenancy**: is_default is user-scoped (projects already have owner_id)

### Not In Scope

- ❌ Redesigning entire setup wizard flow
- ❌ Cross-session memory of main project (that's M0 FOLLOWUP territory)
- ❌ Changing main project post-onboarding via chat command (acceptance criteria says "can designate/change" — for this issue, we ensure the mechanism exists; a full change-main-project command is future work)
- ❌ Narrative bridge changes beyond fixing the "main focus" text in MORE_PROJECTS_PROMPTS

### Dependencies

- None (first issue in M0 sequence by design)

### STOP Conditions

- If narrative_bridge integration breaks existing onboarding tests
- If `is_default` persistence requires a new migration (investigate first)
- If the confirmation flow redesign grows beyond 2 days

---

## Files to Modify

| File | Changes |
|------|---------|
| `services/onboarding/portfolio_handler.py` | Replace hard-coded strings with narrative system, fix question logic |
| `services/onboarding/narrative_bridge.py` | Fix "conversational" MORE_PROJECTS_PROMPTS text |
| `services/onboarding/narrative_bridge.py` | Add main-project designation prompts (new templates) |
| `tests/unit/services/onboarding/test_portfolio_onboarding.py` | Update/add tests for new behavior |
| `tests/integration/test_portfolio_onboarding_e2e.py` | Add full-flow integration test |

### Files NOT to modify
- `services/onboarding/grammar_context.py` — Already has everything we need
- `services/onboarding/narrative_helpers.py` — Already wraps the bridge correctly
- `services/onboarding/portfolio_manager.py` — State machine and session management unchanged
- `services/domain/models.py` — `is_default` field already exists
- `services/database/models.py` — `is_default` column already exists

---

_Gameplan v1.0 — 2026-02-16_
_Author: Lead Developer_
_Status: Awaiting PM review_
