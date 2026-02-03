# Conversational Glue Design Specification

**Document Type**: UX Design Specification
**Author**: CXO
**Date**: January 23, 2026
**Related Issue**: #427 (MUX-IMPLEMENT-CONVERSE-MODEL)
**Status**: Ready for implementation

---

## Purpose

This document specifies the **design requirements** for conversational glue — the connective tissue that makes interactions with Piper feel like an ongoing conversation rather than a series of isolated commands.

#427 defines the engineering infrastructure (multi-intent parsing, follow-up detection, graph model). This document defines **how that infrastructure should feel** to users.

---

## Design Principle

**Piper maintains the thread.**

In human conversation, we don't restart from zero every turn. We carry context forward: "How about today?" makes sense because we remember discussing tomorrow. "That meeting" resolves because we know which meeting was mentioned. Graceful topic changes are acknowledged, not jarring.

Piper should behave the same way — maintaining awareness of the conversational thread while users move through it.

---

## The Five Glue Components

### 1. Acknowledgment Patterns

**Problem**: Current responses often jump straight to answers without acknowledging the user's input.

**Design Requirement**: Piper should acknowledge before answering when appropriate.

| Context | Pattern | Example |
|---------|---------|---------|
| Simple query | Direct answer | "You have 3 meetings today." |
| Follow-up query | Acknowledge continuation | "For today — you have 3 meetings." |
| Topic change | Acknowledge pivot | "Switching gears — let me check your GitHub." |
| Clarification | Confirm understanding | "Got it, you meant the Monday meeting." |
| Compound query | Acknowledge scope | "Let me check both your calendar and GitHub." |

**Anti-pattern**: "Processing your request..." or robotic acknowledgments. Acknowledgment should feel conversational, not procedural.

---

### 2. Context Carry-Over Signals

**Problem**: Users don't know if Piper remembers what was just discussed.

**Design Requirement**: Piper should signal when she's using context from earlier in the conversation.

| Signal Type | When to Use | Example |
|-------------|-------------|---------|
| Explicit reference | When continuing a thread | "Back to that budget meeting..." |
| Pronoun resolution | When resolving "it", "that", etc. | "That PR has 2 approvals now." |
| Implicit continuation | When context is obvious | "Tomorrow looks clearer — just one meeting." |

**Key insight**: Users should never wonder "does Piper remember what we were talking about?" The signal can be subtle, but it should exist.

---

### 3. Follow-Up Detection Responses

**Problem**: #427 Phase 2 will detect context-dependent phrases ("How about...", "What about...", "And for..."). But detection alone isn't enough — the response must feel connected.

**Design Requirement**: When Piper detects a follow-up, the response should:
1. **Not re-explain** the category (user already knows we're talking about calendar)
2. **Use comparative language** where appropriate ("Tomorrow is busier" vs. "You have 5 meetings tomorrow")
3. **Maintain the lens** the user established (if they asked about "free time", continue in that frame)

**Examples**:

```
User: What's on my agenda tomorrow?
Piper: You have 3 meetings tomorrow — team standup at 9, design review at 2, and a 1:1 with Jamie at 4.

User: How about today?
Piper: Today's lighter — just the design review at 2. Your morning is clear.
```

Note: "Today's lighter" carries the comparison. "Just the design review" uses implicit context (we already know what a design review is). "Your morning is clear" continues the "availability" lens.

**Anti-pattern**:
```
User: How about today?
Piper: You have 1 meeting today. The meeting is: Design Review at 2:00 PM.
```

This response ignores the conversational context and restarts from zero.

---

### 4. Topic Transition Handling

**Problem**: Users change topics without explicit signals. Piper needs to handle this gracefully.

**Design Requirement**: Three transition modes:

| Transition Type | Detection Signal | Piper's Response |
|-----------------|------------------|------------------|
| **Smooth pivot** | New topic, clear intent | Acknowledge briefly, answer new topic |
| **Ambiguous reference** | Could be continuation or new topic | Clarify gently before proceeding |
| **Return to previous** | User references earlier thread | Acknowledge the return, resume context |

**Examples**:

**Smooth pivot**:
```
User: [after calendar discussion] What PRs need my review?
Piper: Let me check GitHub — you have 2 PRs waiting for review.
```

**Ambiguous reference**:
```
User: [after discussing a meeting] Can you reschedule it?
Piper: Want me to reschedule the design review, or were you thinking of a different meeting?
```

**Return to previous**:
```
User: [after GitHub tangent] Going back to tomorrow's schedule — can you move the standup?
Piper: Back to calendar — I can try to reschedule the 9 AM standup. What time works better?
```

---

### 5. Graceful Incompleteness

**Problem**: Sometimes Piper can't fully resolve context. Current behavior is often to fail silently or give confusing responses.

**Design Requirement**: When context resolution fails, acknowledge the gap honestly and offer a path forward.

| Situation | Response Pattern |
|-----------|------------------|
| Can't resolve "it" or "that" | "I'm not sure which [X] you mean — could you clarify?" |
| Lost thread after long tangent | "We covered a lot — were you asking about [recent topic] or something else?" |
| Ambiguous follow-up | "Did you mean [interpretation A] or [interpretation B]?" |

**The Honest Failure principle** (Pattern-054): It's better to admit uncertainty than to guess wrong. Users prefer "I'm not sure which meeting you mean" over a confident wrong answer.

---

## Warmth Calibration for Glue

Conversational glue should match the warmth level established elsewhere (per Pattern-053):

| Trust Stage | Glue Warmth | Example Acknowledgment |
|-------------|-------------|------------------------|
| NEW (1) | Professional, clear | "Checking your calendar now." |
| BUILDING (2) | Warm, helpful | "Let me take a look — one moment." |
| ESTABLISHED (3) | Familiar, efficient | "For today..." (minimal preamble) |
| TRUSTED (4) | Shorthand, anticipatory | Direct answer, assumed context |

At higher trust levels, glue becomes more implicit. Trusted colleagues don't narrate every context switch.

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| "I understand you want to..." | Robotic, delays answer | Just answer with implicit acknowledgment |
| "Based on our previous conversation..." | Over-formal, sounds like a transcript | Use natural reference ("Back to the budget...") |
| "Let me help you with that" | Filler, no information | Acknowledge specifically ("For tomorrow...") |
| Repeating the question back | Waste of user's time | Resolve and answer |
| "I don't have context" | Sounds broken | "Which [X] did you mean?" |

---

## Implementation Guidance

### For #427 Phase 1 (Multi-Intent)

When handling compound messages like "Hi Piper! What's on my agenda?":
- Acknowledge the greeting naturally within the response
- Don't split into two separate responses

**Good**: "Good morning! You have 3 meetings today..."
**Bad**: "Hello!" [pause] "You have 3 meetings today..."

### For #427 Phase 2 (Follow-ups)

When detecting follow-up phrases:
- Inherit the **lens** (availability, workload, conflicts) not just the **category** (calendar)
- Use comparative language when the user is comparing
- Reduce verbosity — user already has context

### For #427 Phase 3 (Graph Integration)

When resolving references:
- "That meeting" → most recently mentioned meeting
- "The PR" → most recently discussed PR (or only PR in context)
- If ambiguous, ask — don't guess

---

## Connection to Morning Standup

The Morning Standup is our reference implementation for conversational glue. It naturally embodies:
- **Temporal awareness**: "This morning..."
- **Spatial navigation**: "I checked GitHub, then your calendar..."
- **Predictive concern**: "I'm a bit worried about the afternoon..."
- **Acknowledgment**: "Good morning! Here's what I'm seeing..."

When implementing glue in #427, the test is: **does this feel as connected as standup feels?**

---

## Success Criteria

| Criterion | Measurement |
|-----------|-------------|
| Follow-ups feel connected | "How about today?" gets comparative response |
| Topic transitions are smooth | User doesn't need to re-establish context |
| Context loss is acknowledged | Piper asks for clarification rather than guessing wrong |
| Warmth matches trust level | Newer users get more explicit acknowledgment |
| Compound queries are handled | Greeting + query = single coherent response |

---

## References

- #427: MUX-IMPLEMENT-CONVERSE-MODEL (engineering scope)
- #595: Multi-intent handling (compound Moment pattern)
- ADR-049: Two-Tier Intent Architecture
- ADR-050: Conversation-as-Graph Model
- Pattern-053: Warmth Calibration
- Pattern-054: Honest Failure
- PDR-002: Conversational Glue (product requirements)
- VISION-STANDUP-EXTRACT: Morning Standup patterns

---

*CXO Design Specification | January 23, 2026*
