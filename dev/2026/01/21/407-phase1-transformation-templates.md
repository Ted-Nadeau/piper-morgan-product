# Phase 1: Transformation Templates

**Issue**: #407 MUX-VISION-STANDUP-EXTRACT
**Date**: January 21, 2026
**Purpose**: Concrete templates for transforming report output to conscious narrative

---

## Template Structure

Each template has:
- **Variables**: Placeholders for data
- **Variants**: Alternative phrasings for variety
- **Constraints**: When to use/avoid

---

## Opening Templates

### Template: Temporal Greeting

```python
TEMPORAL_GREETINGS = {
    "morning": [
        "Good morning! I've been looking through your work context...",
        "Morning! Let me share what I found looking at your day...",
        "Good morning! Here's what I see as we start the day...",
    ],
    "late_morning": [
        "Starting a bit later? No worries - let me catch you up...",
        "Good morning! Here's what I found looking through your context...",
    ],
    "afternoon": [
        "Afternoon check-in! Here's where things stand...",
        "Quick afternoon summary - here's what I see...",
    ],
    "evening": [
        "End of day? Let's look at what you accomplished...",
        "Wrapping up? Here's how the day went from what I can see...",
    ],
}
```

### Template: Context Acknowledgment

```python
CONTEXT_ACKNOWLEDGMENTS = {
    "in_meeting": [
        "I see you're in a meeting - I'll keep this brief...",
        "Looks like you're busy right now. Quick summary...",
    ],
    "heavy_meeting_day": [
        "You've got a packed day ahead - {meeting_hours} hours of meetings. Here's what matters most...",
        "Heavy meeting day! Let me highlight what's most important given your {meeting_count} meetings...",
    ],
    "focus_time": [
        "You've got some focus time coming up - let me help you make the most of it...",
        "I see a {duration}-minute focus block ahead. Here's what might be worth tackling...",
    ],
    "general": [
        "Here's what I found looking through your context...",
        "Let me share what I see for today...",
    ],
}
```

---

## Navigation Templates

### Template: Spatial Journey

```python
SPATIAL_JOURNEY_TEMPLATES = {
    "single_source": [
        "I checked {source}...",
        "Looking at {source}...",
    ],
    "two_sources": [
        "I started by checking {source1}, then looked at {source2}...",
        "I checked {source1} first, and also looked through {source2}...",
    ],
    "three_plus_sources": [
        "I've been looking through {sources_list}, and {final_source}...",
        "I checked {sources_list}. Also pulled up {final_source}...",
    ],
}

# Source name mappings for natural language
SOURCE_NAMES = {
    "github": "GitHub",
    "calendar": "your calendar",
    "documents": "some relevant documents",
    "session": "your recent session context",
    "issues": "your open issues",
}
```

### Template: Source Attribution

```python
SOURCE_ATTRIBUTION_TEMPLATES = {
    "github": [
        "In GitHub, I see {finding}...",
        "Your GitHub activity shows {finding}...",
        "Looking at GitHub, {finding}...",
    ],
    "calendar": [
        "Your calendar shows {finding}...",
        "Looking at your schedule, {finding}...",
    ],
    "inference": [
        "Based on what I'm seeing, {finding}...",
        "Putting this together, it looks like {finding}...",
    ],
}
```

---

## Discovery Templates

### Template: Accomplishment Recognition

```python
ACCOMPLISHMENT_TEMPLATES = {
    "single_major": [
        "Nice work on {accomplishment}! That looked like a big one.",
        "I see you finished {accomplishment} - great progress!",
        "You completed {accomplishment} - that's been on the list a while!",
    ],
    "single_minor": [
        "You worked on {accomplishment}...",
        "I see {accomplishment} got done...",
    ],
    "multiple": [
        "Looks like you made good progress - {main}, plus {count} other {items}.",
        "Productive day! You finished {main}, along with {count} other {items}.",
        "Nice momentum - {main} done, and {count} more {items} checked off.",
    ],
    "none": [
        "I didn't find much recorded activity yesterday. You might have been in meetings or doing work I can't see. What were you focused on?",
        "Quiet day on the tools I can see - probably means heads-down work or meetings. What were you working on?",
    ],
}
```

### Template: Priority Framing

```python
PRIORITY_TEMPLATES = {
    "single_clear": [
        "The main thing today looks like {priority}...",
        "I'd focus on {priority} - it seems like the critical path.",
        "Today's priority looks like {priority}...",
    ],
    "multiple_ranked": [
        "A few things competing for attention today. I'd suggest: {priority1} first, then {priority2}.",
        "You've got {priority1} and {priority2} on deck. {priority1} seems more urgent.",
    ],
    "multiple_equal": [
        "You've got {count} priorities today: {priorities}. Which feels most important to you?",
        "Several things to tackle: {priorities}. What's your instinct on where to start?",
    ],
    "with_calendar_context": [
        "Given your {meeting_count} meetings, maybe focus on {priority} during your {focus_duration} focus block?",
        "With {meeting_hours} hours of meetings, your best window for {priority} is probably {time_slot}.",
    ],
}
```

---

## Concern Templates

### Template: Gentle Flagging

```python
GENTLE_FLAGGING_TEMPLATES = {
    "blocker": [
        "One thing I wanted to flag - {blocker}. This might need attention.",
        "I noticed {blocker} - something to keep an eye on.",
        "There's one thing I'm watching: {blocker}.",
    ],
    "potential_issue": [
        "I'm not sure if this is a problem, but {concern}...",
        "This might be nothing, but I noticed {concern}...",
        "I could be wrong about this, but it looks like {concern}...",
    ],
    "workload": [
        "You've got a lot on your plate today - {count} items. Let me know if you want help prioritizing.",
        "That's a full agenda. If something needs to slip, what would it be?",
    ],
}
```

### Template: Missing Data Explanation

```python
MISSING_DATA_TEMPLATES = {
    "no_github": [
        "I didn't see much GitHub activity yesterday - you might have been in meetings or doing work I can't see. What were you focused on?",
        "Quiet day on GitHub. That usually means meetings or deep work elsewhere. What's the context?",
    ],
    "no_calendar": [
        "Your calendar looks open today. That could mean focus time, or maybe meetings aren't synced?",
        "I don't see any calendar events. Is your calendar connected, or is today really that open?",
    ],
    "no_context": [
        "I don't have much context from yesterday. Want to fill me in so I can track it going forward?",
        "Starting fresh today - I don't have history from yesterday. What should I know?",
    ],
}
```

---

## Closing Templates

### Template: Summary Synthesis

```python
SUMMARY_TEMPLATES = {
    "positive": [
        "Overall, good momentum from yesterday carrying into today.",
        "Looks like a productive day ahead with clear priorities.",
        "Nice progress yesterday, and today's plan looks solid.",
    ],
    "neutral": [
        "That's the picture from what I can see.",
        "Here's where things stand heading into today.",
    ],
    "cautious": [
        "It's a busy day, but manageable if you protect your focus time.",
        "A lot on the plate today - staying focused on {main_priority} will be key.",
    ],
    "with_concern": [
        "Good direction overall, though {concern} is worth watching.",
        "Solid plan, with one thing to keep an eye on: {concern}.",
    ],
}
```

### Template: Dialogue Invitation

```python
DIALOGUE_INVITATION_TEMPLATES = [
    "How does that sound? Anything you'd like me to adjust?",
    "Does this capture your priorities? Let me know what to change.",
    "What do you think? I can update this if something's off.",
    "Anything I missed or got wrong?",
    "Let me know if you want to adjust anything.",
]
```

---

## Complete Transformation Example

### Input (StandupResult)

```python
result = StandupResult(
    user_id="xian",
    yesterday_accomplishments=[
        "✅ Completed MUX-GATE-2 verification",
        "📋 Updated pattern documentation",
    ],
    today_priorities=[
        "🎯 Continue V2 sprint work",
        "🎯 Review issue #407",
    ],
    blockers=[],
    github_activity={"commits": 5, "prs": 1},
    context_source="persistent",
    time_saved_minutes=15,
)
```

### Template Selection

```python
context = ConsciousnessContext(
    time_of_day="morning",
    is_first_interaction_today=True,
    has_accomplishments=True,
    has_github_activity=True,
    data_sources_count=2,
)

templates_used = [
    TEMPORAL_GREETINGS["morning"][0],
    SPATIAL_JOURNEY_TEMPLATES["two_sources"],
    ACCOMPLISHMENT_TEMPLATES["multiple"],
    PRIORITY_TEMPLATES["multiple_ranked"],
    SUMMARY_TEMPLATES["positive"],
    DIALOGUE_INVITATION_TEMPLATES[0],
]
```

### Output (Conscious Narrative)

```
Good morning! I've been looking through your work context...

I started by checking GitHub, then looked at your session context.
Looks like you made good progress - completed MUX-GATE-2 verification,
plus 1 other item (pattern docs update).

A few things competing for attention today. I'd suggest: V2 sprint work
first, then reviewing issue #407. Both are substantial but the sprint
work seems more time-sensitive.

Overall, good momentum from yesterday carrying into today.

How does that sound? Anything you'd like me to adjust?
```

---

## Template Selection Logic

```python
def select_template(category: str, context: ConsciousnessContext, data: Dict) -> str:
    """Select appropriate template based on context and data."""

    if category == "accomplishment":
        if not data.get("accomplishments"):
            return random.choice(ACCOMPLISHMENT_TEMPLATES["none"])
        elif len(data["accomplishments"]) == 1:
            return random.choice(ACCOMPLISHMENT_TEMPLATES["single_major"])
        else:
            return random.choice(ACCOMPLISHMENT_TEMPLATES["multiple"])

    elif category == "priority":
        priorities = data.get("priorities", [])
        if len(priorities) == 1:
            return random.choice(PRIORITY_TEMPLATES["single_clear"])
        elif context.meeting_load == "heavy":
            return random.choice(PRIORITY_TEMPLATES["with_calendar_context"])
        else:
            return random.choice(PRIORITY_TEMPLATES["multiple_ranked"])

    # ... etc for other categories
```

---

## Anti-Pattern Templates (What NOT to Generate)

```python
# These patterns should NEVER appear in output

ANTI_PATTERNS = [
    # Report headers instead of greetings
    "*Morning Standup for {user}*",
    "Standup Report - {date}",

    # Bullet lists without narrative
    "• {item}\n• {item}\n• {item}",

    # Metrics as closing
    "_Generated in {time}s_",
    "Time saved: {minutes}m",

    # Judgmental language
    "No accomplishments recorded",
    "No activity detected",

    # Missing attribution
    "You have 5 commits",  # vs "I see in GitHub you have 5 commits"

    # No invitation
    # (any output that ends without question or invitation)
]
```

---

## Next Steps

1. **Implement template engine** in `services/consciousness/templates.py`
2. **Create MVC documentation** (formal spec)
3. **Build format replacement functions**
4. **Add unit tests for template selection**

---

*Phase 1 Transformation Templates Complete*
*Ready for MVC documentation and implementation*
