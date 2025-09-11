"""
Backend utilities for formatting standup metrics in human-readable format.
Mirrors the frontend formatting functions for consistent rendering.

This module provides human-readable formatting for standup metrics, transforming
technical values into user-friendly display text with contextual feedback.

Examples:
    >>> from services.utils.standup_formatting import format_duration, format_efficiency_multiplier
    >>> format_duration(5297)
    '5.3s'
    >>> format_duration_with_context(5297)
    '5.3s (under target)'
    >>> format_efficiency_multiplier(15, 5.3)
    '170x faster'
    >>> format_time_saved(18)
    '18m saved'

Usage in API:
    from services.utils.standup_formatting import format_standup_metrics
    formatted = format_standup_metrics({
        'generation_time_ms': 5297,
        'time_saved_minutes': 18
    })
    # Returns enhanced dict with formatted fields added
"""


def format_duration(ms):
    """
    Convert milliseconds to human-readable duration.
    Mirrors the frontend formatDuration() function.

    Args:
        ms: Duration in milliseconds

    Returns:
        str: Human-readable duration string
    """
    if not ms:
        return "N/A"

    seconds = ms / 1000
    if seconds < 1:
        return f"{ms}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    else:
        minutes = int(seconds // 60)
        remaining_seconds = int(seconds % 60)
        if remaining_seconds == 0:
            return f"{minutes}m"
        else:
            return f"{minutes}m {remaining_seconds}s"


def format_duration_with_context(ms):
    """
    Convert milliseconds to human-readable duration with contextual feedback.
    Mirrors the frontend formatDurationWithContext() function.

    Args:
        ms: Duration in milliseconds

    Returns:
        str: Human-readable duration with context
    """
    if not ms:
        return "N/A"

    formatted = format_duration(ms)
    seconds = ms / 1000

    if seconds < 5:
        return f"{formatted} (lightning fast ⚡)"
    elif seconds < 10:
        return f"{formatted} (under target)"
    elif seconds < 15:
        return f"{formatted} (good)"
    else:
        return f"{formatted} (optimize me)"


def format_time_saved(minutes):
    """
    Format time saved in human-readable format.
    Mirrors the frontend formatTimeSaved() function.

    Args:
        minutes: Time saved in minutes

    Returns:
        str: Human-readable time saved string
    """
    if not minutes or minutes <= 0:
        return "No time saved"

    if minutes < 1:
        seconds = int(minutes * 60)
        return f"{seconds}s saved"
    elif minutes < 60:
        if minutes == int(minutes):
            return f"{int(minutes)}m saved"
        else:
            return f"{minutes:.1f}m saved"
    else:
        hours = int(minutes // 60)
        remaining_minutes = int(minutes % 60)
        if remaining_minutes == 0:
            return f"{hours}h saved"
        else:
            return f"{hours}h {remaining_minutes}m saved"


def format_efficiency_multiplier(base_minutes, actual_seconds):
    """
    Calculate and format efficiency multiplier.
    Shows how much faster the automated process is vs manual.

    Args:
        base_minutes: Manual process baseline in minutes (usually 15)
        actual_seconds: Actual automated time in seconds

    Returns:
        str: Human-readable efficiency multiplier
    """
    if not actual_seconds or actual_seconds <= 0:
        return "N/A"

    base_seconds = base_minutes * 60
    multiplier = base_seconds / actual_seconds

    if multiplier >= 100:
        return f"{multiplier:.0f}x faster"
    elif multiplier >= 10:
        return f"{multiplier:.1f}x faster"
    else:
        return f"{multiplier:.2f}x faster"


def format_standup_metrics(metrics_dict):
    """
    Format complete standup metrics for human-readable display.
    Converts raw metrics to formatted versions.

    Args:
        metrics_dict: Dict with keys like 'generation_time_ms', 'time_saved_minutes'

    Returns:
        dict: Formatted metrics with human-readable values
    """
    formatted = {}

    # Copy original metrics
    formatted.update(metrics_dict)

    # Add formatted versions
    if "generation_time_ms" in metrics_dict:
        formatted["generation_time_formatted"] = format_duration(metrics_dict["generation_time_ms"])
        formatted["generation_time_with_context"] = format_duration_with_context(
            metrics_dict["generation_time_ms"]
        )

        # Calculate efficiency multiplier (15 min baseline)
        if metrics_dict["generation_time_ms"]:
            actual_seconds = metrics_dict["generation_time_ms"] / 1000
            formatted["efficiency_multiplier"] = format_efficiency_multiplier(15, actual_seconds)

    if "time_saved_minutes" in metrics_dict:
        formatted["time_saved_formatted"] = format_time_saved(metrics_dict["time_saved_minutes"])

    return formatted
