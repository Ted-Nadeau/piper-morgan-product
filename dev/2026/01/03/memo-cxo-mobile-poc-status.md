# Memo: Mobile 2.0 PoC Status

**To**: Chief Experience Officer
**From**: Mobile App Consultant
**Date**: January 3, 2026
**Re**: Gestural Interaction PoC — Progress and Learnings

---

## Executive Summary

The Mobile 2.0 skunkworks project set out to explore whether **entity-based gesture mapping** could create an intuitive mobile interaction model for Piper Morgan. The core code was completed rapidly (12 minutes on Dec 5), but we have not yet validated the concept through tactile testing due to iOS deployment friction. The PoC is currently in a "code complete, testing blocked" state. Simulator testing reveals buggy behavior that needs debugging before meaningful UX validation can occur.

Despite the delays, the project has produced valuable insights for UX strategy.

---

## What We Set Out to Learn

The central hypothesis: **Gestures should be semantic, not positional.**

In most mobile apps, swipe-left means "delete" or "archive" regardless of what you're swiping. We proposed that in a PM assistant, the same gesture should mean different things depending on the entity type:

| Entity | Swipe Right | Swipe Left |
|--------|-------------|------------|
| Task | Complete | Defer |
| Decision | Approve | Decline |
| Person | Message | Snooze |
| Project | Dashboard | Archive |
| Blocker | Resolved | Escalate |

This maps gestures to the **entity model** rather than to arbitrary UI conventions — an approach grounded in your prior CloudOn work on object-based touch interaction.

The key questions we wanted to answer:
1. Does this feel intuitive or confusing?
2. Can users learn the gesture vocabulary quickly?
3. Does haptic feedback create a satisfying sense of "commitment"?

---

## Current State

| Component | Status |
|-----------|--------|
| Conceptual framework | ✓ Complete |
| Code implementation | ✓ Complete |
| Simulator testing | ⚠ Buggy — gestures don't fire intents |
| Device testing | ⏳ Blocked by deployment issues |
| UX validation | ⏳ Not yet possible |

**The honest assessment**: We built the instrument but haven't yet played it. The code compiles and installs, but the gesture-to-intent wiring appears broken. This is typical of rapid "vibe coding" — the broad strokes work, the connections need debugging.

---

## What We've Learned (Even Without Tactile Validation)

### 1. Platform choice matters for gesture work

Expo Go (the fastest prototyping path) had a native module version mismatch that blocked testing for two weeks. Native builds via Xcode work but introduce iOS deployment friction (certificates, USB connectivity, provisioning).

**Implication for UX strategy**: If mobile gestures are strategically important, budget for native development complexity. The web-first progressive enhancement path (ADR-042) may be wise for initial release, with native gesture work reserved for a later phase when the investment is justified by usage patterns.

### 2. "Code complete" ≠ "Validated"

The PoC was declared complete on Dec 5. It's now Jan 3 and we still haven't felt the gestures. For UX exploration, the definition of "done" should be "humans have interacted with it," not "it compiles."

**Implication for UX strategy**: Validation-first thinking applies to UX experiments too. Rapid prototyping is valuable, but the prototype must reach human hands quickly or the learning cycle stalls.

### 3. The conceptual framework holds up

Even without tactile testing, the design exploration produced durable insights:

- **"The user is mobile"** — There is no separate mobile UX, only a holistic UX with mobile touchpoints for specific jobs-to-be-done.

- **Moment-optimized, not feature-portable** — Mobile Piper shouldn't shrink the desktop; it should specialize in bounded-time interactions (pre-meeting briefing, post-meeting capture, triage while waiting).

- **Front-end / back-end split** — Phone for quick decisions and approvals; laptop for context synthesis and complex work. Piper bridges the handoff.

- **Entity-based gestures as embodied grammar** — The "Entities experience Moments in Places" object model has natural gestural expression. Touch an entity, gesture an intent.

These insights remain valuable for UX strategy regardless of whether this particular PoC ever runs on a device.

---

## Recommendations

### For this PoC

1. **Debug the gesture wiring** — The intent callbacks likely aren't connected. A focused debugging session (1-2 hours) should identify the issue.

   *Technical note*: The symptoms (cards animate but intents never fire) point to a specific failure mode. The pan gesture handler moves the card (visual feedback works), but the `onEnd` handler either isn't detecting threshold crossings or isn't calling the intent callback. A code review of `EntityCard.tsx` (gesture handlers) → `GestureLabScreen.tsx` (intent state management) should locate the disconnect. Look for: (a) threshold comparison logic, (b) `runOnJS` calls to escape the worklet, (c) callback prop connection between components.

2. **Lower the bar for validation** — If device deployment remains cursed, Simulator with click-and-drag can at least validate the code logic. Haptics require a real device, but intent firing doesn't.

3. **Let it simmer** — This is a side project. It's OK for it to move slowly. The conceptual work is done; the implementation will catch up when attention is available.

### For UX strategy

1. **Preserve ADR-042's progressive enhancement approach** — The mobile PoC difficulties reinforce that native mobile development has real friction. Web-first, then PWA, then native (if usage justifies) remains sound.

2. **Keep the gestural grammar in the design toolkit** — Even if we don't build it now, the entity-to-gesture mapping is a powerful concept worth preserving for future mobile work.

3. **Track mobile usage patterns** — The triggers in ADR-042 (mobile traffic >20% for PWA, >30% for native) will tell us when to revisit this exploration with full investment.

---

## Summary

The Mobile 2.0 skunkworks has not yet delivered tactile validation of its core hypothesis, but it has:

- Produced a complete (if buggy) implementation
- Generated durable UX insights about mobile interaction patterns
- Stress-tested the "vibe coding" approach (verdict: fast to code, slow to deploy)
- Reinforced the wisdom of the current progressive enhancement strategy

The project is **on hold, not abandoned**. When bandwidth allows, debugging the gesture wiring and getting hands on the prototype remains worthwhile. The questions we wanted to answer — does entity-based gesture mapping feel intuitive? — are still worth answering.

---

*Prepared by: Mobile App Consultant*
*Project: Piper Morgan Mobile 2.0 Skunkworks*
