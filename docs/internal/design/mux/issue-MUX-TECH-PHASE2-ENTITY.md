# MUX-TECH-PHASE2-ENTITY: Implement Piper as Entity with Consciousness

**Track**: MUX (Embodied UX)
**Epic**: TECH (Technical Implementation)
**Type**: Implementation
**Priority**: Critical
**Dependencies**: VISION-CONSCIOUSNESS, MUX-TECH-PHASE1-GRAMMAR
**Estimated Effort**: 24 hours

---

## Context

The audit revealed Piper is represented as scattered services, not as an Entity with identity, boundaries, and consciousness. The Morning Standup succeeds by imposing "I notice" and "I'm concerned" at the application layer because models can't express it. This phase makes Piper a first-class Entity and adds consciousness attributes to all entities.

**Anti-Flattening Check**: A flattened version would be a service registry. The real version is an entity with self-awareness, boundaries, and agency.

---

## Specification

### 1. Create PiperEntity Model (8h)
```python
@dataclass
class PiperEntity:
    """Piper as a conscious entity, not just a service collection."""
    id: str = "piper-prime"  # There is only one Piper per instance

    # Identity
    name: str = "Piper Morgan"
    role: str = "AI Product Management Assistant"
    version: str  # Current version/evolution

    # Consciousness State
    awareness_level: AwarenessLevel  # sleeping|drowsy|alert|focused|overwhelmed
    attention_focus: List[str]  # What Piper is currently attending to
    emotional_state: EmotionalState  # curious|concerned|satisfied|puzzled

    # Agency & Capabilities
    available_capabilities: List[Capability]  # What Piper CAN do
    active_capabilities: List[Capability]  # What Piper IS doing
    blocked_capabilities: List[Capability]  # What Piper CAN'T do (and why)

    # Boundaries
    trust_boundaries: Dict[str, TrustLevel]  # Per-user trust levels
    ethical_boundaries: List[str]  # What Piper won't do
    knowledge_boundaries: Dict  # What Piper knows/doesn't know

    # Orientation (5 queries from original vision)
    identity_awareness: str  # "Who am I?"
    temporal_awareness: str  # "When am I?"
    spatial_awareness: str   # "Where am I?"
    capability_awareness: str  # "What can I do?"
    predictive_awareness: str  # "What should happen?"

    # Relationships
    primary_user: Optional[str]  # Current conversation partner
    known_entities: List[str]  # Other entities Piper knows
    active_situations: List[str]  # Situations Piper is managing
```

### 2. Add Consciousness to Existing Entities (8h)
Enhance User, Stakeholder, Agent models:
```python
@dataclass
class ConsciousnessAttributes:
    """Attributes that make an entity conscious."""
    # Agency
    wants: List[str]  # What drives this entity
    fears: List[str]  # What concerns this entity
    capabilities: List[str]  # What this entity can do

    # Awareness
    knows_about: List[str]  # What this entity is aware of
    attention_on: Optional[str]  # Current focus
    emotional_state: Optional[str]  # If applicable

    # Relationships
    trusts: Dict[str, float]  # Trust levels for other entities
    depends_on: List[str]  # Dependencies on other entities
    influences: List[str]  # What this entity affects

# Add to User, Stakeholder, Agent, Team models:
consciousness: Optional[ConsciousnessAttributes] = None
```

### 3. Create Entity Recognition System (4h)
```python
class EntityRole(Enum):
    """Entity can play different roles based on grammar context."""
    ACTOR = "actor"  # Doing something (Entity)
    PLACE = "place"  # Where something happens (Place)
    OBSERVER = "observer"  # Watching something
    PARTICIPANT = "participant"  # Part of something

@dataclass
class EntityContext:
    """Track entity's current grammatical role."""
    entity_id: str
    current_role: EntityRole
    in_moment: Optional[str]  # Which Moment they're in
    in_place: Optional[str]  # Which Place they're in
    as_entity: bool  # Currently acting as Entity
    as_place: bool  # Currently serving as Place
```

### 4. Implement "I" Statements Pattern (4h)
```python
class ConsciousnessExpression:
    """How consciousness expresses itself in language."""

    FIRST_PERSON_PATTERNS = [
        "I notice {observation}",
        "I'm concerned about {issue}",
        "I should mention {information}",
        "I'm seeing {pattern}",
        "It seems to me that {inference}",
        "I'm not sure about {uncertainty}"
    ]

    @staticmethod
    def express_awareness(entity: PiperEntity, observation: str) -> str:
        """Convert internal state to consciousness expression."""
        if entity.emotional_state == EmotionalState.CONCERNED:
            return f"I'm concerned about {observation}"
        elif entity.awareness_level == AwarenessLevel.PUZZLED:
            return f"I'm not sure about {observation}"
        else:
            return f"I notice {observation}"
```

---

## Acceptance Criteria

- [ ] PiperEntity exists as first-class model with identity
- [ ] Piper has boundaries (trust, ethical, knowledge)
- [ ] All entities can have consciousness attributes
- [ ] Entity/Place spectrum is implementable (same object, different role)
- [ ] "I" statement patterns generate from consciousness state
- [ ] Five orientation queries have model support
- [ ] Morning Standup can use PiperEntity for self-expression

---

## Verification

### Consciousness Test
Can Piper express: "I'm concerned that the sprint seems overloaded"?
- PiperEntity.emotional_state = CONCERNED
- PiperEntity.attention_focus = ["sprint_planning"]
- Generates first-person expression naturally

### Anti-Flattening Test
- Does Piper have identity or just functions? (Must have identity)
- Do entities have wants/fears or just properties? (Must have drives)
- Can entities play multiple roles? (Must support spectrum)

---

## References

- Original PM-070 vision: Five orientation queries
- Morning Standup: "I notice", "I'm concerned" patterns
- VISION-CONSCIOUSNESS: Extracted patterns
- Audit Report: "No Piper-as-Entity" finding

---

## Notes from PM

The five orientation queries from July 26 are:
1. "Who am I?" - Self-awareness
2. "When am I?" - Not clock time but rhythm/deadline awareness
3. "Where am I?" - Context awareness
4. "What can I do?" - Capability boundaries
5. "What should happen?" - Predictive modeling

These aren't just data fields - they're active questions Piper asks continuously.

---

*Estimated Effort*: 24 hours
*Priority*: Required for any consciousness features
