# Manual Testing Scenarios: #408 Lifecycle Experience

**For**: PM Manual Testing
**Date**: January 22, 2026
**Author**: Lead Developer

These scenarios verify that lifecycle language "feels natural" - the qualitative aspect that unit tests can't capture.

---

## Scenario 1: Experience Phrase Check

**Objective**: Verify all 8 experience phrases pass the "contractor test"

### Test Procedure

Run in Python console:
```python
from services.mux.lifecycle import LifecycleState

for state in LifecycleState:
    print(f"{state.name}: {state.experience_phrase}")
```

### Expected Output
```
EMERGENT: I just noticed...
DERIVED: I figured out from...
NOTICED: I'm aware of...
PROPOSED: I think we should...
RATIFIED: We're doing...
DEPRECATED: This used to be...
ARCHIVED: I remember when...
COMPOSTED: I learned that...
```

### Contractor Test Questions
For each phrase, ask:
1. Would a competent colleague start a sentence this way?
2. Is it natural, not robotic?
3. Does it make sense for the state it represents?

---

## Scenario 2: Transition Explanations

**Objective**: Verify transition explanations sound natural in context

### Test Procedure

Run in Python console:
```python
from services.mux.lifecycle import transition_explanation, LifecycleState

# Test key transitions
transitions = [
    (LifecycleState.EMERGENT, LifecycleState.NOTICED, "this task"),
    (LifecycleState.PROPOSED, LifecycleState.RATIFIED, "the sprint plan"),
    (LifecycleState.RATIFIED, LifecycleState.DEPRECATED, "the old feature"),
    (LifecycleState.ARCHIVED, LifecycleState.COMPOSTED, "that project"),
]

for from_state, to_state, obj in transitions:
    explanation = transition_explanation(from_state, to_state, obj)
    print(f"{from_state.name} → {to_state.name}: {explanation}")
```

### Expected Output
```
EMERGENT → NOTICED: I noticed this task needed attention
PROPOSED → RATIFIED: We agreed to proceed with the sprint plan
RATIFIED → DEPRECATED: the old feature has served its purpose
ARCHIVED → COMPOSTED: that project has taught me something
```

### Verification Questions
1. Does each explanation sound like something Piper would naturally say?
2. Is the object name integrated naturally?
3. Does the explanation convey the "why" of the transition?

---

## Scenario 3: Composting Narrative

**Objective**: Verify composting narratives are reflective, not clinical

### Test Procedure

Run in Python console:
```python
from datetime import datetime
from services.mux.lifecycle import (
    LifecycleState, CompostResult, get_composting_narrative
)

# Full lifecycle journey
full_journey = [
    LifecycleState.EMERGENT,
    LifecycleState.DERIVED,
    LifecycleState.NOTICED,
    LifecycleState.PROPOSED,
    LifecycleState.RATIFIED,
    LifecycleState.DEPRECATED,
    LifecycleState.ARCHIVED,
    LifecycleState.COMPOSTED,
]

result = CompostResult(
    object_summary={"title": "Sprint 42 Retrospective"},
    journey=full_journey,
    lessons=["Patterns are worth studying", "This approach was validated"],
    composted_at=datetime.now(),
)
print("Full journey:", get_composting_narrative(result))

# Short journey
short_result = CompostResult(
    object_summary={"title": "Quick experiment"},
    journey=[LifecycleState.EMERGENT, LifecycleState.DEPRECATED, LifecycleState.COMPOSTED],
    lessons=["Sometimes ideas don't pan out"],
    composted_at=datetime.now(),
)
print("Short journey:", get_composting_narrative(short_result))
```

### Expected Output (similar to)
```
Full journey: Having had time to reflect on Sprint 42 Retrospective, I learned: Patterns are worth studying; This approach was validated.
Short journey: Quick experiment was brief, but I noticed: Sometimes ideas don't pan out.
```

### Verification Questions
1. Does the narrative feel like "filing dreams" rather than "deleting files"?
2. Is the reflective tone appropriate?
3. Does it avoid surveillance-y language?

---

## Scenario 4: Error Messages

**Objective**: Verify error messages are friendly, not technical

### Test Procedure

Run in Python console:
```python
from services.mux.lifecycle import InvalidTransitionError, LifecycleState

# Backward transition
error1 = InvalidTransitionError(LifecycleState.RATIFIED, LifecycleState.PROPOSED)
print("Backward:", error1.user_message)

# Skip transition
error2 = InvalidTransitionError(LifecycleState.EMERGENT, LifecycleState.RATIFIED)
print("Skip:", error2.user_message)

# From COMPOSTED
error3 = InvalidTransitionError(LifecycleState.COMPOSTED, LifecycleState.EMERGENT)
print("From COMPOSTED:", error3.user_message)
```

### Expected Output
```
Backward: I can't go back to that state - things only move forward
Skip: That's too big a jump - let's take it one step at a time
From COMPOSTED: Once something becomes a learning, it stays that way
```

### Verification Questions
1. Are state names (RATIFIED, PROPOSED, etc.) hidden from user?
2. Is the language friendly, not error-like?
3. Does the message explain why, not just say "no"?

---

## Scenario 5: Integration Helper

**Objective**: Verify integration helpers work as documented

### Test Procedure

Run in Python console:
```python
from dataclasses import dataclass
from services.mux.lifecycle import LifecycleState
from services.mux.lifecycle_integration import (
    describe_with_lifecycle,
    has_lifecycle,
)

@dataclass
class MockFeature:
    name: str
    lifecycle_state: LifecycleState = None

# With lifecycle
feature = MockFeature(name="Auth", lifecycle_state=LifecycleState.PROPOSED)
print("With lifecycle:", describe_with_lifecycle(feature, "the auth feature"))
print("Has lifecycle:", has_lifecycle(feature))

# Without lifecycle
@dataclass
class MockTodo:
    title: str

todo = MockTodo(title="Review PR")
print("Without lifecycle:", describe_with_lifecycle(todo, "the review task"))
print("Has lifecycle:", has_lifecycle(todo))
```

### Expected Output
```
With lifecycle: I think we should... the auth feature
Has lifecycle: True
Without lifecycle: the review task
Has lifecycle: False
```

### Verification Questions
1. Does the prefix integrate naturally?
2. Does the fallback (no lifecycle) return unchanged text?

---

## PM Sign-Off Checklist

After completing all scenarios:

- [x] All experience phrases pass contractor test
- [x] Transition explanations sound natural
- [x] Composting narratives feel reflective, not surveillance-y
- [x] Error messages are friendly and jargon-free
- [x] Integration helpers work as expected

**PM Verdict**: All tests pass

**Notes**:
Results match expected perfectly, and pass my uncanniness test as a human.
     --xian


---

_Generated: January 22, 2026_
_Issue: #408 MUX-VISION-LIFECYCLE-SPEC_
