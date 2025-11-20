# Prompt for Claude Code: TEST Epic Reconciliation and Gameplan Update

## Your Identity
You are Claude Code, a systematic development agent with excellent investigation and documentation skills. You excel at reconciling plans with actual work completed and providing accurate status updates.

## Session Log Management
Create a session log at: `docs/development/session-logs/2025-11-20-1120-code-test-reconciliation-log.md`

## Mission
Reconcile the TEST epic gameplan with actual work completed today (November 20, 2025) and provide comprehensive status update.

## Background Context

A TEST epic gameplan was created yesterday (November 19) for systematic test infrastructure improvement. Today, various agents have been working on test-related issues somewhat independently ("freelance" as the PM calls it). We need to:

1. Understand what was originally planned
2. Document what actually got done
3. Update the gameplan for remaining work
4. Update/close GitHub issues appropriately
5. Report back with clear status

## Investigation Tasks

### Phase 1: Gather Context (30 minutes)

**1.1 Find and Review Original Gameplan**
- [ ] Locate the TEST- gameplan (likely in /docs or /dev)
- [ ] Document original phases and tasks
- [ ] Note estimated timelines
- [ ] List GitHub issues referenced

**1.2 Discover Today's Work**
- [ ] Check session logs from 2025-11-20-*-code-*.md
- [ ] Look for test-related commits since Nov 19
- [ ] Review any skip test audit reports
- [ ] Find document handler investigation results
- [ ] Check for P0 test fixes

**1.3 Current Test Status**
- [ ] Run current test suite for baseline
- [ ] Count passing/failing/skipped
- [ ] Note test health score if available
- [ ] Compare to gameplan targets

### Phase 2: Reconciliation (45 minutes)

**2.1 Create Status Matrix**

For each gameplan task, document:
```markdown
| Gameplan Task | Original Est | Actual Status | Work Done By | Evidence | Remaining |
|---------------|--------------|---------------|--------------|----------|-----------|
| Task 1        | 4 hrs        | Complete      | Code (11/20) | [commit] | 0 hrs     |
| Task 2        | 2 hrs        | Partial       | Code (11/20) | [log]    | 1 hr      |
| Task 3        | 6 hrs        | Not started   | -            | -        | 6 hrs     |
```

**2.2 GitHub Issue Updates**

For each TEST- related issue:
```markdown
| Issue # | Title | Original Status | Current Status | Action Needed |
|---------|-------|----------------|----------------|---------------|
| #xxx    | ...   | Open           | Complete       | Close         |
| #yyy    | ...   | Open           | Partial        | Update        |
```

**2.3 Discovered Issues**

New issues found during today's work:
```markdown
| Description | Severity | Bead/Issue | Effort | Priority |
|-------------|----------|------------|--------|----------|
| Slack webhook signature | P0 | piper-morgan-xxx | 30 min | Critical |
| API Pattern-007 violation | P1 | piper-morgan-b3x | 2 hrs | High |
```

### Phase 3: Gameplan Update (30 minutes)

**3.1 Revised Gameplan Structure**

Update the gameplan to reflect:
- ✅ Completed work (with evidence)
- 🔄 In-progress items
- 📋 Remaining tasks
- 🆕 New discoveries
- ❌ Deprecated/removed items

**3.2 Realistic Timeline**

Based on actual velocity:
```markdown
## Revised Timeline

### Already Complete (as of Nov 20)
- Skip test cleanup: 87/100 health ✅
- P0 test fixes: 365/366 passing ✅
- Document handler investigation ✅

### Sprint S1 (Nov 21-27)
- Remaining P1 test fixes (8 hrs)
- Slack webhook signature (30 min)
- API graceful degradation (2 hrs)

### Sprint S2 (Nov 28-Dec 4)
- [Updated based on findings]
```

### Phase 4: Comprehensive Report (15 minutes)

**4.1 Executive Summary**
```markdown
# TEST- Epic Status Report

## Headlines
- Test health: XX% → YY% improvement
- Tests passing: XXX → YYY
- Critical bugs found: N
- Estimated completion: [date]

## Key Achievements Today
1. [Achievement with metrics]
2. [Achievement with metrics]
3. [Achievement with metrics]

## Blockers/Risks
1. [Blocker and mitigation]
2. [Risk and plan]

## Recommendations
1. [Priority action]
2. [Resource allocation]
3. [Dependency management]
```

## Deliverables

### 1. Updated Gameplan
File: `docs/gameplans/TEST-epic-gameplan-v2.md`
- Current status clearly marked
- Remaining work prioritized
- Dependencies identified
- Resource needs specified

### 2. Issue Status Report
File: `docs/reports/test-epic-issues-status-20251120.md`
- All TEST- issues reviewed
- Clear close/update/create recommendations
- Bead tracking for deferred work

### 3. Executive Summary
File: `docs/reports/test-epic-executive-summary-20251120.md`
- For PM and Chief Architect
- Clear metrics and progress
- Actionable recommendations
- Risk assessment

## Success Criteria

- [ ] Located original gameplan
- [ ] Found all work done today
- [ ] Reconciled plan vs actual
- [ ] Updated gameplan reflects reality
- [ ] GitHub issues have clear actions
- [ ] Executive summary is actionable
- [ ] No work lost or duplicated
- [ ] Clear path forward identified

## STOP Conditions

Stop and report if you discover:
- Original gameplan cannot be found
- Major test infrastructure corruption
- Security vulnerabilities in test code
- Conflicting work by multiple agents
- Test suite in worse state than planned

## Time Budget

**Total: 2 hours**
- Phase 1: 30 minutes (gather)
- Phase 2: 45 minutes (reconcile)
- Phase 3: 30 minutes (update)
- Phase 4: 15 minutes (report)

---

**Remember:**
- Evidence-based reporting only
- Include actual test output
- Note agent session logs reviewed
- Track all bead IDs discovered
- Be honest about what's incomplete

**Start with:** Locating the original TEST- gameplan document

---

*Created by*: Chief Architect
*Date*: November 20, 2025, 11:20 AM
*Context*: Reconciling planned vs actual test infrastructure work
