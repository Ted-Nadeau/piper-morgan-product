# Lead Developer Prompt: #420 MUX-NAV-UTILITY Implementation

## Your Identity
You are the Lead Developer (Claude Code), implementing #420 MUX-NAV-UTILITY - Navigation Utility Layer. You follow systematic methodology and provide evidence for all claims.

## Essential Context
- **GitHub Issue**: #420 MUX-NAV-UTILITY - Navigation Utility Layer
- **Current State**: Nav exists but uses database-style labels, no trust awareness
- **Target State**: Trust-gated, natural language nav that supports home state paradigm
- **Dependencies**: #419 (COMPLETE - provides trust_stage context)
- **User Data Risk**: None - UI refactoring
- **Infrastructure Verified**: Yes (Phase -1 gameplan)

---

## CRITICAL: Evidence and Handoff Requirements

### Acceptance Criteria (from issue)

**Functionality**
- [ ] Nav items use natural language (not database table names)
- [ ] Trust-gated visibility working (Stage 1-2 minimal, Stage 3-4 full)
- [ ] Home link prominent; other items secondary
- [ ] Search trigger invokes command palette (or placeholder for #421)
- [ ] All nav items pass anti-flattening test
- [ ] Nav available on all 17 current templates

**Testing**
- [ ] Unit tests for nav item content
- [ ] Unit tests for trust-gated visibility
- [ ] Accessibility tests (keyboard nav, ARIA)
- [ ] Full unit test suite passes with no regressions

**Quality**
- [ ] No regressions introduced
- [ ] Visual hierarchy supports home-state-first paradigm
- [ ] Anti-flattening test: All items describable as "Piper can help you..."
- [ ] Accessibility maintained (WCAG 2.1 AA)

**Documentation**
- [ ] Vocabulary mapping documented
- [ ] Usage pattern documented (when to use nav vs palette)
- [ ] Session log documents design decisions

### Handoff Format Required
```markdown
## Issue #420 Completion Report
**Status**: Complete/Partial/Blocked

**Tests**:
- X tests added in [location]
- `pytest [path] -v` output: [paste actual output]

**Verification**:
[Actual command output showing success]

**Files Modified**:
- [file1] (+X/-Y lines)
- [file2] (+X/-Y lines)

**User Testing Steps**:
1. [Step 1]
2. [Step 2]
3. [Expected result]

**Blockers** (if any):
- [Blocker description]
```

---

## Mission
Refactor navigation from "browse Piper like an app" to utility layer that supports home state without undermining colleague paradigm.

**Scope Boundaries**:
- This prompt covers: Phases 1-4 + Z from gameplan
- NOT in scope: #419 (done), #421 (separate), #684 (separate)

---

## Infrastructure Verification (MANDATORY FIRST ACTION)

```bash
# 1. Verify nav component exists
ls -la templates/components/navigation.html
# Expected: ~730 line file

# 2. Verify trust_stage available from #419
grep -n "trust_stage" web/api/routes/ui.py
# Expected: trust_stage in template context

# 3. Check current nav item labels
grep -n "dropdown\|nav-item" templates/components/navigation.html | head -20

# 4. Check where nav is included
grep -r "navigation.html" templates/ --include="*.html" | wc -l
# Expected: ~17 templates
```

**If infrastructure differs from expected**: STOP and document gaps.

---

## Phase 0: Mandatory Verification

```bash
# 1. GitHub issue exists
gh issue view 420

# 2. Check #419 complete (dependency)
gh issue view 419 --json state | jq -r '.state'
# Expected: OPEN (waiting for PM review) or CLOSED

# 3. Check trust_stage is passed to templates
grep -A 20 "def home" web/api/routes/ui.py | grep "trust_stage"

# 4. Check naming conventions doc exists
ls -la docs/internal/architecture/current/naming-conventions-v1.md
```

---

## Implementation Approach

### Step 1: Audit Current Nav Items

**Expected Files**:
- `templates/components/navigation.html`

**Verification**:
```bash
# Extract current nav item labels
grep -n "dropdown-item\|nav-link" templates/components/navigation.html | head -30
```

**Evidence Required**:
- [ ] Current nav items documented
- [ ] Anti-flattening assessment for each

### Step 2: Implement Vocabulary Refactor (Phase 1)

**Vocabulary Mapping**:
| Current | Proposed | Anti-Flattening |
|---------|----------|-----------------|
| My Work | Remove or "Your stuff" | "Piper tracks your..." ✅ |
| Todos | "Things to do" | "Piper helps you with..." ✅ |
| Projects | "What you're working on" | "Piper knows about..." ✅ |
| Files | "Documents" | "Piper has access to..." ✅ |
| Lists | "Collections" | "Piper organizes..." ✅ |

**Implementation**:
```bash
# Modify navigation.html with new labels
# Update dropdown text
# Ensure aria-labels updated too
```

**Evidence Required**:
- [ ] Before/after nav labels
- [ ] Modified navigation.html

### Step 3: Implement Trust-Gated Visibility (Phase 2)

**Trust-Visibility Matrix**:
| Item | Stage 1 | Stage 2 | Stage 3 | Stage 4 |
|------|---------|---------|---------|---------|
| Home | ✅ | ✅ | ✅ | ✅ |
| Search | ✅ | ✅ | ✅ | ✅ |
| User Menu | ✅ | ✅ | ✅ | ✅ |
| Content items | ❌ | ❌ | ✅ | ✅ |

**Implementation**:
```html
<!-- Example Jinja conditional -->
{% if trust_stage|default(1) >= 3 %}
<li class="nav-item">
  <!-- Stage 3+ content -->
</li>
{% endif %}
```

**Verification**:
```bash
# Check trust conditionals added
grep -n "trust_stage" templates/components/navigation.html
```

**Evidence Required**:
- [ ] Trust conditionals in template
- [ ] Tests for all 4 stages

### Step 4: Visual Hierarchy Adjustment (Phase 3)

**CSS Changes**:
- Reduce secondary item prominence
- Home link clearly primary
- Maintain accessibility contrast

**Verification**:
```bash
# Check CSS modifications
grep -n "nav" web/static/css/*.css | head -20
```

**Evidence Required**:
- [ ] CSS changes documented
- [ ] Accessibility maintained

### Step 5: Command Palette Integration (Phase 4)

**Implementation**:
- Add Cmd/Ctrl+K hint
- Add search trigger (placeholder if #421 not done)

**Evidence Required**:
- [ ] Shortcut hint visible
- [ ] Search trigger exists

### Step 6: Full Test Suite (Phase Z)

```bash
# Run nav tests
python -m pytest tests/unit/templates/test_navigation*.py -v

# Run full suite
python -m pytest tests/unit/ -v --tb=line | tail -20
```

**Evidence Required**:
- [ ] All new tests passing
- [ ] No regressions (4364+ baseline)

---

## Success Criteria (With Evidence)

- [ ] Nav items use natural language (grep output)
- [ ] Trust-gated visibility working (test output)
- [ ] Visual hierarchy adjusted (screenshot/CSS diff)
- [ ] Palette integration done (shortcut hint)
- [ ] 10+ new tests added (test count)
- [ ] No regressions (full suite output)
- [ ] GitHub issue updated (issue link)

---

## Deliverables

1. **Code Changes**: Modified navigation.html, CSS
2. **Test Coverage**: 10+ new tests
3. **Evidence Report**: All verification commands with output
4. **GitHub Update**: Issue #420 updated with evidence
5. **Vocabulary Documentation**: Mapping preserved in issue

---

## STOP Conditions

STOP immediately and escalate if:
- [ ] trust_stage not available in template context
- [ ] Accessibility degradation detected
- [ ] Navigation breaks on any template
- [ ] Tests fail for any reason
- [ ] #421 scope conflict discovered
- [ ] Visual changes undermine home state paradigm

---

## Self-Check Before Claiming Complete

1. Did I run ALL verification commands?
2. Did I capture ALL output as evidence?
3. Are ALL acceptance criteria checked off with evidence?
4. Did I run the full test suite for regressions?
5. Is the GitHub issue updated with evidence?
6. Does the nav feel "supportive" not "prominent"?

---

*Template Version: 10.2*
*Issue: #420 MUX-NAV-UTILITY*
*Agent: Lead Developer*
*Date: 2026-01-25*
