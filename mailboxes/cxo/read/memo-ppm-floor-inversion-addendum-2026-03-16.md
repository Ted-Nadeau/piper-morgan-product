# Addendum: Floor Inversion Synthesis — Canonical Retest Implications

**To**: Lead Developer
**CC**: PM, Chief Architect, CXO
**From**: PPM
**Date**: 2026-03-16
**Re**: Supplement to `memo-ppm-floor-inversion-synthesis-2026-03-16.md` based on CXO failure gap analysis
**Status**: Additional guidance — does not change existing synthesis, adds to it

---

## Why This Addendum

The CXO's revised failure gap analysis (`memo-cxo-failure-gap-revised-2026-03-13.md`) was written before the floor inversion work began. Now that floor-first routing is the direction, several of the CXO's findings have different implications for your work. This addendum connects the failure gap data to the migration plan.

---

## Immediate Actions (Add to Current Work)

### 1. Update Q2 Test Expectation

Q2 ("What can you help me with?") was classified as a failure because the test expected `identity` but got `discovery`. The CXO assessed this as correctly routed — the user is asking about capabilities, and the discovery handler shows capabilities. Update the test expectation to accept `discovery` for this query. This changes the impl baseline from 43/53 to 44/53 (83.0%).

### 2. Investigate Q16 Integration Failure

Q16 ("Create a GitHub issue about testing") routed correctly to execution but the GitHub API returned no response. Determine whether this is a test environment artifact (canonical-test account lacks real credentials) or a real bug. If real, file as a GitHub integration issue.

### 3. Re-run Canonical Retest After Phase 2-3 Migration

This is the most important new action. The CXO's analysis identified 5 keyword collisions and 3 predictive routing failures. Under floor-first routing, most of these produce acceptable experiences because the misclassified query reaches the floor with context instead of the wrong template.

Run the full canonical test suite after Phase 2-3 floor migration to establish the actual post-inversion pass rate. This replaces projection with measurement and tells us whether the classifier keyword work is still needed for read-only categories.

**Expected outcome**: ~90%+ on implemented queries from floor routing alone, without classifier changes.

---

## Revised Classifier Work Scope

The CXO identified 5 classifier keyword collisions. Under floor-first routing, the urgency changes:

| Query | Misroute | Floor Handles It? | Classifier Fix Still Needed? |
|-------|----------|-------------------|------------------------------|
| Q33: "Find time for a 1:1" | time → temporal | Yes (temporal is read-only → floor) | No — floor with calendar context is adequate |
| Q40: "Update the project roadmap" | project → portfolio | **No** (portfolio has write actions → canonical) | **Yes — real misroute to wrong action handler** |
| Q43: "What's blocking the milestone?" | milestone → status | Yes (status is read-only → floor) | No — floor with project context is adequate |
| Q62: "Check my calendar for conflicts" | calendar → temporal | Yes (temporal-calendar → floor) | No — floor with calendar context is adequate |
| Q27: "Tell me about GitHub integration" | about → identity | Yes (adjacent identity → floor) | No — floor with integration context is adequate |

**Only Q40 requires a classifier fix.** The other 4 are adequately handled by the floor. This means the classifier keyword disambiguation issue — if filed — should be scoped to **side-effect category misroutes only**, not all keyword collisions.

The principle: classifier accuracy matters most for routing *actions* correctly. For read-only *conversations*, the floor provides adequate coverage regardless of classification category.

---

## Floor Quality Verification Points

When running the post-migration canonical retest, pay specific attention to these queries as quality indicators for the floor:

**Keyword collision queries (should produce good floor responses):**
- Q33: "Find time for a 1:1 with the team lead" — floor should discuss scheduling, offer to check calendar
- Q43: "What's blocking the milestone?" — floor should attempt blocker analysis with project context
- Q62: "Check my calendar for conflicts" — floor should discuss calendar with assembled calendar data
- Q27: "Tell me more about the GitHub integration" — floor should describe integration capabilities

**Predictive routing queries (should improve over templates):**
- Q23: "What risks should I be aware of?" — floor should discuss project risks, not give time-of-day advice
- Q24: "What opportunities should I pursue?" — floor should discuss opportunities with project context
- Q25: "What's the next milestone?" — floor should discuss milestone status with project data

**Not-implemented queries (should engage, not deflect):**
- Q31: "Schedule a meeting" — floor should discuss scheduling and suggest alternatives
- Q32: "Remind me to review PRs" — floor should suggest todo as alternative
- Q45: "Close completed issues" — floor should discuss which issues and suggest commands

These queries are the floor's report card. If they produce good responses, the floor inversion is working. If they're shallow or generic, the Context Assembler needs enrichment for those categories.

---

## What This Doesn't Change

Everything in the main synthesis stands. This addendum adds:
- Two concrete immediate actions (Q2 test update, Q16 investigation)
- A post-migration canonical retest as a required milestone
- Revised scope for classifier work (side-effect misroutes only)
- Specific quality verification points for the retest

---

*PPM Addendum | March 16, 2026*
