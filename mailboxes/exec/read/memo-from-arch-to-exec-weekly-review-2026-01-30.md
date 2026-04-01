# Weekly Review: January 23-29, 2026

**From**: Chief Architect
**To**: Chief of Staff
**Date**: January 30, 2026
**Re**: Week in Review - Architectural Perspective
**Period**: Friday Jan 23 - Thursday Jan 29

---

## Executive Summary

An exceptionally productive week culminating in v0.8.5 release, followed by alpha testing that revealed foundational gaps, then systematic root cause investigation. The week's arc: **build fast → ship → discover what's broken → find root causes**.

**Headline metrics**:
- ~74 issues closed
- ~37 issues created (including 19 alpha bugs)
- ~2,200 tests added
- 1 major release (v0.8.5)
- 1 P0 bug discovered (#728) with root cause found (#736)
- 1 systemic architectural gap identified (#734)

---

## Daily Summary

| Day | Rating | Theme | Issues Closed | Issues Created | Tests |
|-----|--------|-------|---------------|----------------|-------|
| Fri 23 | HIGH-COMPLEXITY | TRUST-LEVELS epic complete | 18+ | - | ~636 |
| Sat 24 | HIGH-COMPLEXITY | MUX-INTERACT Gate #534, Mobile PoC | 12+ | - | ~434 |
| Sun 25 | HIGH-VELOCITY | MUX-IMPLEMENT P1-P3 sprint | 21 | - | ~1000 |
| Mon 26 | HIGH-ALIGNMENT | ADR-049/050 architectural decisions | 5 | - | ~80 |
| Tue 27 | HIGH-VELOCITY | v0.8.5 release, MUX-IMPLEMENT complete | 10 | 18 | ~50 |
| Wed 28 | MIXED-DAY | Alpha testing → P0 bug discovered | 8 | 12 | - |
| Thu 29 | LIGHT-DAY | Bug triage, root causes, parallel agents | 0 | 7 | - |

---

## Key Accomplishments

### 1. MUX-IMPLEMENT Super Epic Complete (Jan 18-27)

10-day sprint delivered:
- Navigation, settings, documentation access
- Lifecycle indicators on Todos, Projects, Work Items
- WCAG 2.1 AA accessibility compliance
- Design token system enforced
- 5253 tests passing

**Alpha testers unblocked**: Jake, Rebecca, Dominique

### 2. TRUST-LEVELS Epic Complete (Jan 23)

ADR-053 fully implemented with 453 tests covering:
- Stage progression (1-5)
- Regression on complaints
- Soft signal detection
- Floor enforcement

### 3. Architectural Decisions Finalized (Jan 26)

| ADR | Decision | Rationale |
|-----|----------|-----------|
| ADR-049 (Two-Tier Intent) | APPROVED for MVP | User notices onboarding derailment |
| ADR-050 Phases 1-3 | Deferred to V2 | Multi-party features, post-MVP |

**MVP vs V2 Rubric established**: "Does user notice gap?" is the key question.

### 4. v0.8.5 Released (Jan 27)

Clean release with comprehensive documentation updates. Three alpha testers notified.

### 5. Bug Triage & Root Cause Investigation (Jan 29)

A LIGHT-DAY but productive:
- **#731 fixed & verified**: Conversation persistence when typing directly
- **#736 fixed**: Projects global constraint → per-user composite constraint
- **3 parallel agents deployed** for deeper investigation
- Root causes documented for systematic fix planning

---

## Critical Discoveries

### P0 Bug #728: Portfolio Never Saves Projects (Jan 28)

**Discovery**: Alpha testing revealed portfolio onboarding has **never** worked correctly.

**Symptoms**:
- User goes through onboarding
- Piper says "I've added them to your portfolio"
- Projects page shows nothing
- **No code ever writes to database**

**Root Cause Found (Jan 29)**: #736 - The projects table has a GLOBAL unique constraint on `name`, not per-user. Different users couldn't have projects with the same name. Migration applied to create composite constraint `(owner_id, name)`.

**Pattern**: Classic "75% completion" - UI works, conversation works, success message displays, but final persistence step was never implemented.

### #731: Conversations Not Persisting (Jan 29)

**Discovery**: When users type directly in chat (without "+ New Chat"), no conversation was created in DB.

**Fix**: Auto-create conversation record in `/api/v1/intent` before processing. **Verified working** by PM.

### Systemic Issue #734: Multi-Tenancy Isolation Failures (Jan 28-29)

**Discovery**: Investigation of calendar token leakage revealed 38+ locations with isolation failures.

**Critical finding**: Integration tokens (calendar, GitHub, Slack) stored globally without user_id prefix. Alpha tester saw previous user's calendar events.

**Scope**: Not a bug - a missing architectural layer. OAuth tokens, API keys, config services, repositories all have incomplete user scoping.

**Status**: Full guidance delivered Jan 30 (today). PM approved domain-driven refactor with "break loudly" philosophy.

### Two Sidebar Features? (Jan 29)

**Question raised**: There appear to be TWO sidebar features:
1. **Left sidebar** — conversation list (works)
2. **Right History sidebar** (#425) — search, date grouping (never mounted)

May be duplicate functionality needing PM decision.

---

## Architectural Observation: The Persistence Layer Pattern

**#728 and #734 are related.** Both stem from the same underlying gap: incomplete persistence layer work.

The pattern:
1. **Feature development focuses on happy path** (UI, conversation, in-memory state)
2. **Persistence is assumed** but not verified
3. **Tests mock the database** so gaps aren't caught
4. **Real usage reveals the truth**

This is the third manifestation we've seen:
- Aug 2025: ConversationRepository stubs (75% pattern origin)
- Jan 28: Portfolio projects never saved (#728)
- Jan 30: Multi-tenancy isolation gaps (#734)

**Recommendation**: Future epic completion criteria should include "persistence layer audit" as a gate. Mocking is useful for unit tests but dangerous for completion verification.

---

## Methodology Observations

### What Worked

**Audit Cascade Discipline**: Jan 25's 21-issue day succeeded because every issue went through full audit → gameplan → approval → implementation flow. No shortcuts, no rework.

**"Cathedral to Rooms" Pattern**: Jan 27's modeling philosophy - "model completely first, document thoroughly, THEN prioritize" - prevented premature flattening.

**Simple Trigger Architecture**: Logging discipline investigation (Jan 25) confirmed that verbose protocols fail post-compaction. Simple triggers survive.

### What Needs Attention

**Integration Testing Gap**: Unit tests with mocked databases hide persistence gaps. Need more E2E tests that verify actual database state.

**Multi-Tenancy as Foundational**: This should have been caught earlier. The Oct 2025 multi-user commit was incomplete - storage updated, retrieval forgotten.

---

## My Activity This Week

| Date | Session | Key Output |
|------|---------|------------|
| Jan 26 | ADR-049/050 Guidance | MVP vs V2 rubric, memo to Lead Dev |
| Jan 30 | Multi-tenancy Guidance | 6-question response, ADR-058 recommended |

**Pending items**: None. All requests addressed.

---

## Looking Ahead

### Immediate (Next Week)

1. **#734 Multi-tenancy refactor** - Lead Dev executing with my guidance
2. **Verify #736 fix** - Re-test project onboarding with migration applied
3. **Session singleton debug** - Trace why onboarding sessions disappear between messages
4. **Continue E2E alpha testing** - More flows to validate
5. **Two-sidebar decision** - PM to determine if duplicate functionality

### Architectural Priorities

1. **ADR-058**: Document multi-tenancy isolation architecture (Lead Dev to draft)
2. **Persistence layer audit**: Consider adding to epic completion checklist
3. **Integration test coverage**: E2E tests that verify database state

---

## Metrics Summary

| Metric | This Week |
|--------|-----------|
| Issues Closed | ~74 |
| Issues Created | ~37 (including 19 bugs from alpha testing) |
| Tests Added | ~2,200 |
| Test Suite Total | 5,253 |
| Releases | 1 (v0.8.5) |
| ADRs Decided | 2 (049, 050) |
| P0 Bugs Found | 1 (#728, root cause #736) |
| P1 Bugs Fixed | 2 (#731, #736) |
| Systemic Gaps Identified | 1 (#734 multi-tenancy) |
| Parallel Agent Deployments | 3 (Jan 29 investigation) |

---

## Closing Assessment

**Week character**: Build velocity was excellent (Jan 23-27), alpha testing revealed hidden gaps (Jan 28), and systematic investigation began finding root causes (Jan 29). The arc is healthy: build → ship → discover → diagnose → fix.

**The good news**: We found these issues during alpha, not after launch. Root causes are being identified (not just symptoms patched). The methodology is working.

**The sobering news**: Oct 2025 multi-user implementation was incomplete. Some paths use user scoping, others don't. This has been lurking for months.

**The work ahead**: #734 multi-tenancy refactor is substantial but PM has approved proper foundation-building over racing to dates. This is the right call.

---

*Weekly review complete. Available for questions or deeper discussion on any topic.*
