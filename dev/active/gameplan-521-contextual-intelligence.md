# Gameplan: Issue #521 - Contextual Intelligence Queries

**GitHub Issue**: #521
**Date**: December 27, 2025
**Lead Developer**: Opus 4.5
**Status**: APPROVED

---

## Queries in Scope

| Query # | User Query | Category |
|---------|------------|----------|
| #29 | "What changed since X?" | Conversational |
| #30 | "What needs my attention?" | Conversational |

---

## Phase 0: Infrastructure Verification

### Available Infrastructure (from Dec 25 reconnaissance)

| Component | Status | Location |
|-----------|--------|----------|
| AuditLog table | ✅ Exists | `services/database/models.py` |
| Entity timestamps | ✅ All have `created_at`, `updated_at` | Domain models |
| Priority detection (todos) | ✅ Exists | `CanonicalHandlers._handle_priority_query()` |
| Calendar urgency | ✅ Exists | `get_temporal_summary()` |
| IntentService | ✅ Exists | `services/intent/intent_service.py` |

### What's Missing

- Unified "activity since X" aggregation handler
- Cross-integration attention aggregation
- Time-range parsing for "since yesterday", "since Monday", etc.

---

## Multi-Agent Coordination Plan

### Agent Deployment Map

| Phase | Agent Type | Queries | Evidence Required | Handoff |
|-------|------------|---------|-------------------|---------|
| 1 | Code Agent | #29, #30 | 6+ tests, handlers added | Test locations, pytest output |
| 2 | Lead Dev | Verification | Tests pass independently | User test steps |

---

## Phase 1: Code Agent Deployment

### Prompt for Code Agent

```
GitHub Issue: #521 (Contextual Intelligence Queries)
Session Log: dev/active/2025-12-27-0610-lead-code-opus-log.md

## Your Task
Implement 2 canonical query handlers for contextual intelligence:

### Query #29: "What changed since X?"
- Parse time expressions: "since yesterday", "since Monday", "in the last hour"
- Aggregate from:
  1. AuditLog table (user actions)
  2. Entity timestamps (created_at, updated_at on todos, projects, files)
- Return formatted activity summary

### Query #30: "What needs my attention?"
- Aggregate attention items from:
  1. High-priority todos (use existing priority detection)
  2. Overdue items
  3. Calendar urgency (upcoming meetings from get_temporal_summary)
  4. Stale projects (no recent activity)
- Return prioritized attention list

## Acceptance Criteria
- [ ] Query #29: Handler parses time expressions and returns activity summary
- [ ] Query #30: Handler aggregates attention items across integrations
- [ ] 6+ tests added (3 per query minimum)
- [ ] Tests in tests/unit/services/intent_service/test_contextual_query_handlers.py
- [ ] All tests passing
- [ ] No regressions in existing intent service tests

## Infrastructure to Use
- AuditLog: services/database/models.py
- Priority detection: Look at CanonicalHandlers._handle_priority_query()
- Calendar: CalendarIntegrationRouter.get_temporal_summary()
- Existing patterns: See test_todo_query_handlers.py for handler test patterns

## Evidence Required
1. Test count: "Added X tests in [file]"
2. Test output: Full pytest output
3. Files modified: List with line counts
4. Example responses: Show sample output for each query

## Handoff Format
Return with:
- Issue #521 Completion Report
- Status: Complete/Partial/Blocked
- All evidence listed above
```

---

## Phase 2: Lead Dev Verification

### Verification Checklist
- [ ] Run tests independently: `pytest tests/unit/services/intent_service/test_contextual_query_handlers.py -v`
- [ ] Run full intent service tests: `pytest tests/unit/services/intent_service/ -v`
- [ ] Verify no regressions
- [ ] Review handler implementations
- [ ] Document in session log

---

## Success Criteria

| Criterion | Required |
|-----------|----------|
| Both queries functional | Yes |
| 6+ tests added | Yes |
| No regressions | Yes |
| Evidence documented | Yes |

---

## STOP Conditions

- AuditLog table structure different than expected → STOP
- Time parsing requires external library not installed → STOP
- Cross-integration access patterns unclear → STOP

---

## Manual Testing Note

✅ **Can test immediately** - No integration setup blockers. These queries work with existing audit/activity data in the database.

---

**Status**: APPROVED - Ready for Code Agent deployment
