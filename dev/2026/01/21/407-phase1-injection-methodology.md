# Phase 1: Consciousness Injection Methodology

**Issue**: #407 MUX-VISION-STANDUP-EXTRACT
**Date**: January 21, 2026
**Purpose**: Define how to transform data-driven output into conscious expression

---

## Core Principle

> "The value is in synthesis, not just data display" - PM Interview

Consciousness injection is not about adding words - it's about **transforming how information is presented** from report format to conversational synthesis.

---

## The Injection Pipeline

```
Raw Data (StandupResult)
    ↓
┌─────────────────────────────────┐
│  1. CONTEXT ANALYSIS            │
│  - Time of day                  │
│  - User situation               │
│  - Data richness                │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│  2. PATTERN SELECTION           │
│  - Choose appropriate patterns  │
│  - Based on context + data      │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│  3. NARRATIVE CONSTRUCTION      │
│  - Apply patterns to data       │
│  - Build arc: Open→Journey→     │
│    Discover→Concern→Close       │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│  4. MVC VALIDATION              │
│  - Has "I" statement?           │
│  - Has uncertainty?             │
│  - Has invitation?              │
│  - Has attribution?             │
└─────────────────────────────────┘
    ↓
Conscious Output
```

---

## Step 1: Context Analysis

Before selecting patterns, analyze the context:

```python
@dataclass
class ConsciousnessContext:
    """Context for consciousness injection decisions."""

    # Temporal
    time_of_day: str  # "morning", "late_morning", "afternoon", "evening"
    is_first_interaction_today: bool

    # Situational
    user_in_meeting: bool
    has_focus_time: bool
    meeting_load: str  # "light", "moderate", "heavy"

    # Data richness
    has_accomplishments: bool
    has_github_activity: bool
    has_calendar_data: bool
    has_blockers: bool
    data_sources_count: int

    # Derived
    @property
    def richness_level(self) -> str:
        if self.data_sources_count >= 3:
            return "rich"
        elif self.data_sources_count >= 1:
            return "moderate"
        return "sparse"
```

### Context → Pattern Mapping

| Context | Recommended Patterns |
|---------|---------------------|
| Morning + Rich data | Full ritual arc with spatial journey |
| Morning + Sparse data | Gentle greeting + missing data explanation |
| Afternoon | Shortened arc, skip temporal greeting |
| Heavy meeting day | Lead with calendar concern |
| No accomplishments | Missing data explanation (non-judgmental) |
| User in meeting | Brief mode, acknowledge context |

---

## Step 2: Pattern Selection

Based on context, select which patterns to apply:

```python
def select_patterns(context: ConsciousnessContext) -> List[Pattern]:
    """Select appropriate patterns based on context."""

    patterns = []

    # Opening - always include one
    if context.time_of_day == "morning" and context.is_first_interaction_today:
        patterns.append(TemporalGreeting())
    elif context.user_in_meeting:
        patterns.append(ContextAcknowledgment(situation="meeting"))
    else:
        patterns.append(ContextAcknowledgment(situation="general"))

    # Navigation - only if multiple sources
    if context.data_sources_count > 1:
        patterns.append(SpatialJourney())

    # Discovery - based on data presence
    if context.has_accomplishments:
        patterns.append(AccomplishmentRecognition())
    patterns.append(PriorityFraming())  # Always include

    # Concern - based on blockers or data gaps
    if context.has_blockers:
        patterns.append(GentleFlagging())
    if not context.has_accomplishments:
        patterns.append(MissingDataExplanation())

    # Closing - always include
    patterns.append(SummarySynthesis())
    patterns.append(DialogueInvitation())

    return patterns
```

---

## Step 3: Narrative Construction

Apply selected patterns to build the narrative arc:

### The Five-Part Arc

```
1. OPENING (1-2 sentences)
   Pattern: TemporalGreeting or ContextAcknowledgment
   Purpose: Establish presence, acknowledge moment

2. JOURNEY (1-2 sentences, optional)
   Pattern: SpatialJourney
   Purpose: Show Piper exploring on user's behalf

3. DISCOVERY (2-4 sentences)
   Patterns: AccomplishmentRecognition, PriorityFraming
   Purpose: Present findings with voice

4. CONCERN (1-2 sentences, if applicable)
   Patterns: GentleFlagging, MissingDataExplanation
   Purpose: Raise issues gently with uncertainty

5. CLOSING (1-2 sentences)
   Patterns: SummarySynthesis, DialogueInvitation
   Purpose: Tie together, invite response
```

### Construction Example

**Input Data**:
```python
StandupResult(
    user_id="xian",
    yesterday_accomplishments=["Completed MUX-GATE-2", "Updated docs"],
    today_priorities=["Continue V2 sprint", "Review #407"],
    blockers=[],
    github_activity={"commits": 5, "prs": 1},
    time_saved_minutes=15
)
```

**Context Analysis**:
```python
ConsciousnessContext(
    time_of_day="morning",
    is_first_interaction_today=True,
    has_accomplishments=True,
    has_github_activity=True,
    data_sources_count=2,
    richness_level="moderate"
)
```

**Selected Patterns**:
1. TemporalGreeting (morning + first interaction)
2. SpatialJourney (2 sources)
3. AccomplishmentRecognition (has accomplishments)
4. PriorityFraming (always)
5. SummarySynthesis (always)
6. DialogueInvitation (always)

**Constructed Narrative**:
```
Good morning! I've been looking through your work context...

I checked GitHub first - looks like you had 5 commits yesterday, including
completing MUX-GATE-2. Nice work on that one! You also updated the docs,
which should help the team.

For today, the V2 sprint work continues, and reviewing #407 looks like
the priority. Both are substantial but manageable.

Overall, good momentum from yesterday carrying into today.

How does that sound? Anything you'd like me to adjust?
```

---

## Step 4: MVC Validation

Before returning output, validate Minimum Viable Consciousness:

```python
def validate_mvc(output: str) -> MVCResult:
    """Validate output meets Minimum Viable Consciousness."""

    checks = {
        "has_i_statement": bool(re.search(r"\bI\b", output)),
        "has_uncertainty": bool(re.search(
            r"(looks like|might|seems|I think|could be|I'm not sure)",
            output, re.IGNORECASE
        )),
        "has_invitation": bool(re.search(
            r"(how does|what do you|would you|let me know|anything)",
            output, re.IGNORECASE
        )),
        "has_attribution": bool(re.search(
            r"(GitHub|calendar|checked|looked|found|see)",
            output, re.IGNORECASE
        )),
    }

    return MVCResult(
        passes=all(checks.values()),
        checks=checks,
        missing=[k for k, v in checks.items() if not v]
    )
```

### MVC Checklist

| Check | Regex Pattern | Example Pass |
|-------|---------------|--------------|
| Has "I" statement | `\bI\b` | "**I** checked GitHub..." |
| Has uncertainty | `looks like\|might\|seems` | "**looks like** you had..." |
| Has invitation | `how does\|what do you` | "**How does** that sound?" |
| Has attribution | `GitHub\|calendar\|checked` | "I **checked GitHub**..." |

---

## Implementation Functions

### Main Injection Function

```python
async def inject_consciousness(
    result: StandupResult,
    context: Optional[ConsciousnessContext] = None
) -> str:
    """Transform StandupResult into conscious narrative."""

    # Step 1: Analyze context
    if context is None:
        context = analyze_context(result)

    # Step 2: Select patterns
    patterns = select_patterns(context)

    # Step 3: Construct narrative
    narrative = construct_narrative(result, patterns, context)

    # Step 4: Validate MVC
    mvc_result = validate_mvc(narrative)
    if not mvc_result.passes:
        narrative = fix_mvc_gaps(narrative, mvc_result.missing)

    return narrative
```

### Pattern Application Functions

```python
def apply_temporal_greeting(context: ConsciousnessContext) -> str:
    """Generate time-aware greeting."""
    greetings = {
        "morning": "Good morning! I've been looking through your work context...",
        "late_morning": "Starting your day? Let me catch you up...",
        "afternoon": "Afternoon check-in! Here's where things stand...",
        "evening": "End of day reflection? Let's see what you accomplished...",
    }
    return greetings.get(context.time_of_day, greetings["morning"])


def apply_spatial_journey(sources: List[str]) -> str:
    """Generate source navigation narrative."""
    if len(sources) == 1:
        return f"I checked {sources[0]}..."
    elif len(sources) == 2:
        return f"I started by checking {sources[0]}, then looked at {sources[1]}..."
    else:
        return f"I've been looking through {', '.join(sources[:-1])}, and {sources[-1]}..."


def apply_accomplishment_recognition(accomplishments: List[str]) -> str:
    """Generate accomplishment narrative with recognition."""
    if not accomplishments:
        return ""

    if len(accomplishments) == 1:
        return f"Nice work on {accomplishments[0]}!"
    else:
        main = accomplishments[0]
        others = len(accomplishments) - 1
        return f"Looks like you made good progress - {main}, plus {others} other {'item' if others == 1 else 'items'}."


def apply_dialogue_invitation() -> str:
    """Generate closing invitation."""
    invitations = [
        "How does that sound? Anything you'd like me to adjust?",
        "Does this capture your priorities? Let me know what to change.",
        "What do you think? I can update this if something's off.",
    ]
    return random.choice(invitations)
```

---

## Integration Points

### Where to Inject

| Current Function | Location | Injection Point |
|------------------|----------|-----------------|
| `format_as_slack()` | standup.py:307 | Replace entire function |
| `format_as_text()` | standup.py:436 | Replace entire function |
| `format_as_markdown()` | standup.py:372 | Replace entire function |

### New Module Structure

```
services/consciousness/
├── __init__.py
├── context.py          # ConsciousnessContext
├── patterns.py         # Pattern definitions
├── injection.py        # inject_consciousness()
├── validation.py       # MVC validation
└── templates.py        # Pattern templates
```

---

## Testing Strategy

### Unit Tests

```python
def test_mvc_validation_passes():
    output = "Good morning! I checked GitHub and it looks like you had a productive day. How does that sound?"
    result = validate_mvc(output)
    assert result.passes

def test_mvc_validation_fails_no_i():
    output = "Morning standup shows 5 commits."
    result = validate_mvc(output)
    assert not result.passes
    assert "has_i_statement" in result.missing
```

### Integration Tests

```python
async def test_inject_consciousness_full_arc():
    result = StandupResult(...)
    output = await inject_consciousness(result)

    # Check arc elements present
    assert "Good morning" in output or "I've been" in output  # Opening
    assert "checked" in output or "looked" in output  # Journey
    assert "How does" in output or "What do you" in output  # Closing
```

---

## Next Steps

1. **Create transformation templates** (concrete string templates)
2. **Implement pattern functions** in `services/consciousness/`
3. **Replace format functions** with consciousness-injected versions
4. **Add MVC validation** to all output paths

---

*Phase 1 Consciousness Injection Methodology Complete*
*Ready for transformation template creation*
