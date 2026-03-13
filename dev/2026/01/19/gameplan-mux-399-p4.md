# Gameplan: MUX-399-P4 Metadata Schema & Journal Extensions

**GitHub Issue**: #616
**Epic**: #399 MUX-VISION-OBJECT-MODEL
**Dependencies**: #613 (P1 - Complete), #614 (P2 - Complete), #615 (P3 - Complete)
**Estimated Effort**: ~4 hours
**Template Version**: v9.3

---

## Phase -1: Infrastructure Verification Checkpoint (MANDATORY)

### Part A: Lead Developer's Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI (verified - web/app.py)
- [x] Testing framework: pytest (verified - pytest.ini)
- [x] MUX module: services/mux/ (verified - protocols.py, ownership.py, lifecycle.py)
- [x] P1 Protocols complete: EntityProtocol, MomentProtocol, PlaceProtocol (101 tests)
- [x] P2 Ownership complete: OwnershipCategory, HasOwnership, OwnershipResolver (25 tests)
- [x] P3 Lifecycle complete: LifecycleState, HasLifecycle, LifecycleManager (69 tests)

**My understanding of the task**:
- Implement 6 universal metadata dimensions: Provenance, Relevance, Attention, Confidence, Relations, Journal
- Create HasMetadata protocol with optional dimensions
- Create trackers/calculators/registries for each dimension
- Implement two-layer journal (Session + Insight)

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

Worktrees ADD value when:
- [ ] Multiple agents will work in parallel (single agent)
- [x] Task duration >30 minutes (~4 hours)
- [ ] Multi-component work (MUX only)
- [ ] Exploratory/risky changes (follows P1/P2/P3 patterns)

Worktrees ADD overhead when:
- [x] Single agent, sequential work
- [ ] Small fixes (<15 min)
- [x] Tightly coupled files requiring atomic commits
- [ ] Time-critical work

**Assessment:**
- [x] **SKIP WORKTREE** - Single agent, extends existing MUX module, follows established P1/P2/P3 patterns. Worktree overhead exceeds benefit.

### Part B: PM Verification Required

**Verification Commands (Agent will run):**
```bash
# Verify MUX module structure
ls -la services/mux/

# Verify P1/P2/P3 complete
pytest tests/unit/services/mux/ -v --tb=no | tail -5

# Check for existing metadata patterns
grep -r "metadata" services/ --include="*.py" | head -10

# Check for existing journal/logging patterns
grep -r "journal\|session.*log" services/ --include="*.py" | head -10

# Verify test directory structure
ls -la tests/unit/services/mux/
```

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - P1, P2, P3 complete (195 tests), MUX module established, patterns proven

---

## Phase 0: Initial Bookending - GitHub Investigation

**Skip**: Issue #616 already verified as open and ready for implementation.

### Phase 0.5-0.8: Conditional Phases

**Phase 0.5 (Frontend-Backend Contract)**: N/A - No UI work
**Phase 0.6 (Data Flow)**: N/A - Self-contained MUX module
**Phase 0.7 (Conversation Design)**: N/A - Not conversational
**Phase 0.8 (Post-Completion)**: N/A - No user state changes

---

## Phase 1: Metadata Dimension Definitions (TDD)

**Objective**: Define the 6 universal metadata dimensions

### Tests First
```python
# tests/unit/services/mux/test_metadata.py

class TestProvenanceDimension:
    """Test Provenance metadata type"""

    def test_provenance_has_source(self):
        """Provenance tracks where data came from"""
        p = Provenance(source="github", fetched_at=datetime.utcnow())
        assert p.source == "github"

    def test_provenance_has_confidence(self):
        """Provenance includes source confidence"""
        p = Provenance(source="github", confidence=0.95)
        assert 0 <= p.confidence <= 1

    def test_provenance_calculates_freshness(self):
        """Provenance can determine data freshness"""
        # Freshness decreases over time


class TestRelevanceDimension:
    """Test Relevance metadata type"""

    def test_relevance_has_score(self):
        """Relevance has a score"""

    def test_relevance_tracks_factors(self):
        """Relevance records what contributed to score"""

    def test_relevance_decays_over_time(self):
        """Relevance fades based on decay_rate"""


class TestAttentionStateDimension:
    """Test Attention State metadata type"""

    def test_attention_tracks_who_noticed(self):
        """Attention records who has noticed"""

    def test_attention_has_priority_level(self):
        """Attention has priority/urgency level"""


class TestConfidenceDimension:
    """Test Confidence metadata type"""

    def test_confidence_has_score(self):
        """Confidence has a score 0-1"""

    def test_confidence_tracks_basis(self):
        """Confidence records what it's based on"""


class TestRelationsDimension:
    """Test Relations metadata type"""

    def test_relation_has_target(self):
        """Relation points to another object"""

    def test_relation_has_type(self):
        """Relation has a type (REFERENCES, BLOCKS, etc.)"""


class TestJournalDimension:
    """Test Journal metadata type"""

    def test_session_entry_is_audit_trail(self):
        """Session journal captures what happened"""

    def test_insight_entry_captures_meaning(self):
        """Insight journal captures interpretations"""
```

### Implementation
```python
# services/mux/metadata.py

@dataclass
class Provenance:
    """Where did this data come from?"""
    source: str
    fetched_at: datetime = field(default_factory=datetime.utcnow)
    confidence: float = 1.0  # Source confidence 0-1

    @property
    def freshness(self) -> float:
        """How fresh is this data? (0=stale, 1=fresh)"""
        age = (datetime.utcnow() - self.fetched_at).total_seconds()
        # Decay over 1 hour
        return max(0, 1 - (age / 3600))


@dataclass
class Relevance:
    """How important is this?"""
    score: float  # 0-1
    factors: List[str] = field(default_factory=list)
    context: str = ""
    decay_rate: float = 0.1  # How quickly relevance fades


@dataclass
class AttentionState:
    """Who has noticed this?"""
    noticed_by: List[str] = field(default_factory=list)
    noticed_at: Optional[datetime] = None
    attention_level: str = "normal"  # low, normal, high, urgent


@dataclass
class Confidence:
    """How sure are we?"""
    score: float  # 0-1
    basis: str = ""  # What is confidence based on
    last_validated: Optional[datetime] = None


@dataclass
class Relation:
    """Connection to another object"""
    target_id: str
    relation_type: str  # REFERENCES, BLOCKS, CONTAINS, etc.
    strength: float = 1.0  # 0-1
    bidirectional: bool = False


@dataclass
class JournalEntry:
    """Base journal entry"""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    content: str = ""
    actor: str = "system"


@dataclass
class SessionJournalEntry(JournalEntry):
    """Audit trail - what happened (objective)"""
    event_type: str = ""
    trigger: str = ""


@dataclass
class InsightJournalEntry(JournalEntry):
    """Meaning extraction - what it meant (interpretive)"""
    learning: str = ""
    connected_insights: List[str] = field(default_factory=list)
```

### Evidence Command
```bash
pytest tests/unit/services/mux/test_metadata.py -xvs -k "Dimension"
```

**Expected**: 15+ tests passing

### Verification Gate
- [ ] All 6 dimension types defined
- [ ] Tests for each dimension passing
- [ ] Dataclasses with proper defaults

---

## Phase 2: HasMetadata Protocol (TDD)

**Objective**: Create @runtime_checkable protocol with optional dimensions

### Tests First
```python
class TestHasMetadataProtocol:
    """Test protocol definition"""

    def test_protocol_is_runtime_checkable(self):
        """Protocol can be used with isinstance()"""

    def test_object_with_all_dimensions_complies(self):
        """Object with full metadata satisfies protocol"""

    def test_object_with_partial_dimensions_complies(self):
        """Object with only some dimensions still satisfies"""

    def test_dimensions_are_optional(self):
        """None values for missing dimensions are OK"""
```

### Implementation
```python
@runtime_checkable
class HasMetadata(Protocol):
    """
    Protocol for objects with metadata awareness.

    All dimensions are optional - objects declare what metadata
    they carry. "Metadata is what Piper knows about what it perceives."
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
    def journal(self) -> Optional[List[JournalEntry]]:
        """What is the history?"""
        ...
```

### Evidence Command
```bash
pytest tests/unit/services/mux/test_metadata.py -xvs -k "Protocol"
```

**Expected**: 4+ tests passing

### Verification Gate
- [ ] HasMetadata protocol with @runtime_checkable
- [ ] All dimensions optional (Optional[...])
- [ ] Protocol compliance tests passing

---

## Phase 3: Trackers and Calculators (TDD)

**Objective**: Implement ProvenanceTracker and ConfidenceCalculator

### Tests First
```python
class TestProvenanceTracker:
    """Test source tracking"""

    def test_tracker_records_source(self):
        """Tracker captures source information"""

    def test_tracker_timestamps_fetch(self):
        """Tracker records when data was fetched"""

    def test_tracker_from_integration(self):
        """Tracker creates provenance from integration name"""


class TestConfidenceCalculator:
    """Test confidence calculation"""

    def test_calculator_produces_score(self):
        """Calculator outputs score 0-1"""

    def test_calculator_records_basis(self):
        """Calculator documents what score is based on"""

    def test_direct_observation_high_confidence(self):
        """Direct observation gets high confidence"""

    def test_inferred_lower_confidence(self):
        """Inferred data gets lower confidence"""
```

### Implementation
```python
class ProvenanceTracker:
    """Records where data comes from"""

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
        """Create provenance for user-provided data"""
        return Provenance(source="user", confidence=1.0)


class ConfidenceCalculator:
    """Calculates confidence scores with basis tracking"""

    @staticmethod
    def from_observation(direct: bool = True) -> Confidence:
        """Calculate confidence from observation type"""
        return Confidence(
            score=0.95 if direct else 0.7,
            basis="direct observation" if direct else "inference",
            last_validated=datetime.utcnow()
        )
```

### Evidence Command
```bash
pytest tests/unit/services/mux/test_metadata.py -xvs -k "Tracker or Calculator"
```

**Expected**: 8+ tests passing

### Verification Gate
- [ ] ProvenanceTracker implemented
- [ ] ConfidenceCalculator implemented
- [ ] Tests passing

---

## Phase 4: Relations Registry (TDD)

**Objective**: Implement typed relationships between objects

### Tests First
```python
class TestRelationType:
    """Test relation type enum"""

    def test_relation_types_exist(self):
        """Common relation types are defined"""
        # REFERENCES, BLOCKS, CONTAINS, DERIVES_FROM, etc.


class TestRelationRegistry:
    """Test relation management"""

    def test_registry_adds_relation(self):
        """Can add relation between objects"""

    def test_registry_finds_relations_for_object(self):
        """Can retrieve all relations for an object"""

    def test_bidirectional_creates_both_directions(self):
        """Bidirectional flag creates inverse relation"""

    def test_registry_removes_relation(self):
        """Can remove relations"""
```

### Implementation
```python
class RelationType(str, Enum):
    """Types of relationships between objects"""
    REFERENCES = "references"
    BLOCKS = "blocks"
    CONTAINS = "contains"
    DERIVES_FROM = "derives_from"
    RELATED_TO = "related_to"


class RelationRegistry:
    """Manages typed relationships between objects"""

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
                relation_type=f"inverse_{relation.relation_type}",
                strength=relation.strength,
                bidirectional=False  # Don't recurse
            )
            self.add(relation.target_id, inverse)

    def get_relations(self, object_id: str) -> List[Relation]:
        """Get all relations for an object"""
        return self._relations.get(object_id, [])
```

### Evidence Command
```bash
pytest tests/unit/services/mux/test_metadata.py -xvs -k "Relation"
```

**Expected**: 6+ tests passing

### Verification Gate
- [ ] RelationType enum defined
- [ ] RelationRegistry implemented
- [ ] Bidirectional relations working
- [ ] Tests passing

---

## Phase 5: Two-Layer Journal (TDD)

**Objective**: Implement Session + Insight journal layers

### Tests First
```python
class TestSessionJournal:
    """Test audit trail layer"""

    def test_session_entry_captures_event(self):
        """Session journal records what happened"""

    def test_session_entry_has_timestamp(self):
        """Entries are timestamped"""

    def test_session_entry_tracks_trigger(self):
        """Records what triggered the event"""


class TestInsightJournal:
    """Test meaning extraction layer"""

    def test_insight_entry_captures_learning(self):
        """Insight journal records learnings"""

    def test_insight_connects_to_other_insights(self):
        """Insights can reference other insights"""


class TestJournalManager:
    """Test journal coordination"""

    def test_manager_logs_session_event(self):
        """Manager can log session events"""

    def test_manager_extracts_insight(self):
        """Manager can extract insights"""

    def test_manager_retrieves_full_history(self):
        """Manager provides combined view"""
```

### Implementation
```python
@dataclass
class Journal:
    """Two-layer journal: Session (audit) + Insight (meaning)"""
    session_entries: List[SessionJournalEntry] = field(default_factory=list)
    insight_entries: List[InsightJournalEntry] = field(default_factory=list)


class JournalManager:
    """Coordinates session and insight journal layers"""

    def __init__(self):
        self._journals: Dict[str, Journal] = {}

    def log_session_event(
        self,
        object_id: str,
        event_type: str,
        content: str,
        trigger: str = ""
    ) -> SessionJournalEntry:
        """Log an audit trail event"""
        entry = SessionJournalEntry(
            event_type=event_type,
            content=content,
            trigger=trigger
        )
        self._get_journal(object_id).session_entries.append(entry)
        return entry

    def extract_insight(
        self,
        object_id: str,
        learning: str,
        content: str = ""
    ) -> InsightJournalEntry:
        """Extract and record an insight"""
        entry = InsightJournalEntry(
            learning=learning,
            content=content
        )
        self._get_journal(object_id).insight_entries.append(entry)
        return entry

    def get_journal(self, object_id: str) -> Journal:
        """Get full journal for an object"""
        return self._get_journal(object_id)

    def _get_journal(self, object_id: str) -> Journal:
        if object_id not in self._journals:
            self._journals[object_id] = Journal()
        return self._journals[object_id]
```

### Evidence Command
```bash
pytest tests/unit/services/mux/test_metadata.py -xvs -k "Journal"
```

**Expected**: 8+ tests passing

### Verification Gate
- [ ] SessionJournalEntry and InsightJournalEntry defined
- [ ] Journal dataclass combining both
- [ ] JournalManager implemented
- [ ] Tests passing

---

## Phase Z: Completion & Handoff

### Completion Matrix

| Deliverable | Target | Actual | Status |
|-------------|--------|--------|--------|
| Provenance dimension | 1 | 0 | Pending |
| Relevance dimension | 1 | 0 | Pending |
| AttentionState dimension | 1 | 0 | Pending |
| Confidence dimension | 1 | 0 | Pending |
| Relation type + RelationType enum | 1 | 0 | Pending |
| Journal dimension (Session + Insight) | 1 | 0 | Pending |
| HasMetadata protocol | 1 | 0 | Pending |
| ProvenanceTracker | 1 | 0 | Pending |
| ConfidenceCalculator | 1 | 0 | Pending |
| RelationRegistry | 1 | 0 | Pending |
| JournalManager | 1 | 0 | Pending |
| ADR-055 metadata diagram | 1 | 0 | Pending |
| Unit Tests | 40+ | 0 | Pending |

**TOTAL: 0/13 = 0%**

Only claim complete when **13/13 = 100%**

### Evidence Commands

```bash
# Run all P4 tests
pytest tests/unit/services/mux/test_metadata.py -xvs

# Run combined P1+P2+P3+P4 tests
pytest tests/unit/services/mux/ -v

# Run full unit test suite for regression
pytest tests/unit/ -v --tb=no | tail -5

# Verify file created
ls -la services/mux/metadata.py
wc -l services/mux/metadata.py
```

### Handoff Format

```markdown
## P4 Complete - Evidence

**Files Created:**
- `services/mux/metadata.py` (+N lines)
- `tests/unit/services/mux/test_metadata.py` (+N lines)
- ADR-055 updated with metadata diagram

**Test Results:**
[paste pytest output]

**Combined MUX Tests:**
[paste pytest output showing P1+P2+P3+P4]

**Regression Check:**
[paste unit test output confirming no regressions]

**Completion Matrix:**
| Deliverable | Status | Evidence |
|-------------|--------|----------|
| Provenance | ✅ | metadata.py:XX-YY |
| ... | ... | ... |
```

---

## Multi-Agent Coordination Plan

### Agent Deployment Map

| Phase | Agent Type | Deliverables | Evidence Required |
|-------|------------|--------------|-------------------|
| 1-5 | Code Agent | 6 dimensions, protocol, trackers, registry, manager | 40+ tests |
| Z | Code Agent | ADR-055 update, completion report | Documentation |

**Single Agent Justification**: Follows same pattern as successful P1 (101 tests), P2 (25 tests), P3 (69 tests). Sequential TDD phases, single file output, tight coupling between components.

### Verification Gates

- [ ] Phase 1: 15+ dimension tests passing
- [ ] Phase 2: 4+ protocol tests passing
- [ ] Phase 3: 8+ tracker/calculator tests passing
- [ ] Phase 4: 6+ relation tests passing
- [ ] Phase 5: 8+ journal tests passing
- [ ] Phase Z: All 40+ tests passing, no regressions

---

## STOP Conditions

**STOP immediately and escalate if:**
1. Metadata dimensions conflict with existing patterns
2. Journal integration breaks existing logging
3. Relations create circular dependency issues
4. Performance concerns with metadata storage
5. Scope creep into UI/migration territory
6. Any P1/P2/P3 tests regress
7. Pattern conflicts with existing MUX design

**When stopped**: Document the issue, provide options, wait for PM decision.

---

## Related Documentation

- **P1**: #613 - Core Grammar & Lens Infrastructure (protocols.py)
- **P2**: #614 - Ownership Model (ownership.py)
- **P3**: #615 - Lifecycle State Machine (lifecycle.py)
- **ADR-045**: Object Model concepts
- **ADR-050**: Conversation-as-Graph
- **ADR-055**: Implementation details

---

## Key Patterns from P1/P2/P3 to Follow

1. **Dataclass for types**: Provenance, Relevance, etc. follow LifecycleTransition pattern
2. **@runtime_checkable protocols**: HasMetadata follows HasOwnership, HasLifecycle patterns
3. **Registry/Manager pattern**: RelationRegistry, JournalManager follow LifecycleManager pattern
4. **Optional dimensions**: Use Optional[...] for flexibility
5. **Experience framing**: Document what each dimension means for Piper's perception

---

_Gameplan created: 2026-01-19_
_Template version: v9.3_
