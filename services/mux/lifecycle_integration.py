"""
Lifecycle Integration Helpers for Intent Handlers.

This module provides helper functions for integrating lifecycle-aware
language into intent handler responses. Handlers can use these helpers
to describe objects with lifecycle-appropriate phrases.

Also provides status-to-lifecycle mapping and synchronization functions
for automatically managing lifecycle state based on object status.

Example:
    from services.mux.lifecycle_integration import describe_with_lifecycle

    # In a handler:
    description = describe_with_lifecycle(
        feature, "the authentication feature"
    )
    # Returns: "I just noticed the authentication feature..." if EMERGENT
    # Returns: "the authentication feature" if no lifecycle state

Example (initialization):
    from services.mux.lifecycle_integration import initialize_lifecycle

    item = WorkItem(status="open")
    initialize_lifecycle(item)
    # item.lifecycle_state is now LifecycleState.NOTICED
"""

import logging
from typing import Any, Dict, Optional

from services.mux.lifecycle import (
    InvalidTransitionError,
    LifecycleManager,
    LifecycleState,
    transition_explanation,
)

logger = logging.getLogger(__name__)

# Status-to-lifecycle mappings for domain objects
# These define the canonical mapping from object status to lifecycle state

WORKITEM_STATUS_TO_LIFECYCLE: Dict[str, LifecycleState] = {
    "open": LifecycleState.NOTICED,
    "in_progress": LifecycleState.RATIFIED,
    "done": LifecycleState.DEPRECATED,
    "closed": LifecycleState.ARCHIVED,
}

FEATURE_STATUS_TO_LIFECYCLE: Dict[str, LifecycleState] = {
    "draft": LifecycleState.EMERGENT,
    "proposed": LifecycleState.PROPOSED,
    "approved": LifecycleState.RATIFIED,
    "shipped": LifecycleState.DEPRECATED,
    "archived": LifecycleState.ARCHIVED,
}


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


def get_lifecycle_for_status(obj: Any) -> Optional[LifecycleState]:
    """
    Get the appropriate lifecycle state for an object's current status.

    Uses the status-to-lifecycle mappings defined for each object type.

    Args:
        obj: Object with a status field (WorkItem, Feature, etc.)

    Returns:
        Appropriate LifecycleState or None if no mapping exists
    """
    status = getattr(obj, "status", None)
    if status is None:
        return None

    # Determine object type and get appropriate mapping
    class_name = obj.__class__.__name__

    if class_name == "WorkItem":
        return WORKITEM_STATUS_TO_LIFECYCLE.get(status)
    elif class_name == "Feature":
        return FEATURE_STATUS_TO_LIFECYCLE.get(status)

    return None


def initialize_lifecycle(obj: Any) -> bool:
    """
    Set initial lifecycle_state based on object's current status.

    Only sets lifecycle_state if it's currently None. This prevents
    overwriting explicitly set lifecycle states.

    Args:
        obj: Object to initialize (must have lifecycle_state attribute)

    Returns:
        True if lifecycle was initialized, False otherwise
    """
    # Only initialize if lifecycle_state exists and is None
    if not hasattr(obj, "lifecycle_state"):
        return False

    if obj.lifecycle_state is not None:
        return False  # Already has a state

    lifecycle = get_lifecycle_for_status(obj)
    if lifecycle:
        obj.lifecycle_state = lifecycle
        return True

    return False


def sync_lifecycle_to_status(obj: Any, notify: bool = False) -> bool:
    """
    Synchronize lifecycle_state to match current status.

    If the object's status has changed, attempts to transition the
    lifecycle state to match. Invalid transitions are logged but
    do not raise exceptions.

    Args:
        obj: Object to sync (must have lifecycle_state and status)
        notify: Whether to trigger notifications (future use)

    Returns:
        True if lifecycle was updated, False otherwise
    """
    target_state = get_lifecycle_for_status(obj)
    if target_state is None:
        return False

    current_state = getattr(obj, "lifecycle_state", None)

    # Already in target state
    if current_state == target_state:
        return False

    # No current state - just set it (initialization case)
    if current_state is None:
        obj.lifecycle_state = target_state
        return True

    # Attempt transition
    try:
        manager = LifecycleManager()
        manager.transition(obj, target_state)
        logger.debug(
            f"Lifecycle transition: {obj.__class__.__name__} "
            f"{current_state.value} -> {target_state.value}"
        )
        return True
    except InvalidTransitionError as e:
        # Invalid transitions are not errors - just log and skip
        logger.warning(
            f"Lifecycle transition skipped for {obj.__class__.__name__}: " f"{e.user_message}"
        )
        return False
