# Memo: Sprint Gate Template — Delivered

**To**: Chief of Staff
**From**: Chief Architect
**Date**: February 3, 2026
**Re**: Anti-Flattening Gates for MVP Sprints

---

## Deliverable

Attached: `sprint-gate-template-v1.md`

A reusable GitHub issue template covering all three requested gates:

1. **Persistence Layer Audit** — Success messages mapped to DB writes, E2E test evidence required
2. **Anti-Flattening Verification** — Design intent check, parrot audit, Colleague Test log
3. **Multi-Tenancy Sanity Check** — User scoping verified, grep evidence, cross-user test required

---

## Template Design Decisions

### Evidence Tables
Each gate includes a table for recording specific evidence (test names, files reviewed, endpoints audited). This prevents "checked the box without doing the work."

### Sign-off Separation
Gates require explicit sign-off with name and date. Recommend sign-off by someone other than primary implementer where feasible—fresh eyes catch what familiar eyes miss.

### N/A Option
Gate 3 (Multi-Tenancy) includes N/A path with required justification. Not all sprints touch user data.

### Progressive Fill
Usage notes encourage filling evidence as work progresses rather than batching at sprint end. The 75% pattern thrives when verification is deferred.

---

## Recommended Workflow

1. **Sprint creation**: Create Gate issue, link as blocker to epic
2. **During sprint**: Fill evidence tables incrementally
3. **Pre-closure**: Review all gates, obtain sign-offs
4. **Closure**: Gate issue closes → Epic can close
5. **Retro**: Archive gate in sprint retrospective for pattern tracking

---

## Ready for M0

Template is ready for immediate use. Suggest creating `M0-GATE` issue now so it's in place when M0 begins.

---

*Let me know if any criteria need adjustment.*
