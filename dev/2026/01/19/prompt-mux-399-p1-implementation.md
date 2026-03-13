# Claude Code Agent Prompt: MUX-399-P1 Core Grammar & Lens Infrastructure

## Your Identity
You are Claude Code, a specialized development agent working on the Piper Morgan project. You follow systematic TDD methodology and provide evidence for all claims.

## Essential Context
Read these briefing documents first in knowledge/:
- BRIEFING-ESSENTIAL-AGENT.md - Your role requirements
- BRIEFING-CURRENT-STATE.md - Current epic and focus

Then read:
- `dev/2026/01/19/gameplan-mux-399-p1.md` - Full gameplan
- `dev/2026/01/19/p0-*.md` - P0 investigation findings (4 documents)

---

## CRITICAL: Post-Compaction Protocol

**If you just finished compacting**:

1. **STOP** - Do not continue working
2. **REPORT** - Summarize what was just completed
3. **ASK** - "Should I proceed to next task?"
4. **WAIT** - For explicit instructions

---

## CRITICAL: Evidence and Handoff Requirements

You are being deployed to complete GitHub Issue #613. Your work is part of a multi-phase coordination chain.

### Your Acceptance Criteria
- [ ] 3 Protocols defined and testable with isinstance() (PM will validate)
- [ ] Situation context manager works with async with (PM will validate)
- [ ] All 8 lenses implemented with NOTICING mode (PM will validate)
- [ ] LensSet compound perception working (PM will validate)
- [ ] >50 tests passing (PM will validate)
- [ ] 0 regressions in smoke tests (PM will validate)
- [ ] ADR-055 draft complete (PM will validate)

**Every checkbox must be addressed in your handoff.**

### Completion Matrix (Track Throughout)

| Deliverable | Target | Actual | Status |
|-------------|--------|--------|--------|
| EntityProtocol | 1 | 0 | Pending |
| MomentProtocol | 1 | 0 | Pending |
| PlaceProtocol | 1 | 0 | Pending |
| Situation | 1 | 0 | Pending |
| TemporalLens | 1 | 0 | Pending |
| HierarchyLens | 1 | 0 | Pending |
| PriorityLens | 1 | 0 | Pending |
| CollaborativeLens | 1 | 0 | Pending |
| FlowLens | 1 | 0 | Pending |
| QuantitativeLens | 1 | 0 | Pending |
| CausalLens | 1 | 0 | Pending |
| ContextualLens | 1 | 0 | Pending |
| LensSet | 1 | 0 | Pending |
| ADR-055 Draft | 1 | 0 | Pending |
| Unit Tests | 50+ | 0 | Pending |

**TOTAL: 0/14 deliverables = 0%**

Update this matrix as you complete work. Only claim "complete" when 14/14 = 100%.

### Your Handoff Format
```
## Issue #613 Completion Report
**Status**: Complete/Partial/Blocked

**Completion Matrix**:
[Updated matrix showing 14/14 = 100%]

**Tests**:
- X tests added in tests/unit/services/mux/
- `pytest tests/unit/services/mux/ -v` output: [paste actual output]

**Smoke Test Verification**:
```bash
pytest tests/ -m smoke
# [paste actual output showing 0 regressions]
```

**Files Created**:
- services/mux/__init__.py
- services/mux/protocols.py (+X lines)
- services/mux/situation.py (+X lines)
- services/mux/perception.py (+X lines)
- services/mux/lenses/__init__.py
- services/mux/lenses/base.py (+X lines)
- services/mux/lenses/temporal.py (+X lines)
- services/mux/lenses/hierarchy.py (+X lines)
- services/mux/lenses/priority.py (+X lines)
- services/mux/lenses/collaborative.py (+X lines)
- services/mux/lenses/flow.py (+X lines)
- services/mux/lenses/quantitative.py (+X lines)
- services/mux/lenses/causal.py (+X lines)
- services/mux/lenses/contextual.py (+X lines)
- services/mux/lenses/lens_set.py (+X lines)
- tests/unit/services/mux/*.py (X files)
- docs/internal/architecture/current/adrs/adr-055-object-model-implementation.md

**ADR-055 Draft Location**:
docs/internal/architecture/current/adrs/adr-055-object-model-implementation.md

**Blockers** (if any):
- [Blocker description and why it prevents completion]
```

---

## INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

### Verify Gameplan Assumptions FIRST
```bash
# 1. Verify services directory exists
ls -la services/

# 2. Check if mux directory already exists (should NOT)
ls -la services/mux/ 2>/dev/null || echo "services/mux/ does not exist (expected)"

# 3. Verify spatial integration locations from P0
ls -la services/intelligence/spatial/
ls -la services/integrations/spatial/

# 4. Verify ADR locations
ls -la docs/internal/architecture/current/adrs/adr-055* 2>/dev/null || echo "ADR-055 does not exist yet (expected)"

# 5. Verify Morning Standup reference
ls -la services/features/morning_standup.py

# 6. Check existing tests directory
ls -la tests/unit/services/
```

**If reality doesn't match gameplan**:
1. **STOP immediately**
2. **Report the mismatch with evidence**
3. **Wait for revised gameplan**

---

## Mission

Implement the foundational grammar abstractions for the MUX-VISION-OBJECT-MODEL epic:

1. **Protocol Definitions** - EntityProtocol, MomentProtocol, PlaceProtocol
2. **Situation Context Manager** - Async context manager for framing Moments
3. **Perception Infrastructure** - PerceptionMode enum and Perception dataclass
4. **Lens Infrastructure** - Base Lens class and 8 individual lens implementations
5. **LensSet** - Compound perception from multiple lenses
6. **ADR-055 Draft** - Implementation specification document

**Scope Boundaries**:
- This prompt covers ONLY: Core grammar infrastructure
- NOT in scope: Integration with existing services, user-facing features
- Future phases handle: Ownership model (P2), Lifecycle (P3), Metadata (P4)

---

## Context

- **GitHub Issue**: #613 - P1: Core Grammar & Lens Infrastructure
- **Current State**: P0 investigation complete, no implementation exists
- **Target State**: New `services/mux/` module with protocols, situation, lenses
- **Dependencies**: P0 findings in `dev/2026/01/19/p0-*.md`
- **User Data Risk**: None (new infrastructure, no user data affected)
- **Infrastructure Verified**: Awaiting your verification

---

## Implementation Approach (TDD)

### Phase 1: Protocol Definitions

**Step 1.1: Create module structure**
```bash
mkdir -p services/mux/lenses
touch services/mux/__init__.py
touch services/mux/protocols.py
touch services/mux/situation.py
touch services/mux/perception.py
touch services/mux/lenses/__init__.py

mkdir -p tests/unit/services/mux/lenses
touch tests/unit/services/mux/__init__.py
touch tests/unit/services/mux/conftest.py
```

**Step 1.2: Write Protocol tests FIRST**
```python
# tests/unit/services/mux/test_protocols.py
import pytest
from typing import runtime_checkable, Protocol

def test_entity_protocol_is_runtime_checkable():
    """EntityProtocol can be used with isinstance()"""
    from services.mux.protocols import EntityProtocol
    assert hasattr(EntityProtocol, '__runtime_checkable__') or runtime_checkable

def test_moment_protocol_is_runtime_checkable():
    """MomentProtocol can be used with isinstance()"""
    from services.mux.protocols import MomentProtocol
    # Similar to above

def test_place_protocol_is_runtime_checkable():
    """PlaceProtocol can be used with isinstance()"""
    from services.mux.protocols import PlaceProtocol
    # Similar to above

def test_role_fluidity_same_object_multiple_protocols():
    """Same object can satisfy Entity and Place protocols"""
    from services.mux.protocols import EntityProtocol, PlaceProtocol
    # Create object that satisfies both
    # Verify isinstance() works for both

def test_entity_requires_experiences_method():
    """EntityProtocol requires experiences() method"""

def test_moment_requires_captures_method():
    """MomentProtocol requires captures() method"""

def test_place_requires_contains_method():
    """PlaceProtocol requires contains() method"""
```

**Step 1.3: Run tests (expect failures)**
```bash
python -m pytest tests/unit/services/mux/test_protocols.py -v
# Expected: 7 tests FAILED (not yet implemented)
```

**Step 1.4: Implement Protocols**
See gameplan Phase 1 for implementation details.

**Step 1.5: Run tests (expect passes)**
```bash
python -m pytest tests/unit/services/mux/test_protocols.py -v
# Expected: 7 tests PASSED
```

**Evidence Required**:
```bash
# Capture this output
python -m pytest tests/unit/services/mux/test_protocols.py -v 2>&1
```

### Phase 2: Situation Context Manager

**Step 2.1: Write Situation tests FIRST**
```python
# tests/unit/services/mux/test_situation.py
import pytest

@pytest.mark.asyncio
async def test_situation_is_async_context_manager():
    """Situation can be used with async with"""

@pytest.mark.asyncio
async def test_situation_captures_moments():
    """Moments added during situation are captured"""

@pytest.mark.asyncio
async def test_situation_has_dramatic_tension():
    """Situation carries tension description"""

@pytest.mark.asyncio
async def test_situation_extracts_learning_on_exit():
    """Exiting situation produces learning"""
```

**Step 2.2: Run tests, implement, run tests**

**Evidence Required**:
```bash
python -m pytest tests/unit/services/mux/test_situation.py -v 2>&1
```

### Phase 3: Lens Infrastructure

**Step 3.1: Perception and PerceptionMode**
```bash
python -m pytest tests/unit/services/mux/test_perception.py -v 2>&1
```

**Step 3.2: Lens Base Class**
```bash
python -m pytest tests/unit/services/mux/lenses/test_lens_base.py -v 2>&1
```

**Step 3.3: Individual Lenses (8 total)**

For EACH lens, follow this pattern:
1. Write 3+ tests in `tests/unit/services/mux/lenses/test_[lens].py`
2. Run tests (expect fail)
3. Implement in `services/mux/lenses/[lens].py`
4. Run tests (expect pass)
5. Capture evidence

**Lenses to implement**:
| # | Lens | Test File | Implementation |
|---|------|-----------|----------------|
| 1 | Temporal | test_temporal.py | temporal.py |
| 2 | Hierarchy | test_hierarchy.py | hierarchy.py |
| 3 | Priority | test_priority.py | priority.py |
| 4 | Collaborative | test_collaborative.py | collaborative.py |
| 5 | Flow | test_flow.py | flow.py |
| 6 | Quantitative | test_quantitative.py | quantitative.py |
| 7 | Causal | test_causal.py | causal.py |
| 8 | Contextual | test_contextual.py | contextual.py |

**Step 3.4: LensSet**
```bash
python -m pytest tests/unit/services/mux/lenses/test_lens_set.py -v 2>&1
```

### Phase 4: Visual Diagram

Create mermaid diagram in ADR-055 (see gameplan for content).

### Phase 5: ADR-055 Draft

Create `docs/internal/architecture/current/adrs/adr-055-object-model-implementation.md`:
- Status: Proposed
- Context: P0 findings
- Decision: Implementation approach
- Protocol definitions
- Lens architecture
- Diagram
- References to ADR-038, ADR-045

### Phase Z: Completion

**Run full test suite**:
```bash
python -m pytest tests/unit/services/mux/ -v 2>&1 | tee p1-test-results.txt
# Must show 50+ tests passing
```

**Verify no regressions**:
```bash
python -m pytest tests/ -m smoke 2>&1 | tee p1-smoke-results.txt
# Must show 0 failures
```

---

## Verification Gates

| Gate | Command | Expected |
|------|---------|----------|
| Phase 1 Complete | `pytest tests/unit/services/mux/test_protocols.py -v` | 7 tests pass |
| Phase 2 Complete | `pytest tests/unit/services/mux/test_situation.py -v` | 4 tests pass |
| Phase 3.1 Complete | `pytest tests/unit/services/mux/test_perception.py -v` | 3 tests pass |
| Phase 3.2 Complete | `pytest tests/unit/services/mux/lenses/test_lens_base.py -v` | 3 tests pass |
| Phase 3.3 Complete | `pytest tests/unit/services/mux/lenses/test_*.py -v` | 24+ tests pass |
| Phase 3.4 Complete | `pytest tests/unit/services/mux/lenses/test_lens_set.py -v` | 3+ tests pass |
| Phase Z Complete | `pytest tests/unit/services/mux/ -v` | 50+ tests pass |
| Regression Check | `pytest tests/ -m smoke` | 0 failures |

---

## STOP Conditions

**STOP immediately and escalate if**:
- Protocol pattern doesn't support role fluidity with isinstance()
- Existing spatial infrastructure can't be called from lenses
- Performance concerns with @runtime_checkable (measure first)
- "Flattening" detected (code feels like database schema, not grammar)
- Architectural conflict with existing patterns
- Tests fail and you're unsure why
- Any assumption needs to be made

**When stopped**: Document the issue, provide options, wait for PM decision.

---

## Key P0 Findings to Remember

1. **Lenses must be CREATED, not wrapped** - No `services/spatial/dimensions/*.py` exists
2. **Use Direct Integration (Option B)** - Lenses call `integration.dimensions["TEMPORAL"](target)`
3. **Morning Standup patterns** - Reference `services/features/morning_standup.py` for consciousness preservation
4. **8 dimensions = 8 lenses** - Map from ADR-038 spatial dimensions
5. **Situation is a frame, not substrate** - Async context manager, not fourth substrate

---

## Session Log

Create or append to: `dev/2026/01/19/2026-01-19-HHMM-p1-code-log.md`

Include:
- Start time
- Infrastructure verification results
- Each phase completion with evidence
- Any blockers or decisions
- End time and completion status

---

## Self-Check Before Claiming Complete

1. Is completion matrix 14/14 = 100%?
2. Did I provide test output for every phase?
3. Can someone else run `pytest tests/unit/services/mux/ -v` and see 50+ passing?
4. Did smoke tests show 0 regressions?
5. Does ADR-055 draft exist?
6. Am I rationalizing any gaps as "minor"?
7. Do I have evidence, not just assertions?

---

## Related Documentation

- Gameplan: `dev/2026/01/19/gameplan-mux-399-p1.md`
- P0 Investigation: `dev/2026/01/19/p0-*.md`
- ADR-038: `docs/internal/architecture/current/adrs/adr-038-spatial-intelligence-patterns.md`
- ADR-045: `docs/internal/architecture/current/adrs/adr-045-object-model.md`
- Morning Standup: `services/features/morning_standup.py`

---

*Prompt created: 2026-01-19*
*Template version: v10.2*
