# Gameplan: #424 MUX-IMPLEMENT-COMPOST

**Issue**: #424 MUX-IMPLEMENT-COMPOST: Composting Interface
**Date**: 2026-01-25
**Author**: Lead Developer (Claude Opus)

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI (confirmed)
- [x] Backend composting: `services/mux/composting_*.py` (complete)
- [x] InsightJournal: `services/mux/composting_pipeline.py` (complete)
- [x] Design specs: D2, D3 (CXO approved)
- [x] Trust-gating pattern: CSS classes + JavaScript (from #684)

**My understanding of the task**:
- Surface Piper's composting learnings through reflection summaries
- Create Insight Journal browser
- Implement control interface (correct, delete, reset) per D2 spec
- "Filing dreams" metaphor - processing during quiet hours
- No surveillance language

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**
- [ ] Multiple agents in parallel - No
- [x] Task duration >30 min - Yes
- [ ] Multi-component work - No
- [ ] Exploratory/risky - No, specs approved

**Assessment**: [ ] SKIP WORKTREE
**Rationale**: Single agent, clear D2/D3 specs, backend complete

### Part B: PM Verification Required

**What actually exists**:
```
services/mux/composting_models.py - Pattern, Insight, Correction, ExtractedLearning
services/mux/composting_pipeline.py - InsightJournal, CompostingPipeline
services/mux/compost_bin.py - CompostBin staging
services/mux/composting_scheduler.py - Quiet hours scheduling
D2 spec - Control interface patterns
D3 spec - Composting experience design
```

**Recent work**: Backend complete, D2/D3 CXO approved
**Actual task**: Create UI components following approved specs

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - Specs approved, backend complete

---

## Phase 0: Initial Bookending

### Required Actions

1. **GitHub Issue Verification**
   ```bash
   gh issue view 424
   ```

2. **Infrastructure Verification**
   ```bash
   # Verify InsightJournal API
   python -c "from services.mux.composting_pipeline import InsightJournal; print(dir(InsightJournal))"

   # Verify composting models
   python -c "from services.mux.composting_models import SurfaceableInsight; print(SurfaceableInsight.__annotations__)"

   # Run backend tests
   pytest tests/unit/services/mux/test_composting*.py -v --tb=short
   ```

3. **D2/D3 Spec Review**
   - Review D2 for control interface patterns
   - Review D3 for reflection openers, language patterns
   - Verify no surveillance language in specs

4. **Update GitHub Issue**
   - Mark Phase 0 checkboxes complete
   - Document any spec clarifications needed

### STOP Conditions
- D2/D3 specs unclear or conflicting
- Backend API changed from spec
- Composting tests failing

---

## Phase 1: Reflection Summary Component

### Objective
Morning/session-start reflection display with rotating openers.

### Agent Instructions

```markdown
## Task: Create Reflection Summary Component

**Issue**: #424 (Composting Interface)

### Context
- Display at session start for Stage 3+ users
- Rotating opener phrases (never formulaic)
- 2-4 insights per summary
- Confidence indicators per insight

### Files to Create
- `templates/components/reflection_summary.html`

### Reflection Openers (must rotate)
- "Having had some time to reflect..."
- "Looking back on our work together..."
- "Something occurred to me..."
- "I've been thinking about..."

### Acceptance Criteria
- [ ] Displays at session start
- [ ] Trust-gated: Stage 3+ only
- [ ] Opener rotates (never same twice in row)
- [ ] Shows 2-4 insights
- [ ] Each insight has confidence indicator
- [ ] "Not now" dismiss option
- [ ] ARIA live region for accessibility

### Confidence Display
- High (0.8+): No qualifier
- Medium (0.6-0.8): "I think..." or "It looks like..."
- Low (0.4-0.6): "I'm not sure, but..."

### Test Requirements
- 5+ tests
- Test opener rotation (no repeats)
- Test insight count limits
- Test confidence display
- Test trust-gating
- Test dismiss behavior

### Evidence Required
- Different openers on sequential renders
- Confidence language matches spec
- Test output

### STOP Conditions
- Surveillance language anywhere
- Opener feels formulaic
- More than 4 insights shown
```

### Deliverables
- `templates/components/reflection_summary.html`
- `tests/unit/templates/test_reflection_summary.py` (5+ tests)

---

## Phase 2: Insight Journal View

### Objective
Browsable collection of all learnings organized by topic.

### Agent Instructions

```markdown
## Task: Create Insight Journal Page

**Issue**: #424 (Composting Interface)

### Context
- Route: `/insights`
- Browse all learnings by topic
- Control actions: Correct, Delete, "Why?"
- Trust-gated visibility by insight confidence

### Files to Create/Modify
- `templates/insights.html` (NEW)
- `web/api/routes/ui.py` (add /insights route)

### Topic Organization
- Work Patterns
- Projects
- Preferences
- Relationships
- Scheduling

### Acceptance Criteria
- [ ] Page renders at /insights
- [ ] Topics displayed with insight counts
- [ ] Recency weighting within topics
- [ ] Control actions visible: Correct, Delete, "Why?"
- [ ] Empty state: "No insights yet - we'll learn together"
- [ ] Trust-gated visibility per insight

### Test Requirements
- 5+ tests
- Test route exists
- Test topic grouping
- Test control actions present
- Test empty state

### Evidence Required
- Page accessible at /insights
- Topics render correctly
- Test output

### STOP Conditions
- Technical organization (not topical)
- Surveillance language in UI
- Control actions feel "bureaucratic"
```

### Deliverables
- `templates/insights.html`
- Route in `web/api/routes/ui.py`
- `tests/unit/templates/test_insights_page.py` (5+ tests)

---

## Phase 3: Individual Insight Card

### Objective
Expanded view of single insight with controls.

### Agent Instructions

```markdown
## Task: Create Insight Detail Card

**Issue**: #424 (Composting Interface)

### Context
- Modal or expandable card
- Shows type, confidence, source count
- Shows narrative explanation
- Control actions: Correct, Delete, Confirm

### Files to Create
- `templates/components/insight_card.html`

### Confidence Language
- High (0.8+): "I've noticed that..." (no qualifier)
- Medium (0.6-0.8): "I think..." or "It looks like..."
- Low (0.4-0.6): "I'm not sure, but..."

### Acceptance Criteria
- [ ] Shows insight type
- [ ] Shows confidence with appropriate language
- [ ] Shows source count ("based on 3 observations")
- [ ] Shows narrative explanation
- [ ] Correct action opens correction flow
- [ ] Delete action opens confirmation
- [ ] Confirm action ("That's right") reinforces insight
- [ ] ARIA labels for actions

### Test Requirements
- 5+ tests
- Test confidence language selection
- Test action buttons present
- Test narrative display

### Evidence Required
- Card renders correctly
- Confidence language matches spec
- Test output

### STOP Conditions
- Technical confidence numbers shown (not language)
- Actions feel "bureaucratic"
```

### Deliverables
- `templates/components/insight_card.html`
- `tests/unit/templates/test_insight_card.py` (5+ tests)

---

## Phase 4: Control Interface (D2 Compliance)

### Objective
Implement correction, deletion, and reset flows per D2 spec.

### Agent Instructions

```markdown
## Task: Implement D2 Control Flows

**Issue**: #424 (Composting Interface)

### Context
- D2 spec is CXO approved - must follow exactly
- No arguing with corrections
- Deletion is permanent
- Reset requires "RESET" confirmation

### Correction Flow
1. User clicks "Correct"
2. Input field appears
3. User enters correction
4. Show before/after
5. "Thanks, I'll remember that"

### Deletion Flow
1. User clicks "Delete"
2. Confirmation: "This will permanently remove this insight. Continue?"
3. User confirms
4. "Got it, that's gone"

### Reset Flow
1. User accesses reset option
2. Shows list of what will be deleted
3. "Type RESET to confirm"
4. User types exactly "RESET"
5. "Starting fresh"

### Acceptance Criteria
- [ ] Correction shows before/after
- [ ] No argument/guilt on correction ("Thanks, I'll remember that")
- [ ] Deletion is permanent (no soft delete)
- [ ] Deletion confirms before action
- [ ] Reset requires typing "RESET" exactly
- [ ] Reset shows what will be deleted
- [ ] No guilt language anywhere

### Test Requirements
- 5+ tests
- Test correction flow completes
- Test deletion is permanent
- Test reset requires exact word
- Test no guilt language

### Evidence Required
- Each flow works end-to-end
- No guilt/argument in any message
- Test output

### STOP Conditions
- User feels guilted about corrections/deletions
- Deletion not permanent
- Reset doesn't require exact "RESET"
- Any arguing with user
```

### Deliverables
- Control flow implementations in components
- `tests/unit/templates/test_insight_controls.py` (5+ tests)

---

## Phase 5: Composting Status (Optional)

### Objective
Transparency about what's being processed.

### Agent Instructions

```markdown
## Task: Add Composting Status Query

**Issue**: #424 (Composting Interface)

### Context
- Optional but valuable for transparency
- "What are you reflecting on?" query
- Shows queue count and next scheduled time

### Acceptance Criteria
- [ ] Query "What are you reflecting on?" works
- [ ] Shows items in composting queue (count only)
- [ ] Shows next scheduled composting time
- [ ] No over-detail (not "3 tasks from yesterday")

### Test Requirements
- 2-3 tests
- Test query response
- Test queue count display

### Evidence Required
- Query works
- Appropriate level of detail

### STOP Conditions
- Over-detailed attribution
- Feels like surveillance
```

### Deliverables
- Status query handler integration
- Tests (2-3)

---

## Phase Z: Final Bookending & Handoff

### Required Actions

1. **Evidence Compilation**
   ```bash
   # Run all #424-specific tests
   pytest tests/unit/templates/test_reflection_summary.py tests/unit/templates/test_insights_page.py tests/unit/templates/test_insight_card.py tests/unit/templates/test_insight_controls.py -v

   # Run full test suite
   pytest tests/unit/ -v --tb=short
   ```

2. **D2/D3 Compliance Check**
   - Verify no surveillance language
   - Verify no guilt on user actions
   - Verify reflection feels natural

3. **GitHub Issue Update**
   - Fill completion matrix with evidence
   - Mark all acceptance criteria
   - Update status to "Complete - Awaiting PM Review"

4. **Session Log Update**
   - Document all files created/modified
   - Include test counts
   - Note any D2/D3 clarifications

### Success Criteria
- [ ] All acceptance criteria met
- [ ] 25+ tests passing
- [ ] D2/D3 compliance verified
- [ ] No regressions
- [ ] Evidence provided

---

## Multi-Agent Coordination

### Deployment Map

| Phase | Type | Work | Evidence |
|-------|------|------|----------|
| 1 | Sequential | Reflection summary | 5+ tests |
| 2 | Sequential | Insight Journal | 5+ tests |
| 3 | Sequential | Insight card | 5+ tests |
| 4 | Sequential | Control flows | 5+ tests |
| 5 | Sequential | Status (optional) | 2-3 tests |
| Z | Sequential | Final verification | Full suite |

**Note**: Single agent sequential work - D2/D3 compliance requires careful attention.

---

## Verification Gates

- [ ] Phase 1: Reflection openers rotate, no surveillance language
- [ ] Phase 2: Journal organizes by topic correctly
- [ ] Phase 3: Confidence language matches spec
- [ ] Phase 4: All control flows work, no guilt
- [ ] Phase 5: Status doesn't over-detail (optional)
- [ ] Phase Z: Full suite 0 regressions, D2/D3 compliance verified

---

## STOP Conditions (Apply Throughout)

- Surveillance language detected ("monitoring", "observed", "tracking")
- Guilt language detected ("you didn't", "you should have")
- Over-detailed attribution ("at 2:15 PM on Tuesday")
- Real-time learning notifications (learning should be invisible until reflection)
- Deletion feels recoverable (must be permanent)
- Tests fail for any reason

---

## Cross-References

- **#684**: Trust-gating pattern source
- **#421**: Command palette pattern
- **#423**: COMPOSTED stage visualization (lifecycle)
- **D2**: Control Interface Patterns (source of truth for flows)
- **D3**: Composting Experience Design (source of truth for language)
- **services/mux/composting_pipeline.py**: Backend source of truth

---

## Language Patterns (from D3)

### Reflection Openers (rotate)
- "Having had some time to reflect..."
- "Looking back on our work together..."
- "Something occurred to me..."
- "I've been thinking about..."

### Temporal Framing (Good)
- "Looking back at last week..."
- "Thinking about how that project went..."
- "In hindsight..."

### Temporal Framing (Bad - NEVER use)
- "I noticed you doing X yesterday..."
- "While you were working, I saw..."
- "I've been tracking..."

### Control Acknowledgments (D2)
- Correction: "Thanks, I'll remember that"
- Deletion: "Got it, that's gone"
- Reset: "Starting fresh"

---

## Anti-Patterns to Avoid (from issue)

1. **Real-time learning notifications**: Learning invisible until reflection
2. **Surveillance language**: No "monitoring", "observed", "tracking"
3. **Over-detailed attribution**: No "at 2:15 PM on Tuesday"
4. **Guilt-inducing reflection**: No "you didn't follow through"
5. **Arguing with corrections**: User's statement is authoritative

---

## Audit Notes

This gameplan follows gameplan-template.md v9.3:
- [x] Phase -1 Infrastructure Verification
- [x] Phase 0 Initial Bookending
- [x] Phases 1-5 Development Work
- [x] Phase Z Final Bookending
- [x] Multi-Agent Coordination
- [x] STOP Conditions
- [x] Evidence Requirements

---

_Gameplan created: 2026-01-25_
