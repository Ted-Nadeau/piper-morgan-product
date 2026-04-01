# CANONICAL-TODO-COMPLETE: Todo Completion and Lifecycle Management

**Labels**: `enhancement`, `M1`, `canonical-queries`
**Priority**: P3 — Completes partially-implemented todo category
**Discovered**: #884 Run 4, 2026-03-12
**Source**: CXO failure gap analysis

---

## Problem

Todo management is partially implemented: users can add todos (Q54) and list them (Q56), but cannot mark them complete (Q55). This creates an asymmetric experience — users can create work but can't close it. The December canonical test matrix flagged todo management as "fundamental functionality" for alpha.

## Affected Queries

| Query # | Input | Current Status |
|---------|-------|---------------|
| Q54 | "Add a todo: review the deployment plan" | ✅ PASS (asks for clarification) |
| Q55 | "Complete the PR review todo" | ❌ NOT_IMPL (graceful fallback) |
| Q56 | "Show my todos" | ✅ PASS |
| Q57 | "What's my next todo?" | ✅ PASS |

## Acceptance Criteria

- [ ] User can mark a todo as complete via natural language ("complete", "done", "finish", "mark done")
- [ ] Completed todos are distinguished from active todos in list view
- [ ] Partial matching works ("complete the PR review" matches "review the PR" todo)
- [ ] Graceful handling when no matching todo found

## Context

Todo CRUD is a core PM workflow. Users who discover they can add and list todos will naturally try to complete them. The current graceful fallback ("I don't have that capability yet") is adequate for alpha but should be resolved before beta.

## Sprint Placement

M1 — Todo add/list/priority infrastructure already passes. Completion is a state change on existing persistence. No M3 dependencies required.

---

*Drafted by CXO, 2026-03-13*
