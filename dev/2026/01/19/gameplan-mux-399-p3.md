# Gameplan: MUX-399-P3 Lifecycle State Machine with Composting

**GitHub Issue**: #615
**Epic**: #399 MUX-VISION-OBJECT-MODEL
**Dependencies**: #613 (P1 - Complete), #614 (P2 - Complete)
**Estimated Effort**: ~4 hours
**Template Version**: v9.3

---

## Phase -1: Infrastructure Verification Checkpoint (MANDATORY)

### Part A: Lead Developer's Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI (verified - web/app.py)
- [x] Testing framework: pytest (verified - pytest.ini)
- [x] MUX module: services/mux/ (verified - protocols.py, ownership.py)
- [x] P1 Protocols complete: EntityProtocol, MomentProtocol, PlaceProtocol (101 tests)
- [x] P2 Ownership complete: OwnershipCategory, HasOwnership, OwnershipResolver (25 tests)

**My understanding of the task**:
- Implement 8-stage lifecycle state machine: EMERGENT → DERIVED → NOTICED → PROPOSED → RATIFIED → DEPRECATED → ARCHIVED → COMPOSTED
- Create transition rules (valid paths between states)
- Create HasLifecycle protocol (@runtime_checkable)
- Create LifecycleManager for transitions
- Integrate composting with learning system

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

Worktrees ADD value when:
- [ ] Multiple agents will work in parallel (single agent)
- [x] Task duration >30 minutes (~4 hours)
- [ ] Multi-component work (MUX only)
- [ ] Exploratory/risky changes (follows P1/P2 patterns)

Worktrees ADD overhead when:
- [x] Single agent, sequential work
- [ ] Small fixes (<15 min)
- [x] Tightly coupled files requiring atomic commits
- [ ] Time-critical work

**Assessment:**
- [x] **SKIP WORKTREE** - Single agent, extends existing MUX module, follows established P1/P2 patterns. Worktree overhead exceeds benefit.

### Part B: PM Verification Required

**Verification Commands (Agent will run):**
```bash
# Verify MUX module structure
ls -la services/mux/

# Verify P1 protocols exist
grep -n "class.*Protocol" services/mux/protocols.py

# Verify P2 ownership exists
grep -n "class Ownership" services/mux/ownership.py

# Verify learning service exists (for composting integration)
find services/ -name "*learn*" -type f

# Check tests directory structure
ls -la tests/unit/services/mux/
```

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - P1 and P2 complete (126 tests), MUX module established, patterns proven

---

## Phase 0: Initial Bookending - GitHub Investigation

**Skip**: Issue #615 already verified as open and ready for implementation.

### Phase 0.5-0.8: Conditional Phases

**Phase 0.5 (Frontend-Backend Contract)**: N/A - No UI work
**Phase 0.6 (Data Flow)**: N/A - Self-contained MUX module
**Phase 0.7 (Conversation Design)**: N/A - Not conversational
**Phase 0.8 (Post-Completion)**: N/A - No user state changes

---

## Phase 1: Lifecycle State Definitions (TDD)

**Objective**: Define the 8-stage lifecycle enum with metaphors

### Tests First
```python
# tests/unit/services/mux/test_lifecycle.py

class TestLifecycleStateBasics:
    """Test basic enum functionality"""

    def test_lifecycle_state_has_eight_states(self):
        """All 8 lifecycle states exist"""
        assert len(LifecycleState) == 8

    def test_lifecycle_state_values(self):
        """States have expected names"""
        assert LifecycleState.EMERGENT.value == "emergent"
        assert LifecycleState.COMPOSTED.value == "composted"

class TestLifecycleStateMetaphors:
    """Test consciousness-forward experience framing"""

    def test_lifecycle_state_has_meaning(self):
        """Each state has a meaning"""
        assert LifecycleState.EMERGENT.meaning == "Just appearing, not yet fully formed"

    def test_lifecycle_state_has_experience_phrase(self):
        """Each state has an experience phrase"""
        assert "appearing" in LifecycleState.EMERGENT.experience_phrase

    def test_lifecycle_state_has_typical_objects(self):
        """Each state documents typical objects"""
        assert len(LifecycleState.EMERGENT.typical_objects) > 0
```

### Implementation
```python
# services/mux/lifecycle.py

class LifecycleState(str, Enum):
    """
    8-stage lifecycle representing object journey from emergence to composting.

    "Nothing disappears, it transforms." - Each state honors the object's journey.
    """
    EMERGENT = "emergent"      # Just appearing
    DERIVED = "derived"        # Computed from others
    NOTICED = "noticed"        # Brought to attention
    PROPOSED = "proposed"      # Suggested for action
    RATIFIED = "ratified"      # Accepted, committed
    DEPRECATED = "deprecated"  # Being phased out
    ARCHIVED = "archived"      # Preserved but inactive
    COMPOSTED = "composted"    # Transformed to learning
```

### Evidence Command
```bash
pytest tests/unit/services/mux/test_lifecycle.py -xvs -k "Basics or Metaphors"
```

**Expected**: 8+ tests passing

### Verification Gate
- [ ] LifecycleState enum with 8 states
- [ ] Meanings, experience phrases, typical objects documented
- [ ] Tests passing

---

## Phase 2: Transition Rules (TDD)

**Objective**: Define valid state transitions with validation

### Tests First
```python
class TestLifecycleTransitionRules:
    """Test transition map enforcement"""

    def test_emergent_can_transition_to_derived(self):
        """EMERGENT → DERIVED is valid"""
        assert LifecycleState.DERIVED in VALID_TRANSITIONS[LifecycleState.EMERGENT]

    def test_emergent_cannot_skip_to_composted(self):
        """EMERGENT → COMPOSTED is invalid (can't skip stages)"""
        assert LifecycleState.COMPOSTED not in VALID_TRANSITIONS[LifecycleState.EMERGENT]

    def test_all_paths_lead_to_composted(self):
        """Every state can eventually reach COMPOSTED"""
        # BFS/DFS to verify connectivity

    def test_composted_is_terminal(self):
        """COMPOSTED has no outgoing transitions"""
        assert len(VALID_TRANSITIONS[LifecycleState.COMPOSTED]) == 0

class TestLifecycleTransition:
    """Test transition dataclass"""

    def test_transition_captures_reason(self):
        """Transitions record why they happened"""
        t = LifecycleTransition(
            from_state=LifecycleState.RATIFIED,
            to_state=LifecycleState.DEPRECATED,
            reason="Project completed"
        )
        assert t.reason == "Project completed"

    def test_transition_has_timestamp(self):
        """Transitions are timestamped"""
        t = LifecycleTransition(...)
        assert t.timestamp is not None
```

### Implementation
```python
VALID_TRANSITIONS: Dict[LifecycleState, Set[LifecycleState]] = {
    LifecycleState.EMERGENT: {LifecycleState.DERIVED, LifecycleState.NOTICED},
    LifecycleState.DERIVED: {LifecycleState.NOTICED, LifecycleState.DEPRECATED},
    LifecycleState.NOTICED: {LifecycleState.PROPOSED, LifecycleState.DEPRECATED},
    LifecycleState.PROPOSED: {LifecycleState.RATIFIED, LifecycleState.DEPRECATED},
    LifecycleState.RATIFIED: {LifecycleState.DEPRECATED},
    LifecycleState.DEPRECATED: {LifecycleState.ARCHIVED},
    LifecycleState.ARCHIVED: {LifecycleState.COMPOSTED},
    LifecycleState.COMPOSTED: set(),  # Terminal
}

@dataclass
class LifecycleTransition:
    from_state: LifecycleState
    to_state: LifecycleState
    timestamp: datetime = field(default_factory=datetime.utcnow)
    reason: str = ""
    actor: str = "system"

    def is_valid(self) -> bool:
        return self.to_state in VALID_TRANSITIONS.get(self.from_state, set())
```

### Evidence Command
```bash
pytest tests/unit/services/mux/test_lifecycle.py -xvs -k "Transition"
```

**Expected**: 8+ tests passing

### Verification Gate
- [ ] VALID_TRANSITIONS map defined
- [ ] LifecycleTransition dataclass with is_valid()
- [ ] All paths lead to COMPOSTED verified
- [ ] Tests passing

---

## Phase 3: HasLifecycle Protocol (TDD)

**Objective**: Create @runtime_checkable protocol for lifecycle-aware objects

### Tests First
```python
class TestHasLifecycleProtocol:
    """Test protocol definition and compliance"""

    def test_protocol_is_runtime_checkable(self):
        """Protocol can be used with isinstance()"""
        @dataclass
        class Task:
            lifecycle_state: LifecycleState = LifecycleState.EMERGENT
            lifecycle_history: List[LifecycleTransition] = field(default_factory=list)

        task = Task()
        assert isinstance(task, HasLifecycle)

    def test_non_compliant_object_fails(self):
        """Objects without required properties don't satisfy protocol"""
        class NotALifecycleObject:
            pass
        assert not isinstance(NotALifecycleObject(), HasLifecycle)

    def test_protocol_requires_state_property(self):
        """lifecycle_state property is required"""
        # Verify protocol definition
```

### Implementation
```python
@runtime_checkable
class HasLifecycle(Protocol):
    """
    Protocol for objects that have lifecycle awareness.

    Entities with lifecycle know where they are in their journey
    from emergence to composting.
    """

    @property
    def lifecycle_state(self) -> LifecycleState:
        """Current lifecycle state"""
        ...

    @property
    def lifecycle_history(self) -> List[LifecycleTransition]:
        """History of state transitions"""
        ...
```

### Evidence Command
```bash
pytest tests/unit/services/mux/test_lifecycle.py -xvs -k "Protocol"
```

**Expected**: 3+ tests passing

### Verification Gate
- [ ] HasLifecycle protocol with @runtime_checkable
- [ ] Protocol compliance tests passing
- [ ] isinstance() verification working

---

## Phase 4: Lifecycle Manager (TDD)

**Objective**: Implement central lifecycle management with validation and events

### Tests First
```python
class TestLifecycleManager:
    """Test lifecycle management operations"""

    def test_manager_validates_transitions(self):
        """Invalid transitions are rejected"""
        manager = LifecycleManager()
        obj = MockLifecycleObject(state=LifecycleState.EMERGENT)

        with pytest.raises(InvalidTransitionError):
            manager.transition(obj, LifecycleState.COMPOSTED, "skip all")

    def test_manager_updates_state(self):
        """Valid transitions update object state"""
        manager = LifecycleManager()
        obj = MockLifecycleObject(state=LifecycleState.EMERGENT)

        manager.transition(obj, LifecycleState.NOTICED, "User saw it")
        assert obj.lifecycle_state == LifecycleState.NOTICED

    def test_manager_records_history(self):
        """Transitions are recorded in history"""
        manager = LifecycleManager()
        obj = MockLifecycleObject(state=LifecycleState.EMERGENT)

        manager.transition(obj, LifecycleState.NOTICED, "User saw it")
        assert len(obj.lifecycle_history) == 1
        assert obj.lifecycle_history[0].reason == "User saw it"

    def test_manager_emits_events(self):
        """Transitions emit events for observers"""
        events = []
        manager = LifecycleManager(on_transition=lambda e: events.append(e))
        obj = MockLifecycleObject(state=LifecycleState.EMERGENT)

        manager.transition(obj, LifecycleState.NOTICED, "User saw it")
        assert len(events) == 1
```

### Implementation
```python
class LifecycleManager:
    """
    Manages lifecycle transitions with validation and event emission.

    "Nothing disappears, it transforms" - this manager ensures
    objects journey properly through their lifecycle.
    """

    def __init__(self, on_transition: Optional[Callable] = None):
        self._on_transition = on_transition

    def transition(
        self,
        obj: HasLifecycle,
        to_state: LifecycleState,
        reason: str,
        actor: str = "system"
    ) -> LifecycleTransition:
        """Execute a lifecycle transition with validation"""
        transition = LifecycleTransition(
            from_state=obj.lifecycle_state,
            to_state=to_state,
            reason=reason,
            actor=actor
        )

        if not transition.is_valid():
            raise InvalidTransitionError(...)

        # Update object (implementation depends on object structure)
        # Record history
        # Emit event

        return transition
```

### Evidence Command
```bash
pytest tests/unit/services/mux/test_lifecycle.py -xvs -k "Manager"
```

**Expected**: 6+ tests passing

### Verification Gate
- [ ] LifecycleManager with transition() method
- [ ] Validation of transitions
- [ ] History tracking
- [ ] Event emission
- [ ] Tests passing

---

## Phase 5: Composting Integration (TDD)

**Objective**: Extract learning when objects reach COMPOSTED state

### Tests First
```python
class TestCompostingExtractor:
    """Test learning extraction from composted objects"""

    def test_extractor_captures_key_attributes(self):
        """Composting extracts object's key information"""
        obj = MockLifecycleObject(name="Q4 Planning", description="Strategic planning")
        extractor = CompostingExtractor()

        compost = extractor.extract(obj)
        assert compost.object_summary["name"] == "Q4 Planning"

    def test_extractor_captures_journey(self):
        """Composting preserves the object's lifecycle journey"""
        obj = MockLifecycleObject()
        obj.lifecycle_history = [
            LifecycleTransition(...),  # EMERGENT → NOTICED
            LifecycleTransition(...),  # NOTICED → RATIFIED
            # ... full journey
        ]

        compost = extractor.extract(obj)
        assert len(compost.journey) == len(obj.lifecycle_history)

    def test_extractor_generates_lessons(self):
        """Composting extracts lessons from the journey"""
        obj = MockLifecycleObject()
        extractor = CompostingExtractor()

        compost = extractor.extract(obj)
        assert "lessons" in compost.__dict__

    def test_composting_integrates_with_learning(self):
        """Composted data is fed to learning service"""
        # Mock learning service integration
```

### Implementation
```python
@dataclass
class CompostResult:
    """What we extract when composting an object"""
    object_summary: Dict[str, Any]
    journey: List[LifecycleTransition]
    lessons: List[str]
    composted_at: datetime = field(default_factory=datetime.utcnow)

class CompostingExtractor:
    """
    Extracts learning from objects reaching COMPOSTED state.

    "The shadow side of PM work is ending things - but ending
    should feed new beginnings."
    """

    def extract(self, obj: HasLifecycle) -> CompostResult:
        """Extract learning from composted object"""
        return CompostResult(
            object_summary=self._summarize(obj),
            journey=obj.lifecycle_history,
            lessons=self._extract_lessons(obj)
        )
```

### Evidence Command
```bash
pytest tests/unit/services/mux/test_lifecycle.py -xvs -k "Composting"
```

**Expected**: 5+ tests passing

### Verification Gate
- [ ] CompostResult dataclass defined
- [ ] CompostingExtractor with extract() method
- [ ] Journey preservation working
- [ ] Learning service integration (mock for MVP)
- [ ] Tests passing

---

## Phase Z: Completion & Handoff

### Completion Matrix

| Deliverable | Target | Actual | Status |
|-------------|--------|--------|--------|
| LifecycleState enum (8 states) | 1 | 0 | Pending |
| Transition rules + LifecycleTransition | 1 | 0 | Pending |
| HasLifecycle protocol | 1 | 0 | Pending |
| LifecycleManager | 1 | 0 | Pending |
| CompostingExtractor | 1 | 0 | Pending |
| CompostResult dataclass | 1 | 0 | Pending |
| ADR-055 lifecycle diagram | 1 | 0 | Pending |
| Unit Tests | 30+ | 0 | Pending |

**TOTAL: 0/8 = 0%**

Only claim complete when **8/8 = 100%**

### Evidence Commands

```bash
# Run all P3 tests
pytest tests/unit/services/mux/test_lifecycle.py -xvs

# Run combined P1+P2+P3 tests
pytest tests/unit/services/mux/ -v

# Run full unit test suite for regression
pytest tests/unit/ -v

# Verify file created
ls -la services/mux/lifecycle.py
wc -l services/mux/lifecycle.py
```

### Handoff Format

```markdown
## P3 Complete - Evidence

**Files Created:**
- `services/mux/lifecycle.py` (+N lines)
- `tests/unit/services/mux/test_lifecycle.py` (+N lines)
- ADR-055 updated with lifecycle diagram

**Test Results:**
[paste pytest output]

**Combined MUX Tests:**
[paste pytest output showing P1+P2+P3]

**Regression Check:**
[paste unit test output confirming no regressions]

**Completion Matrix:**
| Deliverable | Status | Evidence |
|-------------|--------|----------|
| LifecycleState | ✅ | lifecycle.py:XX-YY |
| ... | ... | ... |
```

---

## Multi-Agent Coordination Plan

### Agent Deployment Map

| Phase | Agent Type | Deliverables | Evidence Required |
|-------|------------|--------------|-------------------|
| 1-5 | Code Agent | LifecycleState, transitions, protocol, manager, composting | 30+ tests |
| Z | Code Agent | ADR-055 update, completion report | Documentation |

**Single Agent Justification**: Follows same pattern as successful P1 (101 tests) and P2 (25 tests). Sequential TDD phases, single file output, tight coupling between components.

### Verification Gates

- [ ] Phase 1: 8+ enum tests passing
- [ ] Phase 2: 8+ transition tests passing
- [ ] Phase 3: 3+ protocol tests passing
- [ ] Phase 4: 6+ manager tests passing
- [ ] Phase 5: 5+ composting tests passing
- [ ] Phase Z: All 30+ tests passing, no regressions

---

## STOP Conditions

**STOP immediately and escalate if:**
1. 8-state model doesn't fit real object lifecycles
2. Composting creates data integrity issues
3. Learning service integration is blocked
4. Transition rules too rigid or too permissive
5. Performance concerns with history tracking
6. Any P1 or P2 tests regress
7. Pattern conflicts with existing MUX design

**When stopped**: Document the issue, provide options, wait for PM decision.

---

## Related Documentation

- **P1**: #613 - Core Grammar & Lens Infrastructure (protocols.py)
- **P2**: #614 - Ownership Model (ownership.py)
- **ADR-045**: Object Model concepts
- **ADR-055**: Implementation details
- **PPM Memo**: "Nothing disappears, it transforms"

---

## Key Patterns from P1/P2 to Follow

1. **Enum with rich properties**: LifecycleState follows PerceptionMode/OwnershipCategory pattern
2. **@runtime_checkable protocols**: HasLifecycle follows HasOwnership pattern
3. **Resolver/Manager pattern**: LifecycleManager follows OwnershipResolver pattern
4. **Experience framing**: Meanings and metaphors for consciousness-forward design
5. **TDD sequence**: Tests first, then implementation

---

_Gameplan created: 2026-01-19_
_Template version: v9.3_
