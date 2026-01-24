"""
Unit tests for ProactivityGate.

Issue #648: TRUST-LEVELS-2 - Integration
ADR-053: Trust Computation Architecture

Tests stage-based behavior gating logic.
"""

import pytest

from services.shared_types import TrustStage
from services.trust.proactivity_gate import PROACTIVITY_CONFIGS, ProactivityConfig, ProactivityGate


class TestProactivityConfigDataclass:
    """Test ProactivityConfig dataclass."""

    def test_config_has_required_fields(self):
        """ProactivityConfig has all required fields."""
        config = ProactivityConfig(
            can_offer_hints=True,
            can_suggest=False,
            can_act_autonomously=False,
            max_suggestions_per_session=5,
            suggestion_delay_seconds=3,
        )
        assert config.can_offer_hints is True
        assert config.can_suggest is False
        assert config.can_act_autonomously is False
        assert config.max_suggestions_per_session == 5
        assert config.suggestion_delay_seconds == 3


class TestProactivityConfigsMapping:
    """Test PROACTIVITY_CONFIGS constant."""

    def test_all_stages_have_config(self):
        """Every TrustStage has a configuration."""
        for stage in TrustStage:
            assert stage in PROACTIVITY_CONFIGS, f"Missing config for {stage}"

    def test_new_stage_blocks_all(self):
        """NEW stage blocks all proactive behavior."""
        config = PROACTIVITY_CONFIGS[TrustStage.NEW]
        assert config.can_offer_hints is False
        assert config.can_suggest is False
        assert config.can_act_autonomously is False
        assert config.max_suggestions_per_session == 0

    def test_building_stage_allows_hints_only(self):
        """BUILDING stage allows hints but not suggestions or autonomous."""
        config = PROACTIVITY_CONFIGS[TrustStage.BUILDING]
        assert config.can_offer_hints is True
        assert config.can_suggest is False
        assert config.can_act_autonomously is False
        assert config.max_suggestions_per_session > 0

    def test_established_stage_allows_suggestions(self):
        """ESTABLISHED stage allows hints and suggestions."""
        config = PROACTIVITY_CONFIGS[TrustStage.ESTABLISHED]
        assert config.can_offer_hints is True
        assert config.can_suggest is True
        assert config.can_act_autonomously is False

    def test_trusted_stage_allows_all(self):
        """TRUSTED stage allows all proactive behaviors."""
        config = PROACTIVITY_CONFIGS[TrustStage.TRUSTED]
        assert config.can_offer_hints is True
        assert config.can_suggest is True
        assert config.can_act_autonomously is True

    def test_suggestion_delay_decreases_with_trust(self):
        """Higher trust stages have shorter suggestion delays."""
        new_delay = PROACTIVITY_CONFIGS[TrustStage.NEW].suggestion_delay_seconds
        building_delay = PROACTIVITY_CONFIGS[TrustStage.BUILDING].suggestion_delay_seconds
        established_delay = PROACTIVITY_CONFIGS[TrustStage.ESTABLISHED].suggestion_delay_seconds
        trusted_delay = PROACTIVITY_CONFIGS[TrustStage.TRUSTED].suggestion_delay_seconds

        # NEW has 0 delay but also 0 suggestions allowed
        assert building_delay > established_delay
        assert established_delay >= trusted_delay
        assert trusted_delay == 0  # No delay for trusted users


class TestCanOfferCapabilityHints:
    """Test can_offer_capability_hints method."""

    @pytest.fixture
    def gate(self):
        """Create ProactivityGate instance."""
        return ProactivityGate()

    def test_new_stage_cannot_offer_hints(self, gate):
        """NEW stage: cannot offer capability hints."""
        assert gate.can_offer_capability_hints(TrustStage.NEW) is False

    def test_building_stage_can_offer_hints(self, gate):
        """BUILDING stage: can offer capability hints."""
        assert gate.can_offer_capability_hints(TrustStage.BUILDING) is True

    def test_established_stage_can_offer_hints(self, gate):
        """ESTABLISHED stage: can offer capability hints."""
        assert gate.can_offer_capability_hints(TrustStage.ESTABLISHED) is True

    def test_trusted_stage_can_offer_hints(self, gate):
        """TRUSTED stage: can offer capability hints."""
        assert gate.can_offer_capability_hints(TrustStage.TRUSTED) is True


class TestCanProactiveSuggest:
    """Test can_proactive_suggest method."""

    @pytest.fixture
    def gate(self):
        """Create ProactivityGate instance."""
        return ProactivityGate()

    def test_new_stage_cannot_suggest(self, gate):
        """NEW stage: cannot proactively suggest."""
        assert gate.can_proactive_suggest(TrustStage.NEW) is False

    def test_building_stage_cannot_suggest(self, gate):
        """BUILDING stage: cannot proactively suggest (hints only)."""
        assert gate.can_proactive_suggest(TrustStage.BUILDING) is False

    def test_established_stage_can_suggest(self, gate):
        """ESTABLISHED stage: can proactively suggest."""
        assert gate.can_proactive_suggest(TrustStage.ESTABLISHED) is True

    def test_trusted_stage_can_suggest(self, gate):
        """TRUSTED stage: can proactively suggest."""
        assert gate.can_proactive_suggest(TrustStage.TRUSTED) is True


class TestCanActWithoutAsking:
    """Test can_act_without_asking method."""

    @pytest.fixture
    def gate(self):
        """Create ProactivityGate instance."""
        return ProactivityGate()

    def test_new_stage_cannot_act(self, gate):
        """NEW stage: cannot act autonomously."""
        assert gate.can_act_without_asking(TrustStage.NEW) is False

    def test_building_stage_cannot_act(self, gate):
        """BUILDING stage: cannot act autonomously."""
        assert gate.can_act_without_asking(TrustStage.BUILDING) is False

    def test_established_stage_cannot_act(self, gate):
        """ESTABLISHED stage: cannot act autonomously."""
        assert gate.can_act_without_asking(TrustStage.ESTABLISHED) is False

    def test_trusted_stage_can_act(self, gate):
        """TRUSTED stage: can act autonomously."""
        assert gate.can_act_without_asking(TrustStage.TRUSTED) is True


class TestGetProactivityConfig:
    """Test get_proactivity_config method."""

    @pytest.fixture
    def gate(self):
        """Create ProactivityGate instance."""
        return ProactivityGate()

    def test_returns_dict_for_all_stages(self, gate):
        """Returns dict with all keys for every stage."""
        expected_keys = {
            "can_offer_hints",
            "can_suggest",
            "can_act_autonomously",
            "max_suggestions_per_session",
            "suggestion_delay_seconds",
        }
        for stage in TrustStage:
            config = gate.get_proactivity_config(stage)
            assert isinstance(config, dict)
            assert set(config.keys()) == expected_keys

    def test_new_stage_config(self, gate):
        """NEW stage config matches expected values."""
        config = gate.get_proactivity_config(TrustStage.NEW)
        assert config["can_offer_hints"] is False
        assert config["can_suggest"] is False
        assert config["can_act_autonomously"] is False
        assert config["max_suggestions_per_session"] == 0

    def test_trusted_stage_config(self, gate):
        """TRUSTED stage config matches expected values."""
        config = gate.get_proactivity_config(TrustStage.TRUSTED)
        assert config["can_offer_hints"] is True
        assert config["can_suggest"] is True
        assert config["can_act_autonomously"] is True


class TestGetMaxSuggestionsPerSession:
    """Test get_max_suggestions_per_session method."""

    @pytest.fixture
    def gate(self):
        """Create ProactivityGate instance."""
        return ProactivityGate()

    def test_new_stage_zero_suggestions(self, gate):
        """NEW stage: 0 suggestions allowed."""
        assert gate.get_max_suggestions_per_session(TrustStage.NEW) == 0

    def test_building_stage_limited_suggestions(self, gate):
        """BUILDING stage: limited suggestions."""
        max_suggestions = gate.get_max_suggestions_per_session(TrustStage.BUILDING)
        assert max_suggestions > 0
        assert max_suggestions < 5  # Should be modest

    def test_suggestions_increase_with_trust(self, gate):
        """Higher trust allows more suggestions."""
        new = gate.get_max_suggestions_per_session(TrustStage.NEW)
        building = gate.get_max_suggestions_per_session(TrustStage.BUILDING)
        established = gate.get_max_suggestions_per_session(TrustStage.ESTABLISHED)
        trusted = gate.get_max_suggestions_per_session(TrustStage.TRUSTED)

        assert new < building
        assert building < established
        assert established < trusted


class TestGetSuggestionDelaySeconds:
    """Test get_suggestion_delay_seconds method."""

    @pytest.fixture
    def gate(self):
        """Create ProactivityGate instance."""
        return ProactivityGate()

    def test_trusted_has_no_delay(self, gate):
        """TRUSTED stage: no delay."""
        assert gate.get_suggestion_delay_seconds(TrustStage.TRUSTED) == 0

    def test_building_has_delay(self, gate):
        """BUILDING stage: has delay (hesitation)."""
        delay = gate.get_suggestion_delay_seconds(TrustStage.BUILDING)
        assert delay > 0


class TestShouldSuggestNow:
    """Test should_suggest_now composite method."""

    @pytest.fixture
    def gate(self):
        """Create ProactivityGate instance."""
        return ProactivityGate()

    def test_new_stage_never_suggests(self, gate):
        """NEW stage: should never suggest."""
        assert gate.should_suggest_now(TrustStage.NEW, suggestions_this_session=0) is False

    def test_building_stage_never_suggests(self, gate):
        """BUILDING stage: should never suggest (hints only)."""
        assert gate.should_suggest_now(TrustStage.BUILDING, suggestions_this_session=0) is False

    def test_established_stage_suggests_under_limit(self, gate):
        """ESTABLISHED stage: suggests when under limit."""
        assert gate.should_suggest_now(TrustStage.ESTABLISHED, suggestions_this_session=0) is True

    def test_established_stage_respects_limit(self, gate):
        """ESTABLISHED stage: respects session limit."""
        max_suggestions = gate.get_max_suggestions_per_session(TrustStage.ESTABLISHED)
        # Under limit
        assert (
            gate.should_suggest_now(
                TrustStage.ESTABLISHED, suggestions_this_session=max_suggestions - 1
            )
            is True
        )
        # At limit
        assert (
            gate.should_suggest_now(
                TrustStage.ESTABLISHED, suggestions_this_session=max_suggestions
            )
            is False
        )
        # Over limit
        assert (
            gate.should_suggest_now(
                TrustStage.ESTABLISHED, suggestions_this_session=max_suggestions + 1
            )
            is False
        )

    def test_trusted_stage_suggests_under_limit(self, gate):
        """TRUSTED stage: suggests when under limit."""
        assert gate.should_suggest_now(TrustStage.TRUSTED, suggestions_this_session=0) is True

    def test_trusted_stage_respects_limit(self, gate):
        """TRUSTED stage: respects session limit (high but not infinite)."""
        max_suggestions = gate.get_max_suggestions_per_session(TrustStage.TRUSTED)
        assert (
            gate.should_suggest_now(TrustStage.TRUSTED, suggestions_this_session=max_suggestions)
            is False
        )


class TestEdgeCases:
    """Test edge cases and robustness."""

    @pytest.fixture
    def gate(self):
        """Create ProactivityGate instance."""
        return ProactivityGate()

    def test_multiple_instances_same_behavior(self):
        """Multiple gate instances behave identically."""
        gate1 = ProactivityGate()
        gate2 = ProactivityGate()

        for stage in TrustStage:
            assert gate1.can_offer_capability_hints(stage) == gate2.can_offer_capability_hints(
                stage
            )
            assert gate1.can_proactive_suggest(stage) == gate2.can_proactive_suggest(stage)
            assert gate1.can_act_without_asking(stage) == gate2.can_act_without_asking(stage)

    def test_gate_is_stateless(self, gate):
        """Gate methods don't modify state."""
        # Call methods multiple times
        for _ in range(10):
            gate.can_offer_capability_hints(TrustStage.BUILDING)
            gate.can_proactive_suggest(TrustStage.ESTABLISHED)
            gate.get_proactivity_config(TrustStage.TRUSTED)

        # Results should still be consistent
        assert gate.can_offer_capability_hints(TrustStage.BUILDING) is True
        assert gate.can_proactive_suggest(TrustStage.ESTABLISHED) is True
