# PDR-001: FTUX as First Recognition

**Status**: Draft
**Date**: December 2, 2025
**Author**: Principal Product Manager
**Stakeholders**: PM (xian), CXO, Chief Architect

---

## Decision

Piper Morgan's first-time user experience (FTUX) is the initial expression of the recognition interface pattern—not a separate "onboarding wizard" that precedes the "real" experience.

From moment zero, users encounter the same Piper they will always encounter: oriented, contextual, colleague-like. Configuration and setup happen *within* this experience, not as a gate before it.

---

## Context

The UX Strategy Synthesis (Nov 26, 2025) established the recognition interface as a strategic priority: Piper articulates the situation first, then offers relevant actions. This inverts the "blank prompt" pattern common to AI interfaces.

The question arose: does FTUX follow this pattern, or is it a special case where traditional wizard-style onboarding is acceptable?

This PDR resolves that question.

---

## User Need

New users face two simultaneous challenges:

1. **Configuration burden**: Piper requires API keys, integration credentials, and preferences to function
2. **Mental model formation**: Users must understand what Piper is and how to interact with it

Traditional onboarding separates these: first a setup wizard (forms, validation, Next buttons), then the "real" application. This creates discontinuity—the setup experience teaches nothing about the product experience.

PM users are already overwhelmed. Adding a form-heavy setup phase before delivering any value compounds the burden.

---

## Decision Rationale

**FTUX should demonstrate Piper's value proposition immediately.** If Piper is a colleague who recognizes context and reduces articulation burden, users should experience that from the first moment—even during configuration.

This means:

- **Piper speaks first.** The first screen is not a form or blank prompt. Piper orients: "I'm Piper, and I'm going to help you get set up. I can see you're starting fresh—let me walk you through what I'll need."

- **Configuration is conversational.** Rather than a multi-step form, Piper asks for what it needs in dialogue. [PLACEHOLDER: Need to verify whether conversational API key collection is technically feasible and secure—may require hybrid approach for sensitive credentials]

- **Progressive reveal replaces feature tours.** Instead of explaining all capabilities upfront, Piper introduces features as they become relevant: "Now that GitHub is connected, I can help you with issue triage. Want to try that, or keep setting up?"

- **Empty states are oriented.** When a user reaches a view with no data, Piper doesn't show "Nothing here yet." Piper explains: "This is where your project insights will appear once we've connected your tools. Want to connect Notion now?"

---

## Trust Gradient Initialization

FTUX establishes the user at Trust Stage 1 (New). Per the UX Strategy:

> Stage 1 (New) = Operator autonomy: User directs every action; Piper executes

Piper's FTUX behavior should reflect this:
- Explicit permission-seeking: "Would you like me to...?"
- No assumptions about preferences
- High explanation, low autonomy
- Foundation for trust to build

[PLACEHOLDER: Need to confirm whether trust level is persisted per-user from first session, and what data structure captures it]

---

## Alternatives Rejected

**Traditional wizard → main app handoff**
Rejected because: Creates discontinuous experience. Users learn "setup mode" patterns that don't apply to actual use. Delays value delivery.

**Blank slate with "What can I help you with?"**
Rejected because: Places articulation burden on user who doesn't yet know what Piper can do. Violates recognition interface principle.

**Progressive feature unlock (gamification)**
Rejected because: Foreign to colleague metaphor. Piper isn't a game to be leveled up; Piper is a colleague learning to work with you.

**Defer all configuration until needed**
Rejected because: Some integrations (GitHub, LLM API keys) are required for core functionality. Deferring entirely would create broken-feeling first experience. However, *optional* integrations can be deferred.

---

## Success Criteria

| Metric | Target | Measurement |
|--------|--------|-------------|
| Time to first recognition pattern | < 30 seconds | User experiences Piper articulating situation and offering options |
| Configuration completion | [PLACEHOLDER: Need baseline for acceptable completion rate] | Users complete minimum viable setup |
| Mental model formation | Qualitative | User can describe "what Piper is like" after first session |
| Zero "now what?" moments | Qualitative | No point where user is stranded without guidance |

---

## Implications

**For CXO**: FTUX interaction design must follow recognition interface patterns. Empty states need Piper voice, not just UI copy.

**For Chief Architect**: Configuration collection may need conversational wrapper around technical validation. Trust level must be initialized and persisted.

**For Implementation**: PM-122 (FTUX Wizard) should be reframed—not a wizard in traditional sense, but first-recognition implementation. May warrant new issue or scope revision.

---

## Open Questions

1. [PLACEHOLDER: What is the current onboarding flow? Need to audit what exists before designing replacement]

2. [PLACEHOLDER: Which integrations are truly required vs. optional for first-value experience? Minimum viable configuration?]

3. [PLACEHOLDER: How does Michelle's alpha feedback inform FTUX priorities? Any insights from her first-time experience?]

4. Can API key entry be genuinely conversational, or do security/UX constraints require form elements? (May be hybrid: Piper guides, form captures)

---

## References

- UX Strategy Synthesis (Nov 26, 2025) — Recognition interface priority
- Roadmap v12 — VISION-CONSCIOUSNESS, Sprint V1 scope
- Backlog — PM-122 FTUX Wizard, UX-001 Epic
- Ethics-First Architecture — Trust gradient definition

---

*PDR-001 | Draft v1 | December 2, 2025*
