"""
Tests for MUX Metadata Schema.

P4 of MUX implementation: Metadata dimensions and journal infrastructure.

"Metadata is what Piper knows about what it perceives."

The 6 dimensions:
1. Provenance - Where did this come from?
2. Relevance - How important is this?
3. AttentionState - Who has noticed this?
4. Confidence - How sure are we?
5. Relations - How does this connect?
6. Journal - What is the history?
"""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import List, Optional

import pytest

from services.mux.metadata import (  # Dimension types; Protocol; Utilities
    AttentionState,
    Confidence,
    ConfidenceCalculator,
    HasMetadata,
    InsightJournalEntry,
    Journal,
    JournalManager,
    Provenance,
    ProvenanceTracker,
    Relation,
    RelationRegistry,
    RelationType,
    Relevance,
    SessionJournalEntry,
)

# =============================================================================
# Phase 1: Metadata Dimension Definitions (~15 tests)
# =============================================================================


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
        before = datetime.now(timezone.utc)
        p = Provenance(source="github")
        after = datetime.now(timezone.utc)
        assert before <= p.fetched_at <= after

    def test_provenance_freshness_decreases_over_time(self):
        """Freshness decays over time"""
        old_time = datetime.now(timezone.utc) - timedelta(hours=2)
        p = Provenance(source="github", fetched_at=old_time)
        assert p.freshness < 0.5  # Should be stale after 2 hours

    def test_provenance_fresh_data_high_freshness(self):
        """Fresh data has high freshness score"""
        p = Provenance(source="github")
        assert p.freshness > 0.9  # Just created, should be very fresh

    def test_provenance_default_confidence_is_full(self):
        """Default source confidence is 1.0"""
        p = Provenance(source="user")
        assert p.confidence == 1.0


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

    def test_relevance_default_empty_factors(self):
        """Default factors is empty list"""
        r = Relevance(score=0.5)
        assert r.factors == []

    def test_relevance_has_decay_rate(self):
        """Relevance can have decay rate"""
        r = Relevance(score=0.8, decay_rate=0.2)
        assert r.decay_rate == 0.2


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

    def test_attention_default_level_is_normal(self):
        """Default attention level is normal"""
        a = AttentionState()
        assert a.attention_level == "normal"

    def test_attention_tracks_when_noticed(self):
        """AttentionState can record when noticed"""
        now = datetime.now(timezone.utc)
        a = AttentionState(noticed_at=now)
        assert a.noticed_at == now

    def test_attention_empty_noticed_by_default(self):
        """Default noticed_by is empty list"""
        a = AttentionState()
        assert a.noticed_by == []


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

    def test_confidence_default_empty_basis(self):
        """Default basis is empty"""
        c = Confidence(score=0.5)
        assert c.basis == ""

    def test_confidence_has_validation_time(self):
        """Confidence can track last validation"""
        now = datetime.now(timezone.utc)
        c = Confidence(score=0.9, last_validated=now)
        assert c.last_validated == now


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

    def test_relation_has_strength(self):
        """Relation can have strength"""
        r = Relation(target_id="obj_456", relation_type=RelationType.RELATED_TO, strength=0.5)
        assert r.strength == 0.5

    def test_relation_default_strength_is_full(self):
        """Default relation strength is 1.0"""
        r = Relation(target_id="obj_456", relation_type=RelationType.BLOCKS)
        assert r.strength == 1.0

    def test_relation_can_be_bidirectional(self):
        """Relation can be marked bidirectional"""
        r = Relation(target_id="obj_456", relation_type=RelationType.RELATED_TO, bidirectional=True)
        assert r.bidirectional is True

    def test_relation_type_parent_child(self):
        """RelationType includes parent/child"""
        assert RelationType.PARENT_OF
        assert RelationType.CHILD_OF


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

    def test_session_entry_has_trigger(self):
        """Session entries can have trigger"""
        e = SessionJournalEntry(event_type="updated", content="Modified", trigger="user_action")
        assert e.trigger == "user_action"

    def test_session_entry_has_actor(self):
        """Session entries track actor"""
        e = SessionJournalEntry(event_type="created", content="Created", actor="user_123")
        assert e.actor == "user_123"

    def test_insight_entry_has_learning(self):
        """Insight journal captures learning"""
        i = InsightJournalEntry(learning="User prefers morning standups")
        assert "morning" in i.learning

    def test_insight_entry_has_connected_insights(self):
        """Insight entries can reference other insights"""
        i = InsightJournalEntry(learning="Pattern found", connected_insights=["insight_1"])
        assert "insight_1" in i.connected_insights

    def test_journal_has_both_layers(self):
        """Journal combines session and insight entries"""
        j = Journal()
        assert hasattr(j, "session_entries")
        assert hasattr(j, "insight_entries")

    def test_journal_entries_start_empty(self):
        """Journal starts with empty entry lists"""
        j = Journal()
        assert len(j.session_entries) == 0
        assert len(j.insight_entries) == 0


# =============================================================================
# Phase 2: HasMetadata Protocol (~4 tests)
# =============================================================================


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

        obj = PartialMetadata(_provenance=Provenance(source="github"))
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


# =============================================================================
# Phase 3: Trackers and Calculators (~8 tests)
# =============================================================================


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

    def test_from_inference_lower_confidence(self):
        """Inferred data has lower confidence"""
        p = ProvenanceTracker.from_inference()
        assert p.source == "derived"
        assert p.confidence == 0.7


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

    def test_from_source_reliability(self):
        """Can create confidence from source reliability"""
        c = ConfidenceCalculator.from_source_reliability(0.85)
        assert c.score == 0.85
        assert "reliability" in c.basis.lower()


# =============================================================================
# Phase 4: Relations Registry (~6 tests)
# =============================================================================


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
        rel = Relation(target_id="obj_456", relation_type=RelationType.BLOCKS, bidirectional=True)
        registry.add("obj_123", rel)

        # Check forward relation
        forward = registry.get_relations("obj_123")
        assert len(forward) == 1

        # Check inverse relation was created
        inverse = registry.get_relations("obj_456")
        assert len(inverse) == 1
        assert inverse[0].target_id == "obj_123"

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

    def test_registry_get_by_type(self):
        """Can filter relations by type"""
        registry = RelationRegistry()
        registry.add("obj_123", Relation(target_id="obj_456", relation_type=RelationType.BLOCKS))
        registry.add(
            "obj_123", Relation(target_id="obj_789", relation_type=RelationType.REFERENCES)
        )

        blocks = registry.get_relations("obj_123", relation_type=RelationType.BLOCKS)
        assert len(blocks) == 1
        assert blocks[0].relation_type == RelationType.BLOCKS


# =============================================================================
# Phase 5: Journal Manager (~8 tests)
# =============================================================================


class TestJournalManager:
    """Test journal coordination"""

    def test_manager_logs_session_event(self):
        """Manager can log session events"""
        manager = JournalManager()
        entry = manager.log_session_event(
            object_id="obj_123", event_type="created", content="Task was created"
        )
        assert entry.event_type == "created"

    def test_manager_extracts_insight(self):
        """Manager can extract insights"""
        manager = JournalManager()
        entry = manager.extract_insight(
            object_id="obj_123", learning="User prefers async communication"
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
            "obj_123", "completed", "Task done", trigger="user_action"
        )
        assert entry.trigger == "user_action"

    def test_insight_connects_to_others(self):
        """Insights can reference other insights"""
        manager = JournalManager()
        entry = manager.extract_insight(
            "obj_123",
            learning="Pattern identified",
            connected_insights=["insight_1", "insight_2"],
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

    def test_manager_logs_actor(self):
        """Manager tracks who performed action"""
        manager = JournalManager()
        entry = manager.log_session_event(
            "obj_123", "updated", "Modified by user", actor="user_123"
        )
        assert entry.actor == "user_123"

    def test_manager_multiple_events_same_object(self):
        """Manager accumulates events for same object"""
        manager = JournalManager()
        manager.log_session_event("obj_123", "created", "Created")
        manager.log_session_event("obj_123", "updated", "Updated")
        manager.log_session_event("obj_123", "completed", "Completed")

        journal = manager.get_journal("obj_123")
        assert len(journal.session_entries) == 3
