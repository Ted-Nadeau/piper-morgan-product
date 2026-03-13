# MUX-NAV-UTILITY - Navigation Utility Layer

**Priority**: P1
**Labels**: `MUX-IMPLEMENT`, `navigation`, `consciousness`
**Milestone**: Sprint P1 (Navigation Paradigm)
**Epic**: #418 MUX-IMPLEMENT
**Related**: #419 (Home State), #421 (Command Palette), #684 (Places), ADR-045, ADR-053

---

## Problem Statement

### Current State
Current navigation components (`templates/components/navigation.html`, ~730 lines) were "vibe coded" before MUX consciousness work:
- Dropdown menu of data types: "Todos", "Projects", "Files", "Lists"
- Static structure regardless of trust level
- No consciousness grammar (treats Piper as filing system)
- No awareness of what user needs right now

The navigation technically works but undermines the colleague paradigm.

### Impact
- **Blocks**: #419 establishes home as primary experience; nav must support (not compete with) this paradigm
- **User Impact**: Users see nav and think "Piper is an app I browse" instead of "Piper is a colleague who helps"
- **Technical Debt**: Nav items hardcoded; trust-gated visibility requires refactoring

### Strategic Context
P1 establishes navigation paradigm. #419 (Home State) is primary experience; this issue makes nav the "filing cabinet in the corner" - available for power users but not prominent. Complements #421 (Command Palette) for keyboard-first access.

---

## Goal

**Primary Objective**: Transform the navigation from "browse Piper like an app" to a utility layer that supports the home state experience without undermining the colleague paradigm.

**Example User Experience**:
```
BEFORE (Stage 3 user):
- Sees: "My Work" dropdown with Todos, Projects, Files, Lists
- Feels like: Filing cabinet to browse
- Behavior: User starts browsing instead of asking Piper

AFTER (Stage 3 user):
- Sees: Minimal nav with "Home", search trigger, user menu
- Home state surfaces what's relevant
- Nav available but not prominent
- Behavior: User converses with Piper; nav is escape hatch
```

**Not In Scope** (explicitly):
- ❌ Home state design (tracked in #419)
- ❌ Command palette implementation (tracked in #421)
- ❌ Places as Windows visualization (tracked in #684)
- ❌ Mobile-specific nav patterns (future sprint)
- ❌ Complete nav redesign from scratch (refactor existing)

---

## What Already Exists

### Infrastructure ✅
- `templates/components/navigation.html` (~730 lines) - Full navigation component
- `templates/components/user_menu.html` - User menu dropdown
- `web/static/css/` - Navigation CSS
- Deployed on 17 templates
- Mobile hamburger menu
- ARIA labels and keyboard navigation
- #419 established HardnessLevel enum for trust-gated visibility

### What's Missing ❌
- Trust-gated nav item visibility
- Consciousness-aware item labeling
- Clear hierarchy (home state primary, nav secondary)
- Integration points with command palette
- Natural language item names (not database table names)

---

## Requirements

### Phase 0: Investigation & Verification
**Objective**: Audit current nav and establish design direction

**Tasks**:
- [ ] Audit all nav items against anti-flattening rubric
- [ ] Map current items to consciousness grammar equivalents
- [ ] Identify trust-appropriate visibility for each item
- [ ] Review naming-conventions-v1 for vocabulary guidance
- [ ] Check #419 HardnessLevel for visibility rules alignment

**Deliverables**:
- Nav item audit table (current → proposed)
- Trust-visibility matrix
- Any blockers identified

### Phase 1: Item Vocabulary Refactor
**Objective**: Replace database-style labels with consciousness grammar

**Tasks**:
- [ ] Replace "My Work" with natural language equivalent
- [ ] Replace "Todos/Projects/Files/Lists" with action-oriented labels
- [ ] Ensure labels pass anti-flattening test ("What can Piper help with?")
- [ ] Update `navigation.html` with new labels
- [ ] Write unit tests for nav content

**Deliverables**:
- Modified `templates/components/navigation.html`
- Tests for nav item content
- Vocabulary mapping documentation

### Phase 2: Trust-Gated Visibility
**Objective**: Show/hide nav items based on trust stage

**Tasks**:
- [ ] Pass trust_stage to nav component
- [ ] Implement visibility rules using HardnessLevel
- [ ] Stage 1-2: Minimal nav (Home, Search, User Menu)
- [ ] Stage 3-4: Full nav with progressive items
- [ ] Write unit tests for trust-gated visibility

**Deliverables**:
- Modified `templates/components/navigation.html`
- Modified template inclusion with trust context
- Tests for visibility at each trust stage

### Phase 3: Visual Hierarchy Adjustment
**Objective**: Position nav as secondary to home state

**Tasks**:
- [ ] Reduce nav visual prominence (size, color, position)
- [ ] Ensure home state is clearly primary
- [ ] Add visual cue that nav is "utility" not "main"
- [ ] CSS modifications for subtlety
- [ ] Verify no accessibility degradation

**Deliverables**:
- Modified CSS for nav
- Accessibility audit results
- Before/after screenshots

### Phase 4: Command Palette Integration Points
**Objective**: Clarify nav vs palette usage

**Tasks**:
- [ ] Add keyboard shortcut hint in nav (Cmd/Ctrl+K for palette)
- [ ] Ensure nav items don't duplicate palette actions
- [ ] Add search trigger that invokes command palette
- [ ] Document intended usage pattern

**Deliverables**:
- Modified nav with palette trigger
- Usage pattern documentation

### Phase Z: Completion & Handoff
- [ ] All acceptance criteria met
- [ ] Evidence provided for each criterion
- [ ] Session log completed
- [ ] GitHub issue updated with evidence
- [ ] No regressions in test suite

---

## Acceptance Criteria

### Functionality
- [ ] Nav items use natural language (not database table names)
- [ ] Trust-gated visibility working (Stage 1-2 minimal, Stage 3-4 full)
- [ ] Home link prominent; other items secondary
- [ ] Search trigger invokes command palette (or placeholder for #421)
- [ ] All nav items pass anti-flattening test
- [ ] Nav available on all 17 current templates

### Testing
- [ ] Unit tests for nav item content
- [ ] Unit tests for trust-gated visibility
- [ ] Accessibility tests (keyboard nav, ARIA)
- [ ] Full unit test suite passes with no regressions

### Quality
- [ ] No regressions introduced
- [ ] Visual hierarchy supports home-state-first paradigm
- [ ] Anti-flattening test: All items describable as "Piper can help you..."
- [ ] Accessibility maintained (WCAG 2.1 AA)

### Documentation
- [ ] Vocabulary mapping documented
- [ ] Usage pattern documented (when to use nav vs palette)
- [ ] Session log documents design decisions

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| Phase 0: Investigation | ⏸️ | |
| Phase 1: Vocabulary | ⏸️ | |
| Phase 2: Trust-Gated | ⏸️ | |
| Phase 3: Visual Hierarchy | ⏸️ | |
| Phase 4: Palette Integration | ⏸️ | |
| Phase Z: Completion | ⏸️ | |
| All unit tests pass | ⏸️ | |
| No regressions | ⏸️ | |

---

## Testing Strategy

### Unit Tests
```
tests/unit/templates/test_navigation.py:
- test_nav_items_use_natural_language
- test_nav_available_on_required_templates
- test_search_trigger_exists

tests/unit/templates/test_navigation_trust.py:
- test_stage_1_sees_minimal_nav
- test_stage_2_sees_minimal_nav
- test_stage_3_sees_expanded_nav
- test_stage_4_sees_full_nav
- test_trust_context_passed_to_nav
```

### Integration Tests
Not required - template tests sufficient.

### Manual Testing Checklist
**Scenario 1**: New user (Stage 1) nav experience
1. [ ] Log in as new user
2. [ ] Verify nav shows only: Home, Search, User Menu
3. [ ] Verify "My Work" dropdown NOT visible
4. [ ] Verify home state is visually primary

**Scenario 2**: Trusted user (Stage 4) nav experience
1. [ ] Log in as trusted user
2. [ ] Verify full nav visible with all items
3. [ ] Verify items use natural language
4. [ ] Verify Cmd/Ctrl+K hint visible

---

## Success Metrics

### Quantitative
- All 5 phases complete with tests
- 10+ new unit tests passing
- 0 regressions in existing tests
- Nav loads in <50ms

### Qualitative
- Nav feels "supportive" not "prominent"
- Items describable as "Piper can help you..."
- Users don't default to browsing nav first
- Clear distinction from command palette

---

## STOP Conditions

**STOP immediately and escalate if**:
- Trust context not available in templates (blocks Phase 2)
- Accessibility degradation detected
- #419 HardnessLevel enum insufficient for nav visibility rules
- Navigation breaks on any of 17 templates
- Command palette (#421) scope conflicts discovered
- Tests fail for any reason

**When stopped**: Document the issue, provide options, wait for PM decision.

---

## Effort Estimate

**Overall Size**: Medium

**Breakdown by Phase**:
- Phase 0: Small (audit and planning)
- Phase 1: Small (label changes)
- Phase 2: Medium (trust integration)
- Phase 3: Small (CSS adjustments)
- Phase 4: Small (palette trigger)
- Phase Z: Small (documentation)

**Complexity Notes**:
- Trust context flow from #419 should make Phase 2 straightforward
- Vocabulary decisions may need PM input
- CSS changes low risk with careful testing

---

## Dependencies

### Required (Must be complete first)
- [x] #419 MUX-NAV-HOME (provides trust_stage context and HardnessLevel)

### Optional (Nice to have)
- [ ] #421 MUX-NAV-PALETTE (palette trigger placeholder can work without it)
- [ ] #684 MUX-NAV-PLACES (no direct dependency)

---

## Related Documentation

- **Architecture**: ADR-045 (Object Model), ADR-053 (Trust Computation)
- **Naming**: `docs/internal/architecture/current/naming-conventions-v1.md`
- **Philosophy**: `docs/internal/architecture/current/consciousness-philosophy.md`
- **Patterns**: ownership-metaphors.md (NATIVE/FEDERATED/SYNTHETIC)

---

## Evidence Section

[To be filled during implementation]

### Implementation Evidence
```bash
# Phase 0 evidence (audit results)
# Phase 1 evidence (vocabulary changes)
# Phase 2 evidence (trust-gated visibility)
# Phase 3 evidence (visual hierarchy)
# Phase 4 evidence (palette integration)
# Full test suite
```

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

## Design Principles (Preserved from Original)

### Navigation as Utility, Not Primary Experience
- Home state is the primary experience
- Navigation is the "filing cabinet in the corner" - available but not prominent
- Users shouldn't need nav for daily work once trust builds

### Preserve Consciousness Grammar
- Menu items should use natural language, not internal jargon
- Items should reflect "What can Piper help with?" not "What database tables exist?"
- Trust-gated visibility applies here too

### Progressive Disclosure
- Stage 1-2: Minimal nav, encourage home state learning
- Stage 3-4: Richer nav for power users who've earned trust

### Anti-Patterns to Avoid
- Nav that encourages "browsing" instead of asking Piper
- CRUD-style menu items ("View Tasks", "Manage Projects")
- Exposing internal vocabulary (Lenses, Moments, Places directly)

---

_Issue created: 2026-01-25_
_Last updated: 2026-01-25_
