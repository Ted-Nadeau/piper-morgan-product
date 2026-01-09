# Cross-Session Greeting: Visual Treatment & Interaction Design

**Document Type**: UX Specification
**Author**: Chief Experience Officer
**Date**: January 4, 2026
**For**: Principal Product Manager, Lead Developer, Front-end Implementation
**Implements**: PDR-001 v3 Cross-Session Greeting Patterns

---

## Overview

PDR-001 establishes context-aware greetings that adapt based on session history. This document specifies the visual treatment and interaction design for the "continue or start fresh?" experience.

---

## Design Principles

1. **Light touch**: Context should feel helpful, not surveillance
2. **Easy pivot**: "Start fresh" must be frictionless, not buried
3. **Graceful absence**: When there's nothing to reference, don't force it
4. **Emotional awareness**: Bad sessions get clean slates

---

## Greeting Scenarios

### Scenario A: Same Day Return (Active Context)

**Trigger**: User returns within same calendar day, previous session had meaningful work

**Greeting Pattern**:
```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  Welcome back! We were working on the Q1 roadmap        │
│  review.                                                │
│                                                         │
│  ┌──────────────────┐  ┌──────────────────┐            │
│  │   Continue ↗     │  │   Start fresh    │            │
│  └──────────────────┘  └──────────────────┘            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Visual Specs**:
- Context summary: 1 line, specific reference to work item
- Two equal-weight buttons, "Continue" slightly emphasized (filled vs outline)
- No timestamp clutter—"same day" is implicit

**Interaction**:
- "Continue" → Load previous context, Piper summarizes where we left off
- "Start fresh" → Clear context, standard greeting

---

### Scenario B: Next Day Return (Light Reference)

**Trigger**: 1-2 days since last session, previous session had meaningful work

**Greeting Pattern**:
```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  Good morning! Yesterday we discussed GitHub issue      │
│  triage.                                                │
│                                                         │
│  ┌──────────────────┐  ┌──────────────────┐            │
│  │   Pick up there  │  │   Something new  │            │
│  └──────────────────┘  └──────────────────┘            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Visual Specs**:
- Context summary: Brief topic reference (not full detail)
- Softer language: "Pick up there" / "Something new" (not "Continue" / "Start fresh")
- Equal visual weight on both options

**Interaction**:
- "Pick up there" → Brief recap then ready for input
- "Something new" → Standard greeting, no context loaded

---

### Scenario C: Week+ Gap (Offer Choice)

**Trigger**: 7+ days since last session

**Greeting Pattern**:
```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  Hey, it's been a bit! Last time we were looking at     │
│  sprint planning.                                       │
│                                                         │
│  ┌──────────────────┐  ┌──────────────────┐            │
│  │   Catch me up    │  │   Fresh start    │            │
│  └──────────────────┘  └──────────────────┘            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Visual Specs**:
- Warmer tone acknowledging the gap
- "Catch me up" implies Piper will summarize, not dump raw history
- "Fresh start" is default-weight (user likely wants new context)

**Interaction**:
- "Catch me up" → Piper provides 2-3 sentence summary of last session's key points
- "Fresh start" → Standard greeting

---

### Scenario D: Month+ Gap (Gentle Reorientation)

**Trigger**: 30+ days since last session

**Greeting Pattern**:
```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  Welcome back! It's been a while.                       │
│                                                         │
│  ┌──────────────────┐  ┌──────────────────┐            │
│  │   What's changed │  │   Start fresh    │            │
│  └──────────────────┘  └──────────────────┘            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Visual Specs**:
- No specific context reference (too stale to be relevant)
- "What's changed" offers to show what Piper has learned/integrated since last visit
- "Start fresh" is equal weight (likely choice)

**Interaction**:
- "What's changed" → Summary of new integrations, capabilities, or notable activity
- "Start fresh" → Standard greeting

---

### Scenario E: Bad Last Session (Clean Slate)

**Trigger**: Previous session ended with frustration signals (explicit abandonment, multiple dead-ends)

**Greeting Pattern**:
```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  Good morning! What can I help with today?              │
│                                                         │
│  ┌─────────────────────────────────────────┐           │
│  │  Type a message...                      │           │
│  └─────────────────────────────────────────┘           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Visual Specs**:
- No reference to previous session
- No choice buttons—just open input
- Standard, friendly greeting

**Interaction**:
- User starts fresh with no baggage from frustrating experience
- Previous context still accessible if user explicitly asks ("what were we working on?")

---

### Scenario F: Trivial Previous Session

**Trigger**: Previous session was brief, contained only greetings or single quick query

**Greeting Pattern**:
```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  Hi! What can I help with?                              │
│                                                         │
│  ┌─────────────────────────────────────────┐           │
│  │  Type a message...                      │           │
│  └─────────────────────────────────────────┘           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Visual Specs**:
- No context reference (nothing meaningful to reference)
- Clean start is the only option

---

## Visual Design Specifications

### Button Styling

**Primary action** (Continue/Pick up):
- Filled background, brand color
- Slightly larger touch target
- Left position (for LTR reading)

**Secondary action** (Fresh start/Something new):
- Outline style, same brand color
- Equal size touch target
- Right position

**When equal weight desired** (week+ scenarios):
- Both outline style
- Same visual treatment

### Typography

- **Greeting line**: Body text, conversational tone
- **Context reference**: Same weight, integrated into sentence (not a separate "Previous: X" label)
- **Button text**: Sentence case, action-oriented verbs

### Spacing

- Greeting block: Centered in chat area
- Padding: Comfortable whitespace (not cramped)
- Buttons: Horizontal layout on desktop, stack vertically on mobile if needed

### Animation

- **Entrance**: Fade in (200ms), no bounce or slide
- **Button press**: Standard press state (slight darken/scale)
- **Transition out**: Fade, then first Piper message appears

---

## Mobile Considerations

### Compact Layout

On narrow screens:
```
┌─────────────────────────┐
│                         │
│  Welcome back! We were  │
│  working on Q1 roadmap. │
│                         │
│  ┌───────────────────┐  │
│  │     Continue      │  │
│  └───────────────────┘  │
│  ┌───────────────────┐  │
│  │    Start fresh    │  │
│  └───────────────────┘  │
│                         │
└─────────────────────────┘
```

- Buttons stack vertically
- Primary action on top
- Adequate tap targets (44px minimum height)

### Quick Dismissal

- Tapping anywhere outside greeting block = "Start fresh" (implicit dismissal)
- Swiping down on greeting = dismiss to fresh start
- User can always type directly to skip greeting entirely

---

## Edge Cases

### Multiple Unfinished Threads

If previous session touched multiple topics:
- Reference the most recent/substantial one
- Don't try to list all ("We were working on X, Y, and Z...")
- "Pick up" loads full context; user can navigate to other threads

### Integration Changes Since Last Session

If new integrations connected since last visit (relevant for month+ gaps):
- "What's changed" should highlight: "You've connected Slack since we last talked. Want to see what I can do with it?"

### First-Ever Session

No greeting block at all. Proceed directly to FTUX flow per PDR-001.

### Returning After FTUX Abandonment

If user left during FTUX and returns:
- Offer to continue FTUX: "Looks like we didn't finish setting up. Want to continue, or skip for now?"
- "Skip" should work—user can complete setup later

---

## Implementation Notes

### Context Detection Logic

```
if (previous_session.frustration_signals):
    scenario = E  # Clean slate
elif (previous_session.trivial):
    scenario = F  # No reference
elif (days_since < 1):
    scenario = A  # Same day
elif (days_since < 3):
    scenario = B  # Next day
elif (days_since < 30):
    scenario = C  # Week+ gap
else:
    scenario = D  # Month+ gap
```

### Frustration Signals (from PDR-001 v3)

- Explicit abandonment language: "never mind," "forget it," "this isn't working"
- Session closed mid-task (no natural completion)
- High dead-end ratio (>50% of exchanges hit limits)
- Explicit negative feedback

### Context Summary Generation

- Pull from session metadata, not raw transcript
- 1 sentence max for context reference
- Entity names preferred over descriptions ("Q1 roadmap" not "that document we discussed")

---

## Success Criteria

| Metric | Target |
|--------|--------|
| Context acceptance rate | >60% choose "Continue" when offered |
| False positive frustration detection | <5% clean slates when user wanted to continue |
| Time to first message | <10 seconds (greeting doesn't slow users down) |
| User feedback | "Greeting felt helpful" > "Greeting felt intrusive" |

---

*Cross-Session Greeting UX Spec v1 | January 4, 2026 | Chief Experience Officer*
