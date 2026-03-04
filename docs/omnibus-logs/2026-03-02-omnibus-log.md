# Omnibus Log: March 2, 2026

**Day**: Monday
**Sessions**: 2 (Lead Developer, CIO)
**Day Rating**: **BUG RESOLUTION + INNOVATION** — Lead Dev resolves systemic error contract regression (#875) and workflow polling defect (#878), closing 5 issues. CIO reviews innovation backlog, identifies "synthesis layer as infrastructure" as cross-cutting theme.

**Git Commits**: None (all work uncommitted on `claude/m0-conversational-glue`)

---

## Sessions Overview

| Start | Role | Duration | Primary Focus |
|-------|------|----------|---------------|
| 7:09 AM | Lead Developer | ~11 hrs | #875 smoke test, #876 audit, #878 fix, 5 issues closed |
| 5:40 PM | CIO | ~25 min | Innovation backlog review (3 articles, 3 ideas) |

---

## Unified Chronological Timeline

- 7:09 AM: **Lead Developer** resumes from Mar 1 carry-over — uncommitted fixes for #871 (header cleanup) and #875 (error response contract) pending PM smoke test
- ~7:15 AM: **Lead Developer** begins #876 audit cascade — 54+ raw error messages in `intent_service.py` across 30+ handler methods
- ~7:30 AM: **Lead Developer** delivers #876 findings — 4 categories: 27 raw exception leaks (Category A), 17 technical validation (B), 4 infrastructure/timeout (C), 8+ already conversational (D). Recommends `safe_intent_handler` decorator. ~9 hrs estimated.
- 7:49 AM: **PM** delivers smoke test results — Test 1: partial success (extraneous workflow triggered), Test 3: "An API error occurred" (red error box)
- ~7:55 AM: **Lead Developer** investigates Test 3 — root cause: server PID 41689 started Mar 1 3:59 PM, running pre-fix code. Kills old process, restarts. Test 3 now passes.
- ~8:00 AM: **Lead Developer** investigates extraneous workflow — discovers unhandled action fallback returns `workflow_id` but `error=None`, bypassing polling guard. Files #878.
- ~8:05 AM: **Lead Developer** discovers classifier non-determinism — no `temperature=0`, same message routes differently each call
- ~8:10 AM: **Lead Developer** discovers `GitHubIntegrationRouter.create_issue()` missing `assignees` parameter — pre-existing bug blocking all issue creation via intent. Files #879.
- ~8:15 AM: **Lead Developer** files #880 — Calendar credential setup fails with 401 Unauthorized (from CXO Mar 1 bug report)
- 5:19 PM: **PM** delivers re-test results — Test 1: routes to STRATEGY → raw error (Category A, #876 scope), Test 3: Pass, Test 4: Pass
- ~5:30 PM: **Lead Developer** begins #878 audit cascade — discovers **75 code paths** return workflow_id with error=None (not just 2). Architectural: `process_intent` creates workflow for ALL intents.
- ~5:45 PM: **Lead Developer** implements #878 fix (4 changes): `intent_service.py` ×2 (unhandled EXECUTION + generic STRATEGY → `workflow_id=None`), `intent.py` (strip workflow_id on failure/clarification), `chat.js` (add `!requires_clarification` guard)
- ~6:00 PM: **Lead Developer** verifies #878 — 11 integration tests pass, curl tests confirm `workflow_id: null` for planning and bug report queries
- ~6:15 PM: **Lead Developer** closes 5 issues with evidence: #875 (systemic error contract), #872 (planning raw error), #873 (workflow timeout), #874 (API error on issue query), #878 (extraneous workflow polling)
- 5:40 PM: **CIO** starts session — PM shares 3 innovation backlog items for analysis
- ~5:45 PM: **CIO** analyzes "Death of the AI Wrapper" (Collins/Medium) — validates Piper's domain model + entity relationships as moat, not LLM layer. "Skate to the puck" = Time Lord philosophy.
- ~5:50 PM: **CIO** analyzes Knowledge Graph Extraction Challenges (Yáñez Romero/Medium) — coreference problem maps to Piper's future entity extraction. Asserted vs. augmented graph maps to trust/provenance architecture.
- ~5:55 PM: **CIO** analyzes Jesse Vincent's Engineering Notebook (Prime Radiant) — convergent evolution with omnibus system. Automated JSONL ingestion vs. our manual Docs agent synthesis. We're ahead on cross-agent coordination; he's ahead on automation.
- ~6:00 PM: **CIO** identifies cross-cutting theme: **"The synthesis layer is becoming a first-class infrastructure concern."** Value isn't in the LLM call — it's in accumulated context over time.
- ~6:05 PM: **CIO** generates 3 ideas: (1) blog post comparing omnibus with Vincent's eng-notebook, (2) mail automation (web-to-mailbox bridge is specific bottleneck), (3) engineering-notebook evaluation to supplement omnibus
- ~6:30 PM: **Lead Developer** wraps session — 6 open items for tomorrow including committing all work, #876 implementation, #879 quick fix

---

## Executive Summary

### Lead Developer: Systemic Bug Resolution Day

The day centered on resolving the Nov 2025 error contract regression (#875) and its cascading effects. The fix itself was applied Mar 1, but PM smoke testing on Mar 2 revealed two additional issues:

1. **Stale server** — Test 3 failure was simply the old server process (pre-fix) still running. Restart resolved it immediately.
2. **#878 Workflow polling** — What appeared to be a 2-path bug turned out to be **75 code paths** returning `workflow_id` with `error=None`. Root cause: architectural — `process_intent` creates a workflow for ALL intents, but no handler actually starts async work. Fixed with 4 targeted changes (2 in intent_service, 1 in route layer, 1 in frontend).

**5 issues closed**: #872, #873, #874, #875, #878 — all with evidence and verification.

**3 new issues filed**: #878 (fixed same day), #879 (create_issue missing assignees param), #880 (calendar credential 401).

**#876 Audit delivered**: 54+ raw error messages categorized into 4 tiers. Recommended `safe_intent_handler` decorator for 27 Category A exception leaks. ~9 hours estimated work.

**Key finding**: The #878 audit cascade pattern (discovering 75 paths when investigating 2) exemplifies why audit cascades matter — surface symptoms rarely reveal full scope.

### CIO: Innovation Backlog Review

Short but substantive session analyzing 3 PM-collected articles:

- **"Death of the AI Wrapper"**: External validation of Piper's infrastructure-first approach
- **KG Extraction Challenges**: Pipeline error propagation relevant to future entity extraction design
- **Jesse Vincent's Engineering Notebook**: Convergent evolution with omnibus system — same problem, different angles

**Cross-cutting theme**: "The synthesis layer is becoming a first-class infrastructure concern." All three articles independently point to accumulated context over time as the value layer, not the LLM call itself.

**3 actionable ideas**: Blog post (omnibus vs eng-notebook), mail automation (web-to-mailbox bridge bottleneck), eng-notebook evaluation (supplement omnibus lower layer).

---

## Day Metrics

| Metric | Value |
|--------|-------|
| Sessions | 2 |
| Issues closed | 5 (#872, #873, #874, #875, #878) |
| Issues filed | 3 (#878, #879, #880) |
| Commits | 0 (work uncommitted) |
| Code paths audited | 75 (#878) + 54 (#876) |
| Innovation items reviewed | 3 |

---

## Decisions Made

1. **#876 approach**: `safe_intent_handler` decorator for Category A (27 exception leaks), validation helper library for Category B (17 technical messages)
2. **#878 fix scope**: Targeted 4 changes rather than stripping workflow_id from all 75 paths (conservative approach)
3. **Mail automation**: Identified web-to-mailbox bridge as specific bottleneck (CIO idea, not yet prioritized)

---

## Open Items Carried Forward

| Item | Owner | Status | Next Step |
|------|-------|--------|-----------|
| Commit #871/#875/#878 | Lead Dev | Uncommitted | Commit to branch |
| #876 raw error humanization | Lead Dev | Audited (~9 hrs) | PM to prioritize |
| #879 create_issue assignees | Lead Dev | Filed | Quick fix |
| #880 Calendar credential 401 | Lead Dev | Filed | PM to triage |
| Pattern-062 review | PM | Draft complete | PM review, then commit |
| Mollick + KG article citations | Docs | Pending | Next docs cycle |
| Blog post: omnibus vs eng-notebook | CIO/Comms | Idea | Outline when PM ready |
| Mail automation | CIO | Idea | Map workflow, evaluate |
| Eng-notebook evaluation | CIO | Idea | Review tool |

---

## Source Logs

1. `dev/2026/03/02/2026-03-02-0709-lead-code-opus-log.md`
2. `dev/2026/03/02/2026-03-02-1740-cio-opus-log.md`
