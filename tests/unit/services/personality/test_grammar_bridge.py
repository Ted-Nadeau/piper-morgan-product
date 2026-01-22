"""
Tests for PersonalityGrammarBridge.

Issue #627: GRAMMAR-TRANSFORM: Personality System
Phase 2: Narrative Bridge Tests
"""

import pytest

from services.personality.grammar_bridge import PersonalityGrammarBridge
from services.personality.grammar_context import (
    GrammarLens,
    PersonalityGrammarContext,
    SituationType,
)
from services.personality.personality_profile import ConfidenceDisplayStyle


class TestGetGreeting:
    """Test greeting generation."""

    def test_warm_first_interaction(self):
        """Warm greeting for first interaction."""
        bridge = PersonalityGrammarBridge()
        ctx = PersonalityGrammarContext(
            warmth_level=0.8,
            is_first_interaction=True,
        )
        result = bridge.get_greeting(ctx)

        assert "Hey" in result or "Hi" in result
        assert "Piper" in result  # Introduces self

    def test_professional_first_interaction(self):
        """Professional greeting for first interaction."""
        bridge = PersonalityGrammarBridge()
        ctx = PersonalityGrammarContext(
            warmth_level=0.3,
            is_first_interaction=True,
        )
        result = bridge.get_greeting(ctx)

        assert "Piper" in result

    def test_returning_user(self):
        """Greeting for returning user."""
        bridge = PersonalityGrammarBridge()
        ctx = PersonalityGrammarContext(
            warmth_level=0.7,
            is_first_interaction=False,
        )
        result = bridge.get_greeting(ctx)

        assert "again" in result.lower() or "back" in result.lower()


class TestGetSituationPhrase:
    """Test situation phrase generation."""

    def test_success_warm(self):
        """Success phrase with warm tone."""
        bridge = PersonalityGrammarBridge()
        ctx = PersonalityGrammarContext(
            warmth_level=0.8,
            situation=SituationType.SUCCESS,
        )
        result = bridge.get_situation_phrase(ctx)

        assert "well" in result.lower() or "worked" in result.lower()

    def test_error_warm(self):
        """Error phrase with warm tone."""
        bridge = PersonalityGrammarBridge()
        ctx = PersonalityGrammarContext(
            warmth_level=0.8,
            situation=SituationType.ERROR,
        )
        result = bridge.get_situation_phrase(ctx)

        assert "ran into" in result.lower() or "something" in result.lower()

    def test_clarification_professional(self):
        """Clarification phrase with professional tone."""
        bridge = PersonalityGrammarBridge()
        ctx = PersonalityGrammarContext(
            warmth_level=0.3,
            situation=SituationType.CLARIFICATION,
        )
        result = bridge.get_situation_phrase(ctx)

        assert "clarif" in result.lower()  # Matches "clarify" or "clarification"

    def test_busy_terse(self):
        """Busy situation with terse tone returns empty."""
        bridge = PersonalityGrammarBridge()
        ctx = PersonalityGrammarContext(
            warmth_level=0.5,
            situation=SituationType.BUSY,
            seems_busy=True,
        )
        result = bridge.get_situation_phrase(ctx)

        assert result == ""  # No preamble when terse


class TestGetErrorPhrase:
    """Test error phrase generation."""

    def test_warm_error(self):
        """Error with warm tone."""
        bridge = PersonalityGrammarBridge()
        ctx = PersonalityGrammarContext(
            warmth_level=0.8,
            situation=SituationType.ERROR,
        )
        result = bridge.get_error_phrase(ctx)

        assert "help" in result.lower() or "trouble" in result.lower()

    def test_professional_error(self):
        """Error with professional tone."""
        bridge = PersonalityGrammarBridge()
        ctx = PersonalityGrammarContext(warmth_level=0.3)
        result = bridge.get_error_phrase(ctx)

        assert "error" in result.lower() or "problem" in result.lower()


class TestGetConfidencePhrase:
    """Test confidence phrase generation."""

    def test_high_confidence_warm(self):
        """High confidence with warm tone."""
        bridge = PersonalityGrammarBridge()
        ctx = PersonalityGrammarContext(warmth_level=0.8)
        result = bridge.get_confidence_phrase(ctx, confidence=0.95)

        assert "confident" in result.lower()

    def test_medium_confidence(self):
        """Medium confidence phrase."""
        bridge = PersonalityGrammarBridge()
        ctx = PersonalityGrammarContext(warmth_level=0.6)
        result = bridge.get_confidence_phrase(ctx, confidence=0.8)

        assert "believe" in result.lower() or "think" in result.lower()

    def test_low_confidence(self):
        """Low confidence phrase."""
        bridge = PersonalityGrammarBridge()
        ctx = PersonalityGrammarContext(warmth_level=0.6)
        result = bridge.get_confidence_phrase(ctx, confidence=0.5)

        assert "uncertain" in result.lower() or "not entirely" in result.lower()

    def test_hidden_confidence(self):
        """Hidden confidence style returns empty."""
        bridge = PersonalityGrammarBridge()
        ctx = PersonalityGrammarContext(confidence_style=ConfidenceDisplayStyle.HIDDEN)
        result = bridge.get_confidence_phrase(ctx, confidence=0.95)

        assert result == ""


class TestGetClosing:
    """Test closing phrase generation."""

    def test_warm_closing(self):
        """Warm closing phrase."""
        bridge = PersonalityGrammarBridge()
        ctx = PersonalityGrammarContext(warmth_level=0.8)
        result = bridge.get_closing(ctx)

        assert "help" in result.lower() or "anything" in result.lower()

    def test_terse_no_closing(self):
        """Terse tone has no closing."""
        bridge = PersonalityGrammarBridge()
        ctx = PersonalityGrammarContext(
            warmth_level=0.5,
            seems_busy=True,
        )
        result = bridge.get_closing(ctx)

        assert result == ""


class TestGetLensPhrase:
    """Test lens phrase generation."""

    def test_collaborative_lens_warm(self):
        """Collaborative lens with warm tone."""
        bridge = PersonalityGrammarBridge()
        ctx = PersonalityGrammarContext(
            warmth_level=0.8,
            active_lenses=[GrammarLens.COLLABORATIVE],
        )
        result = bridge.get_lens_phrase(ctx, GrammarLens.COLLABORATIVE)

        assert "together" in result.lower()

    def test_temporal_lens(self):
        """Temporal lens phrase."""
        bridge = PersonalityGrammarBridge()
        ctx = PersonalityGrammarContext(
            warmth_level=0.8,
            active_lenses=[GrammarLens.TEMPORAL],
        )
        result = bridge.get_lens_phrase(ctx, GrammarLens.TEMPORAL)

        assert "time" in result.lower() or "tight" in result.lower()

    def test_epistemic_lens(self):
        """Epistemic lens phrase."""
        bridge = PersonalityGrammarBridge()
        ctx = PersonalityGrammarContext(
            warmth_level=0.6,
            active_lenses=[GrammarLens.EPISTEMIC],
        )
        result = bridge.get_lens_phrase(ctx, GrammarLens.EPISTEMIC)

        assert "clear" in result.lower()

    def test_inactive_lens_empty(self):
        """Inactive lens returns empty."""
        bridge = PersonalityGrammarBridge()
        ctx = PersonalityGrammarContext(active_lenses=[])
        result = bridge.get_lens_phrase(ctx, GrammarLens.COLLABORATIVE)

        assert result == ""


class TestNarrateRelationship:
    """Test relationship narration."""

    def test_first_time(self):
        """First interaction."""
        bridge = PersonalityGrammarBridge()
        ctx = PersonalityGrammarContext(is_first_interaction=True)
        result = bridge.narrate_relationship(ctx)

        assert "first time" in result.lower()

    def test_few_interactions(self):
        """Few previous interactions."""
        bridge = PersonalityGrammarBridge()
        ctx = PersonalityGrammarContext(
            is_first_interaction=False,
            interaction_count=4,
        )
        result = bridge.narrate_relationship(ctx)

        assert "few" in result.lower()

    def test_many_interactions(self):
        """Many previous interactions."""
        bridge = PersonalityGrammarBridge()
        ctx = PersonalityGrammarContext(
            is_first_interaction=False,
            interaction_count=15,
        )
        result = bridge.narrate_relationship(ctx)

        assert "while" in result.lower()


class TestApplyPersonality:
    """Test apply_personality_to_message."""

    def test_basic_message(self):
        """Basic message without additions."""
        bridge = PersonalityGrammarBridge()
        ctx = PersonalityGrammarContext()
        result = bridge.apply_personality_to_message(
            "Here's your data.",
            ctx,
        )

        assert "Here's your data." in result

    def test_with_greeting(self):
        """Message with greeting."""
        bridge = PersonalityGrammarBridge()
        ctx = PersonalityGrammarContext(warmth_level=0.8)
        result = bridge.apply_personality_to_message(
            "Here's your data.",
            ctx,
            include_greeting=True,
        )

        assert "Hi" in result or "Hey" in result
        assert "Here's your data." in result

    def test_with_closing(self):
        """Message with closing."""
        bridge = PersonalityGrammarBridge()
        ctx = PersonalityGrammarContext(warmth_level=0.8)
        result = bridge.apply_personality_to_message(
            "Here's your data.",
            ctx,
            include_closing=True,
        )

        assert "Here's your data." in result
        assert "help" in result.lower() or "else" in result.lower()

    def test_with_situation(self):
        """Message with situation phrase."""
        bridge = PersonalityGrammarBridge()
        ctx = PersonalityGrammarContext(
            warmth_level=0.8,
            situation=SituationType.SUCCESS,
        )
        result = bridge.apply_personality_to_message(
            "Task completed.",
            ctx,
        )

        assert "Task completed." in result
        assert "well" in result.lower() or "worked" in result.lower()

    def test_unavailable_personality(self):
        """Unavailable personality returns message unchanged."""
        bridge = PersonalityGrammarBridge()
        ctx = PersonalityGrammarContext(personality_available=False)
        result = bridge.apply_personality_to_message(
            "Original message.",
            ctx,
            include_greeting=True,
            include_closing=True,
        )

        assert result == "Original message."


class TestContractorTest:
    """Verify phrases pass the Contractor Test."""

    def test_no_raw_data_terms(self):
        """Phrases don't use raw data terms."""
        bridge = PersonalityGrammarBridge()
        ctx = PersonalityGrammarContext(
            warmth_level=0.8,
            situation=SituationType.ERROR,
        )

        greeting = bridge.get_greeting(ctx)
        error = bridge.get_error_phrase(ctx)
        closing = bridge.get_closing(ctx)

        combined = f"{greeting} {error} {closing}"

        # No technical terms
        assert "warmth_level" not in combined
        assert "situation_type" not in combined
        assert "formality" not in combined

    def test_natural_language(self):
        """Phrases use natural language."""
        bridge = PersonalityGrammarBridge()

        # Phrases should be capitalized and readable
        ctx = PersonalityGrammarContext(warmth_level=0.8)
        greeting = bridge.get_greeting(ctx)

        assert greeting[0].isupper()
        assert "!!!" not in greeting

    def test_professional_appropriate(self):
        """Professional phrases are appropriately formal."""
        bridge = PersonalityGrammarBridge()
        ctx = PersonalityGrammarContext(warmth_level=0.3)

        greeting = bridge.get_greeting(ctx)
        closing = bridge.get_closing(ctx)

        # No overly casual language
        assert "Hey there" not in greeting
        assert "!" not in greeting or greeting.count("!") <= 1
