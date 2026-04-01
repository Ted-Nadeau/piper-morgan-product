# CLASSIFIER-KEYWORD: Intent Disambiguation for Multi-Trigger Keywords

**Labels**: `bug`, `M1`, `canonical-queries`
**Parent**: #884 (CANONICAL-RETEST)
**Priority**: P2 — Affects 5 canonical queries (9.4% of total)
**Discovered**: #884 Run 4, 2026-03-12
**Source**: CXO failure gap analysis (memo-cxo-failure-gap-revised-2026-03-13.md)

---

## Problem

The intent classifier routes 5 canonical queries to the wrong handler because a surface keyword in the query triggers a handler that doesn't match the user's actual intent. In each case, the classifier latches onto a single word ("time", "project", "calendar", "milestone", "about") and ignores the rest of the sentence.

This is a Colleague Test failure: Piper hears one word instead of the whole question.

## Affected Queries

| Query # | Input | Expected | Actual | Trigger Word |
|---------|-------|----------|--------|-------------|
| Q27 | "Tell me more about the GitHub integration" | query | identity | "about" |
| Q33 | "Find time for a 1:1 with the team lead" | execution | temporal | "time" |
| Q40 | "Update the project roadmap document" | execution | portfolio | "project" |
| Q43 | "What's blocking the milestone?" | analysis | status | "milestone" |
| Q62 | "Check my calendar for conflicts" | query | temporal | "calendar" |

## Root Cause

The pre-classifier pattern matching (likely in `pre_classify()` or `detect_multiple_intents()`) assigns intent based on keyword presence without weighing sentence structure or action verbs. "Find time" should weigh "find" (action → execution) over "time" (topic → temporal). "Update the project roadmap" should weigh "update" (action → execution) over "project" (topic → portfolio).

## Acceptance Criteria

- [ ] All 5 queries route to correct handler (verified via canonical retest script)
- [ ] No regressions in currently-passing queries (run full 61-query suite)
- [ ] Fix approach documented (pattern priority change vs. structural classifier change)

## Implementation Notes

**Investigation first**: Determine whether this is fixable by adjusting pattern priorities in the existing classifier, or whether it requires structural changes (e.g., verb-first classification, two-pass classification). The former is a few hours of work; the latter is a larger effort that may warrant deferring to M2.

**Specific patterns to examine**:
- Does "about" in `pre_classify()` trigger identity patterns? Q27 suggests yes.
- Does "time" trigger temporal before execution gets a chance? Q33 suggests yes.
- Does "project" trigger portfolio/status before execution? Q40 suggests yes.
- How does the classifier handle action verbs ("find", "update", "check", "tell me") — are these weighted at all?

**Test approach**: The canonical retest script (`canonical-retest-884.py`) already covers all 5 queries. Run it before and after changes to verify fixes and catch regressions.

## Sprint Placement

M1 if fixable via pattern priority tuning (estimated 2-4 hours).
Defer to M2 if structural classifier changes required.

Lead Dev to assess complexity before committing to sprint.

---

*Drafted by CXO, 2026-03-13*
