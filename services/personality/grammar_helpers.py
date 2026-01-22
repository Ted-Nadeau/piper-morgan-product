"""
Personality Grammar Helpers for Canonical Handlers.

This module provides helper functions to apply grammar-conscious
personality to responses within canonical handlers.

Issue #627: GRAMMAR-TRANSFORM: Personality System
Phase 3: Helper Integration
"""

from typing import Any, Dict, Optional

from services.personality.grammar_bridge import PersonalityGrammarBridge
from services.personality.grammar_context import (
    GrammarLens,
    PersonalityGrammarContext,
    SituationType,
)
from services.personality.personality_profile import PersonalityProfile

# Singleton bridge instance
_grammar_bridge = PersonalityGrammarBridge()


def apply_personality(
    message: str,
    profile: Optional[PersonalityProfile] = None,
    profile_data: Optional[Dict[str, Any]] = None,
    situation: SituationType = SituationType.NORMAL,
    interaction_count: int = 0,
    include_greeting: bool = False,
    include_closing: bool = False,
) -> str:
    """Apply personality to any message.

    This is the main helper for adding personality to responses.

    Args:
        message: Base message to enhance
        profile: PersonalityProfile object (preferred)
        profile_data: Dictionary with profile data (alternative)
        situation: Current situation type
        interaction_count: Previous interaction count
        include_greeting: Whether to add greeting
        include_closing: Whether to add closing

    Returns:
        Personality-enhanced message

    Example:
        Input: "Task completed."
        Output: "That worked out well! Task completed. Anything else?"
    """
    if profile:
        ctx = PersonalityGrammarContext.from_personality_profile(
            profile, situation, interaction_count
        )
    elif profile_data:
        ctx = PersonalityGrammarContext.from_dict(profile_data, situation)
    else:
        ctx = PersonalityGrammarContext.default()

    return _grammar_bridge.apply_personality_to_message(
        message, ctx, include_greeting, include_closing
    )


def get_greeting(
    profile: Optional[PersonalityProfile] = None,
    profile_data: Optional[Dict[str, Any]] = None,
    is_first_interaction: bool = True,
) -> str:
    """Get personality-appropriate greeting.

    Args:
        profile: PersonalityProfile object (preferred)
        profile_data: Dictionary with profile data (alternative)
        is_first_interaction: Whether this is first interaction

    Returns:
        Appropriate greeting string

    Example:
        Warm + first: "Hey there! Nice to meet you!"
        Professional + returning: "Hello again."
    """
    if profile:
        ctx = PersonalityGrammarContext.from_personality_profile(
            profile, interaction_count=0 if is_first_interaction else 1
        )
    elif profile_data:
        profile_data["is_first_interaction"] = is_first_interaction
        ctx = PersonalityGrammarContext.from_dict(profile_data)
    else:
        ctx = PersonalityGrammarContext(is_first_interaction=is_first_interaction)

    return _grammar_bridge.get_greeting(ctx)


def get_error_phrase(
    profile: Optional[PersonalityProfile] = None,
    profile_data: Optional[Dict[str, Any]] = None,
    seems_frustrated: bool = False,
) -> str:
    """Get personality-appropriate error phrase.

    Args:
        profile: PersonalityProfile object (preferred)
        profile_data: Dictionary with profile data (alternative)
        seems_frustrated: Whether user seems frustrated

    Returns:
        Gentle error phrase appropriate for personality

    Example:
        Warm: "I want to help, but something's not quite right."
        Professional: "An error occurred."
    """
    if profile:
        ctx = PersonalityGrammarContext.from_personality_profile(
            profile, situation=SituationType.ERROR
        )
    elif profile_data:
        ctx = PersonalityGrammarContext.from_dict(profile_data, situation=SituationType.ERROR)
    else:
        ctx = PersonalityGrammarContext(situation=SituationType.ERROR)

    ctx.seems_frustrated = seems_frustrated

    return _grammar_bridge.get_error_phrase(ctx)


def get_closing(
    profile: Optional[PersonalityProfile] = None,
    profile_data: Optional[Dict[str, Any]] = None,
    is_busy: bool = False,
) -> str:
    """Get personality-appropriate closing phrase.

    Args:
        profile: PersonalityProfile object (preferred)
        profile_data: Dictionary with profile data (alternative)
        is_busy: Whether user seems busy (skip closing if so)

    Returns:
        Closing phrase or empty string if not appropriate

    Example:
        Warm: "Anything else I can help with?"
        Busy: ""
    """
    if profile:
        ctx = PersonalityGrammarContext.from_personality_profile(profile)
    elif profile_data:
        ctx = PersonalityGrammarContext.from_dict(profile_data)
    else:
        ctx = PersonalityGrammarContext()

    ctx.seems_busy = is_busy

    return _grammar_bridge.get_closing(ctx)


def get_confidence_phrase(
    confidence: float,
    profile: Optional[PersonalityProfile] = None,
    profile_data: Optional[Dict[str, Any]] = None,
) -> str:
    """Get personality-appropriate confidence expression.

    Args:
        confidence: Confidence level (0.0-1.0)
        profile: PersonalityProfile object (preferred)
        profile_data: Dictionary with profile data (alternative)

    Returns:
        Confidence phrase appropriate for level and preference

    Example:
        High confidence + warm: "I'm pretty confident about this."
        Hidden confidence: ""
    """
    if profile:
        ctx = PersonalityGrammarContext.from_personality_profile(profile)
    elif profile_data:
        ctx = PersonalityGrammarContext.from_dict(profile_data)
    else:
        ctx = PersonalityGrammarContext()

    return _grammar_bridge.get_confidence_phrase(ctx, confidence)


def get_situation_tone(
    situation: SituationType,
    profile: Optional[PersonalityProfile] = None,
    profile_data: Optional[Dict[str, Any]] = None,
) -> str:
    """Get the tone phrase for a situation.

    Args:
        situation: Current situation type
        profile: PersonalityProfile object (preferred)
        profile_data: Dictionary with profile data (alternative)

    Returns:
        Situation-appropriate tone phrase

    Example:
        SUCCESS + warm: "That worked out well!"
        ERROR + professional: "An error occurred."
    """
    if profile:
        ctx = PersonalityGrammarContext.from_personality_profile(profile, situation=situation)
    elif profile_data:
        ctx = PersonalityGrammarContext.from_dict(profile_data, situation=situation)
    else:
        ctx = PersonalityGrammarContext(situation=situation)

    return _grammar_bridge.get_situation_phrase(ctx)


def get_formality(
    profile: Optional[PersonalityProfile] = None,
    profile_data: Optional[Dict[str, Any]] = None,
    situation: SituationType = SituationType.NORMAL,
) -> str:
    """Get appropriate formality level for context.

    Args:
        profile: PersonalityProfile object (preferred)
        profile_data: Dictionary with profile data (alternative)
        situation: Current situation type

    Returns:
        "warm", "conversational", "professional", or "terse"
    """
    if profile:
        ctx = PersonalityGrammarContext.from_personality_profile(profile, situation=situation)
    elif profile_data:
        ctx = PersonalityGrammarContext.from_dict(profile_data, situation=situation)
    else:
        ctx = PersonalityGrammarContext(situation=situation)

    return ctx.get_formality()


def is_warm_user(
    profile: Optional[PersonalityProfile] = None,
    profile_data: Optional[Dict[str, Any]] = None,
) -> bool:
    """Check if user prefers warm tone.

    Args:
        profile: PersonalityProfile object (preferred)
        profile_data: Dictionary with profile data (alternative)

    Returns:
        True if user prefers warm interactions
    """
    if profile:
        ctx = PersonalityGrammarContext.from_personality_profile(profile)
    elif profile_data:
        ctx = PersonalityGrammarContext.from_dict(profile_data)
    else:
        return False

    return ctx.is_warm()
