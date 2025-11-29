# UI-QUICK-FIXES - Investigation & Triage of UI Issues

**Priority**: P0 (Alpha blocking - some issues)
**Labels**: `ux`, `alpha-prep`, `bug-triage`
**Milestone**: Sprint A9 (Final Alpha Prep)
**Epic**: Alpha Launch
**Related**: Issue #376 (FRONTEND-RBAC-AWARENESS)

---

## Problem Statement

### Current State
Navigation QA testing revealed 14 UI issues across the application. Many features are 75-90% complete with missing wiring, broken buttons, or incomplete integration. Issues range from critical (buttons don't work) to cosmetic (layout problems).

### Impact
- **Blocks**: Smooth alpha user experience for Michelle tomorrow
- **User Impact**: Confusion, broken workflows, features appearing available but non-functional
- **Technical Debt**: Accumulating 75% complete work without proper completion/documentation

### Strategic Context
This is rapid alpha prep work. We need to:
1. Fix quick wins (likely miswiring in new code)
2. Honestly assess what's truly broken vs incomplete
3. Add clear "Coming Soon" messaging where needed
4. Document remaining issues for post-alpha work

---

## Goal

**Primary Objective**: Investigate all 14 UI issues, fix quick wins, triage the rest

**Approach**: Option C Strategy
- Phase 1: Quick investigation of new code issues (#6, #7, #14)
- Evaluation Point: Assess depth of remaining issues
- Phase 2+: Prioritize based on findings

**Example User Experience**:
```
BEFORE:
- Click "Create New List" → Nothing happens → Confusion
- Click "Integrations" → JavaScript error → Frustration
- Try to logout → Button doesn't work → Can't switch users

AFTER:
- "Create New List" works OR shows clear "Coming Soon" message
- "Integrations" either works or clearly states "Available in beta"
- Logout functions properly OR provides workaround instructions
```

---

## What Already Exists

### Working Infrastructure ✅
- Permission-aware UI from Issue #376 (Option B + C)
- User context system
- Resource pages (Lists, Todos, Projects)
- Backend APIs for most features

### Known Issues ❌ (from CSV)
See `dev/active/UI-issues.csv` for complete list

**High Priority** (6 issues):
- #4: Standup generation broken
- #6: Create New List button fails
- #7: Create New Todo button fails
- #8: Files page disconnected
- #13: Integrations page broken + causes error
- #14: Login/logout broken

**Medium Priority** (3 issues):
- #5, #9, #12: UX polish issues

**Low Priority** (5 issues):
- #1, #2, #3, #10, #11: Cosmetic issues

---

## Requirements

### Phase 1: Quick Investigation & Fixes (60 minutes)
**Objective**: Fix new code issues that are likely simple miswiring

**Issues to Investigate**:
- [ ] #6: Create New List button (built today - likely API missing)
- [ ] #7: Create New Todo button (built today - likely API missing)
- [ ] #14: Login/logout UI (known issue - needs UI implementation)

**For each issue**:
- [ ] Use Serena to find relevant code
- [ ] Check git history for what was built
- [ ] Identify root cause (missing API? miswiring? 75% complete?)
- [ ] Estimate fix effort (quick win vs rabbit hole)

**Deliverables**:
- Investigation report for #6, #7, #14
- Fixes for any quick wins found
- Severity re-assessment based on actual findings

### Evaluation Point 1: After Phase 1
**Stop and assess**:
- How many issues were quick fixes?
- What's the real depth of remaining issues?
- Do we have time/capacity to fix more today?
- What should be deferred with clear messaging?

**Decision criteria**:
- **If 2+ issues fixed quickly**: Continue to Phase 2
- **If all are rabbit holes**: Triage and add "Coming Soon" messaging
- **If mixed**: PM decides priority for remaining work

### Phase 2: Remaining High-Priority Issues (TBD after Phase 1)
Will be defined based on Phase 1 findings

### Phase Z: Documentation & Handoff
- [ ] Update Known Issues document
- [ ] Add "Coming Soon" messaging where needed
- [ ] Document investigation findings
- [ ] Update alpha onboarding guide
- [ ] Session log complete

---

## Acceptance Criteria

### Phase 1 Complete When:
- [ ] #6, #7, #14 investigated with Serena
- [ ] Root causes documented
- [ ] Quick wins fixed OR marked as complex
- [ ] Investigation report shows effort estimates
- [ ] PM has data to make Phase 2 decisions

### Overall Complete When:
- [ ] All High priority issues either fixed OR have "Coming Soon" messaging
- [ ] Known Issues document updated
- [ ] No broken functionality exposed without clear communication
- [ ] Michelle can use core features tomorrow

### Testing
- [ ] All fixed buttons tested manually
- [ ] JavaScript console shows no errors on affected pages
- [ ] "Coming Soon" messaging clear and helpful
- [ ] No regressions to working features

### Quality
- [ ] Investigation thorough (Serena, git history, docs checked)
- [ ] Honest assessment of 75% completion pattern
- [ ] Clear severity ratings based on evidence
- [ ] Alpha-appropriate solutions (not over-engineered)

### Documentation
- [ ] Investigation findings documented
- [ ] Known Issues updated
- [ ] Alpha onboarding guide reflects current state
- [ ] Session log complete

---

## Investigation Strategy

### For Each Issue, Use:

**1. Serena Symbolic Queries**:
```bash
# Find related code
mcp__serena__find_symbol "createList" depth=1 include_body=true
mcp__serena__find_referencing_symbols "list_router"

# Search for patterns
mcp__serena__search_for_pattern "Create.*List"
```

**2. Git History**:
```bash
# When was this feature last touched?
git log --oneline --all --grep="list" -- templates/ web/

# What changed recently?
git log -p --since="2 weeks ago" -- templates/lists.html
```

**3. Documentation**:
```bash
# Check for related docs
grep -r "lists\|todos\|files" docs/ --include="*.md"

# Check session logs
ls -lt dev/2025/11/ | grep -i "list\|todo\|file"
```

**4. Backend API Verification**:
```bash
# Do the endpoints exist?
grep -r "\/api\/v1\/lists" services/ web/
curl -X GET http://localhost:8001/api/v1/lists
curl -X POST http://localhost:8001/api/v1/lists
```

---

## Timeline Estimate

**Phase 1 Investigation**: 60 minutes
- #6 investigation: 20 min
- #7 investigation: 20 min
- #14 investigation: 20 min

**Phase 1 Fixes** (if quick wins): 15-30 min

**Evaluation Point**: 15 min

**Phase 2** (TBD): Depends on Phase 1 findings

**Target Start**: 2:20 PM
**Phase 1 Complete**: 3:30 PM
**Evaluation**: 3:45 PM

---

## STOP Conditions

**STOP immediately if**:
- Investigation shows major architectural issues
- Fixes require breaking changes
- Backend APIs completely missing (not just unwired)
- Time investment exceeds alpha testing value
- Security vulnerabilities discovered

**When stopped**: Document findings, add clear messaging, move to Known Issues

---

## Success Metrics

### Quantitative
- Number of issues fixed vs deferred
- Zero JavaScript errors on tested pages
- Zero broken buttons without "Coming Soon" messaging

### Qualitative
- Michelle can use core features tomorrow
- Honest assessment of system completeness
- Clear communication about alpha state
- Sustainable approach (not accumulating more 75% work)

---

## Completion Checklist

Before requesting PM review:
- [ ] Phase 1 investigation complete ✅
- [ ] Investigation report written ✅
- [ ] Quick wins fixed and tested ✅
- [ ] Remaining issues triaged ✅
- [ ] Known Issues document updated ✅
- [ ] Session log complete ✅
- [ ] Ready for PM evaluation decision ✅

**Status**: Not Started

---

## Notes for Implementation

This is triage work, not feature development. Focus on:
1. **Investigation thoroughness** - Use all tools (Serena, git, docs)
2. **Honest assessment** - Don't rationalize 75% as "complete"
3. **Alpha-appropriate fixes** - Quick wins only, not refactors
4. **Clear communication** - Better to say "Coming Soon" than silently broken

---

**Remember**:
- Quality investigation over rushed fixes
- Evidence required for all assessments
- PM evaluates at Phase 1 checkpoint
- Michelle's alpha experience is tomorrow!

---

_Issue created: November 23, 2025, 2:18 PM_
_Last updated: November 23, 2025_
_Target: Phase 1 complete by 3:30 PM today_
