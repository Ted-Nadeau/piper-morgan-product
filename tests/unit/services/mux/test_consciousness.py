"""
Tests for MUX consciousness types.

Part of #434 MUX-TECH-PHASE2-ENTITY.
"""

import pytest

from services.mux.consciousness import (
    AwarenessLevel,
    Capability,
    ConsciousnessAttributes,
    ConsciousnessExpression,
    EmotionalState,
    EntityContext,
    EntityRole,
    PiperEntity,
    TrustLevel,
)


class TestAwarenessLevel:
    """Tests for AwarenessLevel enum."""

    def test_has_five_levels(self):
        """AwarenessLevel has exactly 5 states."""
        assert len(AwarenessLevel) == 5

    def test_sleeping_is_lowest(self):
        """SLEEPING represents inactive state."""
        assert AwarenessLevel.SLEEPING.value == "sleeping"

    def test_drowsy_is_passive(self):
        """DROWSY represents passive monitoring."""
        assert AwarenessLevel.DROWSY.value == "drowsy"

    def test_alert_is_normal(self):
        """ALERT represents normal operation."""
        assert AwarenessLevel.ALERT.value == "alert"

    def test_focused_is_deep(self):
        """FOCUSED represents deep attention."""
        assert AwarenessLevel.FOCUSED.value == "focused"

    def test_overwhelmed_is_degraded(self):
        """OVERWHELMED represents too much input."""
        assert AwarenessLevel.OVERWHELMED.value == "overwhelmed"

    def test_all_values_are_lowercase_strings(self):
        """All enum values are lowercase strings."""
        for level in AwarenessLevel:
            assert level.value == level.value.lower()
            assert isinstance(level.value, str)


class TestEmotionalState:
    """Tests for EmotionalState enum."""

    def test_has_four_states(self):
        """EmotionalState has exactly 4 states."""
        assert len(EmotionalState) == 4

    def test_curious_is_default_exploration(self):
        """CURIOUS represents exploring mode."""
        assert EmotionalState.CURIOUS.value == "curious"

    def test_concerned_for_issues(self):
        """CONCERNED represents worry about issues."""
        assert EmotionalState.CONCERNED.value == "concerned"

    def test_satisfied_for_contentment(self):
        """SATISFIED represents things going well."""
        assert EmotionalState.SATISFIED.value == "satisfied"

    def test_puzzled_for_uncertainty(self):
        """PUZZLED represents needing clarification."""
        assert EmotionalState.PUZZLED.value == "puzzled"

    def test_all_values_are_lowercase_strings(self):
        """All enum values are lowercase strings."""
        for state in EmotionalState:
            assert state.value == state.value.lower()
            assert isinstance(state.value, str)


class TestEntityRole:
    """Tests for EntityRole enum."""

    def test_has_four_roles(self):
        """EntityRole has exactly 4 roles."""
        assert len(EntityRole) == 4

    def test_actor_for_doing(self):
        """ACTOR is for entities doing things."""
        assert EntityRole.ACTOR.value == "actor"

    def test_place_for_context(self):
        """PLACE is for context where things happen."""
        assert EntityRole.PLACE.value == "place"

    def test_observer_for_watching(self):
        """OBSERVER is for entities watching."""
        assert EntityRole.OBSERVER.value == "observer"

    def test_participant_for_involvement(self):
        """PARTICIPANT is for entities part of something."""
        assert EntityRole.PARTICIPANT.value == "participant"

    def test_all_values_are_lowercase_strings(self):
        """All enum values are lowercase strings."""
        for role in EntityRole:
            assert role.value == role.value.lower()
            assert isinstance(role.value, str)


class TestConsciousnessAttributesDefaults:
    """Tests for ConsciousnessAttributes default values."""

    def test_empty_defaults(self):
        """ConsciousnessAttributes defaults to empty collections."""
        attrs = ConsciousnessAttributes()
        assert attrs.wants == []
        assert attrs.fears == []
        assert attrs.capabilities == []
        assert attrs.knows_about == []
        assert attrs.attention_on is None
        assert attrs.emotional_state is None
        assert attrs.trusts == {}
        assert attrs.depends_on == []
        assert attrs.influences == []

    def test_lists_are_independent(self):
        """Each instance has independent lists (no shared mutable defaults)."""
        attrs1 = ConsciousnessAttributes()
        attrs2 = ConsciousnessAttributes()

        attrs1.wants.append("test")

        assert "test" in attrs1.wants
        assert "test" not in attrs2.wants

    def test_dicts_are_independent(self):
        """Each instance has independent dicts."""
        attrs1 = ConsciousnessAttributes()
        attrs2 = ConsciousnessAttributes()

        attrs1.trusts["entity-1"] = 0.9

        assert "entity-1" in attrs1.trusts
        assert "entity-1" not in attrs2.trusts


class TestConsciousnessAttributesWithValues:
    """Tests for ConsciousnessAttributes with provided values."""

    def test_with_agency_values(self):
        """ConsciousnessAttributes accepts agency values."""
        attrs = ConsciousnessAttributes(
            wants=["ship features", "help users"],
            fears=["missing deadlines", "confusing users"],
            capabilities=["planning", "tracking", "analysis"],
        )
        assert "ship features" in attrs.wants
        assert "missing deadlines" in attrs.fears
        assert "planning" in attrs.capabilities

    def test_with_awareness_values(self):
        """ConsciousnessAttributes accepts awareness values."""
        attrs = ConsciousnessAttributes(
            knows_about=["sprint", "backlog", "deadlines"],
            attention_on="sprint planning",
            emotional_state=EmotionalState.CURIOUS,
        )
        assert "sprint" in attrs.knows_about
        assert attrs.attention_on == "sprint planning"
        assert attrs.emotional_state == EmotionalState.CURIOUS

    def test_with_relationship_values(self):
        """ConsciousnessAttributes accepts relationship values."""
        attrs = ConsciousnessAttributes(
            trusts={"user-1": 0.9, "user-2": 0.5},
            depends_on=["calendar", "github"],
            influences=["task-list", "notifications"],
        )
        assert attrs.trusts["user-1"] == 0.9
        assert "calendar" in attrs.depends_on
        assert "task-list" in attrs.influences


class TestConsciousnessAttributesMethods:
    """Tests for ConsciousnessAttributes helper methods."""

    def test_is_aware_of_known_topic(self):
        """is_aware_of returns True for known topics."""
        attrs = ConsciousnessAttributes(knows_about=["sprint", "backlog"])
        assert attrs.is_aware_of("sprint") is True

    def test_is_aware_of_unknown_topic(self):
        """is_aware_of returns False for unknown topics."""
        attrs = ConsciousnessAttributes(knows_about=["sprint", "backlog"])
        assert attrs.is_aware_of("unknown") is False

    def test_is_aware_of_empty(self):
        """is_aware_of returns False when knows_about is empty."""
        attrs = ConsciousnessAttributes()
        assert attrs.is_aware_of("anything") is False

    def test_trust_level_default(self):
        """trust_level returns 0.5 for unknown entities."""
        attrs = ConsciousnessAttributes()
        assert attrs.trust_level("unknown-entity") == 0.5

    def test_trust_level_known(self):
        """trust_level returns stored value for known entities."""
        attrs = ConsciousnessAttributes(trusts={"user-1": 0.9})
        assert attrs.trust_level("user-1") == 0.9

    def test_trust_level_zero(self):
        """trust_level can return 0.0 if explicitly set."""
        attrs = ConsciousnessAttributes(trusts={"untrusted": 0.0})
        assert attrs.trust_level("untrusted") == 0.0

    def test_trust_level_full(self):
        """trust_level can return 1.0 if explicitly set."""
        attrs = ConsciousnessAttributes(trusts={"trusted": 1.0})
        assert attrs.trust_level("trusted") == 1.0

    def test_is_focused_when_attention_set(self):
        """is_focused returns True when attention_on is set."""
        attrs = ConsciousnessAttributes(attention_on="sprint planning")
        assert attrs.is_focused() is True

    def test_not_focused_when_attention_none(self):
        """is_focused returns False when attention_on is None."""
        attrs = ConsciousnessAttributes()
        assert attrs.is_focused() is False

    def test_not_focused_when_attention_empty_string(self):
        """is_focused returns True even for empty string (truthy check)."""
        # Note: Empty string is falsy in Python but our method checks for None
        attrs = ConsciousnessAttributes(attention_on="")
        # Empty string is not None, so is_focused returns True
        # This is intentional - empty string means "attending to something"
        assert attrs.is_focused() is True


class TestConsciousnessAttributesIntegration:
    """Integration tests for ConsciousnessAttributes."""

    def test_full_consciousness_profile(self):
        """Test a fully populated consciousness profile."""
        attrs = ConsciousnessAttributes(
            # Agency
            wants=["ship features", "maintain quality"],
            fears=["missing deadlines", "introducing bugs"],
            capabilities=["planning", "tracking", "analysis", "communication"],
            # Awareness
            knows_about=["sprint-42", "backlog", "team-velocity"],
            attention_on="sprint-42",
            emotional_state=EmotionalState.CURIOUS,
            # Relationships
            trusts={"user-alice": 0.95, "user-bob": 0.8, "system": 1.0},
            depends_on=["calendar-api", "github-api"],
            influences=["task-list", "notifications", "reports"],
        )

        # Verify agency
        assert len(attrs.wants) == 2
        assert len(attrs.fears) == 2
        assert len(attrs.capabilities) == 4

        # Verify awareness
        assert attrs.is_aware_of("sprint-42")
        assert attrs.is_focused()
        assert attrs.emotional_state == EmotionalState.CURIOUS

        # Verify relationships
        assert attrs.trust_level("user-alice") == 0.95
        assert attrs.trust_level("unknown") == 0.5  # Default
        assert len(attrs.depends_on) == 2
        assert len(attrs.influences) == 3


class TestCapability:
    """Tests for Capability dataclass."""

    def test_basic_capability(self):
        """Capability stores name and description."""
        cap = Capability(name="planning", description="Create and track plans")
        assert cap.name == "planning"
        assert cap.description == "Create and track plans"
        assert cap.requires == []
        assert cap.blocked_by is None

    def test_capability_with_requirements(self):
        """Capability can have requirements."""
        cap = Capability(
            name="github-sync",
            description="Sync with GitHub",
            requires=["github-token", "repo-access"],
        )
        assert len(cap.requires) == 2
        assert "github-token" in cap.requires

    def test_is_blocked_when_none(self):
        """is_blocked returns False when blocked_by is None."""
        cap = Capability(name="test", description="test")
        assert cap.is_blocked() is False

    def test_is_blocked_when_set(self):
        """is_blocked returns True when blocked_by is set."""
        cap = Capability(
            name="calendar-sync",
            description="Sync with calendar",
            blocked_by="Missing calendar credentials",
        )
        assert cap.is_blocked() is True
        assert cap.blocked_by == "Missing calendar credentials"


class TestTrustLevel:
    """Tests for TrustLevel enum."""

    def test_has_five_levels(self):
        """TrustLevel has exactly 5 levels."""
        assert len(TrustLevel) == 5

    def test_unknown_is_default(self):
        """UNKNOWN represents no history."""
        assert TrustLevel.UNKNOWN.value == "unknown"

    def test_cautious_for_concern(self):
        """CAUTIOUS represents some concern."""
        assert TrustLevel.CAUTIOUS.value == "cautious"

    def test_standard_for_normal(self):
        """STANDARD represents normal trust."""
        assert TrustLevel.STANDARD.value == "standard"

    def test_trusted_for_high(self):
        """TRUSTED represents high trust."""
        assert TrustLevel.TRUSTED.value == "trusted"

    def test_full_for_complete(self):
        """FULL represents complete trust."""
        assert TrustLevel.FULL.value == "full"

    def test_all_values_are_lowercase_strings(self):
        """All enum values are lowercase strings."""
        for level in TrustLevel:
            assert level.value == level.value.lower()
            assert isinstance(level.value, str)


class TestPiperEntityDefaults:
    """Tests for PiperEntity default values."""

    def test_default_identity(self):
        """PiperEntity has default identity."""
        piper = PiperEntity()
        assert piper.id == "piper-prime"
        assert piper.name == "Piper Morgan"
        assert piper.role == "AI Product Management Assistant"
        assert piper.version == "0.8.4"

    def test_default_consciousness_state(self):
        """PiperEntity has default consciousness state."""
        piper = PiperEntity()
        assert piper.awareness_level == AwarenessLevel.ALERT
        assert piper.attention_focus == []
        assert piper.emotional_state == EmotionalState.CURIOUS

    def test_default_capabilities(self):
        """PiperEntity has empty capability lists by default."""
        piper = PiperEntity()
        assert piper.available_capabilities == []
        assert piper.active_capabilities == []
        assert piper.blocked_capabilities == []

    def test_default_boundaries(self):
        """PiperEntity has default ethical boundaries."""
        piper = PiperEntity()
        assert len(piper.ethical_boundaries) == 4
        assert "Never deceive users about AI nature" in piper.ethical_boundaries
        assert piper.trust_boundaries == {}
        assert piper.knowledge_boundaries == {}

    def test_default_orientation_awareness(self):
        """PiperEntity has default identity awareness."""
        piper = PiperEntity()
        assert piper.identity_awareness == "I am Piper Morgan, an AI PM assistant"
        assert piper.temporal_awareness == ""
        assert piper.spatial_awareness == ""

    def test_default_relationships(self):
        """PiperEntity has empty relationships by default."""
        piper = PiperEntity()
        assert piper.primary_user is None
        assert piper.known_entities == []
        assert piper.active_situations == []

    def test_lists_are_independent(self):
        """Each PiperEntity instance has independent lists."""
        piper1 = PiperEntity()
        piper2 = PiperEntity()

        piper1.attention_focus.append("test")
        piper1.known_entities.append("entity-1")

        assert "test" in piper1.attention_focus
        assert "test" not in piper2.attention_focus
        assert "entity-1" in piper1.known_entities
        assert "entity-1" not in piper2.known_entities


class TestPiperEntityOrientationQueries:
    """Tests for PiperEntity five orientation queries."""

    def test_who_am_i(self):
        """who_am_i returns identity awareness."""
        piper = PiperEntity()
        assert piper.who_am_i() == "I am Piper Morgan, an AI PM assistant"

    def test_who_am_i_custom(self):
        """who_am_i returns custom identity if set."""
        piper = PiperEntity(identity_awareness="Custom identity")
        assert piper.who_am_i() == "Custom identity"

    def test_when_am_i_default(self):
        """when_am_i returns default message when no temporal context."""
        piper = PiperEntity()
        assert piper.when_am_i() == "No temporal context set"

    def test_when_am_i_with_context(self):
        """when_am_i returns temporal context when set."""
        piper = PiperEntity(temporal_awareness="Sprint 42, Day 3 of 10")
        assert piper.when_am_i() == "Sprint 42, Day 3 of 10"

    def test_where_am_i_default(self):
        """where_am_i returns default message when no spatial context."""
        piper = PiperEntity()
        assert piper.where_am_i() == "No spatial context set"

    def test_where_am_i_with_context(self):
        """where_am_i returns spatial context when set."""
        piper = PiperEntity(spatial_awareness="In standup meeting")
        assert piper.where_am_i() == "In standup meeting"

    def test_what_can_i_do_empty(self):
        """what_can_i_do reports zeros when no capabilities."""
        piper = PiperEntity()
        assert piper.what_can_i_do() == "0 capabilities available, 0 active, 0 blocked"

    def test_what_can_i_do_with_capabilities(self):
        """what_can_i_do reports capability counts."""
        piper = PiperEntity(
            available_capabilities=[
                Capability(name="a", description="a"),
                Capability(name="b", description="b"),
            ],
            active_capabilities=[Capability(name="c", description="c")],
            blocked_capabilities=[],
        )
        assert piper.what_can_i_do() == "2 capabilities available, 1 active, 0 blocked"

    def test_what_should_happen_default(self):
        """what_should_happen returns default when no predictions."""
        piper = PiperEntity()
        assert piper.what_should_happen() == "No predictions active"

    def test_what_should_happen_with_prediction(self):
        """what_should_happen returns prediction when set."""
        piper = PiperEntity(predictive_awareness="User will ask about sprint status")
        assert piper.what_should_happen() == "User will ask about sprint status"


class TestPiperEntityContextUpdates:
    """Tests for PiperEntity context update methods."""

    def test_update_temporal_context(self):
        """update_temporal_context sets temporal awareness."""
        piper = PiperEntity()
        piper.update_temporal_context("End of sprint")
        assert piper.temporal_awareness == "End of sprint"
        assert piper.when_am_i() == "End of sprint"

    def test_update_spatial_context(self):
        """update_spatial_context sets spatial awareness."""
        piper = PiperEntity()
        piper.update_spatial_context("Planning meeting")
        assert piper.spatial_awareness == "Planning meeting"
        assert piper.where_am_i() == "Planning meeting"

    def test_set_attention_single(self):
        """set_attention sets single focus."""
        piper = PiperEntity()
        piper.set_attention("sprint planning")
        assert piper.attention_focus == ["sprint planning"]

    def test_set_attention_multiple(self):
        """set_attention sets multiple focuses."""
        piper = PiperEntity()
        piper.set_attention("sprint", "backlog", "velocity")
        assert piper.attention_focus == ["sprint", "backlog", "velocity"]

    def test_set_attention_replaces(self):
        """set_attention replaces previous focuses."""
        piper = PiperEntity()
        piper.set_attention("first")
        piper.set_attention("second", "third")
        assert piper.attention_focus == ["second", "third"]

    def test_add_situation(self):
        """add_situation adds situation ID."""
        piper = PiperEntity()
        piper.add_situation("standup-001")
        assert "standup-001" in piper.active_situations

    def test_add_situation_no_duplicates(self):
        """add_situation doesn't add duplicates."""
        piper = PiperEntity()
        piper.add_situation("standup-001")
        piper.add_situation("standup-001")
        assert piper.active_situations.count("standup-001") == 1

    def test_remove_situation(self):
        """remove_situation removes situation ID."""
        piper = PiperEntity()
        piper.add_situation("standup-001")
        piper.add_situation("planning-002")
        piper.remove_situation("standup-001")
        assert "standup-001" not in piper.active_situations
        assert "planning-002" in piper.active_situations

    def test_remove_situation_not_present(self):
        """remove_situation does nothing if not present."""
        piper = PiperEntity()
        piper.remove_situation("not-there")  # Should not raise


class TestPiperEntityStateQueries:
    """Tests for PiperEntity state query methods."""

    def test_is_overwhelmed_false(self):
        """is_overwhelmed returns False when not overwhelmed."""
        piper = PiperEntity()
        assert piper.is_overwhelmed() is False

    def test_is_overwhelmed_true(self):
        """is_overwhelmed returns True when overwhelmed."""
        piper = PiperEntity(awareness_level=AwarenessLevel.OVERWHELMED)
        assert piper.is_overwhelmed() is True

    def test_is_focused_empty(self):
        """is_focused returns False when no attention focus."""
        piper = PiperEntity()
        assert piper.is_focused() is False

    def test_is_focused_with_attention(self):
        """is_focused returns True when has attention focus."""
        piper = PiperEntity()
        piper.set_attention("something")
        assert piper.is_focused() is True

    def test_get_trust_level_unknown(self):
        """get_trust_level returns UNKNOWN for unknown entity."""
        piper = PiperEntity()
        assert piper.get_trust_level("unknown-entity") == TrustLevel.UNKNOWN

    def test_get_trust_level_known(self):
        """get_trust_level returns stored level."""
        piper = PiperEntity(trust_boundaries={"user-1": TrustLevel.TRUSTED})
        assert piper.get_trust_level("user-1") == TrustLevel.TRUSTED

    def test_set_trust_level(self):
        """set_trust_level stores trust level."""
        piper = PiperEntity()
        piper.set_trust_level("user-1", TrustLevel.FULL)
        assert piper.get_trust_level("user-1") == TrustLevel.FULL


class TestEntityContextDefaults:
    """Tests for EntityContext default values."""

    def test_default_values(self):
        """EntityContext has sensible defaults."""
        ctx = EntityContext(entity_id="entity-1")
        assert ctx.entity_id == "entity-1"
        assert ctx.current_role == EntityRole.ACTOR
        assert ctx.in_moment is None
        assert ctx.in_place is None
        assert ctx.as_entity is True
        assert ctx.as_place is False


class TestEntityContextRoleSwitching:
    """Tests for EntityContext role switching methods."""

    def test_switch_to_actor(self):
        """switch_to_actor sets ACTOR role."""
        ctx = EntityContext(entity_id="entity-1")
        ctx.switch_to_place()  # Start as place
        ctx.switch_to_actor()
        assert ctx.current_role == EntityRole.ACTOR
        assert ctx.as_entity is True
        assert ctx.as_place is False

    def test_switch_to_actor_with_moment(self):
        """switch_to_actor can set moment ID."""
        ctx = EntityContext(entity_id="entity-1")
        ctx.switch_to_actor(moment_id="moment-123")
        assert ctx.current_role == EntityRole.ACTOR
        assert ctx.in_moment == "moment-123"

    def test_switch_to_place(self):
        """switch_to_place sets PLACE role."""
        ctx = EntityContext(entity_id="entity-1")
        ctx.switch_to_place()
        assert ctx.current_role == EntityRole.PLACE
        assert ctx.as_entity is False
        assert ctx.as_place is True

    def test_switch_to_observer(self):
        """switch_to_observer sets OBSERVER role."""
        ctx = EntityContext(entity_id="entity-1")
        ctx.switch_to_observer(moment_id="moment-456")
        assert ctx.current_role == EntityRole.OBSERVER
        assert ctx.in_moment == "moment-456"
        assert ctx.as_entity is True
        assert ctx.as_place is False

    def test_switch_to_participant(self):
        """switch_to_participant sets PARTICIPANT role."""
        ctx = EntityContext(entity_id="entity-1")
        ctx.switch_to_participant(moment_id="moment-789")
        assert ctx.current_role == EntityRole.PARTICIPANT
        assert ctx.in_moment == "moment-789"
        assert ctx.as_entity is True
        assert ctx.as_place is False

    def test_switch_to_participant_with_place(self):
        """switch_to_participant can set place ID."""
        ctx = EntityContext(entity_id="entity-1")
        ctx.switch_to_participant(moment_id="moment-789", place_id="place-abc")
        assert ctx.in_moment == "moment-789"
        assert ctx.in_place == "place-abc"


class TestEntityContextQueries:
    """Tests for EntityContext query methods."""

    def test_is_participating_in_true(self):
        """is_participating_in returns True for current moment."""
        ctx = EntityContext(entity_id="entity-1")
        ctx.switch_to_participant(moment_id="moment-123")
        assert ctx.is_participating_in("moment-123") is True

    def test_is_participating_in_false(self):
        """is_participating_in returns False for other moment."""
        ctx = EntityContext(entity_id="entity-1")
        ctx.switch_to_participant(moment_id="moment-123")
        assert ctx.is_participating_in("moment-456") is False

    def test_is_located_in_true(self):
        """is_located_in returns True for current place."""
        ctx = EntityContext(entity_id="entity-1")
        ctx.switch_to_participant(moment_id="m", place_id="place-abc")
        assert ctx.is_located_in("place-abc") is True

    def test_is_located_in_false(self):
        """is_located_in returns False for other place."""
        ctx = EntityContext(entity_id="entity-1")
        ctx.switch_to_participant(moment_id="m", place_id="place-abc")
        assert ctx.is_located_in("place-xyz") is False


class TestConsciousnessExpressionPatterns:
    """Tests for ConsciousnessExpression first-person patterns."""

    def test_has_patterns_for_all_emotional_states(self):
        """ConsciousnessExpression has patterns for all emotional states."""
        patterns = ConsciousnessExpression.FIRST_PERSON_PATTERNS
        assert EmotionalState.CURIOUS in patterns
        assert EmotionalState.CONCERNED in patterns
        assert EmotionalState.SATISFIED in patterns
        assert EmotionalState.PUZZLED in patterns

    def test_curious_patterns_exist(self):
        """CURIOUS has multiple expression patterns."""
        patterns = ConsciousnessExpression.FIRST_PERSON_PATTERNS[EmotionalState.CURIOUS]
        assert len(patterns) >= 2
        assert any("I notice" in p for p in patterns)

    def test_concerned_patterns_exist(self):
        """CONCERNED has multiple expression patterns."""
        patterns = ConsciousnessExpression.FIRST_PERSON_PATTERNS[EmotionalState.CONCERNED]
        assert len(patterns) >= 2
        assert any("I'm concerned" in p for p in patterns)


class TestConsciousnessExpressionExpress:
    """Tests for ConsciousnessExpression.express method."""

    def test_express_with_curious_state(self):
        """express generates curious expression."""
        piper = PiperEntity(emotional_state=EmotionalState.CURIOUS)
        result = ConsciousnessExpression.express(piper, "the sprint is on track", "observation")
        assert "I notice the sprint is on track" == result

    def test_express_with_concerned_state(self):
        """express generates concerned expression."""
        piper = PiperEntity(emotional_state=EmotionalState.CONCERNED)
        result = ConsciousnessExpression.express(piper, "deadline slipping", "issue")
        assert "I'm concerned about deadline slipping" == result

    def test_express_with_puzzled_state(self):
        """express generates puzzled expression."""
        piper = PiperEntity(emotional_state=EmotionalState.PUZZLED)
        result = ConsciousnessExpression.express(piper, "the requirements", "uncertainty")
        assert "I'm not sure about the requirements" == result

    def test_express_falls_back_to_first_pattern(self):
        """express falls back to first pattern with non-matching type."""
        piper = PiperEntity(emotional_state=EmotionalState.CURIOUS)
        result = ConsciousnessExpression.express(piper, "something odd", "nonexistent_type")
        # Should use first pattern's placeholder
        assert "I notice something odd" == result


class TestConsciousnessExpressionConvenienceMethods:
    """Tests for ConsciousnessExpression convenience methods."""

    def test_express_awareness(self):
        """express_awareness generates observation expression."""
        piper = PiperEntity(emotional_state=EmotionalState.SATISFIED)
        result = ConsciousnessExpression.express_awareness(piper, "progress is good")
        assert "I notice progress is good" == result

    def test_express_concern(self):
        """express_concern always uses concerned pattern."""
        piper = PiperEntity(emotional_state=EmotionalState.CURIOUS)  # Different state
        result = ConsciousnessExpression.express_concern(piper, "the blocker")
        assert "I'm concerned about the blocker" == result

    def test_express_uncertainty(self):
        """express_uncertainty always uses puzzled pattern."""
        piper = PiperEntity(emotional_state=EmotionalState.SATISFIED)  # Different state
        result = ConsciousnessExpression.express_uncertainty(piper, "how to proceed")
        assert "I'm not sure about how to proceed" == result


class TestConsciousnessIntegration:
    """Integration tests for full consciousness system."""

    def test_piper_with_full_consciousness_profile(self):
        """Test PiperEntity with full consciousness configuration."""
        piper = PiperEntity(
            id="piper-test",
            awareness_level=AwarenessLevel.FOCUSED,
            emotional_state=EmotionalState.CURIOUS,
            available_capabilities=[
                Capability(name="planning", description="Plan sprints"),
                Capability(name="tracking", description="Track progress"),
            ],
            blocked_capabilities=[
                Capability(
                    name="github",
                    description="GitHub integration",
                    blocked_by="Missing token",
                ),
            ],
            trust_boundaries={"user-alice": TrustLevel.TRUSTED},
            temporal_awareness="Mid-sprint review",
            spatial_awareness="In retrospective meeting",
        )

        # Check identity
        assert piper.who_am_i() == "I am Piper Morgan, an AI PM assistant"

        # Check context
        assert piper.when_am_i() == "Mid-sprint review"
        assert piper.where_am_i() == "In retrospective meeting"

        # Check capabilities
        assert "2 capabilities available, 0 active, 1 blocked" == piper.what_can_i_do()

        # Check trust
        assert piper.get_trust_level("user-alice") == TrustLevel.TRUSTED
        assert piper.get_trust_level("unknown") == TrustLevel.UNKNOWN

        # Check state
        assert piper.is_overwhelmed() is False

    def test_entity_role_fluidity(self):
        """Test that entity can switch between roles fluidly."""
        # A Team entity that can be both ACTOR and PLACE
        ctx = EntityContext(entity_id="team-engineering")

        # Team as actor (taking action)
        ctx.switch_to_actor(moment_id="sprint-planning")
        assert ctx.current_role == EntityRole.ACTOR
        assert ctx.as_entity is True
        assert ctx.as_place is False

        # Team as place (where work happens)
        ctx.switch_to_place()
        assert ctx.current_role == EntityRole.PLACE
        assert ctx.as_entity is False
        assert ctx.as_place is True

        # Team as observer (watching demo)
        ctx.switch_to_observer(moment_id="demo-meeting")
        assert ctx.current_role == EntityRole.OBSERVER
        assert ctx.in_moment == "demo-meeting"

    def test_expression_changes_with_emotional_state(self):
        """Test that expression changes based on emotional state."""
        piper = PiperEntity()
        content = "the deadline is approaching"

        # Curious state
        piper.emotional_state = EmotionalState.CURIOUS
        curious_expr = ConsciousnessExpression.express(piper, content, "observation")
        assert "I notice" in curious_expr

        # Concerned state
        piper.emotional_state = EmotionalState.CONCERNED
        concerned_expr = ConsciousnessExpression.express(piper, content, "issue")
        assert "I'm concerned" in concerned_expr

        # Expressions are different
        assert curious_expr != concerned_expr
