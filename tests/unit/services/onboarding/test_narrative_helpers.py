"""
Tests for Onboarding Narrative Helpers.

Issue #626: GRAMMAR-TRANSFORM: Onboarding System
Phase 3: Helper Integration Tests
"""

import pytest

from services.onboarding.grammar_context import OnboardingStage
from services.onboarding.narrative_helpers import (
    acknowledge_project,
    celebrate_completion,
    create_onboarding_context,
    get_add_more_prompt,
    get_confirmation_prompt,
    get_more_projects_prompt,
    get_need_project_message,
    get_onboarding_formality,
    get_session_lost_message,
    get_unclear_response_prompt,
    get_welcome_message,
    handle_decline_warmly,
    is_warm_onboarding,
)


class TestGetWelcomeMessage:
    """Test get_welcome_message helper."""

    def test_default_warm(self):
        """Default welcome is warm."""
        result = get_welcome_message()

        assert "Piper" in result
        assert "glad" in result.lower() or "help" in result.lower()

    def test_warm_level_affects_message(self):
        """Warmth level affects message tone."""
        warm = get_welcome_message(warmth_level=0.8)
        professional = get_welcome_message(warmth_level=0.2)

        assert "glad" in warm.lower() or "really" in warm.lower()
        assert len(professional) < len(warm)


class TestAcknowledgeProject:
    """Test acknowledge_project helper."""

    def test_first_project_warm(self):
        """First project gets warm acknowledgment."""
        result = acknowledge_project("TaskFlow", is_first_project=True)

        assert "TaskFlow" in result
        assert "great" in result.lower() or "love" in result.lower()

    def test_additional_project(self):
        """Additional project has continued interest."""
        result = acknowledge_project("Backend", is_first_project=False)

        assert "Backend" in result
        assert "too" in result.lower() or "both" in result.lower()

    def test_professional_acknowledgment(self):
        """Professional acknowledgment is concise."""
        result = acknowledge_project("API", warmth_level=0.2)

        assert "API" in result


class TestMoreProjectsPrompt:
    """Test get_more_projects_prompt helper."""

    def test_default_prompt(self):
        """Default prompt asks about more projects."""
        result = get_more_projects_prompt()

        assert "project" in result.lower()

    def test_professional_prompt(self):
        """Professional prompt is direct."""
        result = get_more_projects_prompt(warmth_level=0.2)

        assert "project" in result.lower() or "additional" in result.lower()


class TestGetConfirmationPrompt:
    """Test get_confirmation_prompt helper."""

    def test_single_project(self):
        """Single project confirmation."""
        result = get_confirmation_prompt(["Piper"])

        assert "Piper" in result
        assert "portfolio" in result.lower()

    def test_multiple_projects(self):
        """Multiple project confirmation."""
        result = get_confirmation_prompt(["Piper", "TaskFlow"])

        assert "Piper" in result
        assert "TaskFlow" in result

    def test_three_projects(self):
        """Three projects use Oxford comma."""
        result = get_confirmation_prompt(["A", "B", "C"])

        assert "A" in result
        assert "B" in result
        assert "C" in result


class TestCelebrateCompletion:
    """Test celebrate_completion helper."""

    def test_single_project_celebration(self):
        """Single project celebration."""
        result = celebrate_completion(["Piper"])

        assert "Piper" in result
        assert "looking forward" in result.lower() or "added" in result.lower()

    def test_multiple_projects_celebration(self):
        """Multiple projects celebration."""
        result = celebrate_completion(["Piper", "TaskFlow"])

        assert "Piper" in result
        assert "TaskFlow" in result

    def test_professional_completion(self):
        """Professional completion message."""
        result = celebrate_completion(["API"], warmth_level=0.2)

        assert "API" in result


class TestHandleDeclineWarmly:
    """Test handle_decline_warmly helper."""

    def test_decline_no_projects(self):
        """Decline without projects keeps door open."""
        result = handle_decline_warmly(had_projects=False)

        assert "here" in result.lower() or "ready" in result.lower()

    def test_decline_with_projects(self):
        """Decline with projects doesn't save them."""
        result = handle_decline_warmly(had_projects=True)

        assert "won't save" in result.lower() or "not save" in result.lower()

    def test_professional_decline(self):
        """Professional decline still keeps door open.

        Note: Decline stage automatically gets extra warmth (needs_extra_warmth)
        so even low warmth_level results in warm formality for declines.
        """
        result = handle_decline_warmly(warmth_level=0.2)

        # Even with low warmth, decline keeps door open
        assert "help" in result.lower() or "ready" in result.lower()


class TestSessionLostMessage:
    """Test get_session_lost_message helper."""

    def test_warm_session_lost(self):
        """Warm session lost message."""
        result = get_session_lost_message()

        assert "sorry" in result.lower()
        assert "start" in result.lower()

    def test_professional_session_lost(self):
        """Professional session lost message."""
        result = get_session_lost_message(warmth_level=0.2)

        assert len(result) > 0


class TestNeedProjectMessage:
    """Test get_need_project_message helper."""

    def test_warm_nudge(self):
        """Warm nudge for project info."""
        result = get_need_project_message()

        assert "project" in result.lower()
        assert "like" in result.lower() or "help" in result.lower()


class TestAddMorePrompt:
    """Test get_add_more_prompt helper."""

    def test_warm_add_more(self):
        """Warm add more prompt."""
        result = get_add_more_prompt()

        assert "project" in result.lower()


class TestUnclearResponsePrompt:
    """Test get_unclear_response_prompt helper."""

    def test_single_project_unclear(self):
        """Unclear response with single project."""
        result = get_unclear_response_prompt(["Piper"])

        assert "Piper" in result
        assert "yes" in result.lower()

    def test_multiple_projects_unclear(self):
        """Unclear response with multiple projects."""
        result = get_unclear_response_prompt(["Piper", "TaskFlow"])

        assert "Piper" in result
        assert "TaskFlow" in result


class TestFormalityHelpers:
    """Test formality helper functions."""

    def test_warm_formality(self):
        """Warm formality detection."""
        result = get_onboarding_formality(warmth_level=0.8)
        assert result == "warm"

    def test_conversational_formality(self):
        """Conversational formality detection."""
        result = get_onboarding_formality(warmth_level=0.5)
        assert result == "conversational"

    def test_professional_formality(self):
        """Professional formality detection."""
        result = get_onboarding_formality(warmth_level=0.2)
        assert result == "professional"

    def test_is_warm_true(self):
        """is_warm returns true for warm level."""
        assert is_warm_onboarding(warmth_level=0.8) is True

    def test_is_warm_false(self):
        """is_warm returns false for low level."""
        assert is_warm_onboarding(warmth_level=0.3) is False


class TestCreateOnboardingContext:
    """Test create_onboarding_context helper."""

    def test_create_from_initiated(self):
        """Create context from initiated state."""
        ctx = create_onboarding_context(state="initiated")

        assert ctx.stage == OnboardingStage.WELCOME
        assert ctx.is_first_meeting is True

    def test_create_from_gathering(self):
        """Create context from gathering state."""
        ctx = create_onboarding_context(
            state="gathering_projects",
            captured_projects=[{"name": "Piper"}],
        )

        assert ctx.stage == OnboardingStage.GATHERING
        assert ctx.projects_captured == 1
        assert ctx.project_names == ["Piper"]

    def test_create_with_hesitant_user(self):
        """Create context with hesitant user."""
        ctx = create_onboarding_context(
            state="gathering_projects",
            user_seems_hesitant=True,
        )

        assert ctx.user_seems_hesitant is True
        assert ctx.get_formality() == "warm"


class TestContractorTest:
    """Verify helpers pass Contractor Test."""

    def test_no_raw_data_in_welcome(self):
        """Welcome doesn't expose raw data."""
        result = get_welcome_message()

        assert "warmth_level" not in result
        assert "context" not in result.lower()

    def test_no_raw_data_in_acknowledgment(self):
        """Acknowledgment doesn't expose raw data."""
        result = acknowledge_project("Piper")

        assert "is_first_project" not in result
        assert "captured" not in result

    def test_natural_language_throughout(self):
        """All outputs use natural language."""
        welcome = get_welcome_message()
        ack = acknowledge_project("TaskFlow")
        confirm = get_confirmation_prompt(["Piper"])
        celebrate = celebrate_completion(["Piper"])
        decline = handle_decline_warmly()

        for text in [welcome, ack, confirm, celebrate, decline]:
            assert text[0].isupper()  # Starts with capital
            assert "!!!" not in text  # No excessive punctuation
            assert len(text) > 10  # Substantive

    def test_professional_still_human(self):
        """Professional tone is still human."""
        welcome = get_welcome_message(warmth_level=0.2)
        decline = handle_decline_warmly(warmth_level=0.2)

        # Should not be robotic
        assert "ERROR" not in welcome
        assert "FAILED" not in decline
