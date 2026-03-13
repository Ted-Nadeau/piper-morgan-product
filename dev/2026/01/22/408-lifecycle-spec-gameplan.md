# Gameplan: #408 MUX-VISION-LIFECYCLE-SPEC

**Issue**: #408 MUX-VISION-LIFECYCLE-SPEC: Formalize 8-stage lifecycle with composting
**Date**: January 22, 2026
**Author**: Lead Developer
**Priority**: P1 (Part of MUX-VISION sprint)

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI
- [x] Database: PostgreSQL on 5433
- [x] Testing framework: pytest
- [x] Lifecycle infrastructure: `services/mux/lifecycle.py` exists with 471 lines
- [x] Intent handlers: `services/intent_service/canonical_handlers.py` (4000+ lines, 17 handlers)

**My understanding of the task**:
- Replace existing poetic `experience_phrase` values with issue-specified actionable phrases
- Add transition explanation capability
- Add user-facing composting narrative
- Add friendly error messages for invalid transitions
- Integrate lifecycle phrases into intent handlers
- Create documentation

**Forensic finding**: Issue phrases from Nov 27 CXO session; code phrases added during Jan 19 implementation drifted from original spec. PM approved replacing with original intent.

### Part A.2: Work Characteristics Assessment

- [x] Single agent, sequential work
- [x] Focused changes to existing infrastructure
- [x] Duration ~4-6 hours estimated

**Assessment**: ☐ SKIP WORKTREE - Single agent, sequential, contained scope

### Part B: PM Verification

**PM Decision (7:54 AM)**: Approved recommendations:
1. Replace existing phrases with issue-specified ones
2. Unit tests + PM review for testing
3. All handlers systematically, Tier 1 priority for manual testing
4. PM manual testing for "feels natural" assessment

### Part C: Proceed Decision

- [x] **PROCEED** - Understanding verified, approach approved

---

## Phase 0: Initial Bookending

### GitHub Issue Verification
```bash
gh issue view 408
```
- Issue exists ✅
- Parent epic #401 MUX-VISION ✅
- Dependencies #399, #400 both CLOSED ✅

### Codebase Investigation

**Existing infrastructure**:
- `services/mux/lifecycle.py` - LifecycleState enum with properties
- `services/mux/lifecycle.py` - LifecycleTransition, LifecycleManager, CompostingExtractor
- `services/intent_service/canonical_handlers.py` - 17 handlers to integrate

**Gap confirmed**:
- `experience_phrase` values don't match issue spec (poetic vs actionable)
- No transition explanation method
- No user-facing composting narrative
- InvalidTransitionError has technical message, no friendly version

---

## Phase 0.5: Frontend-Backend Contract Verification

**N/A** - This is backend experience layer work, no new API endpoints.

---

## Phase 0.6: Data Flow & Integration Verification

### Integration Points

| Caller | Callee | Verified? |
|--------|--------|-----------|
| Intent handlers | LifecycleState.experience_phrase | ✅ Property exists |
| Intent handlers | LifecycleState.transition_explanation() | ❌ To be created |
| Intent handlers | CompostingExtractor.narrative() | ❌ To be created |

### Pattern Adaptation Notes

**Source Pattern**: Existing `experience_phrase` property
**This Implementation**: Replace values, add methods
**Why Different**: Original was placeholder; this is production experience layer

---

## Phase 0.8: Post-Completion Integration

**N/A** - This feature changes presentation layer only (phrase text). No database state changes, no downstream behavior changes beyond response wording.

---

## Phase 1: Replace Experience Phrases

**Objective**: Update `experience_phrase` property to match issue specification

### Tasks
- [ ] Update EMERGENT phrase: "I just noticed..."
- [ ] Update DERIVED phrase: "I figured out from..."
- [ ] Update NOTICED phrase: "I'm aware of..."
- [ ] Update PROPOSED phrase: "I think we should..."
- [ ] Update RATIFIED phrase: "We're doing..."
- [ ] Update DEPRECATED phrase: "This used to be..."
- [ ] Update ARCHIVED phrase: "I remember when..."
- [ ] Update COMPOSTED phrase: "I learned that..."
- [ ] Update tests for new phrase values
- [ ] Run all lifecycle tests

### Deliverables
- Modified `services/mux/lifecycle.py`
- Updated tests in `tests/unit/services/mux/test_lifecycle.py`
- All 69 lifecycle tests passing

### STOP Conditions
- If tests fail for reasons other than expected phrase changes
- If other code depends on exact phrase wording (grep first)

---

## Phase 2: Add Transition Explanations

**Objective**: Add method to explain why objects transition between states

### Tasks
- [ ] Add `transition_explanation(from_state, to_state, reason=None)` method
- [ ] Create explanation templates for each valid transition
- [ ] Handle invalid transition explanation gracefully
- [ ] Add unit tests for transition explanations
- [ ] Verify friendly language (contractor test)

### Deliverables
- New method in `services/mux/lifecycle.py`
- 16+ tests (one per valid transition + edge cases)

### STOP Conditions
- Transition explanation templates don't cover all 11 valid transitions
- Explanation language fails contractor test
- Technical jargon leaks into explanations

### Transition Explanation Templates

| From | To | Template |
|------|-----|----------|
| EMERGENT | DERIVED | "I recognized a pattern in {object}" |
| EMERGENT | NOTICED | "I noticed {object} needed attention" |
| DERIVED | NOTICED | "{object} caught my attention" |
| DERIVED | DEPRECATED | "{object} is no longer relevant" |
| NOTICED | PROPOSED | "I think we should act on {object}" |
| NOTICED | DEPRECATED | "{object} is no longer a priority" |
| PROPOSED | RATIFIED | "We agreed to proceed with {object}" |
| PROPOSED | DEPRECATED | "We decided not to pursue {object}" |
| RATIFIED | DEPRECATED | "{object} has served its purpose" |
| DEPRECATED | ARCHIVED | "I'm preserving {object} for reference" |
| ARCHIVED | COMPOSTED | "{object} has taught me something" |

---

## Phase 3: Composting Narrative

**Objective**: Add user-facing narrative for composting process

### Tasks
- [ ] Add `get_composting_narrative(compost_result)` function
- [ ] Create narrative templates based on journey length/type
- [ ] Integrate with "filing dreams" metaphor
- [ ] Add unit tests for narrative generation
- [ ] Verify no "deletion" language

### Deliverables
- New function in `services/mux/lifecycle.py` or separate module
- 10+ tests for narrative variations

### STOP Conditions
- Narrative sounds like surveillance ("I noticed while you were away...")
- "Filing dreams" metaphor feels creepy instead of reflective
- Any "deletion" language appears

### Narrative Templates

| Journey Type | Narrative |
|--------------|-----------|
| Full lifecycle | "Having had time to reflect on {object}, I learned: {lessons}" |
| Short lifecycle | "{object} was brief, but I noticed: {lessons}" |
| Ratified then deprecated | "{object} worked for a while. Looking back: {lessons}" |

---

## Phase 4: Friendly Error Messages

**Objective**: Add user-friendly messages to InvalidTransitionError

### Tasks
- [ ] Add `user_message` property to InvalidTransitionError
- [ ] Create friendly explanations for common invalid transitions
- [ ] Ensure no technical jargon in user-facing message
- [ ] Add unit tests

### Deliverables
- Updated InvalidTransitionError class
- 8+ tests for error message generation

### STOP Conditions
- Friendly message still exposes state names (EMERGENT, DEPRECATED, etc.)
- Technical jargon leaks through
- User could be confused about what they did wrong

### Error Message Templates

| Invalid Transition | Friendly Message |
|-------------------|------------------|
| Backward (any) | "I can't go back to that state - things only move forward" |
| Skip state | "That's too big a jump - let's take it one step at a time" |
| From COMPOSTED | "Once something becomes a learning, it stays that way" |

---

## Phase 5: Intent Handler Integration

**Objective**: Integrate lifecycle phrases into relevant intent handlers

### Tier 1 Handlers (Priority for manual testing)
- [ ] `_handle_status_query` (line 1107)
- [ ] `_handle_status_report` (line 3144)
- [ ] `_handle_retrospective_query` (line 2940)
- [ ] `_handle_priority_query` (line 1493)
- [ ] `_handle_spatial_project_landscape` (line 3082)

### Tier 2 Handlers
- [ ] `_handle_temporal_query` (line 664)
- [ ] `_handle_temporal_last_activity` (line 3014)
- [ ] `_handle_agenda_query` (line 2717)
- [ ] `_handle_guidance_query` (line 3900)

### Tier 3 Handlers (Lower lifecycle relevance)
- [ ] `_handle_identity_query` (line 172)
- [ ] `_handle_identity_health_check` (line 329)
- [ ] `_handle_identity_help` (line 477)
- [ ] `_handle_identity_differentiation` (line 559)
- [ ] `_handle_spatial_project_list` (line 1439)
- [ ] `_handle_temporal_project_duration` (line 3739)
- [ ] `_handle_conversation_query` (line 4038)

### Integration Pattern
```python
# When describing object state:
lifecycle_state = obj.lifecycle_state
phrase = lifecycle_state.experience_phrase
# e.g., "I just noticed this task..." for EMERGENT

# When explaining transitions:
explanation = LifecycleState.transition_explanation(
    from_state, to_state, reason=context
)
```

### Deliverables
- Updated handlers in `services/intent_service/canonical_handlers.py`
- Integration tests verifying phrase usage
- No regressions in existing handler tests

### STOP Conditions
- Handler tests fail after integration
- Lifecycle method not accessible from handler context
- Existing handler behavior changes unexpectedly

### Wiring Tests Required
```python
# Verify LifecycleState importable from handlers
def test_lifecycle_importable_from_handlers():
    from services.mux.lifecycle import LifecycleState
    assert hasattr(LifecycleState.EMERGENT, 'experience_phrase')

# Verify transition_explanation method exists
def test_transition_explanation_callable():
    from services.mux.lifecycle import transition_explanation
    assert callable(transition_explanation)
```

---

## Phase 6: Documentation

**Objective**: Create lifecycle experience guide

### Tasks
- [ ] Create `docs/internal/architecture/current/lifecycle-experience-guide.md`
- [ ] Document all 8 states with experience phrases
- [ ] Document transition explanations
- [ ] Document composting narrative patterns
- [ ] Document error handling approach
- [ ] Add integration examples for handlers

### Deliverables
- Complete documentation file
- Cross-referenced from ADR-055

---

## Phase 7: Manual Testing Scenarios

**Objective**: Prepare scenarios for PM manual testing

### Scenarios for PM Review

**Scenario 1: Status Query with Lifecycle**
1. Query: "What's the status of [project]?"
2. Expected: Response uses lifecycle-appropriate language
3. Verify: Phrases feel natural, not robotic

**Scenario 2: Transition Explanation**
1. Action: Mark task as deprecated
2. Expected: Piper explains transition naturally
3. Verify: "This served us well" not "State changed to DEPRECATED"

**Scenario 3: Composting Narrative**
1. Action: Archive and compost old sprint
2. Expected: Piper reflects on learnings
3. Verify: "Filing dreams" tone, not surveillance tone

**Scenario 4: Error Handling**
1. Action: Attempt invalid transition
2. Expected: Friendly explanation of why not possible
3. Verify: No technical error message shown to user

### Deliverables
- Test scenario document for PM
- Checklist for alpha testing manual (future)

---

## Phase Z: Final Bookending & Handoff

### Completion Checklist
- [ ] All acceptance criteria met
- [ ] All tests passing (69 existing + new)
- [ ] Documentation complete
- [ ] PM manual testing complete
- [ ] No "deletion" language verified
- [ ] Session log updated
- [ ] GitHub issue updated with evidence

### Evidence Required
- Test output showing all tests pass
- Sample phrases from each state
- Sample transition explanations
- Sample composting narrative
- PM sign-off on "feels natural"

---

## Acceptance Criteria

### Functionality
- [ ] All 8 states have updated experience phrases matching issue spec
- [ ] Transition explanations work for all valid transitions
- [ ] Composting narrative generates appropriate story
- [ ] Error messages are user-friendly
- [ ] Intent handlers use lifecycle phrases where appropriate

### Testing
- [ ] Unit tests for phrase generation (8 tests)
- [ ] Unit tests for transition explanations (16+ tests)
- [ ] Unit tests for composting narrative (10+ tests)
- [ ] Unit tests for error messages (8+ tests)
- [ ] Integration tests for handler usage
- [ ] PM manual testing of scenarios

### Quality
- [ ] No regressions in existing tests
- [ ] Contractor test passes on all phrases
- [ ] No "deletion" language anywhere
- [ ] No technical jargon in user-facing messages

### Documentation
- [ ] Lifecycle experience guide created
- [ ] Integration examples documented
- [ ] Session log complete

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| Phase 1: Experience phrases | ✅ | 454 mux tests passing |
| Phase 2: Transition explanations | ✅ | 11 transition templates + 11 tests |
| Phase 3: Composting narrative | ✅ | get_composting_narrative() + 10 tests |
| Phase 4: Friendly errors | ✅ | user_message property + 4 tests |
| Phase 5: Handler integration | ✅ | lifecycle_integration.py + 20 tests |
| Phase 6: Documentation | ✅ | lifecycle-experience-guide.md + ADR-055 update |
| Phase 7: Manual testing | ✅ | 408-manual-testing-scenarios.md prepared |
| Phase Z: Closeout | ✅ | 499 mux tests, all phases complete |

---

## Testing Strategy

### Unit Tests
```python
# Phase 1: Phrase tests
def test_emergent_experience_phrase():
    assert "noticed" in LifecycleState.EMERGENT.experience_phrase.lower()

# Phase 2: Transition tests
def test_transition_explanation_emergent_to_derived():
    explanation = transition_explanation(EMERGENT, DERIVED, "pattern found")
    assert "recognized" in explanation.lower()

# Phase 3: Narrative tests
def test_composting_narrative_full_journey():
    result = CompostResult(journey=[EMERGENT, ..., COMPOSTED], lessons=["..."])
    narrative = get_composting_narrative(result)
    assert "reflect" in narrative.lower()

# Phase 4: Error tests
def test_invalid_transition_user_message():
    error = InvalidTransitionError(COMPOSTED, EMERGENT)
    assert "learning" in error.user_message.lower()
```

### Integration Tests
```python
# Phase 5: Handler integration
async def test_status_query_uses_lifecycle_phrase():
    result = await handler._handle_status_query(intent, session_id)
    # Verify response includes lifecycle-aware language
```

---

## Success Metrics

### Quantitative
- 69 existing lifecycle tests still passing
- 40+ new tests added
- 17 handlers updated
- 0 regressions

### Qualitative
- PM confirms phrases "feel natural"
- Contractor test passes on all new language
- No uncanny valley effect in responses

---

## STOP Conditions

- Existing lifecycle tests fail unexpectedly
- Other code depends on exact phrase wording (check grep results)
- Handler changes break existing functionality
- PM feedback indicates fundamental approach issues
- "Deletion" language discovered anywhere

---

## Effort Estimate

**Overall Size**: Medium

| Phase | Estimate |
|-------|----------|
| Phase 1: Phrases | Small (30 min) |
| Phase 2: Transitions | Medium (1 hour) |
| Phase 3: Narrative | Medium (1 hour) |
| Phase 4: Errors | Small (30 min) |
| Phase 5: Handlers | Medium-Large (2 hours) |
| Phase 6: Documentation | Small (30 min) |
| Phase 7: Manual testing | PM time |
| **Total** | ~5-6 hours |

---

## Dependencies

### Required (Complete)
- [x] #399 - Object Model Implementation
- [x] #400 - Consciousness Philosophy

### Optional
- [ ] MUX super-epic completion for full E2E testing

---

## Related Documentation

- **Architecture**: ADR-055 Object Model Implementation
- **Source Design**: `dev/2025/11/29/object-model-brief-v2.md`
- **Composting Architecture**: `docs/internal/architecture/current/composting-learning-architecture.md`
- **Pattern**: Pattern-050 Context-Dataclass Pair (for phrase organization)

---

## Notes for Implementation

**Key insight from forensic research**: The issue phrases are the original CXO session intent. The code phrases were implementation drift. Replace to restore original design.

**Integration approach**: Lifecycle phrases are a foundation layer. Handlers call into LifecycleState properties; changes propagate automatically once properties are updated.

**Manual testing priority**: Tier 1 handlers (status, retrospective, priority) are most lifecycle-relevant. PM should focus manual testing there.

---

_Gameplan created: January 22, 2026_
_PM approved approach: 7:54 AM_
