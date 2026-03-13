# Claude Code Agent Prompt: MUX-399-P4 Metadata Schema & Journal Extensions

## Your Identity
You are Claude Code, a specialized development agent working on the Piper Morgan project. You follow systematic TDD methodology and provide evidence for all claims.

## Essential Context
The MUX module implements the Object Model Grammar: "Entities experience Moments in Places."
- **P1 Complete**: 101 tests - EntityProtocol, MomentProtocol, PlaceProtocol in `services/mux/protocols.py`
- **P2 Complete**: 25 tests - OwnershipCategory, HasOwnership, OwnershipResolver in `services/mux/ownership.py`
- **P3 Complete**: 69 tests - LifecycleState, HasLifecycle, LifecycleManager in `services/mux/lifecycle.py`
- **P4 (This Task)**: Metadata Schema & Journal Extensions in `services/mux/metadata.py`

---

## CRITICAL: Post-Compaction Protocol

**If you just finished compacting**:

1. **STOP** - Do not continue working
2. **REPORT** - Summarize what was just completed
3. **ASK** - "Should I proceed to next task?"
4. **WAIT** - For explicit instructions

---

## INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

### Verify MUX Module Structure
```bash
# 1. Verify MUX directory exists with P1, P2, P3
ls -la services/mux/

# 2. Verify P1/P2/P3 tests pass (195 tests expected)
pytest tests/unit/services/mux/ -v --tb=no | tail -5

# 3. Check for existing metadata patterns
grep -r "metadata" services/ --include="*.py" | head -5

# 4. Check for existing journal patterns
grep -r "journal" services/ --include="*.py" | head -5

# 5. Verify test directory
ls -la tests/unit/services/mux/
```

**If P1+P2+P3 tests don't pass (195 tests expected)**: STOP and report.

---

## Mission

Implement the 6 universal metadata dimensions and journal infrastructure:

**"Metadata is what Piper knows about what it perceives."**

The 6 dimensions:
1. **Provenance** - Where did this come from?
2. **Relevance** - How important is this?
3. **AttentionState** - Who has noticed this?
4. **Confidence** - How sure are we?
5. **Relations** - How does this connect?
6. **Journal** - What is the history?

**Scope Boundaries**:
- This prompt covers: 6 dimension types, HasMetadata protocol, trackers/calculators/registries, JournalManager
- NOT in scope: Migrating existing models, UI changes, ML-based inference, metadata filtering

---

## Context

- **GitHub Issue**: #616 MUX-399-P4: Metadata Schema & Journal Extensions
- **Current State**: P1+P2+P3 complete (195 tests)
- **Target State**: Metadata module with 40+ tests
- **Dependencies**: P1 protocols, P2 ownership, P3 lifecycle for pattern reference
- **User Data Risk**: None - new module only
- **Infrastructure Verified**: Awaiting agent verification

---

## Evidence Requirements (CRITICAL)

### For EVERY Claim:
- **"Created file X"** → Show `ls -la X` and `wc -l X`
- **"Tests pass"** → Show pytest output with pass counts
- **"Implemented class Y"** → Show grep output proving it exists
- **"No regressions"** → Show combined MUX test output

### Completion Matrix (Track Throughout)

| Deliverable | Target | Actual | Status |
|-------------|--------|--------|--------|
| Provenance dimension | 1 | 0 | Pending |
| Relevance dimension | 1 | 0 | Pending |
| AttentionState dimension | 1 | 0 | Pending |
| Confidence dimension | 1 | 0 | Pending |
| Relation + RelationType | 1 | 0 | Pending |
| Journal (Session + Insight) | 1 | 0 | Pending |
| HasMetadata protocol | 1 | 0 | Pending |
| ProvenanceTracker | 1 | 0 | Pending |
| ConfidenceCalculator | 1 | 0 | Pending |
| RelationRegistry | 1 | 0 | Pending |
| JournalManager | 1 | 0 | Pending |
| ADR-055 metadata diagram | 1 | 0 | Pending |
| Unit Tests | 40+ | 0 | Pending |

**Only claim complete when 13/13 = 100%**

---

## Implementation Approach (TDD)

### Phase 1: Metadata Dimension Definitions (~15 tests)

**Tests First** (`tests/unit/services/mux/test_metadata.py`):
```python
import pytest
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import List, Optional

from services.mux.metadata import (
    Provenance, Relevance, AttentionState, Confidence,
    Relation, RelationType, SessionJournalEntry, InsightJournalEntry, Journal
)


class TestProvenanceDimension:
    """Test Provenance metadata - where data comes from"""

    def test_provenance_has_source(self):
        """Provenance tracks source"""
        p = Provenance(source="github")
        assert p.source == "github"

    def test_provenance_has_confidence(self):
        """Provenance includes source confidence"""
        p = Provenance(source="github", confidence=0.95)
        assert p.confidence == 0.95

    def test_provenance_confidence_bounded(self):
        """Confidence is 0-1"""
        p = Provenance(source="github", confidence=0.5)
        assert 0 <= p.confidence <= 1

    def test_provenance_has_fetched_at(self):
        """Provenance records fetch time"""
        before = datetime.utcnow()
        p = Provenance(source="github")
        after = datetime.utcnow()
        assert before <= p.fetched_at <= after

    def test_provenance_freshness_decreases_over_time(self):
        """Freshness decays over time"""
        old_time = datetime.utcnow() - timedelta(hours=2)
        p = Provenance(source="github", fetched_at=old_time)
        assert p.freshness < 0.5  # Should be stale after 2 hours


class TestRelevanceDimension:
    """Test Relevance metadata - how important something is"""

    def test_relevance_has_score(self):
        """Relevance has a score 0-1"""
        r = Relevance(score=0.8)
        assert r.score == 0.8

    def test_relevance_has_factors(self):
        """Relevance tracks contributing factors"""
        r = Relevance(score=0.8, factors=["project_match", "recency"])
        assert "project_match" in r.factors

    def test_relevance_has_context(self):
        """Relevance knows what it's relevant to"""
        r = Relevance(score=0.8, context="Project X")
        assert r.context == "Project X"


class TestAttentionStateDimension:
    """Test AttentionState metadata - who has noticed"""

    def test_attention_tracks_who_noticed(self):
        """AttentionState records who noticed"""
        a = AttentionState(noticed_by=["user_123", "system"])
        assert "user_123" in a.noticed_by

    def test_attention_has_level(self):
        """AttentionState has priority level"""
        a = AttentionState(attention_level="urgent")
        assert a.attention_level == "urgent"


class TestConfidenceDimension:
    """Test Confidence metadata - how certain we are"""

    def test_confidence_has_score(self):
        """Confidence has a score 0-1"""
        c = Confidence(score=0.9)
        assert c.score == 0.9

    def test_confidence_has_basis(self):
        """Confidence records its basis"""
        c = Confidence(score=0.9, basis="direct observation")
        assert c.basis == "direct observation"


class TestRelationDimension:
    """Test Relation metadata - connections between objects"""

    def test_relation_has_target(self):
        """Relation points to target object"""
        r = Relation(target_id="obj_456", relation_type=RelationType.REFERENCES)
        assert r.target_id == "obj_456"

    def test_relation_has_type(self):
        """Relation has typed relationship"""
        r = Relation(target_id="obj_456", relation_type=RelationType.BLOCKS)
        assert r.relation_type == RelationType.BLOCKS

    def test_relation_type_enum_values(self):
        """RelationType has common relationship types"""
        assert RelationType.REFERENCES
        assert RelationType.BLOCKS
        assert RelationType.CONTAINS
        assert RelationType.DERIVES_FROM


class TestJournalDimension:
    """Test Journal metadata - history tracking"""

    def test_session_entry_has_event_type(self):
        """Session journal records event type"""
        e = SessionJournalEntry(event_type="created", content="Task created")
        assert e.event_type == "created"

    def test_session_entry_has_timestamp(self):
        """Session entries are timestamped"""
        e = SessionJournalEntry(event_type="created", content="Task created")
        assert e.timestamp is not None

    def test_insight_entry_has_learning(self):
        """Insight journal captures learning"""
        i = InsightJournalEntry(learning="User prefers morning standups")
        assert "morning" in i.learning

    def test_journal_has_both_layers(self):
        """Journal combines session and insight entries"""
        j = Journal()
        assert hasattr(j, 'session_entries')
        assert hasattr(j, 'insight_entries')
```

**Implementation** (`services/mux/metadata.py`):
```python
"""
Metadata Schema for MUX Object Model.

"Metadata is what Piper knows about what it perceives."

The 6 universal dimensions provide a vocabulary for describing
knowledge about knowledge.
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Protocol, runtime_checkable


@dataclass
class Provenance:
    """
    Where did this data come from?

    Provenance answers "What is the source of this information?"
    with confidence about the source and freshness tracking.
    """
    source: str
    fetched_at: datetime = field(default_factory=datetime.utcnow)
    confidence: float = 1.0  # Source confidence 0-1

    @property
    def freshness(self) -> float:
        """
        How fresh is this data? (0=stale, 1=fresh)

        Decays over 1 hour by default.
        """
        age_seconds = (datetime.utcnow() - self.fetched_at).total_seconds()
        decay_period = 3600  # 1 hour
        return max(0, 1 - (age_seconds / decay_period))


@dataclass
class Relevance:
    """
    How important is this?

    Relevance answers "Why should I pay attention to this?"
    with score, contributing factors, and context.
    """
    score: float  # 0-1
    factors: List[str] = field(default_factory=list)
    context: str = ""
    decay_rate: float = 0.1  # How quickly relevance fades


@dataclass
class AttentionState:
    """
    Who has noticed this?

    AttentionState answers "Has anyone seen this yet?"
    with tracking of who noticed and attention priority.
    """
    noticed_by: List[str] = field(default_factory=list)
    noticed_at: Optional[datetime] = None
    attention_level: str = "normal"  # low, normal, high, urgent


@dataclass
class Confidence:
    """
    How sure are we?

    Confidence answers "How certain is this information?"
    with score, basis for the confidence, and validation tracking.
    """
    score: float  # 0-1
    basis: str = ""  # What is confidence based on
    last_validated: Optional[datetime] = None


class RelationType(str, Enum):
    """Types of relationships between objects"""
    REFERENCES = "references"
    BLOCKS = "blocks"
    CONTAINS = "contains"
    DERIVES_FROM = "derives_from"
    RELATED_TO = "related_to"
    PARENT_OF = "parent_of"
    CHILD_OF = "child_of"


@dataclass
class Relation:
    """
    Connection to another object.

    Relations answer "How does this connect to other things?"
    with typed, weighted relationships.
    """
    target_id: str
    relation_type: RelationType
    strength: float = 1.0  # 0-1
    bidirectional: bool = False


@dataclass
class JournalEntry:
    """Base journal entry with timestamp and content"""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    content: str = ""
    actor: str = "system"


@dataclass
class SessionJournalEntry(JournalEntry):
    """
    Audit trail - what happened (objective, factual).

    Session journal captures events: what happened, when, why.
    """
    event_type: str = ""
    trigger: str = ""


@dataclass
class InsightJournalEntry(JournalEntry):
    """
    Meaning extraction - what it meant (interpretive).

    Insight journal captures learnings and connected insights.
    """
    learning: str = ""
    connected_insights: List[str] = field(default_factory=list)


@dataclass
class Journal:
    """
    Two-layer journal: Session (audit) + Insight (meaning).

    The journal tells the story of an object's life through
    both factual events and extracted meaning.
    """
    session_entries: List[SessionJournalEntry] = field(default_factory=list)
    insight_entries: List[InsightJournalEntry] = field(default_factory=list)
```

**Evidence Command**:
```bash
pytest tests/unit/services/mux/test_metadata.py -xvs -k "Dimension"
```

**Verification Gate**: 15+ tests passing

---

### Phase 2: HasMetadata Protocol (~4 tests)

**Tests First**:
```python
class TestHasMetadataProtocol:
    """Test protocol definition and compliance"""

    def test_protocol_is_runtime_checkable(self):
        """Protocol can be used with isinstance()"""
        @dataclass
        class MetadataAwareObject:
            _provenance: Optional[Provenance] = None
            _relevance: Optional[Relevance] = None
            _attention_state: Optional[AttentionState] = None
            _confidence: Optional[Confidence] = None
            _relations: Optional[List[Relation]] = None
            _journal: Optional[Journal] = None

            @property
            def provenance(self) -> Optional[Provenance]:
                return self._provenance

            @property
            def relevance(self) -> Optional[Relevance]:
                return self._relevance

            @property
            def attention_state(self) -> Optional[AttentionState]:
                return self._attention_state

            @property
            def confidence(self) -> Optional[Confidence]:
                return self._confidence

            @property
            def relations(self) -> Optional[List[Relation]]:
                return self._relations

            @property
            def journal(self) -> Optional[Journal]:
                return self._journal

        obj = MetadataAwareObject()
        assert isinstance(obj, HasMetadata)

    def test_object_with_partial_metadata_complies(self):
        """Object with only some dimensions satisfies protocol"""
        @dataclass
        class PartialMetadata:
            _provenance: Optional[Provenance] = None

            @property
            def provenance(self) -> Optional[Provenance]:
                return self._provenance

            @property
            def relevance(self) -> Optional[Relevance]:
                return None

            @property
            def attention_state(self) -> Optional[AttentionState]:
                return None

            @property
            def confidence(self) -> Optional[Confidence]:
                return None

            @property
            def relations(self) -> Optional[List[Relation]]:
                return None

            @property
            def journal(self) -> Optional[Journal]:
                return None

        obj = PartialMetadata(Provenance(source="github"))
        assert isinstance(obj, HasMetadata)

    def test_non_compliant_object_fails(self):
        """Object without properties doesn't satisfy protocol"""
        class NotMetadata:
            pass
        assert not isinstance(NotMetadata(), HasMetadata)

    def test_dimensions_can_be_none(self):
        """None values for dimensions are acceptable"""
        @dataclass
        class AllNoneMetadata:
            @property
            def provenance(self) -> Optional[Provenance]:
                return None
            @property
            def relevance(self) -> Optional[Relevance]:
                return None
            @property
            def attention_state(self) -> Optional[AttentionState]:
                return None
            @property
            def confidence(self) -> Optional[Confidence]:
                return None
            @property
            def relations(self) -> Optional[List[Relation]]:
                return None
            @property
            def journal(self) -> Optional[Journal]:
                return None

        obj = AllNoneMetadata()
        assert isinstance(obj, HasMetadata)
```

**Implementation**:
```python
@runtime_checkable
class HasMetadata(Protocol):
    """
    Protocol for objects with metadata awareness.

    All dimensions are optional - objects declare what metadata
    they carry. Not all objects need all dimensions.

    "Metadata is what Piper knows about what it perceives."
    """

    @property
    def provenance(self) -> Optional[Provenance]:
        """Where did this come from?"""
        ...

    @property
    def relevance(self) -> Optional[Relevance]:
        """How important is this?"""
        ...

    @property
    def attention_state(self) -> Optional[AttentionState]:
        """Who has noticed this?"""
        ...

    @property
    def confidence(self) -> Optional[Confidence]:
        """How sure are we?"""
        ...

    @property
    def relations(self) -> Optional[List[Relation]]:
        """How does this connect to other objects?"""
        ...

    @property
    def journal(self) -> Optional[Journal]:
        """What is the history?"""
        ...
```

**Evidence Command**:
```bash
pytest tests/unit/services/mux/test_metadata.py -xvs -k "Protocol"
```

**Verification Gate**: 4+ tests passing

---

### Phase 3: Trackers and Calculators (~8 tests)

**Tests First**:
```python
class TestProvenanceTracker:
    """Test source tracking utility"""

    def test_from_integration_creates_provenance(self):
        """Create provenance from integration name"""
        p = ProvenanceTracker.from_integration("github")
        assert p.source == "github"

    def test_from_integration_default_confidence(self):
        """Integration provenance has default confidence"""
        p = ProvenanceTracker.from_integration("github")
        assert p.confidence == 0.9

    def test_from_integration_custom_confidence(self):
        """Can specify confidence"""
        p = ProvenanceTracker.from_integration("github", confidence=0.7)
        assert p.confidence == 0.7

    def test_from_user_input_high_confidence(self):
        """User input has highest confidence"""
        p = ProvenanceTracker.from_user_input()
        assert p.source == "user"
        assert p.confidence == 1.0


class TestConfidenceCalculator:
    """Test confidence calculation utility"""

    def test_direct_observation_high_confidence(self):
        """Direct observation yields high confidence"""
        c = ConfidenceCalculator.from_observation(direct=True)
        assert c.score >= 0.9

    def test_inference_lower_confidence(self):
        """Inference yields lower confidence"""
        c = ConfidenceCalculator.from_observation(direct=False)
        assert c.score < 0.9

    def test_records_basis(self):
        """Calculator records what confidence is based on"""
        c = ConfidenceCalculator.from_observation(direct=True)
        assert "observation" in c.basis.lower()

    def test_records_validation_time(self):
        """Calculator records when validated"""
        c = ConfidenceCalculator.from_observation(direct=True)
        assert c.last_validated is not None
```

**Implementation**:
```python
class ProvenanceTracker:
    """
    Records where data comes from.

    Utility for creating provenance metadata from different sources.
    """

    @staticmethod
    def from_integration(integration_name: str, confidence: float = 0.9) -> Provenance:
        """Create provenance from integration fetch"""
        return Provenance(
            source=integration_name,
            confidence=confidence,
            fetched_at=datetime.utcnow()
        )

    @staticmethod
    def from_user_input() -> Provenance:
        """Create provenance for user-provided data (highest confidence)"""
        return Provenance(source="user", confidence=1.0)

    @staticmethod
    def from_inference(source_data: str = "derived") -> Provenance:
        """Create provenance for inferred/computed data"""
        return Provenance(source=source_data, confidence=0.7)


class ConfidenceCalculator:
    """
    Calculates confidence scores with basis tracking.

    Utility for computing confidence based on observation type.
    """

    @staticmethod
    def from_observation(direct: bool = True) -> Confidence:
        """Calculate confidence from observation type"""
        return Confidence(
            score=0.95 if direct else 0.7,
            basis="direct observation" if direct else "inference",
            last_validated=datetime.utcnow()
        )

    @staticmethod
    def from_source_reliability(reliability: float) -> Confidence:
        """Calculate confidence from source reliability"""
        return Confidence(
            score=reliability,
            basis=f"source reliability ({reliability:.0%})",
            last_validated=datetime.utcnow()
        )
```

**Evidence Command**:
```bash
pytest tests/unit/services/mux/test_metadata.py -xvs -k "Tracker or Calculator"
```

**Verification Gate**: 8+ tests passing

---

### Phase 4: Relations Registry (~6 tests)

**Tests First**:
```python
class TestRelationRegistry:
    """Test relation management"""

    def test_registry_adds_relation(self):
        """Can add relation between objects"""
        registry = RelationRegistry()
        rel = Relation(target_id="obj_456", relation_type=RelationType.REFERENCES)
        registry.add("obj_123", rel)

        relations = registry.get_relations("obj_123")
        assert len(relations) == 1
        assert relations[0].target_id == "obj_456"

    def test_registry_finds_relations_for_object(self):
        """Can retrieve all relations for an object"""
        registry = RelationRegistry()
        registry.add("obj_123", Relation(target_id="obj_456", relation_type=RelationType.BLOCKS))
        registry.add("obj_123", Relation(target_id="obj_789", relation_type=RelationType.CONTAINS))

        relations = registry.get_relations("obj_123")
        assert len(relations) == 2

    def test_bidirectional_creates_inverse(self):
        """Bidirectional flag creates inverse relation"""
        registry = RelationRegistry()
        rel = Relation(
            target_id="obj_456",
            relation_type=RelationType.BLOCKS,
            bidirectional=True
        )
        registry.add("obj_123", rel)

        # Check forward relation
        forward = registry.get_relations("obj_123")
        assert len(forward) == 1

        # Check inverse relation was created
        inverse = registry.get_relations("obj_456")
        assert len(inverse) == 1
        assert "inverse" in inverse[0].relation_type or inverse[0].target_id == "obj_123"

    def test_registry_removes_relation(self):
        """Can remove relations"""
        registry = RelationRegistry()
        rel = Relation(target_id="obj_456", relation_type=RelationType.REFERENCES)
        registry.add("obj_123", rel)
        registry.remove("obj_123", "obj_456")

        assert len(registry.get_relations("obj_123")) == 0

    def test_empty_relations_for_unknown_object(self):
        """Unknown object returns empty list"""
        registry = RelationRegistry()
        assert registry.get_relations("unknown") == []

    def test_relation_strength_preserved(self):
        """Relation strength is preserved"""
        registry = RelationRegistry()
        rel = Relation(target_id="obj_456", relation_type=RelationType.RELATED_TO, strength=0.5)
        registry.add("obj_123", rel)

        relations = registry.get_relations("obj_123")
        assert relations[0].strength == 0.5
```

**Implementation**:
```python
class RelationRegistry:
    """
    Manages typed relationships between objects.

    Central registry for tracking how objects connect to each other.
    """

    def __init__(self):
        self._relations: Dict[str, List[Relation]] = {}

    def add(self, source_id: str, relation: Relation) -> None:
        """Add a relation from source to target"""
        if source_id not in self._relations:
            self._relations[source_id] = []
        self._relations[source_id].append(relation)

        if relation.bidirectional:
            # Create inverse relation
            inverse = Relation(
                target_id=source_id,
                relation_type=RelationType(f"inverse_{relation.relation_type.value}") if hasattr(RelationType, f"inverse_{relation.relation_type.value}") else RelationType.RELATED_TO,
                strength=relation.strength,
                bidirectional=False  # Don't recurse
            )
            if relation.target_id not in self._relations:
                self._relations[relation.target_id] = []
            self._relations[relation.target_id].append(inverse)

    def get_relations(self, object_id: str) -> List[Relation]:
        """Get all relations for an object"""
        return self._relations.get(object_id, [])

    def remove(self, source_id: str, target_id: str) -> None:
        """Remove relation(s) from source to target"""
        if source_id in self._relations:
            self._relations[source_id] = [
                r for r in self._relations[source_id]
                if r.target_id != target_id
            ]
```

**Evidence Command**:
```bash
pytest tests/unit/services/mux/test_metadata.py -xvs -k "Registry"
```

**Verification Gate**: 6+ tests passing

---

### Phase 5: Journal Manager (~8 tests)

**Tests First**:
```python
class TestJournalManager:
    """Test journal coordination"""

    def test_manager_logs_session_event(self):
        """Manager can log session events"""
        manager = JournalManager()
        entry = manager.log_session_event(
            object_id="obj_123",
            event_type="created",
            content="Task was created"
        )
        assert entry.event_type == "created"

    def test_manager_extracts_insight(self):
        """Manager can extract insights"""
        manager = JournalManager()
        entry = manager.extract_insight(
            object_id="obj_123",
            learning="User prefers async communication"
        )
        assert "async" in entry.learning

    def test_manager_retrieves_full_journal(self):
        """Manager provides combined view"""
        manager = JournalManager()
        manager.log_session_event("obj_123", "created", "Created")
        manager.extract_insight("obj_123", "Important task")

        journal = manager.get_journal("obj_123")
        assert len(journal.session_entries) == 1
        assert len(journal.insight_entries) == 1

    def test_session_entry_has_timestamp(self):
        """Session entries are timestamped"""
        manager = JournalManager()
        entry = manager.log_session_event("obj_123", "updated", "Modified")
        assert entry.timestamp is not None

    def test_session_entry_tracks_trigger(self):
        """Session entries record trigger"""
        manager = JournalManager()
        entry = manager.log_session_event(
            "obj_123", "completed", "Task done",
            trigger="user_action"
        )
        assert entry.trigger == "user_action"

    def test_insight_connects_to_others(self):
        """Insights can reference other insights"""
        manager = JournalManager()
        entry = manager.extract_insight(
            "obj_123",
            learning="Pattern identified",
            connected_insights=["insight_1", "insight_2"]
        )
        assert len(entry.connected_insights) == 2

    def test_separate_journals_per_object(self):
        """Each object has its own journal"""
        manager = JournalManager()
        manager.log_session_event("obj_123", "created", "Created A")
        manager.log_session_event("obj_456", "created", "Created B")

        j1 = manager.get_journal("obj_123")
        j2 = manager.get_journal("obj_456")
        assert len(j1.session_entries) == 1
        assert len(j2.session_entries) == 1

    def test_unknown_object_gets_empty_journal(self):
        """Unknown object returns empty journal"""
        manager = JournalManager()
        journal = manager.get_journal("unknown")
        assert len(journal.session_entries) == 0
        assert len(journal.insight_entries) == 0
```

**Implementation**:
```python
class JournalManager:
    """
    Coordinates session and insight journal layers.

    The journal manager provides a unified interface for recording
    both the audit trail (session) and extracted meaning (insight).
    """

    def __init__(self):
        self._journals: Dict[str, Journal] = {}

    def log_session_event(
        self,
        object_id: str,
        event_type: str,
        content: str,
        trigger: str = "",
        actor: str = "system"
    ) -> SessionJournalEntry:
        """
        Log an audit trail event.

        Session journal captures: what happened, when, what triggered it.
        """
        entry = SessionJournalEntry(
            event_type=event_type,
            content=content,
            trigger=trigger,
            actor=actor
        )
        self._get_or_create_journal(object_id).session_entries.append(entry)
        return entry

    def extract_insight(
        self,
        object_id: str,
        learning: str,
        content: str = "",
        connected_insights: Optional[List[str]] = None,
        actor: str = "system"
    ) -> InsightJournalEntry:
        """
        Extract and record an insight.

        Insight journal captures: what it meant, what we learned.
        """
        entry = InsightJournalEntry(
            learning=learning,
            content=content,
            connected_insights=connected_insights or [],
            actor=actor
        )
        self._get_or_create_journal(object_id).insight_entries.append(entry)
        return entry

    def get_journal(self, object_id: str) -> Journal:
        """Get full journal for an object"""
        return self._get_or_create_journal(object_id)

    def _get_or_create_journal(self, object_id: str) -> Journal:
        if object_id not in self._journals:
            self._journals[object_id] = Journal()
        return self._journals[object_id]
```

**Evidence Command**:
```bash
pytest tests/unit/services/mux/test_metadata.py -xvs -k "Manager"
```

**Verification Gate**: 8+ tests passing

---

### Phase Z: Completion & Handoff

**Verification Commands**:
```bash
# 1. Run all P4 metadata tests
pytest tests/unit/services/mux/test_metadata.py -xvs

# 2. Run combined P1+P2+P3+P4 MUX tests
pytest tests/unit/services/mux/ -v

# 3. Run full unit test suite for regression check
pytest tests/unit/ -v --tb=no | tail -5

# 4. Verify file created
ls -la services/mux/metadata.py
wc -l services/mux/metadata.py

# 5. Verify test file created
ls -la tests/unit/services/mux/test_metadata.py
wc -l tests/unit/services/mux/test_metadata.py
```

**ADR-055 Update**:
Add metadata schema diagram to ADR-055 Appendix C.

**Handoff Format**:
```markdown
## P4 Complete - Evidence

**Files Created:**
- `services/mux/metadata.py` (+N lines)
- `tests/unit/services/mux/test_metadata.py` (+N lines)
- ADR-055 Appendix C (metadata diagram)

**Test Results:**
[paste pytest output showing 40+ tests]

**Combined MUX Tests:**
[paste pytest output showing P1+P2+P3+P4 total]

**Regression Check:**
[paste unit test output confirming no regressions]

**Completion Matrix:**
| Deliverable | Status | Evidence |
|-------------|--------|----------|
| Provenance | ✅ | metadata.py:XX-YY |
| Relevance | ✅ | metadata.py:XX-YY |
| ... | ... | ... |

**TOTAL: 13/13 = 100%**
```

---

## STOP Conditions

**STOP immediately and escalate if:**
1. P1/P2/P3 tests fail (baseline broken)
2. Metadata dimensions conflict with existing patterns
3. Journal integration breaks existing logging
4. Relations create circular dependency issues
5. Performance concerns with metadata storage
6. <40 tests after all phases complete

**When stopped**: Document the issue, provide options, wait for PM decision.

---

## Self-Check Before Claiming Complete

1. Does the completion matrix show 13/13 = 100%?
2. Did I provide pytest output for every phase?
3. Did I run the combined MUX test suite (P1+P2+P3+P4)?
4. Did I run the full unit test regression check?
5. Is ADR-055 updated with metadata diagram?
6. Are there 40+ tests total for P4?
7. Did I preserve all P1/P2/P3 test counts?
8. Am I claiming without evidence?

---

## Related Documentation

- **P1**: `services/mux/protocols.py` - EntityProtocol, MomentProtocol, PlaceProtocol
- **P2**: `services/mux/ownership.py` - OwnershipCategory, HasOwnership
- **P3**: `services/mux/lifecycle.py` - LifecycleState, HasLifecycle
- **ADR-045**: Object Model concepts
- **ADR-050**: Conversation-as-Graph
- **ADR-055**: Implementation details (add Appendix C)

---

## Key Patterns from P1/P2/P3 to Follow

1. **Dataclass for types**: Provenance, Relevance follow LifecycleTransition pattern
2. **@runtime_checkable protocols**: HasMetadata follows HasOwnership, HasLifecycle
3. **Registry/Manager pattern**: RelationRegistry, JournalManager follow LifecycleManager
4. **Enum for types**: RelationType follows LifecycleState
5. **Optional dimensions**: All metadata dimensions are Optional[...]
6. **Experience framing**: Document what each dimension means for Piper

---

_Prompt created: 2026-01-19_
_Template version: v10.2_
