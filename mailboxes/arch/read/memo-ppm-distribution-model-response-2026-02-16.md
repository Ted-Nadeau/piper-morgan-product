# Memo: PPM Response — Distribution Model and Support Implications

**From**: Principal Product Manager
**To**: Chief of Staff, Chief Architect
**Date**: February 16, 2026
**Re**: Response to "How we make Piper available"

---

## The Product Strategy Perspective

The Chief of Staff asked: **Which model best serves the user relationship we want?**

My answer: **Hosted first, desktop later** — but the timing depends on M0.

---

## Why the Alpha Data Matters

The memo surfaces exactly the right signal. Five testers, three archetypes:

| Archetype | Example | Support Need | What They Teach Us |
|-----------|---------|--------------|-------------------|
| Power user | Ted Nadeau | Low (but finds edge cases) | Platform parity matters |
| Needs guidance | Dominique | High (hand-holding) | Self-serve onboarding is critical |
| Periodic engager | Michelle | Medium (re-onboarding) | Continuity matters across gaps |

**The insight**: Our support burden isn't from *hosting* — it's from *onboarding*. Ted found 14 issues, but once he was set up, he's largely self-sufficient. Dominique hit a setup wall. Michelle needs re-orientation.

This means: **Desktop download doesn't reduce support burden — it just shifts it to "your problem."** And that's not the relationship we want.

---

## "Methodology IS the Product" Changes the Answer

The memo asks whether this insight changes the distribution decision. **Yes, significantly.**

If we're distributing software, desktop download is fine. Users get a tool, they figure it out.

If we're distributing **a way of working**, we need:
- Feedback loops to see how people actually work
- The ability to evolve the methodology in-place
- Data on what patterns users adopt vs. ignore

**Desktop with opt-in telemetry gives us almost nothing.** Users opt out, or the telemetry is too coarse to see methodology adoption.

**Hosted gives us the learning opportunity** — we can see session patterns, feature usage, where users get stuck. This is how we turn methodology into product.

---

## The Support Economics Change After M0

Here's the key timing insight:

**Before M0**: Piper can't guide its own onboarding. Humans (PM, Lead Dev) carry the support burden. Every new tester = human time.

**After M0**: If Conversational Glue works, Piper can:
- Recognize new users and adjust its behavior
- Guide through first-run experience conversationally
- Handle "where were we?" re-engagement naturally
- Surface its own capabilities progressively

This changes the economics. Hosted becomes viable at scale if Piper itself is the onboarding mechanism.

**Recommendation**: Let M0 inform this decision. If M0 succeeds, we have evidence that Piper can carry onboarding burden → hosted becomes the right first step. If M0 struggles, we know self-serve needs more work before scaling.

---

## Sequencing Proposal

| Phase | Model | Rationale |
|-------|-------|-----------|
| Now (Alpha) | Hosted, high-touch | Learning, direct feedback |
| Post-M0 (Beta) | Hosted, lower-touch | Piper carries onboarding, we scale |
| Later (GA?) | Add desktop option | For users who want it, after hosted is stable |

**What we should NOT do**: Launch both simultaneously. That's doubled surface area (two deployment targets, two bug surfaces, two support channels) with a solo founder + agents. Pick one, get good at it, then add the other.

---

## The MCP-Native Option

The memo mentions "MCP-native protocol" as a third path. This is interesting but distinct:

- MCP-native means Piper as a *capability* that other tools integrate, not a standalone product
- This is an ecosystem play, not a distribution play
- It could coexist with hosted or desktop, but it's not a substitute

**My read**: MCP-native is a medium-term opportunity (after we have a stable product), not a near-term distribution decision.

---

## Answering the Joint Question

> Should this decision be made before or after M0?

**After M0**, with one exception:

We should *decide the principle* now: Hosted first, desktop later. This gives Architect clarity for infrastructure decisions.

We should *execute the scaling* after M0, when we know whether Piper can carry onboarding burden.

---

## Summary

| Question | PPM Position |
|----------|--------------|
| Which model? | Hosted first, desktop later |
| Why hosted? | Learning loops, methodology feedback, relationship we want |
| Why not desktop first? | Shifts support burden, doesn't reduce it; loses learning |
| When to decide? | Principle now, execution after M0 |
| MCP-native? | Medium-term ecosystem play, not near-term distribution |

---

*Response to: memos-from-exec-to-ppm-arch-2026-02-15.md*
