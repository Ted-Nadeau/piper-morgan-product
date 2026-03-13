# Gameplan: #420 MUX-NAV-UTILITY - Navigation Utility Layer

**Issue**: #420
**Priority**: P1
**Sprint**: P1 (Navigation Paradigm)
**Epic**: #418 MUX-IMPLEMENT
**Created**: 2026-01-25

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI (confirmed)
- [x] Template engine: Jinja2 (confirmed)
- [x] Database: PostgreSQL on 5433 (confirmed)
- [x] Testing framework: pytest (confirmed)
- [x] Existing nav: `templates/components/navigation.html` (~730 lines)
- [x] Trust context: Available from #419 implementation

**My understanding of the task**:
- I believe we need to: Refactor existing nav from "browse app" to "utility layer"
- I think this involves: Vocabulary changes, trust-gated visibility, visual hierarchy
- I assume the current state is: Nav works but uses database-style labels and no trust awareness

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

Worktrees ADD value when:
- [ ] Multiple agents will work in parallel on different files/features
- [ ] Task duration >30 minutes (main branch may advance)
- [ ] Multi-component work (e.g., frontend + backend by different agents)
- [ ] Exploratory/risky changes where easy rollback is valuable
- [ ] Coordination queue prompt being claimed

Worktrees ADD overhead when:
- [x] Single agent, sequential work
- [ ] Small fixes (<15 min)
- [x] Tightly coupled files requiring atomic commits
- [ ] Time-critical work where setup overhead matters

**Assessment:**
- [x] **SKIP WORKTREE** - Single Lead Dev, template refactoring work
- Document rationale: Single agent, tightly coupled template/CSS changes, sequential phases

### Part B: PM Verification Required

**PM, please correct/confirm the above and provide**:

1. **What actually exists in the filesystem?**
   ```bash
   # Navigation component
   ls -la templates/components/navigation.html
   # Expected: ~730 line nav component

   # Trust context from #419
   grep -n "trust_stage" web/api/routes/ui.py
   # Expected: trust_stage passed to templates
   ```

2. **Recent work in this area?**
   - Last changes: #419 added trust_stage to home route
   - Known issues: Nav labels are database-style (vibe coded)
   - Previous attempts: None for trust-gated nav

3. **Actual task needed?**
   - [ ] Create new feature from scratch
   - [x] Add to existing application (refactor nav)
   - [ ] Fix broken functionality
   - [x] Refactor existing code

4. **Critical context I'm missing?**
   - None identified

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - Understanding is correct
- [ ] **REVISE** - Major assumptions wrong
- [ ] **CLARIFY** - Need more context

---

## Phase 0: Initial Bookending - GitHub Investigation

### Required Actions

1. **GitHub Issue Verification**
   ```bash
   gh issue view 420
   ```
   - Issue exists with restructured content ✅

2. **Codebase Investigation**
   ```bash
   # Check current nav items
   grep -n "dropdown\|nav-item" templates/components/navigation.html | head -20

   # Check where nav is used
   grep -r "navigation.html" templates/ --include="*.html" | wc -l

   # Check trust_stage availability
   grep -n "trust_stage" web/api/routes/ui.py
   ```

3. **Current Nav Item Audit**
   Document current labels vs consciousness grammar:
   | Current Label | Consciousness Grammar | Hardness |
   |---------------|----------------------|----------|
   | My Work | "What I'm tracking" | HARD |
   | Todos | "Things to do" | HARD |
   | Projects | "What you're working on" | HARD |
   | Files | "Documents" | HARD |
   | Lists | "Collections" | HARD |
   | Learning | "What Piper knows" | MEDIUM |

4. **Update GitHub Issue**
   ```bash
   gh issue edit 420 --body "Status: Investigation Started"
   ```

### STOP Conditions Check
- [x] Issue exists: #420 confirmed
- [x] Feature to refactor exists: navigation.html confirmed
- [x] Dependencies met: #419 complete

---

## Phase 0.5: Frontend-Backend Contract Verification

### When to Apply
- [ ] Creating new API endpoints + UI that calls them - NO
- [ ] Modifying existing API paths - NO
- [x] Template changes using existing context - YES

### Required Actions

#### 1. Verify trust_stage Available in Templates
```bash
# Check trust_stage passed to templates
grep -n "trust_stage" web/api/routes/ui.py | head -5

# Check which templates get trust_stage
grep -rn "trust_stage" templates/ --include="*.html" | head -10
```

#### 2. Template Context Verification
Nav component needs trust_stage in context to implement trust-gated visibility.
Verify home route passes trust_stage (from #419).

### STOP Conditions
- [ ] If trust_stage not available in template context → escalate (#419 incomplete)

---

## Phase 0.6: Data Flow & Integration Verification

### Part A: Data Flow Requirements

#### Trust Context Propagation

| Layer | Needs trust_stage? | Source |
|-------|-------------------|--------|
| Home route | [x] Yes | TrustComputationService (from #419) |
| Template context | [x] Yes | Passed from route |
| Navigation component | [x] Yes | Included from template |

**Verification Commands**:
```bash
# Check route passes trust_stage
grep -A 5 "return templates.TemplateResponse" web/api/routes/ui.py | head -10
```

### Part B: Integration Points Checklist

| Caller | Callee | Verified? |
|--------|--------|-----------|
| ui.py home route | navigation.html include | [x] |
| navigation.html | trust_stage context | [ ] (to verify) |

### STOP Conditions
- [ ] If navigation component can't access trust_stage → fix include pattern

---

## Phase 0.7: Conversation Design

**Not applicable** - This is template/UI work, not a conversational feature.

---

## Phase 0.8: Post-Completion Integration

### When to Apply
- [ ] Features that change user state - NO
- [ ] Features that create/modify database records - NO
- [x] Features that should affect other feature behavior - YES (nav appearance)

### Downstream Behavior Changes

| Feature | Before Completion | After Completion |
|---------|-------------------|------------------|
| Navigation | Same for all users | Trust-gated visibility |
| Item labels | Database-style | Natural language |
| Visual hierarchy | Nav prominent | Home state primary |

---

## Phase 1: Item Vocabulary Refactor

### Objective
Replace database-style labels with consciousness grammar.

### Deploy: Lead Developer (Single Agent)

### Tasks
- [ ] Audit current nav item labels
- [ ] Design new vocabulary using naming-conventions-v1
- [ ] Ensure all items pass anti-flattening test
- [ ] Update navigation.html with new labels
- [ ] Write tests for nav content

### Vocabulary Mapping
| Current | Proposed | Anti-Flattening Test |
|---------|----------|---------------------|
| My Work | "Your stuff" or remove | "Piper tracks your..." ✅ |
| Todos | "Things to do" | "Piper helps you with..." ✅ |
| Projects | "What you're working on" | "Piper knows about..." ✅ |
| Files | "Documents" | "Piper has access to..." ✅ |
| Lists | "Collections" | "Piper organizes..." ✅ |
| Standup | "Morning briefing" | "Piper prepares..." ✅ |
| Learning | "What Piper knows" | "Piper has learned..." ✅ |

### Verification Commands
```bash
# Check labels updated
grep -n "nav-item\|dropdown-item" templates/components/navigation.html | head -20

# Run label tests
python -m pytest tests/unit/templates/test_navigation.py -v
```

### Evidence Required
- [ ] Before/after nav item labels
- [ ] Anti-flattening test results
- [ ] Test output

---

## Phase 2: Trust-Gated Visibility

### Objective
Show/hide nav items based on trust stage.

### Deploy: Lead Developer (Single Agent)

### Tasks
- [ ] Ensure trust_stage available in nav template context
- [ ] Implement Jinja conditionals for trust-gated items
- [ ] Stage 1-2: Show only Home, Search, User Menu
- [ ] Stage 3-4: Show additional items progressively
- [ ] Write tests for trust-gated visibility

### Trust-Visibility Matrix
| Item | Stage 1 | Stage 2 | Stage 3 | Stage 4 |
|------|---------|---------|---------|---------|
| Home | ✅ | ✅ | ✅ | ✅ |
| Search | ✅ | ✅ | ✅ | ✅ |
| User Menu | ✅ | ✅ | ✅ | ✅ |
| "Your stuff" | ❌ | ❌ | ✅ | ✅ |
| Standup | ❌ | ❌ | ✅ | ✅ |
| Learning | ❌ | ❌ | ❌ | ✅ |

### Verification Commands
```bash
# Check trust conditionals in template
grep -n "trust_stage" templates/components/navigation.html

# Run trust visibility tests
python -m pytest tests/unit/templates/test_navigation_trust.py -v
```

### Evidence Required
- [ ] Trust conditionals in template
- [ ] Test output for all 4 trust stages

---

## Phase 3: Visual Hierarchy Adjustment

### Objective
Position nav as secondary to home state.

### Deploy: Lead Developer (Single Agent)

### Tasks
- [ ] Reduce nav visual prominence
- [ ] Ensure home state clearly primary
- [ ] CSS modifications for subtlety
- [ ] Verify accessibility maintained

### CSS Changes
- Reduce nav item font size slightly
- Reduce contrast for secondary items
- Add visual indicator that home is primary
- Maintain WCAG AA contrast minimums

### Verification Commands
```bash
# Check CSS changes
grep -n "navigation\|nav-item" web/static/css/*.css

# Manual: Visual inspection of hierarchy
```

### Evidence Required
- [ ] CSS modifications
- [ ] Accessibility check (contrast ratios)

---

## Phase 4: Command Palette Integration Points

### Objective
Clarify nav vs palette usage.

### Deploy: Lead Developer (Single Agent)

### Tasks
- [ ] Add keyboard shortcut hint (Cmd/Ctrl+K)
- [ ] Add search trigger that invokes palette (or placeholder)
- [ ] Document intended usage pattern
- [ ] Ensure no duplication between nav and palette

### Verification Commands
```bash
# Check keyboard shortcut hint
grep -n "Cmd\|Ctrl\|keyboard" templates/components/navigation.html
```

### Evidence Required
- [ ] Shortcut hint visible
- [ ] Usage pattern documented

---

## Phase Z: Final Bookending & Handoff

### Required Actions

#### 1. Full Test Suite Verification
```bash
# Run all nav-related tests
python -m pytest tests/unit/templates/test_navigation*.py -v

# Run full unit test suite
python -m pytest tests/unit/ -v --tb=line | tail -20
```

#### 2. Acceptance Criteria Verification

**Functionality**
- [ ] Nav items use natural language
- [ ] Trust-gated visibility working
- [ ] Home link prominent
- [ ] Search trigger exists
- [ ] All items pass anti-flattening test
- [ ] Nav available on all 17 templates

**Testing**
- [ ] Unit tests for nav content
- [ ] Unit tests for trust-gated visibility
- [ ] Accessibility tests
- [ ] Full suite passes

**Quality**
- [ ] No regressions
- [ ] Visual hierarchy supports home-state-first
- [ ] Anti-flattening test passes
- [ ] Accessibility maintained

**Documentation**
- [ ] Vocabulary mapping documented
- [ ] Usage pattern documented
- [ ] Session log complete

#### 3. GitHub Final Update
```bash
gh issue edit 420 --body "
## Status: Complete - Awaiting PM Approval

### Evidence Summary
- [x] All acceptance criteria met
- [x] Tests passing: [evidence]
- [x] No regressions: [evidence]

### Ready for PM Review
"
```

---

## Multi-Agent Coordination Plan

### Agent Deployment Map

| Phase | Agent Type | Issue | Evidence Required | Handoff |
|-------|------------|-------|------------------|---------|
| 1-4 | Lead Developer | #420 | Tests, modified files | Phase Z |
| Z | Lead Developer | #420 | Full verification | PM Review |

**Single agent justified**: Sequential template refactoring, tightly coupled changes.

### Verification Gates
- [ ] Phase 1: Vocabulary tests passing
- [ ] Phase 2: Trust visibility tests passing
- [ ] Phase 3: Accessibility maintained
- [ ] Phase 4: Palette integration clear
- [ ] Phase Z: Full suite, no regressions

---

## STOP Conditions (Apply Throughout)

Stop immediately and escalate if:
- Trust context not available in templates
- Accessibility degradation detected
- Navigation breaks on any template
- Tests fail for any reason
- #421 scope conflict discovered
- Visual hierarchy undermines home state

---

## Success Criteria

### Issue Completion Requires
- [ ] All acceptance criteria met
- [ ] Evidence provided for each criterion
- [ ] Tests passing (with output)
- [ ] 10+ new unit tests
- [ ] No regressions
- [ ] Documentation updated
- [ ] GitHub issue fully updated
- [ ] PM approval received

---

## Notes

### Dependency on #419
- trust_stage context must be available in templates
- HardnessLevel enum provides visibility framework
- Home state is established as primary experience

### Vocabulary Decisions
May need PM input on specific label choices during Phase 1.

---

*Gameplan created: 2026-01-25*
*Template version: v9.3*
