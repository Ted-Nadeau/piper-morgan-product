"""
Workspace navigation language generation.

Part of #659 WORKSPACE-NAVIGATION (child of #416 MUX-INTERACT-WORKSPACE epic).

This module provides:
- NAVIGATION_PATTERNS: Template patterns for context switches
- navigate_language(): Generate natural switch language
- reference_language(): Generate natural cross-context references
- humanize_duration(): Human-readable time intervals

Generates conversational, natural-feeling language when Piper
references or switches between contexts.

Anti-patterns avoided:
- "workspace_id: W123ABC" → "your Slack workspace"
- "Integration: slack" → "#general"
- "Context changed to: GitHub" → "Over in GitHub..."
"""

from datetime import timedelta
from typing import List, Optional

from services.mux.workspace_detection import ContextSwitch, WorkspaceContext

# =============================================================================
# Navigation Patterns
# =============================================================================

NAVIGATION_PATTERNS = {
    "switch_to": [
        "Over in {destination}...",
        "Looking at {destination}...",
        "In your {destination}...",
    ],
    "return_to": [
        "Back in {destination}...",
        "Returning to {destination}...",
        "Picking up where we left off in {destination}...",
    ],
    "reference": [
        "Meanwhile, in {location}...",
        "Over in {location}, I see...",
        "In {location}...",
    ],
}


# =============================================================================
# Duration Humanization
# =============================================================================


def humanize_duration(duration: timedelta) -> str:
    """
    Convert a timedelta to human-readable text.

    Examples:
        - 30 minutes → "30 minutes"
        - 1 hour → "an hour"
        - 2 hours → "a couple hours"
        - 5 hours → "about 5 hours"
        - 1 day → "a day"
        - 3 days → "a few days"

    Args:
        duration: Time interval to humanize

    Returns:
        Human-readable duration string
    """
    total_seconds = duration.total_seconds()

    if total_seconds < 0:
        return "moments ago"

    minutes = total_seconds / 60
    hours = total_seconds / 3600
    days = total_seconds / 86400

    if minutes < 1:
        return "a few seconds"
    elif minutes < 2:
        return "a minute"
    elif minutes < 60:
        return f"{int(minutes)} minutes"
    elif hours < 1.5:
        return "an hour"
    elif hours < 2.5:
        return "a couple hours"
    elif hours < 24:
        return f"about {int(hours)} hours"
    elif days < 1.5:
        return "a day"
    elif days < 7:
        return f"a few days"
    elif days < 14:
        return "about a week"
    else:
        return f"about {int(days / 7)} weeks"


# =============================================================================
# Navigation Language Generation
# =============================================================================


def _select_pattern(patterns: List[str], seed: str) -> str:
    """
    Select a pattern deterministically based on a seed string.

    Uses hash-based selection for consistency (same input → same pattern).
    This makes behavior predictable for testing while still varying output.

    Args:
        patterns: List of pattern templates
        seed: String to hash for selection (e.g., workspace_id)

    Returns:
        Selected pattern template
    """
    if not patterns:
        return "{destination}"

    index = hash(seed) % len(patterns)
    return patterns[index]


def navigate_language(
    switch: ContextSwitch,
    include_context: bool = True,
) -> str:
    """
    Generate natural navigation language for a context switch.

    Args:
        switch: The detected context switch
        include_context: Whether to include time-away context for returns

    Returns:
        Natural-feeling navigation phrase

    Examples:
        >>> navigate_language(explicit_switch)
        "Over in #general..."
        >>> navigate_language(return_switch_with_time)
        "Back in your Slack workspace... (it's been about 2 hours)"
    """
    # Select patterns based on switch type
    if switch.switch_type == "return":
        patterns = NAVIGATION_PATTERNS["return_to"]
    else:
        patterns = NAVIGATION_PATTERNS["switch_to"]

    # Get friendly name from destination context
    destination = switch.to_context.friendly_name

    # Select pattern deterministically based on destination
    pattern = _select_pattern(patterns, switch.to_context.workspace_id)

    # Build base message
    message = pattern.format(destination=destination)

    # Add time-away context for returns when appropriate
    if include_context and switch.switch_type == "return" and switch.time_away:
        # Only include for significant time gaps (> 1 hour)
        if switch.time_away > timedelta(hours=1):
            duration_text = humanize_duration(switch.time_away)
            message += f" (it's been {duration_text})"

    return message


def reference_language(
    location: WorkspaceContext,
    observation: str,
) -> str:
    """
    Generate language for referencing another context.

    Used when mentioning something in a different workspace without
    fully switching to it.

    Args:
        location: The workspace being referenced
        observation: What Piper observed there

    Returns:
        Natural-feeling reference phrase with observation

    Examples:
        >>> reference_language(github_context, "there's a new PR")
        "Over in GitHub, I see... there's a new PR"
    """
    patterns = NAVIGATION_PATTERNS["reference"]

    # Select pattern deterministically based on location
    pattern = _select_pattern(patterns, location.workspace_id)

    # Format and combine with observation
    prefix = pattern.format(location=location.friendly_name)

    # Handle patterns that end with "I see..."
    if prefix.rstrip().endswith("I see..."):
        # Lowercase the observation to flow naturally
        observation = observation.lstrip()
        if observation and observation[0].isupper():
            observation = observation[0].lower() + observation[1:]
        return f"{prefix} {observation}"

    # Standard concatenation
    return f"{prefix} {observation}"
