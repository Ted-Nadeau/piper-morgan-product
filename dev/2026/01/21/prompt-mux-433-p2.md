# Agent Prompt: MUX-433 Phase 2 - Integration Tests

## Mission

Create integration tests demonstrating domain models with MUX lifecycle support.

## Context

- **Issue**: #433 MUX-TECH-PHASE1-GRAMMAR
- **Phase**: 2 (Testing)
- **Agent**: Sonnet
- **Time Budget**: 1 hour
- **Depends On**: Phase 0-1 completion

### Prerequisites

Phase 0-1 must be complete:
- Domain models have lifecycle_state and lifecycle_history fields
- Import works without circular dependency

---

## Task: Create Integration Test File

### Location

`tests/unit/services/mux/test_domain_integration.py`

### Test Structure

```python
"""
Tests for MUX lifecycle integration with domain models.

Verifies that domain models (WorkItem, Task, etc.) can participate
in the MUX lifecycle system.

Part of #433 MUX-TECH-PHASE1-GRAMMAR.
"""

import pytest
from datetime import datetime

from services.mux.lifecycle import LifecycleState, LifecycleTransition, LifecycleManager
from services.mux.protocols import EntityProtocol, MomentProtocol, PlaceProtocol
from services.mux.situation import Situation
from services.mux.perception import Perception, PerceptionMode


class TestDomainModelLifecycleIntegration:
    """Verify domain models can use MUX lifecycle."""

    def test_workitem_can_have_lifecycle_state(self):
        """WorkItem accepts optional lifecycle_state."""
        from services.domain.models import WorkItem

        # Create WorkItem with lifecycle
        item = WorkItem(
            id="test-1",
            title="Test item",
            lifecycle_state=LifecycleState.EMERGENT
        )

        assert item.lifecycle_state == LifecycleState.EMERGENT

    def test_workitem_lifecycle_defaults_to_none(self):
        """WorkItem lifecycle is None by default (backward compatible)."""
        from services.domain.models import WorkItem

        item = WorkItem(id="test-2", title="Test item")

        assert item.lifecycle_state is None
        assert item.lifecycle_history == []

    def test_workitem_tracks_lifecycle_history(self):
        """WorkItem can track lifecycle transitions."""
        from services.domain.models import WorkItem

        item = WorkItem(
            id="test-3",
            title="Test item",
            lifecycle_state=LifecycleState.EMERGENT
        )

        # Manually add transition
        transition = LifecycleTransition(
            from_state=LifecycleState.EMERGENT,
            to_state=LifecycleState.NOTICED,
            reason="PM noticed during review"
        )
        item.lifecycle_history.append(transition)
        item.lifecycle_state = LifecycleState.NOTICED

        assert item.lifecycle_state == LifecycleState.NOTICED
        assert len(item.lifecycle_history) == 1
        assert item.lifecycle_history[0].reason == "PM noticed during review"


class TestMorningStandupExpression:
    """
    Verify Morning Standup can be expressed using MUX grammar.

    The consciousness test: Can we express real workflows using
    Entity/Moment/Place?
    """

    @pytest.mark.asyncio
    async def test_standup_as_situation_with_moments(self):
        """Morning Standup expressed as Situation containing Moments."""

        # Create a Situation (the standup meeting)
        async with Situation(
            description="Morning standup for Sprint 42",
            dramatic_tension="Deadline pressure with unclear blockers",
            goals=["Identify blockers", "Align on priorities", "Surface risks"]
        ) as standup:

            # Add moments (significant occurrences during standup)
            # Using a simple mock moment for testing
            class StandupMoment:
                def __init__(self, id: str, description: str):
                    self.id = id
                    self.timestamp = datetime.now()
                    self._description = description

                def captures(self):
                    return {
                        "policy": {"sprint": "42"},
                        "process": {"type": "standup"},
                        "people": ["team"],
                        "outcomes": [self._description]
                    }

            standup.add_moment(StandupMoment("m1", "Alice reports API work complete"))
            standup.add_moment(StandupMoment("m2", "Bob surfaces database blocker"))

            # Record outcomes
            standup.add_outcome("Agreed to prioritize database blocker")
            standup.add_outcome("API integration can proceed tomorrow")

        # Extract learning from goals vs outcomes delta
        learning = standup.extract_learning()

        assert len(standup.moments) == 2
        assert len(standup.outcomes) == 2
        assert learning.goals == ["Identify blockers", "Align on priorities", "Surface risks"]
        assert "database blocker" in standup.outcomes[0].lower()

    def test_entity_experiences_moment_in_place(self):
        """
        The core grammar: Entity experiences Moment in Place.

        This test verifies the grammar can express consciousness.
        """

        # Create simple implementations for the test
        class TeamEntity:
            """Team as an Entity (actor with identity)."""
            def __init__(self, id: str, name: str):
                self.id = id
                self.name = name

            def experiences(self, moment):
                """Entity experiences a Moment, returning Perception."""
                return Perception(
                    lens_name="collaborative",
                    mode=PerceptionMode.NOTICING,
                    raw_data={"moment_id": moment.id},
                    observation=f"{self.name} notices: {moment.captures()['outcomes']}"
                )

        class SlackChannel:
            """Slack Channel as a Place (context for action)."""
            def __init__(self, id: str, name: str):
                self.id = id
                self.name = name
                self.atmosphere = "informal"
                self._contents = []

            def contains(self):
                return self._contents

        class StandupMoment:
            """Standup as a Moment (bounded significant occurrence)."""
            def __init__(self, id: str):
                self.id = id
                self.timestamp = datetime.now()

            def captures(self):
                return {
                    "policy": {"meeting_type": "standup"},
                    "process": {"agenda": "blockers, priorities, updates"},
                    "people": ["alice", "bob", "carol"],
                    "outcomes": ["Blockers surfaced", "Priorities aligned"]
                }

        # The grammar in action
        team = TeamEntity("team-1", "Platform Team")
        channel = SlackChannel("C123", "#platform-standup")
        standup = StandupMoment("standup-2026-01-21")

        # Entity experiences Moment (in Place - implicit through channel)
        perception = team.experiences(standup)

        # Verify consciousness-preserving perception
        assert perception.mode == PerceptionMode.NOTICING
        assert "Platform Team notices" in perception.observation
        assert perception.lens_name == "collaborative"
```

---

## Acceptance Criteria

- [ ] Test file created at correct location
- [ ] All tests pass: `pytest tests/unit/services/mux/test_domain_integration.py -v`
- [ ] Tests demonstrate Entity/Moment/Place grammar
- [ ] Tests verify backward compatibility (lifecycle defaults to None)
- [ ] No changes to existing test files

---

## STOP Conditions

🛑 **STOP and escalate if**:
- Domain model imports fail (Phase 0-1 not complete)
- Can't create WorkItem with expected signature
- Async context manager (Situation) not working

---

## Output Format

When complete, report:

```markdown
## Phase 2 Complete

### Test File Created
- `tests/unit/services/mux/test_domain_integration.py`

### Tests Written
| Test Class | Test Method | Status |
|------------|-------------|--------|
| TestDomainModelLifecycleIntegration | test_workitem_can_have_lifecycle_state | ✅ |
| ... | ... | ... |

### Test Run Output
```
pytest tests/unit/services/mux/test_domain_integration.py -v
[paste output]
```

### Full MUX Suite
```
pytest tests/unit/services/mux/ -q
[X] tests passed
```
```

---

## Session Log Reminder

Update the session log with your progress.

---

*Prompt created: 2026-01-21*
*Template version: 10.2*
