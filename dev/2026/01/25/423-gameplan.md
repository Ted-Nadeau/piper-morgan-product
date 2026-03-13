# Gameplan: #423 MUX-IMPLEMENT-LIFECYCLE

**Issue**: #423 MUX-IMPLEMENT-LIFECYCLE: Object Lifecycle Visualization
**Date**: 2026-01-25
**Author**: Lead Developer (Claude Opus)

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI (confirmed)
- [x] Backend lifecycle: `services/mux/lifecycle.py` (complete, 53 tests)
- [x] Experience phrases: lifecycle-experience-guide.md (verified)
- [x] Place window pattern: `templates/components/place_window.html` (from #684)
- [x] Command palette: `templates/components/command_palette.html` (from #421)
- [x] Trust-gating pattern: CSS classes + JavaScript (from #684)

**My understanding of the task**:
- Visualize 8-stage lifecycle model using experience phrases (not technical labels)
- Backend is complete - this is UI only
- Lifecycle indicator for objects, journey view for detail
- Stage filtering via command palette

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**
- [ ] Multiple agents in parallel - No
- [x] Task duration >30 min - Yes
- [ ] Multi-component work - No
- [ ] Exploratory/risky - No, backend proven with 53 tests

**Assessment**: [ ] SKIP WORKTREE
**Rationale**: Single agent, backend complete, clear specifications

### Part B: PM Verification Required

**What actually exists**:
```
services/mux/lifecycle.py - 8 states, experience phrases, 53 tests
services/mux/lifecycle_integration.py - Handler helpers
lifecycle-experience-guide.md - Experience phrase reference
templates/components/place_window.html - Component pattern
templates/components/command_palette.html - Filter command pattern
```

**Recent work**: 53 backend tests passing, experience phrases defined
**Actual task**: Create UI components to surface backend functionality

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - Backend complete, specifications clear

---

## Phase 0: Initial Bookending

### Required Actions

1. **GitHub Issue Verification**
   ```bash
   gh issue view 423
   ```

2. **Infrastructure Verification**
   ```bash
   # Verify lifecycle.py API
   python -c "from services.mux.lifecycle import LifecycleState; print([s.value for s in LifecycleState])"

   # Verify experience phrases exist
   grep -n "experience_phrase" services/mux/lifecycle.py | head -5

   # Run backend tests
   pytest tests/unit/services/mux/test_lifecycle.py -v --tb=short
   ```

3. **Experience Phrase Verification**
   Verify these match `lifecycle-experience-guide.md`:

   | Stage | Expected Phrase |
   |-------|-----------------|
   | EMERGENT | "I just noticed..." |
   | DERIVED | "I figured out from..." |
   | NOTICED | "I'm aware of..." |
   | PROPOSED | "I think we should..." |
   | RATIFIED | "We're doing..." |
   | DEPRECATED | "This used to be..." |
   | ARCHIVED | "I remember when..." |
   | COMPOSTED | "I learned that..." |

4. **Update GitHub Issue**
   - Mark Phase 0 checkboxes complete
   - Document any phrase mismatches

### STOP Conditions
- Experience phrases don't match guide
- Backend API changed
- Lifecycle tests failing

---

## Phase 1: Lifecycle Indicator Component

### Objective
Create compact, reusable indicator showing object's lifecycle stage with experience phrase.

### Agent Instructions

```markdown
## Task: Create Lifecycle Indicator Component

**Issue**: #423 (Object Lifecycle Visualization)

### Context
- Compact indicator showing lifecycle stage
- Uses experience phrases (not technical labels like "EMERGENT")
- 8 stages, each with semantic color
- Supports compact mode (dot) and expanded mode (dot + phrase)

### Files to Create
- `templates/components/lifecycle_indicator.html`

### Stage Colors (semantic)
- EMERGENT: #bfdbfe (soft blue) - forming
- DERIVED: #ddd6fe (light purple) - connected
- NOTICED: #fef08a (yellow) - attention
- PROPOSED: #fed7aa (orange) - action needed
- RATIFIED: #bbf7d0 (green) - active
- DEPRECATED: #e5e7eb (gray) - inactive
- ARCHIVED: #f3f4f6 (light gray) - reference
- COMPOSTED: #fde68a (warm gold) - transformed

### Acceptance Criteria
- [ ] Renders all 8 stages with correct colors
- [ ] Experience phrase as tooltip (never technical label)
- [ ] Compact mode: colored dot only
- [ ] Expanded mode: dot + experience phrase text
- [ ] data-lifecycle-stage attribute
- [ ] ARIA labels for accessibility
- [ ] JavaScript API: LifecycleIndicator.create(stage), update(stage)

### Test Requirements
- 8+ unit tests in `tests/unit/templates/test_lifecycle_indicator.py`
- One test per stage (color, phrase, aria)
- Test compact vs expanded mode

### Evidence Required
- All 8 stages render correctly
- Experience phrases match backend exactly
- Test output showing all tests pass

### STOP Conditions
- Phrase mismatch with backend
- Color fails contrast requirements
- Technical labels appear anywhere
```

### Deliverables
- `templates/components/lifecycle_indicator.html`
- `tests/unit/templates/test_lifecycle_indicator.py` (8+ tests)

---

## Phase 2: Lifecycle Detail Card

### Objective
Expanded view showing object's journey through stages.

### Agent Instructions

```markdown
## Task: Create Lifecycle Detail Card

**Issue**: #423 (Object Lifecycle Visualization)

### Context
- Expandable card showing lifecycle journey
- Shows current stage highlighted
- Shows past stages with dates
- Future stages grayed out
- Forward-looking message for active items

### Files to Create
- `templates/components/lifecycle_detail.html`

### Acceptance Criteria
- [ ] Journey timeline shows all 8 stages
- [ ] Current stage highlighted with experience phrase
- [ ] Past stages shown with transition dates
- [ ] Future stages grayed (not selectable)
- [ ] Forward-looking message: "What's next: [next stage phrase]"
- [ ] ARIA labels for timeline navigation

### Test Requirements
- 5+ unit tests
- Test current stage highlighting
- Test past/future stage styling
- Test forward-looking message

### Evidence Required
- Journey renders correctly for different stages
- Test output

### STOP Conditions
- Timeline not linear (must show forward-only)
- Future stages look selectable
```

### Deliverables
- `templates/components/lifecycle_detail.html`
- Tests added to test_lifecycle_indicator.py (5+ tests)

---

## Phase 3: Stage Filtering

### Objective
Let users filter/find objects by lifecycle stage via command palette.

### Agent Instructions

```markdown
## Task: Add Stage Filter Commands

**Issue**: #423 (Object Lifecycle Visualization)

### Context
- Add commands to command palette from #421
- One command per stage that makes sense to filter
- Badge counts in nav (Stage 4+ only)

### Files to Modify
- `templates/components/command_palette.html`

### Commands to Add
- "Show emergent items" - Items just noticed
- "Show proposed items" - Items needing decision
- "Show active items" - RATIFIED items
- "Show archived items" - Reference items
- "Show composted learnings" - Insights gained

### Acceptance Criteria
- [ ] Commands appear in palette
- [ ] Commands filter relevant views
- [ ] Hardness appropriate per command
- [ ] Natural language (not "Show EMERGENT")

### Test Requirements
- 3+ tests
- Test commands exist
- Test filter execution

### Evidence Required
- Commands visible in palette
- Filter works correctly

### STOP Conditions
- Technical labels in commands
- Filtering breaks existing functionality
```

### Deliverables
- Updated command_palette.html
- Tests (3+)

---

## Phase 4: Transition Notifications

### Objective
Notify users when objects transition (Stage 3+ only).

### Agent Instructions

```markdown
## Task: Create Transition Notification Component

**Issue**: #423 (Object Lifecycle Visualization)

### Context
- Notify when lifecycle changes
- Use transition explanations from lifecycle.py
- Trust-gated: Stage 3+ only
- Must feel natural, not system-y

### Files to Create
- `templates/components/lifecycle_notification.html`

### Notification Format
"[Object name] moved from [old phrase] to [new phrase]"
Example: "Sprint planning moved from 'I think we should...' to 'We're doing...'"

### Acceptance Criteria
- [ ] Notification appears on transition
- [ ] Uses experience phrases (not technical stages)
- [ ] Trust-gated: only Stage 3+
- [ ] Auto-dismiss after 5 seconds
- [ ] Can be manually dismissed
- [ ] ARIA live region for accessibility

### Test Requirements
- 3+ tests
- Test notification appears
- Test trust-gating
- Test auto-dismiss

### Evidence Required
- Notification appears correctly
- Trust-gating works
- Test output

### STOP Conditions
- Technical language in notifications
- Notifications feel "system" not "colleague"
```

### Deliverables
- `templates/components/lifecycle_notification.html`
- Tests (3+)

---

## Phase Z: Final Bookending & Handoff

### Required Actions

1. **Evidence Compilation**
   ```bash
   # Run all #423-specific tests
   pytest tests/unit/templates/test_lifecycle_*.py -v

   # Run full test suite
   pytest tests/unit/ -v --tb=short
   ```

2. **Experience Phrase Verification**
   ```bash
   # Verify all 8 phrases render correctly
   # Manual verification needed
   ```

3. **GitHub Issue Update**
   - Fill completion matrix with evidence
   - Mark all acceptance criteria
   - Update status to "Complete - Awaiting PM Review"

4. **Session Log Update**
   - Document all files created/modified
   - Include test counts
   - Note any phrase adjustments

### Success Criteria
- [ ] All 8 stages render correctly
- [ ] Experience phrases match backend exactly
- [ ] 20+ tests passing
- [ ] No regressions
- [ ] Evidence provided

---

## Multi-Agent Coordination

### Deployment Map

| Phase | Type | Work | Evidence |
|-------|------|------|----------|
| 1 | Sequential | Indicator component | 8+ tests |
| 2 | Sequential | Detail card | 5+ tests |
| 3 | Sequential | Filter commands | 3+ tests |
| 4 | Sequential | Notifications | 3+ tests |
| Z | Sequential | Final verification | Full suite |

**Note**: Single agent sequential work - phases depend on Phase 1 component.

---

## Verification Gates

- [ ] Phase 1: All 8 stages render with correct phrases
- [ ] Phase 2: Journey view shows timeline correctly
- [ ] Phase 3: Filter commands work
- [ ] Phase 4: Notifications trust-gated correctly
- [ ] Phase Z: Full suite 0 regressions

---

## STOP Conditions (Apply Throughout)

- Experience phrases don't match backend/guide
- Technical labels appear anywhere in UI
- Colors fail contrast requirements
- Lifecycle feels like "status tracking" not "consciousness"
- Tests fail for any reason

---

## Cross-References

- **#684**: Place window pattern source
- **#421**: Command palette pattern
- **#422**: Documents will use lifecycle indicator
- **#424**: COMPOSTED stage detail (composting interface)
- **lifecycle-experience-guide.md**: Experience phrase source of truth
- **services/mux/lifecycle.py**: Backend source of truth

---

## Design Principles (from issue)

### The Contractor Test
Every phrase must pass: "Would a colleague say this naturally?"
- "I just noticed this task needs attention"
- NOT: "I sense something forming"

### Forward-Only Movement
Lifecycle states only move forward. Error messages explain naturally:
- "I can't go back to that state - things only move forward"

### First-Person Perspective
All phrases use "I" or "We":
- "I just noticed..." (EMERGENT)
- "We're doing..." (RATIFIED)
- "I learned that..." (COMPOSTED)

---

## Audit Notes

This gameplan follows gameplan-template.md v9.3:
- [x] Phase -1 Infrastructure Verification
- [x] Phase 0 Initial Bookending
- [x] Phases 1-4 Development Work
- [x] Phase Z Final Bookending
- [x] Multi-Agent Coordination
- [x] STOP Conditions
- [x] Evidence Requirements

---

_Gameplan created: 2026-01-25_
