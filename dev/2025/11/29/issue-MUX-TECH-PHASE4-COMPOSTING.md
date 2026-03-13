# MUX-TECH-PHASE4-COMPOSTING: Implement Composting to Learning Pipeline

**Track**: MUX (Embodied UX)
**Epic**: TECH (Technical Implementation)
**Type**: Implementation
**Priority**: High
**Dependencies**: MUX-TECH-PHASE1-GRAMMAR, MUX-VISION-LEARNING-UX
**Estimated Effort**: 12 hours

---

## Context

The audit found no lifecycle transformation - objects are deleted, not composted. The 8-stage lifecycle ends in "Composted" where deprecated objects decompose into learnings that feed new Emergent objects. This creates Piper's learning system, connecting to the "filing dreams" metaphor from UX design. Without this, Piper can't learn from experience.

**Anti-Flattening Check**: A flattened version would be an audit log. The real version is organic decomposition where experience becomes wisdom.

---

## Specification

### 1. Implement Composting Mechanics (4h)
```python
@dataclass
class CompostingEvent:
    """When an object decomposes into learnings."""
    id: str
    source_object_id: str
    source_object_type: str

    # What triggers composting
    trigger: CompostingTrigger  # age|irrelevance|manual|scheduled
    triggered_at: datetime

    # Decomposition process
    decomposition_method: str  # How we extract learnings
    extracted_patterns: List[Pattern]
    extracted_insights: List[Insight]
    extracted_corrections: List[Correction]

    # The delta that creates learning
    goal_outcome_delta: Dict  # What was intended vs what happened
    confidence_score: float  # How sure are we about these learnings

    # Where learnings go
    fed_to_insight_journal: List[str]  # Journal entry IDs
    created_emergent_objects: List[str]  # New objects spawned

class CompostingTrigger(Enum):
    AGE = "age"  # Object is old enough
    IRRELEVANCE = "irrelevance"  # No longer referenced
    MANUAL = "manual"  # User triggered
    SCHEDULED = "scheduled"  # During "rest" periods
    CONTRADICTION = "contradiction"  # New info invalidates

@dataclass
class CompostBin:
    """Staging area for objects ready to decompose."""
    id: str = "compost-bin"

    # Objects awaiting composting
    pending: List[Tuple[Any, CompostingTrigger]]

    # Processing state
    is_composting: bool = False  # "Filing dreams" in progress
    last_composted: Optional[datetime] = None
    next_scheduled: Optional[datetime] = None

    # Thresholds
    min_age_days: int = 30  # How old before composting
    max_pending: int = 100  # Trigger if this many waiting
    quiet_hours: List[int] = [2, 3, 4, 5]  # When to "dream"
```

### 2. Create Learning Extraction (4h)
```python
@dataclass
class ExtractedLearning:
    """What Piper learns from composted objects."""
    id: str
    source_objects: List[str]  # What was composted

    # Types of learning
    pattern: Optional[Pattern] = None
    insight: Optional[Insight] = None
    correction: Optional[Correction] = None
    preference: Optional[Preference] = None

    # Confidence and relevance
    confidence: float  # How sure about this learning
    relevance_score: float  # How important right now
    applies_to_entities: List[str]  # Who this learning is about

    # Integration
    creates_rule: bool = False  # Should this become a rule?
    modifies_behavior: bool = False  # Should this change how Piper acts?
    requires_confirmation: bool = True  # Should user verify?

@dataclass
class Pattern:
    """Recurring structure noticed across objects."""
    description: str
    occurrences: List[str]  # Where pattern was seen
    frequency: float  # How often it appears
    predictive_power: float  # How well it predicts

@dataclass
class Insight:
    """Understanding that emerges from patterns."""
    description: str  # "User prefers morning standups on Monday"
    derived_from_patterns: List[str]
    confidence: float
    surprisingness: float  # How unexpected

@dataclass
class Correction:
    """Learning that invalidates previous understanding."""
    previous_understanding: str
    new_understanding: str
    evidence: List[str]
    confidence: float
```

### 3. Connect to Insight Journal (2h)
```python
@dataclass
class InsightJournalEntry:
    """Entry in Piper's Insight Journal (not Session Journal)."""
    id: str
    created_at: datetime

    # The insight
    learning: ExtractedLearning
    expression: str  # How Piper would say this

    # Surfacing control (from MUX-VISION-LEARNING-UX)
    visibility_level: VisibilityLevel  # pull|passive|push
    trust_level_required: int  # 1-4

    # The "filing dreams" metaphor
    discovered_during: str  # "reflection"|"rest"|"composting"
    framing: str  # "Having had some time to reflect..."

    # User interaction
    user_acknowledged: bool = False
    user_corrected: Optional[str] = None
    user_confirmed: bool = False

class InsightJournal:
    """Piper's collection of learnings (vs Session Journal for audit)."""

    def add_from_composting(self, learning: ExtractedLearning):
        """Add learning from composting process."""
        entry = InsightJournalEntry(
            id=generate_id(),
            created_at=datetime.now(),
            learning=learning,
            expression=self._express_learning(learning),
            discovered_during="composting",
            framing="Having had some time to reflect, it occurs to me that..."
        )
        self.entries.append(entry)

    def surface_relevant(self, context: Context) -> List[InsightJournalEntry]:
        """Get insights relevant to current context."""
        # Trust gradient aware surfacing
        user_trust = context.user_trust_level
        return [e for e in self.entries
                if e.trust_level_required <= user_trust
                and self._is_relevant(e, context)]
```

### 4. Create Emergent Objects from Learnings (2h)
```python
class EmergentObjectCreator:
    """How composted learnings spawn new objects."""

    def create_from_insight(self, insight: Insight) -> Optional[Any]:
        """Create new Emergent object from an insight."""
        if insight.predictive_power > 0.7:
            # Create a Moment for predicted event
            return Moment(
                id=generate_id(),
                lifecycle_state=LifecycleState(
                    stage=LifecycleStage.EMERGENT,
                    entered_at=datetime.now(),
                    cycle_shape="spiral",  # Learning creates spiral
                    composting_potential={"spawned_from": insight.id}
                )
            )

    def create_from_correction(self, correction: Correction) -> Optional[Any]:
        """Update or create objects based on corrections."""
        # Find objects affected by old understanding
        affected = self.find_affected(correction.previous_understanding)
        for obj in affected:
            obj.lifecycle_state.stage = LifecycleStage.EMERGENT
            obj.metadata["corrected_from"] = correction.id
        return affected
```

---

## Acceptance Criteria

- [ ] 8-stage lifecycle includes COMPOSTED stage
- [ ] CompostBin stages objects for decomposition
- [ ] Extraction produces Patterns, Insights, Corrections
- [ ] Learnings feed to Insight Journal (not Session Journal)
- [ ] "Filing dreams" metaphor in quiet periods
- [ ] Composted learnings can create new Emergent objects
- [ ] Trust gradient controls learning visibility

---

## Verification

### Composting Test
Given a deprecated sprint plan that failed:
1. Can it move to COMPOSTED stage?
2. Does it extract the goal-outcome delta?
3. Does learning appear in Insight Journal?
4. Can it spawn new Emergent planning approach?

### Anti-Flattening Test
- Is composting transformation or deletion? (Must transform)
- Do learnings create new objects or just records? (Must create)
- Is it "filing dreams" or data processing? (Must feel organic)

---

## References

- Object Model Brief v2: 8-stage lifecycle with composting
- MUX-VISION-LEARNING-UX: "Filing dreams" metaphor, trust gradient
- Audit Report: "No transformation, only deletion" finding
- CXO session: "Having had some time to reflect..." language

---

## Notes from PM

Composting is how Piper's experience becomes wisdom. The "filing dreams" metaphor is intentional - this happens during rest, not constantly.

Key insight from CXO: "Having had some time to reflect..." is better than "while you were away" because it doesn't imply surveillance.

The cycle is: Experience → Deprecation → Composting → Learning → New Emergent → Experience

This is how Piper gets smarter without being creepy.

---

*Estimated Effort*: 12 hours
*Priority*: Enables learning system and continuous improvement
