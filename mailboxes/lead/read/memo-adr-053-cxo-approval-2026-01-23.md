# Memo: CXO Review and Approval of ADR-053 (Trust Computation Architecture)

**From**: CXO
**To**: PM (xian), Chief Architect, PPM
**Date**: January 23, 2026
**Re**: ADR-053 Ratification Review

---

## Verdict

**CXO APPROVES ADR-053** for implementation, with three minor suggestions for consideration during implementation.

---

## Assessment Summary

ADR-053 provides a well-designed architecture for the trust gradient system. The core principle — "invisible computation, visible effects" — is correctly implemented throughout. Users will experience trust through Piper's behavior changes, not through exposed metrics or badges.

### What's Working Well

| Element | Assessment |
|---------|------------|
| Four-stage model | Appropriate progression; behaviors per stage are well-defined |
| Stage 2 floor | Humane — users don't drop to "stranger" after earning trust |
| 90-day inactivity threshold | Gentler than aggressive alternatives; respects that life happens |
| Regression on explicit complaint | Immediate but not punitive (Stage 2, not Stage 1) |
| TrustExplainer templates | Natural language that passes the Contractor Test |
| Audit trail (stage_history) | Enables forensics without user exposure |

### ProactivityGate Behaviors (Correctly Calibrated)

| Stage | Behavior | Design Rationale |
|-------|----------|------------------|
| NEW (1) | Respond only | Appropriate for new relationships |
| BUILDING (2) | Offer related capabilities after task completion | Helpful but not presumptuous |
| ESTABLISHED (3) | Proactive suggestions based on context | Earned through demonstrated history |
| TRUSTED (4) | "I'll do X unless you stop me" | Requires explicit trust signal |

This progression mirrors how trust develops in human professional relationships — exactly as PDR-002 intended.

---

## Minor Suggestions

### Suggestion 1: Stage 3→4 Signal Recognition

**Issue**: The ADR mentions users might say "you can just do that" to signal Stage 4 readiness, but doesn't specify how Piper recognizes this intent.

**Risk**: Without explicit handling, Stage 4 may be unreachable in practice.

**Recommendation**: Add to Phase 2 or Phase 3 scope — create an intent pattern for trust-escalation signals. Example phrases to recognize:
- "Just handle it"
- "Do that automatically next time"
- "I trust you to..."
- "You don't need to ask me about that"

Alternatively, consider whether a settings toggle ("Let Piper act on my behalf for [X]") could serve as the explicit signal for certain action categories.

---

### Suggestion 2: Welcome Back Pattern for Inactivity Regression

**Issue**: A user who returns after 90+ days will find Piper less proactive than before. Without context, this could feel like rejection or broken functionality.

**Risk**: User confusion or perception that "Piper forgot me."

**Recommendation**: When serving a user who has regressed due to inactivity, Piper could acknowledge this once:

> "Good to see you again! It's been a while — I'll ease back into helping proactively as we work together."

This explains the behavior change naturally without exposing trust mechanics. Implement as a one-time message per regression event, not on every interaction.

---

### Suggestion 3: Explanation Availability at Stage 4

**Issue**: The ADR specifies `explanation_level: "minimal"` at Stage 4, which makes sense for unsolicited context. However, users should always be able to request fuller explanation.

**Risk**: Stage 4 users who ask "why did you do that?" might get insufficient detail.

**Recommendation**: Clarify in implementation that `explanation_level` affects *unsolicited* explanation depth only. When a user explicitly asks for explanation (via TrustExplainer), Piper should provide full context regardless of trust stage.

The principle: trusted colleagues don't over-explain unprompted, but they answer questions fully when asked.

---

## Open Questions — CXO Input

The ADR flags four open questions. My input on each:

### Q1: Outcome Classification Heuristics

> How do we determine if an interaction was "successful"?

**CXO Input**: Define per intent type, starting with clear signals:
- User clicked a provided link → successful
- User ran a suggested command → successful
- User said "thanks" or expressed satisfaction → successful
- User asked follow-up question on same topic → successful (engagement)
- User changed topic without acknowledgment → neutral
- User said "that's not what I wanted" → negative

When uncertain, default to "neutral." Don't over-engineer; the thresholds (10, 50) provide buffer for noise. Iterate based on real usage patterns.

### Q2: Stage 3→4 Explicit Signal

> What constitutes an "explicit user comfort signal"?

**CXO Input**: See Suggestion 1 above. Two paths:
1. **Conversational**: Recognize intent patterns like "just handle it" or "you don't need to ask"
2. **Settings-based**: Optional toggle for specific action categories

I lean toward conversational as primary (more natural, matches how human trust escalates), with settings as secondary for users who prefer explicit control.

### Q3: Cross-Device Trust

> If user interacts on mobile and desktop, is trust unified?

**CXO Input**: Yes, unified per-user. Trust is about the relationship between Piper and the person, not between Piper and a device. A user who builds trust on desktop shouldn't start over on mobile.

### Q4: Privacy Mode Interaction

> Should "don't remember this session" interactions count toward trust?

**CXO Input**: No, correctly excluded. Privacy mode means "don't remember" — that contract extends to trust computation. Users opting for privacy mode are explicitly declining relationship-building for that session.

---

## Alignment with Design Principles

ADR-053 aligns with established CXO design guidance:

| Principle | How ADR-053 Honors It |
|-----------|----------------------|
| **Piper is a colleague, not a character** | Trust builds through work quality, not personality performance |
| **Contractor Test** | TrustExplainer responses sound like a professional explaining their judgment |
| **Invisible mechanics, visible effects** | No "Trust Level: 3" badges; users experience behavior changes |
| **Discussable on request** | Users can always ask "why did you do that?" and get real answers |
| **Mirrors human relationships** | Incremental building, possible regression, floor once earned |

---

## Conclusion

ADR-053 is ready for implementation. The architecture preserves consciousness, supports the grammar ("Entities experience Moments in Places" — trust is how Piper's experience of the user-Entity evolves over time), and provides clear governance for proactivity.

The three suggestions above are minor refinements that can be addressed during implementation phases, not blockers to approval.

**Status**: APPROVED by CXO

---

*Filed: 2026-01-23 9:15 AM PT*
