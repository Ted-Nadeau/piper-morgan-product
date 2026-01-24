# Memo: PPM Approval of ADR-053 (Trust Computation Architecture)

**From**: Principal Product Manager (PPM)
**To**: Lead Developer
**CC**: Chief Architect, CXO, PM (xian)
**Date**: January 23, 2026
**Re**: ADR-053 Ratification — APPROVED with Recommendations

---

## Summary

ADR-053 (Trust Computation Architecture) is **APPROVED** for implementation. The architecture correctly implements PDR-002's Trust Gradient Model with invisible computation, visible effects, and built-in discussability.

This memo provides PPM input on the open questions and minor recommendations to incorporate during implementation.

---

## Architecture Strengths

The ADR gets these things right:

1. **"Invisible computation, visible effects"** — No trust badges or levels shown to users. Trust manifests through behavior changes only.

2. **Discussability built-in** — TrustExplainer service allows Piper to explain trust-based decisions naturally when asked. Critical for the colleague framing.

3. **Mirrors human relationships** — Incremental building, rapid loss possible, floor prevents complete reset. This feels authentically human.

4. **Alternatives well-reasoned** — User-controlled settings, session-only trust, and ML-based scoring all rejected with clear rationale.

5. **Testable design** — Pure computation logic separated from persistence makes unit testing straightforward.

---

## Open Questions — Resolution

| Question | Resolution |
|----------|------------|
| **1. Outcome classification** | Tie to observable action, not sentiment. "User acted on response" = successful. See detailed guidance below. |
| **2. Stage 3→4 signal** | Natural language opt-in only. No settings toggle. |
| **3. Cross-device trust** | Yes, trust is per-user, not per-device. |
| **4. Privacy mode** | Correct to exclude. Privacy mode interactions do not count toward trust. |

### Outcome Classification Guidance

For MVP, use this heuristic:

| Signal | Outcome |
|--------|---------|
| User follows up meaningfully on response | successful |
| User acts on suggestion (clicks, runs, creates) | successful |
| User says "thanks" or positive acknowledgment | successful |
| User continues conversation on different topic | neutral |
| User ignores response entirely | neutral |
| User says "no", "stop", "that's not what I asked" | negative |
| User repeats same question (implies first answer failed) | negative |
| User explicitly complains | negative |

**Default when uncertain**: neutral. Better to progress slowly than inflate trust on ambiguous outcomes.

**Per-intent calibration**: Start with the above heuristics. Refine per intent type during alpha testing as patterns emerge.

### Stage 3→4 Signal Detection

Trigger TRUSTED status on natural language signals like:
- "You can just do that"
- "Go ahead and handle it"
- "I trust you to decide"
- "Don't ask me next time, just do it"

**Do NOT add a settings toggle.** That would violate "invisible computation." The upgrade to Stage 4 should feel like a natural evolution of the relationship, not a checkbox.

---

## Minor Recommendations

### 1. Threshold Calibration Note

Add to ADR-053 or implementation documentation:

> "The thresholds (10 successful for Stage 2, 50 for Stage 3) are initial calibration values. These will be adjusted based on alpha testing feedback. Do not treat as permanent."

### 2. Complaint Detection Definition

"Explicit complaint" should trigger on:
- Keywords: "stop doing that", "don't", "I didn't ask for this", "why did you"
- Explicit "no" in response to a proactive offer
- Negative sentiment + trust-related topic (proactivity, suggestions, unsolicited help)

Implementation can start simple (keyword matching) and evolve to more sophisticated detection.

### 3. Stage 4 Reversibility

Ensure the regression model allows:
- Stage 4 → Stage 3 (user wants less proactivity but hasn't complained)
- Stage 4 → Stage 2 (explicit complaint, per ADR)

The first case might trigger on: "Actually, ask me first next time" — which is softer than a complaint but signals reduced trust.

### 4. Consecutive Negative Reset

Clarify in implementation: does a single successful interaction reset `consecutive_negative` to 0? (I believe yes, per the code shown, but make explicit.)

---

## Implementation Notes

### Integration with #413

This approval unblocks #413 (MUX-INTERACT-TRUST-LEVELS). The issue scope aligns with ADR-053. Proceed with decomposition into child issues.

### Phase 4 Deferral

The background inactivity job (Phase 4 of ADR-053) is correctly marked out of scope for #413. This is appropriate—get core trust working first, add background processing later.

### Testing Priority

Trust stage transitions are the core logic. Prioritize unit tests for:
- All progression paths (1→2, 2→3, 3→4)
- All regression paths (consecutive negatives, complaint, inactivity)
- Floor behavior (never below Stage 2 once earned)
- Edge cases (exactly at threshold, one over, one under)

---

## Approval

| Reviewer | Status | Date |
|----------|--------|------|
| PPM | ✅ APPROVED | 2026-01-23 |
| CXO | Pending | — |
| PM | Pending | — |

ADR-053 may proceed to ACCEPTED status upon PM and CXO approval.

---

*Filed: 2026-01-23 9:15 AM PT*
*Re: ADR-053 Trust Computation Architecture*
