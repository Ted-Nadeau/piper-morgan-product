# Lifecycle Experience Guide

**Status**: Implemented (#408)
**Last Updated**: January 22, 2026

This guide documents how Piper expresses lifecycle states to users, ensuring consistent, natural language across all interactions.

## Overview

Piper's 8-stage lifecycle model tracks how objects (features, work items, etc.) evolve from initial perception to learning extraction. Each stage has:

1. **Experience Phrase**: How Piper begins describing something in that state
2. **Transition Explanation**: How Piper explains movement between states
3. **Error Messages**: User-friendly explanations when transitions fail

## The 8 Lifecycle States

### EMERGENT
**Experience Phrase**: "I just noticed..."
**Meaning**: Something forming that hasn't been categorized yet
**Typical Objects**: Vague patterns, initial signals, half-formed ideas

### DERIVED
**Experience Phrase**: "I figured out from..."
**Meaning**: Inferred from other information, connected dots
**Typical Objects**: Synthesized insights, connected patterns, derived conclusions

### NOTICED
**Experience Phrase**: "I'm aware of..."
**Meaning**: Explicitly brought to attention
**Typical Objects**: Flagged items, tracked tasks, watched projects

### PROPOSED
**Experience Phrase**: "I think we should..."
**Meaning**: Suggested for action or decision
**Typical Objects**: Recommendations, suggested actions, proposed changes

### RATIFIED
**Experience Phrase**: "We're doing..."
**Meaning**: Confirmed, agreed upon, in active use
**Typical Objects**: Active projects, confirmed plans, committed work

### DEPRECATED
**Experience Phrase**: "This used to be..."
**Meaning**: Still exists but no longer active
**Typical Objects**: Completed work, superseded plans, past commitments

### ARCHIVED
**Experience Phrase**: "I remember when..."
**Meaning**: Preserved for reference, not for active use
**Typical Objects**: Historical records, completed projects, past learnings

### COMPOSTED
**Experience Phrase**: "I learned that..."
**Meaning**: Transformed into learning, enriching future work
**Typical Objects**: Wisdom extracted from experience, lessons learned

## Transition Explanations

When objects move between states, Piper explains why:

| From → To | Explanation Template |
|-----------|---------------------|
| EMERGENT → DERIVED | "I recognized a pattern in {object}" |
| EMERGENT → NOTICED | "I noticed {object} needed attention" |
| DERIVED → NOTICED | "{object} caught my attention" |
| DERIVED → DEPRECATED | "{object} is no longer relevant" |
| NOTICED → PROPOSED | "I think we should act on {object}" |
| NOTICED → DEPRECATED | "{object} is no longer a priority" |
| PROPOSED → RATIFIED | "We agreed to proceed with {object}" |
| PROPOSED → DEPRECATED | "We decided not to pursue {object}" |
| RATIFIED → DEPRECATED | "{object} has served its purpose" |
| DEPRECATED → ARCHIVED | "I'm preserving {object} for reference" |
| ARCHIVED → COMPOSTED | "{object} has taught me something" |

### Using Transition Explanations

```python
from services.mux.lifecycle import transition_explanation, LifecycleState

# Basic usage
explanation = transition_explanation(
    LifecycleState.PROPOSED,
    LifecycleState.RATIFIED,
    "the sprint plan"
)
# Returns: "We agreed to proceed with the sprint plan"

# With reason
explanation = transition_explanation(
    LifecycleState.NOTICED,
    LifecycleState.DEPRECATED,
    "this task",
    reason="priorities shifted"
)
# Returns: "this task is no longer a priority - priorities shifted"
```

## Friendly Error Messages

When invalid transitions are attempted, Piper explains without technical jargon:

| Scenario | User Message |
|----------|-------------|
| Going backward | "I can't go back to that state - things only move forward" |
| Skipping states | "That's too big a jump - let's take it one step at a time" |
| From COMPOSTED | "Once something becomes a learning, it stays that way" |

### Using Error Messages

```python
from services.mux.lifecycle import InvalidTransitionError, LifecycleState

try:
    # Attempt invalid transition
    manager.transition(obj, LifecycleState.EMERGENT)  # Going backward
except InvalidTransitionError as e:
    # Technical message (for logs)
    print(str(e))
    # User-friendly message (for display)
    print(e.user_message)
    # "I can't go back to that state - things only move forward"
```

## Composting Narratives

When objects reach COMPOSTED, Piper generates reflective narratives:

### Narrative Templates by Journey Type

| Journey | Narrative Style |
|---------|-----------------|
| Full lifecycle (6+ states, ratified) | "Having had time to reflect on {object}, I learned: {lessons}" |
| Full but never ratified | "{object} went through many stages but never quite landed. Still, I noticed: {lessons}" |
| Short (≤3 states, not ratified) | "{object} was brief, but I noticed: {lessons}" |
| Ratified then deprecated | "{object} worked for a while. Looking back: {lessons}" |

### Using Composting Narratives

```python
from services.mux.lifecycle import get_composting_narrative, CompostingExtractor

# Extract wisdom and generate narrative
extractor = CompostingExtractor()
result = extractor.extract(completed_feature)
narrative = get_composting_narrative(result)
# "Having had time to reflect on the auth feature, I learned: patterns are worth studying; this approach was validated."
```

## Integration with Handlers

### Helper Functions

The `lifecycle_integration` module provides helpers for intent handlers:

```python
from services.mux.lifecycle_integration import (
    describe_with_lifecycle,
    has_lifecycle,
    format_lifecycle_context,
)

# Check if object has lifecycle
if has_lifecycle(feature):
    # Add lifecycle-aware prefix
    description = describe_with_lifecycle(feature, "the auth feature")
    # "I just noticed the auth feature" (if EMERGENT)

    # Get lifecycle context
    context = format_lifecycle_context(feature)
    # "I just noticed..."
```

### Integration Pattern

```python
# In a handler formatting response:
def format_feature_status(feature):
    if has_lifecycle(feature):
        prefix = feature.lifecycle_state.experience_phrase
        return f"{prefix} {feature.name} is {feature.status}"
    return f"{feature.name} is {feature.status}"
```

## Design Principles

### The "Contractor Test"
Every phrase must pass: "Would a colleague say this naturally?"

**Pass**: "I just noticed this task needs attention"
**Fail**: "I sense something forming, though its shape is not yet clear"

### No Deletion Language
COMPOSTED objects are never "deleted" - they transform into learning:

**Good**: "I learned that daily standups work better in morning"
**Bad**: "The standup experiment was deleted"

### First-Person Perspective
All phrases use "I" or "We" perspective:
- "I just noticed..." (EMERGENT)
- "We're doing..." (RATIFIED)
- "I learned that..." (COMPOSTED)

### Forward-Only Movement
Lifecycle states only move forward. Error messages explain this naturally:
- Not: "Error: Invalid transition RATIFIED→PROPOSED"
- But: "I can't go back to that state - things only move forward"

## Related Documentation

- **ADR-055**: Object Model Implementation
- **Pattern-050**: Context-Dataclass Pair
- **Architecture**: `composting-learning-architecture.md`
- **Source Design**: `dev/2025/11/29/object-model-brief-v2.md`

## Test Coverage

| Component | Test Count | File |
|-----------|------------|------|
| Experience phrases | 8 | `test_lifecycle.py` |
| Transition explanations | 11 | `test_lifecycle.py` |
| Composting narratives | 10 | `test_lifecycle.py` |
| Error messages | 4 | `test_lifecycle.py` |
| Integration helpers | 20 | `test_lifecycle_integration.py` |
| **Total** | **53** | |

All tests verify natural language and absence of technical jargon.
