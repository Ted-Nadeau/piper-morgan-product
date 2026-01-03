# Gameplan: Canonical Queries Phase A (Quick Wins)

**GitHub Issue**: #518
**Date**: December 26, 2025
**Lead Developer**: Opus 4.5
**Status**: AWAITING PM APPROVAL

---

## Phase -1: Infrastructure Verification

### Verified Infrastructure

| Component | Status | Evidence |
|-----------|--------|----------|
| IntentService | ✅ Exists | `services/intent/intent_service.py` |
| CalendarMCPAdapter | ✅ Exists | `services/integrations/calendar/` |
| GitHubIntegrationRouter | ✅ Exists | `services/integrations/github/` |
| TodoRepository | ✅ Exists | `services/repositories/todo_repository.py` |

### Known Gaps (from Dec 25 reconnaissance)
- GitHubIntegrationRouter has no `list_pull_requests()` method - Query #42 may need this
- Calendar OAuth not yet configured for alpha users

### Worktree Assessment
- [ ] **SKIP WORKTREE** - Single Lead Dev coordinating, sequential phases, <3 hour estimate

---

## Phase 0: Initial Bookending

### Queries to Implement (8 total)

**Calendar Cluster (3 queries)**:
- #34: How much time in meetings?
- #35: Review my recurring meetings
- #61: What's my week look like?

**GitHub Cluster (2 queries)**:
- #41: What did we ship this week?
- #42: Show me stale PRs

**Todo Cluster (2 queries)**:
- #56: Show my todos
- #57: What's my next todo?

**Productivity (1 query)**:
- #51: What's my productivity this week?

---

## Multi-Agent Coordination Plan

### Agent Deployment Map

| Phase | Agent Type | Queries | Evidence Required | Handoff |
|-------|------------|---------|-------------------|---------|
| 1 | Code Agent | #56, #57 (Todos) | 6 tests, routing verified | Test locations |
| 2 | Code Agent | #41, #42 (GitHub) | 6 tests, PR method if needed | Test locations |
| 3 | Code Agent | #34, #35, #61 (Calendar) | 9 tests, OAuth note | Test locations |
| 4 | Code Agent | #51 (Productivity) | 3 tests | Test locations |
| 5 | Lead Dev | Integration verification | All 24 tests pass | User demo |

### Verification Gates
- [ ] Phase 1: Todo tests passing, user can ask "show my todos"
- [ ] Phase 2: GitHub tests passing, user can ask "what did we ship"
- [ ] Phase 3: Calendar tests passing (or graceful degradation if no OAuth)
- [ ] Phase 4: Productivity test passing
- [ ] Phase 5: All 8 queries demonstrated

---

## Phase 1: Todo Cluster (#56, #57)

### Deploy: Code Agent

**Prompt**:
```
GitHub Issue: #518 (Phase A Quick Wins)
Focus: Queries #56 and #57

Task:
1. Add intent routing for "show my todos" → TodoRepository.list_by_owner()
2. Add intent routing for "what's my next todo" → TodoRepository with priority sort
3. Format responses for user display
4. Add 6 unit tests (3 per query)

Acceptance Criteria:
- [ ] Query #56: "Show my todos" returns formatted todo list
- [ ] Query #57: "What's my next todo" returns highest priority item
- [ ] 6 tests in tests/unit/services/intent_service/test_todo_handlers.py
- [ ] All tests passing

Evidence Required:
- pytest output
- Files modified
- Example responses
```

---

## Phase 2: GitHub Cluster (#41, #42)

### Deploy: Code Agent

**Prompt**:
```
GitHub Issue: #518 (Phase A Quick Wins)
Focus: Queries #41 and #42

Task:
1. Add intent routing for "what did we ship this week" → list closed issues/PRs
2. Add intent routing for "show me stale PRs" → list PRs older than X days
3. If PR list method missing, add to GitHubIntegrationRouter
4. Format responses for user display
5. Add 6 unit tests (3 per query)

Acceptance Criteria:
- [ ] Query #41: "What did we ship" returns closed items this week
- [ ] Query #42: "Show stale PRs" returns PRs older than 7 days
- [ ] 6 tests in tests/unit/services/intent_service/test_github_handlers.py
- [ ] All tests passing

Evidence Required:
- pytest output
- Files modified (note if GitHubIntegrationRouter changed)
- Example responses
```

---

## Phase 3: Calendar Cluster (#34, #35, #61)

### Deploy: Code Agent

**Prompt**:
```
GitHub Issue: #518 (Phase A Quick Wins)
Focus: Queries #34, #35, #61

Task:
1. Add intent routing for "how much time in meetings" → CalendarMCPAdapter.get_events() + duration calc
2. Add intent routing for "review recurring meetings" → filter for recurring events
3. Add intent routing for "what's my week look like" → week date range query
4. Graceful degradation if Calendar not configured
5. Add 9 unit tests (3 per query)

Acceptance Criteria:
- [ ] Query #34: Returns meeting time summary (or "Calendar not configured" gracefully)
- [ ] Query #35: Returns recurring meeting list
- [ ] Query #61: Returns week calendar view
- [ ] 9 tests in tests/unit/services/intent_service/test_calendar_handlers.py
- [ ] Tests mock CalendarMCPAdapter for CI compatibility

Evidence Required:
- pytest output
- Files modified
- Example responses (with and without calendar configured)
```

---

## Phase 4: Productivity Query (#51)

### Deploy: Code Agent

**Prompt**:
```
GitHub Issue: #518 (Phase A Quick Wins)
Focus: Query #51

Task:
1. Add intent routing for "what's my productivity this week"
2. Aggregate from available sources (todos completed, issues closed, etc.)
3. Format as productivity summary
4. Add 3 unit tests

Acceptance Criteria:
- [ ] Query #51: Returns productivity metrics
- [ ] 3 tests in tests/unit/services/intent_service/test_productivity_handlers.py
- [ ] Graceful handling if some data sources unavailable

Evidence Required:
- pytest output
- Files modified
- Example response
```

---

## Phase 5: Integration Verification (Lead Dev)

### Verification Checklist
- [ ] All 24+ tests passing: `pytest tests/unit/services/intent_service/ -v`
- [ ] No regressions: Original 227 canonical tests still pass
- [ ] Demo each query in browser/chat interface
- [ ] Update canonical-queries-v2.1.md with implementation status

### Evidence Compilation
- Total test count
- Full pytest output
- User demo screenshots/transcripts
- Files modified summary

---

## Phase Z: Final Bookending

### GitHub Issue Update
```markdown
## Status: Complete

### Implementation Evidence
- Tests: 24 tests added across 4 test files
- Verification: All tests passing (output below)
- Files modified: [list]
- User verification: [demo results]

### Queries Implemented
- [x] #34: How much time in meetings
- [x] #35: Review recurring meetings
- [x] #41: What did we ship this week
- [x] #42: Show me stale PRs
- [x] #51: Productivity this week
- [x] #56: Show my todos
- [x] #57: What's my next todo
- [x] #61: What's my week look like

Ready for PM review.
```

### Documentation Updates
- [ ] canonical-queries-v2.1.md: Update 8 queries to ✅
- [ ] Session log: Full evidence recorded
- [ ] Test matrix: Update if applicable

---

## Success Criteria

| Criterion | Required |
|-----------|----------|
| All 8 queries functional | Yes |
| 24+ tests added | Yes |
| No regressions | Yes |
| Evidence documented | Yes |
| PM approval | Yes |

---

## STOP Conditions

- Calendar OAuth blocking more than calendar queries → Escalate
- GitHub PR method requires architectural decision → Escalate
- Test failures in existing canonical tests → Stop and diagnose
- Any query requires schema changes → Escalate

---

**Status**: AWAITING PM APPROVAL

*When approved, Lead Developer will execute phases sequentially, deploying Code agents with the prompts above.*
