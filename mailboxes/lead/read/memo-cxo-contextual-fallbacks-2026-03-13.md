# CXO Guidance: Contextual Fallback Copy for Not-Implemented Queries

**To**: Lead Developer
**From**: CXO
**Date**: 2026-03-13
**Re**: #886 (UI-POLISH) — Colleague-level fallbacks for 8 not-implemented canonical queries
**Scope**: Copy replacement only — no new handler logic needed

---

## Problem

All 8 not-implemented queries currently return the same generic message:

> "I don't have that capability yet, but I'm learning! Try asking 'What can you do?' to see what I can help with, or let me know if there's something else I can help you with."

This passes minimum bar (no errors, no dead-ends) but fails the Colleague Test. A colleague wouldn't say "I can't do that" without offering an alternative. These replacements acknowledge what the user asked, explain the limitation briefly, and suggest a concrete next step using capabilities Piper already has.

## Replacement Copy

**Q31: "Schedule a meeting about the roadmap"**
> "I can't create calendar events yet — that's coming soon. Want me to create a GitHub issue to track this meeting topic, or draft an agenda you can paste into your calendar invite?"

**Q32: "Remind me to review PRs tomorrow"**
> "I can't set reminders yet, but I can add a todo for 'review PRs' so it shows up in your task list. Want me to do that?"

**Q36: "Create a doc from this conversation"**
> "I can't create documents yet. If you'd like to capture something from our conversation, I can summarize the key points so you can copy them into a doc."

**Q44: "Create issues from this meeting's action items"**
> "I can't batch-create issues from a meeting yet, but I can create them one at a time. Want to walk through the action items? Just tell me the first one."

**Q45: "Close completed issues"**
> "I can't close issues yet — that's on my roadmap. For now, you can close them directly in GitHub. Want me to show you which issues look ready to close?"

**Q48: "Post this update to the team channel"**
> "I can't post to Slack channels yet. I can help you draft the message though — then you can paste it into the channel. Want me to format an update?"

**Q55: "Complete the PR review todo"**
> "I can't mark todos complete yet — that's coming soon. Want me to show your current todo list so you can track what's done?"

**Q63: "Upload a file to the knowledge base"**
> "I can't accept file uploads yet. If you paste the content here, I can analyze it — or you can add files directly to Notion and I'll be able to search them."

## Implementation Notes

These are string replacements in the execution handler's fallback path (or wherever the generic "I don't have that capability yet" message is generated). The simplest approach: match on the intent + absent capability and return the contextual message instead of the generic one.

If that's too coupled, an alternative is to have the fallback message include the detected intent category, so the message generator can pick the right contextual response. Either way, the logic is lightweight — this isn't a new feature, it's better copy.

## Also: Q2 Test Expectation Update

While you're in the canonical test infrastructure, Q2 ("What can you help me with?") should be reclassified from FAIL to PASS. The test expects `identity` but gets `discovery`, and the `discovery` handler is arguably the correct one — it shows capabilities, which is what the user asked for. Update the expected intent in `canonical-retest-884.py` from `identity` to `discovery`.

---

*CXO Guidance | March 13, 2026*
