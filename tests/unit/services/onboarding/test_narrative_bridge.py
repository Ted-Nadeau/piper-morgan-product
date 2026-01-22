"""
Tests for Onboarding Narrative Bridge.

Issue #626: GRAMMAR-TRANSFORM: Onboarding System
Phase 2: Narrative Bridge Tests
"""

import pytest

from services.onboarding.grammar_context import OnboardingGrammarContext, OnboardingStage
from services.onboarding.narrative_bridge import OnboardingNarrativeBridge


class TestGetWelcomeMessage:
    """Test welcome message generation."""

    def test_warm_welcome(self):
        """Warm welcome introduces Piper and asks about projects."""
        bridge = OnboardingNarrativeBridge()
        ctx = OnboardingGrammarContext(warmth_level=0.8)

        result = bridge.get_welcome_message(ctx)

        assert "Piper" in result
        assert "glad" in result.lower() or "help" in result.lower()
        assert "project" in result.lower()

    def test_conversational_welcome(self):
        """Conversational welcome is friendly but concise."""
        bridge = OnboardingNarrativeBridge()
        ctx = OnboardingGrammarContext(warmth_level=0.5)

        result = bridge.get_welcome_message(ctx)

        assert "Piper" in result
        assert "project" in result.lower()

    def test_professional_welcome(self):
        """Professional welcome is direct."""
        bridge = OnboardingNarrativeBridge()
        ctx = OnboardingGrammarContext(warmth_level=0.2)

        result = bridge.get_welcome_message(ctx)

        assert "Piper" in result
        assert "Hello" in result


class TestAcknowledgeProject:
    """Test project acknowledgment generation."""

    def test_first_project_warm(self):
        """First project gets enthusiastic acknowledgment."""
        bridge = OnboardingNarrativeBridge()
        ctx = OnboardingGrammarContext(
            warmth_level=0.8,
            projects_captured=1,
        )

        result = bridge.acknowledge_project(ctx, "TaskFlow")

        assert "TaskFlow" in result
        assert "great" in result.lower() or "love" in result.lower()

    def test_additional_project_warm(self):
        """Additional project acknowledged with continued interest."""
        bridge = OnboardingNarrativeBridge()
        ctx = OnboardingGrammarContext(
            warmth_level=0.8,
            projects_captured=2,
        )

        result = bridge.acknowledge_project(ctx, "Backend")

        assert "Backend" in result
        assert "too" in result.lower() or "both" in result.lower()

    def test_first_project_professional(self):
        """Professional acknowledgment is concise."""
        bridge = OnboardingNarrativeBridge()
        ctx = OnboardingGrammarContext(
            warmth_level=0.2,
            projects_captured=1,
        )

        result = bridge.acknowledge_project(ctx, "API")

        assert "API" in result
        assert "Noted" in result or "track" in result.lower()


class TestMoreProjectsPrompt:
    """Test prompts for additional projects."""

    def test_warm_prompt(self):
        """Warm prompt invites more sharing."""
        bridge = OnboardingNarrativeBridge()
        ctx = OnboardingGrammarContext(warmth_level=0.8)

        result = bridge.get_more_projects_prompt(ctx)

        assert "project" in result.lower()
        assert "happy" in result.lower() or "other" in result.lower()

    def test_conversational_prompt(self):
        """Conversational prompt asks naturally."""
        bridge = OnboardingNarrativeBridge()
        ctx = OnboardingGrammarContext(warmth_level=0.5)

        result = bridge.get_more_projects_prompt(ctx)

        assert "project" in result.lower()

    def test_professional_prompt(self):
        """Professional prompt is direct."""
        bridge = OnboardingNarrativeBridge()
        ctx = OnboardingGrammarContext(warmth_level=0.2)

        result = bridge.get_more_projects_prompt(ctx)

        assert "project" in result.lower() or "additional" in result.lower()


class TestConfirmationPrompt:
    """Test confirmation prompt generation."""

    def test_single_project_warm(self):
        """Single project confirmation is warm."""
        bridge = OnboardingNarrativeBridge()
        ctx = OnboardingGrammarContext(
            warmth_level=0.8,
            projects_captured=1,
            project_names=["Piper"],
        )

        result = bridge.get_confirmation_prompt(ctx)

        assert "Piper" in result
        assert "looking forward" in result.lower() or "portfolio" in result.lower()

    def test_multiple_projects_warm(self):
        """Multiple project confirmation mentions all."""
        bridge = OnboardingNarrativeBridge()
        ctx = OnboardingGrammarContext(
            warmth_level=0.8,
            projects_captured=2,
            project_names=["Piper", "TaskFlow"],
        )

        result = bridge.get_confirmation_prompt(ctx)

        assert "Piper" in result
        assert "TaskFlow" in result
        assert "excited" in result.lower() or "portfolio" in result.lower()

    def test_professional_confirmation(self):
        """Professional confirmation is brief."""
        bridge = OnboardingNarrativeBridge()
        ctx = OnboardingGrammarContext(
            warmth_level=0.2,
            projects_captured=1,
            project_names=["API"],
        )

        result = bridge.get_confirmation_prompt(ctx)

        assert "API" in result
        assert "Confirm" in result or "portfolio" in result.lower()


class TestCelebrateCompletion:
    """Test completion celebration generation."""

    def test_warm_celebration(self):
        """Warm celebration expresses excitement."""
        bridge = OnboardingNarrativeBridge()
        ctx = OnboardingGrammarContext(
            warmth_level=0.8,
            projects_captured=2,
            project_names=["Piper", "TaskFlow"],
        )

        result = bridge.celebrate_completion(ctx)

        assert "Piper" in result
        assert "TaskFlow" in result
        assert "looking forward" in result.lower() or "wonderful" in result.lower()

    def test_conversational_celebration(self):
        """Conversational celebration is friendly."""
        bridge = OnboardingNarrativeBridge()
        ctx = OnboardingGrammarContext(
            warmth_level=0.5,
            projects_captured=1,
            project_names=["MyApp"],
        )

        result = bridge.celebrate_completion(ctx)

        assert "MyApp" in result
        assert "set" in result.lower() or "added" in result.lower()

    def test_professional_completion(self):
        """Professional completion is efficient."""
        bridge = OnboardingNarrativeBridge()
        ctx = OnboardingGrammarContext(
            warmth_level=0.2,
            projects_captured=1,
            project_names=["API"],
        )

        result = bridge.celebrate_completion(ctx)

        assert "API" in result
        assert "updated" in result.lower() or "help" in result.lower()


class TestHandleDecline:
    """Test decline handling generation."""

    def test_warm_decline_no_projects(self):
        """Warm decline keeps door open."""
        bridge = OnboardingNarrativeBridge()
        ctx = OnboardingGrammarContext(
            warmth_level=0.8,
            projects_captured=0,
        )

        result = bridge.handle_decline(ctx)

        assert "rush" in result.lower() or "here" in result.lower()
        assert "help" in result.lower()

    def test_warm_decline_with_projects(self):
        """Warm decline with projects doesn't save them."""
        bridge = OnboardingNarrativeBridge()
        ctx = OnboardingGrammarContext(
            warmth_level=0.8,
            projects_captured=2,
            project_names=["A", "B"],
        )

        result = bridge.handle_decline(ctx)

        assert "won't save" in result.lower() or "not save" in result.lower()
        assert "help" in result.lower()

    def test_professional_decline(self):
        """Professional decline is brief."""
        bridge = OnboardingNarrativeBridge()
        ctx = OnboardingGrammarContext(
            warmth_level=0.2,
            projects_captured=0,
        )

        result = bridge.handle_decline(ctx)

        assert "anytime" in result.lower() or "assist" in result.lower()


class TestSessionLostMessage:
    """Test session recovery message generation."""

    def test_warm_session_lost(self):
        """Warm session lost is apologetic."""
        bridge = OnboardingNarrativeBridge()
        ctx = OnboardingGrammarContext(warmth_level=0.8)

        result = bridge.get_session_lost_message(ctx)

        assert "sorry" in result.lower()
        assert "start" in result.lower()

    def test_professional_session_lost(self):
        """Professional session lost is direct."""
        bridge = OnboardingNarrativeBridge()
        ctx = OnboardingGrammarContext(warmth_level=0.2)

        result = bridge.get_session_lost_message(ctx)

        assert "restart" in result.lower() or "interrupted" in result.lower()


class TestNeedProjectMessage:
    """Test need-at-least-one-project message generation."""

    def test_warm_need_project(self):
        """Warm nudge for project info."""
        bridge = OnboardingNarrativeBridge()
        ctx = OnboardingGrammarContext(warmth_level=0.8)

        result = bridge.get_need_project_message(ctx)

        assert "project" in result.lower()
        assert "like" in result.lower() or "working" in result.lower()

    def test_professional_need_project(self):
        """Professional request for project info."""
        bridge = OnboardingNarrativeBridge()
        ctx = OnboardingGrammarContext(warmth_level=0.2)

        result = bridge.get_need_project_message(ctx)

        assert "project" in result.lower()


class TestNarrateStage:
    """Test stage narration for logging."""

    def test_narrate_welcome(self):
        """Welcome stage narration."""
        bridge = OnboardingNarrativeBridge()
        ctx = OnboardingGrammarContext(stage=OnboardingStage.WELCOME)

        result = bridge.narrate_stage(ctx)

        assert "first meeting" in result.lower()

    def test_narrate_complete(self):
        """Complete stage narration."""
        bridge = OnboardingNarrativeBridge()
        ctx = OnboardingGrammarContext(stage=OnboardingStage.COMPLETE)

        result = bridge.narrate_stage(ctx)

        assert "relationship established" in result.lower()


class TestAddMorePrompt:
    """Test add more projects prompt."""

    def test_warm_add_more(self):
        """Warm prompt for adding more projects."""
        bridge = OnboardingNarrativeBridge()
        ctx = OnboardingGrammarContext(warmth_level=0.8)

        result = bridge.get_add_more_prompt(ctx)

        assert "project" in result.lower()
        assert "tell" in result.lower() or "sure" in result.lower()


class TestUnclearResponsePrompt:
    """Test unclear response clarification prompt."""

    def test_warm_unclear_prompt(self):
        """Warm clarification when response unclear."""
        bridge = OnboardingNarrativeBridge()
        ctx = OnboardingGrammarContext(
            warmth_level=0.8,
            project_names=["Piper", "TaskFlow"],
        )

        result = bridge.get_unclear_response_prompt(ctx)

        assert "Piper" in result
        assert "TaskFlow" in result
        assert "yes" in result.lower()


class TestContractorTest:
    """Verify phrases pass the Contractor Test."""

    def test_no_raw_data_in_welcome(self):
        """Welcome doesn't expose raw data."""
        bridge = OnboardingNarrativeBridge()
        ctx = OnboardingGrammarContext(warmth_level=0.8)

        result = bridge.get_welcome_message(ctx)

        assert "warmth_level" not in result
        assert "context" not in result.lower()
        assert "formality" not in result

    def test_no_raw_data_in_confirmation(self):
        """Confirmation doesn't expose raw data."""
        bridge = OnboardingNarrativeBridge()
        ctx = OnboardingGrammarContext(
            warmth_level=0.8,
            project_names=["Piper"],
            projects_captured=1,
        )

        result = bridge.get_confirmation_prompt(ctx)

        assert "project_names" not in result
        assert "captured" not in result

    def test_natural_language_celebration(self):
        """Celebration uses natural language."""
        bridge = OnboardingNarrativeBridge()
        ctx = OnboardingGrammarContext(
            warmth_level=0.8,
            project_names=["TaskFlow"],
            projects_captured=1,
        )

        result = bridge.celebrate_completion(ctx)

        # Should read like a human wrote it
        assert result[0].isupper()  # Starts with capital
        assert "!!!" not in result  # No excessive punctuation
        assert len(result) > 20  # Substantive message

    def test_professional_still_appropriate(self):
        """Professional tone is appropriate, not cold."""
        bridge = OnboardingNarrativeBridge()
        ctx = OnboardingGrammarContext(warmth_level=0.2)

        welcome = bridge.get_welcome_message(ctx)
        decline = bridge.handle_decline(ctx)

        # Professional but not rude
        assert "ERROR" not in welcome
        assert "ERROR" not in decline
        assert (
            "please" in welcome.lower() or "help" in welcome.lower() or "assist" in decline.lower()
        )
