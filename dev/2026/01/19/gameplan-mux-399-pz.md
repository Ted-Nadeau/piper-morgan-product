# Gameplan: MUX-399-PZ Verification & Anti-Flattening Tests

**GitHub Issue**: #618
**Epic**: #399 MUX-VISION-OBJECT-MODEL
**Dependencies**: #612 (P0), #613 (P1), #614 (P2), #615 (P3), #616 (P4), #617 (P4.5) - All Complete
**Estimated Effort**: ~4 hours
**Template Version**: v9.3

---

## Phase -1: Infrastructure Verification Checkpoint (MANDATORY)

### Part A: Lead Developer's Current Understanding

**Infrastructure Status**:
- [x] P0 Investigation: Complete
- [x] P1 Protocols: 101 tests (protocols.py)
- [x] P2 Ownership: 25 tests (ownership.py)
- [x] P3 Lifecycle: 69 tests (lifecycle.py)
- [x] P4 Metadata: 67 tests (metadata.py)
- [x] P4.5 Grammar Validation: 100% coverage (63/63 queries)
- [x] ADR-055: Draft with Appendix A-D
- [x] Total MUX tests: 262

**My understanding of the task**:
- Create anti-flattening test suite that catches "consciousness regression"
- Write experience-language tests verifying grammar expressiveness
- Create implementation guide for future developers
- Finalize ADR-055 for acceptance
- Obtain PM/CXO sign-off (async, documented)
- Write final experience checkpoint

**Note**: Some deliverables (PM/CXO sign-off) require human review. Agent will prepare materials and document for review.

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

Worktrees ADD value when:
- [ ] Multiple agents will work in parallel (single agent)
- [x] Task duration >30 minutes (~4 hours)
- [ ] Multi-component work (test suite + docs)
- [ ] Exploratory/risky changes (verification, not feature)

Worktrees ADD overhead when:
- [x] Single agent, sequential work
- [ ] Small fixes (<15 min)
- [x] Tightly coupled files requiring atomic commits
- [x] Verification/documentation work (no risky changes)

**Assessment:**
- [x] **SKIP WORKTREE** - Single agent, verification and documentation work. No risky code changes.

### Part B: PM Verification Required

**Verification Commands (Agent will run):**
```bash
# Verify all MUX modules exist
ls -la services/mux/

# Verify combined MUX test count (262 expected)
pytest tests/unit/services/mux/ --collect-only -q | tail -3

# Verify ADR-055 exists with all appendices
grep "Appendix" docs/internal/architecture/current/adrs/adr-055-object-model-implementation.md

# Check for existing anti-flattening tests
ls tests/unit/services/mux/test_anti_flattening.py 2>/dev/null || echo "Not yet created"

# Verify P4.5 coverage in ADR
grep "100%" docs/internal/architecture/current/adrs/adr-055-object-model-implementation.md | head -3
```

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - All P0-P4.5 complete (262 tests), ADR-055 exists with appendices, ready for verification phase

---

## Phase 0: Initial Bookending - GitHub Investigation

**Skip**: Issue #618 already verified as open and ready for implementation.

### Phase 0.5-0.8: Conditional Phases

**Phase 0.5 (Frontend-Backend Contract)**: N/A - No UI work
**Phase 0.6 (Data Flow)**: N/A - Verification tests only
**Phase 0.7 (Conversation Design)**: N/A - Not conversational
**Phase 0.8 (Post-Completion)**: N/A - No user state changes

---

## Phase 1: Technical Anti-Flattening Tests (TDD)

**Objective**: Create test suite that catches "consciousness regression"

### Tests First
```python
# tests/unit/services/mux/test_anti_flattening.py

"""
Anti-Flattening Test Suite

These tests verify that the MUX implementation preserves consciousness
rather than flattening to mere database schema.

Pass condition: Grammar concepts express experience
Fail condition: Implementation reduces to data manipulation
"""

import pytest
from services.mux.protocols import EntityProtocol, MomentProtocol, PlaceProtocol
from services.mux.ownership import OwnershipCategory, HasOwnership
from services.mux.lifecycle import LifecycleState, CompostingExtractor
from services.mux.metadata import Provenance, Journal, JournalManager


class TestEntityPreservesIdentity:
    """Entities are actors with identity, not just data records"""

    def test_entity_has_identity_not_just_id(self):
        """Entity identity is more than database ID"""
        # Entity must have name/identity that describes WHO it is
        # Not just what its primary key is

    def test_entity_has_agency(self):
        """Entities can act, not just be acted upon"""
        # Entity protocol should enable action, not just storage

    def test_entity_memory_persists(self):
        """Entity identity persists across contexts"""
        # Same entity recognized in different situations


class TestMomentPreservesSignificance:
    """Moments are bounded scenes, not timestamps"""

    def test_moment_has_boundaries(self):
        """Moments have beginning/middle/end structure"""
        # Not just start_time/end_time

    def test_moment_captures_significance(self):
        """Moments record why they matter, not just that they occurred"""
        # Insight journal captures meaning

    def test_moment_can_be_remembered(self):
        """Moments are memorable, not just queryable"""
        # Experience framing: "Remember when..." not "Query returned..."


class TestPlacePreservesAtmosphere:
    """Places have character, not just configuration"""

    def test_place_has_atmosphere(self):
        """Places have modality describing how interaction happens"""
        # Not just connection strings

    def test_place_contains_not_just_references(self):
        """Places contain their contents, not just point to them"""
        # Spatial relationship, not foreign keys

    def test_place_has_affordances(self):
        """Places describe what can happen there"""
        # GitHub affords issues; Calendar affords meetings


class TestSituationPreservesFrame:
    """Situations frame experience, not just enumerate state"""

    def test_situation_has_dramatic_tension(self):
        """Situations capture what's at stake"""
        # Not just current_state

    def test_situation_captures_learning_on_exit(self):
        """Exiting a situation extracts insight"""
        # Composting pattern

    def test_situation_frames_not_enumerates(self):
        """Situations provide context, not just list contents"""
        # "Morning standup situation" vs "meeting + tasks + PRs"


class TestLifecyclePreservesTransformation:
    """Lifecycle includes composting, not just deletion"""

    def test_composting_extracts_learning(self):
        """Composting transforms objects into wisdom"""
        extractor = CompostingExtractor()
        # Result should have lessons, not just "deleted"

    def test_lifecycle_tells_story(self):
        """Lifecycle history is narrative, not audit log"""
        # "This emerged, was noticed, ratified, and composted"
        # Not "status changed from X to Y"

    def test_nothing_truly_deleted(self):
        """Composted objects leave behind learning"""
        # "Nothing disappears, it transforms"
```

### Implementation Notes
- Tests verify CONCEPTS, not just code
- Each test documents pass/fail conditions in experience language
- Tests should fail if someone reduces grammar to database schema

**Deliverable**: `tests/unit/services/mux/test_anti_flattening.py` (20+ tests)

**Verification Command**:
```bash
pytest tests/unit/services/mux/test_anti_flattening.py -xvs
```

**Verification Gate**: 20+ anti-flattening tests passing

---

## Phase 2: Design Anti-Flattening Tests

**Objective**: Document CXO design principle compliance

### Design Principles to Verify

| Principle | Pass | Fail |
|-----------|------|------|
| Response framing | "I notice..." | "Found X results" |
| Empty states | "Nothing here yet..." | "No data" |
| Error handling | "I couldn't reach..." | "Operation failed" |
| History display | Moments by significance | Timestamp list |
| Entity references | Names and relationships | IDs and labels |

### Tests or Documentation
```python
class TestDesignAntiFlattening:
    """Design principles from CXO memo"""

    def test_response_framing_uses_experience_language(self):
        """Responses say 'I notice' not 'Found X results'"""
        # Verify experience framing in protocol definitions

    def test_empty_states_have_atmosphere(self):
        """Empty states acknowledge absence, not report zero"""
        # Verify empty state messages in protocols

    def test_lifecycle_states_have_experience_phrases(self):
        """Each lifecycle state has experience_phrase attribute"""
        for state in LifecycleState:
            assert hasattr(state, 'experience_phrase')
```

**Deliverable**: Design anti-flattening tests OR documentation checklist

**Verification Gate**: All design principles verified

---

## Phase 3: Experience Tests Documentation

**Objective**: Document that features are expressible in grammar

### Morning Standup (Reference Implementation)
```markdown
## Morning Standup Experience Description

**Grammar Expression**:
- **Entity**: User (you) and Piper (assistant)
- **Moment**: The standup conversation (bounded, has beginning/end)
- **Place**: Calendar (where meetings live) + GitHub (where work lives)
- **Lenses**: Temporal (today), Priority (what matters), Collaborative (team)
- **Situation**: "Preparing for the day" frame with tension (what needs attention?)

**Experience Language** (PASS):
- "Piper noticed that you have 3 meetings today"
- "Piper remembers that you completed 2 PRs yesterday"
- "Piper anticipates a busy afternoon"

**Database Language** (FAIL):
- "Query returned 3 calendar events"
- "Found 2 merged PRs in date range"
- "Calculated meeting density > threshold"
```

**Deliverable**: Experience test documentation for major features

---

## Phase 4: Implementation Guide

**Objective**: Create guide for future developers

### Guide Structure
```markdown
# MUX Implementation Guide

## Core Concepts
- Entities experience Moments in Places
- 8 Lenses for perceiving
- Lifecycle for transformation
- Metadata for knowing about knowing

## How to Add a New Feature

### Step 1: Identify Grammar Elements
- Who are the Entities? (actors with agency)
- What are the Moments? (bounded occurrences)
- Where are the Places? (contexts with atmosphere)

### Step 2: Choose Lenses
- Which perceptual dimensions apply?
- Primary lens + secondary lenses

### Step 3: Apply Protocols
- Implement HasOwnership if ownership matters
- Implement HasLifecycle if state transitions matter
- Implement HasMetadata if provenance/confidence matter

### Step 4: Frame as Situation
- What's the dramatic tension?
- What learning is extracted on exit?

## Anti-Patterns (What NOT to Do)
- Don't reduce Entities to database IDs
- Don't flatten Moments to timestamps
- Don't configure Places without atmosphere
- Don't enumerate without framing

## Code Examples
[Reference Morning Standup implementation]
```

**Deliverable**: `docs/internal/development/mux-implementation-guide.md`

---

## Phase 5: ADR-055 Finalization

**Objective**: Complete ADR for acceptance

### Verification Checklist
- [ ] All appendices complete (A, B, C, D)
- [ ] Status changed from "Draft" to "Proposed"
- [ ] Implementation evidence included
- [ ] Links to test files
- [ ] Answers "why" questions

**Deliverable**: ADR-055 ready for PM acceptance

---

## Phase 6: Sign-Off Preparation

**Objective**: Prepare materials for PM/CXO review

### Sign-Off Package
```markdown
## MUX-V1 Verification Summary

### Technical Evidence
- P1 (Protocols): 101 tests ✅
- P2 (Ownership): 25 tests ✅
- P3 (Lifecycle): 69 tests ✅
- P4 (Metadata): 67 tests ✅
- P4.5 (Coverage): 100% ✅
- PZ (Anti-Flattening): XX tests ✅
- Total: XXX tests, 0 regressions

### Grammar Validation
- 63 canonical queries mapped
- 100% expressible (61 clean, 2 caveat, 0 gaps)

### Anti-Flattening Verification
- Technical tests: PASS
- Design principles: PASS
- Experience language: PASS

### PM Sign-Off Request
[ ] Technical implementation approved
[ ] Experience preservation approved
[ ] ADR-055 accepted

### CXO Sign-Off Request
[ ] Consciousness preservation approved
[ ] Design principle compliance approved
```

**Deliverable**: Sign-off package document

---

## Phase Z: Completion & Handoff

### Final Experience Checkpoint
```markdown
## MUX-V1 Experience Checkpoint

### The Journey
From ADR-045 concept ("Entities experience Moments in Places") to working
implementation with 262+ tests proving the grammar works.

### The Grammar in Action
- 8 lenses for perceiving information
- Lifecycle state machine with composting (nothing truly deleted)
- Metadata schema for "knowing about knowing"
- 100% canonical query coverage validates expressiveness

### Consciousness Preserved
Anti-flattening tests ensure we built a cathedral, not a shed.
"I notice" not "Found X results" at every layer.

### Foundation for Future
MUX-V2 can build on this foundation without re-flattening.

### Lessons Learned
[What the P0-PZ journey taught us]
```

### Verification Commands
```bash
# 1. Run anti-flattening tests
pytest tests/unit/services/mux/test_anti_flattening.py -xvs

# 2. Run full MUX suite
pytest tests/unit/services/mux/ -v --tb=no | tail -5

# 3. Verify implementation guide exists
ls -la docs/internal/development/mux-implementation-guide.md

# 4. Verify ADR-055 status
grep "Status:" docs/internal/architecture/current/adrs/adr-055-object-model-implementation.md
```

### Completion Matrix

| Deliverable | Target | Status |
|-------------|--------|--------|
| Technical anti-flattening tests | 20+ | Pending |
| Design anti-flattening verification | 1 | Pending |
| Experience tests documentation | 1 | Pending |
| Implementation guide | 1 | Pending |
| ADR-055 finalization | 1 | Pending |
| Sign-off package | 1 | Pending |
| Final experience checkpoint | 1 | Pending |

**TOTAL: 0/7 = 0% (starting point)**
**Only claim complete when 7/7 = 100%**

---

## Multi-Agent Coordination

### Agent Deployment Map

| Phase | Agent | Focus | Verification Gate |
|-------|-------|-------|-------------------|
| 1-Z | Verification Agent | Full PZ implementation | 7/7 deliverables |

**Single Agent Justification**: Verification and documentation work is sequential and coherent. Sign-off requires human review after agent preparation.

### Cross-Validation
- PM reviews sign-off package
- Anti-flattening tests are self-validating

---

## STOP Conditions

**STOP immediately and escalate if**:
1. Anti-flattening tests reveal fundamental issues with P1-P4 implementation
2. Experience tests cannot be written (grammar doesn't support experience language)
3. ADR-055 reveals unresolved contradictions
4. More than 10% of tests fail unexpectedly
5. Implementation guide reveals patterns that contradict the grammar

**When stopped**: Document the issue, provide options, wait for PM decision.

---

## Evidence Requirements

**For each phase, provide:**
- Test counts and passing status
- Documentation created
- Verification commands run

**Final Evidence:**
- Anti-flattening test suite (20+ tests)
- Design verification (documentation or tests)
- Experience test documentation
- Implementation guide
- ADR-055 finalized
- Sign-off package
- Final checkpoint

---

## Related Documentation

- **P1**: `services/mux/protocols.py` - Lenses and Protocols
- **P2**: `services/mux/ownership.py` - Ownership Model
- **P3**: `services/mux/lifecycle.py` - Lifecycle State Machine
- **P4**: `services/mux/metadata.py` - Metadata Schema
- **P4.5**: ADR-055 Appendix D - Grammar Validation
- **ADR-045**: Object Model specification
- **ADR-055**: Implementation details (finalize)
- **CXO Memo**: Design principles

---

_Gameplan created: 2026-01-19_
_Template version: v9.3_
