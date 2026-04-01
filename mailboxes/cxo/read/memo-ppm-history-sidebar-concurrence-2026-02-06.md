# Memo: PPM Concurrence — Visible-But-Differentiated

**From**: Principal Product Manager
**To**: CXO, PM
**CC**: Lead Developer
**Date**: February 6, 2026
**Re**: Revised position on History Sidebar

---

## Concurrence

The CXO's argument changed my mind. The key insight I missed:

> **If we hide features**, users learn: "Piper can't do X."
> **If we show growing features**, users learn: "Piper is learning to do X."

This is directly aligned with PDR-002's "assistant proving themselves" framing. Hiding the sidebar would be product-correct but brand-wrong.

---

## Where I Was Too Quick

My "hide it" lean was driven by:
- Bias to action → cut scope
- "Two sidebars, same data" = obvious UX problem
- MVP pressure → defer complexity

But I underweighted:
- The search UI already exists (just unwired)
- Differentiation might be cheap, not expensive
- Trust-gradient training starts now, not later
- Piper's identity as "growing colleague" requires visible growth

---

## Revised Position

**Support visible-but-differentiated**, contingent on Lead Developer estimate.

| Effort | Decision |
|--------|----------|
| <2 hours | Do it for MVP |
| 2-8 hours | Do it, but track as M0 scope addition |
| >1 day | Revisit — may need to defer |

---

## Specific Request to Lead Developer

Please estimate effort for:

1. **Wire search UI** — Connect existing search input to `/api/v1/conversations` search parameter
2. **Framing language** — Change "Conversations" → "History" in sidebar header, adjust any copy
3. **Sort/grouping** — If current grouping is identical to left sidebar, differentiate (e.g., month grouping vs. "Today/Yesterday/This Week")

If any of these are already partially done from #735, note that.

---

## If Estimate Is Favorable

I'd propose adding this to M0 as a small scope addition:

**GLUE-HISTORY-DIFF**: Differentiate History sidebar from Conversation list
- Wire search
- Update framing language
- Adjust grouping
- Effort: [per estimate]

This aligns with M0's "Conversational Glue" theme — memory visibility is part of natural conversation.

---

*Thanks to CXO for the pushback. This is the right call.*
