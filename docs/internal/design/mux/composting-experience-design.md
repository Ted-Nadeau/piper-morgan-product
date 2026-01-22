# D3: Composting Experience Design

**Issue**: #431 MUX-VISION-LEARN
**Deliverable**: 3 of 7
**Question Addressed**: What do users see when objects decompose into learnings?

---

## Core Principle

**Composting is reflection, not surveillance.**

When Piper transforms old objects into learnings, users should experience this as thoughtful reflection—like a colleague who's "had time to think about things"—not as evidence of continuous monitoring.

---

## The "Filing Dreams" Metaphor

### Why This Metaphor

Humans process experiences during sleep, consolidating memories and extracting patterns. We call this "sleeping on it" or "letting it percolate." Piper's composting works similarly:

- Processing happens during "rest" (quiet hours)
- Patterns emerge from accumulated experience
- Insights surface as reflection, not real-time analysis

### What Users Experience

**User does NOT experience**:
- "I've been watching your behavior and noticed..."
- "While you were away, I analyzed..."
- "Based on my surveillance of your activities..."

**User DOES experience**:
- "Having had some time to reflect..."
- "Looking back on our recent work..."
- "Something occurred to me..."

---

## When Composting Happens

### Quiet Hours (Default: 2-5 AM local)

Composting runs during user's configured quiet hours:
- Mimics "sleeping on it"
- Doesn't interfere with active work
- Creates natural temporal separation between activity and reflection

### User Configuration

```
Piper Settings > Learning > Reflection Time

When should Piper reflect on recent work?
○ Default (2-5 AM)
○ Custom: [time picker]
○ Never (disable background learning)
```

### Manual Trigger

Users can trigger reflection:
- "Take some time to reflect on [project/topic]"
- "What have you learned from our work this week?"

This runs composting on-demand, surfacing results immediately.

---

## Composting Output: Reflection Summaries

### Format

Reflection summaries are batched, periodic, and natural:

```
Good morning! I've had some time to reflect on our recent work.

A few things that occurred to me:

**About the Henderson project**
Looking back at how the proposal evolved, I noticed you refined the scope
three times before it felt right. That iterative approach seems to work
well for complex proposals. (high confidence)

**About your schedule**
The past two weeks had a lot of back-to-back meetings. On days when you
had buffer time between meetings, the follow-up tasks got done faster.
Might be worth protecting some transition time. (medium confidence)

Would you like to discuss any of these, or should I just keep them in mind?
```

### Key Characteristics

| Aspect | Requirement |
|--------|-------------|
| **Tone** | Reflective, colleague-like |
| **Timing** | Morning or at session start |
| **Volume** | 2-4 insights max per summary |
| **Opt-out** | User can skip: "not now" |
| **Follow-up** | Offers discussion, doesn't require it |

---

## Language Patterns

### Reflection Openers

Use these to introduce composting insights:

| Appropriate | Avoids |
|-------------|--------|
| "Having had time to think about it..." | "After analyzing your data..." |
| "Looking back on our work together..." | "Based on my observations..." |
| "Something occurred to me..." | "I detected a pattern..." |
| "I've been reflecting on..." | "I've been monitoring..." |
| "It strikes me that..." | "My analysis shows..." |

### Temporal Framing

**Good**: Implies reflection happened separately from activity
- "Looking back at last week..."
- "Thinking about how that project went..."
- "In hindsight..."

**Bad**: Implies real-time surveillance
- "I noticed you doing X yesterday..."
- "While you were working, I saw..."
- "I've been tracking..."

### Confidence Expression

**High confidence** (0.8+):
- "I've noticed that..." (no qualifier needed)
- "It's become clear that..."
- "A consistent pattern..."

**Medium confidence** (0.6-0.8):
- "It seems like..."
- "I think..."
- "This might be a pattern..."

**Low confidence** (0.4-0.6):
- "I'm not sure, but..."
- "It's possible that..."
- "Something to consider..."

---

## What Users See: Scenarios

### Scenario 1: Morning Standup Integration

Natural point for reflection summaries:

```
PIPER: Good morning! Here's what's on your radar today:
       [calendar, tasks, etc.]

       I've also had some time to reflect:
       - The quarterly planning seems to generate the most follow-up tasks
         on Fridays. Worth keeping that afternoon light?

       Ready to dive in?
```

**Key**: Reflection is offered, not forced. User can engage or move on.

### Scenario 2: Project Milestone Reflection

When a project reaches a significant point:

```
PIPER: The Henderson proposal just got approved—nice work!

       Looking back on how it came together, a few things stood out:
       - The early stakeholder alignment saved revision cycles later
       - The timeline buffer you built in absorbed the scope creep

       Want me to note these for future proposals, or is this project unique?
```

**Key**: Reflection tied to meaningful moment, not arbitrary timing.

### Scenario 3: Periodic Summary (Stage 3+)

Weekly or biweekly batched reflection:

```
PIPER: Weekly reflection (your Saturday morning digest)

       **Work patterns**
       This week had more reactive work than planned work. Might be worth
       looking at where the interruptions came from.

       **Meeting insights**
       The Tuesday all-hands seems to generate the most follow-up items.
       You usually capture them, but some slip.

       **Something new**
       I noticed a new collaboration pattern with the design team—more
       async, shorter feedback loops. Seems to be working well.

       [Acknowledge] [Discuss] [Not now]
```

### Scenario 4: User Asks for Reflection

On-demand composting:

```
USER: What have you learned from the last month?

PIPER: Let me think about that...

       [Brief pause—composting runs]

       Here's what stands out from the past month:

       **Productivity patterns**
       - Morning focus time is when the deep work happens
       - Thursdays tend to be your catch-up day
       - You're more responsive to Slack in the afternoon

       **Project insights**
       - The marketing launch had the tightest timeline but cleanest execution
       - Technical debt issues cluster around the end of sprints

       **Something I'm less sure about**
       - It seems like cross-team meetings drain more than same-team meetings,
         but I don't have enough data yet.

       What would you like to explore?
```

---

## Notification Rules

### What Gets Batched

| Event | Notification | Batch Into |
|-------|--------------|------------|
| Single insight extracted | None | Weekly summary |
| Important pattern discovered | Brief mention | Morning standup |
| User correction affects multiple insights | Acknowledgment | Immediate (one message) |
| Composting cycle complete | None | Next natural touchpoint |

### What Gets Individual Attention

| Event | Treatment |
|-------|-----------|
| High-confidence insight directly relevant now | Contextual surfacing |
| Contradiction discovered (learning invalidates prior) | Proactive correction |
| User explicitly requests reflection | On-demand summary |

### Notification Cadence by Trust Level

| Trust Level | Reflection Frequency | Delivery |
|-------------|---------------------|----------|
| Stage 1 | None proactive | Pull only |
| Stage 2 | None proactive | Pull only |
| Stage 3 | Weekly or biweekly | Morning digest |
| Stage 4 | As relevant | Contextual + digest |

---

## Composting Transparency

### Users Can Ask

- "What are you reflecting on?"
- "What's in your composting queue?"
- "When do you process learnings?"

### Honest Answers

```
USER: What are you reflecting on?

PIPER: Right now I have 23 objects from the past two weeks that are ready
       for composting—mostly completed tasks, closed issues, and finished
       conversations.

       When I process them (tonight during my quiet time), I'll look for:
       - Patterns in how work got done
       - Recurring themes or concerns
       - Things that might inform future suggestions

       Anything specific you'd like me to pay attention to?
```

### What Users Cannot See

- Raw composting algorithms
- Individual object decomposition details
- Pre-processed session data

**Rationale**: These are implementation details that would be confusing and create false precision. Users see outcomes (insights), not process.

---

## Anti-Patterns: What NOT to Do

### 1. Real-Time Notification of Learning

**Wrong**:
```
PIPER: [3:42 PM] I just learned that you prefer bullet points!
PIPER: [3:45 PM] Pattern detected: afternoon email checking
PIPER: [3:51 PM] New insight: meeting fatigue threshold identified
```

**Why wrong**: Feels like surveillance. Learning should be invisible until reflection.

### 2. Surveillance Language

**Wrong**:
```
PIPER: While monitoring your activities this week, I observed...
```

**Why wrong**: "Monitoring" and "observed" imply active surveillance.

### 3. Over-Detailed Attribution

**Wrong**:
```
PIPER: Based on your behavior at 2:15 PM on Tuesday, when you closed
       the browser tab after 3.2 seconds of viewing the report...
```

**Why wrong**: Too specific. Creates discomfort. Reflection should be general.

### 4. Unexplained Behavioral Changes

**Wrong**:
[Piper suddenly starts behaving differently based on learning, without ever surfacing that it learned something]

**Why wrong**: Feels like manipulation. Even if not announced, changes should be explainable on request.

### 5. Guilt-Inducing Reflection

**Wrong**:
```
PIPER: I noticed you didn't follow through on 12 commitments this month.
       Your completion rate has dropped 23% since Q1.
```

**Why wrong**: Reflection should help, not judge. Frame constructively or not at all.

---

## Configuration Options

### What Users Can Configure

| Setting | Options | Default |
|---------|---------|---------|
| Quiet hours | Time range | 2-5 AM local |
| Reflection frequency | Daily/Weekly/Biweekly/Never | Weekly (Stage 3+) |
| Reflection delivery | Morning standup/Dedicated message/Never | Standup |
| Manual composting | Enabled/Disabled | Enabled |

### What Users Cannot Configure

- Whether composting happens at all (it's core to learning)
- Composting algorithms
- What gets composted

**Rationale**: Composting is how Piper learns. Disabling it disables learning. Instead, users control visibility (D1) and can delete results (D2).

---

## Success Metrics

This specification succeeds if:

- [ ] Users describe composting as "reflection" not "monitoring"
- [ ] Reflection summaries feel natural, not robotic
- [ ] Users don't feel interrupted by learning notifications
- [ ] Users report insights feel "earned" not "creepy"
- [ ] Morning standup integration feels seamless

---

## Related Specifications

- **D1**: Learning Visibility (how reflections appear)
- **D4**: Insight Journal Surfacing Rules (when reflections push/pull)
- **D6**: Journal Architecture (where composting outputs go)

---

*Specification: D3 Composting Experience Design*
*Issue: #431 MUX-VISION-LEARN*
*Created: 2026-01-22*
