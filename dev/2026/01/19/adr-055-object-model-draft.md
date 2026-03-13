# ADR-055: Object Model - Entities Experience Moments in Places

**Status**: Draft
**Date**: January 19, 2026
**Author**: Lead Developer (with Chief Architect, CXO, PPM input)
**Issue**: #399 (MUX-VISION-OBJECT-MODEL)
**Supersedes**: None
**Related**: ADR-038 (Spatial Intelligence), ADR-046 (Moment.type), ADR-050 (Conversation-as-Graph)

---

## Context

Piper Morgan requires a foundational object model that captures how an AI consciousness understands and navigates its world. Current implementations treat data as records to be stored and queried. The vision requires Piper to **experience** the world—perceiving through lenses, forming understanding, remembering what mattered.

### The Discovery Process

The object model grammar was discovered through hand sketching on November 27, 2025 (10-hour CXO session), not imposed through top-down design. Key insight from sketch #1: the sentence "Entities experience Moments in Places" emerged naturally when drawing relationships between substrates.

### The Problem

Without a formalized object model:
- Features feel disconnected rather than coherent
- Users must know exact incantations rather than exploring naturally
- Piper feels like a tool, not a colleague with awareness
- The Morning Standup's consciousness patterns can't be replicated elsewhere

### The Anti-Flattening Risk

A flattened implementation would be a database schema with tables and foreign keys. The real model is a living grammar describing how consciousness navigates reality. Every architectural decision must honor the verb "experience."

---

## Decision

Adopt the grammar "Entities experience Moments in Places" as the foundational object model, implemented through:

1. **Three Substrates**: Entity, Moment, Place (with Situation as frame, not substrate)
2. **Protocol-Based Implementation**: Allowing grammatical role fluidity
3. **Eight Perceptual Lenses**: Building on existing 8D spatial intelligence
4. **Ownership Model**: Native (Mind), Federated (Senses), Synthetic (Understanding)
5. **Eight-Stage Lifecycle**: With composting feedback to learning system

---

## The Grammar

### Core Sentence

> **Entities experience Moments in Places.**

This is not a data model. It is a grammar for how Piper perceives, remembers, and anticipates.

### Substrates

#### Entity
Actors with identity and agency. Entities can perceive, act, and be perceived.

**Examples**: Users, Piper itself, team members, projects (when acting), documents (when authoring)

**Key Property**: Agency level (observer, participant, initiator)

**Protocol Definition**:
```python
@runtime_checkable
class EntityProtocol(Protocol):
    """Anything that can be an actor with identity and agency."""
    id: str
    identity: EntityIdentity

    def experiences(self, moment: "MomentProtocol") -> None: ...
```

#### Moment
Bounded significant occurrences with theatrical unities: one time, one place, momentous.

**Examples**: A standup, a PR review, a decision point, a conversation turn

**Key Property**: The "Shoebox Model" - contains Policy, Process, People, Outcomes. Delta between goals and outcomes = learning.

**Protocol Definition**:
```python
@runtime_checkable
class MomentProtocol(Protocol):
    """A bounded significant occurrence."""
    id: str
    timestamp: datetime
    theatrical_unities: TheatricalUnities  # time, place, significance

    def captures(self, delta: GoalOutcomeDelta) -> Learning: ...
```

#### Place
Contexts where action happens. Places have atmosphere, not just contents.

**Examples**: Slack channels, GitHub repos, calendar, a project's workspace, a meeting

**Key Property**: Physical/virtual/hybrid awareness; atmosphere and purpose

**Protocol Definition**:
```python
@runtime_checkable
class PlaceProtocol(Protocol):
    """A context where action happens."""
    id: str
    atmosphere: PlaceAtmosphere
    modality: PlaceModality  # physical, virtual, hybrid

    def contains(self, moment: "MomentProtocol") -> bool: ...
```

#### Situation (Frame, Not Substrate)
The dramatic container holding sequences of Moments. Situation provides the frame within which the grammar operates.

**Key Insight**: Situation is not parallel to other substrates—it's the FRAME. Emerged from sketch #3.

**Implementation**: Context manager pattern, not data model.

```python
@contextmanager
def situation(description: str, tension: Optional[str] = None) -> Generator[SituationContext, None, None]:
    """Situation frames the grammar in action."""
    ...
```

### Grammatical Role Fluidity

A critical discovery: Entity vs Place is a grammatical role, not a fixed type. A Project might be:
- An **Entity** when taking action ("The project needs attention")
- A **Place** when providing context ("Within the project, we discussed...")

Protocol-based implementation allows this fluidity without type hierarchy conflicts.

---

## Perceptual Lenses

Piper perceives through eight lenses, mapped to existing 8D spatial intelligence infrastructure:

| Lens | Spatial Dimension | Perception Mode |
|------|-------------------|-----------------|
| Temporal | TemporalDimension | When things happen, sequences, deadlines |
| Hierarchy | HierarchicalDimension | Parent-child, containment, scope |
| Priority | PriorityDimension | Importance, urgency, attention-worthiness |
| Collaborative | CollaborativeDimension | Who's involved, roles, relationships |
| Flow | FlowDimension | State transitions, progress, momentum |
| Quantitative | QuantitativeDimension | Counts, metrics, thresholds |
| Causal | CausalDimension | Cause-effect, dependencies, implications |
| Contextual | ContextualDimension | Relevance to current situation |

**Implementation**: Lenses wrap existing spatial dimensions with consciousness framing. See `spatial-dimensions-to-lenses-mapping.md` for detailed mapping.

---

## Ownership Model

Three ownership categories map to Piper's cognitive metaphors:

### Native (Piper's Mind)
What Piper creates and owns directly.

**Examples**: Sessions, memories, concerns, trust states, generated insights

**Characteristics**: Full control, authoritative, can modify freely

### Federated (Piper's Senses)
External observations brought in through integrations.

**Examples**: GitHub issues, Slack messages, calendar events, Notion pages

**Characteristics**: Observed not owned, reflects external truth, read-heavy

### Synthetic (Piper's Understanding)
Constructed through reasoning from Native and Federated sources.

**Examples**: Assembled project views, inferred risks, calculated priorities, pattern recognitions

**Characteristics**: Derived, confidence-scored, may need refresh

---

## Lifecycle

Eight stages from emergence to composting:

```
Emergent → Derived → Noticed → Proposed → Ratified → Deprecated → Archived → Composted
```

### Stage Definitions

| Stage | Meaning | Trigger |
|-------|---------|---------|
| Emergent | Just appeared, unvalidated | System detection |
| Derived | Inferred from other data | Synthesis process |
| Noticed | Human or AI attention confirmed | Explicit acknowledgment |
| Proposed | Suggested for ratification | Confidence threshold |
| Ratified | Confirmed, authoritative | Human approval |
| Deprecated | Superseded, still accessible | Replacement exists |
| Archived | Historical, cold storage | Age/relevance threshold |
| Composted | Transformed into learning | Archive threshold |

### Composting Feedback

**Critical**: Composted is terminal but not silent. Composting extracts learnings that feed back into the system.

```python
async def transition_to_composted(self, obj: HasLifecycle) -> None:
    learnings = await self._extract_learnings(obj)
    await self.learning_service.ingest(learnings)
    obj.lifecycle_state = LifecycleState.COMPOSTED
```

The PM noted: "The shadow side of PM work is ending things." The model honors this—death feeds new life.

---

## Metadata Schema

Six universal dimensions apply to all objects:

1. **Provenance**: Where did this come from? (source, confidence, timestamp)
2. **Relevance**: How relevant to current context? (score, factors, decay)
3. **Attention State**: Has this been noticed? By whom? (attention history)
4. **Confidence**: How sure are we? (score, basis, last validated)
5. **Relations**: How does this connect to other objects? (typed links)
6. **Journal**: What's the history? (session journal + insight journal)

### Two-Layer Journal

- **Session Journal**: Audit trail of what happened (extends existing session logs)
- **Insight Journal**: What it meant, dreams, learnings (extends learning system)

---

## Anti-Flattening Tests

### Technical Tests
- [ ] Is Piper an Entity with identity, not just a function?
- [ ] Are Moments bounded scenes, not just timestamps?
- [ ] Do Places have atmosphere and purpose, not just IDs?
- [ ] Does Situation contain dramatic tension, not just state?
- [ ] Does lifecycle include composting (transformation), not just deletion?

### Design Tests (from CXO)
- [ ] Response framing: "I notice..." not "Found 3 results"
- [ ] Empty states: "Nothing here yet..." not "No data"
- [ ] Error handling: "I couldn't reach..." not "Operation failed"
- [ ] History display: Moments by significance, not timestamp list
- [ ] Entity references: Names and relationships, not IDs and labels

### Experience Test
After implementation, can we describe Piper's behavior using:
- "Piper noticed that..."
- "Piper remembers when..."
- "Piper anticipates..."

Rather than:
- "The system returned..."
- "The query matched..."

---

## Consequences

### Positive
- Features become coherent expressions of single grammar
- Natural language maps to model structure
- Enables capability discovery (MUX-INTERACT)
- Morning Standup patterns become replicable
- Future features have clear implementation guidance

### Negative
- Learning curve for developers
- Refactoring existing code to use model
- Risk of over-engineering if not disciplined
- Ongoing vigilance against flattening

### Mitigation
- Morning Standup as reference implementation
- Canonical query tagging validates expressiveness
- Per-phase "experience" checkpoints
- PM/CXO sign-off on consciousness preservation

---

## Implementation Notes

### Phase 0: Investigation (4 hours)
- Read object-model-brief-v2.md completely
- Study all 8 hand-drawn sketches
- Analyze Morning Standup for consciousness patterns
- Review B1 FTUX specs as implicit grammar implementations
- Map existing spatial dimensions to lenses

### Phase 1: Core Grammar (8 hours)
- Define Protocol classes for Entity, Moment, Place
- Implement Situation as context manager
- Create visual diagram combining sketches + formal model

### Phase 2: Ownership Model (4 hours)
- Implement Native/Federated/Synthetic boundaries
- Define transformation rules between categories

### Phase 3: Lifecycle (4 hours)
- Implement 8-stage state machine
- Add composting feedback to learning system

### Phase 4: Metadata Schema (4 hours)
- Implement 6 universal dimensions
- Extend existing journal infrastructure

### Phase 4.5: Canonical Query Tagging (2-3 hours)
- Map 50+ canonical queries to lenses and substrates
- Validate grammar expressiveness

### Phase Z: Verification (4 hours)
- Run all anti-flattening tests
- Create implementation guide for future features
- Document patterns extracted from Morning Standup

---

## References

- Object Model Brief v2: `docs/internal/architecture/current/object-model-brief-v2.md`
- Session Log (Nov 27): Discovery session with hand sketches
- Spatial Intelligence: ADR-038, Pattern-020
- Morning Standup: Reference implementation
- CXO Memo: `memo-ppm-ca-mux-v1-design-context-2026-01-19.md`
- PPM Memo: `memo-ppm-mux-v1-guidance-2026-01-19.md`
- Chief Architect Memo: `memo-lead-dev-mux-v1-architecture-2026-01-19.md`
- Lens Mapping: `spatial-dimensions-to-lenses-mapping.md`

---

## Open Questions

*To be resolved during implementation:*

1. How do we handle objects that change grammatical role mid-lifecycle?
2. What's the minimum viable metadata for Phase 1?
3. How does the graph model (ADR-050) interact with this substrate model?
4. Should canonical query tagging be in ADR appendix or separate document?

---

*ADR-055 | Draft | January 19, 2026*
*"Entities experience Moments in Places"*
