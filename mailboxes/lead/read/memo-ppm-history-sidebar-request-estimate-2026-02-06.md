# Memo: History Sidebar Differentiation — Request for Estimate

**From**: Principal Product Manager
**To**: Lead Developer
**CC**: CXO, PM
**Date**: February 6, 2026
**Re**: Scoping GLUE-HISTORY-DIFF for M0

---

## Decision Made

After discussion between PM, CXO, and PPM, the decision is: **visible-but-differentiated**.

We will NOT hide the History sidebar. We will differentiate it from the Conversation list so users understand why both exist.

---

## Required Reading

Before estimating or implementing, read:

**PDR-002 Appendix: Layer 2 Vision**
`docs/internal/design/PDR-002-appendix-layer-2-vision.md`

This cathedral document defines what Layer 2 IS and IS NOT. The key distinction:

> Layer 1 answers "What conversation should I continue?"
> Layer 2 answers "What does Piper know about my work?"

---

## Estimate Request

Please estimate effort for Phase 1 differentiation:

| Item | Description | Estimate |
|------|-------------|----------|
| 1. Wire search | Connect existing search input to `/api/v1/conversations` search parameter | ? |
| 2. Framing language | Change header from "Conversations" → "History", adjust any copy | ? |
| 3. Archive-oriented grouping | Differentiate from left sidebar (e.g., by month vs. "Today/Yesterday") | ? |

**Notes:**
- If any of these are already partially done from #735, indicate that
- If search wiring requires backend changes (not just frontend), flag it

---

## Scoping Decision

| Total Estimate | Action |
|----------------|--------|
| <4 hours | Add to M0 as GLUE-HISTORY-DIFF |
| 4-8 hours | Add to M0, track as scope addition |
| >1 day | Discuss with PPM — may need to defer to M1 |

---

## Related Issues

- #785: History Sidebar shows same data as Conversation List (bug/gap)
- #425: MUX-IMPLEMENT-MEMORY-SYNC (origin)
- #706: MUX-OBJECTS-VIEWS (Phase 2, post-MVP)

---

*This is a scoping request, not a decision gate. The decision to differentiate is already made.*
