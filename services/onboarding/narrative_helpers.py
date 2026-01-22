"""
Onboarding Narrative Helpers for Handlers.

This module provides simple helper functions for onboarding handlers
to generate warm, relationship-building responses.

Issue #626: GRAMMAR-TRANSFORM: Onboarding System
Phase 3: Helper Integration
"""

from typing import Any, Dict, List, Optional

from services.onboarding.grammar_context import OnboardingGrammarContext, OnboardingStage
from services.onboarding.narrative_bridge import OnboardingNarrativeBridge

# Singleton bridge instance
_narrative_bridge = OnboardingNarrativeBridge()


def get_welcome_message(
    warmth_level: float = 0.8,
    include_atmosphere: bool = True,
) -> str:
    """Get warm welcome message for first meeting.

    Args:
        warmth_level: User's warmth preference (default warm for onboarding)
        include_atmosphere: Whether to include workspace atmosphere

    Returns:
        Welcome message for first meeting

    Example:
        "Hi there! I'm Piper, and I'm really glad to meet you..."
    """
    ctx = OnboardingGrammarContext(
        stage=OnboardingStage.WELCOME,
        warmth_level=warmth_level,
    )

    return _narrative_bridge.get_welcome_message(ctx)


def acknowledge_project(
    project_name: str,
    is_first_project: bool = True,
    warmth_level: float = 0.8,
) -> str:
    """Acknowledge project with genuine interest.

    Args:
        project_name: Name of the project
        is_first_project: Whether this is the first project captured
        warmth_level: User's warmth preference

    Returns:
        Acknowledgment with project name

    Example:
        "TaskFlow - that sounds like a great project! I'd love to help..."
    """
    ctx = OnboardingGrammarContext(
        stage=OnboardingStage.GATHERING,
        projects_captured=1 if is_first_project else 2,
        warmth_level=warmth_level,
    )

    return _narrative_bridge.acknowledge_project(ctx, project_name)


def get_more_projects_prompt(warmth_level: float = 0.8) -> str:
    """Get prompt asking about additional projects.

    Args:
        warmth_level: User's warmth preference

    Returns:
        Prompt for more projects

    Example:
        "Are there any other projects you'd like me to know about?"
    """
    ctx = OnboardingGrammarContext(
        stage=OnboardingStage.GATHERING,
        warmth_level=warmth_level,
    )

    return _narrative_bridge.get_more_projects_prompt(ctx)


def get_confirmation_prompt(
    project_names: List[str],
    warmth_level: float = 0.8,
) -> str:
    """Get confirmation prompt for captured projects.

    Args:
        project_names: List of project names to confirm
        warmth_level: User's warmth preference

    Returns:
        Confirmation prompt mentioning projects

    Example:
        "Should I add Piper and TaskFlow to your portfolio?"
    """
    ctx = OnboardingGrammarContext(
        stage=OnboardingStage.CONFIRMING,
        projects_captured=len(project_names),
        project_names=project_names,
        warmth_level=warmth_level,
    )

    return _narrative_bridge.get_confirmation_prompt(ctx)


def celebrate_completion(
    project_names: List[str],
    warmth_level: float = 0.8,
) -> str:
    """Celebrate successful onboarding - relationship established!

    Args:
        project_names: List of project names added
        warmth_level: User's warmth preference

    Returns:
        Celebration message

    Example:
        "Wonderful! I've added Piper to your portfolio. I'm really looking
        forward to working together..."
    """
    ctx = OnboardingGrammarContext(
        stage=OnboardingStage.COMPLETE,
        projects_captured=len(project_names),
        project_names=project_names,
        warmth_level=warmth_level,
    )

    return _narrative_bridge.celebrate_completion(ctx)


def handle_decline_warmly(
    had_projects: bool = False,
    warmth_level: float = 0.8,
) -> str:
    """Handle decline with warmth and keep door open.

    Args:
        had_projects: Whether projects were captured before decline
        warmth_level: User's warmth preference

    Returns:
        Warm decline message

    Example:
        "No rush at all - I'll be here whenever you're ready!"
    """
    ctx = OnboardingGrammarContext(
        stage=OnboardingStage.DECLINED,
        projects_captured=2 if had_projects else 0,
        project_names=["placeholder"] if had_projects else [],
        warmth_level=warmth_level,
    )

    return _narrative_bridge.handle_decline(ctx)


def get_session_lost_message(warmth_level: float = 0.8) -> str:
    """Get warm message for session recovery.

    Args:
        warmth_level: User's warmth preference

    Returns:
        Session lost recovery message

    Example:
        "I'm sorry, I seem to have lost track of where we were..."
    """
    ctx = OnboardingGrammarContext(warmth_level=warmth_level)

    return _narrative_bridge.get_session_lost_message(ctx)


def get_need_project_message(warmth_level: float = 0.8) -> str:
    """Get message asking for at least one project.

    Args:
        warmth_level: User's warmth preference

    Returns:
        Nudge for project info

    Example:
        "I'd really like to help you with at least one project..."
    """
    ctx = OnboardingGrammarContext(
        stage=OnboardingStage.GATHERING,
        warmth_level=warmth_level,
    )

    return _narrative_bridge.get_need_project_message(ctx)


def get_add_more_prompt(warmth_level: float = 0.8) -> str:
    """Get prompt when user wants to add more projects.

    Args:
        warmth_level: User's warmth preference

    Returns:
        Prompt for additional project

    Example:
        "Sure! What other project would you like to tell me about?"
    """
    ctx = OnboardingGrammarContext(
        stage=OnboardingStage.GATHERING,
        warmth_level=warmth_level,
    )

    return _narrative_bridge.get_add_more_prompt(ctx)


def get_unclear_response_prompt(
    project_names: List[str],
    warmth_level: float = 0.8,
) -> str:
    """Get prompt when user response is unclear during confirmation.

    Args:
        project_names: List of project names captured
        warmth_level: User's warmth preference

    Returns:
        Clarification prompt

    Example:
        "I have Piper noted. Should I save this to your portfolio?"
    """
    ctx = OnboardingGrammarContext(
        stage=OnboardingStage.CONFIRMING,
        projects_captured=len(project_names),
        project_names=project_names,
        warmth_level=warmth_level,
    )

    return _narrative_bridge.get_unclear_response_prompt(ctx)


def get_onboarding_formality(warmth_level: float = 0.8) -> str:
    """Get appropriate formality level for onboarding.

    Args:
        warmth_level: User's warmth preference

    Returns:
        "warm", "conversational", or "professional"
    """
    ctx = OnboardingGrammarContext(warmth_level=warmth_level)
    return ctx.get_formality()


def is_warm_onboarding(warmth_level: float = 0.8) -> bool:
    """Check if onboarding should use warm tone.

    Args:
        warmth_level: User's warmth preference

    Returns:
        True if warm tone appropriate
    """
    ctx = OnboardingGrammarContext(warmth_level=warmth_level)
    return ctx.is_warm()


# Convenience function for creating context from session
def create_onboarding_context(
    state: str,
    captured_projects: Optional[List[Dict[str, Any]]] = None,
    warmth_level: float = 0.8,
    user_seems_hesitant: bool = False,
) -> OnboardingGrammarContext:
    """Create grammar context from session state.

    Args:
        state: Session state string
        captured_projects: List of project dicts
        warmth_level: User's warmth preference
        user_seems_hesitant: Whether user seems hesitant

    Returns:
        OnboardingGrammarContext for generating messages
    """
    ctx = OnboardingGrammarContext.from_session(
        state=state,
        captured_projects=captured_projects,
        warmth_level=warmth_level,
    )
    ctx.user_seems_hesitant = user_seems_hesitant
    return ctx
