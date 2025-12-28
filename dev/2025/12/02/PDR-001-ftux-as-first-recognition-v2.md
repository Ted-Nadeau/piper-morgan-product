# PDR-001: First Contact is First Recognition

**Status**: Draft v2
**Date**: December 2, 2025
**Author**: Principal Product Manager
**Reviewers**: CXO, Chief Architect
**Stakeholders**: PM (xian)

---

## Decision

Piper Morgan's first-time user experience is the initial expression of the recognition interface pattern—not a separate "onboarding wizard" that precedes the "real" experience.

From moment zero, users encounter the same Piper they will always encounter: oriented, contextual, colleague-like. Configuration and setup happen *within* this experience, not as a gate before it.

**In short**: First contact with Piper *is* first recognition. You're meeting a colleague, not configuring software.

---

## Context

The UX Strategy Synthesis (Nov 26, 2025) established the recognition interface as a strategic priority: Piper articulates the situation first, then offers relevant actions. This inverts the "blank prompt" pattern common to AI interfaces.

The question arose: does FTUX follow this pattern, or is it a special case where traditional wizard-style onboarding is acceptable?

This PDR resolves that question: **FTUX is not a special case.** It is the pattern's first expression.

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

### Piper Speaks First

The first screen is not a form or blank prompt. Piper orients:

> "Hi, I'm Piper. I'm going to be your PM partner—think of me as a colleague who's learning how you work. Let me help you get set up so we can start collaborating."

This immediately establishes the colleague metaphor and demonstrates recognition behavior.

### Configuration is Conversationally Framed

Rather than presenting a multi-step form, Piper guides the user through what's needed:

> "To connect to GitHub, I'll need you to authorize access. This lets me see your issues and PRs so I can help you stay on top of your work."

The *actual capture* happens in secure UI elements (OAuth redirect, masked input field). Piper then acknowledges completion:

> "Great, GitHub is connected. I can see you have 12 open issues across 3 repos. Want me to summarize the landscape, or shall we finish setting up first?"

This hybrid approach preserves conversational *experience* while respecting security constraints. Users perceive Piper guiding them, even when discrete form elements handle sensitive capture.

### Tiered Configuration (Minimum Viable Path)

Rather than requiring all integrations upfront (risk: users bail) or deferring everything (risk: empty first experience), configuration follows tiers:

| Tier | Timing | What Happens | Outcome |
|------|--------|--------------|---------|
| **Tier 0** | Immediate | Piper introduces itself, explains what it needs | User meets Piper |
| **Tier 1** | Required | LLM API key entered | Piper becomes conversational |
| **Tier 2** | First value | Connect ONE integration (user's choice) | Real value with real data |
| **Tier 3** | Deferred | Additional integrations added over time | Configuration spreads naturally |

This reaches "first recognition pattern" quickly while allowing setup to continue organically. Users experience value at Tier 2, not after completing all possible configuration.

### Empty States are Recognition Moments

When a user reaches a view with no data, Piper doesn't show "Nothing here yet." Every empty state follows the recognition pattern:

> "This is where your project insights will appear. Once we connect your tools, I'll be watching for patterns worth surfacing. Shall we connect Notion now, or would you rather explore what's here first?"

The pattern:
- Explains what *will* happen (sets expectation)
- Offers a clear next action
- Gives user agency ("or would you rather...")

Every empty state is a micro-FTUX moment. They follow the same recognition interface.

---

## Trust Gradient Initialization

FTUX establishes the user at Trust Stage 1 (New). Per the UX Strategy:

> Stage 1 (New) = Operator autonomy: User directs every action; Piper executes

Piper's FTUX behavior reflects this:
- Explicit permission-seeking: "Would you like me to...?"
- No assumptions about preferences
- High explanation, low autonomy
- Foundation for trust to build through interaction

This aligns with guidance from our Anthropic advisor emphasizing relationship-based ethics: trust is earned through demonstrated reliability, not granted by default.

---

## Architectural Integration

### Moment Generation

FTUX naturally generates typed Moments (per ADR-046) that feed our learning system:
- `Moment.type: ONBOARDING_INTRO` — First contact
- `Moment.type: INTEGRATION_CONNECTED` — Each successful connection
- `Moment.type: FIRST_VALUE_DELIVERED` — User experiences real data

These become trackable data for relationship building—FTUX isn't just user experience, it's system learning from interaction one.

### Trust State Persistence

**Dependency**: Requires `UserTrustProfile` model that persists trust level across sessions. Implementation should track:
- Current trust stage (1-4)
- Stage progression history
- Trust-affecting events (successes, corrections, failures)

---

## Alternatives Rejected

**Traditional wizard → main app handoff**
Rejected because: Creates discontinuous experience. Users learn "setup mode" patterns that don't apply to actual use. Delays value delivery.

**Blank slate with "What can I help you with?"**
Rejected because: Places articulation burden on user who doesn't yet know what Piper can do. Violates recognition interface principle.

**Progressive feature unlock (gamification)**
Rejected because: Foreign to colleague metaphor. Piper isn't a game to be leveled up; Piper is a colleague learning to work with you.

**Require all integrations before proceeding**
Rejected because: Creates abandonment risk. Tier 2 (one integration) is sufficient for first value.

**Defer all configuration until needed**
Rejected because: LLM API key is required for Piper to be conversational. Can't demonstrate recognition without it. Tier 1 is true minimum.

---

## Success Criteria

| Metric | Target | Measurement |
|--------|--------|-------------|
| Time to first recognition | < 30 seconds | User experiences Piper articulating situation and offering options |
| Time to Tier 2 (first value) | < 5 minutes | User has one integration connected and sees real data |
| Mental model formation | Qualitative | If asked "What is Piper?", user answers in one sentence capturing colleague/assistant nature (not "a chatbot" or "an AI tool") |
| Configuration completion | > 80% reach Tier 2 | Users complete minimum viable setup |
| Zero "now what?" moments | Qualitative | No point where user is stranded without guidance |
| Trust progression rate | Track over time | How quickly users advance from Stage 1 to Stage 2 |
| Return user recognition | > 90% accuracy | Piper correctly recognizes returning users and their context |

---

## Technical Notes

### Secure Credential Wrapper Pattern
- Piper articulates the need conversationally (logged, safe)
- Secure form element captures the credential (not logged, masked)
- Piper confirms success without revealing sensitive data
- Failed attempts handled gracefully with guidance

### Loading State Recognition
When Piper is processing (connecting integration, validating key), maintain recognition pattern:
> "Connecting to GitHub now... I'll let you know what I find."

Not a spinner with no context. Piper narrates what's happening.

### Current State Audit
[PLACEHOLDER: Architect to document existing onboarding flow before implementation begins]

---

## Implementation Implications

**For CXO**: Design interaction patterns for each tier, empty state templates, conversational framing for all credential types.

**For Chief Architect**: Implement secure credential wrapper, `UserTrustProfile` persistence, Moment.type generation for FTUX events.

**For Principal PM**: Define integration priority for Tier 2 options, coordinate user research on mental model formation, track success metrics.

**For Implementation**: PM-122 (FTUX Wizard) should be reframed as "First Contact Implementation" with tiered approach. May warrant scope revision or new epic structure.

---

## Open Questions

1. **Integration priority**: Which integrations should be offered at Tier 2? Recommend user's choice from available options, but may want to guide toward highest-value first experience.

2. **Michelle's feedback**: What did our alpha tester experience in her first contact? Any insights to incorporate? [Pending: interview/synthesis when more data available]

3. **Tier 1 alternatives**: If user doesn't have an LLM API key, what's the fallback? Trial key? Degraded experience? This affects accessibility.

---

## References

- UX Strategy Synthesis (Nov 26, 2025) — Recognition interface priority
- Roadmap v12 — VISION-CONSCIOUSNESS, Sprint V1 scope
- ADR-046 — Moment.type definitions
- Ethics-First Architecture — Trust gradient definition
- CXO Memo (Dec 2, 2025) — UX refinements
- Chief Architect Memo (Dec 2, 2025) — Architectural assessment

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| Draft v1 | Dec 2, 2025 | Initial draft |
| Draft v2 | Dec 2, 2025 | Incorporated CXO and Architect feedback: title change, tiered FTUX, hybrid credentials, enhanced empty states, sharpened success criteria, technical notes, Moment.type integration |

---

*PDR-001 | Draft v2 | December 2, 2025*
