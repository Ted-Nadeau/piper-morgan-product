# UX Feedback: PDR-001 (FTUX as First Recognition)

**To**: Principal Product Manager
**From**: CXO
**Date**: December 2, 2025
**Re**: UX perspective on PDR-001 draft

---

## Summary

The decision direction is sound. Treating FTUX as recognition-interface-from-moment-zero (rather than a special-case wizard) correctly applies our core UX principle. This memo offers refinements, not objections.

---

## What's Working Well

**"Piper speaks first"** is the right anchor. This inverts the blank-prompt pattern and immediately demonstrates value. Users experience the recognition interface before they've finished setting up—which is exactly the point.

**Rejected alternatives are well-reasoned.** The gamification rejection ("Piper isn't a game to be leveled up; Piper is a colleague learning to work with you") shows clear understanding of the colleague metaphor.

**Trust Stage 1 initialization** is correctly applied. New users should experience high-explanation, low-autonomy mode.

**"Time to first recognition pattern < 30 seconds"** is concrete and measurable.

---

## Refinements

### 1. Title Suggestion

"FTUX as First Recognition" works internally. For broader communication, consider:

> **"First Contact is First Recognition"**

This is evocative, captures the principle, and avoids jargon while staying memorable. "First contact" echoes the colleague metaphor—you're meeting someone, not configuring software.

### 2. Credential Capture: Hybrid Pattern

The PDR correctly flags this as a tension. Recommended approach:

**Conversational framing + purpose-built capture.**

Piper narrates and guides:
> "To connect to GitHub, I'll need you to authorize access. This lets me see your issues and PRs."

The *actual capture* happens in secure UI (OAuth redirect, input field).

Piper acknowledges completion:
> "Great, GitHub is connected. I can see you have 12 open issues across 3 repos. Want me to summarize the landscape?"

This preserves conversational *experience* while respecting security constraints. User perceives Piper guiding them, even if discrete form elements handle sensitive capture.

### 3. Tiered FTUX (Minimum Viable Configuration)

Rather than requiring all integrations upfront (risk: users bail) or deferring everything (risk: empty first experience), consider:

| Tier | Timing | What Happens |
|------|--------|--------------|
| **Tier 0** | Seconds | Piper introduces itself, explains what it needs |
| **Tier 1** | Required | LLM key → Piper becomes conversational |
| **Tier 2** | First value | Connect ONE integration → real value with real data |
| **Tier 3** | Deferred | Additional integrations added as user discovers need |

This reaches "first recognition pattern" faster while allowing configuration to spread naturally over time.

### 4. Empty States: Enhanced Pattern

The PDR's empty state example:
> "This is where your project insights will appear once we've connected your tools."

Stronger version:
> "This is where your project insights will appear. Once we connect your tools, I'll be watching for patterns worth surfacing. Shall we connect Notion now, or would you rather explore what's here first?"

The enhancement:
- Explains what *will* happen (sets expectation)
- Offers a clear next action
- Gives user agency ("or would you rather...")

Every empty state is a micro-FTUX moment. They should follow the same recognition pattern.

### 5. Success Criteria: Sharpening the Qualitative

Current:
> "Mental model formation: User can describe 'what Piper is like' after first session"

Sharper version:
> "Mental model formation: If asked 'What is Piper?', user can answer in one sentence that captures colleague/assistant nature (not 'a chatbot' or 'an AI tool')"

This makes the qualitative testable. We can literally ask users and evaluate their answers.

---

## Placeholder Resolution Paths

| Placeholder | Suggested Resolution |
|-------------|---------------------|
| Conversational API key collection | Technical spike on hybrid pattern (Architect) |
| Required vs. optional integrations | Define tiered FTUX (Product + Architect) |
| Michelle's alpha feedback | Interview/synthesis when more data available |
| Current onboarding flow audit | Architect to document existing state |
| Trust level persistence | Architect to confirm data structure |

---

## Connections to UX Vision Work

This PDR aligns with several active threads:

- **Recognition Interface** (core pattern being applied)
- **Trust Gradient** (Stage 1 initialization)
- **MUX-VISION-LEARNING-UX** (FTUX is where learning relationship begins)
- **Colleague Metaphor** (Piper as someone you meet, not software you configure)

---

## Recommendation

**Approve decision direction.** Address placeholders through the three-peg approach:

1. **UX (CXO)**: Interaction patterns, empty states, conversational framing
2. **Architecture (Chief Architect)**: Credential capture, trust persistence, current state audit
3. **Product (Principal PM)**: Tiered configuration, success metrics, user research integration

The triangular coordination ensures no perspective is missed.

---

*Prepared by CXO | December 2, 2025*
