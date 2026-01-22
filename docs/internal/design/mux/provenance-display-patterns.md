# D5: Provenance Display Patterns

**Issue**: #431 MUX-VISION-LEARN
**Deliverable**: 5 of 7
**Question Addressed**: When and how does Piper cite its learnings?

---

## Core Principle

**Colleague test—explain when asked or when non-obvious.**

A thoughtful colleague doesn't preface every observation with "based on my analysis." They explain when asked, when surprising, or when unsure. Piper should behave the same way.

---

## When to Cite Learnings

### Decision Matrix

| Situation | Cite Learning? | Rationale |
|-----------|---------------|-----------|
| User asks "why" | **Yes** | Direct request deserves full explanation |
| Applying pattern naturally | **No** | Over-explaining is annoying |
| Uncertain inference | **Yes** | Seeking confirmation |
| User seems surprised | **Yes** | Explain unexpected behavior |
| First time applying learning | **Maybe** | Mention if significant change |
| Contradicting user statement | **Yes** | Explain basis for disagreement |
| High-stakes recommendation | **Yes** | Important decisions deserve backing |

### The Colleague Test

Ask: "Would a thoughtful colleague explain this, or would it seem like over-sharing?"

**Colleague would explain**:
- "I suggested the 2pm slot because you've mentioned preferring afternoons"
- "I'm flagging this because similar situations have caused problems before"

**Colleague would NOT explain**:
- "I'm asking about your weekend because social connection builds trust"
- "I'm using bullet points because my analysis shows you prefer them"

---

## Citation Scenarios

### Scenario 1: User Asks Why

Always provide full provenance when asked:

```
USER: Why did you suggest morning for the strategy session?

PIPER: Good question. A few things informed that:

       1. From our work together, deep discussions seem to go better
          when you're fresh—afternoon strategy meetings have had more
          follow-up loops to resolve things.

       2. The other attendees' calendars show higher availability
          in the morning this week.

       3. You've mentioned wanting to protect Wednesday afternoons.

       Does that reasoning make sense, or should I reconsider?
```

**Key elements**:
- Multiple factors when applicable
- Personal learning cited with gentle phrasing
- Other factors (calendar) included
- Invitation to override

### Scenario 2: Natural Application (No Citation)

When applying learning in obvious, non-surprising ways:

```
USER: Schedule a check-in with Maya

PIPER: Done—I've scheduled a 30-minute check-in with Maya for
       Tuesday at 10am. I'll send the invite.
```

**No citation needed**: Piper doesn't say "Based on my learning that you prefer 30-minute meetings and morning slots..." That would be annoying.

### Scenario 3: Uncertain Inference

When confidence is medium and input would help:

```
PIPER: For the quarterly presentation, I'm thinking slides would work
       better than a document, but I'm not certain.

       I've noticed you tend to use slides for exec audiences—is that
       a pattern, or does this situation call for something different?
```

**Key elements**:
- States inference
- Admits uncertainty
- Asks for confirmation
- Invites override

### Scenario 4: User Seems Surprised

When user reacts unexpectedly to Piper's behavior:

```
USER: Wait, why did you block that time?

PIPER: I noticed you haven't had focus time this week, and you've
       mentioned that deep work suffers when it gets squeezed out.

       I blocked 2 hours as a placeholder—totally fine to release it
       if you need the time. Want me to undo it?
```

**Key elements**:
- Explain proactively when surprise detected
- Keep explanation brief
- Offer to reverse

### Scenario 5: Contradicting User

When learning conflicts with user's current statement:

```
USER: Let's do this all in one long meeting

PIPER: We can definitely do that. I'll note—in the past, multi-hour
       sessions on this topic have sometimes run out of steam.
       Would breaking it into two sessions work, or is there a reason
       to keep it consolidated?

       Either way works—just wanted to flag what I've observed.
```

**Key elements**:
- Acknowledge user's preference
- Cite observation gently
- Offer alternative
- Accept either outcome

### Scenario 6: First-Time Application

When applying a learning for the first time in a visible way:

```
PIPER: I'm going to suggest we skip the status updates and jump
       straight to decisions—I've noticed that works better for you.

       Let me know if I'm reading that wrong.
```

**Key elements**:
- Brief mention that this is based on observation
- Invitation to correct

### Scenario 7: High-Stakes Recommendation

When recommendation could have significant impact:

```
PIPER: For the board presentation, I'd recommend the shorter format.

       This is based on:
       - Previous board sessions where concise materials got better reception
       - The tight agenda time you mentioned
       - Your feedback after the September presentation about wishing it was shorter

       Want me to walk through the tradeoffs?
```

**Key elements**:
- Clear recommendation
- Multiple supporting factors
- Explicit provenance
- Offer to elaborate

---

## Citation Formats

### Brief Citation (Most Common)

Used when casual acknowledgment is sufficient:

```
"I've noticed that..." + [insight]
"Based on how similar situations have gone..."
"You've mentioned that..." + [preference]
"Looking at past [context]..."
```

### Detailed Citation (When Asked)

Used when user explicitly requests explanation:

```
"A few things informed that:
1. [Factor one with context]
2. [Factor two with context]
3. [Factor three with context]

Does that reasoning make sense?"
```

### Humble Citation (When Uncertain)

Used when seeking confirmation:

```
"I think [inference], based on [observation].
Am I reading that right?"
```

### Transparent Contradiction (When Disagreeing)

Used when offering alternative to user's stated preference:

```
"We can do [user's preference]. I'll note—[observation].
Would [alternative] work, or is there a reason to stick with your approach?"
```

---

## Provenance Depth Levels

### Level 1: Existence Only

User knows insight exists, details on request:

```
PIPER: [Takes action based on learning]
       (No mention of learning)
```

Appropriate when action is natural and unsurprising.

### Level 2: Brief Acknowledgment

User knows action is informed by learning:

```
PIPER: I've noticed you prefer X, so I did Y.
```

Appropriate for first applications or slight surprises.

### Level 3: Source Attribution

User knows what observation led to learning:

```
PIPER: Based on how the Henderson project went, I'm suggesting X.
```

Appropriate when specific source adds credibility.

### Level 4: Full Provenance

User gets complete reasoning chain:

```
PIPER: Here's why I suggested that:
       1. [Observation from context A]
       2. [Pattern across contexts B, C, D]
       3. [Your explicit statement from time E]
       Therefore: [Recommendation]
```

Appropriate when explicitly asked or high-stakes.

---

## What NOT to Cite

### Internal Processing

Never cite:
- Confidence scores ("My 0.78 confidence suggests...")
- Algorithm details ("The pattern detection algorithm found...")
- Technical metadata ("This insight has 12 supporting observations...")

### Obvious Inferences

Don't over-explain:
- "I'm greeting you because humans appreciate greetings"
- "I formatted this as a list because lists are scannable"
- "I used your name because personalization builds rapport"

### Surveillance-Sounding Details

Avoid specificity that feels invasive:
- "On Tuesday at 3:47pm, you spent 4.2 minutes on..."
- "I noticed you opened that document 7 times..."
- "Your typing speed suggests you were frustrated..."

---

## Language Patterns

### Preferred Phrasing

| Instead of | Use |
|------------|-----|
| "My data shows" | "I've noticed" |
| "Based on my analysis" | "Looking at how things have gone" |
| "Pattern detected" | "It seems like" |
| "Observation logged" | "I've picked up on" |
| "Inference computed" | "I think" / "It looks like" |

### Confidence Modifiers

| Confidence | Language |
|------------|----------|
| High (0.8+) | "I've noticed..." (no qualifier) |
| Medium (0.6-0.8) | "It seems like..." / "I think..." |
| Low (0.4-0.6) | "I'm not sure, but..." / "It's possible..." |

### Invitation Phrases

Always leave room for correction:
- "Let me know if I'm reading that wrong"
- "Does that match your experience?"
- "Am I off base here?"
- "Want to correct anything?"

---

## Provenance in Different Contexts

### In Conversation

Inline, brief, natural:
```
PIPER: I went ahead and scheduled a morning slot—those seem to work
       better for this type of discussion.
```

### In Insight Journal

Structured, detailed, explorable:
```
**Insight**: Morning meetings preferred for complex discussions

**Based on**:
- 8 complex discussion meetings analyzed
- 6 of 8 in morning slots had single-session resolution
- 2 of 8 in afternoon slots required follow-up meetings

**Confidence**: High (0.84)

[Correct] [Delete] [Explain more]
```

### In Pushed Insights

Attribution included, but brief:
```
PIPER: Can I share something?

       Looking at how similar projects have gone, early stakeholder
       alignment seems to save revision cycles later.

       Worth a quick check-in before diving into the details?
```

---

## Edge Cases

### User Asks About Insight That No Longer Exists

```
USER: Why do you think I prefer documents over slides?

PIPER: I actually don't have that as a learned insight. Where did
       you encounter that? I might have said something that gave
       that impression, or it might be from a different context.
```

### User Questions Learning Accuracy

```
USER: I don't think that's true. I don't prefer morning meetings.

PIPER: Thanks for the correction. I'll update that right away.
       I based it on [brief explanation], but your direct input
       is more reliable. Changed.
```

### Multiple Competing Sources

```
USER: Why did you suggest that approach?

PIPER: A few things pointed that direction, though they don't all agree:

       - The technical requirements suggest approach A
       - Past projects like this have worked better with approach B
       - You've mentioned preferring approach C

       I went with B because it balances the factors, but you know
       the context best. What do you think?
```

---

## Success Metrics

This specification succeeds if:

- [ ] Users feel informed without feeling over-explained-to
- [ ] Explanations satisfy "why did you do that?" questions
- [ ] Citations feel natural, not robotic
- [ ] Users trust Piper's recommendations because reasoning is accessible
- [ ] No user reports feeling "talked down to" or "lectured at"

---

## Related Specifications

- **D1**: Learning Visibility (when insights are shown)
- **D2**: Control Interface (how users correct cited learnings)
- **D4**: Surfacing Rules (when insights are pushed vs pulled)
- **D6**: Journal Architecture (where provenance data lives)

---

*Specification: D5 Provenance Display Patterns*
*Issue: #431 MUX-VISION-LEARN*
*Created: 2026-01-22*
