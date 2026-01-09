# Contextual Capability Hints: UX Specification

**Document Type**: UX Specification
**Author**: Chief Experience Officer
**Date**: January 4, 2026
**For**: Principal Product Manager, Lead Developer, Front-end Implementation
**Implements**: PDR-002 Discovery Glue - Contextual Capability Hints

---

## Overview

Contextual capability hints surface Piper's capabilities at moments when they're relevant—after successful task completion, during natural pauses, or when context suggests a capability would help.

PDR-002 establishes throttling rules. This document specifies visual design, placement, timing, and dismissal patterns.

---

## Design Principles

1. **Relevant, not impressive**: Surface capabilities that relate to what user just did
2. **Peripheral, not central**: Hints should be noticeable but not block workflow
3. **Dismissible, not persistent**: Easy to ignore, never blocks progress
4. **Learning, not lecturing**: Show what's possible, don't explain how it works

---

## Hint Types

### Type A: Post-Task Suggestion

**Trigger**: User completes a task successfully

**Example**:
```
User: "Generate my standup"
Piper: [standup content]

┌─────────────────────────────────────────────────────────┐
│ 💡 I can also post this to Slack or create issues from  │
│    the blockers.                                   [×]  │
└─────────────────────────────────────────────────────────┘
```

### Type B: Context-Aware Suggestion

**Trigger**: Piper detects context that suggests a capability

**Example**:
```
User: "Show me my calendar for today"
Piper: [calendar with meeting in 30 minutes]

┌─────────────────────────────────────────────────────────┐
│ 💡 You have a standup in 30 minutes. Want me to prep    │
│    your notes?                                    [×]   │
└─────────────────────────────────────────────────────────┘
```

### Type C: Dead-End Recovery (Different from hints—see Recovery section)

---

## Visual Design

### Hint Container

```
┌─────────────────────────────────────────────────────────┐
│ 💡 [Hint text - one sentence, actionable]         [×]   │
└─────────────────────────────────────────────────────────┘
```

**Specs**:
- Background: Subtle tint (light blue or light gray, not yellow—not a warning)
- Border: 1px, slightly darker than background
- Border radius: 8px (softer than main UI cards)
- Icon: 💡 or subtle lightbulb SVG (not ⚠️ or ℹ️)
- Dismiss: [×] in top-right, visible on hover/focus

### Placement

**After Piper's response**:
- Below the response content
- Above the input field
- Indented slightly to distinguish from main response

```
┌──────────────────────────────────────┐
│ Piper's Response                     │
│ [Main content here]                  │
│                                      │
│   ┌────────────────────────────┐     │
│   │ 💡 Capability hint    [×]  │     │
│   └────────────────────────────┘     │
│                                      │
└──────────────────────────────────────┘
┌──────────────────────────────────────┐
│ [Type your message...]               │
└──────────────────────────────────────┘
```

### Typography

- Font size: Slightly smaller than body text (0.9em)
- Color: Muted but readable (not gray-on-gray)
- Weight: Regular (not bold, not light)

### Animation

- **Entrance**: Fade in + slight slide up (200ms, 50ms delay after response)
- **Dismissal**: Fade out (150ms)
- **No bounce, no attention-grabbing animation**

---

## Timing & Throttling

### From PDR-002

| Rule | Implementation |
|------|----------------|
| Maximum 2 suggestions per 5 interactions | Track hint_count and interaction_count per session |
| Stop after 2 ignored suggestions | If hint dismissed without action twice, suppress for session |
| Never interrupt flow | Only show at natural pause points (after response completes) |
| Never repeat same hint | Track shown_hints per user, don't resurface |

### Timing Details

- **Display delay**: 500ms after response renders (let user read first)
- **Auto-dismiss**: None (user controls dismissal)
- **Session reset**: hint_count resets on new session
- **Permanent suppression**: If user clicks "Don't show hints" (see below), suppress indefinitely

---

## Dismissal Patterns

### Quick Dismiss

**Action**: Click [×] or press Escape
**Effect**: Hint fades out, counts as "ignored"
**No confirmation needed**

### Action Dismiss

**Action**: User clicks/taps on the hint to act on it
**Effect**: Hint fades out, action begins, counts as "accepted"

### Implicit Dismiss

**Action**: User starts typing next message
**Effect**: Hint fades out, counts as "ignored"
**Rationale**: User is moving on; don't leave hint lingering

### Permanent Suppress

**UI**: After 2nd ignored hint, next hint includes option:

```
┌─────────────────────────────────────────────────────────┐
│ 💡 I can also track time on tasks.               [×]   │
│    ───────────────────────────────────                  │
│    Don't show suggestions like this                     │
└─────────────────────────────────────────────────────────┘
```

**Action**: Clicking "Don't show suggestions" suppresses hints for this user
**Reversible**: In Settings → Preferences → "Show capability hints"

---

## Hint Content Guidelines

### Structure

```
💡 [What Piper can do] + [Optional: trigger phrase or action]
```

### Examples

| After | Hint |
|-------|------|
| Standup generated | "I can also post this to Slack or create issues from blockers." |
| Issue created | "Want me to add it to a project or set a milestone?" |
| Calendar shown | "I can find free time for meetings—just say 'schedule time with...'" |
| Document summarized | "I can also extract action items or create issues from this." |
| Todo completed | "Nice! I can show you what's next or generate a progress summary." |

### Voice

- First person ("I can...")
- Action-oriented
- Brief (under 15 words if possible)
- No exclamation points
- No "Did you know..." framing

### Anti-Patterns

❌ "Did you know I can also post to Slack?"
✅ "I can also post this to Slack."

❌ "Pro tip: Try asking me to create issues from blockers!"
✅ "I can create issues from blockers if you'd like."

❌ "You might find it helpful to..."
✅ "I can also..."

---

## Mobile Considerations

### Compact Hints

On narrow screens, hints may need to wrap:

```
┌───────────────────────────┐
│ 💡 I can also post this   │
│    to Slack.        [×]   │
└───────────────────────────┘
```

### Touch Targets

- Dismiss [×]: Minimum 44×44px touch target
- Entire hint is tappable to act on suggestion

### Swipe Dismiss

- Swipe right on hint = dismiss (same as [×])
- Provides quick, natural mobile interaction

---

## State Management

### Session State

```javascript
{
  hint_count: 0,           // Hints shown this session
  interaction_count: 0,    // Total interactions this session
  ignored_count: 0,        // Hints dismissed without action
  shown_hints: ["standup_to_slack", "issue_to_project", ...]
}
```

### User Preferences (Persistent)

```javascript
{
  hints_enabled: true,     // Can be toggled in Settings
  suppressed_hints: [],    // Specific hints user said "don't show again"
}
```

### Hint Eligibility Check

```python
def should_show_hint(session, user, hint_id):
    if not user.hints_enabled:
        return False
    if hint_id in user.suppressed_hints:
        return False
    if hint_id in session.shown_hints:
        return False
    if session.ignored_count >= 2:
        return False
    if session.hint_count >= 2 and session.interaction_count < 5:
        return False
    return True
```

---

## Hint Catalog

Initial hints to implement:

| ID | After | Hint Text |
|----|-------|-----------|
| standup_to_slack | Standup generated | "I can also post this to Slack." |
| standup_issues | Standup with blockers | "Want me to create issues from the blockers?" |
| issue_to_project | Issue created | "I can add this to a project or set a milestone." |
| calendar_schedule | Calendar viewed | "Need to schedule something? Just say 'find time for...'" |
| doc_actions | Document summarized | "I can extract action items from this." |
| todo_next | Todo completed | "Want to see what's next?" |
| pr_release | PR list shown | "I can generate release notes from merged PRs." |
| github_triage | Issues viewed | "Want me to suggest priority for these?" |

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Hint acceptance rate | >25% | Hints acted on / Hints shown |
| Hint annoyance rate | <10% | "Don't show" clicks / Hints shown |
| Discovery attribution | >20% | Features first used via hint / Total feature discoveries |
| Session depth after hint | +1.5 interactions | Average interactions after accepted hint vs baseline |

---

## Relationship to Other Discovery Mechanisms

Contextual hints are ONE discovery mechanism. They complement:

- **Empty state education**: Hints in empty views
- **"What can you help with?"**: Explicit capability query
- **Dead-end recovery**: Options when Piper can't help
- **Command palette**: Direct capability access

Hints should not duplicate what these other mechanisms provide. If a capability is obvious from the empty state, don't hint at it again after first use.

---

*Contextual Hint UX Spec v1 | January 4, 2026 | Chief Experience Officer*
