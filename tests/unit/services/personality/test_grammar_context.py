"""
Tests for PersonalityGrammarContext.

Issue #627: GRAMMAR-TRANSFORM: Personality System
Phase 1: Response Context Tests
"""

from datetime import datetime

import pytest

from services.personality.grammar_context import (
    GrammarLens,
    PersonalityGrammarContext,
    SituationType,
)
from services.personality.personality_profile import (
    ActionLevel,
    ConfidenceDisplayStyle,
    PersonalityProfile,
    TechnicalPreference,
)


class TestFromPersonalityProfile:
    """Test building context from PersonalityProfile."""

    def test_basic_profile(self):
        """Build from basic profile."""
        profile = PersonalityProfile(
            id="test",
            user_id="user-1",
            warmth_level=0.7,
            confidence_style=ConfidenceDisplayStyle.CONTEXTUAL,
            action_orientation=ActionLevel.MEDIUM,
            technical_depth=TechnicalPreference.BALANCED,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        ctx = PersonalityGrammarContext.from_personality_profile(profile)

        assert ctx.warmth_level == 0.7
        assert ctx.personality_available is True
        assert GrammarLens.COLLABORATIVE in ctx.active_lenses

    def test_error_situation(self):
        """Error situation adds temporal lens."""
        profile = PersonalityProfile.get_default("user-1")
        ctx = PersonalityGrammarContext.from_personality_profile(
            profile,
            situation=SituationType.ERROR,
        )

        assert ctx.situation == SituationType.ERROR
        assert GrammarLens.TEMPORAL in ctx.active_lenses

    def test_clarification_situation(self):
        """Clarification adds epistemic lens."""
        profile = PersonalityProfile.get_default("user-1")
        ctx = PersonalityGrammarContext.from_personality_profile(
            profile,
            situation=SituationType.CLARIFICATION,
        )

        assert GrammarLens.EPISTEMIC in ctx.active_lenses

    def test_interaction_count(self):
        """Interaction count sets first interaction flag."""
        profile = PersonalityProfile.get_default("user-1")

        first = PersonalityGrammarContext.from_personality_profile(profile, interaction_count=0)
        assert first.is_first_interaction is True

        repeat = PersonalityGrammarContext.from_personality_profile(profile, interaction_count=5)
        assert repeat.is_first_interaction is False
        assert repeat.interaction_count == 5


class TestFromDict:
    """Test building context from dictionary."""

    def test_empty_dict(self):
        """Empty dict returns unavailable."""
        ctx = PersonalityGrammarContext.from_dict({})

        assert ctx.personality_available is False

    def test_none_returns_unavailable(self):
        """None returns unavailable."""
        ctx = PersonalityGrammarContext.from_dict(None)

        assert ctx.personality_available is False

    def test_basic_dict(self):
        """Build from basic dict."""
        data = {
            "warmth_level": 0.8,
            "confidence_style": "numeric",
            "action_level": "high",
        }
        ctx = PersonalityGrammarContext.from_dict(data)

        assert ctx.warmth_level == 0.8
        assert ctx.confidence_style == ConfidenceDisplayStyle.NUMERIC
        assert ctx.action_level == ActionLevel.HIGH

    def test_invalid_warmth_defaults(self):
        """Invalid warmth level defaults to 0.6."""
        data = {"warmth_level": 5.0}  # Invalid
        ctx = PersonalityGrammarContext.from_dict(data)

        assert ctx.warmth_level == 0.6

    def test_invalid_enum_defaults(self):
        """Invalid enum values default."""
        data = {
            "confidence_style": "invalid",
            "action_level": "invalid",
        }
        ctx = PersonalityGrammarContext.from_dict(data)

        assert ctx.confidence_style == ConfidenceDisplayStyle.CONTEXTUAL
        assert ctx.action_level == ActionLevel.MEDIUM


class TestWarmthMethods:
    """Test warmth-related methods."""

    def test_is_warm(self):
        """High warmth detected."""
        warm = PersonalityGrammarContext(warmth_level=0.8)
        assert warm.is_warm() is True

        not_warm = PersonalityGrammarContext(warmth_level=0.5)
        assert not_warm.is_warm() is False

    def test_is_professional(self):
        """Low warmth = professional."""
        pro = PersonalityGrammarContext(warmth_level=0.3)
        assert pro.is_professional() is True

        casual = PersonalityGrammarContext(warmth_level=0.6)
        assert casual.is_professional() is False

    def test_needs_extra_warmth(self):
        """Error/frustrated needs extra warmth."""
        error = PersonalityGrammarContext(situation=SituationType.ERROR)
        assert error.needs_extra_warmth() is True

        frustrated = PersonalityGrammarContext(situation=SituationType.FRUSTRATED)
        assert frustrated.needs_extra_warmth() is True

        normal = PersonalityGrammarContext(situation=SituationType.NORMAL)
        assert normal.needs_extra_warmth() is False


class TestEffectiveWarmth:
    """Test effective warmth calculation."""

    def test_normal_situation(self):
        """Normal situation uses base warmth."""
        ctx = PersonalityGrammarContext(warmth_level=0.5)
        assert ctx.get_effective_warmth() == 0.5

    def test_error_increases_warmth(self):
        """Error situation increases warmth."""
        ctx = PersonalityGrammarContext(
            warmth_level=0.5,
            situation=SituationType.ERROR,
        )
        assert ctx.get_effective_warmth() == 0.7  # +0.2

    def test_warmth_capped_at_1(self):
        """Warmth can't exceed 1.0."""
        ctx = PersonalityGrammarContext(
            warmth_level=0.9,
            situation=SituationType.ERROR,
        )
        assert ctx.get_effective_warmth() == 1.0


class TestFormality:
    """Test formality calculation."""

    def test_warm_formality(self):
        """High warmth -> warm formality."""
        ctx = PersonalityGrammarContext(warmth_level=0.8)
        assert ctx.get_formality() == "warm"

    def test_professional_formality(self):
        """Low warmth -> professional formality."""
        ctx = PersonalityGrammarContext(warmth_level=0.3)
        assert ctx.get_formality() == "professional"

    def test_conversational_formality(self):
        """Medium warmth -> conversational."""
        ctx = PersonalityGrammarContext(warmth_level=0.5)
        assert ctx.get_formality() == "conversational"

    def test_busy_is_terse(self):
        """Busy situation -> terse."""
        ctx = PersonalityGrammarContext(
            warmth_level=0.8,  # Would normally be warm
            seems_busy=True,
        )
        assert ctx.get_formality() == "terse"


class TestConciseness:
    """Test conciseness detection."""

    def test_busy_is_concise(self):
        """Busy user -> concise."""
        ctx = PersonalityGrammarContext(seems_busy=True)
        assert ctx.should_be_concise() is True

    def test_busy_situation_is_concise(self):
        """Busy situation -> concise."""
        ctx = PersonalityGrammarContext(situation=SituationType.BUSY)
        assert ctx.should_be_concise() is True

    def test_normal_not_concise(self):
        """Normal situation -> not concise."""
        ctx = PersonalityGrammarContext()
        assert ctx.should_be_concise() is False


class TestLenses:
    """Test lens methods."""

    def test_has_lens(self):
        """Check lens presence."""
        ctx = PersonalityGrammarContext(
            active_lenses=[GrammarLens.COLLABORATIVE, GrammarLens.TEMPORAL]
        )

        assert ctx.has_lens(GrammarLens.COLLABORATIVE) is True
        assert ctx.has_lens(GrammarLens.TEMPORAL) is True
        assert ctx.has_lens(GrammarLens.EPISTEMIC) is False


class TestConfidenceApproach:
    """Test confidence approach descriptions."""

    def test_numeric(self):
        """Numeric confidence approach."""
        ctx = PersonalityGrammarContext(confidence_style=ConfidenceDisplayStyle.NUMERIC)
        assert "percentage" in ctx.get_confidence_approach().lower()

    def test_descriptive(self):
        """Descriptive confidence approach."""
        ctx = PersonalityGrammarContext(confidence_style=ConfidenceDisplayStyle.DESCRIPTIVE)
        assert "likely" in ctx.get_confidence_approach().lower()

    def test_hidden(self):
        """Hidden confidence approach."""
        ctx = PersonalityGrammarContext(confidence_style=ConfidenceDisplayStyle.HIDDEN)
        assert "avoid" in ctx.get_confidence_approach().lower()
