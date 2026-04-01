# Memo: History Sidebar — The Case for Visible-But-Differentiated

**From**: CXO
**To**: PPM
**CC**: PM
**Date**: February 6, 2026
**Re**: MVP approach to History Sidebar — respectful counterpoint to "hide it"

---

## The PPM Position (As I Understand It)

You're leaning toward hiding the right sidebar during MVP. The logic is sound: if it shows the same data as the left sidebar, it's confusing. Shipping confusion is worse than shipping less. Bias to action means cutting scope, not shipping half-baked features.

I respect this. It's often the right call.

---

## The CXO Counterpoint

I think there's a middle path that serves users better: **visible, differentiated, with honest framing about what's coming**.

### Three Distinctions

| Scenario | Recommendation |
|----------|----------------|
| Feature is broken | Hide it |
| Feature works but is incomplete | Show it with "growing" framing |
| Feature duplicates another | Differentiate or hide |

The History Sidebar is currently in scenario 3 — but it's fixable without major work.

### Minimum Viable Differentiation

To make the right sidebar worth showing, it needs to answer a *different question* than the left:

| Left Sidebar | Right Sidebar (Differentiated) |
|--------------|-------------------------------|
| "Resume a conversation" | "Search your history" |
| Recent-first, quick access | Search-first, archive feel |
| Active context | Accumulated knowledge |

**What this requires:**
- Wire up the search UI that already exists
- Change the framing language ("History" not "Conversations")
- Optionally: different sort order or grouping

This isn't major feature work. It's UX framing that makes the existing functionality feel intentional.

### Why "Visible" Matters for Piper's Identity

PDR-002 established the "assistant proving themselves" framing — Piper is a junior colleague earning trust through demonstrated competence. This has UX implications:

**If we hide features**, users learn: "Piper can't do X."
**If we show growing features**, users learn: "Piper is learning to do X."

The second framing is truer to Piper's identity and creates anticipation rather than limitation.

### The Trust Gradient Argument

We've already committed to trust-gated features. Users will see some features locked until Piper knows them better. If we establish the pattern now — "here's what's possible, here's what's unlocked" — users are trained for the experience.

If we hide things, then suddenly reveal them later, it feels like we were holding out. Worse, users may not discover features that were always there.

---

## Proposed Middle Path

**For MVP:**
1. Keep the right sidebar visible
2. Wire up search (it's already built, just not connected)
3. Frame it as "History" with archive-oriented language
4. Add a subtle "More coming soon" indicator for entity surfacing

**For M1:**
- Begin surfacing WorkItems with lifecycle states
- The "coming soon" becomes "now available"

**If differentiation proves too costly for MVP:**
- Then I'd agree with hiding — confusion is worse than absence
- But let's verify the cost before assuming it

---

## What I'm Not Saying

I'm not saying ship broken things. I'm not saying ignore the bias to action. I'm not saying the PPM's instinct is wrong.

I'm saying: the History Sidebar can be made to feel intentional with modest effort, and that effort buys us UX consistency with our trust-gradient vision.

If investigation reveals the effort isn't modest, I'll defer to your judgment.

---

## Request

Before deciding to hide, can we get a Lead Developer estimate on:
1. Wiring up the existing search UI
2. Changing the framing language/labels
3. Adjusting sort order if needed

If it's <2 hours, I'd advocate for visible-but-differentiated.
If it's >1 day, hiding is probably right for MVP.

---

*This memo is a design perspective offered in the spirit of collaborative decision-making, not a veto of product judgment.*
