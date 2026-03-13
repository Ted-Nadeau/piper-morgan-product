# Gameplan: MUX-399-P2 Ownership Model (Native/Federated/Synthetic)

**GitHub Issue**: #614
**Parent Epic**: #399 MUX-VISION-OBJECT-MODEL
**Type**: Implementation
**Estimated Effort**: Medium (4 hours)
**Created**: 2026-01-19
**Depends On**: #613 (P1 Core Grammar) - COMPLETE ✅

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Infrastructure Status** (verified):
- [x] P1 Infrastructure: `services/mux/` module complete (101 tests passing)
- [x] Protocols: EntityProtocol, MomentProtocol, PlaceProtocol in `services/mux/protocols.py`
- [x] ADR-045: Grammar definition ACCEPTED
- [x] ADR-055: Implementation specification COMPLETE
- [x] Domain models: `services/domain/models.py` exists

**Key Context from P1**:
1. Protocols use `@runtime_checkable` - Ownership should compose similarly
2. Experience framing transforms data → consciousness language
3. Tests follow TDD pattern in `tests/unit/services/mux/`

**My understanding of the task**:
- Define 3 ownership categories (NATIVE, FEDERATED, SYNTHETIC)
- Create HasOwnership protocol for ownership-aware objects
- Build OwnershipResolver for automatic category determination
- Track transformations between categories
- Map existing domain models to ownership categories

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

Worktrees ADD value when:
- [ ] Multiple agents will work in parallel
- [x] Task duration >30 minutes ← YES, ~4 hours
- [ ] Exploratory/risky changes

Worktrees ADD overhead when:
- [x] Single agent, sequential work ← Dominant
- [ ] Small fixes
- [x] Building on existing module structure ← Extends services/mux/

**Assessment:**
- [ ] **USE WORKTREE**
- [x] **SKIP WORKTREE** - Single agent, extending existing module
- [ ] **PM DECISION**

**Rationale**: Extends existing `services/mux/` module with clear structure. Sequential TDD work, no parallel risk.

### Part B: PM Verification Required

**PM, please confirm**:

1. **Location for ownership code**: `services/mux/ownership.py`
2. **Protocol placement**: Add to existing `services/mux/protocols.py` or new file?
3. **Tests location**: `tests/unit/services/mux/test_ownership.py`

### Part C: Proceed/Revise Decision

- [ ] **PROCEED** - Understanding is correct
- [ ] **REVISE** - Need different approach
- [ ] **CLARIFY** - Need more context

---

## Phase 0: GitHub Orientation & Setup

### Required Actions

1. **Verify P1 complete and infrastructure available**
   ```bash
   pytest tests/unit/services/mux/ -v --tb=short | tail -10
   # Expected: 101 tests passing
   ```

2. **Review existing domain models for mapping**
   ```bash
   grep -n "^class " services/domain/models.py | head -30
   ```

3. **Verify services/mux/ structure**
   ```bash
   ls -la services/mux/
   ```

4. **Create session log**
   ```bash
   # File: dev/2026/01/19/2026-01-19-HHMM-p2-code-log.md
   ```

### Deliverables
- [ ] P1 infrastructure verified
- [ ] Domain models identified for mapping
- [ ] Session log created

### Evidence Required
```bash
pytest tests/unit/services/mux/ -v --tb=no | tail -5
ls -la services/mux/
```

---

## Phase 0.5-0.8: NOT APPLICABLE

These phases (Frontend-Backend Contract, Data Flow, Conversation Design, Post-Completion) are for UI/integration work. P2 is pure backend infrastructure extending P1.

---

## Phase 1: Ownership Definitions (1 hour)

### Objective
Define the three ownership categories and their characteristics.

### TDD Sequence

**Step 1.1: Write tests FIRST**
```python
# tests/unit/services/mux/test_ownership.py
import pytest
from services.mux.ownership import OwnershipCategory

def test_ownership_category_has_native():
    """NATIVE category exists for Piper's Mind."""
    assert OwnershipCategory.NATIVE is not None

def test_ownership_category_has_federated():
    """FEDERATED category exists for Piper's Senses."""
    assert OwnershipCategory.FEDERATED is not None

def test_ownership_category_has_synthetic():
    """SYNTHETIC category exists for Piper's Understanding."""
    assert OwnershipCategory.SYNTHETIC is not None

def test_ownership_categories_have_descriptions():
    """Each category has meaningful description."""
    assert OwnershipCategory.NATIVE.description
    assert OwnershipCategory.FEDERATED.description
    assert OwnershipCategory.SYNTHETIC.description

def test_ownership_categories_have_metaphors():
    """Each category has consciousness metaphor."""
    assert "Mind" in OwnershipCategory.NATIVE.metaphor
    assert "Senses" in OwnershipCategory.FEDERATED.metaphor
    assert "Understanding" in OwnershipCategory.SYNTHETIC.metaphor
```

**Step 1.2: Run tests (expect failures)**
```bash
pytest tests/unit/services/mux/test_ownership.py -v
```

**Step 1.3: Implement OwnershipCategory**
```python
# services/mux/ownership.py
from enum import Enum
from dataclasses import dataclass
from typing import Optional

class OwnershipCategory(Enum):
    """
    Describes Piper's relationship to knowledge.

    The three categories represent Piper's epistemology:
    - NATIVE: Piper's Mind - what Piper creates/owns directly
    - FEDERATED: Piper's Senses - what Piper observes externally
    - SYNTHETIC: Piper's Understanding - what Piper constructs through reasoning
    """

    NATIVE = "native"
    FEDERATED = "federated"
    SYNTHETIC = "synthetic"

    @property
    def description(self) -> str:
        """Detailed description of this ownership category."""
        descriptions = {
            self.NATIVE: "Objects Piper creates and owns directly - sessions, memories, trust states, learning",
            self.FEDERATED: "Objects Piper observes from external sources - GitHub issues, Slack messages, calendar events",
            self.SYNTHETIC: "Objects Piper constructs through reasoning - inferred status, assembled risk, pattern recognition"
        }
        return descriptions[self]

    @property
    def metaphor(self) -> str:
        """Consciousness metaphor for this category."""
        metaphors = {
            self.NATIVE: "Piper's Mind",
            self.FEDERATED: "Piper's Senses",
            self.SYNTHETIC: "Piper's Understanding"
        }
        return metaphors[self]

    @property
    def experience_phrase(self) -> str:
        """How Piper expresses knowledge from this category."""
        phrases = {
            self.NATIVE: "I know this because I created it",
            self.FEDERATED: "I see this in {place}",
            self.SYNTHETIC: "I understand this to mean..."
        }
        return phrases[self]
```

**Step 1.4: Run tests (expect passes)**
```bash
pytest tests/unit/services/mux/test_ownership.py -v
```

### Deliverables
- `services/mux/ownership.py` with OwnershipCategory enum
- `tests/unit/services/mux/test_ownership.py` with category tests

### Evidence Required
```bash
pytest tests/unit/services/mux/test_ownership.py -v 2>&1
```

---

## Phase 2: HasOwnership Protocol (1 hour)

### Objective
Create protocol for objects with ownership awareness.

### TDD Sequence

**Step 2.1: Write tests FIRST**
```python
# Add to tests/unit/services/mux/test_ownership.py

from typing import runtime_checkable
from services.mux.ownership import HasOwnership, OwnershipCategory

def test_has_ownership_is_runtime_checkable():
    """HasOwnership protocol can be used with isinstance()."""
    # Protocol should be @runtime_checkable

def test_has_ownership_requires_category():
    """HasOwnership requires ownership_category property."""

def test_has_ownership_requires_source():
    """HasOwnership requires ownership_source property."""

def test_has_ownership_requires_confidence():
    """HasOwnership requires ownership_confidence property."""

def test_mock_object_satisfies_protocol():
    """A properly structured object satisfies HasOwnership."""
    class MockNativeObject:
        ownership_category = OwnershipCategory.NATIVE
        ownership_source = "piper"
        ownership_confidence = 1.0

    obj = MockNativeObject()
    assert isinstance(obj, HasOwnership)
```

**Step 2.2: Implement HasOwnership Protocol**
```python
# Add to services/mux/ownership.py

from typing import Protocol, runtime_checkable

@runtime_checkable
class HasOwnership(Protocol):
    """
    Protocol for objects that have ownership awareness.

    Any object can satisfy this protocol by providing:
    - ownership_category: Which category (NATIVE/FEDERATED/SYNTHETIC)
    - ownership_source: Where this object came from
    - ownership_confidence: How certain we are of the categorization
    """

    @property
    def ownership_category(self) -> OwnershipCategory:
        """The ownership category of this object."""
        ...

    @property
    def ownership_source(self) -> str:
        """The source/origin of this object (e.g., 'piper', 'github', 'inference')."""
        ...

    @property
    def ownership_confidence(self) -> float:
        """Confidence in ownership categorization (0.0 to 1.0)."""
        ...
```

### Deliverables
- HasOwnership protocol in `services/mux/ownership.py`
- Protocol compliance tests

### Evidence Required
```bash
pytest tests/unit/services/mux/test_ownership.py -v 2>&1
```

---

## Phase 3: Ownership Resolver (1 hour)

### Objective
Implement rules for determining ownership category.

### TDD Sequence

**Step 3.1: Write tests FIRST**
```python
# Add to tests/unit/services/mux/test_ownership.py

from services.mux.ownership import OwnershipResolver, OwnershipCategory

def test_resolver_native_for_piper_created():
    """Objects created by Piper are NATIVE."""
    resolver = OwnershipResolver()
    category = resolver.determine(source="piper", created_by="piper")
    assert category == OwnershipCategory.NATIVE

def test_resolver_federated_for_integration():
    """Objects from integrations are FEDERATED."""
    resolver = OwnershipResolver()
    category = resolver.determine(source="github", created_by="external")
    assert category == OwnershipCategory.FEDERATED

def test_resolver_synthetic_for_derived():
    """Derived/computed objects are SYNTHETIC."""
    resolver = OwnershipResolver()
    category = resolver.determine(source="inference", is_derived=True)
    assert category == OwnershipCategory.SYNTHETIC

def test_resolver_returns_confidence():
    """Resolver provides confidence score."""
    resolver = OwnershipResolver()
    result = resolver.resolve(source="github")
    assert hasattr(result, 'confidence')
    assert 0.0 <= result.confidence <= 1.0

def test_resolver_handles_cached_federated():
    """Cached federated data remains FEDERATED."""
    resolver = OwnershipResolver()
    category = resolver.determine(source="github", is_cached=True)
    assert category == OwnershipCategory.FEDERATED
```

**Step 3.2: Implement OwnershipResolver**
```python
# Add to services/mux/ownership.py

@dataclass
class OwnershipResolution:
    """Result of ownership resolution."""
    category: OwnershipCategory
    confidence: float
    reasoning: str

class OwnershipResolver:
    """
    Resolves ownership category for objects based on their characteristics.

    Resolution rules:
    1. If created by Piper → NATIVE
    2. If fetched from integration → FEDERATED
    3. If derived/computed → SYNTHETIC
    """

    NATIVE_SOURCES = {"piper", "system", "internal"}
    FEDERATED_SOURCES = {"github", "slack", "notion", "calendar", "linear"}

    def determine(
        self,
        source: str,
        created_by: str = "unknown",
        is_derived: bool = False,
        is_cached: bool = False
    ) -> OwnershipCategory:
        """Determine ownership category based on characteristics."""
        if is_derived:
            return OwnershipCategory.SYNTHETIC
        if source in self.NATIVE_SOURCES or created_by == "piper":
            return OwnershipCategory.NATIVE
        if source in self.FEDERATED_SOURCES:
            return OwnershipCategory.FEDERATED
        # Default to SYNTHETIC for unknown derived data
        return OwnershipCategory.SYNTHETIC

    def resolve(
        self,
        source: str,
        created_by: str = "unknown",
        is_derived: bool = False,
        is_cached: bool = False
    ) -> OwnershipResolution:
        """Full resolution with confidence and reasoning."""
        category = self.determine(source, created_by, is_derived, is_cached)

        # Calculate confidence based on how clear the determination is
        if source in self.NATIVE_SOURCES:
            confidence = 1.0
            reasoning = f"Source '{source}' is known internal source"
        elif source in self.FEDERATED_SOURCES:
            confidence = 0.95 if not is_cached else 0.9
            reasoning = f"Source '{source}' is known integration"
        elif is_derived:
            confidence = 0.85
            reasoning = "Object is derived/computed"
        else:
            confidence = 0.7
            reasoning = f"Unknown source '{source}', defaulting to {category.value}"

        return OwnershipResolution(
            category=category,
            confidence=confidence,
            reasoning=reasoning
        )
```

### Deliverables
- OwnershipResolver class
- Resolution tests

### Evidence Required
```bash
pytest tests/unit/services/mux/test_ownership.py -v 2>&1
```

---

## Phase 4: Transformation Tracking (30 min)

### Objective
Track when objects transform between ownership categories.

### TDD Sequence

**Step 4.1: Write tests FIRST**
```python
# Add to tests/unit/services/mux/test_ownership.py

from services.mux.ownership import OwnershipTransformation, OwnershipCategory

def test_valid_transformation_federated_to_synthetic():
    """FEDERATED → SYNTHETIC is valid (observation → understanding)."""
    transform = OwnershipTransformation(
        from_category=OwnershipCategory.FEDERATED,
        to_category=OwnershipCategory.SYNTHETIC
    )
    assert transform.is_valid()

def test_valid_transformation_synthetic_to_native():
    """SYNTHETIC → NATIVE is valid (understanding → memory)."""
    transform = OwnershipTransformation(
        from_category=OwnershipCategory.SYNTHETIC,
        to_category=OwnershipCategory.NATIVE
    )
    assert transform.is_valid()

def test_transformation_has_description():
    """Transformations have meaningful descriptions."""
    transform = OwnershipTransformation(
        from_category=OwnershipCategory.FEDERATED,
        to_category=OwnershipCategory.SYNTHETIC
    )
    assert "observation" in transform.description.lower() or "understanding" in transform.description.lower()
```

**Step 4.2: Implement Transformation Tracking**
```python
# Add to services/mux/ownership.py

@dataclass
class OwnershipTransformation:
    """
    Records transformation between ownership categories.

    Valid transformations:
    - FEDERATED → SYNTHETIC: Observation becomes understanding
    - SYNTHETIC → NATIVE: Understanding becomes memory
    - NATIVE → FEDERATED: Publishing internal state (rare)
    """
    from_category: OwnershipCategory
    to_category: OwnershipCategory
    timestamp: Optional[datetime] = None
    reason: str = ""

    VALID_TRANSFORMATIONS = {
        (OwnershipCategory.FEDERATED, OwnershipCategory.SYNTHETIC): "Observation becomes understanding",
        (OwnershipCategory.SYNTHETIC, OwnershipCategory.NATIVE): "Understanding becomes memory",
        (OwnershipCategory.NATIVE, OwnershipCategory.FEDERATED): "Publishing internal state",
    }

    def is_valid(self) -> bool:
        """Check if this transformation is valid."""
        return (self.from_category, self.to_category) in self.VALID_TRANSFORMATIONS

    @property
    def description(self) -> str:
        """Get description of this transformation."""
        key = (self.from_category, self.to_category)
        return self.VALID_TRANSFORMATIONS.get(key, "Unknown transformation")
```

### Deliverables
- OwnershipTransformation dataclass
- Transformation tests

### Evidence Required
```bash
pytest tests/unit/services/mux/test_ownership.py -v 2>&1
```

---

## Phase 5: Model Mapping Documentation (30 min)

### Objective
Document how existing domain models map to ownership categories.

### Tasks

**Step 5.1: Review domain models**
```bash
grep -n "^class " services/domain/models.py
```

**Step 5.2: Create mapping table**

| Domain Model | Ownership Category | Reasoning |
|--------------|-------------------|-----------|
| Session | NATIVE | Created by Piper |
| Memory | NATIVE | Piper's internal state |
| TrustState | NATIVE | Piper's assessment |
| GitHubIssue | FEDERATED | External observation |
| SlackMessage | FEDERATED | External observation |
| CalendarEvent | FEDERATED | External observation |
| ProjectHealth | SYNTHETIC | Derived from observations |
| RiskAssessment | SYNTHETIC | Computed understanding |

**Step 5.3: Update ADR-055 with mapping**

### Deliverables
- Model mapping table in ADR-055 appendix
- `services/mux/ownership.py` with MODEL_OWNERSHIP_MAP constant

### Evidence Required
```bash
grep "MODEL_OWNERSHIP_MAP" services/mux/ownership.py
```

---

## Phase Z: Completion & Handoff

### Required Actions

1. **Run full ownership test suite**
   ```bash
   pytest tests/unit/services/mux/test_ownership.py -v
   # Expected: 15+ tests passing
   ```

2. **Verify no regressions in P1**
   ```bash
   pytest tests/unit/services/mux/ -v --tb=short | tail -10
   # Expected: 115+ tests passing (101 P1 + 15+ P2)
   ```

3. **Smoke test verification**
   ```bash
   pytest tests/ -m smoke --tb=short | tail -5
   # Expected: 0 failures
   ```

4. **Update ADR-055 with ownership appendix**

5. **Update session log with completion evidence**

### Deliverables
- Updated ADR-055 with ownership appendix
- Completion matrix 100%

### Evidence Required
```bash
pytest tests/unit/services/mux/test_ownership.py -v 2>&1
pytest tests/ -m smoke --tb=no | tail -3
```

---

## Completion Matrix

| Deliverable | Target | Status | Evidence |
|-------------|--------|--------|----------|
| OwnershipCategory enum | 1 | ❌ | [pending] |
| HasOwnership protocol | 1 | ❌ | [pending] |
| OwnershipResolver | 1 | ❌ | [pending] |
| OwnershipTransformation | 1 | ❌ | [pending] |
| Model mapping table | 1 | ❌ | [pending] |
| ADR-055 appendix | 1 | ❌ | [pending] |
| Unit tests (15+) | 15+ | ❌ | [pending] |

**TOTAL: 0/7 deliverables = 0%**

Only claim "complete" when 7/7 = 100%.

---

## STOP Conditions

**Standard STOP conditions**:
- Infrastructure doesn't match assumptions
- Tests fail for any reason
- Pattern conflicts with P1 Protocols
- Can't provide verification evidence
- Completion bias detected

**Domain-specific STOP conditions**:
- Ownership categories don't map cleanly to existing models
- Transformation rules create circular dependencies
- Experience phrases feel forced/unnatural
- Model mapping reveals fundamental design issues

**When stopped**: Document the issue, provide options, wait for PM decision.

---

## Multi-Agent Deployment

### Recommendation: Single Agent, Sequential TDD

**Rationale**:
- Small scope (~4 hours)
- Sequential TDD pattern
- Extends existing module structure
- No parallelization opportunity

---

## Related Documentation

- Parent epic: #399
- Depends on: #613 (P1) - COMPLETE ✅
- P1 Implementation: `services/mux/` module
- ADR-045: Grammar definition
- ADR-055: Implementation specification
- Domain models: `services/domain/models.py`

---

*Gameplan created: 2026-01-19*
*Template version: v9.3*
