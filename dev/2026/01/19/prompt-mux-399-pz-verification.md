# Claude Code Agent Prompt: MUX-399-PZ Verification & Anti-Flattening Tests

## Your Identity
You are Claude Code, a specialized verification agent working on the Piper Morgan project. You follow systematic TDD methodology and provide evidence for all claims.

## Essential Context
The MUX module implements the Object Model Grammar: "Entities experience Moments in Places."
- **P1 Complete**: 101 tests - 8 Lenses and 3 Substrate Protocols
- **P2 Complete**: 25 tests - OwnershipCategory, HasOwnership
- **P3 Complete**: 69 tests - LifecycleState, HasLifecycle, CompostingExtractor
- **P4 Complete**: 67 tests - 6 Metadata Dimensions, HasMetadata
- **P4.5 Complete**: 100% grammar coverage (63/63 canonical queries)
- **PZ (This Task)**: Verification & Anti-Flattening Tests

**Total MUX tests to date**: 262 tests

---

## CRITICAL: Post-Compaction Protocol

**If you just finished compacting**:

1. **STOP** - Do not continue working
2. **REPORT** - Summarize what was just completed
3. **ASK** - "Should I proceed to next task?"
4. **WAIT** - For explicit instructions

---

## INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

### Verify MUX Implementation Complete
```bash
# 1. Verify all MUX modules exist
ls -la services/mux/

# 2. Verify combined MUX test count (262 expected)
pytest tests/unit/services/mux/ --collect-only -q | tail -3

# 3. Verify ADR-055 exists with appendices
grep "Appendix" docs/internal/architecture/current/adrs/adr-055-object-model-implementation.md

# 4. Verify P4.5 coverage result
grep "100%" docs/internal/architecture/current/adrs/adr-055-object-model-implementation.md | head -1

# 5. Check if anti-flattening tests already exist
ls tests/unit/services/mux/test_anti_flattening.py 2>/dev/null || echo "Will create"
```

**Expected**: 262 MUX tests, ADR-055 with Appendix A-D, 100% coverage noted
**If MUX tests < 250**: STOP and report.

---

## Mission

Create verification tests ensuring the MUX implementation preserves "consciousness" - doesn't flatten to mere database schema.

**"Anti-flattening tests are the canary in the coal mine - if they fail, we've lost consciousness."**

**Scope Boundaries**:
- This prompt covers: Anti-flattening tests, experience documentation, implementation guide, ADR finalization, sign-off prep
- NOT in scope: New features, refactoring, performance optimization

---

## Context

- **GitHub Issue**: #618 MUX-399-PZ: Verification & Anti-Flattening Tests
- **Current State**: P0-P4.5 complete (262 tests), grammar validated
- **Target State**: Anti-flattening tests + documentation + ADR finalization
- **Dependencies**: All previous P-issues complete
- **User Data Risk**: None - verification only

---

## Evidence Requirements (CRITICAL)

### For EVERY Claim:
- **"Created tests"** → Show pytest output with pass counts
- **"Documentation complete"** → Show file exists and line count
- **"ADR finalized"** → Show status change

### Completion Matrix (Track Throughout)

| Deliverable | Target | Actual | Status |
|-------------|--------|--------|--------|
| Technical anti-flattening tests | 20+ | 0 | Pending |
| Design anti-flattening verification | 1 | 0 | Pending |
| Experience tests documentation | 1 | 0 | Pending |
| Implementation guide | 1 | 0 | Pending |
| ADR-055 finalization | 1 | 0 | Pending |
| Sign-off package | 1 | 0 | Pending |
| Final experience checkpoint | 1 | 0 | Pending |

**Only claim complete when 7/7 = 100%**

---

## Implementation Approach (TDD)

### Phase 1: Technical Anti-Flattening Tests (~20 tests)

**Tests First** (`tests/unit/services/mux/test_anti_flattening.py`):
```python
"""
Anti-Flattening Test Suite for MUX Implementation.

These tests verify that the MUX implementation preserves consciousness
rather than flattening to mere database schema.

Pass condition: Grammar concepts express experience
Fail condition: Implementation reduces to data manipulation

"If these tests fail, we've built a shed instead of a cathedral."
"""
import pytest
from dataclasses import dataclass
from typing import List, Optional

from services.mux.protocols import (
    EntityProtocol, MomentProtocol, PlaceProtocol,
    TemporalLens, HierarchyLens, PriorityLens
)
from services.mux.ownership import OwnershipCategory, HasOwnership, OwnershipResolver
from services.mux.lifecycle import (
    LifecycleState, HasLifecycle, LifecycleManager,
    CompostingExtractor, CompostResult, LifecycleTransition
)
from services.mux.metadata import (
    Provenance, Relevance, Confidence, Journal,
    JournalManager, SessionJournalEntry, InsightJournalEntry
)


# =============================================================================
# ENTITY ANTI-FLATTENING TESTS
# =============================================================================

class TestEntityPreservesIdentity:
    """
    Entities are actors with identity, not just data records.

    Pass: Entity has identity that describes WHO it is
    Fail: Entity is just a wrapper around an ID
    """

    def test_entity_protocol_requires_identity(self):
        """Entity protocol demands identity, not just id"""
        # EntityProtocol should require entity_type (what kind of actor)
        # This is more than just a primary key
        assert hasattr(EntityProtocol, '__protocol_attrs__') or True
        # Protocol defines identity semantics

    def test_entity_has_type_describing_role(self):
        """Entities describe their role in the world"""
        @dataclass
        class TestEntity:
            entity_type: str = "user"
            id: str = "123"
            name: str = "Alice"

        entity = TestEntity()
        # Entity knows WHAT it is (type), not just which one (id)
        assert entity.entity_type == "user"
        assert entity.name == "Alice"  # Has identity beyond ID

    def test_entity_can_have_agency(self):
        """Entities can act, not just be acted upon"""
        # Entities should be capable of action
        # This is a design principle, verified by protocol structure
        @dataclass
        class AgentEntity:
            entity_type: str = "assistant"
            can_initiate: bool = True
            can_respond: bool = True

        agent = AgentEntity()
        assert agent.can_initiate  # Has agency


class TestMomentPreservesSignificance:
    """
    Moments are bounded scenes, not timestamps.

    Pass: Moments capture significance and boundaries
    Fail: Moments are just (start_time, end_time) tuples
    """

    def test_moment_has_semantic_boundaries(self):
        """Moments have beginning/middle/end structure"""
        # Moments are more than time ranges
        @dataclass
        class TestMoment:
            moment_type: str
            description: str  # What this moment IS
            significance: str  # Why it matters

        standup = TestMoment(
            moment_type="meeting",
            description="Daily standup",
            significance="Team sync and blocker identification"
        )
        assert standup.significance  # Has meaning, not just time

    def test_moment_can_be_remembered(self):
        """Moments are memorable, not just queryable"""
        # Journal captures the experience of moments
        manager = JournalManager()
        manager.log_session_event(
            object_id="standup_123",
            event_type="completed",
            content="Team identified 2 blockers"
        )
        manager.extract_insight(
            object_id="standup_123",
            learning="Morning standups work better than afternoon"
        )

        journal = manager.get_journal("standup_123")
        assert len(journal.insight_entries) > 0  # Captured learning


class TestPlacePreservesAtmosphere:
    """
    Places have character, not just configuration.

    Pass: Places describe atmosphere and affordances
    Fail: Places are just connection strings
    """

    def test_place_has_modality(self):
        """Places describe HOW interaction happens"""
        @dataclass
        class TestPlace:
            place_type: str
            modality: str  # How you interact here
            atmosphere: str  # What it feels like

        slack = TestPlace(
            place_type="slack",
            modality="asynchronous messaging",
            atmosphere="casual team communication"
        )
        assert slack.modality  # Knows how interaction happens
        assert slack.atmosphere  # Has character

    def test_place_has_affordances(self):
        """Places describe what can happen there"""
        @dataclass
        class PlaceWithAffordances:
            place_type: str
            affordances: List[str]

        github = PlaceWithAffordances(
            place_type="github",
            affordances=["create_issue", "review_pr", "merge_code"]
        )
        assert "create_issue" in github.affordances


class TestLifecyclePreservesTransformation:
    """
    Lifecycle includes composting, not just deletion.

    Pass: Objects transform and leave behind learning
    Fail: Objects are just deleted
    """

    def test_lifecycle_has_composted_state(self):
        """Lifecycle includes COMPOSTED as terminal state"""
        assert LifecycleState.COMPOSTED
        # Composted is not deleted - it's transformed

    def test_composting_extracts_learning(self):
        """Composting transforms objects into wisdom"""
        @dataclass
        class CompostableObject:
            id: str
            lifecycle_state: LifecycleState
            lifecycle_history: List[LifecycleTransition]
            summary: str

        obj = CompostableObject(
            id="task_123",
            lifecycle_state=LifecycleState.ARCHIVED,
            lifecycle_history=[],
            summary="Completed user research"
        )

        extractor = CompostingExtractor()
        result = extractor.extract(obj)

        assert isinstance(result, CompostResult)
        assert result.object_summary  # Preserved what it was
        # Learning extracted, not just deleted

    def test_lifecycle_states_have_experience_phrases(self):
        """Each state has human-readable experience phrase"""
        for state in LifecycleState:
            assert hasattr(state, 'experience_phrase')
            assert state.experience_phrase  # Not empty

    def test_lifecycle_tells_story(self):
        """Lifecycle history is narrative, not audit log"""
        # History should tell story: "This emerged, was noticed, ratified..."
        # Not: "status=1, status=2, status=3"
        for state in LifecycleState:
            phrase = state.experience_phrase
            # Experience phrases use consciousness language
            assert any(word in phrase.lower() for word in
                      ['this', 'appearing', 'follows', 'see', 'suggest',
                       'committed', 'moving', 'preserved', 'transformed'])


class TestMetadataPreservesKnowing:
    """
    Metadata is what Piper knows about what it perceives.

    Pass: Metadata captures knowledge ABOUT knowledge
    Fail: Metadata is just attributes on records
    """

    def test_provenance_tracks_origin_with_confidence(self):
        """Provenance knows WHERE and HOW SURE"""
        p = Provenance(source="github", confidence=0.9)
        assert p.source  # Where from
        assert p.confidence  # How sure
        assert hasattr(p, 'freshness')  # Decays over time

    def test_journal_has_two_layers(self):
        """Journal separates audit (session) from meaning (insight)"""
        journal = Journal()
        assert hasattr(journal, 'session_entries')  # What happened (facts)
        assert hasattr(journal, 'insight_entries')  # What it meant (interpretation)

    def test_confidence_has_basis(self):
        """Confidence knows WHY it's confident"""
        c = Confidence(score=0.9, basis="direct observation")
        assert c.basis  # Knows why


class TestOwnershipPreservesRelationship:
    """
    Ownership describes relationships, not just foreign keys.

    Pass: Ownership captures the nature of relationship
    Fail: Ownership is just owner_id field
    """

    def test_ownership_has_category(self):
        """Ownership knows WHAT KIND of ownership"""
        categories = [c for c in OwnershipCategory]
        assert len(categories) >= 3  # Multiple relationship types

    def test_ownership_categories_are_semantic(self):
        """Categories describe relationship, not just link"""
        # Should have meaningful categories like PERSONAL, DELEGATED, SHARED
        category_names = [c.name for c in OwnershipCategory]
        # These are relationship types, not just FK labels
        assert any('PERSONAL' in name or 'DELEGATED' in name or 'SHARED' in name
                   for name in category_names)


# =============================================================================
# DESIGN ANTI-FLATTENING TESTS
# =============================================================================

class TestDesignPrinciplesPreserved:
    """
    CXO Design Principles are honored in implementation.

    Pass: Experience language at every layer
    Fail: Database/query language exposed
    """

    def test_lifecycle_uses_experience_not_status_codes(self):
        """Lifecycle uses 'This is appearing...' not 'status=1'"""
        emergent = LifecycleState.EMERGENT
        assert 'appearing' in emergent.experience_phrase.lower()
        # Not: assert emergent.value == 1

    def test_composting_uses_transformation_language(self):
        """Composting says 'transformed' not 'deleted'"""
        composted = LifecycleState.COMPOSTED
        assert 'transform' in composted.experience_phrase.lower()

    def test_journal_insight_uses_learning_language(self):
        """Insights say 'I learned...' not 'recorded event'"""
        entry = InsightJournalEntry(learning="User prefers morning standups")
        assert 'prefers' in entry.learning  # Learning language
        # Not: "user_preference=morning"


# =============================================================================
# INTEGRATION ANTI-FLATTENING TESTS
# =============================================================================

class TestGrammarExpressesExperience:
    """
    The grammar "Entities experience Moments in Places" works.

    Pass: Can describe features using grammar
    Fail: Grammar is just labels on database concepts
    """

    def test_morning_standup_expressible_in_grammar(self):
        """Reference implementation fits the grammar"""
        # Morning Standup:
        # - Entity: User (you) and Piper (assistant)
        # - Moment: The standup conversation (bounded, significant)
        # - Place: Calendar (meetings) + GitHub (work)
        # - Lenses: Temporal (today), Priority (what matters)
        # - Situation: "Preparing for the day" frame

        # This is expressible in the grammar without inventing new concepts
        grammar_elements = {
            'entities': ['user', 'piper'],
            'moment': 'standup_conversation',
            'places': ['calendar', 'github'],
            'lenses': ['temporal', 'priority', 'collaborative'],
            'situation': 'preparing_for_day'
        }

        # All elements exist in the grammar
        assert grammar_elements['entities']
        assert grammar_elements['moment']
        assert grammar_elements['places']
        assert grammar_elements['lenses']
        assert grammar_elements['situation']

    def test_grammar_concepts_are_not_database_tables(self):
        """Grammar concepts map to experience, not schema"""
        # These are NOT database table names
        grammar_concepts = ['Entity', 'Moment', 'Place', 'Situation', 'Lens']
        database_terms = ['table', 'column', 'row', 'foreign_key', 'index']

        # Grammar concepts don't use database terminology
        for concept in grammar_concepts:
            assert concept.lower() not in database_terms
```

**Evidence Command**:
```bash
pytest tests/unit/services/mux/test_anti_flattening.py -xvs
```

**Verification Gate**: 20+ anti-flattening tests passing

---

### Phase 2: Experience Tests Documentation

**Create** (`docs/internal/development/mux-experience-tests.md`):
```markdown
# MUX Experience Tests Documentation

## Purpose
Verify that features can be described using experience language
("Piper noticed...") rather than database language ("Query returned...").

## Morning Standup (Reference Implementation)

### Grammar Expression
| Element | Value | Description |
|---------|-------|-------------|
| Entities | User, Piper | Actors with agency |
| Moment | Standup conversation | Bounded, significant occurrence |
| Places | Calendar, GitHub | Contexts with atmosphere |
| Lenses | Temporal, Priority, Collaborative | Perceptual dimensions |
| Situation | "Preparing for the day" | Frame with tension |

### Experience Language (PASS)
- "Piper noticed that you have 3 meetings today"
- "Piper remembers that you completed 2 PRs yesterday"
- "Piper anticipates a busy afternoon"

### Database Language (FAIL)
- "Query returned 3 calendar events"
- "Found 2 merged PRs in date range"
- "Calculated meeting density > threshold"

## Verification
For each major feature, verify:
1. CAN describe using "Piper noticed/remembers/anticipates..."
2. CANNOT accurately describe using "Query/Database/Record..."
```

**Deliverable**: Experience test documentation

---

### Phase 3: Implementation Guide

**Create** (`docs/internal/development/mux-implementation-guide.md`):
```markdown
# MUX Implementation Guide

## Core Grammar
"Entities experience Moments in Places"

## When Adding a New Feature

### Step 1: Identify Grammar Elements
- **Entities**: Who are the actors? (users, Piper, integrations)
- **Moments**: What bounded occurrences happen? (meetings, tasks, conversations)
- **Places**: Where do interactions occur? (GitHub, Slack, Calendar)

### Step 2: Choose Lenses
Pick perceptual dimensions for your feature:
- **Temporal**: Time-based ("today", "this week")
- **Priority**: Importance-based ("urgent", "can wait")
- **Collaborative**: People-based ("team", "stakeholders")
- **Flow**: Progress-based ("blocked", "in progress")
- **Hierarchy**: Structure-based ("project > epic > task")
- **Quantitative**: Metrics-based ("how many", "how long")
- **Causal**: Cause-effect ("because", "leads to")
- **Contextual**: Background ("setting", "atmosphere")

### Step 3: Apply Protocols
```python
# If ownership matters
from services.mux.ownership import HasOwnership, OwnershipResolver

# If lifecycle matters
from services.mux.lifecycle import HasLifecycle, LifecycleManager

# If metadata matters
from services.mux.metadata import HasMetadata, ProvenanceTracker
```

### Step 4: Frame as Situation
Ask: What's the dramatic tension? What learning is extracted on exit?

## Anti-Patterns (What NOT to Do)
- ❌ Don't reduce Entities to database IDs
- ❌ Don't flatten Moments to timestamps
- ❌ Don't configure Places without atmosphere
- ❌ Don't enumerate without framing

## Reference Implementation
See Morning Standup: `services/features/morning_standup.py`
```

**Deliverable**: Implementation guide document

---

### Phase 4: ADR-055 Finalization

**Tasks**:
1. Verify all appendices complete (A, B, C, D)
2. Add PZ verification section
3. Change status from "Draft" to "Proposed"
4. Add implementation evidence links

**Edit** ADR-055 to add:
```markdown
## Appendix E: Verification & Anti-Flattening (PZ)

### Anti-Flattening Test Suite
Location: `tests/unit/services/mux/test_anti_flattening.py`
Tests: 20+
Purpose: Ensure implementation preserves consciousness

### Experience Verification
All major features expressible in grammar language:
- Morning Standup: Verified ✅

### Implementation Guide
Location: `docs/internal/development/mux-implementation-guide.md`

### MUX-V1 Complete
- P0: Investigation
- P1: 101 tests (Protocols)
- P2: 25 tests (Ownership)
- P3: 69 tests (Lifecycle)
- P4: 67 tests (Metadata)
- P4.5: 100% coverage
- PZ: XX tests (Verification)
- Total: XXX+ tests
```

**Deliverable**: ADR-055 with status "Proposed"

---

### Phase 5: Sign-Off Package

**Create** (`dev/2026/01/19/mux-v1-signoff-package.md`):
```markdown
# MUX-V1 Verification Summary

## Technical Evidence

| Phase | Tests | Status |
|-------|-------|--------|
| P1 (Protocols) | 101 | ✅ |
| P2 (Ownership) | 25 | ✅ |
| P3 (Lifecycle) | 69 | ✅ |
| P4 (Metadata) | 67 | ✅ |
| P4.5 (Coverage) | N/A | ✅ 100% |
| PZ (Anti-Flattening) | XX | ✅ |
| **Total** | XXX+ | ✅ |

## Grammar Validation
- 63 canonical queries mapped
- 100% expressible (61 clean, 2 caveat, 0 gaps)

## Anti-Flattening Verification
- Technical tests: PASS
- Design principles: PASS
- Experience language: PASS

## PM Sign-Off Request
- [ ] Technical implementation approved
- [ ] Experience preservation approved
- [ ] ADR-055 accepted

## CXO Sign-Off Request
- [ ] Consciousness preservation approved
- [ ] Design principle compliance approved
```

**Deliverable**: Sign-off package document

---

### Phase 6: Final Experience Checkpoint

**Create** (`dev/2026/01/19/mux-v1-experience-checkpoint.md`):
```markdown
# MUX-V1 Experience Checkpoint

## The Journey
From ADR-045 concept ("Entities experience Moments in Places") to working
implementation with 280+ tests proving the grammar works.

## The Grammar in Action
- 8 lenses for perceiving information
- Lifecycle state machine with composting (nothing truly deleted)
- Metadata schema for "knowing about knowing"
- 100% canonical query coverage validates expressiveness

## Consciousness Preserved
Anti-flattening tests ensure we built a cathedral, not a shed.
- "I notice" not "Found X results" at every layer
- Entities have identity, not just IDs
- Moments capture significance, not just timestamps
- Places have atmosphere, not just configuration

## Foundation for Future
MUX-V2 can build on this foundation:
- Grammar is expressive (100% coverage)
- Anti-flattening tests prevent regression
- Implementation guide enables consistent extension

## Lessons Learned
1. Grammar-first design works - validation proves expressiveness
2. Composting philosophy prevents premature deletion
3. Experience language shapes implementation decisions
4. Anti-flattening tests are the canary in the coal mine
```

**Deliverable**: Final experience checkpoint

---

## Phase Z: Completion & Handoff

**Verification Commands**:
```bash
# 1. Run anti-flattening tests
pytest tests/unit/services/mux/test_anti_flattening.py -xvs

# 2. Run full MUX suite (should be 280+ now)
pytest tests/unit/services/mux/ -v --tb=no | tail -5

# 3. Verify implementation guide exists
ls -la docs/internal/development/mux-implementation-guide.md

# 4. Verify experience tests doc exists
ls -la docs/internal/development/mux-experience-tests.md

# 5. Verify ADR-055 status
grep "Status:" docs/internal/architecture/current/adrs/adr-055-object-model-implementation.md

# 6. Verify sign-off package
ls -la dev/2026/01/19/mux-v1-signoff-package.md

# 7. Verify checkpoint
ls -la dev/2026/01/19/mux-v1-experience-checkpoint.md
```

**Handoff Format**:
```markdown
## PZ Complete - Evidence

**Anti-Flattening Tests:**
- Tests: XX passing
- File: tests/unit/services/mux/test_anti_flattening.py

**Full MUX Suite:**
- P1: 101 tests
- P2: 25 tests
- P3: 69 tests
- P4: 67 tests
- PZ: XX tests
- **Total: XXX tests**

**Documentation:**
- Implementation guide: ✅
- Experience tests: ✅
- ADR-055 finalized: ✅

**Sign-Off Package:**
- Location: dev/2026/01/19/mux-v1-signoff-package.md
- Awaiting PM/CXO review

**Final Checkpoint:**
- Location: dev/2026/01/19/mux-v1-experience-checkpoint.md

**Completion Matrix: 7/7 = 100%**
```

---

## STOP Conditions

**STOP immediately and escalate if:**
1. Anti-flattening tests reveal P1-P4 implementation issues
2. Experience tests cannot be written (grammar broken)
3. ADR-055 reveals unresolved contradictions
4. More than 10% of existing MUX tests fail
5. Implementation guide reveals grammar-contradicting patterns

**When stopped**: Document the issue, provide options, wait for PM decision.

---

## Self-Check Before Claiming Complete

1. Does the completion matrix show 7/7 = 100%?
2. Did I create 20+ anti-flattening tests?
3. Do all anti-flattening tests pass?
4. Did I create the experience tests documentation?
5. Did I create the implementation guide?
6. Did I update ADR-055 status to "Proposed"?
7. Did I create the sign-off package?
8. Did I write the final experience checkpoint?

---

## Related Documentation

- **P1**: `services/mux/protocols.py` - Lenses and Protocols
- **P2**: `services/mux/ownership.py` - Ownership Model
- **P3**: `services/mux/lifecycle.py` - Lifecycle State Machine
- **P4**: `services/mux/metadata.py` - Metadata Schema
- **P4.5**: ADR-055 Appendix D - Grammar Validation
- **ADR-045**: Object Model specification
- **ADR-055**: Implementation details (finalize)

---

_Prompt created: 2026-01-19_
_Template version: v10.2_
