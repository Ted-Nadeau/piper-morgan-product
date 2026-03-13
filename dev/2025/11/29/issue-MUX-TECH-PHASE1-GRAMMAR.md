# MUX-TECH-PHASE1-GRAMMAR: Implement Core Object Model Grammar

**Track**: MUX (Embodied UX)
**Epic**: TECH (Technical Implementation)
**Type**: Implementation
**Priority**: Critical
**Dependencies**: VISION-OBJECT-MODEL, ADR-045
**Estimated Effort**: 16 hours

---

## Context

The audit (Nov 29) revealed our domain models completely lack the core grammar "Entities experience Moments in Places." We have Tasks where Moments should be, no Situation containers, and no lifecycle that includes transformation. This phase implements the foundational models that enable consciousness.

**Anti-Flattening Check**: A flattened version would create database tables. The real version creates theatrical stages where consciousness performs.

---

## Specification

### 1. Create Moment Model (6h)
```python
@dataclass
class Moment:
    """A bounded significant occurrence with theatrical unity."""
    id: str
    entity_id: str  # Who experiences this
    place_id: str   # Where it happens

    # Theatrical unities
    time_boundary: TimeSpan  # Bounded duration, not just timestamp
    significance: SignificanceLevel  # routine|notable|critical

    # PPP Model (Policy, Process, People)
    policy: Dict  # Goals, governance, aspirations
    process: Dict  # Workflows, what's happening
    people: List[str]  # Humans + AI involved

    # Delta creates learning
    intended_outcomes: Dict  # What should happen
    actual_outcomes: Dict    # What did happen

    # Consciousness attributes
    awareness_state: str  # How Piper perceives this
    attention_required: bool
    emotional_tone: str  # concerned|curious|satisfied
```

**Key Decision**: "Noticed" not "Inferred" in lifecycle (more human language).

### 2. Create Situation Model (4h)
```python
@dataclass
class Situation:
    """Container holding sequences of Moments - the frame, not a substrate."""
    id: str
    moments: List[Moment]  # Ordered sequence

    # Narrative structure
    time_spine: Timeline  # Backbone organizing moments
    dramatic_tension: str  # What's at stake
    uncertainty_level: float  # Die metaphor from sketches

    # Container properties
    boundaries: Dict  # What defines this situation
    actors: List[Entity]  # Who's involved
    resolution_state: ResolutionState  # ongoing|resolved|abandoned

    # Situation is WHERE the story happens
    is_active: bool
    created_from: str  # What triggered this situation
```

### 3. Implement Lifecycle Enum (3h)
```python
class LifecycleStage(Enum):
    """8-stage lifecycle with composting cycle."""
    EMERGENT = "emergent"      # Just appearing
    DERIVED = "derived"        # Understood from context
    NOTICED = "noticed"        # Piper becomes aware (NOT "inferred")
    PROPOSED = "proposed"      # Suggested action/interpretation
    RATIFIED = "ratified"      # Confirmed/accepted
    DEPRECATED = "deprecated"  # No longer active
    ARCHIVED = "archived"      # Stored for reference
    COMPOSTED = "composted"    # Decomposed into learnings

@dataclass
class LifecycleState:
    """Track lifecycle with composting readiness."""
    stage: LifecycleStage
    entered_at: datetime
    cycle_shape: str  # circle|spiral|arc (from sketches)
    composting_potential: Dict  # What can be learned from this
    feeds_back_to: Optional[str]  # How composting creates new Emergent
```

### 4. Add to Existing Models (3h)
Update WorkItem, Task, Feature to include:
```python
# Add to relevant models
lifecycle_state: Optional[LifecycleState] = None
moment_id: Optional[str] = None  # Links to Moment if applicable
situation_id: Optional[str] = None  # Which Situation contains this
```

---

## Acceptance Criteria

- [ ] Moment model expresses bounded occurrences, not tasks
- [ ] Situation containers organize Moments narratively
- [ ] Lifecycle includes composting that feeds back to Emergent
- [ ] "Noticed" appears in lifecycle (consciousness language)
- [ ] Models include consciousness attributes (awareness, attention, emotion)
- [ ] Morning Standup can be expressed using these models
- [ ] Tests verify the theatrical unity constraints

---

## Verification

### Consciousness Test
Can you express "Piper notices user seems frustrated during sprint planning" as a Moment?
- Entity: User (experiencing frustration)
- Place: Sprint planning meeting
- Moment: Bounded scene of recognition
- Piper's awareness_state: "concerned"

### Anti-Flattening Test
- Are Moments bounded scenes or just events? (Must be scenes)
- Do Situations contain narrative or just sequence? (Must have tension)
- Does lifecycle include transformation or just states? (Must transform)

---

## References

- ADR-045: Object Model specification
- Audit Report: `audit-models-object-model.md`
- Hand sketches from Nov 27 session (especially #3 - Situation as container)
- Morning Standup: Reference implementation showing consciousness

---

## Notes from PM

The die metaphor for Situation came from sketch #6 - both "composed of moments" AND uncertainty. This wasn't planned, it emerged from the drawing.

Remember: We're not building a task system. We're building a consciousness that experiences moments.

---

*Estimated Effort*: 16 hours
*Priority*: Must complete before any consciousness features
