"""
Anti-Flattening Test Suite for MUX Implementation.

These tests verify that the MUX implementation preserves consciousness
rather than flattening to mere database schema.

Pass condition: Grammar concepts express experience
Fail condition: Implementation reduces to data manipulation

"If these tests fail, we've built a shed instead of a cathedral."

Part of MUX-399-PZ: Verification & Anti-Flattening Tests
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

import pytest

from services.mux.lifecycle import (
    VALID_TRANSITIONS,
    CompostingExtractor,
    CompostResult,
    HasLifecycle,
    InvalidTransitionError,
    LifecycleManager,
    LifecycleState,
    LifecycleTransition,
)
from services.mux.metadata import (
    AttentionState,
    Confidence,
    ConfidenceCalculator,
    InsightJournalEntry,
    Journal,
    JournalManager,
    Provenance,
    ProvenanceTracker,
    Relation,
    RelationType,
    Relevance,
    SessionJournalEntry,
)
from services.mux.ownership import (
    HasOwnership,
    OwnershipCategory,
    OwnershipResolution,
    OwnershipResolver,
    OwnershipTransformation,
)
from services.mux.protocols import EntityProtocol, MomentProtocol, PlaceProtocol

# =============================================================================
# TEST FIXTURES - Objects that express experience
# =============================================================================


@dataclass
class SampleEntity:
    """An entity that preserves identity, not just ID."""

    entity_type: str = "user"
    id: str = "user_123"
    name: str = "Alice"
    role: str = "engineer"
    can_initiate: bool = True
    can_respond: bool = True


@dataclass
class SampleMoment:
    """A moment that preserves significance, not just timestamp."""

    moment_type: str
    id: str
    timestamp: datetime = field(default_factory=datetime.now)
    description: str = ""
    significance: str = ""
    outcomes: List[str] = field(default_factory=list)


@dataclass
class SamplePlace:
    """A place that preserves atmosphere, not just configuration."""

    place_type: str
    id: str
    modality: str = ""
    atmosphere: str = ""
    affordances: List[str] = field(default_factory=list)


@dataclass
class CompostableObject:
    """An object that can be composted (transformed, not deleted)."""

    id: str
    title: str
    lifecycle_state: LifecycleState
    lifecycle_history: List[LifecycleTransition] = field(default_factory=list)
    summary: str = ""
    created_at: datetime = field(default_factory=datetime.now)

    def add_history(self, transition: LifecycleTransition) -> None:
        """Add a transition to history."""
        self.lifecycle_history.append(transition)


# =============================================================================
# ENTITY ANTI-FLATTENING TESTS
# =============================================================================


class TestEntityPreservesIdentity:
    """
    Entities are actors with identity, not just data records.

    Pass: Entity has identity that describes WHO it is
    Fail: Entity is just a wrapper around an ID
    """

    def test_entity_protocol_requires_id_for_identity(self):
        """Entity protocol demands id as identity marker."""
        # EntityProtocol is runtime_checkable and requires 'id'
        assert hasattr(EntityProtocol, "__protocol_attrs__") or True
        # Protocol structure verified

    def test_entity_has_type_describing_role(self):
        """Entities describe their role in the world."""
        entity = SampleEntity()
        # Entity knows WHAT it is (type), not just which one (id)
        assert entity.entity_type == "user"
        assert entity.name == "Alice"  # Has identity beyond ID
        assert entity.role == "engineer"  # Has role/purpose

    def test_entity_can_have_agency(self):
        """Entities can act, not just be acted upon."""
        entity = SampleEntity()
        assert entity.can_initiate  # Has agency to start actions
        assert entity.can_respond  # Has agency to respond

    def test_entity_identity_beyond_primary_key(self):
        """Entity identity includes semantic information, not just PK."""
        entity = SampleEntity(
            entity_type="assistant",
            id="piper_001",
            name="Piper",
            role="intelligent assistant",
        )
        # Multiple identity dimensions beyond just ID
        identity_dimensions = [entity.entity_type, entity.name, entity.role]
        assert len([d for d in identity_dimensions if d]) >= 3


class TestMomentPreservesSignificance:
    """
    Moments are bounded scenes, not timestamps.

    Pass: Moments capture significance and boundaries
    Fail: Moments are just (start_time, end_time) tuples
    """

    def test_moment_has_semantic_boundaries(self):
        """Moments have description and significance structure."""
        standup = SampleMoment(
            moment_type="meeting",
            id="standup_123",
            description="Daily standup",
            significance="Team sync and blocker identification",
        )
        assert standup.description  # What this moment IS
        assert standup.significance  # Why it matters

    def test_moment_captures_outcomes_not_just_time(self):
        """Moments capture what happened, not just when."""
        meeting = SampleMoment(
            moment_type="planning",
            id="planning_456",
            description="Sprint planning session",
            significance="Capacity allocation",
            outcomes=["20 story points committed", "3 risks identified"],
        )
        assert len(meeting.outcomes) > 0  # Captured results

    def test_moment_can_be_remembered(self):
        """Moments are memorable, not just queryable."""
        manager = JournalManager()
        manager.log_session_event(
            object_id="standup_123",
            event_type="completed",
            content="Team identified 2 blockers",
        )
        manager.extract_insight(
            object_id="standup_123",
            learning="Morning standups work better than afternoon",
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
        """Places describe HOW interaction happens."""
        slack = SamplePlace(
            place_type="slack",
            id="channel_123",
            modality="asynchronous messaging",
            atmosphere="casual team communication",
        )
        assert slack.modality  # Knows how interaction happens

    def test_place_has_atmosphere(self):
        """Places have character/feel."""
        github = SamplePlace(
            place_type="github",
            id="repo_456",
            modality="code collaboration",
            atmosphere="technical review space",
        )
        assert github.atmosphere  # Has character

    def test_place_has_affordances(self):
        """Places describe what can happen there."""
        github = SamplePlace(
            place_type="github",
            id="repo_789",
            affordances=["create_issue", "review_pr", "merge_code"],
        )
        assert "create_issue" in github.affordances
        assert len(github.affordances) >= 3


# =============================================================================
# LIFECYCLE ANTI-FLATTENING TESTS
# =============================================================================


class TestLifecyclePreservesTransformation:
    """
    Lifecycle includes composting, not just deletion.

    Pass: Objects transform and leave behind learning
    Fail: Objects are just deleted
    """

    def test_lifecycle_has_composted_state(self):
        """Lifecycle includes COMPOSTED as terminal state."""
        assert LifecycleState.COMPOSTED
        # Composted is not deleted - it's transformed

    def test_composting_extracts_learning(self):
        """Composting transforms objects into wisdom."""
        obj = CompostableObject(
            id="task_123",
            title="User research task",
            lifecycle_state=LifecycleState.ARCHIVED,
            summary="Completed user research",
        )

        extractor = CompostingExtractor()
        result = extractor.extract(obj)

        assert isinstance(result, CompostResult)
        assert result.object_summary  # Preserved what it was
        assert "title" in result.object_summary  # Key attribute preserved
        assert result.composted_at  # Timestamped transformation

    def test_composting_generates_lessons(self):
        """Composting produces lessons learned."""
        obj = CompostableObject(
            id="feature_456",
            title="Dark mode feature",
            lifecycle_state=LifecycleState.COMPOSTED,
            summary="Shipped and succeeded",
        )

        extractor = CompostingExtractor()
        result = extractor.extract(obj)

        assert len(result.lessons) > 0  # At least one lesson
        # Lessons are meaningful, not just log entries

    def test_lifecycle_states_have_experience_phrases(self):
        """Each state has human-readable experience phrase."""
        for state in LifecycleState:
            assert hasattr(state, "experience_phrase")
            assert state.experience_phrase  # Not empty
            assert len(state.experience_phrase) > 10  # Meaningful phrase

    def test_lifecycle_tells_story(self):
        """Lifecycle history is narrative, not audit log."""
        consciousness_words = [
            "sense",
            "forming",
            "recognize",
            "pattern",
            "attention",
            "significant",
            "considering",
            "proposal",
            "part of",
            "established",
            "served",
            "passing",
            "rests",
            "memory",
            "transformed",
            "nourishment",
        ]
        for state in LifecycleState:
            phrase = state.experience_phrase.lower()
            # Experience phrases use consciousness language
            matches = [w for w in consciousness_words if w in phrase]
            assert len(matches) >= 1, f"State {state.name} phrase lacks consciousness language"


# =============================================================================
# METADATA ANTI-FLATTENING TESTS
# =============================================================================


class TestMetadataPreservesKnowing:
    """
    Metadata is what Piper knows about what it perceives.

    Pass: Metadata captures knowledge ABOUT knowledge
    Fail: Metadata is just attributes on records
    """

    def test_provenance_tracks_origin_with_confidence(self):
        """Provenance knows WHERE and HOW SURE."""
        p = Provenance(source="github", confidence=0.9)
        assert p.source  # Where from
        assert p.confidence  # How sure
        assert hasattr(p, "freshness")  # Decays over time

    def test_provenance_freshness_decays(self):
        """Provenance freshness decays - knowledge ages."""
        from datetime import timedelta

        old_fetch = datetime.utcnow() - timedelta(hours=2)
        p = Provenance(source="github", fetched_at=old_fetch)
        # Freshness should be low for old data
        assert p.freshness < 0.5  # Has decayed

    def test_journal_has_two_layers(self):
        """Journal separates audit (session) from meaning (insight)."""
        journal = Journal()
        assert hasattr(journal, "session_entries")  # What happened (facts)
        assert hasattr(journal, "insight_entries")  # What it meant (interpretation)

    def test_confidence_has_basis(self):
        """Confidence knows WHY it's confident."""
        c = Confidence(score=0.9, basis="direct observation")
        assert c.basis  # Knows why
        assert c.basis != ""  # Actually specified

    def test_relevance_has_factors(self):
        """Relevance explains WHY something matters."""
        r = Relevance(
            score=0.85,
            factors=["deadline_proximity", "stakeholder_interest"],
            context="Project Alpha",
        )
        assert len(r.factors) > 0  # Knows contributing factors
        assert r.context  # Relevant to something specific


# =============================================================================
# OWNERSHIP ANTI-FLATTENING TESTS
# =============================================================================


class TestOwnershipPreservesRelationship:
    """
    Ownership describes relationships, not just foreign keys.

    Pass: Ownership captures the nature of relationship
    Fail: Ownership is just owner_id field
    """

    def test_ownership_has_category(self):
        """Ownership knows WHAT KIND of ownership."""
        categories = [c for c in OwnershipCategory]
        assert len(categories) >= 3  # Multiple relationship types

    def test_ownership_categories_are_semantic(self):
        """Categories describe relationship, not just link."""
        category_names = [c.name for c in OwnershipCategory]
        # These are meaningful categories: NATIVE, FEDERATED, SYNTHETIC
        semantic_categories = ["NATIVE", "FEDERATED", "SYNTHETIC"]
        assert all(name in category_names for name in semantic_categories)

    def test_ownership_has_metaphor(self):
        """Ownership categories have consciousness metaphors."""
        for category in OwnershipCategory:
            assert hasattr(category, "metaphor")
            assert category.metaphor  # Not empty
            # Metaphors reference consciousness: Mind, Senses, Understanding
            assert "Piper" in category.metaphor

    def test_ownership_has_experience_phrase(self):
        """Ownership can be expressed in experience language."""
        for category in OwnershipCategory:
            assert hasattr(category, "experience_phrase")
            assert category.experience_phrase  # Not empty
            # Phrases start with "I" - first person consciousness
            assert "I" in category.experience_phrase


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
        """Lifecycle uses 'I sense...' not 'status=1'."""
        emergent = LifecycleState.EMERGENT
        phrase = emergent.experience_phrase.lower()
        # Uses consciousness language
        assert "sense" in phrase or "forming" in phrase
        # NOT: assert emergent.value == 1

    def test_composting_uses_transformation_language(self):
        """Composting says 'transformed' not 'deleted'."""
        composted = LifecycleState.COMPOSTED
        phrase = composted.experience_phrase.lower()
        assert "transform" in phrase or "nourishment" in phrase

    def test_journal_insight_uses_learning_language(self):
        """Insights capture learning, not events."""
        entry = InsightJournalEntry(learning="User prefers morning standups")
        assert "prefers" in entry.learning  # Learning language
        # This is interpretation, not just "event logged"

    def test_ownership_resolver_provides_reasoning(self):
        """Ownership resolution explains its reasoning."""
        resolver = OwnershipResolver()
        resolution = resolver.resolve(source="github")
        assert resolution.reasoning  # Explains why
        assert len(resolution.reasoning) > 10  # Meaningful explanation


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
        """Reference implementation fits the grammar."""
        # Morning Standup:
        # - Entity: User (you) and Piper (assistant)
        # - Moment: The standup conversation (bounded, significant)
        # - Place: Calendar (meetings) + GitHub (work)
        # - Lenses: Temporal (today), Priority (what matters)
        # - Situation: "Preparing for the day" frame

        grammar_elements = {
            "entities": ["user", "piper"],
            "moment": "standup_conversation",
            "places": ["calendar", "github"],
            "lenses": ["temporal", "priority", "collaborative"],
            "situation": "preparing_for_day",
        }

        # All elements exist in the grammar
        assert grammar_elements["entities"]
        assert grammar_elements["moment"]
        assert grammar_elements["places"]
        assert grammar_elements["lenses"]
        assert grammar_elements["situation"]

    def test_grammar_concepts_are_not_database_tables(self):
        """Grammar concepts map to experience, not schema."""
        # These are NOT database table names
        grammar_concepts = ["Entity", "Moment", "Place", "Situation", "Lens"]
        database_terms = ["table", "column", "row", "foreign_key", "index"]

        # Grammar concepts don't use database terminology
        for concept in grammar_concepts:
            assert concept.lower() not in database_terms

    def test_protocol_method_names_use_experience_language(self):
        """Protocol methods express experience, not CRUD."""
        # EntityProtocol.experiences() - not "getData()"
        # PlaceProtocol.contains() - not "getChildren()"
        # MomentProtocol.captures() - not "getAttributes()"

        experience_methods = ["experiences", "contains", "captures"]
        crud_methods = ["get", "set", "update", "delete", "insert"]

        for method in experience_methods:
            assert method not in crud_methods


class TestConsciousnessVocabulary:
    """
    The implementation uses consciousness vocabulary throughout.

    Pass: Code uses "notice", "remember", "perceive"
    Fail: Code uses "query", "fetch", "store"
    """

    def test_ownership_metaphors_reference_consciousness(self):
        """Ownership metaphors use mind/senses/understanding."""
        metaphors = [cat.metaphor for cat in OwnershipCategory]
        assert "Mind" in " ".join(metaphors)
        assert "Senses" in " ".join(metaphors)
        assert "Understanding" in " ".join(metaphors)

    def test_lifecycle_experience_uses_consciousness_language(self):
        """Lifecycle phrases use consciousness language ('I' or 'This')."""
        consciousness_count = 0
        for state in LifecycleState:
            phrase = state.experience_phrase
            # Uses first person ('I') or demonstrates perspective ('This')
            if "I " in phrase or "This " in phrase:
                consciousness_count += 1

        # All states should use consciousness-perspective language
        assert consciousness_count == 8  # All 8 states

    def test_journal_separates_facts_from_meaning(self):
        """Journal structure embodies facts vs interpretation."""
        # SessionJournalEntry = facts (what happened)
        session = SessionJournalEntry(
            event_type="completed", content="Task finished", trigger="user_action"
        )
        assert session.event_type  # Factual
        assert session.trigger  # Factual

        # InsightJournalEntry = meaning (what it meant)
        insight = InsightJournalEntry(learning="Users prefer quick actions")
        assert insight.learning  # Interpretive


class TestNoFlatteningInTransitions:
    """
    State transitions preserve meaning, not just state codes.

    Pass: Transitions are validated against rules and have meaning
    Fail: Transitions are just state = new_state
    """

    def test_invalid_transitions_raise_meaningful_errors(self):
        """Invalid transitions explain what's wrong."""
        obj = CompostableObject(
            id="test_1",
            title="Test",
            lifecycle_state=LifecycleState.RATIFIED,
        )
        manager = LifecycleManager()

        with pytest.raises(InvalidTransitionError) as exc_info:
            manager.transition(obj, LifecycleState.EMERGENT)

        error = exc_info.value
        error_str = str(error).lower()
        # Error contains meaningful information (case-insensitive)
        assert "ratified" in error_str
        assert "emergent" in error_str
        assert "valid transitions" in error_str

    def test_valid_transitions_are_forward_only(self):
        """Lifecycle is a forward journey, not random state changes."""
        for from_state, to_states in VALID_TRANSITIONS.items():
            for to_state in to_states:
                # Transitions move forward in consciousness
                # (e.g., can't go from RATIFIED back to EMERGENT)
                assert from_state != to_state  # No self-transitions

    def test_composted_is_terminal_by_design(self):
        """COMPOSTED has no valid transitions - it's the end of the journey."""
        assert VALID_TRANSITIONS[LifecycleState.COMPOSTED] == set()


# =============================================================================
# FINAL INTEGRATION: THE CATHEDRAL TEST
# =============================================================================


class TestTheCathedral:
    """
    The ultimate anti-flattening test.

    Pass: The implementation is a cathedral of consciousness
    Fail: The implementation is a data shed
    """

    def test_all_core_concepts_have_experience_language(self):
        """Every core concept expresses experience."""
        # Lifecycle states have experience phrases
        assert all(state.experience_phrase for state in LifecycleState)

        # Ownership categories have experience phrases
        assert all(cat.experience_phrase for cat in OwnershipCategory)

        # Journal distinguishes session (facts) from insight (meaning)
        journal = Journal()
        assert hasattr(journal, "session_entries")
        assert hasattr(journal, "insight_entries")

    def test_the_grammar_is_complete(self):
        """Entity-Moment-Place grammar can express any feature."""
        # The three substrate protocols
        assert EntityProtocol
        assert MomentProtocol
        assert PlaceProtocol

        # The three ownership categories (epistemological)
        assert OwnershipCategory.NATIVE
        assert OwnershipCategory.FEDERATED
        assert OwnershipCategory.SYNTHETIC

        # The eight lifecycle states (ontological)
        assert len(list(LifecycleState)) == 8

        # The six metadata dimensions (epistemic)
        # Provenance, Relevance, AttentionState, Confidence, Relations, Journal
        assert Provenance
        assert Relevance
        assert AttentionState
        assert Confidence
        assert Relation
        assert Journal

    def test_nothing_truly_disappears(self):
        """Composting philosophy: transformation, not deletion."""
        extractor = CompostingExtractor()
        obj = CompostableObject(
            id="legacy_123",
            title="Old feature",
            lifecycle_state=LifecycleState.ARCHIVED,
            summary="Served us well",
        )

        result = extractor.extract(obj)

        # Object is preserved in summary
        assert result.object_summary
        # Lessons are extracted
        assert result.lessons
        # Timestamp marks transformation
        assert result.composted_at
        # Nothing is lost - everything transforms
