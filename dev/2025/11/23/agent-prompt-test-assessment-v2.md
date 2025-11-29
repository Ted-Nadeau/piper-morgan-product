# Prompt for Claude Code: TEST Epic Status Assessment and Planning

## Mission
Assess the TEST epic status based on GitHub issues and actual work completed today, then create an updated plan for remaining work.

## Background Context

The TEST epic was created yesterday (November 19) with multiple GitHub issues. The original gameplan document is lost, but we have:
1. The complete set of TEST- GitHub issues (attached)
2. Evidence of significant test work completed today
3. Various reports from agents working on test issues

Your job: Figure out what's been done, what remains, and create a clear path forward.

## Investigation Tasks

### Phase 1: Understand the Scope (30 minutes)

**1.1 Review GitHub Issues**
- [ ] Read the attached TEST epic GitHub issues document
- [ ] List all issues (P0, P1, P2, P3)
- [ ] Note dependencies between issues
- [ ] Identify critical path items

**1.2 Discover Today's Work**
- [ ] Check session logs from 2025-11-20-*-code-*.md
- [ ] Look for test-related commits since Nov 19
- [ ] Find skip test audit reports (health score 87/100)
- [ ] Find document handler investigation (5/6 implemented)
- [ ] Find P0 test fixes report (99.7% unit tests passing)
- [ ] Check for any other test work

**1.3 Current Test Status**
- [ ] Run current test suite for baseline
- [ ] Count passing/failing/skipped
- [ ] Compare to issues' success criteria
- [ ] Note what's blocking vs working

### Phase 2: Status Assessment (45 minutes)

**2.1 Issue-by-Issue Status**

For each GitHub issue in the TEST epic:
```markdown
| Issue | Priority | Description | Status | Evidence | Remaining Work |
|-------|----------|-------------|--------|----------|----------------|
| TEST-PHANTOM-SPATIAL | P0 | 4 missing methods | ? | [check] | ? |
| TEST-INFRA-ENUM | P0 | 5 missing enums | ? | [check] | ? |
| TEST-DISCIPLINE-KNOWN | P0 | Known failures | ? | [check] | ? |
| ... | | | | | |
```

**2.2 Work Completed Today**

Document all test improvements:
```markdown
| Work Done | By Agent | Evidence | Impact |
|-----------|----------|----------|---------|
| Skip test cleanup | Code | 87/100 health | 146 skips removed |
| Doc handler investigation | Code | 5/6 exist | Only PM-020 missing |
| P0 test fixes | Code | 99.7% passing | 338 tests fixed |
| ... | | | |
```

**2.3 New Discoveries**

Issues found but not in original epic:
```markdown
| Discovery | Severity | Impact | Effort |
|-----------|----------|--------|--------|
| Slack webhook signature broken | P0 | Security | 30 min |
| API Pattern-007 violation | P1 | Architecture | 2 hrs |
| Personality enhancer timeout | P2 | Cleanup | 4 hrs |
| ... | | | |
```

### Phase 3: Create Updated Plan (30 minutes)

**3.1 What Can Be Closed**

Based on work completed:
```markdown
## Issues to Close
- TEST-XXX: [Reason - work completed, evidence: commit/log]
- TEST-YYY: [Superseded by actual implementation]
```

**3.2 What Needs Updates**

Issues partially complete:
```markdown
## Issues to Update
- TEST-XXX: Update description to reflect [finding]
- TEST-YYY: Reduce scope based on [discovery]
```

**3.3 Realistic Test Epic Plan**

```markdown
## TEST Epic - Revised Plan

### Already Complete ✅
- Skip test hygiene (87/100)
- Unit test fixes (99.7% passing)
- Document handler routing identified

### Sprint S1 Priorities (This Week)
P0 items that block development:
1. [ ] TEST-PHANTOM-SPATIAL - Fix missing methods (2 hrs)
2. [ ] TEST-INFRA-ENUM - Add enums (15 min)
3. [ ] Slack webhook signature - Security fix (30 min)

### Sprint S2 Priorities (Next Week)
P1 items for stability:
1. [ ] TEST-DISCIPLINE-KNOWN - Known failures workflow
2. [ ] TEST-INFRA-CONTAINER - Fix fixtures
3. [ ] API Pattern-007 - Graceful degradation

### Backlog (When Possible)
P2/P3 items:
- Phantom test cleanup
- Smoke test creation
- E2E journey tests
```

### Phase 4: Executive Report (15 minutes)

```markdown
# TEST Epic Status Report - November 20, 2025

## Executive Summary

### The Good News
- Test health improved from 62% to 87% (skip cleanup)
- Unit tests at 99.7% passing (up from ~70%)
- Document handlers 83% implemented (not 0%)
- Total improvements today: ~400 tests fixed/cleaned

### The Reality Check
- P0 issues remain (phantom methods, missing enums)
- Security issue discovered (Slack webhook)
- Some "TEST" issues already resolved by other work

### The Path Forward
- 3-4 hours to resolve remaining P0 items
- Most infrastructure issues are minor
- Can achieve 95%+ passing by end of week

## Recommendations

1. **Immediate** (Today):
   - Add missing enums (15 min quick win)
   - Fix Slack webhook signature (security)

2. **This Week**:
   - Resolve phantom spatial methods
   - Implement known-failures workflow

3. **Defer**:
   - Phantom test cleanup (not blocking)
   - E2E tests (nice to have)

## Metrics

| Metric | Start (Nov 19) | Current (Nov 20) | Target |
|--------|---------------|------------------|--------|
| Tests Passing | ~70% | 99.7% (unit) | 95%+ |
| Skip Health | 62/100 | 87/100 | 90/100 |
| P0 Issues | 3 | 1-2 remaining | 0 |
| Collection Errors | Many | 0 | 0 |
```

## Success Criteria

- [ ] All TEST- issues reviewed against actual status
- [ ] Clear list of what's complete vs remaining
- [ ] Realistic timeline based on today's velocity
- [ ] Actionable recommendations for PM
- [ ] No duplicate work or missed fixes

## STOP Conditions

Stop and report if:
- Test suite significantly degraded since morning
- Critical security issues in test code
- Major conflicts in agent work
- Production code broken by test "fixes"

## Time Budget

**Total: 2 hours**
- Phase 1: 30 minutes (understand scope)
- Phase 2: 45 minutes (assess status)
- Phase 3: 30 minutes (create plan)
- Phase 4: 15 minutes (executive report)

## Inputs

1. **GitHub Issues Document**: github-issues-TEST-epic.md (attached by PM)
2. **Session Logs**: Search for 2025-11-20-*-code-*.md
3. **Test Reports**: Look for skip audit, P0 fixes, document handler analysis

---

**Remember:**
- Work from the GitHub issues as source of truth
- Document all evidence of work completed
- Be realistic about remaining effort
- Flag any conflicts or redundancies
- Focus on actionable next steps

**Start with:** Reading the GitHub TEST epic issues document

---

*Created by*: Chief Architect
*Date*: November 20, 2025, 11:51 AM
*Context*: Assessing TEST epic without original gameplan
