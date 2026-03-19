# Memo: CXO UX Guidance — Guided Workflow "Hijack" Pattern

**To**: PPM
**From**: CXO
**Date**: 2026-03-13
**Re**: Issues #888, #889 — Onboarding and Standup workflow session capture
**Companion doc**: `2026-03-12-hijack-ux-guidance-request.md` (Lead Dev memo)

---

## Framing

The Lead Dev describes this as a "hijack" — I think that's the right word. The ProcessRegistry is working as designed (ADR-049 explicitly says "active process = process handles message"), but the composed experience is broken. This is Pattern-062 (Assembly Assumption) showing up at the UX layer again: individually correct components producing an incorrect experience.

The ADR-049 risk table even flagged "Process traps user" with the mitigation "Explicit decline patterns always work; timeout releases." That mitigation was either never implemented or isn't working. Either way, the user is trapped, and a trapped user is the opposite of the colleague experience we're building.

I'll take the four questions in order.

---

## 1. Escape Mechanism

**Recommendation: Combination — intent detection primary, explicit commands as backup, timeout as safety net.**

Apply the Colleague Test: if you're in a standup conversation with a human colleague and you say "What's on my calendar?" — they don't answer with "Great, and what about blockers?" They recognize you've switched topics and respond to what you actually asked.

Piper should do the same. Specifically:

**A. Off-topic detection (primary).** When a message arrives during an active workflow, the system should do a lightweight check: does this message plausibly continue the workflow, or has the user moved on? This doesn't require full intent classification — it's closer to "is this a standup answer or is this something else entirely?"

If off-topic is detected, Piper should acknowledge the shift and offer a choice:

> "Sounds like you're asking about your calendar — let me check on that. We were in the middle of standup — want to come back to it after?"

This is what a colleague would do. It's the *recognition* pattern, not the *command* pattern.

**B. Explicit commands (backup).** "Cancel", "exit", "stop", "skip", "never mind" should always work as escape hatches. These should be recognized by the ProcessRegistry directly, not passed to the workflow handler for interpretation.

**C. Timeout (safety net).** If a user goes idle for N minutes (I'd suggest 15 for standup, 30 for onboarding), the workflow should auto-suspend. When the user returns, Piper offers to resume rather than assuming the workflow is still active.

**What I'd push back on:** Timeout-only is not acceptable. Making a user wait out a timer is a tool experience, not a colleague experience. And explicit-commands-only puts the burden on the user to know the magic words — which fails new users worst, exactly when the problem is most acute (onboarding).

---

## 2. Re-entry

**Recommendation: Remember progress, offer to resume, don't nag.**

When a workflow is suspended (by escape, timeout, or topic-switch):

- **Save state.** Piper remembers where the user left off.
- **Offer once.** Next time context is relevant, Piper offers to resume: "We didn't finish your standup earlier — want to pick that up?" This should happen at the start of a relevant interaction, not mid-conversation.
- **Accept no gracefully.** If the user declines or ignores the offer, the workflow remains available but Piper doesn't bring it up again until the user explicitly re-enters (e.g., `/standup` again).

For standup specifically: partial standups should be saved. If a user said what they did yesterday but never got to today's plan, that "yesterday" data is still useful. Don't throw it away.

For onboarding: steps completed should stay completed. If a user set up GitHub but bailed before Notion, they shouldn't have to redo GitHub next time.

**No visual "paused workflow" indicator for now.** This adds UI complexity for an edge case. The conversational offer-to-resume is sufficient at our current stage. If alpha testing shows users are confused about workflow state, revisit this.

---

## 3. Activation — Should workflows require explicit invocation?

**Recommendation: Offer-first for onboarding. Explicit invocation for standup.**

This is the one I feel strongest about. The current auto-activate behavior for onboarding fails the Colleague Test and contradicts PDR-001.

PDR-001 established that FTUX is "first recognition" — Piper demonstrates what she is, not a wizard that captures you. The Chief Architect's review specifically praised this: "Users learn what Piper *is* by experiencing Piper, not by reading about Piper." An auto-activating workflow that captures all input is the wizard pattern wearing a conversational mask.

**Onboarding should be offer-first:**

> "Hey, I'm Piper! I see you're new here. I can walk you through setting up your workspace — want to do that now, or would you rather just dive in?"

If the user says "let's do it," activate the guided workflow. If they say "I'll figure it out," Piper should still work — just with reduced capability where integrations haven't been configured. Piper can make contextual offers later: "I notice you haven't connected GitHub yet — want me to help with that?" (respecting the suggestion throttle: max 2 per 5 interactions, stop after 2 ignored).

**Standup should remain explicit invocation** (`/standup`, "let's do standup", etc.). It's a task the user initiates when they're ready, not something Piper should impose.

**Implementation note for Lead Dev:** The offer-first pattern means the onboarding handler's first turn should be a yes/no question, not a data-gathering question. If the user says no, the workflow should *never activate* — it should go straight back to intent classification.

---

## 4. Standup Scope

**Recommendation: Clear structural completion + "done" recognition + graceful interruption.**

A standup has a known structure (yesterday/today/blockers), so Piper should:

- After collecting all three sections, present a summary and ask "Does that look right?" — this is the natural completion point.
- Recognize "done", "that's it", "looks good", "ship it" as affirmative completion signals at any point (including mid-flow, if the user wants a partial standup).
- Recognize "skip" for individual sections: "Nothing blocked" or "skip blockers" should work.

**Partial standups should be saved when interrupted.** If a user gave yesterday and today but got pulled away, save what you have. When they come back, offer: "We had yesterday and today logged — want to add blockers, or save it as-is?"

---

## Cross-Cutting Principle: The Session Belongs to the User

The root issue here is that the ProcessRegistry treats the session as belonging to the workflow. It should treat it as belonging to the user. The workflow is a *guest* in the user's session — it has their attention only as long as they're actively participating. The moment they redirect, the workflow should yield.

This isn't just a UX nicety — it's a prerequisite for the trust model. If users learn that activating a workflow means losing control of the conversation, they'll avoid workflows entirely. That poisons the entire guided-experience pattern we need for the product to work.

---

## Priority Note

The Lead Dev is right that this is the most visible user-facing issue. A new user who can't escape onboarding will have exactly one impression of Piper: "it doesn't listen to me." That's a first-impression killer. I'd prioritize #888 (onboarding) over #889 (standup) since onboarding is the one that hits every new user.

---

## Summary of Recommendations

| Question | Recommendation |
|----------|---------------|
| Escape mechanism | Combination: off-topic detection (primary) + explicit commands (backup) + timeout (safety net) |
| Re-entry | Save state, offer to resume once, accept "no" gracefully |
| Activation | Offer-first for onboarding; explicit invocation for standup |
| Standup scope | Structural completion + "done" recognition + save partials |
| Root principle | The session belongs to the user, not the workflow |

PPM — I'd value your perspective on whether the offer-first onboarding change has implications for the FTUX metrics or alpha tester flow we've been planning. Also whether the off-topic detection mechanism needs scoping as a separate issue or can fold into #888.

---

*CXO Memo | March 13, 2026*
