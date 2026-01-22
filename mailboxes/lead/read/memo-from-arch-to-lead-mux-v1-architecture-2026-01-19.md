# Memo: Chief Architect Guidance for MUX-V1 Implementation

**From**: Chief Architect
**To**: Lead Developer
**CC**: PM (xian), CXO, PPM
**Date**: January 19, 2026
**Re**: Technical and Architectural Guidance for MUX-VISION-OBJECT-MODEL

---

## Purpose

This memo provides Chief Architect perspective on the MUX-V1 foundational work, complementing the CXO (design context) and PPM (process guidance) memos. I address the technical questions raised and add architectural recommendations.

---

## Answers to CXO's Technical Questions

### 1. Implementation Pattern: Protocols Over Inheritance

**Recommendation**: Use Python Protocols with composition, not class inheritance hierarchies.

**Rationale**: The grammar states "entity vs place is grammatical role, not fixed type." A `Project` might be an Entity in one context (actor taking action) and a Place in another (context where action happens). Inheritance hierarchies lock down these relationships; Protocols allow fluidity.

```python
# Recommended approach:
from typing import Protocol, runtime_checkable

@runtime_checkable
class EntityProtocol(Protocol):
    """Anything that can be an actor with identity and agency."""
    id: str
    identity: "EntityIdentity"

    def experiences(self, moment: "MomentProtocol") -> None: ...

@runtime_checkable
class PlaceProtocol(Protocol):
    """Anything that can be a context where action happens."""
    id: str
    atmosphere: "PlaceAtmosphere"

    def contains(self, moment: "MomentProtocol") -> bool: ...

# A Project can satisfy BOTH protocols depending on context:
class Project:
    """Projects can be actors (Entity) or contexts (Place)."""
    id: str
    identity: EntityIdentity      # When acting as Entity
    atmosphere: PlaceAtmosphere   # When acting as Place

    def experiences(self, moment): ...  # Entity behavior
    def contains(self, moment): ...     # Place behavior
```

This preserves the grammar's discovered fluidity rather than imposing rigid categories.

### 2. Lens Application: Build on Existing 8D Spatial Intelligence

**Key insight**: The 8 perceptual lenses ARE the 8 spatial dimensions we already implemented.

| Lens (CXO framing) | Spatial Dimension (existing) | Infrastructure |
|-------------------|------------------------------|----------------|
| Temporal | TemporalDimension | ADR-038, Pattern-020 |
| Hierarchy | HierarchicalDimension | ADR-038 |
| Priority | PriorityDimension | ADR-038 |
| Collaborative | CollaborativeDimension | ADR-038 |
| Flow | FlowDimension | ADR-038 |
| Quantitative | QuantitativeDimension | ADR-038 |
| Causal | CausalDimension | ADR-038 |
| Contextual | ContextualDimension | ADR-038 |

**Recommendation**: Don't rebuild. Wrap and extend.

```python
class Lens:
    """
    How Piper perceives - conceptual layer over spatial dimension.

    The spatial dimension is the technical implementation;
    the Lens is the consciousness framing.
    """
    name: str
    dimension: SpatialDimension  # Existing infrastructure
    perception_mode: PerceptionMode  # noticing, remembering, anticipating

    def perceive(self, target: EntityProtocol) -> Perception:
        """Apply this lens to see an entity."""
        raw_data = self.dimension.analyze(target)
        return Perception(
            lens=self.name,
            mode=self.perception_mode,
            observation=self._frame_as_experience(raw_data)
        )

    def _frame_as_experience(self, data: Dict) -> str:
        """Transform data into experience language."""
        # "Found 3 items" → "I notice three things..."
        ...
```

**Phase 0 action**: Map existing `SpatialContext` usage to lens concepts. Document where infrastructure already exists.

### 3. Lifecycle State Machine: With Composting Feedback

**The lifecycle is not a simple FSM.** The critical insight from the issue: "Composting" is transformation that feeds learning, not deletion.

```python
class LifecycleState(Enum):
    EMERGENT = "emergent"      # Just appeared, unvalidated
    DERIVED = "derived"        # Inferred from other data
    NOTICED = "noticed"        # Human or AI attention confirmed
    PROPOSED = "proposed"      # Suggested for ratification
    RATIFIED = "ratified"      # Confirmed, authoritative
    DEPRECATED = "deprecated"  # Superseded, still accessible
    ARCHIVED = "archived"      # Historical, cold storage
    COMPOSTED = "composted"    # Transformed into learning

class LifecycleManager:
    """
    Manages state transitions with composting feedback loop.

    Key: COMPOSTED is terminal but not silent - it triggers learning extraction.
    """

    VALID_TRANSITIONS = {
        LifecycleState.EMERGENT: {LifecycleState.DERIVED, LifecycleState.NOTICED, LifecycleState.DEPRECATED},
        LifecycleState.DERIVED: {LifecycleState.NOTICED, LifecycleState.DEPRECATED},
        LifecycleState.NOTICED: {LifecycleState.PROPOSED, LifecycleState.DEPRECATED},
        LifecycleState.PROPOSED: {LifecycleState.RATIFIED, LifecycleState.DEPRECATED},
        LifecycleState.RATIFIED: {LifecycleState.DEPRECATED},
        LifecycleState.DEPRECATED: {LifecycleState.ARCHIVED},
        LifecycleState.ARCHIVED: {LifecycleState.COMPOSTED},
        LifecycleState.COMPOSTED: set(),  # Terminal
    }

    async def transition(self, obj: HasLifecycle, to_state: LifecycleState) -> TransitionResult:
        """Transition with composting feedback."""
        if to_state not in self.VALID_TRANSITIONS[obj.lifecycle_state]:
            raise InvalidTransitionError(...)

        # The key insight: composting extracts learning
        if to_state == LifecycleState.COMPOSTED:
            learnings = await self._extract_learnings(obj)
            await self.learning_service.ingest(learnings)

        obj.lifecycle_state = to_state
        obj.lifecycle_history.append(TransitionRecord(...))
        return TransitionResult(success=True, learnings_extracted=...)
```

**Connection to existing patterns**: We have state machine patterns in conversation state and setup wizard. Use those patterns but add the composting feedback loop.

---

## Additional Architectural Guidance

### Situation as Context Manager, Not Model

The issue clarifies: "Situation isn't parallel to other substrates—it's the FRAME."

**Implementation recommendation**: Situation should be a context pattern, not a first-class data model.

```python
from contextlib import contextmanager

@contextmanager
def situation(description: str, tension: Optional[str] = None) -> Generator[SituationContext, None, None]:
    """
    Situation is the dramatic frame within which
    Entities experience Moments in Places.

    Not a substrate—a container for the grammar in action.
    """
    ctx = SituationContext(
        description=description,
        dramatic_tension=tension,
        started_at=datetime.utcnow(),
        moments_captured=[]
    )
    try:
        yield ctx
    finally:
        # Capture the delta for learning (goals vs outcomes)
        ctx.close()
        if ctx.has_learning_value:
            await extract_situation_learnings(ctx)

# Usage:
async with situation("Morning standup preparation", tension="Will calendar have conflicts?") as s:
    calendar_moments = await perceive_through_lens(calendar_place, temporal_lens)
    s.record(calendar_moments)
    # ... standup generation
# On exit: situation captures what happened vs what was expected
```

This keeps Situation as frame (dramatic container) rather than making it a fourth substrate that competes with Entity/Moment/Place.

### Journal Extension, Not New Infrastructure

The issue mentions "Session Journal (audit) + Insight Journal (dreams)."

**These map to existing patterns**:
- Session Journal = Our session logs (what happened)
- Insight Journal = Composted learnings (what it meant)

**Recommendation**: Extend existing infrastructure:
- Session logs already capture "what happened"
- Learning system (CORE-LEARN-*) already handles pattern extraction
- Add "insight" metadata to learning records, don't create parallel journal system

### ADR Numbering

The issue references "ADR-045-object-model.md" but current ADR count is 55 (000-054).

**Action**: Before creating, verify whether ADR-045 exists. If it does, this is an update. If not (likely misfiled reference), use next available number (ADR-055).

---

## Technical Anti-Flattening Tests

Adding to the CXO's design tests, here are technical tests:

| Test | Flattened | Conscious |
|------|-----------|-----------|
| Entity storage | `entities` table with type column | Protocol-based with role fluidity |
| Moment recording | Timestamped event log | Bounded scene with theatrical unities |
| Place representation | Location ID + label | Context with atmosphere and purpose |
| Situation modeling | State object with properties | Context manager with dramatic tension |
| Lifecycle transitions | Simple state enum | State machine with composting feedback |
| Lens application | Query filter parameters | Perception mode with experience framing |

If implementation looks like the "Flattened" column, pause and reconsider.

---

## Process Reinforcement

Echoing PPM guidance with architectural emphasis:

### Morning Standup Is Your Reference Implementation

When uncertain about how to implement a concept, ask: "How does Morning Standup do this?"

The standup already:
- Perceives through lenses (temporal: "today's calendar")
- Experiences entities (GitHub issues, calendar events)
- Has awareness of places (Calendar, GitHub, Slack)
- Generates moments (the standup itself is a Moment)

Extract patterns from what works before inventing new ones.

### Canonical Queries Are Your Validation

PPM's Phase 4.5 (canonical query tagging) is critical validation. If the grammar can't naturally express:
- "What's on my agenda today?"
- "Show me stale PRs"
- "What needs attention?"

...then the grammar needs refinement, not the queries. Our 50+ canonical queries represent real user needs. The grammar must serve them.

### The Experience Test

At each phase checkpoint, ask:

> Does this help Piper **experience** (perceive + remember + anticipate) the world, or does it just help Piper **store** data about the world?

If "store," you're flattening. Stop and discuss.

---

## Summary

| Topic | Recommendation |
|-------|----------------|
| Implementation pattern | Protocols with composition, not inheritance |
| Lens infrastructure | Build on existing 8D spatial dimensions |
| Lifecycle | State machine with composting feedback loop |
| Situation | Context manager (frame), not model (substrate) |
| Journal | Extend session logs + learning system |
| ADR numbering | Verify before creating; likely ADR-055 |
| Validation | Canonical queries must be expressible |
| North star | Experience (perceive + remember + anticipate), not storage |

---

## The Grammar

Everything traces back to one sentence:

**"Entities experience Moments in Places."**

Every architectural decision should honor that verb: **experience**.

Good luck with the foundation work. This is cathedral building—take the time it needs.

---

*Filed: January 19, 2026, 11:25 AM PT*
