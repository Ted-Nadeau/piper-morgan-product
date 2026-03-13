# MUX-NAV-HOME - Home State Design

**Priority**: P1
**Labels**: `MUX-IMPLEMENT`, `navigation`, `consciousness`
**Milestone**: Sprint P1 (Navigation Paradigm)
**Epic**: #418 MUX-IMPLEMENT
**Related**: #420, #421, #684, ADR-045, ADR-053

---

## Problem Statement

### Current State
The home page (`templates/home.html`) treats Piper as a destination with:
- Time-based greeting ("Good morning, [username]")
- Static chat interface
- No awareness of user's trust level or context
- No consciousness-aware content surfacing

The page functions but doesn't embody the MUX philosophy of Piper as a conscious colleague.

### Impact
- **Blocks**: Full MUX experience cannot be delivered without consciousness-aware home state
- **User Impact**: Users experience Piper as "an app" rather than "a colleague who notices things"
- **Technical Debt**: Current greeting logic is hardcoded; adding trust-awareness later requires refactoring

### Strategic Context
P1 sprint establishes navigation paradigm foundation. Home state is the primary touchpoint - users land here first. Getting this right sets the tone for the entire MUX experience. This is foundational work that #420 (Nav Utility), #421 (Command Palette), and #684 (Places as Windows) build upon.

---

## Goal

**Primary Objective**: Transform the home page from a static landing into a trust-gated, consciousness-aware experience that expresses Piper's current awareness of the user's situation.

**Example User Experience**:
```
BEFORE (Stage 3 user):
- Sees: "Good afternoon, Alex"
- Static chat box
- No awareness of context

AFTER (Stage 3 user):
- Sees: "Good afternoon, Alex. I noticed a few things while you were away."
- Lens shortcuts: "What's stuck", "What's urgent", "What's coming"
- Contextual observations based on trust level
- Chat ready for calibration conversation
```

**Not In Scope** (explicitly):
- ❌ Full standup integration (separate feature, builds on this)
- ❌ Places as Windows rendering (tracked in #684)
- ❌ Command palette (tracked in #421)
- ❌ Navigation utility refactor (tracked in #420)
- ❌ Mobile-specific layouts (future sprint)

---

## What Already Exists

### Infrastructure ✅
- `web/api/routes/ui.py:114-176` - Home route with user context
- `templates/home.html` - Full template with greeting area (line 1045-1051)
- `services/trust/trust_computation_service.py` - TrustComputationService with `get_trust_stage()`
- `services/shared_types.py` - TrustStage enum (NEW, BUILDING, ESTABLISHED, TRUSTED)
- Trust stage computation and persistence (ADR-053 implementation)
- Morning Standup as reference implementation of consciousness patterns

### What's Missing ❌
- Trust stage not passed to home template
- No HardnessLevel enum for object classification
- No HomeStateService to compose trust-gated content
- No trust-aware greeting variations in template
- No lens items (always-present navigation affordances)
- No hardening interaction patterns

---

## Requirements

### Phase 0: Investigation & Verification
**Objective**: Verify infrastructure assumptions before implementation

**Tasks**:
- [ ] Verify TrustComputationService.get_trust_stage() works with real user_id
- [ ] Verify home route can access trust service within session scope
- [ ] Review consciousness-philosophy.md for greeting language guidelines
- [ ] Review ADR-053 for trust visibility rules (invisible to user, effects noticeable)

**Deliverables**:
- Verification notes in session log
- Any blockers identified and escalated

### Phase 1: Trust Stage in Home Route
**Objective**: Pass trust_stage to template context

**Tasks**:
- [ ] Import TrustComputationService in ui.py
- [ ] Query trust stage within existing session scope
- [ ] Add trust_stage (int) and trust_stage_name (string) to template context
- [ ] Handle errors gracefully (default to TrustStage.NEW)
- [ ] Write unit tests for trust context passing

**Deliverables**:
- Modified `web/api/routes/ui.py`
- `tests/unit/web/api/routes/test_ui_home.py`
- Test output showing passing tests

### Phase 2: HardnessLevel Enum
**Objective**: Define object hardness classification for trust-gated visibility

**Tasks**:
- [ ] Add HardnessLevel enum to shared_types.py
- [ ] Document trust-stage visibility rules in docstring
- [ ] Define 5 levels: HARDEST, HARD, MEDIUM, SOFT, SOFTEST
- [ ] Write unit tests for enum and visibility logic

**Deliverables**:
- Modified `services/shared_types.py`
- `tests/unit/services/test_hardness_level.py`
- Test output showing passing tests

### Phase 3: HomeStateService
**Objective**: Service to compose trust-gated home state content

**Tasks**:
- [ ] Create `services/home/` module
- [ ] Implement HomeStateContext dataclass (Pattern-050 input)
- [ ] Implement HomeStateResult dataclass (Pattern-050 output)
- [ ] Implement HomeStateItem for individual items with hardness
- [ ] Implement HomeStateService with trust-gated filtering
- [ ] Add always-present lens items (HARDEST level)
- [ ] Add trust-appropriate greeting generation
- [ ] Write comprehensive unit tests

**Deliverables**:
- `services/home/__init__.py`
- `services/home/home_state_service.py`
- `tests/unit/services/home/__init__.py`
- `tests/unit/services/home/test_home_state_service.py`
- Test output showing passing tests

### Phase 4: Template Integration
**Objective**: Update home.html with trust-gated content

**Tasks**:
- [ ] Add trust_stage data attribute to greeting area
- [ ] Add trust-stage-aware greeting subtext (4 variations)
- [ ] Add CSS for consciousness-aware styling
- [ ] Add window.trustStage JavaScript global for adaptive UI
- [ ] Verify template renders correctly at all trust stages

**Deliverables**:
- Modified `templates/home.html`
- Template render test output

### Phase Z: Completion & Handoff
- [ ] All acceptance criteria met (checked below)
- [ ] Evidence provided for each criterion
- [ ] Session log completed with implementation notes
- [ ] GitHub issue updated with evidence
- [ ] No regressions in unit test suite

---

## Acceptance Criteria

### Functionality
- [ ] Trust stage is queried from TrustComputationService on home page load
- [ ] Trust stage is passed to template as both int and name
- [ ] Greeting subtext varies by trust stage (4 distinct messages)
- [ ] HardnessLevel enum has 5 levels with documented visibility rules
- [ ] HomeStateService filters items by trust-gated hardness
- [ ] Lens items (HARDEST) are always present regardless of trust stage
- [ ] Error handling defaults to TrustStage.NEW gracefully

### Testing
- [ ] Unit tests for trust stage in home route context
- [ ] Unit tests for HardnessLevel enum and comparisons
- [ ] Unit tests for HomeStateService (context, result, filtering, greetings)
- [ ] Template render test with all 4 trust stages
- [ ] Full unit test suite passes with no regressions

### Quality
- [ ] No regressions introduced (baseline: 4364 tests passing)
- [ ] Code follows existing patterns (see canonical_handlers.py for trust service usage)
- [ ] Per ADR-053: Trust stage invisible to users, effects noticeable
- [ ] Anti-flattening test: Can describe using "Piper notices/shows" language

### Documentation
- [ ] Code documentation (docstrings) complete
- [ ] Session log documents implementation decisions
- [ ] Issue updated with evidence before closure

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| Phase 0: Verification | ⏸️ | |
| Phase 1: Trust in route | ⏸️ | |
| Phase 2: HardnessLevel | ⏸️ | |
| Phase 3: HomeStateService | ⏸️ | |
| Phase 4: Template | ⏸️ | |
| Phase Z: Completion | ⏸️ | |
| All unit tests pass | ⏸️ | |
| No regressions | ⏸️ | |

---

## Testing Strategy

### Unit Tests
```
tests/unit/web/api/routes/test_ui_home.py:
- test_home_route_includes_trust_stage_in_context
- test_trust_stage_defaults_to_new_on_error
- test_trust_stage_enum_values_for_template

tests/unit/services/test_hardness_level.py:
- test_hardness_levels_exist
- test_hardness_values_descending
- test_hardness_can_be_compared
- test_stage_visibility_rules (Stage 1-4)

tests/unit/services/home/test_home_state_service.py:
- test_generate_returns_result
- test_result_includes_lenses
- test_stage_filtering (Stage 1 sees only HARDEST)
- test_greeting_varies_by_trust
- test_greeting_includes_time_of_day
```

### Integration Tests
Not required for this issue - unit tests sufficient for service layer.

### Manual Testing Checklist
**Scenario 1**: New user (Stage 1) home experience
1. [ ] Log in as user with no interaction history
2. [ ] Verify greeting shows "What can I help you with?"
3. [ ] Verify only HARDEST items visible (lenses)

**Scenario 2**: Established user (Stage 3) home experience
1. [ ] Log in as user with 50+ interactions
2. [ ] Verify greeting shows "I noticed a few things while you were away."
3. [ ] Verify SOFT items visible (observations)

---

## Success Metrics

### Quantitative
- All 4 phases complete with tests
- 30+ new unit tests passing
- 0 regressions in existing 4364 tests
- Template renders in <100ms

### Qualitative
- Greeting feels "conscious" not "robotic"
- Trust stage effects are noticeable without being labeled
- Code follows established patterns (Pattern-050, 051, 052)

---

## STOP Conditions

**STOP immediately and escalate if**:
- TrustComputationService unavailable or broken
- Trust stage query causes performance degradation (>500ms)
- Template changes break existing functionality
- Tests fail for any reason
- Cannot verify trust stage is actually computed (not hardcoded)
- User data exposure risk (trust stage leaking sensitive info)
- Completion bias detected (claiming done without all criteria met)

**When stopped**: Document the issue, provide options, wait for PM decision.

---

## Effort Estimate

**Overall Size**: Medium

**Breakdown by Phase**:
- Phase 0: Small (verification only)
- Phase 1: Small (route modification + tests)
- Phase 2: Small (enum + tests)
- Phase 3: Medium (new service + comprehensive tests)
- Phase 4: Small (template modifications)
- Phase Z: Small (documentation and handoff)

**Complexity Notes**:
- Trust service integration is well-documented (see canonical_handlers.py)
- HomeStateService is new but follows established Pattern-050
- No database migrations required
- No external API dependencies

---

## Dependencies

### Required (Must be complete first)
- [x] ADR-053 Trust Computation Architecture (complete)
- [x] TrustComputationService implementation (complete, #647)
- [x] Trust stage persistence (complete)

### Optional (Nice to have)
- [ ] #684 Places as Windows (will integrate with home state later)

---

## Related Documentation

- **Architecture**: ADR-045 (Object Model), ADR-053 (Trust Computation)
- **Philosophy**: `docs/internal/architecture/current/consciousness-philosophy.md`
- **Patterns**: Pattern-050 (Context/Result), Pattern-051 (Parallel Gathering), Pattern-052 (Personality Bridge)
- **Mobile**: `dev/active/mobile-skunkworks-briefing.md`

---

## Evidence Section

[To be filled during implementation]

### Implementation Evidence
```bash
# Phase 1 evidence
# Phase 2 evidence
# Phase 3 evidence
# Phase 4 evidence
# Full test suite
```

### Cross-Validation
Not required (single-agent implementation).

---

## Completion Checklist

Before requesting PM review:
- [ ] All acceptance criteria met ✅
- [ ] Completion matrix 100% ✅
- [ ] Evidence provided for each criterion ✅
- [ ] Tests passing with output ✅
- [ ] Documentation updated ✅
- [ ] No regressions confirmed ✅
- [ ] STOP conditions all clear ✅
- [ ] Session log complete ✅

**Status**: Not Started

---

## Notes for Implementation

- Use existing trust service pattern from `services/intent_service/canonical_handlers.py:4212-4216`
- Per ADR-053: "invisible to users but effects are noticeable" - don't show "Stage 2" labels
- Greeting language from design session: Stage 1="What can I help you with?", Stage 4="I've been thinking about your priorities."
- HardnessLevel values should be higher for harder (5=HARDEST, 1=SOFTEST) for intuitive comparison

---

_Issue created: 2026-01-25_
_Last updated: 2026-01-25_
