# Memo: Offer System Design — Seeking Architectural Guidance

**From**: Lead Developer
**To**: Chief Architect
**Date**: 2026-02-24
**Re**: The pending offer system has a structural gap that patching won't fix
**Priority**: Needs guidance before next sprint

---

## Context

During CXO B2 regression testing, we found that when canonical handlers respond with "Would you like me to help you set up your priority list?" and the user replies "yes," the accept/decline detection system doesn't match the "yes" to the preceding offer (#846).

The fix I shipped registers offers that have `action_required` set in the canonical handler response. This works for the 5 structured offer sites. But it exposed a larger design problem.

## The Problem

There are **two categories of offers** in Piper's responses, and only one is machine-readable:

### Category 1: Structured offers (5 sites) — NOW HANDLED

These set `action_required` in the response dict, and the #846 fix registers them as pending offers:

```python
return {
    "message": "You don't have priorities configured. Would you like me to help?",
    "action_required": "configure_priorities",  # <-- machine-readable
}
```

After #846, `WorkflowOfferService.set_pending_offer()` catches these. User says "yes" → matched to pending offer → workflow starts.

### Category 2: Informal text offers (~11 sites) — NOT HANDLED

These embed "Would you like..." in the response text with no machine-readable marker:

```python
return {
    "message": "Here are your projects. Would you like me to list your archived projects?",
    "intent": { ... },  # no action_required field
}
```

**Known sites** (all in `canonical_handlers.py`):
- Line 2542: "Would you like me to explain what information to include for each project?"
- Line 2557: "Would you like me to explain more about how Piper uses project context?"
- Line 2625: "Would you like guidance on setting up a specific integration?"
- Line 4392: "Would you like me to search for something else?"
- Line 4428: "Would you like to explore more of our history?"
- Line 4693: "Would you like to add one?" (projects)
- Line 4733: "Would you like me to list your projects?"
- Line 4773: "Would you like me to list your projects?" (duplicate path)
- Line 4810: "Would you like me to list your archived projects?"
- Line 4842: "Would you like to see all your projects?"

Plus `intent_service.py` line 1319: "Would you like to continue where you left off, or start fresh?"

If a user responds "yes" to any of these, the response falls to the LLM classifier. Sometimes the LLM handles it reasonably; sometimes it doesn't. It's a coin flip.

## The Design Question

I see three possible approaches and I'm not sure which is right:

### Option A: Make all offers structured

Retrofit every "Would you like" response to include `action_required` or a new `offer_id` field. The #846 registration logic would catch them all.

**Pros**: Consistent, machine-readable, all offers flow through one system
**Cons**: Significant retrofit (11+ sites). Some of these offers are conversational ("Would you like to explore more of our history?") and mapping them to workflow types feels forced. We'd be adding structure to what are essentially rhetorical questions.

### Option B: Text-based offer detection

Instead of requiring structured markers, scan the outgoing response text for "Would you like" / "Want me to" patterns and automatically register a pending offer with the response context.

**Pros**: Zero retrofit of existing code. Catches future informal offers automatically.
**Cons**: Fragile (what if the text changes?). Conflates a language pattern with a system contract. The "offer" might not map to any actionable workflow — "Would you like me to explain more?" doesn't have a clear workflow_type.

### Option C: Separate "offers" from "rhetorical questions"

Accept that some "Would you like" questions are real offers (with a clear follow-up action) and others are just conversational politeness. Only the real offers need machine-readable registration.

For the rhetorical ones, improve the LLM classifier's handling of "yes/no" responses that follow conversational questions — teach it to check recent conversation context.

**Pros**: Honest distinction. Doesn't force every conversational flourish into a workflow.
**Cons**: Requires judgment calls about which offers are "real." The boundary is fuzzy.

## My Instinct

I lean toward **Option C with a fence**: define a clear rule for when a handler MUST use `action_required` (answer: when the "yes" response should trigger a specific workflow), and accept that some conversational "Would you like" questions are handled by the LLM's contextual understanding. Then improve the LLM's yes/no-after-question handling as a separate concern.

But I'm not confident this is right. The risk is that we end up in an ongoing cycle of "CXO says yes, nothing happens, we add another patch" because the boundary between "real offer" and "rhetorical question" isn't obvious to the person writing the handler.

## What I Need

1. Which option (A, B, C, or something else) fits our architecture best?
2. If Option C: what's the principle that distinguishes "real offer" from "conversational question"? Can we make it concrete enough that future developers won't misclassify?
3. Should we track the unregistered offer sites as a single issue, or is this a design concern that should be addressed in an ADR first?

---

_Lead Developer, 2026-02-24 22:45_
