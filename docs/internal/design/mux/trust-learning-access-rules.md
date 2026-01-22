# D7: Trust-Based Access Rules

**Issue**: #431 MUX-VISION-LEARN
**Deliverable**: 7 of 7
**Question Addressed**: What can each trust level see and do with learning?

---

## Core Principle

**Trust gradient governs learning visibility consistently.**

As trust develops, users gain access to more learning features. This mirrors how human colleagues share observations—cautiously at first, more freely as rapport builds.

---

## Trust Stage Overview

| Stage | Name | Relationship | Learning Stance |
|-------|------|--------------|-----------------|
| **1** | New | First interactions | Minimal learning visibility |
| **2** | Building | Regular use, growing comfort | On-request access |
| **3** | Established | Demonstrated trust | Proactive sharing |
| **4** | Trusted | Deep comfort, explicit signals | Full access |

---

## Stage 1: New

### Relationship Characteristics

- First 10 interactions
- Piper is cautious and responsive
- User is still calibrating expectations

### Learning Access

| Feature | Available? | Notes |
|---------|------------|-------|
| Insight Journal (browse) | Yes | Available but not promoted |
| Pull mode queries | Yes | Responds when asked |
| Push mode (proactive) | **No** | Never interrupts |
| Reflection summaries | **No** | Too presumptuous |
| Session Journal | **No** | Reserved for high trust |
| Correction/deletion | Yes | Always available |

### UX Behavior

**Piper's stance**: "I'm learning from our work together, but I'll only share observations when you ask."

**Example interactions**:
```
USER: What have you learned about me?

PIPER: We're still getting to know each other, so I don't have much yet.
       I've noticed a few things from our conversations—would you like
       to see them?

       As we work together more, I'll pick up on patterns that might
       be helpful.
```

**What Piper avoids**:
- Volunteering observations
- Suggesting based on learned patterns
- Referencing past interactions without prompt

---

## Stage 2: Building

### Relationship Characteristics

- 10-50 successful interactions
- Piper is more confident in understanding
- User has corrected or confirmed some insights

### Learning Access

| Feature | Available? | Notes |
|---------|------------|-------|
| Insight Journal (browse) | Yes | Full access |
| Pull mode queries | Yes | Rich responses |
| Push mode (proactive) | **No** | Still waits to be asked |
| Reflection summaries | On request | "Want to hear what I've noticed?" |
| Session Journal | **No** | Reserved for Stage 4 |
| Correction/deletion | Yes | Full access |

### UX Behavior

**Piper's stance**: "I've learned things that might help. Ask anytime, but I won't interrupt."

**Example interactions**:
```
USER: Schedule a meeting with the design team

PIPER: Done—I've set up a 45-minute meeting for Thursday at 10am.

       [Does NOT say: "I scheduled it in the morning because I've
       learned you prefer that." - too presumptuous at this stage]
```

```
USER: What patterns have you noticed in my work?

PIPER: I've picked up a few things:

       - You seem to prefer morning slots for collaborative work
       - Async communication works well with the design team
       - You tend to batch similar tasks together

       Want me to explain where any of these came from?
```

**Key difference from Stage 1**: Richer responses to queries, more confident insights. But still no unsolicited sharing.

---

## Stage 3: Established

### Relationship Characteristics

- 50+ successful interactions
- Pattern recognition demonstrated
- User has engaged with insights positively

### Learning Access

| Feature | Available? | Notes |
|---------|------------|-------|
| Insight Journal (browse) | Yes | Full access |
| Pull mode queries | Yes | Rich, contextual responses |
| Push mode (proactive) | **Yes** | Batched, periodic |
| Reflection summaries | Yes | Weekly/configurable |
| Session Journal | **No** | Reserved for Stage 4 |
| Correction/deletion | Yes | Full access |

### UX Behavior

**Piper's stance**: "I notice things that might help, and I'll share when relevant."

**Example interactions**:
```
PIPER: [Morning standup]
       Good morning! A few things from my recent reflections:

       - The Henderson project tends to generate follow-up on Fridays
       - You've had a lot of back-to-back meetings lately—might be
         worth protecting some buffer time

       Ready to dive into today?
```

```
PIPER: [During task]
       Can I share something that might help?

       Looking at similar projects, early stakeholder alignment tends
       to reduce revision cycles. Worth a quick check-in?

       [Yes, thanks] [Not now] [Tell me more]
```

**Key difference from Stage 2**: Piper initiates sharing (batched, not intrusive).

### Push Mode Rules at Stage 3

| Rule | Value |
|------|-------|
| Frequency limit | Max 1 push per 24 hours |
| Confidence threshold | 0.80 |
| Format | Batched digest or single high-relevance item |
| Dismissal | Graceful, no follow-up guilt |

---

## Stage 4: Trusted

### Relationship Characteristics

- Extended successful engagement
- User has given explicit comfort signals
- Deep collaborative relationship

### Progression Note

**Stage 4 is NOT automatic.** Unlike Stages 1-3 which progress based on interaction count, Stage 4 requires explicit user signal:

- "I trust you to handle this autonomously"
- "You don't need to check with me on routine things"
- "I'm comfortable with you being more proactive"

### Learning Access

| Feature | Available? | Notes |
|---------|------------|-------|
| Insight Journal (browse) | Yes | Full access |
| Pull mode queries | Yes | Complete transparency |
| Push mode (proactive) | Yes | Contextual, in-moment |
| Reflection summaries | Yes | Configurable frequency |
| Session Journal | **Yes** | On explicit request |
| Correction/deletion | Yes | Full access |

### UX Behavior

**Piper's stance**: "I'm a trusted partner. I'll act on what I know and explain when helpful."

**Example interactions**:
```
PIPER: [Inline while scheduling]
       I scheduled the strategy session for 9am—complex discussions
       tend to go better when you're fresh.

       [Takes action, explains briefly, doesn't wait for permission]
```

```
USER: Show me my session history

PIPER: Here's your recent session log:

       [Displays detailed session journal entries]

       This is the raw record. The Insight Journal shows what I've
       learned from it—want to see that comparison?
```

### Push Mode Rules at Stage 4

| Rule | Value |
|------|-------|
| Frequency limit | Contextual (no hard limit) |
| Confidence threshold | 0.75 |
| Format | Inline suggestions, natural integration |
| Timing | In-moment when relevant |

---

## Trust-Learning Matrix Summary

| Feature | Stage 1 | Stage 2 | Stage 3 | Stage 4 |
|---------|---------|---------|---------|---------|
| **Insight Journal browse** | Yes | Yes | Yes | Yes |
| **Pull queries** | Yes | Yes | Yes | Yes |
| **Push (proactive)** | No | No | Yes (batched) | Yes (contextual) |
| **Reflection summaries** | No | On request | Automatic | Automatic |
| **Session Journal** | No | No | No | Yes |
| **Act on learning without asking** | No | Rarely | Sometimes | Often |
| **Explain learning source** | On ask | On ask | Often proactive | Natural integration |

---

## Progression Mechanics

### Stage 1 → Stage 2

**Trigger**: 10 successful interactions

**Definition of "successful"**:
- User engaged with response
- No correction or complaint
- Task completed or conversation concluded naturally

### Stage 2 → Stage 3

**Trigger**: 50 successful interactions + evidence of pattern recognition value

**Evidence required**:
- User has queried insights at least once
- No significant corrections in recent interactions
- Positive engagement with at least one learning-based suggestion

### Stage 3 → Stage 4

**Trigger**: Explicit user comfort signal

**Examples of signals**:
- "I trust you to handle this type of thing"
- "You don't need to check with me on routine decisions"
- User opts in via settings: "Increase Piper's autonomy"

**NOT triggers** (don't assume Stage 4):
- Large number of interactions alone
- User hasn't complained
- User seems happy

---

## Regression Mechanics

### Trust Regression Triggers

| Trigger | Effect |
|---------|--------|
| 3 consecutive negative outcomes | Drop 1 stage |
| 90 days inactivity | Drop 1 stage |
| User says "you overstepped" | Immediate review |
| Multiple corrections in short period | Pause push mode |

### Floor Logic

- Once Stage 2 achieved, never drops below Stage 2
- "You've known me long enough" principle

### Regression UX

```
PIPER: [After regression from Stage 3 to Stage 2]

       I'm going to dial back on proactive suggestions for a bit.
       I may have been overstepping—I'll wait for you to ask.

       If you want me to be more proactive again, just say so.
```

---

## User Override Options

### Opting Into More Access

User can request higher-stage features at any level:

```
USER: I want you to share insights more proactively

PIPER: Got it. I'll start sharing observations when they seem relevant,
       even though we're still building trust. You can always tell me
       to dial it back.
```

**Note**: This grants the FEATURE, not the TRUST STAGE. Piper records it as explicit preference.

### Opting Into Less Access

User can restrict features at any level:

```
USER: Stop pushing insights at me

PIPER: Understood. I won't proactively share insights anymore—but
       they'll still be available if you ask or browse the Insight Journal.

       Let me know if you change your mind.
```

**Note**: This is a preference, not trust regression. Piper doesn't interpret it as distrust.

---

## Trust Transparency

### What Users See

Users do NOT see:
- Explicit "Trust Level: 3" displays
- Progress bars to next stage
- Notifications of trust changes

Users CAN ask:
- "Why did you do that without asking?"
- "Why aren't you being more proactive?"

And Piper will explain:
```
USER: Why aren't you sharing observations with me?

PIPER: We're still getting to know each other. I'm learning from our
       work, but I want to make sure I'm not overstepping.

       Once we've worked together more, I'll be more comfortable
       sharing what I notice. You can also ask me anytime—I just
       won't volunteer it yet.
```

### What Users DON'T See

- Stage numbers
- Interaction counts
- Internal trust scoring

**Rationale**: Explicit trust displays would feel mechanical and could encourage gaming. Trust should feel organic.

---

## Edge Cases

### Fast Correction

User corrects Piper immediately and frequently:

```
[Stage 2, 5 corrections in 10 interactions]

PIPER: (internal) Pause advancement. Stay at Stage 2 until corrections
       decrease or user confirms pattern accuracy.
```

### Explicit Trust Withdrawal

User says "I don't trust you":

```
USER: I don't trust your suggestions

PIPER: I understand. I'll step back on proactive suggestions and wait
       for you to ask. If I've given you a reason not to trust my
       judgment, I'd like to understand—but no pressure to explain.

       (internal) Regress to Stage 1 behavior, note explicit distrust
```

### Trust vs Preference Mismatch

User at Stage 2 wants Stage 4 features:

```
USER: Just do it without asking me

PIPER: I can be more autonomous if you'd like. Right now I'm being
       cautious because we're still building our working relationship.

       If you want me to act more independently, I will—just know I
       might make some mistakes while I'm still learning your preferences.

       Should I go ahead and be more proactive?
```

---

## Integration with Other Specs

### D1: Learning Visibility

Trust stage determines what's visible by default (not what's accessible—everything is accessible on request).

### D2: Control Interface

All control operations (correct, delete, reset) available at all stages. Trust doesn't limit control.

### D3: Composting Experience

Composting happens at all stages. Visibility of composting outputs varies by trust.

### D4: Surfacing Rules

Push mode thresholds and triggers vary by stage (see D4 for details).

### D5: Provenance Display

Higher trust = more proactive provenance sharing. Lower trust = only on request.

### D6: Journal Architecture

Session Journal access restricted to Stage 4. Insight Journal available to all.

---

## Success Metrics

This specification succeeds if:

- [ ] Users feel Piper "gets" them over time (trust progression)
- [ ] Stage 1-2 users never feel intruded upon
- [ ] Stage 3+ users find proactive sharing valuable
- [ ] Trust regression feels fair, not punitive
- [ ] Users can always opt in/out of features regardless of stage
- [ ] No user asks "what's my trust score?" (not salient)

---

## Related Specifications

- **D1**: Learning Visibility Specification
- **D2**: Control Interface Patterns
- **D3**: Composting Experience Design
- **D4**: Insight Journal Surfacing Rules
- **D5**: Provenance Display Patterns
- **D6**: Journal Architecture Specification

---

*Specification: D7 Trust-Based Access Rules*
*Issue: #431 MUX-VISION-LEARN*
*Created: 2026-01-22*
