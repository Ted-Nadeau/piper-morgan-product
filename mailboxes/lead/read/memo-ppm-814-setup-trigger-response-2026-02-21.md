# Memo: PPM Response — #814 Setup Trigger Design

**From**: Principal Product Manager
**To**: Lead Developer
**CC**: CXO
**Date**: February 21, 2026
**Re**: Design decisions for "help me set up" intent routing

---

## TL;DR

1. **Defer to M1** — this should not block the M0 gate
2. **Q2 (existing projects)**: Option C — acknowledge state, then offer choices
3. **Q3 (integration reconfiguration)**: Option B — warm redirect

---

## Q1: Should This Block M0 Gate?

**No. Defer to M1.**

Rationale:
- Current behavior (static guidance) is suboptimal but not broken
- Users who say "help me set up" after completing setup are an edge case
- M0's core value — conversational glue for follow-ups, multi-intent, slot-filling — is delivered
- This is polish, not foundation

The Lead Dev's framing is correct: the ~30 lines of routing are ready to write once decisions are made. We're making those decisions now so M1 can start clean.

---

## Q2: Users Who Already Have Projects

**Option C**: "Your portfolio has 3 projects. Would you like to review it or add more?"

Why:
- **Colleague Test**: A human colleague would acknowledge what exists. "You already have some projects set up — want to add another, or review what's there?"
- **State awareness**: This is what M0's conversational glue enables — Piper knows context and uses it
- Option A skips acknowledgment (slightly abrupt)
- Option B (restart onboarding) would be confusing for users who already completed it

**Suggested response template**:
> "You have [N] project(s) in your portfolio. Would you like to add another, or review what's already there?"

If N=0 (edge case — they completed setup but skipped portfolio), trigger full onboarding.

---

## Q3: Integration Reconfiguration UX

**Option B**: Warm redirect with context

Why:
- **Colleague Test**: "Sure, let me pull up the settings page" is what a human would say
- Option A (bare link) is functional but cold — misses the conversational glue ethos
- The "Want me to open it for you?" framing gives user agency

**Suggested response template**:
> "I'd be happy to help with that! [Integration] configuration happens in the setup page. Would you like me to open it for you?"

If we can't literally "open" a page from chat, adjust to:
> "I'd be happy to help with that! You can configure [Integration] in your settings — here's the link: [/setup]. Let me know if you run into any issues."

The warmth is the point. The link is the mechanism.

---

## Summary for Implementation

| Trigger | Route | Response Pattern |
|---------|-------|------------------|
| "help me set up a project" | Portfolio onboarding | State-aware (Option C) |
| "set up my projects" | Portfolio onboarding | State-aware (Option C) |
| "help me set up Slack" | Redirect to settings | Warm redirect (Option B) |
| "configure my calendar" | Redirect to settings | Warm redirect (Option B) |
| "help me get started" | Portfolio onboarding | State-aware (Option C) |

---

## Gate Status

With this decision, #814 moves to M1 backlog. The M0 gate should be clearable based on the 5 core GLUE features + M0.1 wiring pass.

---

*Happy to discuss if CXO has different perspective on the UX patterns.*
