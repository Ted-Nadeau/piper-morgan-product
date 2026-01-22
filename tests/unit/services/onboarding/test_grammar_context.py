"""
Tests for Onboarding Grammar Context.

Issue #626: GRAMMAR-TRANSFORM: Onboarding System
Phase 1: Context Dataclass Tests
"""

import pytest

from services.onboarding.grammar_context import OnboardingGrammarContext, OnboardingStage


class TestOnboardingStage:
    """Test OnboardingStage enum."""

    def test_all_stages_defined(self):
        """All expected stages exist."""
        assert OnboardingStage.WELCOME == "welcome"
        assert OnboardingStage.GATHERING == "gathering"
        assert OnboardingStage.CONFIRMING == "confirming"
        assert OnboardingStage.COMPLETE == "complete"
        assert OnboardingStage.DECLINED == "declined"

    def test_stage_count(self):
        """Correct number of stages."""
        assert len(OnboardingStage) == 5


class TestContextCreation:
    """Test context creation methods."""

    def test_default_context(self):
        """Default context is warm and welcoming."""
        ctx = OnboardingGrammarContext.default()

        assert ctx.stage == OnboardingStage.WELCOME
        assert ctx.is_first_meeting is True
        assert ctx.warmth_level == 0.8
        assert ctx.context_available is True

    def test_from_session_initiated(self):
        """Create context from initiated session."""
        ctx = OnboardingGrammarContext.from_session(
            state="initiated",
            captured_projects=[],
        )

        assert ctx.stage == OnboardingStage.WELCOME
        assert ctx.projects_captured == 0
        assert ctx.is_first_meeting is True

    def test_from_session_gathering(self):
        """Create context from gathering session."""
        ctx = OnboardingGrammarContext.from_session(
            state="gathering_projects",
            captured_projects=[
                {"name": "Piper"},
                {"name": "TaskFlow"},
            ],
        )

        assert ctx.stage == OnboardingStage.GATHERING
        assert ctx.projects_captured == 2
        assert ctx.project_names == ["Piper", "TaskFlow"]

    def test_from_session_confirming(self):
        """Create context from confirming session."""
        ctx = OnboardingGrammarContext.from_session(
            state="confirming",
            captured_projects=[{"name": "MyApp"}],
        )

        assert ctx.stage == OnboardingStage.CONFIRMING
        assert ctx.projects_captured == 1

    def test_from_session_complete(self):
        """Create context from complete session."""
        ctx = OnboardingGrammarContext.from_session(
            state="complete",
            captured_projects=[{"name": "Done"}],
        )

        assert ctx.stage == OnboardingStage.COMPLETE
        assert ctx.is_complete()

    def test_from_session_declined(self):
        """Create context from declined session."""
        ctx = OnboardingGrammarContext.from_session(state="declined")

        assert ctx.stage == OnboardingStage.DECLINED
        assert ctx.was_declined()

    def test_from_dict(self):
        """Create context from dictionary."""
        data = {
            "stage": "gathering",
            "projects_captured": 3,
            "project_names": ["A", "B", "C"],
            "user_seems_eager": True,
            "warmth_level": 0.9,
        }
        ctx = OnboardingGrammarContext.from_dict(data)

        assert ctx.stage == OnboardingStage.GATHERING
        assert ctx.projects_captured == 3
        assert ctx.user_seems_eager is True
        assert ctx.warmth_level == 0.9

    def test_from_dict_with_stage_enum(self):
        """Create context from dict with stage as enum."""
        data = {
            "stage": OnboardingStage.CONFIRMING,
            "warmth_level": 0.7,
        }
        ctx = OnboardingGrammarContext.from_dict(data)

        assert ctx.stage == OnboardingStage.CONFIRMING


class TestWarmthDetection:
    """Test warmth and formality detection."""

    def test_is_warm_high_warmth(self):
        """High warmth level detected as warm."""
        ctx = OnboardingGrammarContext(warmth_level=0.8)
        assert ctx.is_warm() is True

    def test_is_warm_medium_warmth(self):
        """Medium warmth level detected as warm."""
        ctx = OnboardingGrammarContext(warmth_level=0.6)
        assert ctx.is_warm() is True

    def test_is_warm_low_warmth(self):
        """Low warmth level not detected as warm."""
        ctx = OnboardingGrammarContext(warmth_level=0.3)
        assert ctx.is_warm() is False

    def test_is_professional(self):
        """Low warmth detected as professional."""
        ctx = OnboardingGrammarContext(warmth_level=0.2)
        assert ctx.is_professional() is True

    def test_not_professional_medium_warmth(self):
        """Medium warmth not professional."""
        ctx = OnboardingGrammarContext(warmth_level=0.5)
        assert ctx.is_professional() is False


class TestFormalityDetection:
    """Test formality level derivation."""

    def test_formality_warm(self):
        """High warmth gives warm formality."""
        ctx = OnboardingGrammarContext(warmth_level=0.8)
        assert ctx.get_formality() == "warm"

    def test_formality_conversational(self):
        """Medium warmth gives conversational formality."""
        ctx = OnboardingGrammarContext(warmth_level=0.5)
        assert ctx.get_formality() == "conversational"

    def test_formality_professional(self):
        """Low warmth gives professional formality."""
        ctx = OnboardingGrammarContext(warmth_level=0.2)
        assert ctx.get_formality() == "professional"

    def test_formality_extra_warmth_for_hesitant(self):
        """Hesitant user gets warm formality."""
        ctx = OnboardingGrammarContext(
            warmth_level=0.5,
            user_seems_hesitant=True,
        )
        assert ctx.get_formality() == "warm"

    def test_formality_extra_warmth_for_decline(self):
        """Decline stage gets warm formality."""
        ctx = OnboardingGrammarContext(
            warmth_level=0.5,
            stage=OnboardingStage.DECLINED,
        )
        assert ctx.get_formality() == "warm"


class TestProjectTracking:
    """Test project tracking methods."""

    def test_has_projects_none(self):
        """No projects detected correctly."""
        ctx = OnboardingGrammarContext(projects_captured=0)
        assert ctx.has_projects() is False

    def test_has_projects_some(self):
        """Some projects detected correctly."""
        ctx = OnboardingGrammarContext(projects_captured=2)
        assert ctx.has_projects() is True

    def test_is_single_project(self):
        """Single project detected correctly."""
        ctx = OnboardingGrammarContext(projects_captured=1)
        assert ctx.is_single_project() is True
        assert ctx.is_multiple_projects() is False

    def test_is_multiple_projects(self):
        """Multiple projects detected correctly."""
        ctx = OnboardingGrammarContext(projects_captured=3)
        assert ctx.is_multiple_projects() is True
        assert ctx.is_single_project() is False


class TestProjectSummary:
    """Test project summary generation."""

    def test_summary_empty(self):
        """Empty when no projects."""
        ctx = OnboardingGrammarContext(project_names=[])
        assert ctx.get_project_summary() == ""

    def test_summary_single(self):
        """Single project name returned."""
        ctx = OnboardingGrammarContext(project_names=["Piper"])
        assert ctx.get_project_summary() == "Piper"

    def test_summary_two(self):
        """Two projects joined with 'and'."""
        ctx = OnboardingGrammarContext(project_names=["Piper", "TaskFlow"])
        assert ctx.get_project_summary() == "Piper and TaskFlow"

    def test_summary_three(self):
        """Three+ projects use Oxford comma."""
        ctx = OnboardingGrammarContext(project_names=["Piper", "TaskFlow", "DocGen"])
        assert ctx.get_project_summary() == "Piper, TaskFlow, and DocGen"

    def test_summary_four(self):
        """Four projects formatted correctly."""
        ctx = OnboardingGrammarContext(project_names=["A", "B", "C", "D"])
        assert ctx.get_project_summary() == "A, B, C, and D"


class TestStageChecks:
    """Test stage checking methods."""

    def test_is_at_stage(self):
        """is_at_stage works correctly."""
        ctx = OnboardingGrammarContext(stage=OnboardingStage.GATHERING)
        assert ctx.is_at_stage(OnboardingStage.GATHERING) is True
        assert ctx.is_at_stage(OnboardingStage.WELCOME) is False

    def test_is_complete(self):
        """is_complete works correctly."""
        ctx = OnboardingGrammarContext(stage=OnboardingStage.COMPLETE)
        assert ctx.is_complete() is True

        ctx2 = OnboardingGrammarContext(stage=OnboardingStage.GATHERING)
        assert ctx2.is_complete() is False

    def test_was_declined(self):
        """was_declined works correctly."""
        ctx = OnboardingGrammarContext(stage=OnboardingStage.DECLINED)
        assert ctx.was_declined() is True

    def test_is_gathering(self):
        """is_gathering works correctly."""
        ctx = OnboardingGrammarContext(stage=OnboardingStage.GATHERING)
        assert ctx.is_gathering() is True

    def test_is_confirming(self):
        """is_confirming works correctly."""
        ctx = OnboardingGrammarContext(stage=OnboardingStage.CONFIRMING)
        assert ctx.is_confirming() is True


class TestExtraWarmth:
    """Test extra warmth detection."""

    def test_needs_extra_warmth_hesitant(self):
        """Hesitant user needs extra warmth."""
        ctx = OnboardingGrammarContext(user_seems_hesitant=True)
        assert ctx.needs_extra_warmth() is True

    def test_needs_extra_warmth_declined(self):
        """Declined stage needs extra warmth."""
        ctx = OnboardingGrammarContext(stage=OnboardingStage.DECLINED)
        assert ctx.needs_extra_warmth() is True

    def test_no_extra_warmth_normal(self):
        """Normal context doesn't need extra warmth."""
        ctx = OnboardingGrammarContext(
            stage=OnboardingStage.GATHERING,
            user_seems_hesitant=False,
        )
        assert ctx.needs_extra_warmth() is False


class TestContractorTest:
    """Verify context doesn't expose raw data terms."""

    def test_no_raw_data_in_summary(self):
        """Project summary uses natural language."""
        ctx = OnboardingGrammarContext(
            project_names=["MyApp", "Backend"],
        )
        summary = ctx.get_project_summary()

        assert "project_names" not in summary
        assert "captured" not in summary
        assert "MyApp and Backend" == summary

    def test_formality_returns_readable_string(self):
        """Formality returns human-readable string."""
        ctx = OnboardingGrammarContext(warmth_level=0.8)
        formality = ctx.get_formality()

        assert formality in ["warm", "conversational", "professional"]
        assert "warmth_level" not in formality
