# Memo: Orientation System Experience Design Input

**From**: Lead Developer
**To**: Chief Experience Officer
**CC**: PPM, Architect (at your discretion)
**Date**: 2026-01-23
**Re**: #410 MUX-INTERACT-CANONICAL-ENHANCE - Experience design question
**Response-Requested**: yes
**Priority**: High (blocking implementation)

---

## Summary

I'm implementing the orientation system for #410, which transforms canonical queries into Piper's internal "consciousness model" - how Piper orients itself before engaging. I need your input on the experience design, particularly around **trust-aware surfacing depth** and **articulation patterns**.

---

## Background

### The Orientation Concept
The five canonical query categories (Identity, Temporal, Status, Priority, Guidance) currently work reactively - user asks, Piper answers. We're evolving these into Piper's orientation system:

| Pillar | Current (Reactive) | Target (Proactive Articulation) |
|--------|-------------------|--------------------------------|
| Identity | "Who are you?" → response | Piper knows: "I'm assisting with project work" |
| Temporal | "What time is it?" → response | Piper knows: "It's Thursday morning, standup was 2 hours ago" |
| Spatial | "Where am I?" → response | Piper knows: "We're in Slack, discussing the backend refactor" |
| Agency | "What's the priority?" → response | Piper knows: "Top focus is the API deadline Friday" |
| Prediction | "What can you do?" → response | Piper knows: "I can check GitHub, draft messages, track todos" |

### The Experience Goal
When user intent is unclear, Piper articulates contextual options rather than asking "What did you mean?":

```
User: "help"

BEFORE (generic):
Piper: "I can help with todos, calendar, projects, documents..."

AFTER (orientation-informed):
Piper: "I can help several ways right now:
  - Prep for your standup (30 min away)
  - Check the API PR that needs review
  - Show your priority list
  Which feels most useful?"
```

---

## Experience Design Questions

### 1. Trust-Aware Surfacing Depth

PM has decided to integrate trust now rather than later. The question: **How should trust level affect orientation surfacing?**

| Trust Stage | Possible Surfacing Behavior |
|-------------|----------------------------|
| NEW (1) | Minimal - only respond to explicit requests, no proactive articulation |
| BUILDING (2) | Cautious - offer options when asked "help", but don't volunteer |
| ESTABLISHED (3) | Contextual - proactively surface relevant orientation when intent unclear |
| TRUSTED (4) | Anticipatory - "I notice you're back from your meeting. Want the API status?" |

**Questions**:
- Does this gradient feel right experientially?
- Should NEW users ever see proactive orientation, or only reactive?
- At what stage does "I notice..." language become appropriate?

### 2. Articulation Language Patterns

The consciousness philosophy established patterns like:
- "Having had some time to reflect..." (insight surfacing)
- "Over in GitHub..." (spatial awareness)
- "I'm concerned about..." (prediction pillar)

**For orientation articulation, I'm considering**:

| Pillar | Articulation Pattern |
|--------|---------------------|
| Identity | "I'm here to help with [context]" |
| Temporal | "Right now it's [time context]" |
| Spatial | "We're in [place], working on [topic]" |
| Agency | "Your focus seems to be [priority]" |
| Prediction | "I can [relevant capabilities]" |

**Questions**:
- Do these feel natural or robotic?
- Should the patterns vary by channel (Slack vs web chat)?
- Is "seems to be" appropriately humble, or too uncertain?

### 3. Recognition Option Presentation

When presenting recognition options (2-4 choices from orientation):

**Option A: Direct list**
```
"I can help with:
  - Your standup prep
  - The API PR
  - Your priority list"
```

**Option B: Contextually framed**
```
"Given what I know about your morning:
  - Standup is in 30 min - want help prepping?
  - There's an API PR waiting - want to review it?
  - Your priority list has 3 items - want to see them?"
```

**Option C: Narrative framing**
```
"It looks like a busy morning. You've got standup coming up in 30 minutes,
and there's that API PR waiting for review. Want me to help with either of
those, or would you rather check your priority list?"
```

**Questions**:
- Which feels most like Piper and least like a chatbot menu?
- Should framing style vary by trust level?
- Is Option C too verbose for Slack?

### 4. The "None of These" Escape

When orientation-generated options don't match what user wants:

**Current thinking**:
```
"None of those - I actually need [user types]"
Piper: "Got it - let me help with [new topic]"
```

**Questions**:
- Should Piper explicitly offer "or something else?" every time?
- How do we avoid making users feel trapped in a menu system?
- Should repeated "none of these" responses affect trust computation?

---

## Grammar Alignment Question

Per ADR-055, the grammar is "Entities experience Moments in Places." The Chief Architect is being consulted on whether OrientationState should align with this grammar (as a `Perception` of Piper's current `Situation`).

From an experience perspective: **Does orientation-as-perception change how it should feel to users?**

If orientation is Piper's "perception" of its situation, the framing might be more observational:
- "From what I can see..."
- "Looking at your morning..."
- "I notice..."

vs. more declarative:
- "Right now it's..."
- "You're working on..."

**Which better serves the theatrical/consciousness goals?**

---

## Additional Context

- Trust computation (#413) is complete with ProactivityGate ready to use
- #411 (Recognition patterns) and #412 (Intent-Bridge) build on this work
- #414 (DELEGATION) will formalize system-initiated vs user-initiated patterns
- This directly affects how users experience Piper's "consciousness"

---

## What I Need

1. Guidance on trust-aware surfacing gradient
2. Feedback on articulation language patterns
3. Recommendation on recognition option presentation style
4. Philosophy on "none of these" handling
5. Observational vs. declarative framing preference

A brief response with your experience design guidance would help shape the implementation correctly.

---

_Lead Developer_
_2026-01-23 ~5:00 PM_
