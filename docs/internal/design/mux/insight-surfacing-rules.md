# D4: Insight Journal Surfacing Rules

**Issue**: #431 MUX-VISION-LEARN
**Deliverable**: 4 of 7
**Question Addressed**: When does Piper push, pull, or passively display insights?

---

## Core Principle

**All three modes, context-dependent.**

Insights can be pulled (user asks), passively browsed (user navigates), or pushed (Piper surfaces). The mode depends on trust level, confidence, relevance, and timing.

---

## Three Surfacing Modes

| Mode | User Action | Piper Behavior | Trust Requirement |
|------|-------------|----------------|-------------------|
| **Pull** | Explicit query | Respond with relevant insights | All levels |
| **Passive** | Navigate to journal | Display organized insights | All levels |
| **Push** | None (Piper initiates) | Surface contextually relevant insight | Stage 3+ |

---

## Pull Mode

### Definition

User explicitly requests insight information. Piper responds directly.

### Trigger Phrases

Any natural inquiry about learnings:

| Phrase Category | Examples |
|-----------------|----------|
| Direct query | "What have you learned?" |
| Topic-specific | "What do you know about my calendar habits?" |
| Explanation request | "Why did you suggest that?" |
| Confidence check | "How sure are you about that?" |
| Source inquiry | "Where did that insight come from?" |

### Response Format

```
USER: What have you learned about how I handle deadlines?

PIPER: Here's what I've noticed about your deadline patterns:

**High confidence:**
- You work best with 20% buffer built into timelines
- External deadlines get prioritized over internal ones

**Medium confidence:**
- You tend to front-load effort rather than spread it evenly
- Last-minute work is usually higher quality than rushed early work

**Something I'm less sure about:**
- It seems like you prefer to deliver early on smaller tasks
  but use all available time on larger ones

Would you like me to explain any of these, or correct something that's off?
```

### Pull Mode Rules

| Rule | Requirement |
|------|-------------|
| Response completeness | Show all relevant insights (don't hide low-confidence) |
| Confidence display | Always indicate confidence level |
| Correction invitation | Always offer to correct/explain |
| Scope matching | Match response scope to query scope |
| No deflection | Never say "I don't have insights" if any exist |

---

## Passive Mode

### Definition

Insights are available for browsing in Piper's dedicated space. User chooses to look.

### Access Points

1. **Navigation**: Menu item "What Piper's Learned" or "Insight Journal"
2. **Command**: "Open insights" / "Show journal" / "Show learnings"
3. **Shortcut**: Configurable keyboard shortcut
4. **Link**: From any insight reference in conversation

### Organization Structure

```
Insight Journal
│
├── Recent Reflections (last composting cycle)
│   ├── 3 new insights from this week
│   └── [View all recent]
│
├── Work Patterns
│   ├── Productivity (5 insights)
│   ├── Communication (3 insights)
│   └── Scheduling (7 insights)
│
├── Projects
│   ├── Henderson Proposal (4 insights)
│   ├── Q1 Planning (2 insights)
│   └── [Archived projects...]
│
├── People & Teams
│   ├── Working with Design (2 insights)
│   └── Cross-team collaboration (1 insight)
│
└── Preferences
    ├── Meeting preferences (3 insights)
    ├── Communication style (2 insights)
    └── Tool preferences (1 insight)
```

### Passive Mode Presentation

| Element | Display |
|---------|---------|
| Insight title | Brief, scannable summary |
| Confidence | Visual indicator (high/medium/low) |
| Recency | "Noticed 3 days ago" |
| Source hint | "From project work" / "From scheduling patterns" |
| Actions | [Explain] [Correct] [Delete] |

### Passive Mode Rules

| Rule | Requirement |
|------|-------------|
| No attention-grabbing | No badges, no "new" indicators that persist |
| Organized by topic | Primary organization is topical, not chronological |
| Recency secondary | Within topics, recent insights surface first |
| Low confidence visible | Show all insights, mark confidence clearly |
| Delete accessible | Every insight has visible delete option |

---

## Push Mode

### Definition

Piper proactively surfaces an insight without user request. Most constrained mode.

### Prerequisites (ALL must be met)

| Criterion | Threshold |
|-----------|-----------|
| Trust level | Stage 3 or higher |
| Insight confidence | 0.75 or higher |
| Relevance to current context | High |
| Time since last push | 24+ hours |
| User availability | Not in focus/DND mode |

### Context Relevance Assessment

Push only when insight is directly relevant to what user is doing now:

| Context | Relevant Insight Example |
|---------|-------------------------|
| Scheduling meeting | "You tend to prefer morning slots for deep discussions" |
| Starting project | "Similar projects benefited from early stakeholder alignment" |
| Writing document | "Your best-received docs use bullet points over paragraphs" |
| Approaching deadline | "You work best with buffer time—want me to flag this?" |

### Push Language

**Appropriate openers**:
- "Can I share something that might be relevant?"
- "This might help here..."
- "I've noticed something that could apply..."
- "A thought that occurred to me..."

**Inappropriate openers**:
- "ALERT: Pattern detected"
- "Based on my analysis..."
- "I've been watching and noticed..."
- "Data suggests..."

### Push Format

```
PIPER: Can I share something that might help?

       Looking back at similar proposals, the ones that landed best
       had stakeholder buy-in before the detailed work started.

       Worth a quick alignment check before diving into the details?

       [Yes, thanks] [Not now] [Tell me more]
```

### Push Mode Rules

| Rule | Requirement |
|------|-------------|
| Interruptibility | Must be dismissable with single action |
| Explanation available | "Tell me more" always offered |
| No repeated pushes | Same insight not pushed twice |
| No urgency language | Never "urgent" or "important" |
| Graceful decline | "Not now" is fine, no follow-up guilt |

---

## Mode Selection Logic

```
INSIGHT SURFACES
       │
       ├─── User explicitly asked? ────────────────────► PULL MODE
       │                                                  (respond directly)
       │
       ├─── User navigated to journal? ────────────────► PASSIVE MODE
       │                                                  (display in context)
       │
       └─── Piper wants to share proactively?
                    │
                    ├─── Trust < Stage 3? ─────────────► NO PUSH
                    │                                     (wait for pull)
                    │
                    ├─── Confidence < 0.75? ───────────► NO PUSH
                    │                                     (add to journal only)
                    │
                    ├─── Not contextually relevant? ───► NO PUSH
                    │                                     (add to journal only)
                    │
                    ├─── Last push < 24h ago? ─────────► NO PUSH
                    │                                     (add to journal only)
                    │
                    ├─── User in focus mode? ──────────► NO PUSH
                    │                                     (queue for later)
                    │
                    └─── All criteria met? ────────────► PUSH MODE
                                                          (surface gently)
```

---

## Trust-Based Surfacing Matrix

| Stage | Pull | Passive | Push |
|-------|------|---------|------|
| **Stage 1 (New)** | Yes | Yes | No |
| **Stage 2 (Building)** | Yes | Yes | No |
| **Stage 3 (Established)** | Yes | Yes | Yes (batched) |
| **Stage 4 (Trusted)** | Yes | Yes | Yes (contextual) |

### Stage 3 vs Stage 4 Push Differences

| Aspect | Stage 3 | Stage 4 |
|--------|---------|---------|
| Timing | Batched (morning/weekly) | Contextual (in-moment) |
| Frequency | Lower | Higher (if relevant) |
| Confidence threshold | 0.80 | 0.75 |
| Interruption style | Digest format | Inline suggestion |

---

## Special Surfacing Cases

### Contradiction Discovery

When new learning contradicts existing insight:

**Push regardless of timing** (with Stage 3+ still required):
```
PIPER: Quick heads up—I think I had something wrong.

       I thought you preferred async communication with the design team,
       but looking at recent interactions, you've been opting for calls.

       Should I update my understanding?
```

### High-Stakes Context

When user is in high-stakes situation (big presentation, important deadline):

**More conservative pushing**:
- Raise confidence threshold to 0.90
- Only push if directly actionable
- Prefer "I'll note this for later" over interruption

### New User Orientation

First week of use:

**Pull and passive only**:
- Explain what's available: "I'll learn from our work together. You can always ask what I've noticed."
- No pushing until trust established
- Invitation to browse: "Want to see what I've picked up so far?"

---

## Feedback Loop

### Learning from Surfacing Response

| User Response | Piper Learning |
|---------------|----------------|
| Engages with pushed insight | Increase surfacing confidence |
| Dismisses with "not now" | Neutral (timing issue) |
| Dismisses with "not relevant" | Decrease relevance scoring |
| Corrects insight | Update insight, note correction source |
| Deletes insight | Remove completely, don't resurface |

### Surfacing Calibration

Over time, Piper calibrates:
- Which topics user engages with
- Which contexts are welcome for pushes
- Which times/situations to avoid
- Which formats resonate

---

## Configuration Options

### User-Configurable

| Setting | Options | Default |
|---------|---------|---------|
| Push mode enabled | Yes/No | Yes (Stage 3+) |
| Push frequency limit | Unlimited/Daily/Weekly | Daily |
| Quiet hours | Time range for no pushes | Match system DND |
| Topics to push | All/Selected/None | All |

### Not User-Configurable

- Pull mode availability (always on)
- Passive mode availability (always on)
- Confidence thresholds (system-determined)

---

## Error Handling

### No Relevant Insights

```
USER: What have you learned about my vacation preferences?

PIPER: I don't have any insights about vacation preferences yet.
       This might be because we haven't worked on travel-related tasks,
       or because patterns haven't emerged yet.

       Want to tell me about your preferences, or should I keep an eye
       out as we work together?
```

### Insight Becomes Stale

When insight is old and may no longer apply:

```
PIPER: I have an insight from 6 months ago about your meeting preferences.
       It may be outdated—want me to check if it still holds, or should
       I retire it?
```

### Context Mismatch

When push context doesn't quite fit:

```
[Piper was about to push meeting insight, but user switches tasks]

PIPER: [Holds push, queues for next relevant context]
```

---

## Success Metrics

This specification succeeds if:

- [ ] Pull mode responds to all reasonable phrasings
- [ ] Passive mode is discoverable without instructions
- [ ] Push mode feels helpful, not intrusive
- [ ] Stage 1-2 users never experience unwanted pushes
- [ ] Stage 3+ users find contextual suggestions valuable
- [ ] Dismiss rate for pushes stays below 30%

---

## Related Specifications

- **D1**: Learning Visibility (overall visibility framework)
- **D3**: Composting Experience (where insights originate)
- **D5**: Provenance Display (explaining insight sources)
- **D7**: Trust-Based Access (trust stage definitions)

---

*Specification: D4 Insight Journal Surfacing Rules*
*Issue: #431 MUX-VISION-LEARN*
*Created: 2026-01-22*
