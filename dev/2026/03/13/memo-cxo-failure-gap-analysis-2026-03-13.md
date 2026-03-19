# Memo: CXO Assessment — Canonical Retest Failure Gap Analysis

**To**: PM
**From**: CXO
**Date**: 2026-03-13
**Re**: #884 canonical retest — what's in the remaining 19% and does the roadmap cover it?

---

## The Numbers

From the Lead Dev's Run 4 on March 12:

| Metric | Value |
|--------|-------|
| Total queries tested | 61 |
| Implemented queries | 53 |
| Passing (impl) | 43/53 (81.1%) |
| Failing (impl) | 10 |
| Not implemented | 8 |

The 10 impl failures break down as:

- **8 failures from hijack** (#888/#889) — now addressed by PPM direction memo
- **2 failures from other causes** — likely among #895–#898

So once the hijack fixes ship, projected impl pass rate is **~51/53 (96.2%)**. That's a strong number for M1 Phase 1 diagnostics.

---

## Gap 1: The 2 Non-Hijack Impl Failures

These are the most important unknowns. I don't have the specific query-level detail from the retest — the Lead Dev filed #895–#898 but the omnibus log doesn't describe which canonical queries they correspond to or what the failure modes are.

**CXO ask**: Before I can assess whether these are experience-critical, I need the Lead Dev's test results at query level. Specifically:

- Which 2 implemented queries are still failing (by query number/text)?
- What's the failure mode — wrong handler, error response, partial response, crash?
- Are these among the 5 wiring fix issues that were closed (#890–#894) but maybe not fully resolved?

If these turn out to be edge cases in less-used handlers, they can ride the M1 wiring pass. If they're in high-frequency paths (identity, temporal, spatial, capability), they need immediate attention.

---

## Gap 2: The 8 Not-Implemented Queries

The canonical list has 63 queries. The retest covered 61 (2 apparently excluded). Of those 61, 8 have no handler at all.

From the December test matrix, the not-implemented categories were: Conversational (5), Scheduling (5), Documents (5), GitHub Ops (8), Slack (5), Productivity (3), Todos (4), Calendar Extended (2), Knowledge (1) — totaling 43 queries. Between December and March, implementation jumped from 19 to 53, so 34 queries were implemented during B1/A20/MUX/M0 sprints. That leaves 8 still without handlers.

I don't have the exact 8, but based on the implementation progression and what's most likely still missing, they probably cluster in:

- **Scheduling/Calendar** (#31–34) — Calendar creation, reminders, deconfliction, meeting time analysis. These require calendar write access, which isn't fully wired.
- **Todos** (#54–57) — Todo CRUD. Fundamental but requires a persistence layer we don't have yet.
- **Knowledge** (#63) — File upload/ingestion. Infrastructure-dependent.
- **Possibly some Conversational** (#26–30) — Contextual discovery, feature deep-dive. These are the "glue" queries that need the off-topic detection and discovery mechanisms.

### Roadmap Coverage Assessment

| Gap Category | Likely Queries | Roadmap Coverage | Sprint |
|--------------|---------------|------------------|--------|
| Scheduling/Calendar | #31–34 | #790 (Trust-gated calendar) | M2 |
| Todos | #54–57 | Not explicitly scoped | **Unplanned** |
| Knowledge/Files | #63 | #302, #355 (Document processing) | M4 |
| Conversational discovery | #26–30 | Off-topic detection (new issue from PPM memo) + #886 UI Polish | M1–M2 |
| Predictive gaps | #22–25 | #372 (Learning), #496, #497 | M1 (partial), M3 |

**Key finding**: Todo management (#54–57) appears to be the most significant unplanned gap. The December test matrix flagged it as a "fundamental functionality" alpha target, but I don't see dedicated issues for it in M1–M3. Todos are a natural PM workflow — "remind me to follow up on X" or "add to my task list" — and users will expect this to work.

Everything else maps to existing roadmap items, though spread across M2–M4.

---

## CXO Experience Assessment

From a user experience perspective, here's how I'd prioritize the gaps:

### Must-feel-good-now (M1 priority)

1. **Hijack fixes (#888/#889)** — Already addressed by PPM memo. First-impression critical.
2. **The 2 remaining impl failures** — Need identification. If they're in core paths, fix immediately.
3. **Conversational discovery queries (#26–30)** — "What else can you help with?" and "How do I use X?" are exactly the Pattern-045 discovery problem. The off-topic detection issue from the PPM memo partially addresses this. #886 (UI Polish) may cover surface-level discovery.

### Should-work-by-beta (M2–M3)

4. **Todo management** — Users will try this. Graceful fallback ("I can't manage todos yet, but I can help you create a GitHub issue to track that") is acceptable for alpha. But this needs to be on the roadmap explicitly.
5. **Predictive queries (#22–25)** — "What patterns do you see?" and "What risks should I be aware of?" These are what make Piper a colleague rather than a tool. #372 (Learning) covers the foundation; #496 and #497 in M3 cover the queries.

### Can-wait (M4+)

6. **Calendar write operations** — Read works; write is M2 territory with #790.
7. **Document management** — M4 is the right place for this coherent set.
8. **Knowledge ingestion** — Infrastructure-dependent, M4.

---

## Recommendations

1. **Get query-level detail from Lead Dev.** I can't fully assess the gap without knowing which specific queries failed and why. The 2 non-hijack failures could be trivial or critical — I need to see them.

2. **Add a Todo management issue to the backlog.** This is the one significant gap I see that isn't covered by existing roadmap items. It doesn't need to be M1, but it should be explicitly scoped for M3 (which is "Canonical queries + Core skills") at latest.

3. **Verify the 8 not-impl queries have graceful fallbacks.** Even if we can't implement these yet, a user who asks "Remind me to check in with the team tomorrow" should get a helpful response ("I can't set reminders yet, but I can create a GitHub issue to track that — want me to?"), not a dead-end or an error. This is the Colleague Test applied to missing capabilities. If fallbacks aren't in place, that's a #886 (UI Polish) candidate.

4. **Update the canonical test matrix.** The December matrix is stale — it shows 19/63 when we're now at 53/61. The retest results should become the new baseline. This is probably a Docs task.

---

## Summary

| Gap | Size | Covered by Roadmap? | Action Needed |
|-----|------|---------------------|---------------|
| Hijack failures | 8 queries | Yes — PPM memo (#888/#889) | Implementation underway |
| Non-hijack impl failures | 2 queries | Unknown | Need Lead Dev detail |
| Not-implemented (scheduled) | ~4 queries | Yes — Calendar M2, Docs M4, Predictive M3 | No action |
| Not-implemented (conversational) | ~2 queries | Partially — off-topic detection + #886 | Monitor |
| Not-implemented (todos) | ~2 queries | **No** | Add to backlog (M3 target) |
| Graceful fallbacks for all gaps | All 8 not-impl | Unclear | Verify or add to #886 |

The 19% gap is mostly accounted for. The hijack fixes alone will bring us to ~96% on implemented queries. The not-implemented gaps are largely where the roadmap says they should be (M2–M4). The one hole is todo management, and the one unknown is the 2 non-hijack impl failures that need identification.

---

*CXO Memo | March 13, 2026*
