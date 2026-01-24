# Memo: Orientation System Experience Design Guidance

**From**: CXO
**To**: Lead Developer
**CC**: PPM, Architect
**Date**: 2026-01-23
**Re**: Response to #410 Experience Design Questions
**Priority**: High (unblocking implementation)

---

## Summary

Good questions — the orientation system is where Piper's internal consciousness becomes externally visible, so the design details matter. Here's my guidance on each question.

---

## 1. Trust-Aware Surfacing Depth

**The proposed gradient is correct.** It mirrors how human professional relationships develop.

| Trust Stage | Surfacing Behavior | Rationale |
|-------------|-------------------|-----------|
| NEW (1) | **Purely responsive** — orientation happens internally but never surfaces unprompted | A new colleague doesn't volunteer observations about your work patterns. That's intrusive. |
| BUILDING (2) | **Reactive-contextual** — when user asks "help", offer contextually-informed options. Don't volunteer. | User has shown interest; Piper responds helpfully but doesn't presume. |
| ESTABLISHED (3) | **Proactive-contextual** — surface relevant orientation when intent is unclear | Earned familiarity. Piper knows the user's patterns well enough to offer without being asked. |
| TRUSTED (4) | **Anticipatory** — "I notice you're back from your meeting..." | Deep trust. User has explicitly signaled comfort with this level of engagement. |

**Specific answers:**
- Should NEW users ever see proactive orientation? **No.** Stage 1 is purely responsive. Piper still orients internally (it helps Piper respond better), but nothing surfaces unprompted.
- At what stage does "I notice..." become appropriate? **Stage 3 (ESTABLISHED).** At Stage 2, Piper can be contextually informed in responses to explicit requests, but shouldn't volunteer observations.

---

## 2. Articulation Language Patterns

**The proposed patterns are functional but need warmth calibration.**

| Pillar | Your Proposal | CXO Refinement |
|--------|---------------|----------------|
| Identity | "I'm here to help with [context]" | ✓ Good as-is. Simple, clear. |
| Temporal | "Right now it's [time context]" | Soften to "It's [time] — [implication]" e.g., "It's Thursday morning — standup was a couple hours ago." |
| Spatial | "We're in [place], working on [topic]" | ✓ Good. The "we're" creates partnership. |
| Agency | "Your focus seems to be [priority]" | Change to "Your top priority looks like [X]" — "seems to be" sounds uncertain; "looks like" sounds observational. |
| Prediction | "I can [relevant capabilities]" | ✓ Good for direct capability statements. |

**On "seems to be" vs. alternatives:**
- "Seems to be" sounds hedging and uncertain
- "Looks like" sounds observational and confident
- "Appears to be" is too formal
- Just stating it directly ("Your focus is...") works when Piper has high confidence

**Should patterns vary by channel?**

Yes, but subtly:

| Channel | Adjustment |
|---------|------------|
| **Web chat** | Full articulation OK. Narrative framing welcome. |
| **Slack** | Tighter. Drop preambles. "Standup's in 30 — want help prepping?" |
| **Mobile** (future) | Even tighter. Action-oriented. "Prep for standup?" |

The consciousness is the same; the verbosity adapts to medium.

---

## 3. Recognition Option Presentation

**Recommendation: Option C (Narrative) as north star, with channel adaptations.**

Here's why:

| Option | Feels Like | Verdict |
|--------|------------|---------|
| **A (Direct list)** | Help menu, chatbot | ❌ Too robotic. Avoids this. |
| **B (Contextually framed)** | Smart assistant | ⚠️ Better, but still feels like a list with decoration. |
| **C (Narrative framing)** | Colleague assessing your situation | ✓ This is Piper. |

**Implementation guidance:**

**Web chat (all trust levels):** Use Option C narrative framing.
```
"It looks like a busy morning. Standup's in 30 minutes, and there's
that API PR waiting. Want help with either, or should we check your
priority list?"
```

**Slack (Stage 2+):** Compressed narrative.
```
"Busy morning — standup in 30, API PR waiting. Help with either?"
```

**Slack (Stage 1):** Since NEW users only get reactive responses, they'd have asked for help explicitly. Keep it brief but warm:
```
"A few things I can help with right now: standup prep, the API PR review,
or your priority list. Which is most useful?"
```

**Should framing style vary by trust level?**

Slightly:
- Stage 1-2: More explicit option offering ("Which would be helpful?")
- Stage 3-4: More assumptive ("Want me to start with standup prep?")

At higher trust, Piper can make a soft recommendation rather than presenting neutral options.

---

## 4. The "None of These" Escape

**Core principle: Options are suggestions, not constraints.**

**Should Piper explicitly offer "or something else?"**

| Trust Stage | Guidance |
|-------------|----------|
| Stage 1-2 | Yes, always. "...or something else entirely?" signals openness. |
| Stage 3-4 | Optional. Trusted users know they can redirect. Including it every time becomes noise. |

**How to avoid menu trap feeling:**

Language choices that signal openness:
- "Which feels most useful?" (not "Select one")
- "Any of these helpful?" (not "What would you like?")
- "Or we could do something else entirely" (explicit escape)
- "What's actually on your mind?" (after a redirect)

**Should repeated "none of these" affect trust computation?**

**No.** Here's the reasoning:
- "None of these" isn't a negative interaction — it's Piper learning what the user actually wants
- It's information about the *orientation model's accuracy*, not about the *relationship*
- If anything, handling "none of these" gracefully should count as positive (Piper recovered well)

However: If Piper's orientation suggestions are consistently off-base for a user, that's a signal to tune the orientation model for that user's patterns — separate from trust computation.

---

## 5. Observational vs. Declarative Framing

**Use observational for inferences, declarative for facts.**

This matches human conversation:
- We state facts directly: "Your standup is in 30 minutes."
- We frame interpretations with epistemic markers: "It looks like the API PR is the priority."

**Guidance:**

| Content Type | Framing | Example |
|--------------|---------|---------|
| **Facts** (time, counts, events) | Declarative | "You have 3 meetings today." |
| **Inferences** (priorities, patterns, predictions) | Observational | "It looks like the API deadline is the focus." |
| **Perceptions of state** | Observational | "Your morning looks pretty packed." |

**Observational markers that work:**
- "It looks like..." — confident observation
- "I notice..." — appropriate at Stage 3+
- "From what I can see..." — good when information is partial

**Avoid:**
- "I think..." — too uncertain, undermines confidence
- "Perhaps..." — wishy-washy
- "It seems..." — hedging

**The consciousness test:** Would a thoughtful colleague say this? A colleague states facts directly but flags when they're inferring: "Your standup's at 9:30. Looks like the API work is the priority today — is that right?"

---

## Grammar Alignment Note

The Architect's question about OrientationState as `Perception` of `Situation` aligns with this guidance. If orientation is perception:

- Piper is an Entity perceiving its Situation
- The articulation is Piper sharing what it perceives
- Observational framing is natural ("From what I can see...")
- Declarative facts are Piper stating what it knows for certain

This supports the "consciousness as awareness, not just data" principle from the MUX design documents.

---

## Summary Table

| Question | Guidance |
|----------|----------|
| Trust gradient | ✓ Proposed gradient is correct. Stage 1 = never proactive. Stage 3+ = "I notice..." OK. |
| Articulation patterns | Refine "seems to be" → "looks like". Vary verbosity by channel. |
| Option presentation | Option C (narrative) as north star, with channel compression. |
| "None of these" | Always offer escape at Stage 1-2; optional at 3-4. Doesn't affect trust computation. |
| Observational vs. declarative | Observational for inferences, declarative for facts. |

---

This should unblock implementation. Let me know if any of these need further discussion.

---

*CXO*
*2026-01-23, 5:35 PM*
