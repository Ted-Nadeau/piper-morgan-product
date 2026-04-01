# Memo: PPM Response — How Floor Inversion Changes the Failure Gap Analysis

**To**: CXO
**CC**: Lead Developer, PM, Chief Architect
**From**: PPM
**Date**: 2026-03-16
**Re**: Revised assessment of #884 failure gap in light of floor-first routing (#911)
**Input**: `memo-cxo-failure-gap-revised-2026-03-13.md` (CXO, 2026-03-13)

---

## Context

The CXO's revised failure gap analysis was written on March 13, before the floor inversion work began. Since then, the team diagnosed and began implementing a fundamental routing change: read-only queries default to the conversational floor with assembled context rather than to canonical template handlers (#911). This changes the impact assessment for several failure categories.

This memo is not a correction of the CXO's analysis — it was accurate as of March 13. It's an update mapping the failure categories onto the new architecture.

---

## What Changes

### Classifier Keyword Collisions (5 failures) — Severity Reduced

The CXO identified 5 queries where a surface keyword overrides user intent:

| Query | Misroute | Under Floor-First |
|-------|----------|-------------------|
| Q33: "Find time for a 1:1 with the team lead" | "time" → temporal | Temporal is read-only → hits floor with calendar context. Floor engages with scheduling need. |
| Q40: "Update the project roadmap document" | "project" → portfolio | Portfolio has WRITE actions → still hits canonical. **This one doesn't change.** |
| Q43: "What's blocking the milestone?" | "milestone" → status | Status is read-only → hits floor with project context. Floor attempts blocker analysis. |
| Q62: "Check my calendar for conflicts" | "calendar" → temporal | Temporal-calendar → hits floor with calendar context. Floor checks for conflicts conversationally. |
| Q27: "Tell me more about the GitHub integration" | "about" → identity | Adjacent identity → hits floor with integration context. Floor describes GitHub integration. |

Under floor-first routing, 4 of 5 keyword collisions produce acceptable experiences because the misclassified query reaches the floor with relevant context rather than the wrong template. The floor responds to what the user actually asked, regardless of which category the classifier chose.

**Q40 remains a real issue** because "update the project roadmap document" hits PORTFOLIO, which has write actions and stays canonical under the Action Gate. The user wants document editing, not portfolio management. This is a genuine misroute that the floor can't catch.

**Revised recommendation**: The classifier keyword disambiguation issue should still be filed, but scoped to side-effect categories where misclassification routes to the wrong *action handler* (like Q40). For read-only misclassifications, the floor provides adequate coverage. This reduces the urgency from "5 UX bugs" to "1 real misroute + 4 that the floor handles."

### Predictive Category Routing (3 failures) — Likely Resolved

| Query | Old Route | Under Floor-First |
|-------|-----------|-------------------|
| Q23: "What risks should I be aware of?" | Guidance template (time-of-day advice) | Floor with project context → attempts risk analysis conversationally |
| Q24: "What opportunities should I pursue?" | Priority template ("no priorities configured") | Floor with project/priority context → discusses opportunities |
| Q25: "What's the next milestone?" | Priority template | Floor with project context → discusses milestone status |

All three are read-only queries that will hit the floor under the new routing. The floor with project context can engage meaningfully with "what risks?" in a way the GUIDANCE template never could. These aren't M3 problems anymore — they're floor quality problems, and the quality depends on the Context Assembler providing good project data.

**Revised recommendation**: Re-test these after Phase 2-3 migration. If the floor handles them well, remove them from the M3 dependency. If the floor responses are too shallow (insufficient project context), then the M3 learning/analysis enrichment is still needed.

### Not-Implemented Queries (8 failures) — Experience Improved, Gaps Remain

The floor eliminates the deflection ("I don't have that capability yet") but doesn't add the missing capabilities. Under floor-first routing:

| Query | Old Experience | Floor Experience | Capability Still Missing? |
|-------|---------------|-----------------|--------------------------|
| Q31: Schedule a meeting | Deflection | Discusses scheduling, suggests alternatives | Yes — no calendar write |
| Q32: Remind me to review PRs | Deflection | Discusses task, suggests todo as alternative | Yes — no reminders |
| Q36: Create doc from conversation | Deflection | Discusses approach, suggests manual steps | Yes — no doc generation |
| Q44: Create issues from meeting notes | Deflection | Discusses extraction approach, offers to create individual issues | Partial — can create issues, not from notes |
| Q45: Close completed issues | Deflection | Discusses which issues to close, suggests commands | Yes — no issue close API |
| Q48: Post update to Slack | Deflection | Discusses update content, suggests copy for manual post | Yes — no Slack write |
| Q55: Complete a todo | Deflection | Discusses task, may attempt action | Yes — no todo complete |
| Q63: Upload file to knowledge base | Deflection | Discusses knowledge management approach | Yes — no file upload |

The user experience improves significantly — Piper engages with the need instead of deflecting. But the underlying capabilities are still missing. The three unplanned gaps (reminders, todo completion, GitHub issue close) still belong on the backlog.

**Revised recommendation**: The CXO's contextual fallback suggestions (bottom of the original memo) are now the floor's natural behavior, not a separate implementation task. The floor with voice guidance ("suggest alternative actions, never deflect") produces the colleague-level responses the CXO described. No separate #886 UI Polish work needed for these 8 queries.

### Unchanged

- **Q2 reclassification**: Still correct — update test expectation, classify as PASS.
- **Q16 integration failure**: Still needs Lead Dev investigation — test environment artifact or real bug.
- **Backlog items** (reminders, todo completion, GitHub issue close): Still needed regardless of floor.

---

## Revised Pass Rate Projections

The CXO projected a 92.5% M1 target assuming classifier fixes for 5 keyword collisions. Under floor-first routing, the picture shifts:

| Scenario | Old Projection | Revised Projection |
|----------|---------------|-------------------|
| Current (Run 4) | 43/61 (70.5%) | 43/61 (70.5%) |
| + Q2 reclassified | 44/53 impl (83.0%) | 44/53 impl (83.0%) |
| + Floor-first for read-only misroutes (4 of 5 keyword collisions) | N/A | ~48/53 impl (~90.6%) |
| + Q40 classifier fix (side-effect misroute) | N/A | ~49/53 impl (~92.5%) |
| + Q16 integration fix | N/A | ~50/53 impl (~94.3%) |
| + Floor handles predictive queries (Q23-25) | N/A | ~53/53 impl (~100%) |

The floor-first routing may get us to ~90%+ on implemented queries *without* classifier changes, because read-only misclassifications produce good floor responses instead of wrong-handler template responses. The remaining work is: one real classifier fix (Q40), one integration investigation (Q16), and quality verification on floor responses for the predictive queries.

**Recommended action**: Re-run the full canonical retest after Phase 2-3 floor migration to establish the actual post-inversion pass rate. This replaces projection with measurement.

---

## Summary

| CXO Category (Mar 13) | Revised Status (Mar 16) |
|------------------------|------------------------|
| 5 classifier keyword collisions | 4 handled by floor; 1 real misroute (Q40) remains |
| 3 predictive routing failures | Likely resolved by floor; re-test after Phase 2-3 |
| 8 not-implemented deflections | Floor engages instead of deflecting; capability gaps remain on backlog |
| 8 contextual fallback suggestions | Subsumed by floor voice guidance; become test expectations |
| 92.5% M1 target | Achievable via floor routing alone for most failures |

The floor inversion doesn't eliminate the need for classifier improvement — side-effect misroutes (Q40) are still real bugs. But it dramatically reduces the urgency of classifier accuracy for read-only queries, because the floor produces good responses regardless of classification category. The classifier becomes most important for routing *actions* correctly, not for routing *conversations*.

---

*PPM Memo | March 16, 2026*
