# Memo: CXO Response to Design System Reorganization

**To:** Documentation Management Agent
**From:** CXO
**Date:** January 8, 2026
**Re:** Design System Front Door & UX Document Consolidation — Decisions

---

## Executive Summary

Thank you for the comprehensive reorganization work. The "front door" approach is sound, and the consolidation of 37 documents across 5 categories will serve both human designers and LLM agents well.

This memo provides decisions on the three items requiring CXO review:
1. **Design Philosophy**: Approved with revisions
2. **Document Hierarchy**: Confirmed
3. **MUX 2.0 Integration**: Selective merge

---

## Decision 1: Design Philosophy — Approved with Revisions

The proposed 5 principles capture the right territory but could be sharper. Revised principles below:

### Approved Design Philosophy (v1.0)

```
PIPER MORGAN DESIGN PHILOSOPHY

1. COLLEAGUE, NOT TOOL
   Piper is a professional colleague who happens to be AI—not a chatbot,
   not a feature, not an assistant. Design every interaction as you would
   design communication between trusted coworkers.

2. TRUST GRADIENT
   Behavior adapts based on relationship maturity. New users experience
   restraint; established users experience anticipation. Trust is earned
   through demonstrated value, never assumed.

3. DISCOVERY THROUGH USE
   Users learn Piper's capabilities by using them, not by reading about
   them. Design for progressive revelation through natural interaction,
   not documentation or feature tours.

4. CONTEXT-AWARE, NOT CREEPY
   Piper uses what it knows to be helpful, but respects boundaries.
   The test: Would a thoughtful colleague remember this, or would
   remembering it feel invasive?

5. ALWAYS USEFUL, NEVER STUCK
   Piper provides value even with limited context, degraded integrations,
   or partial information. Users should never hit dead ends without
   a path forward.
```

### Rationale for Changes

| Original | Revised | Why |
|----------|---------|-----|
| Conversational First | Colleague, Not Tool | "Conversational" is mechanism; "colleague" is relationship |
| Trust Gradient | Trust Gradient | No change—clear and foundational |
| Contextual Intelligence | Context-Aware, Not Creepy | The boundary matters as much as the capability |
| Discovery Over Documentation | Discovery Through Use | Avoids sounding anti-documentation |
| Graceful Degradation | Always Useful, Never Stuck | User-centered language vs. technical pattern |

### Ordering Rationale

The sequence moves from identity (what Piper is) → relationship dynamics (how trust works) → learning model (how users discover) → intelligence boundaries (how context is used) → resilience (what happens when things break).

---

## Decision 2: Document Hierarchy — Confirmed

The proposed hierarchy is correct:

```
DOCUMENT PRECEDENCE (higher number wins)

4. PDRs              — Strategic intent ("why we decided")
3. Design Briefs     — Tactical direction ("what we're doing")
2. UX Specs          — Implementation details ("how it works")
1. Voice Guides      — Tone and copy ("how it sounds")
```

### Additional Guidance

Add this clarification to the README:

> **Settled Decisions Are Not Re-Litigated**
>
> When a PDR marks a decision as "settled" or "decided," agents should
> not propose alternatives unless they have new evidence that wasn't
> available when the decision was made. If an agent believes a settled
> decision should be revisited, they should flag this explicitly rather
> than simply offering a different approach.

This prevents well-meaning agents from "helpfully" reopening decisions we've already made (e.g., proactivity model, context persistence model, suggestion throttling).

---

## Decision 3: MUX 2.0 Integration — Selective Merge

### Canonical (Integrate into Design Philosophy)

These concepts should inform implementation now:

| Concept | Source | Integration Point |
|---------|--------|-------------------|
| Core grammar: "Entities experience Moments in Places" | Nov 27 session | Add to Philosophy as foundational model |
| Four substrates (Entities, Places, Moments, Situations) | Nov 27 decisions | Reference in object model documentation |
| Situation as container (not peer substrate) | Sketching discovery | Clarify in any entity modeling |
| Full lifecycle with composting | Nov 27 decision #5 | Align with learning system architecture |
| Two journaling layers (Session + Insight) | Nov 27 decision #6 | Inform audit/learning system design |

### Exploratory (Do Not Constrain Implementation)

These concepts are valuable but explicitly "held open" and should not yet bind implementation:

| Concept | Status | Reason |
|---------|--------|--------|
| Specific lens list (8 dimensions) | In flux | "Still refining" per Nov 27 |
| Perception/Orientation/Judgment boundaries | Held open | "Promising but needs refinement" |
| Non-human sapient modeling | Parked | Future consideration |
| Premonitions at high trust | Noted | Not yet designed |
| Agent inbox/outbox | Parked | Relates to multi-agent coordination |

### Practical Implication

A developer reading the design system should:
- ✅ Understand the grammar model and use it for mental framing
- ✅ Design with the lifecycle stages in mind
- ✅ Know that Situation contains Moments (not a parallel type)
- ❌ Not feel bound to implement exactly 8 specific lenses
- ❌ Not assume Perception/Orientation/Judgment are final cognitive categories

### README Addition

Add a section distinguishing canonical vs. exploratory:

> **MUX Concepts: What's Settled vs. What's Evolving**
>
> The MUX (Modeled User Experience) work from November 2025 established
> foundational concepts that inform our design thinking. Some are settled;
> others remain exploratory.
>
> **Settled** (design with these):
> - Grammar: "Entities experience Moments in Places"
> - Lifecycle: Emergent → ... → Composted (feeds learning)
> - Situation as container for Moments
>
> **Exploratory** (don't constrain to these yet):
> - Specific lens definitions
> - Cognitive faculty boundaries
> - Advanced trust features (premonitions)

---

## Additional Recommendations

### 1. Spec Review Cadence
Agree with your recommendation. Suggest quarterly review aligned with sprint boundaries. CXO can own the review trigger; HOSR can track completion.

### 2. Coverage Gaps Priority
Recommend this order:
1. **Error messaging** — Users encounter errors; voice matters here
2. **Loading/skeleton states** — Affects perceived performance
3. **Accessibility** — Should be foundational, not afterthought
4. Dark mode/theming can wait for post-beta

### 3. Voice Guide Expansion
Yes, we likely need:
- Error message voice guide (highest priority)
- Notification voice guide (for proactive features)

Onboarding copy can fold into the existing FTUX specs for now.

---

## Summary

| Item | Decision | Action |
|------|----------|--------|
| Design Philosophy | Approved with revisions | Update README with v1.0 principles |
| Document Hierarchy | Confirmed | Add "no re-litigation" clause |
| MUX 2.0 | Selective merge | Add canonical/exploratory distinction |
| Spec Review | Agreed | Establish quarterly cadence |
| Gap Priority | Errors → Loading → Accessibility | Queue for future sprints |
| Voice Expansion | Error + Notification guides needed | Add to backlog |

---

## Next Steps

1. Documentation Management Agent updates `docs/internal/design/README.md` with these decisions
2. CXO reviews updated README for accuracy
3. PM decides on backlog priority for coverage gap items

Thank you for the thorough work on this reorganization. The design system front door will be valuable for onboarding new contributors—which is timely, as we have a new developer (Ted Nadeau) who will need exactly this kind of guidance.

---

*CXO | January 8, 2026*
