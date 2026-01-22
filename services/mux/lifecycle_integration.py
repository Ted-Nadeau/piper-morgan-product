"""
Lifecycle Integration Helpers for Intent Handlers.

This module provides helper functions for integrating lifecycle-aware
language into intent handler responses. Handlers can use these helpers
to describe objects with lifecycle-appropriate phrases.

Example:
    from services.mux.lifecycle_integration import describe_with_lifecycle

    # In a handler:
    description = describe_with_lifecycle(
        feature, "the authentication feature"
    )
    # Returns: "I just noticed the authentication feature..." if EMERGENT
    # Returns: "the authentication feature" if no lifecycle state
"""

from typing import Any, Optional

from services.mux.lifecycle import LifecycleState, transition_explanation


def describe_with_lifecycle(
    obj: Any,
    base_description: str,
    include_phrase_prefix: bool = True,
) -> str:
    """
    Generate a lifecycle-aware description of an object.

    If the object has a lifecycle_state, prefixes the description with
    the appropriate experience phrase. Otherwise returns the base description.

    Args:
        obj: Object to describe (may or may not have lifecycle_state)
        base_description: The base description text
        include_phrase_prefix: Whether to add lifecycle phrase prefix

    Returns:
        Lifecycle-aware description or base description
    """
    lifecycle_state = getattr(obj, "lifecycle_state", None)

    if lifecycle_state is None or not include_phrase_prefix:
        return base_description

    phrase = lifecycle_state.experience_phrase
    # Experience phrases end with "..." so we connect naturally
    return f"{phrase} {base_description}"


def format_lifecycle_context(
    obj: Any,
    include_state: bool = True,
    include_meaning: bool = False,
) -> Optional[str]:
    """
    Generate lifecycle context string for an object.

    Useful for adding lifecycle context to responses without
    restructuring the entire description.

    Args:
        obj: Object to get lifecycle context from
        include_state: Include the state experience phrase
        include_meaning: Include the state meaning

    Returns:
        Context string or None if object has no lifecycle
    """
    lifecycle_state = getattr(obj, "lifecycle_state", None)

    if lifecycle_state is None:
        return None

    parts = []

    if include_state:
        parts.append(lifecycle_state.experience_phrase)

    if include_meaning:
        parts.append(f"({lifecycle_state.meaning})")

    return " ".join(parts) if parts else None


def explain_transition(
    from_state: LifecycleState,
    to_state: LifecycleState,
    object_name: str = "this",
    reason: Optional[str] = None,
) -> str:
    """
    Generate a user-friendly explanation for a lifecycle transition.

    Wrapper around transition_explanation for convenience.

    Args:
        from_state: The state the object is transitioning from
        to_state: The state the object is transitioning to
        object_name: Name/description of the object
        reason: Optional context for why the transition happened

    Returns:
        Friendly explanation string
    """
    return transition_explanation(from_state, to_state, object_name, reason)


def has_lifecycle(obj: Any) -> bool:
    """
    Check if an object has lifecycle state tracking.

    Args:
        obj: Object to check

    Returns:
        True if object has a non-None lifecycle_state
    """
    return getattr(obj, "lifecycle_state", None) is not None


def get_lifecycle_state(obj: Any) -> Optional[LifecycleState]:
    """
    Safely get the lifecycle state of an object.

    Args:
        obj: Object to get state from

    Returns:
        LifecycleState or None
    """
    return getattr(obj, "lifecycle_state", None)
