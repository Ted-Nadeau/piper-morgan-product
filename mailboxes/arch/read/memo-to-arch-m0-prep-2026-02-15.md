# Memo: M0 Sprint Preparation — Lead Developer Prompt Request

**From**: Chief of Staff + PM
**To**: Chief Architect
**Date**: February 15, 2026
**Re**: Preparing the Lead Developer for M0 Conversational Glue sprint kickoff

---

## Context

The PM is preparing to resume development work after a two-week period dominated by flu recovery, stabilization releases (v0.8.5.2, v0.8.5.3), and content production. End-to-end alpha testing shows no new issues — the foundation is stable.

M0 (Conversational Glue) is the next sprint. Planning is complete, issues are defined, CXO and Architect reviews are on record. What we need now is a well-prepared Lead Developer session that starts clean and doesn't have to rediscover context.

We'd like you to draft the Lead Developer prompt for the M0 kickoff, following our cathedral doctrine and the established prompt template. Below are the priorities and guidance we'd like incorporated.

---

## Recommended Issue Sequencing

**Start with GLUE-MAINPROJ** (1-2 days). Rationale:
- Smallest issue, known pain point every tester hits
- Clean win to rebuild development momentum after extended non-dev period
- Low risk, high confidence — good re-entry point

**Then GLUE-SLOTFILL or GLUE-FOLLOWUP** based on your assessment of dependency order and technical risk. We defer to your judgment on sequencing the remaining four issues.

---

## Pre-Sprint Verification Requests

Before building on existing infrastructure, we'd like the Lead Dev to verify:

1. **#595 multi-intent foundation**: Confirm the `MultiIntentResult`, `detect_multiple_intents()`, and `classify_multiple()` infrastructure works in the current codebase. A quick smoke test against the 27 existing tests in `test_multi_intent.py` before starting GLUE-MULTIINTENT.

2. **ConversationContext current state**: M0 extends `ConversationContext` with `current_lens` and other fields. Verify the current shape of that class and any changes since the implementation guide was written (Feb 1).

3. **Schema/migration health**: Given the missing migrations discovered this cycle (products, features, work_items tables), confirm no similar gaps exist for conversation-related tables.

---

## Implementation Guidance to Convey

- **Re-read `conversational-glue-implementation-guide.md`** (~4,500 words, Feb 1). This is the source of truth for M0 design intent.
- **CXO anti-patterns are real constraints**: "Scripted Enthusiasm," "Over-Explaining the Obvious," and the **Colleague Test** ("Would a colleague respond this way?") apply to every issue.
- **Sprint gate checks at each issue close.** Use the sprint gate template (Feb 3). We want evidence-based completion, not 75% pattern.
- **B2 quality gate is the M0 exit criterion**: naturalness ≥4/5 from alpha testers, follow-up resolution >90%, compound query handling >85%.

---

## What We're Asking

**Please draft a Lead Developer prompt** for the M0 kickoff session that:

1. Establishes the sprint context (what M0 is, why it matters, where we are)
2. Specifies GLUE-MAINPROJ as the starting issue
3. Includes the verification steps above as pre-sprint checks
4. References the implementation guide, PDR-002 v3, and CXO review notes
5. Sets the tone: methodical re-entry after a break, not a rush to catch up
6. Follows the `agent-prompt-template.md` format

The PM will review your draft before the first Lead Dev session. No rush — M0 kickoff is likely tomorrow (Monday is a federal holiday) or later this week, depending on PM's readiness.

---

## One More Thing

The PM has been away from implementation work for roughly two weeks. The prompt should account for that — not by dumbing anything down, but by ensuring the Lead Dev doesn't assume shared context from recent sessions that didn't happen. Fresh eyes, clean start.

---

*Thanks. We're looking forward to getting back to building.*
