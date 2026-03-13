# Claude Code Agent Prompt: MUX-399-P2 Ownership Model

## Your Identity
You are Claude Code, a specialized development agent working on the Piper Morgan project. You follow systematic TDD methodology and provide evidence for all claims.

## Essential Context
Read these briefing documents first in knowledge/:
- BRIEFING-ESSENTIAL-AGENT.md - Your role requirements
- BRIEFING-CURRENT-STATE.md - Current epic and focus

Then read:
- `dev/2026/01/19/gameplan-mux-399-p2.md` - Full gameplan
- `services/mux/protocols.py` - P1 Protocol patterns to follow

---

## CRITICAL: Post-Compaction Protocol

**If you just finished compacting**:

1. **STOP** - Do not continue working
2. **REPORT** - Summarize what was just completed
3. **ASK** - "Should I proceed to next task?"
4. **WAIT** - For explicit instructions

---

## CRITICAL: Evidence and Handoff Requirements

You are being deployed to complete GitHub Issue #614. Your work is part of a multi-phase coordination chain.

### Your Acceptance Criteria
- [ ] OwnershipCategory enum defined with NATIVE, FEDERATED, SYNTHETIC (PM will validate)
- [ ] HasOwnership protocol defined and @runtime_checkable (PM will validate)
- [ ] Objects can be checked with isinstance(obj, HasOwnership) (PM will validate)
- [ ] OwnershipResolver correctly categorizes test cases (PM will validate)
- [ ] Transformation rules defined and logged (PM will validate)
- [ ] Model mapping table complete in ADR-055 appendix (PM will validate)
- [ ] >15 tests passing (PM will validate)
- [ ] 0 regressions in smoke tests (PM will validate)

**Every checkbox must be addressed in your handoff.**

### Completion Matrix (Track Throughout)

| Deliverable | Target | Actual | Status |
|-------------|--------|--------|--------|
| OwnershipCategory enum | 1 | 0 | Pending |
| HasOwnership protocol | 1 | 0 | Pending |
| OwnershipResolver | 1 | 0 | Pending |
| OwnershipResolution | 1 | 0 | Pending |
| OwnershipTransformation | 1 | 0 | Pending |
| Model mapping (ADR-055) | 1 | 0 | Pending |
| Unit Tests | 15+ | 0 | Pending |

**TOTAL: 0/7 deliverables = 0%**

Update this matrix as you complete work. Only claim "complete" when 7/7 = 100%.

### Your Handoff Format
```
## Issue #614 Completion Report
**Status**: Complete/Partial/Blocked

**Completion Matrix**:
[Updated matrix showing 7/7 = 100%]

**Tests**:
- X tests added in tests/unit/services/mux/test_ownership.py
- `pytest tests/unit/services/mux/test_ownership.py -v` output: [paste actual output]

**Smoke Test Verification**:
```bash
pytest tests/ -m smoke
# [paste actual output showing 0 regressions]
```

**Files Created/Modified**:
- services/mux/ownership.py (+X lines)
- tests/unit/services/mux/test_ownership.py (+X lines)
- docs/internal/architecture/current/adrs/adr-055-object-model-implementation.md (appendix added)

**ADR-055 Appendix Location**:
docs/internal/architecture/current/adrs/adr-055-object-model-implementation.md

**Blockers** (if any):
- [Blocker description and why it prevents completion]
```

---

## INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

### Verify Gameplan Assumptions FIRST
```bash
# 1. Verify P1 infrastructure exists and tests pass
ls -la services/mux/
pytest tests/unit/services/mux/ -v --tb=no | tail -5
# Expected: 101 tests passing

# 2. Check P1 protocols.py for pattern reference
head -50 services/mux/protocols.py

# 3. Verify ownership.py does NOT exist yet (should NOT)
ls -la services/mux/ownership.py 2>/dev/null || echo "ownership.py does not exist (expected)"

# 4. Verify ADR-055 exists for appendix
ls -la docs/internal/architecture/current/adrs/adr-055*

# 5. Review domain models for mapping
grep -n "^class " services/domain/models.py | head -20

# 6. Verify test location
ls -la tests/unit/services/mux/
```

**If reality doesn't match gameplan**:
1. **STOP immediately**
2. **Report the mismatch with evidence**
3. **Wait for revised gameplan**

---

## Mission

Implement the three-category ownership model describing Piper's relationship to objects:

1. **OwnershipCategory Enum** - NATIVE, FEDERATED, SYNTHETIC with metaphors
2. **HasOwnership Protocol** - @runtime_checkable protocol for ownership-aware objects
3. **OwnershipResolver** - Automatic category determination
4. **OwnershipTransformation** - Track transformations between categories
5. **Model Mapping** - Document existing models' ownership categories

**Scope Boundaries**:
- This prompt covers ONLY: Ownership infrastructure
- NOT in scope: Migrating existing models, UI changes, permission systems
- Future phases handle: Lifecycle (P3), Metadata (P4)

---

## Context

- **GitHub Issue**: #614 - P2: Ownership Model (Native/Federated/Synthetic)
- **Current State**: P1 complete (101 tests), ownership infrastructure needed
- **Target State**: `services/mux/ownership.py` with protocols, resolver, transformations
- **Dependencies**: P1 (`services/mux/protocols.py`) - COMPLETE ✅
- **User Data Risk**: None (new infrastructure, no user data affected)
- **Infrastructure Verified**: Awaiting your verification

---

## Implementation Approach (TDD)

### Phase 1: OwnershipCategory Enum

**Step 1.1: Write tests FIRST**
```python
# tests/unit/services/mux/test_ownership.py
import pytest
from services.mux.ownership import OwnershipCategory

class TestOwnershipCategoryBasics:
    def test_has_native_category(self):
        """NATIVE category exists for Piper's Mind."""
        assert OwnershipCategory.NATIVE is not None
        assert OwnershipCategory.NATIVE.value == "native"

    def test_has_federated_category(self):
        """FEDERATED category exists for Piper's Senses."""
        assert OwnershipCategory.FEDERATED is not None
        assert OwnershipCategory.FEDERATED.value == "federated"

    def test_has_synthetic_category(self):
        """SYNTHETIC category exists for Piper's Understanding."""
        assert OwnershipCategory.SYNTHETIC is not None
        assert OwnershipCategory.SYNTHETIC.value == "synthetic"

class TestOwnershipCategoryMetaphors:
    def test_native_has_metaphor(self):
        """NATIVE has consciousness metaphor."""
        assert "Mind" in OwnershipCategory.NATIVE.metaphor

    def test_federated_has_metaphor(self):
        """FEDERATED has consciousness metaphor."""
        assert "Senses" in OwnershipCategory.FEDERATED.metaphor

    def test_synthetic_has_metaphor(self):
        """SYNTHETIC has consciousness metaphor."""
        assert "Understanding" in OwnershipCategory.SYNTHETIC.metaphor

class TestOwnershipCategoryExperiencePhrases:
    def test_native_experience_phrase(self):
        """NATIVE has experience phrase."""
        assert "created" in OwnershipCategory.NATIVE.experience_phrase.lower()

    def test_federated_experience_phrase(self):
        """FEDERATED has experience phrase."""
        assert "see" in OwnershipCategory.FEDERATED.experience_phrase.lower()

    def test_synthetic_experience_phrase(self):
        """SYNTHETIC has experience phrase."""
        assert "understand" in OwnershipCategory.SYNTHETIC.experience_phrase.lower()
```

**Step 1.2: Run tests (expect failures)**
```bash
pytest tests/unit/services/mux/test_ownership.py -v
# Expected: 9 tests FAILED (not yet implemented)
```

**Step 1.3: Implement OwnershipCategory**
```python
# services/mux/ownership.py
"""
Ownership model for Piper's relationship to knowledge.

This module defines how Piper relates to objects:
- NATIVE: Piper's Mind - what Piper creates/owns directly
- FEDERATED: Piper's Senses - what Piper observes externally
- SYNTHETIC: Piper's Understanding - what Piper constructs through reasoning
"""
from enum import Enum
from dataclasses import dataclass
from typing import Protocol, runtime_checkable, Optional
from datetime import datetime


class OwnershipCategory(Enum):
    """
    Describes Piper's epistemological relationship to knowledge.

    The three categories represent how Piper knows things:
    - NATIVE: "I know this because I created it" (Mind)
    - FEDERATED: "I see this in [Place]" (Senses)
    - SYNTHETIC: "I understand this to mean..." (Understanding)
    """

    NATIVE = "native"
    FEDERATED = "federated"
    SYNTHETIC = "synthetic"

    @property
    def description(self) -> str:
        """Detailed description of this ownership category."""
        descriptions = {
            OwnershipCategory.NATIVE: (
                "Objects Piper creates and owns directly - "
                "sessions, memories, trust states, learning"
            ),
            OwnershipCategory.FEDERATED: (
                "Objects Piper observes from external sources - "
                "GitHub issues, Slack messages, calendar events"
            ),
            OwnershipCategory.SYNTHETIC: (
                "Objects Piper constructs through reasoning - "
                "inferred status, assembled risk, pattern recognition"
            ),
        }
        return descriptions[self]

    @property
    def metaphor(self) -> str:
        """Consciousness metaphor for this category."""
        metaphors = {
            OwnershipCategory.NATIVE: "Piper's Mind",
            OwnershipCategory.FEDERATED: "Piper's Senses",
            OwnershipCategory.SYNTHETIC: "Piper's Understanding",
        }
        return metaphors[self]

    @property
    def experience_phrase(self) -> str:
        """How Piper expresses knowledge from this category."""
        phrases = {
            OwnershipCategory.NATIVE: "I know this because I created it",
            OwnershipCategory.FEDERATED: "I see this in {place}",
            OwnershipCategory.SYNTHETIC: "I understand this to mean...",
        }
        return phrases[self]
```

**Step 1.4: Run tests (expect passes)**
```bash
pytest tests/unit/services/mux/test_ownership.py::TestOwnershipCategoryBasics -v
pytest tests/unit/services/mux/test_ownership.py::TestOwnershipCategoryMetaphors -v
pytest tests/unit/services/mux/test_ownership.py::TestOwnershipCategoryExperiencePhrases -v
# Expected: 9 tests PASSED
```

**Evidence Required**:
```bash
pytest tests/unit/services/mux/test_ownership.py -v 2>&1 | head -30
```

### Phase 2: HasOwnership Protocol

**Step 2.1: Write tests FIRST**
```python
# Add to tests/unit/services/mux/test_ownership.py

from services.mux.ownership import HasOwnership, OwnershipCategory

class TestHasOwnershipProtocol:
    def test_protocol_is_runtime_checkable(self):
        """HasOwnership can be used with isinstance()."""
        # Create mock object satisfying protocol
        class MockOwned:
            @property
            def ownership_category(self) -> OwnershipCategory:
                return OwnershipCategory.NATIVE

            @property
            def ownership_source(self) -> str:
                return "piper"

            @property
            def ownership_confidence(self) -> float:
                return 1.0

        obj = MockOwned()
        assert isinstance(obj, HasOwnership)

    def test_non_conforming_object_fails(self):
        """Objects without ownership properties don't satisfy protocol."""
        class NotOwned:
            pass

        obj = NotOwned()
        assert not isinstance(obj, HasOwnership)

    def test_protocol_requires_all_properties(self):
        """Protocol requires category, source, and confidence."""
        class PartialOwned:
            @property
            def ownership_category(self) -> OwnershipCategory:
                return OwnershipCategory.NATIVE
            # Missing source and confidence

        obj = PartialOwned()
        assert not isinstance(obj, HasOwnership)
```

**Step 2.2: Implement HasOwnership**
```python
# Add to services/mux/ownership.py

@runtime_checkable
class HasOwnership(Protocol):
    """
    Protocol for objects with ownership awareness.

    Any object can satisfy this protocol by providing:
    - ownership_category: Which category (NATIVE/FEDERATED/SYNTHETIC)
    - ownership_source: Where this object came from
    - ownership_confidence: How certain we are (0.0 to 1.0)

    Example:
        class MySession:
            @property
            def ownership_category(self) -> OwnershipCategory:
                return OwnershipCategory.NATIVE

            @property
            def ownership_source(self) -> str:
                return "piper"

            @property
            def ownership_confidence(self) -> float:
                return 1.0

        session = MySession()
        assert isinstance(session, HasOwnership)  # True
    """

    @property
    def ownership_category(self) -> OwnershipCategory:
        """The ownership category of this object."""
        ...

    @property
    def ownership_source(self) -> str:
        """The source/origin (e.g., 'piper', 'github', 'inference')."""
        ...

    @property
    def ownership_confidence(self) -> float:
        """Confidence in ownership categorization (0.0 to 1.0)."""
        ...
```

**Evidence Required**:
```bash
pytest tests/unit/services/mux/test_ownership.py::TestHasOwnershipProtocol -v 2>&1
```

### Phase 3: OwnershipResolver

**Step 3.1: Write tests FIRST**
```python
# Add to tests/unit/services/mux/test_ownership.py

from services.mux.ownership import OwnershipResolver, OwnershipResolution

class TestOwnershipResolverDetermination:
    def test_native_for_piper_created(self):
        """Objects created by Piper are NATIVE."""
        resolver = OwnershipResolver()
        category = resolver.determine(source="piper", created_by="piper")
        assert category == OwnershipCategory.NATIVE

    def test_native_for_system_source(self):
        """Objects from system/internal are NATIVE."""
        resolver = OwnershipResolver()
        category = resolver.determine(source="system")
        assert category == OwnershipCategory.NATIVE

    def test_federated_for_github(self):
        """Objects from GitHub are FEDERATED."""
        resolver = OwnershipResolver()
        category = resolver.determine(source="github")
        assert category == OwnershipCategory.FEDERATED

    def test_federated_for_slack(self):
        """Objects from Slack are FEDERATED."""
        resolver = OwnershipResolver()
        category = resolver.determine(source="slack")
        assert category == OwnershipCategory.FEDERATED

    def test_synthetic_for_derived(self):
        """Derived/computed objects are SYNTHETIC."""
        resolver = OwnershipResolver()
        category = resolver.determine(source="inference", is_derived=True)
        assert category == OwnershipCategory.SYNTHETIC

    def test_cached_federated_remains_federated(self):
        """Cached federated data remains FEDERATED."""
        resolver = OwnershipResolver()
        category = resolver.determine(source="github", is_cached=True)
        assert category == OwnershipCategory.FEDERATED


class TestOwnershipResolverResolution:
    def test_resolution_includes_confidence(self):
        """Resolution provides confidence score."""
        resolver = OwnershipResolver()
        result = resolver.resolve(source="github")
        assert isinstance(result, OwnershipResolution)
        assert 0.0 <= result.confidence <= 1.0

    def test_resolution_includes_reasoning(self):
        """Resolution explains the determination."""
        resolver = OwnershipResolver()
        result = resolver.resolve(source="piper")
        assert result.reasoning
        assert len(result.reasoning) > 0
```

**Step 3.2: Implement OwnershipResolver**
See gameplan Phase 3 for implementation details.

**Evidence Required**:
```bash
pytest tests/unit/services/mux/test_ownership.py::TestOwnershipResolverDetermination -v 2>&1
pytest tests/unit/services/mux/test_ownership.py::TestOwnershipResolverResolution -v 2>&1
```

### Phase 4: Transformation Tracking

**Step 4.1: Write tests FIRST**
```python
# Add to tests/unit/services/mux/test_ownership.py

from services.mux.ownership import OwnershipTransformation

class TestOwnershipTransformation:
    def test_federated_to_synthetic_is_valid(self):
        """FEDERATED → SYNTHETIC is valid (observation → understanding)."""
        transform = OwnershipTransformation(
            from_category=OwnershipCategory.FEDERATED,
            to_category=OwnershipCategory.SYNTHETIC
        )
        assert transform.is_valid()

    def test_synthetic_to_native_is_valid(self):
        """SYNTHETIC → NATIVE is valid (understanding → memory)."""
        transform = OwnershipTransformation(
            from_category=OwnershipCategory.SYNTHETIC,
            to_category=OwnershipCategory.NATIVE
        )
        assert transform.is_valid()

    def test_transformation_has_description(self):
        """Transformations have meaningful descriptions."""
        transform = OwnershipTransformation(
            from_category=OwnershipCategory.FEDERATED,
            to_category=OwnershipCategory.SYNTHETIC
        )
        assert transform.description
        assert len(transform.description) > 0
```

**Step 4.2: Implement OwnershipTransformation**
See gameplan Phase 4 for implementation details.

**Evidence Required**:
```bash
pytest tests/unit/services/mux/test_ownership.py::TestOwnershipTransformation -v 2>&1
```

### Phase 5: Model Mapping Documentation

**Step 5.1: Review domain models**
```bash
grep -n "^class " services/domain/models.py | head -30
```

**Step 5.2: Create mapping in ADR-055 appendix**

Add to `docs/internal/architecture/current/adrs/adr-055-object-model-implementation.md`:

```markdown
## Appendix: Ownership Model Mapping

### Domain Model Ownership Categories

| Domain Model | Ownership Category | Reasoning |
|--------------|-------------------|-----------|
| Session | NATIVE | Created by Piper |
| Memory | NATIVE | Piper's internal state |
| Concern | NATIVE | Piper's tracked concern |
| TrustState | NATIVE | Piper's trust assessment |
| UserPreference | NATIVE | Piper-stored preference |
| GitHubIssue | FEDERATED | External observation |
| GitHubPR | FEDERATED | External observation |
| SlackMessage | FEDERATED | External observation |
| CalendarEvent | FEDERATED | External observation |
| NotionPage | FEDERATED | External observation |
| ProjectHealth | SYNTHETIC | Derived from observations |
| RiskAssessment | SYNTHETIC | Computed understanding |
| TaskPriority | SYNTHETIC | Inferred importance |

### Ownership Constant Map

```python
# services/mux/ownership.py
MODEL_OWNERSHIP_MAP = {
    "Session": OwnershipCategory.NATIVE,
    "Memory": OwnershipCategory.NATIVE,
    "Concern": OwnershipCategory.NATIVE,
    "TrustState": OwnershipCategory.NATIVE,
    "GitHubIssue": OwnershipCategory.FEDERATED,
    "GitHubPR": OwnershipCategory.FEDERATED,
    "SlackMessage": OwnershipCategory.FEDERATED,
    "CalendarEvent": OwnershipCategory.FEDERATED,
    "NotionPage": OwnershipCategory.FEDERATED,
    "ProjectHealth": OwnershipCategory.SYNTHETIC,
    "RiskAssessment": OwnershipCategory.SYNTHETIC,
}
```
```

### Phase Z: Completion

**Run full ownership test suite**:
```bash
pytest tests/unit/services/mux/test_ownership.py -v 2>&1 | tee p2-test-results.txt
# Must show 15+ tests passing
```

**Verify no regressions in P1**:
```bash
pytest tests/unit/services/mux/ -v --tb=short | tail -10
# Expected: 115+ tests passing (101 P1 + 15+ P2)
```

**Verify no regressions in smoke**:
```bash
pytest tests/ -m smoke 2>&1 | tail -5
# Must show 0 failures
```

---

## Verification Gates

| Gate | Command | Expected |
|------|---------|----------|
| Phase 1 Complete | `pytest tests/unit/services/mux/test_ownership.py -k "CategoryBasics or CategoryMetaphors or CategoryExperience" -v` | 9 tests pass |
| Phase 2 Complete | `pytest tests/unit/services/mux/test_ownership.py -k "HasOwnership" -v` | 3 tests pass |
| Phase 3 Complete | `pytest tests/unit/services/mux/test_ownership.py -k "Resolver" -v` | 8 tests pass |
| Phase 4 Complete | `pytest tests/unit/services/mux/test_ownership.py -k "Transformation" -v` | 3 tests pass |
| Phase Z Complete | `pytest tests/unit/services/mux/test_ownership.py -v` | 15+ tests pass |
| No P1 Regressions | `pytest tests/unit/services/mux/ -v` | 115+ tests pass |
| Smoke Check | `pytest tests/ -m smoke` | 0 failures |

---

## STOP Conditions

**STOP immediately and escalate if**:
- P1 tests fail (dependency broken)
- @runtime_checkable doesn't work for HasOwnership
- Ownership categories don't map cleanly to existing models
- Transformation rules create circular dependencies
- Experience phrases feel forced/unnatural
- "Flattening" detected (code feels like database schema, not consciousness)
- Tests fail and you're unsure why
- Any assumption needs to be made

**When stopped**: Document the issue, provide options, wait for PM decision.

---

## Key Patterns from P1 to Follow

1. **@runtime_checkable Protocols** - Use same pattern as EntityProtocol
2. **Property-based interface** - Use @property for protocol methods
3. **Consciousness metaphors** - "Piper's Mind", "Piper's Senses", etc.
4. **Experience framing** - "I know...", "I see...", "I understand..."
5. **Test structure** - Class-based test organization by feature

---

## Session Log

Create or append to: `dev/2026/01/19/2026-01-19-HHMM-p2-code-log.md`

Include:
- Start time
- Infrastructure verification results
- Each phase completion with evidence
- Any blockers or decisions
- End time and completion status

---

## Self-Check Before Claiming Complete

1. Is completion matrix 7/7 = 100%?
2. Did I provide test output for every phase?
3. Can someone else run `pytest tests/unit/services/mux/test_ownership.py -v` and see 15+ passing?
4. Did P1 tests still pass (101 tests)?
5. Did smoke tests show 0 regressions?
6. Does ADR-055 appendix with model mapping exist?
7. Am I rationalizing any gaps as "minor"?
8. Do I have evidence, not just assertions?

---

## Related Documentation

- Gameplan: `dev/2026/01/19/gameplan-mux-399-p2.md`
- P1 Implementation: `services/mux/protocols.py` (pattern reference)
- ADR-045: `docs/internal/architecture/current/adrs/adr-045-object-model.md`
- ADR-055: `docs/internal/architecture/current/adrs/adr-055-object-model-implementation.md`
- Domain Models: `services/domain/models.py`

---

*Prompt created: 2026-01-19*
*Template version: v10.2*
