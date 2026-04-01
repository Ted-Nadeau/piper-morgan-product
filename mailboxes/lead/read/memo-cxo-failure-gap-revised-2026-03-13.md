# Memo: CXO Assessment — Canonical Retest Failure Gap (REVISED)

**To**: PM, PPM, Lead Developer
**From**: CXO
**Date**: 2026-03-13 (revised, supersedes earlier gap analysis)
**Re**: #884 canonical retest — query-level failure analysis with roadmap mapping

---

## Correction

My earlier gap analysis assumed 8 of the 10 failures were hijack-related (#888/#889). **That was wrong.** The Run 4 test data shows the hijack was bypassed via data seeding — all 10 failures are genuine routing or integration issues independent of the hijack bugs. The actual gap is larger than I initially estimated.

The corrected picture:

| Category | Count | Post-hijack-fix projection |
|----------|-------|---------------------------|
| Routing failures | 9 | 9 (unchanged — not hijack-related) |
| Integration failures | 1 | 1 (unchanged) |
| Not implemented (graceful) | 8 | 8 (unchanged) |
| Hijack bugs (#888/#889) | not in Run 4 data | 0 (once fixed) |
| **Total non-passing** | **18/61** | **18/61** |
| **Passing** | **43/61 (70.5%)** | **43/61 (70.5%)** |

**Fixing the hijack issues won't change the pass rate** — the test already bypassed them. The 10 impl failures are the real work.

---

## The 10 Failures — Detailed Assessment

### Debatable Classification (1 failure)

**Q2: "What can you help me with?" → got `discovery`, expected `identity`**

This one I'd actually argue is *correctly* routed. The user is asking about capabilities — `discovery` is the handler that shows capabilities. The test expected `identity`, but the response content is appropriate: it lists core capabilities and available integrations. I'd recommend updating the test expectation rather than changing the routing.

**CXO verdict**: Reclassify as PASS. Update test expectations.

### Classifier Keyword Collisions (5 failures)

These share a common root cause: the intent classifier latches onto a keyword and routes to the wrong handler.

| Query | Keyword Trigger | Got | Should Be | Problem |
|-------|----------------|-----|-----------|---------|
| Q33: "Find time for a 1:1 with the team lead" | "time" | temporal | execution | "Time" → temporal handler, but user wants calendar scheduling |
| Q40: "Update the project roadmap document" | "project" | portfolio | execution | "Project" → portfolio handler, but user wants document editing |
| Q43: "What's blocking the milestone?" | "milestone" | status | analysis | "Milestone" → status handler, but user wants analysis |
| Q62: "Check my calendar for conflicts" | "calendar" | temporal | query | "Calendar" → temporal handler, but user wants calendar query |
| Q27: "Tell me more about the GitHub integration" | "about" | identity | query | "About" → identity handler ("tell me about yourself"), but user wants feature info |

These are all cases where a surface keyword overrides the actual user intent. The classifier needs to weigh context and sentence structure, not just individual trigger words.

**CXO verdict**: These are real UX bugs. A user asking "What's blocking the milestone?" and getting a project status dump instead of a blocker analysis will feel unheard. Same Colleague Test failure as the hijack — Piper isn't responding to what the user actually asked.

**Roadmap mapping**: Not explicitly covered by any existing issue. These are intent classifier refinement — they could be scoped as child issues of #884, or as a new "classifier accuracy" issue. The pattern work in #884 (canonical retest) was meant to surface exactly this kind of problem, so this is working as intended. The question is: where do the fixes land?

**Recommendation**: File a new issue (or child of #884) for classifier keyword disambiguation. Scope for M1 if the fixes are small (pattern priority tuning), M2 if they require structural classifier changes.

### Predictive Category Routing (3 failures)

| Query | Got | Should Be |
|-------|-----|-----------|
| Q23: "What risks should I be aware of?" | guidance | analysis |
| Q24: "What opportunities should I pursue?" | priority | synthesis |
| Q25: "What's the next milestone?" | priority | planning |

These are analytically sophisticated queries that the classifier routes to simpler handlers. "What risks?" goes to guidance (which gives time-of-day advice) instead of analysis (which should assess project risk). "What opportunities?" goes to priority (which says "no priorities configured") instead of synthesis.

**CXO verdict**: These are real failures, but they're also at the boundary of what the current system can do. The handlers these SHOULD route to (analysis, synthesis, planning) exist but may not have the depth to answer these questions well yet. Routing them correctly is necessary but not sufficient — the destination handlers also need enrichment.

**Roadmap mapping**: Covered by M3 issues:
- #496 CANONICAL-#9: Priority queries
- #497 CANONICAL-#10: Focus guidance synthesis
- #372 Learning (deferred to M3) — provides the pattern recognition that makes Q22-Q25 meaningful

**Recommendation**: Accept as known M3 work. For M1, consider whether routing them to a better fallback (e.g., "I can see you're asking about risks — that's something I'll be able to help with as I learn more about your project patterns") would be better than the current silent misroute.

### Integration Failure (1 failure)

**Q16: "Create a GitHub issue about testing" → correct routing (execution), but API returned no response**

This routed correctly to the execution handler, and the user got a friendly error: "I ran into something while creating a new issue. Something unexpected happened." The routing is fine; the GitHub API call failed.

**CXO verdict**: Not a UX design issue — this is a backend/integration bug. The error message itself passes the Colleague Test (it's friendly, offers retry). The fix is in the GitHub integration layer.

**Roadmap mapping**: Likely a test environment issue (the canonical-test account may not have a real GitHub token configured). If this reproduces in production with real credentials, it's a bug in the GitHub integration. Either way, not a CXO concern.

**Recommendation**: Lead Dev to verify whether this is a test environment artifact or a real bug. If real, file as GitHub integration issue.

---

## The 8 Not-Implemented — Revised Assessment

Good news: **all 8 have graceful fallbacks.** They all return "I don't have that capability yet, but I'm learning!" with a suggestion to ask what Piper can do. No crashes, no errors, no dead-ends.

| Query | Category | Roadmap Item | Sprint |
|-------|----------|-------------|--------|
| Q31: Schedule a meeting | Scheduling | #790 (Trust-gated calendar) | M2 |
| Q32: Remind me to review PRs | Scheduling/Reminders | **Not planned** | — |
| Q36: Create a doc from conversation | Documents | #302, #355 | M4 |
| Q44: Create issues from meeting notes | GitHub Ops | #315 (Core Skills Library) | M3 |
| Q45: Close completed issues | GitHub Ops | Not explicitly planned | — |
| Q48: Post update to Slack channel | Slack | #244 (Interactive Slack) | M5 |
| Q55: Complete a todo | Todos | **Not planned** | — |
| Q63: Upload file to knowledge base | Knowledge | #302 (Document Processing) | M4 |

**Unplanned gaps (3):**
1. **Reminders** (Q32) — "Remind me to X" is a natural PM workflow with no roadmap coverage
2. **Todo completion** (Q55) — Todo add and list work, but marking complete doesn't. Part of the broader todo gap I flagged earlier
3. **Close GitHub issues** (Q45) — We can create issues but not close them. Users will expect symmetry

### Fallback Quality Assessment

The generic fallback message passes minimum bar but fails the Colleague Test for specificity. "I don't have that capability yet" is one-size-fits-all. A colleague would be more contextual:

| Current | Colleague-level |
|---------|----------------|
| "I don't have that capability yet, but I'm learning!" | "I can't schedule meetings yet — Google Calendar write access is on my roadmap. Want me to create a GitHub issue to track this meeting instead?" |
| (same generic message) | "I can't set reminders yet. Want me to add a todo for 'review PRs' so it shows up in your task list?" |

**Recommendation**: Contextual fallbacks for the 8 not-implemented queries would be a good #886 (UI Polish) candidate. Low effort, high perceived quality.

---

## Revised Summary

| Category | Count | Roadmap Status | Action |
|----------|-------|----------------|--------|
| Reclassify as PASS (Q2) | 1 | N/A | Update test expectations |
| Classifier keyword collisions | 5 | **Not planned** | New issue needed (M1 or M2) |
| Predictive routing | 3 | M3 (#496, #497, #372) | Accept as M3 work; consider better fallback |
| Integration failure (Q16) | 1 | Verify if test artifact | Lead Dev to investigate |
| Not-impl (roadmap covered) | 5 | M2–M5 | No action needed |
| Not-impl (unplanned) | 3 | **Not planned** | Add to backlog |
| Graceful fallback quality | 8 | #886 (UI Polish) | Contextual fallbacks |

### New Roadmap Items Needed

1. **Classifier keyword disambiguation** — 5 routing failures caused by keyword triggers overriding user intent. Scope TBD based on Lead Dev assessment of fix complexity.
2. **Todo management completion** (Q55) — Add/list works, complete doesn't. Target M3.
3. **Reminders** (Q32) — Natural PM workflow, no coverage. Target M3 or M5.
4. **GitHub issue close** (Q45) — Create/update exists, close doesn't. Target M3.

### Corrected Pass Rate Projections

| Scenario | Projected Rate |
|----------|---------------|
| Current (Run 4) | 43/61 (70.5%) |
| + Hijack fixes (#888/#889) | 43/61 (70.5%) — no change, wasn't measured |
| + Q2 reclassified as PASS | 44/53 impl (83.0%) |
| + Classifier fixes (5 queries) | 49/53 impl (92.5%) |
| + Q16 integration fix | 50/53 impl (94.3%) |
| + Predictive routing (M3) | 53/53 impl (100%) |

The realistic M1 target is **~92% impl pass rate** if the classifier keyword collisions can be addressed this sprint.

---

*CXO Memo (Revised) | March 13, 2026*
*Supersedes: memo-cxo-failure-gap-analysis-2026-03-13.md*
