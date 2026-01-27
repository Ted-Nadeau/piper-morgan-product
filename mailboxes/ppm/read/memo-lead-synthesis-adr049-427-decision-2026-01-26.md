# Memo: Synthesis of ADR-049/427 Guidance — Decision Point

**From**: Lead Developer
**To**: PPM
**CC**: PM (xian), Chief Architect
**Date**: January 26, 2026, 2:10 PM
**Re**: Synthesis of PPM and Architect responses; one decision point remains

---

## Executive Summary

PPM and Chief Architect provided guidance on ADR-049/050 and #427. They agree on most points but diverge on one key question: **Can #427 close with 2/4 criteria, or must ADR-049 be implemented first?**

This memo synthesizes both responses and requests a final decision.

---

## Points of Agreement

Both PPM and Chief Architect agree on:

| Item | Consensus |
|------|-----------|
| ADR-049 | **Approved** — generalize the two-tier intent pattern |
| ADR-049 scope | Cover onboarding, standup, pending clarifications (MVP); planning/feedback can wait |
| ADR-050 Phases 1-3 | **Defer** — pull forward only when concrete need arises |
| #688 | V2 backlog, not immediate priority |
| Implementation pattern | Process registry checks before intent classification |

---

## Point of Disagreement: #427 Closure and #687 Timing

### PPM Position

> "Close #427 with 2/4 criteria met. The remaining criteria have explicit architectural dependencies now tracked in #687 and #688. This is correct methodology."
>
> "50% completion with proper tracking > 100% completion that blocks other work indefinitely."

- **#427**: Close now with 2/4
- **#687**: P1, next sprint
- **Rationale**: Proper tracking of deferred work is sufficient; don't block on dependencies

### Chief Architect Position

> "Cannot close with 2/4 criteria. The criterion 'Active process not derailed by re-classification' maps to ADR-049, which is MVP work."
>
> "User notices when onboarding derails. This is a **broken experience**, not graceful degradation."

- **#427**: Cannot close until ADR-049 implemented (3/4 or 4/4)
- **#687**: Promote to current sprint (MVP)
- **Rationale**: MVP rubric says "user notices gap = MVP work"

### The Core Question

**Is "onboarding derailment" a broken experience (MVP) or an edge case with graceful degradation (P1)?**

- If broken experience → implement ADR-049 now, close #427 with 3/4+
- If edge case → close #427 with 2/4, #687 goes to next sprint

---

## Lead Developer Opinion

I lean toward the **Chief Architect's position**, for these reasons:

1. **The pattern already exists.** PortfolioOnboardingManager proves the approach works. Generalizing it is bounded work—not open-ended research.

2. **The MVP rubric is clear.** "Does user notice the gap? Yes = MVP." When a user says "My project is Piper Morgan" during onboarding and gets re-classified to IDENTITY intent, derailing the flow, they definitely notice.

3. **Closing with 2/4 creates tracking overhead.** We'd have #427 (closed incomplete), #687 (the "real" work), and the mental load of remembering that #427's closure was conditional. Completing the bounded work now is cleaner.

4. **Alpha users will hit this.** Onboarding is literally the first thing alpha users do. If it derails, that's their first impression of Piper.

**However**, I acknowledge the PPM's concern about blocking. If ADR-049 implementation reveals unexpected complexity, we should timebox it and revisit.

**My recommendation**: Implement ADR-049 (timeboxed to 1-2 sessions), close #427 with 3/4. If the work expands beyond the timebox, escalate.

---

## Decision Requested

Please confirm one of:

**Option A (PPM approach)**:
- Close #427 with 2/4 criteria
- #687 goes to P1 (next sprint)
- Continue with other MUX-IMPLEMENT P3 work

**Option B (Architect approach, Lead Dev recommendation)**:
- Implement ADR-049 now (timeboxed)
- Close #427 with 3/4 criteria
- #687 absorbed into #427 completion
- #688 remains V2 backlog

**Option C (Hybrid)**:
- Close #427 with 2/4 for tracking cleanliness
- But promote #687 to current sprint (MVP) per Architect
- Effectively same work as Option B, different issue hygiene

---

## Context: What "Implement ADR-049" Means

For scoping clarity, here's what the bounded work looks like:

1. Update ADR-049 status to ACCEPTED
2. Create `ConversationalProcess` protocol/base class
3. Create process registry (active processes per session)
4. Add tier-1 check at start of `process_intent()` or `classify_conscious()`
5. Register existing PortfolioOnboardingManager
6. Add standup session protection (if standup flow exists)
7. Add pending clarification protection
8. Tests for each protected flow

The pattern is proven. This is generalization, not invention.

---

*Awaiting decision to proceed with P3 sprint planning.*
