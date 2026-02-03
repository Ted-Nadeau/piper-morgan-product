# 8D Spatial Dimensions to Perceptual Lenses Mapping

**Location**: `docs/internal/architecture/current/8d-spatial-to-lens-mapping.md`
**Date**: January 19, 2026
**Author**: Chief Architect
**Related**: ADR-038 (Spatial Intelligence), ADR-055 (Object Model)

---

## Overview

This document formally maps the existing 8D spatial intelligence architecture (ADR-038, Pattern-020) to the perceptual lenses concept in the object model grammar.

**Key insight**: The 8 perceptual lenses ARE the 8 spatial dimensions. The spatial architecture was the technical implementation; lenses are the consciousness framing. We do not rebuild—we wrap and extend.

---

## The Mapping

| Lens | Spatial Dimension | Infrastructure Location | Perception Question |
|------|-------------------|-------------------------|---------------------|
| Temporal | `TemporalDimension` | `services/spatial/dimensions/temporal.py` | When did/will this happen? |
| Hierarchy | `HierarchicalDimension` | `services/spatial/dimensions/hierarchical.py` | What contains/is contained by this? |
| Priority | `PriorityDimension` | `services/spatial/dimensions/priority.py` | How important/urgent is this? |
| Collaborative | `CollaborativeDimension` | `services/spatial/dimensions/collaborative.py` | Who is involved? |
| Flow | `FlowDimension` | `services/spatial/dimensions/flow.py` | What state is this in? |
| Quantitative | `QuantitativeDimension` | `services/spatial/dimensions/quantitative.py` | How much/many? |
| Causal | `CausalDimension` | `services/spatial/dimensions/causal.py` | What caused/will result from this? |
| Contextual | `ContextualDimension` | `services/spatial/dimensions/contextual.py` | What surrounds this? |

---

## Detailed Mapping

### 1. Temporal Lens ← TemporalDimension

**Dimension Purpose**: Analyze when things happen, sequences, and time-based relationships.

**Lens Perception Mode**:
- **Noticing**: "You have three meetings today"
- **Remembering**: "This is similar to last Tuesday's pattern"
- **Anticipating**: "Tomorrow looks lighter"

**Existing Capabilities**:
- `analyze_temporal_context()` - Time-based analysis
- `get_temporal_relationships()` - Before/after/during
- `calculate_urgency()` - Deadline awareness

**Lens Extension Needed**:
```python
class TemporalLens(Lens):
    dimension: TemporalDimension

    def perceive(self, target: EntityProtocol, mode: PerceptionMode) -> Perception:
        temporal_data = self.dimension.analyze(target)

        if mode == PerceptionMode.NOTICING:
            return self._frame_as_current(temporal_data)
        elif mode == PerceptionMode.REMEMBERING:
            return self._frame_as_historical(temporal_data)
        elif mode == PerceptionMode.ANTICIPATING:
            return self._frame_as_future(temporal_data)
```

**Example Queries Using This Lens**:
- "What's on my agenda today?" → Temporal (today filter)
- "What did I do last week?" → Temporal (past filter) + Remembering mode
- "When is my next free block?" → Temporal (future filter) + Anticipating mode

---

### 2. Hierarchy Lens ← HierarchicalDimension

**Dimension Purpose**: Analyze parent-child, containment, and scope relationships.

**Lens Perception Mode**:
- **Noticing**: "This issue belongs to the Authentication epic"
- **Remembering**: "This project used to be under Platform team"
- **Anticipating**: "If we merge these, the hierarchy will simplify"

**Existing Capabilities**:
- `get_parent()` / `get_children()` - Tree navigation
- `calculate_depth()` - Level in hierarchy
- `find_common_ancestor()` - Relationship analysis

**Lens Extension Needed**:
```python
class HierarchyLens(Lens):
    dimension: HierarchicalDimension

    def perceive_containment(self, target: EntityProtocol) -> Perception:
        """What contains this? What does this contain?"""
        ...

    def perceive_scope(self, target: EntityProtocol) -> Perception:
        """How broad/narrow is this entity's scope?"""
        ...
```

**Example Queries Using This Lens**:
- "What epic is this under?" → Hierarchy (parent lookup)
- "Show me all issues in this project" → Hierarchy (children lookup)
- "What's the highest-level blocker?" → Hierarchy + Priority (compound)

---

### 3. Priority Lens ← PriorityDimension

**Dimension Purpose**: Analyze importance, urgency, and attention-worthiness.

**Lens Perception Mode**:
- **Noticing**: "Three items need your attention"
- **Remembering**: "This keeps coming back as high priority"
- **Anticipating**: "This will become urgent next week"

**Existing Capabilities**:
- `calculate_priority_score()` - Importance scoring
- `identify_blockers()` - What's preventing progress
- `rank_by_urgency()` - Time-sensitive ordering

**Lens Extension Needed**:
```python
class PriorityLens(Lens):
    dimension: PriorityDimension

    def perceive_attention_need(self, targets: List[EntityProtocol]) -> Perception:
        """What deserves attention right now?"""
        ...

    def perceive_risk(self, target: EntityProtocol) -> Perception:
        """What could go wrong if this is ignored?"""
        ...
```

**Example Queries Using This Lens**:
- "What needs attention?" → Priority (attention-worthy filter)
- "What's blocking me?" → Priority (blocker detection)
- "What can I ignore?" → Priority (low-priority filter)

---

### 4. Collaborative Lens ← CollaborativeDimension

**Dimension Purpose**: Analyze who's involved, roles, and relationships between people/agents.

**Lens Perception Mode**:
- **Noticing**: "Ted is assigned to this"
- **Remembering**: "You and Michelle discussed this last month"
- **Anticipating**: "This will need review from the team"

**Existing Capabilities**:
- `get_assignees()` / `get_participants()` - People involved
- `analyze_collaboration_patterns()` - Who works with whom
- `identify_stakeholders()` - Who cares about this

**Lens Extension Needed**:
```python
class CollaborativeLens(Lens):
    dimension: CollaborativeDimension

    def perceive_involvement(self, target: MomentProtocol) -> Perception:
        """Who is part of this moment?"""
        ...

    def perceive_relationships(self, entities: List[EntityProtocol]) -> Perception:
        """How do these entities relate to each other?"""
        ...
```

**Example Queries Using This Lens**:
- "Who's working on authentication?" → Collaborative (assignee lookup)
- "What has Ted touched recently?" → Collaborative + Temporal (compound)
- "Who should review this?" → Collaborative (stakeholder inference)

---

### 5. Flow Lens ← FlowDimension

**Dimension Purpose**: Analyze state transitions, progress, and momentum.

**Lens Perception Mode**:
- **Noticing**: "This PR is stuck in review"
- **Remembering**: "This moved quickly last time"
- **Anticipating**: "Expect a bottleneck at QA"

**Existing Capabilities**:
- `get_current_state()` - Where in workflow
- `analyze_transitions()` - State change history
- `calculate_velocity()` - Speed of progress

**Lens Extension Needed**:
```python
class FlowLens(Lens):
    dimension: FlowDimension

    def perceive_momentum(self, target: EntityProtocol) -> Perception:
        """Is this moving, stuck, or accelerating?"""
        ...

    def perceive_bottlenecks(self, targets: List[EntityProtocol]) -> Perception:
        """Where is flow being blocked?"""
        ...
```

**Example Queries Using This Lens**:
- "What's stuck?" → Flow (no-transition filter)
- "What moved this week?" → Flow + Temporal (compound)
- "Show me stale PRs" → Flow + Temporal + Priority (compound)

---

### 6. Quantitative Lens ← QuantitativeDimension

**Dimension Purpose**: Analyze counts, metrics, and thresholds.

**Lens Perception Mode**:
- **Noticing**: "You have 12 open items"
- **Remembering**: "That's up from 8 last week"
- **Anticipating**: "At this rate, you'll hit the threshold Tuesday"

**Existing Capabilities**:
- `count()` - Simple counting
- `calculate_metrics()` - Derived numbers
- `compare_to_threshold()` - Limit checking

**Lens Extension Needed**:
```python
class QuantitativeLens(Lens):
    dimension: QuantitativeDimension

    def perceive_magnitude(self, targets: List[EntityProtocol]) -> Perception:
        """How many? How much?"""
        ...

    def perceive_trend(self, target: EntityProtocol, timeframe: TimeBound) -> Perception:
        """Is this increasing, decreasing, stable?"""
        ...
```

**Example Queries Using This Lens**:
- "How many issues are open?" → Quantitative (count)
- "What's my velocity?" → Quantitative + Temporal (compound)
- "Am I over capacity?" → Quantitative + threshold comparison

---

### 7. Causal Lens ← CausalDimension

**Dimension Purpose**: Analyze cause-effect relationships, dependencies, and implications.

**Lens Perception Mode**:
- **Noticing**: "This is blocked by the API changes"
- **Remembering**: "Last time this caused a cascade"
- **Anticipating**: "Completing this will unblock three others"

**Existing Capabilities**:
- `get_dependencies()` - What this needs
- `get_dependents()` - What needs this
- `analyze_impact()` - Downstream effects

**Lens Extension Needed**:
```python
class CausalLens(Lens):
    dimension: CausalDimension

    def perceive_blockers(self, target: EntityProtocol) -> Perception:
        """What is preventing progress?"""
        ...

    def perceive_impact(self, target: EntityProtocol) -> Perception:
        """What will happen if this completes/fails?"""
        ...
```

**Example Queries Using This Lens**:
- "What's blocking this?" → Causal (dependency lookup)
- "What will this unblock?" → Causal (dependent lookup)
- "What's the critical path?" → Causal + Priority (compound)

---

### 8. Contextual Lens ← ContextualDimension

**Dimension Purpose**: Analyze relevance to current situation, surrounding context.

**Lens Perception Mode**:
- **Noticing**: "This is relevant to what you're working on"
- **Remembering**: "You looked at related things yesterday"
- **Anticipating**: "This will become relevant when you start the next epic"

**Existing Capabilities**:
- `analyze_relevance()` - How relevant to current focus
- `get_related_items()` - Contextually similar things
- `calculate_context_score()` - Fit to current situation

**Lens Extension Needed**:
```python
class ContextualLens(Lens):
    dimension: ContextualDimension

    def perceive_relevance(self, target: EntityProtocol, situation: SituationContext) -> Perception:
        """How relevant is this to the current situation?"""
        ...

    def perceive_surroundings(self, target: EntityProtocol) -> Perception:
        """What is around this? What is this near?"""
        ...
```

**Example Queries Using This Lens**:
- "What's relevant to this issue?" → Contextual (relevance)
- "Show me related PRs" → Contextual (similarity)
- "What should I focus on?" → Contextual + Priority (compound)

---

## Compound Lens Patterns

Most real queries use multiple lenses together:

| Query | Primary Lens | Secondary Lens(es) | Perception Mode |
|-------|-------------|-------------------|-----------------|
| "What's on my agenda today?" | Temporal | Contextual | Noticing |
| "Show me stale PRs" | Flow | Temporal, Priority | Noticing |
| "What needs attention?" | Priority | Collaborative, Temporal | Noticing |
| "Who's overloaded?" | Collaborative | Quantitative | Noticing |
| "What will this unblock?" | Causal | Priority | Anticipating |
| "What did we decide last week?" | Temporal | Collaborative | Remembering |
| "Is this project on track?" | Flow | Quantitative, Temporal | Noticing |

---

## Implementation Pattern

### Lens Base Class

```python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from enum import Enum

class PerceptionMode(Enum):
    NOTICING = "noticing"      # Current state
    REMEMBERING = "remembering" # Historical state
    ANTICIPATING = "anticipating" # Future state

class Perception:
    """The result of perceiving through a lens."""
    lens_name: str
    mode: PerceptionMode
    raw_data: Dict[str, Any]  # From spatial dimension
    observation: str  # Human-readable framing
    confidence: float

class Lens(ABC, Generic[DimensionType]):
    """
    A perceptual lens wraps a spatial dimension with consciousness framing.

    Dimensions provide the technical analysis.
    Lenses provide the experiential framing.
    """
    name: str
    dimension: DimensionType

    @abstractmethod
    def perceive(
        self,
        target: Union[EntityProtocol, MomentProtocol, PlaceProtocol],
        mode: PerceptionMode = PerceptionMode.NOTICING
    ) -> Perception:
        """Apply this lens to perceive a target."""
        ...

    def _frame_as_experience(self, raw_data: Dict, mode: PerceptionMode) -> str:
        """
        Transform technical data into experience language.

        "Found 3 items" → "I notice three things..."
        """
        ...
```

### LensSet for Compound Perception

```python
class LensSet:
    """Apply multiple lenses for compound perception."""

    def __init__(self, lenses: List[Lens]):
        self.lenses = {lens.name: lens for lens in lenses}

    def perceive_through(
        self,
        lens_names: List[str],
        target: Union[EntityProtocol, MomentProtocol, PlaceProtocol],
        mode: PerceptionMode = PerceptionMode.NOTICING
    ) -> List[Perception]:
        """Apply multiple lenses to build compound perception."""
        return [
            self.lenses[name].perceive(target, mode)
            for name in lens_names
            if name in self.lenses
        ]

    def synthesize(self, perceptions: List[Perception]) -> str:
        """Combine multiple perceptions into coherent observation."""
        ...
```

---

## Migration Path

### Phase 1: Wrapper Layer
Create `Lens` classes that wrap existing spatial dimensions without modifying them.

### Phase 2: Experience Framing
Add `_frame_as_experience()` methods that transform technical output into consciousness language.

### Phase 3: Perception Modes
Extend dimensions (where needed) to support remembering and anticipating modes.

### Phase 4: Integration
Connect lens infrastructure to canonical query handlers and response generation.

---

## Verification

After implementation, verify:

- [ ] Each existing spatial dimension has a corresponding Lens wrapper
- [ ] Each Lens can operate in all three perception modes
- [ ] Compound queries can use multiple lenses together
- [ ] Response generation uses lens framing, not raw data framing
- [ ] Morning Standup can be expressed using lens vocabulary

---

## References

- ADR-038: Spatial Intelligence Architecture Patterns
- ADR-055: Object Model (draft)
- Pattern-020: Spatial Metaphor Integration
- `services/spatial/` - Existing dimension implementations

---

*Last Updated: January 19, 2026*
*Author: Chief Architect*
