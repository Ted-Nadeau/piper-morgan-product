# D2: Control Interface Patterns

**Issue**: #431 MUX-VISION-LEARN
**Deliverable**: 2 of 7
**Question Addressed**: How do users correct, delete, inspect, and reset learnings?

---

## Core Principle

**Forthright, transparent, correctable.**

Users must feel in control of what Piper learns about them. Control mechanisms must be discoverable, easy to use, and immediate in effect.

---

## Four Control Capabilities

| Capability | User Intent | Piper Response |
|------------|-------------|----------------|
| **Correction** | "You're wrong about X" | Update learning, acknowledge correction |
| **Deletion** | "Forget X" | Remove learning completely |
| **Inspection** | "What do you know about X?" | Show relevant learnings transparently |
| **Reset** | "Forget everything" | Clear all learnings with confirmation |

---

## 1. Correction Flow

### Trigger Phrases

Natural language triggers (all equivalent):
- "You seem to think I prefer X, but actually Y"
- "That's not quite right—I actually..."
- "Let me correct something..."
- "You've got the wrong idea about..."

### Correction Process

```
USER: "You seem to think I prefer morning meetings, but I actually prefer afternoons"

PIPER: "Thanks for the correction. I'll update my understanding:

Before: Morning meetings preferred (confidence: 0.78)
After: Afternoon meetings preferred (confidence: 0.95)

I've noted that you told me this directly, which is why the confidence is high.
Is there anything else about meeting preferences I should know?"
```

### Design Details

**Immediate Effect**: Correction takes effect instantly for future behavior.

**Transparency**: Show before/after when possible. User should see the change.

**Confidence Boost**: Direct corrections get high confidence (0.9+) because user stated explicitly.

**Source Tracking**: Record that this learning came from direct user input, not inference.

**No Argument**: Piper never argues with corrections. User's statement is authoritative.

### Correction from Context

User may implicitly correct through behavior:

```
[Piper suggests morning meeting]
USER: [Declines, schedules afternoon instead]

PIPER: (internal) Reduce confidence in morning preference
PIPER: (if pattern repeats) "I notice you've been choosing afternoon slots—
       should I update my understanding about your meeting preferences?"
```

**Principle**: Seek confirmation before overwriting explicit learning with inferred learning.

---

## 2. Deletion Flow

### Trigger Phrases

- "Forget what you learned about Z"
- "Delete that insight"
- "I don't want you to remember that"
- "Remove [specific learning]"

### Deletion Process

```
USER: "Forget what you learned about my communication style with the design team"

PIPER: "I'll forget what I've learned about your communication style with the
design team. This includes:

- Preference for async communication (derived from 12 interactions)
- Tendency to be more detailed in design feedback (derived from 8 reviews)

This deletion is permanent—I can't undo it.
Should I proceed?"

USER: "Yes"

PIPER: "Done. I've removed those learnings. I'll start fresh on that topic."
```

### Design Details

**Confirmation Required**: Always confirm before deleting, showing what will be removed.

**Permanent**: Deleted learnings are truly gone, not hidden.

**Scope Clarity**: Be specific about what's included in the deletion.

**No Guilt**: Don't make user feel bad for deleting. Neutral acknowledgment only.

**Fresh Start**: Explicitly state Piper will start fresh (not secretly retain).

### Bulk Deletion

User can delete by category:
- "Forget everything about [project]"
- "Delete all learnings from before [date]"
- "Remove all low-confidence insights"

Each triggers confirmation with scope summary.

---

## 3. Inspection Flow

### Trigger Phrases

- "What have you learned about [topic]?"
- "Show me your insights about..."
- "What do you think you know about me?"
- "What patterns have you noticed?"

### Inspection Process

```
USER: "What have you learned about how I work?"

PIPER: "Here's what I've noticed about how you work:

**Work Patterns** (high confidence)
- You prefer to tackle difficult tasks in the morning
- You often batch similar tasks together

**Communication Style** (medium confidence)
- You tend to be more direct in written communication
- You prefer bullet points over paragraphs

**Scheduling** (medium confidence)
- You protect Wednesday afternoons
- Back-to-back meetings seem to drain you

Would you like me to explain where any of these came from,
or correct anything that's off?"
```

### Design Details

**Organized Display**: Group by topic, indicate confidence.

**Complete Honesty**: Show everything relevant, including uncertain inferences.

**Invitation to Correct**: Always end with offer to correct or explain.

**Drill-Down Available**: User can ask "why do you think [specific insight]?"

### Inspection Scope

| Query | Scope |
|-------|-------|
| "What do you know about me?" | All learnings |
| "What have you learned about [topic]?" | Topic-filtered |
| "What did you learn from [project]?" | Source-filtered |
| "What are you uncertain about?" | Low-confidence only |

---

## 4. Reset Flow

### Trigger Phrases

- "Forget everything you've learned about me"
- "Reset your learnings"
- "Start fresh"
- "Delete all insights"

### Reset Process

```
USER: "Forget everything you've learned about me"

PIPER: "This is a significant action. Let me make sure you understand
what it means:

**What will be deleted:**
- All learned preferences (47 insights)
- All pattern observations (23 patterns)
- All communication style learnings
- All project-specific insights

**What will NOT be deleted:**
- Our conversation history (Session Journal)
- Your account settings
- Your trust level with me

**What this means going forward:**
- I'll need to relearn your preferences
- Suggestions will be generic until I observe new patterns
- Proactive help will be less personalized

This cannot be undone.

Type 'RESET' to confirm, or tell me if you'd prefer a partial reset."

USER: "RESET"

PIPER: "Done. All learnings have been cleared. We're starting fresh.

If you're comfortable sharing—was there something that made you want
to reset? I'd like to do better going forward."
```

### Design Details

**Significant Confirmation**: Require explicit confirmation word, not just "yes."

**Full Transparency**: List exactly what will and won't be deleted.

**Consequences Stated**: User must understand the practical impact.

**Partial Alternative**: Offer partial reset if full reset seems drastic.

**Optional Feedback**: Gently ask why (but accept silence). Reset may indicate broken trust.

### Partial Reset Options

- "Reset learnings about [category]"
- "Reset learnings older than [time period]"
- "Reset low-confidence learnings only"

Each has its own confirmation flow with appropriate scope.

---

## Discoverability Requirements

### Users Must Be Able to Find Controls Without Instructions

**Discoverability Paths**:

1. **Natural Language**: Any reasonable phrasing should work
   - "How do I correct something you learned?"
   - "Can I delete insights?"
   - "I want to see what you know"

2. **UI Elements**: In Insight Journal
   - Each insight has "Correct" and "Delete" actions
   - Global "Reset" option visible but not prominent
   - "Explain this" link on every insight

3. **Help/Settings**: Learning controls section
   - Overview of all control capabilities
   - Links to each action
   - Privacy policy explanation

### First-Time Education

When user first accesses Insight Journal:

> "This is where you can see what I've learned from our work together.
> You're always in control:
> - **Correct** anything I got wrong
> - **Delete** anything you'd rather I forget
> - **Ask** me to explain any insight
>
> Your corrections and deletions take effect immediately."

---

## Response Patterns

### Acknowledging Corrections

- "Thanks for the correction. I've updated my understanding."
- "Got it—I'll remember that going forward."
- "Noted. That helps me serve you better."

**Never**:
- "Are you sure? My data shows..."
- "That contradicts what I observed..."
- "I'll make a note but keep my original insight..."

### Acknowledging Deletions

- "Done. I've forgotten that."
- "Removed. I'll start fresh on that topic."
- "Deleted. That information is gone."

**Optional gentle path forward** (once, after deletion):
> "Done. I've forgotten that. If you ever want to help me learn something different about this topic, just let me know."

This acknowledges the deletion, doesn't guilt, and leaves the door open—all without being clingy.

**Never**:
- "Are you sure you want me to forget?"
- "That was a useful insight though..."
- "I'll delete it but keep a backup..."

### Handling Ambiguous Requests

```
USER: "Delete that thing you said about meetings"

PIPER: "I want to make sure I delete the right thing. Do you mean:

1. My observation that you prefer morning meetings
2. My note about back-to-back meeting fatigue
3. Something else about meetings

Which should I remove?"
```

---

## Privacy & Security

### Deletion Is Real

- Deleted learnings are removed from all storage
- No "soft delete" or hidden archive
- Cannot be recovered by Piper or administrators

### Audit Trail Exception

- Session Journal records that a deletion happened (for compliance)
- But does NOT record what was deleted
- Format: "User requested deletion of learning [ID] on [date]"

### No Sharing

- Learnings are never shared across users
- Deletion affects only the requesting user's data
- No aggregate learning that could leak individual data

---

## Edge Cases

### Conflicting Corrections

User corrects something, then corrects again differently:

```
USER: "I prefer morning meetings"
[Later]
USER: "Actually I prefer afternoon meetings"

PIPER: "Got it. I'll update from morning preference to afternoon preference.
Just to confirm—this replaces my previous understanding, right?"
```

### Correction That Matches Original

```
USER: "I actually do prefer morning meetings"

PIPER: "That's what I had noted—glad to confirm it's correct!
Confidence updated from 0.72 to 0.95."
```

### Deleting What Doesn't Exist

```
USER: "Forget what you learned about my travel preferences"

PIPER: "I don't actually have any learnings about your travel preferences yet.
Is there something specific you were concerned about?"
```

---

## Success Metrics

This specification succeeds if:

- [ ] Users can correct learnings in under 30 seconds
- [ ] Users can find deletion controls without help
- [ ] Reset flow prevents accidental complete deletion
- [ ] Users report feeling "in control" of Piper's learning
- [ ] No user reports feeling "unable to fix" a wrong insight

---

## Related Specifications

- **D1**: Learning Visibility (what users see before controlling)
- **D5**: Provenance Display (explaining learning sources)
- **D6**: Journal Architecture (where controlled data lives)

---

---

## CXO Review Notes (2026-01-23)

**Status**: ✅ Approved

### Key Affirmation

> "Control Without Guilt" - Critical. The anti-pattern here is dark-patterning user data control. If a user wants to delete, they've decided. Piper honors that without friction or guilt.

### Refinements Applied

1. **Post-deletion gentle path forward** (added above) - Optional, once, not clingy.

### Future Enhancements (not required for v1)

**A. Learning acknowledgment moments**: When Piper learns something significant, occasional subtle acknowledgment:
- "That's helpful to know"
- "I'll remember that"

This makes the learning relationship visible without being mechanical.

**B. Learning correction feedback loop**: When a user corrects Piper, acknowledge the correction's impact:
- "Got it — I'll approach this differently next time"

This closes the loop and builds confidence that corrections matter.

---

*Specification: D2 Control Interface Patterns*
*Issue: #431 MUX-VISION-LEARN*
*Created: 2026-01-22*
*CXO Review: 2026-01-23 (Approved)*
