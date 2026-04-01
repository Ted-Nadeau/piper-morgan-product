# Memo: M1 Gate Issue #926 — Request for CXO & PPM Review

**To**: CXO, PPM
**CC**: PM (xian)
**From**: Lead Developer
**Date**: 2026-03-22
**Re**: Draft gate issue #926 needs your review before we run it
**Link**: https://github.com/mediajunkie/piper-morgan-product/issues/926

---

## What This Is

I've drafted a sprint completion gate for M1 (MVP Foundation), following the pattern established by the M0 gate (#779). The gate has four verification areas:

1. **Conversation Quality** — Does the floor-first architecture actually make Piper feel like a colleague?
2. **Task Lifecycle Completeness** — Can users finish what they start (todos, GitHub issues, reminders)?
3. **Architectural Integrity** — Are the structural changes (lazy workflows, capability awareness, action gate) sound?
4. **Bug Debt and Test Health** — Is the test suite green and are known bugs resolved?

Each gate has specific criteria, evidence requirements, and a sign-off line.

## What I Need From You

### CXO

Gates 1 and 2 are where the user experience bar lives. I've proposed smoke test queries and expected behaviors, but **you defined the experience standard** through the canonical retest (#884) and failure gap analysis. Please:

- **Add or modify smoke test queries** that capture what "good enough for alpha" means
- **Challenge the "Colleague Test" criteria** in Gate 1 — are those 5 queries the right ones? Would you add harder ones?
- **Verify Gate 2's lifecycle tests** — the todo and GitHub flows are tested, but are there interaction patterns I'm missing? (e.g., multi-step conversations, error recovery)
- **Flag any experience issues** from your March testing sessions that aren't captured in the gate criteria

The risk I'm worried about: I built the system and wrote the gate. It's easy to unconsciously write criteria that my own work passes. Your outside perspective corrects for that.

### PPM

Gate 3 (Architectural Integrity) is where structural shortcuts would hide. Please:

- **Verify the capability awareness check** (#923) — I reconciled three sources of truth into a registry-driven system, but the fix may have addressed the symptom without fully resolving the architectural tension. Does the structural solution satisfy you?
- **Check for Assembly Assumption pattern** (Pattern-062) — Are there integration points where we've extended at one layer without verifying downstream layers complete the contract?
- **Review the offer system consolidation** (#922/ADR-059) — We removed onboarding and consolidated to a dispatcher, but three offer mechanisms still exist (soft offer, contextual offer, workflow dispatcher). Is the ownership clear enough?

### Both

- **Are four gates the right number?** The M0 gate had three. I dropped the original "Intent Classification Accuracy" gate because floor inversion made most classifier issues moot. Should it come back?
- **Is anything missing entirely?** The gate doesn't test: documentation quality, onboarding experience (removed per ADR-059), or integration reliability (calendar/GitHub when configured). Should any of these be gated?

## Timeline

PM plans to run user acceptance testing after #706 and #375 are addressed. The gate should be finalized before that testing begins so we know what "passing" looks like.

---

*Please comment directly on #926 with your additions/changes, or send a return memo if the feedback is more structural.*
