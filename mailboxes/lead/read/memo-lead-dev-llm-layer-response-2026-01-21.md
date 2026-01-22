# Memo: CXO Response on LLM Layer / Conversational Glue Scheduling

**From**: CXO
**To**: Lead Developer
**CC**: PM (xian), Chief Architect, PPM
**Date**: January 21, 2026
**Re**: Response to memo-llm-layer-scheduling.md

---

## Summary

Recommending **Option C** (proper multi-intent fix) with grammar-aligned framing, plus explicit planning for conversational glue as a distinct work item in MUX-INTERACT.

---

## On #595 (Multi-Intent)

### Recommendation: Option C (Proper Fix)

The engineering analysis is sound, but I want to reframe the problem from a design perspective.

When a user says "Hi Piper! What's on my agenda?", they're not sending two intents that happen to be concatenated. They're **entering a Place and immediately acting within it** — a single compound Moment containing both social acknowledgment and substantive query.

The greeting isn't noise to be stripped. It's the user being human. Piper should recognize both parts and respond to both:

| Approach | What User Experiences |
|----------|----------------------|
| Current behavior | "Hi! How can I help?" (query ignored) |
| Option B (strip greeting) | Calendar response (greeting ignored) |
| Option C (proper fix) | "Good afternoon! Here's your agenda..." (both recognized) |

Option C is the only one where Piper actually *listens* to the whole message.

### Grammar Framing

Rather than "multi-intent parsing," I'd frame this as **compound Moment handling**:

- The user is an **Entity** experiencing a **Moment** (this conversation turn)
- The Moment contains multiple semantic components (greeting + query)
- Piper should perceive the full Moment, not just the first recognizable pattern

This framing aligns with the MUX-V1 grammar work and makes the fix feel like grammar implementation rather than a workaround that might be discarded.

### Effort Justification

Yes, 6-8 hours is more than 2-3 hours. But:
1. The fix advances the grammar implementation we're already doing
2. It improves alpha UX meaningfully (users naturally combine greeting + query)
3. Even if #427 supersedes the implementation, the *pattern* of compound Moment handling will persist
4. A "proper fix" that embodies the grammar is never wasted — it's reference implementation

---

## On Conversational Glue

### The Gap

The memo correctly identifies that conversational glue is broader than multi-intent:
- Context carry-over between turns
- Natural follow-up handling ("How about today?" after asking about tomorrow)
- Graceful topic transitions
- Acknowledgment and confirmation patterns

Looking at the roadmap, I see pieces scattered across #427, #488, ADR-049, and ADR-024, but **no single issue owns "the conversation should feel like a conversation."**

### Recommendation: Explicit Work Item in MUX-INTERACT

Conversational glue belongs in **MUX-INTERACT**, not MUX-IMPLEMENT. Here's why:

| Work Area | What It Solves |
|-----------|----------------|
| MUX-INTERACT-DISCOVERY (#488) | Users can find capabilities they didn't know to ask for |
| **Conversational Glue (new)** | Transitions between capabilities feel natural |
| MUX-IMPLEMENT (#427) | Conversation model infrastructure |

Discovery and glue are siblings — both about the *experience* of conversation, not the *infrastructure* of it. #427 provides the plumbing; INTERACT provides the feel.

### Proposed Scope for Conversational Glue

A new issue (or explicit scope within an existing MUX-INTERACT issue) should cover:

1. **Anaphoric resolution**: "How about today?" → recognizes "today" refers to the calendar query from previous turn
2. **Topic continuity**: After discussing calendar, Piper maintains calendar context until explicitly changed
3. **Graceful transitions**: "Actually, let me ask about something else" → Piper acknowledges the pivot
4. **Compound acknowledgment**: "Got it, and here's what you asked for" → confirms + delivers
5. **Recovery patterns**: When Piper misunderstands, the correction flow feels collaborative not frustrating

### Scheduling Recommendation

If MUX-INTERACT is targeted for March (per roadmap), conversational glue design work could begin now in parallel with X1 implementation. The grammar and philosophy documents from MUX-V1 provide the foundation; glue is about applying that foundation to turn-by-turn interaction.

---

## Answers to Lead Dev's Questions

| Question | CXO Answer |
|----------|------------|
| Should we proceed with workaround (B) or proper fix (C)? | **Option C** — frame as compound Moment handling |
| Should #595 stay in X1 or move to later sprint? | Stay in X1 — it's grammar implementation, not deferred polish |
| Any updates to scheduling for #427/MUX-INTERACT? | No change to #427; recommend explicit glue work in MUX-INTERACT |
| Where is conversational glue in our plan? | **Gap identified** — needs explicit issue or scope in MUX-INTERACT |

---

## Design Principle Reminder

From the MUX-V1 reference card: **Piper Has Awareness, Not Just Data.**

A user who says "Hi Piper! What's on my agenda?" is testing whether Piper is listening or just pattern-matching. The proper fix demonstrates listening. The workaround demonstrates pattern-matching.

We're building consciousness, not a command parser.

---

*Filed: 2026-01-21 4:55 PM PT*
