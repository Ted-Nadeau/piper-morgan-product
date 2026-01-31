# Memo: PPM Guidance — Insight Lifecycle Decision

**From**: Principal Product Manager (PPM)
**To**: Lead Developer
**CC**: CXO, PM (xian)
**Date**: January 27, 2026
**Re**: Insight Lifecycle — Consensus Decision
**Related Issues**: #703 MUX-LIFECYCLE-UI, #685 MUX-LIFECYCLE-OBJECTS

---

## Executive Summary

**Decision: Option A — Insights are Composted Output. Defer lifecycle.**

PPM and CXO independently reached the same conclusion. The entity lifecycle pattern doesn't fit insights. This is a principled deferral, not avoidance.

---

## The Consensus

| Advisor | Position | Key Reasoning |
|---------|----------|---------------|
| PPM | Option A | Insights aren't Entities in MUX grammar; they're understanding that *emerges* |
| CXO | Option A | Entity lifecycle creates category error; "BLOCKED insight" is meaningless |
| Lead Dev | Option A | Better to defer than encode wrong model |

**Three independent analyses, same answer.** Confidence is high.

---

## Why Not Entity Lifecycle?

### Grammar Check

MUX grammar: "Entities experience Moments in Places."

- **Entities** have identity and agency (WorkItem, Feature)
- **Insights** are understanding that emerges from composting

Insights don't act. They don't progress through work states. They *are* the output of a process, not participants in one.

### The Category Error Test

| State | WorkItem Meaning | Insight Meaning |
|-------|------------------|-----------------|
| NASCENT | Just created, not started | ??? |
| ACTIVE | Being worked on | ??? |
| BLOCKED | Waiting on dependency | ??? |
| RESOLVED | Work complete | ??? |
| COMPOSTED | Learnings extracted | Circular—insights ARE composted |

The entity lifecycle states don't translate. Forcing them creates confusion.

### The UX Test

If we added lifecycle to Insights, what user action would it enable?

**Answer: None that fits the entity pattern.**

What users *might* need:
- "Has Piper mentioned this before?" → surfaced vs. fresh
- "Have I confirmed this?" → validated vs. unreviewed
- "Is this still relevant?" → current vs. stale

These are **relationship metadata** (user ↔ insight), not **lifecycle states** (insight progression). Different pattern entirely.

---

## CXO's Valuable Addition: Lens Artifact Framing

The CXO preserved the "lens artifact" concept as **design direction**:

> "Insights aren't 'objects to manage'—they're 'observations to consider.'"

This shapes UI treatment:

| If Insights Are Objects | If Insights Are Lens Artifacts |
|------------------------|-------------------------------|
| Show lifecycle badges | Don't show lifecycle badges |
| "Manage your insights" | "What Piper notices" |
| Inbox-style listing | Contextual surfacing |
| User creates/deletes | Piper surfaces, user responds |

**Don't implement this now**, but let it guide presentation choices.

---

## Guidance for #703 Completion

### What to Do

| Model | Lifecycle UI? | Action |
|-------|---------------|--------|
| WorkItem | Yes | Show lifecycle indicators |
| Feature | Yes | Show lifecycle indicators |
| Insight | **No** | Don't add lifecycle infrastructure |

### If Insights Appear in Lifecycle UI

Present them differently:
- No lifecycle badges
- Perhaps freshness indicators ("noticed today", "from last week")
- Perhaps confidence language ("I'm fairly confident...", "I'm not sure, but...")

This aligns with Learning System design: confidence through language, not scores or states.

### Tracking the Deferral

Add to #703 or create tracking note:

> **Deferred: Insight Lifecycle States**
>
> Decision (2026-01-27): Insights use "composted output" model, not entity lifecycle. If insight-specific states are needed later, design fresh—don't shoehorn into entity lifecycle.
>
> Preserved design direction: "Lens artifact" framing—insights are observations to consider, not objects to manage.

---

## Summary

| Question | Answer |
|----------|--------|
| Add lifecycle_state to Insight? | **No** |
| Why not? | Category error—entity lifecycle doesn't fit insight semantics |
| What if we need states later? | Design insight-specific states fresh |
| Preserve lens artifact framing? | Yes, as design direction |
| Defer decision? | **Yes**—principled, not avoidant |

---

## Closing Note

This completes the conceptual guidance needed for P3. Once P3 issues close, we hit a milestone: **planned MUX sprints complete**.

Next: v0.8.5 alpha release → end-to-end UX testing.

Good work surfacing this question properly. The multi-perspective check confirmed the right answer quickly.

---

*Filed: 2026-01-27 7:10 AM PT*
*Session: 2026-01-27-0651-ppm-opus-log.md*
