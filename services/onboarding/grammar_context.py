"""
Onboarding Grammar Context for conscious response generation.

This module provides rich context for grammar-conscious onboarding responses,
treating onboarding as Piper and user's FIRST MEETING - a significant moment
for relationship establishment.

Issue #626: GRAMMAR-TRANSFORM: Onboarding System
Phase 1: Context Dataclass
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class OnboardingStage(str, Enum):
    """Stages of the onboarding conversation.

    Each stage represents a distinct moment in the relationship establishment.
    """

    WELCOME = "welcome"  # Initial greeting - first meeting!
    GATHERING = "gathering"  # Learning about user's projects
    CONFIRMING = "confirming"  # Confirming what we've learned
    COMPLETE = "complete"  # Successfully onboarded - relationship established
    DECLINED = "declined"  # User declined - door stays open


@dataclass
class OnboardingGrammarContext:
    """Rich context for grammar-conscious onboarding responses.

    Captures the state of the onboarding conversation with awareness that
    this is Piper and user's FIRST MEETING - a significant relationship moment.

    In MUX grammar:
    - Entity: User being welcomed, Piper introducing herself
    - Moment: First meeting, relationship establishment
    - Place: User's new workspace
    """

    # Stage tracking
    stage: OnboardingStage = OnboardingStage.WELCOME

    # Relationship context - onboarding IS first meeting
    is_first_meeting: bool = True

    # Progress context
    projects_captured: int = 0
    project_names: List[str] = field(default_factory=list)

    # User signals (detected from conversation)
    user_seems_hesitant: bool = False
    user_seems_eager: bool = False

    # Personality calibration
    # Default WARM for first meeting - this is relationship establishment
    warmth_level: float = 0.8

    # Context availability
    context_available: bool = True

    @classmethod
    def from_session(
        cls,
        state: str,
        captured_projects: Optional[List[Dict[str, Any]]] = None,
        warmth_level: float = 0.8,
    ) -> "OnboardingGrammarContext":
        """Create context from onboarding session state.

        Args:
            state: Session state string (matches PortfolioOnboardingState)
            captured_projects: List of project dicts from session
            warmth_level: User's warmth preference (default warm for onboarding)

        Returns:
            OnboardingGrammarContext for current session state
        """
        # Map session state to stage
        state_to_stage = {
            "initiated": OnboardingStage.WELCOME,
            "gathering_projects": OnboardingStage.GATHERING,
            "confirming": OnboardingStage.CONFIRMING,
            "complete": OnboardingStage.COMPLETE,
            "declined": OnboardingStage.DECLINED,
        }

        stage = state_to_stage.get(state.lower(), OnboardingStage.WELCOME)

        # Extract project info
        projects = captured_projects or []
        project_names = [p.get("name", "unnamed") for p in projects]

        return cls(
            stage=stage,
            is_first_meeting=True,  # Onboarding IS first meeting
            projects_captured=len(projects),
            project_names=project_names,
            warmth_level=warmth_level,
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OnboardingGrammarContext":
        """Create context from dictionary.

        Args:
            data: Dictionary with context fields

        Returns:
            OnboardingGrammarContext instance
        """
        stage_str = data.get("stage", "welcome")
        if isinstance(stage_str, OnboardingStage):
            stage = stage_str
        else:
            stage = OnboardingStage(stage_str)

        return cls(
            stage=stage,
            is_first_meeting=data.get("is_first_meeting", True),
            projects_captured=data.get("projects_captured", 0),
            project_names=data.get("project_names", []),
            user_seems_hesitant=data.get("user_seems_hesitant", False),
            user_seems_eager=data.get("user_seems_eager", False),
            warmth_level=data.get("warmth_level", 0.8),
            context_available=data.get("context_available", True),
        )

    @classmethod
    def default(cls) -> "OnboardingGrammarContext":
        """Create default context for onboarding.

        Returns warm, welcoming defaults appropriate for first meeting.
        """
        return cls(
            stage=OnboardingStage.WELCOME,
            is_first_meeting=True,
            warmth_level=0.8,  # Warm for first meeting
        )

    def is_warm(self) -> bool:
        """Check if context calls for warm tone.

        Onboarding defaults to warm - this is relationship establishment.
        """
        return self.warmth_level >= 0.6

    def is_professional(self) -> bool:
        """Check if context calls for professional tone.

        Even professional onboarding should be welcoming.
        """
        return self.warmth_level < 0.4

    def has_projects(self) -> bool:
        """Check if any projects have been captured."""
        return self.projects_captured > 0

    def is_single_project(self) -> bool:
        """Check if exactly one project captured."""
        return self.projects_captured == 1

    def is_multiple_projects(self) -> bool:
        """Check if multiple projects captured."""
        return self.projects_captured > 1

    def needs_extra_warmth(self) -> bool:
        """Check if situation calls for extra warmth.

        Extra warmth when:
        - User seems hesitant
        - This is a decline (keep door open)
        - Error recovery
        """
        return self.user_seems_hesitant or self.stage == OnboardingStage.DECLINED

    def get_formality(self) -> str:
        """Get appropriate formality level.

        Onboarding skews warm - we want to establish relationship.

        Returns:
            "warm", "conversational", or "professional"
        """
        if self.needs_extra_warmth():
            return "warm"

        if self.warmth_level >= 0.7:
            return "warm"
        elif self.warmth_level >= 0.4:
            return "conversational"
        else:
            return "professional"

    def get_project_summary(self) -> str:
        """Get human-readable project summary.

        Examples:
            "Piper" (single)
            "Piper and TaskFlow" (two)
            "Piper, TaskFlow, and DocGen" (three+)
        """
        if not self.project_names:
            return ""

        if len(self.project_names) == 1:
            return self.project_names[0]
        elif len(self.project_names) == 2:
            return f"{self.project_names[0]} and {self.project_names[1]}"
        else:
            all_but_last = ", ".join(self.project_names[:-1])
            return f"{all_but_last}, and {self.project_names[-1]}"

    def is_at_stage(self, stage: OnboardingStage) -> bool:
        """Check if at a specific stage."""
        return self.stage == stage

    def is_complete(self) -> bool:
        """Check if onboarding completed successfully."""
        return self.stage == OnboardingStage.COMPLETE

    def was_declined(self) -> bool:
        """Check if user declined onboarding."""
        return self.stage == OnboardingStage.DECLINED

    def is_gathering(self) -> bool:
        """Check if in project gathering stage."""
        return self.stage == OnboardingStage.GATHERING

    def is_confirming(self) -> bool:
        """Check if in confirmation stage."""
        return self.stage == OnboardingStage.CONFIRMING
