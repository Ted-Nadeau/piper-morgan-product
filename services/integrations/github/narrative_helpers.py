"""
GitHub Narrative Helpers for Canonical Handlers.

This module provides helper functions to transform raw GitHub data
into grammar-conscious narratives within canonical handlers.

Issue #621: GRAMMAR-TRANSFORM: GitHub Integration
Phase 3: Canonical Handler Integration
"""

from typing import Any, Dict, List, Optional

from services.integrations.github.narrative_bridge import GitHubNarrativeBridge
from services.integrations.github.response_context import GitHubResponseContext

# Singleton bridge instance
_narrative_bridge = GitHubNarrativeBridge()


def narrate_issue_preview(
    issue_data: Dict[str, Any],
    spatial_analysis: Optional[Dict[str, Any]] = None,
    include_age: bool = True,
    include_priority: bool = True,
) -> str:
    """Convert issue data to a narrative preview line.

    Args:
        issue_data: Raw issue data from GitHub API
        spatial_analysis: Optional spatial analysis dict
        include_age: Whether to include age narrative
        include_priority: Whether to include priority narrative

    Returns:
        Human-readable narrative string

    Example:
        Input: {"title": "Fix login", "number": 123, "age_days": 14}
        Output: "Fix login (#123) - waiting for two weeks"
    """
    ctx = GitHubResponseContext.from_issue_data(issue_data, spatial_analysis)

    title = issue_data.get("title", "Untitled")[:60]
    number = issue_data.get("number", "")

    parts = [f"{title}"]
    if number:
        parts[0] = f"{title} (#{number})"

    # Add age narrative
    if include_age and ctx.age_days > 0:
        age_text = _narrative_bridge.narrate_age(ctx.age_days)
        if age_text and age_text != "just created":
            parts.append(age_text)

    # Add priority narrative
    if include_priority and ctx.priority_level != "normal":
        priority_text = _narrative_bridge.narrate_priority(ctx.priority_level)
        if priority_text:
            parts.append(priority_text)

    # Add state narrative
    state_text = _narrative_bridge.narrate_state(ctx)
    if state_text:
        parts.append(state_text)

    if len(parts) == 1:
        return parts[0]

    return f"{parts[0]} - {', '.join(parts[1:])}"


def narrate_issues_list(
    issues: List[Dict[str, Any]],
    max_items: int = 5,
    spatial_analysis: Optional[Dict[str, Any]] = None,
) -> str:
    """Convert a list of issues to narrative format.

    Args:
        issues: List of issue data dicts
        max_items: Maximum items to show
        spatial_analysis: Optional spatial analysis

    Returns:
        Formatted narrative list
    """
    if not issues:
        return "No issues to show."

    lines = []
    for issue in issues[:max_items]:
        narrative = narrate_issue_preview(issue, spatial_analysis)
        lines.append(f"  • {narrative}")

    if len(issues) > max_items:
        remaining = len(issues) - max_items
        lines.append(f"  ... and {remaining} more")

    return "\n".join(lines)


def narrate_open_issues_count(count: int) -> str:
    """Convert issue count to natural language.

    Args:
        count: Number of open issues

    Returns:
        Human-readable string

    Examples:
        0 -> "No open issues"
        1 -> "1 open issue"
        5 -> "5 open issues"
        15 -> "15 open issues - might need attention"
    """
    if count == 0:
        return "No open issues"
    elif count == 1:
        return "1 open issue"
    elif count < 10:
        return f"{count} open issues"
    elif count < 25:
        return f"{count} open issues - might need attention"
    else:
        return f"{count} open issues - this needs some triage"


def narrate_project_health(
    project_name: str,
    github_data: Optional[Dict[str, Any]],
    health_status: str = "unknown",
) -> str:
    """Narrate project health in human terms.

    Args:
        project_name: Name of the project
        github_data: GitHub metadata dict
        health_status: "healthy", "at-risk", "stalled", "unknown"

    Returns:
        Human-readable health description
    """
    if not github_data or health_status == "unknown":
        return f"**{project_name}**: No recent GitHub activity"

    open_issues = github_data.get("open_issues_count", 0)
    issues_text = narrate_open_issues_count(open_issues)

    # Build health narrative based on status
    if health_status == "healthy":
        return f"**{project_name}**: Looking good - {issues_text}"
    elif health_status == "at-risk":
        # Check what's causing at-risk status
        age_days = github_data.get("age_days", 0)
        if age_days > 14:
            age_text = _narrative_bridge.narrate_age(age_days)
            return f"**{project_name}**: {issues_text}, last activity {age_text}"
        return f"**{project_name}**: {issues_text} - worth checking on"
    elif health_status == "stalled":
        return f"**{project_name}**: {issues_text} - been quiet for a while"

    return f"**{project_name}**: {issues_text}"


def narrate_last_activity(
    project_name: str,
    activity_data: Optional[Dict[str, Any]],
) -> str:
    """Narrate when a project was last active.

    Args:
        project_name: Name of the project
        activity_data: Activity metadata with date info

    Returns:
        Human-readable activity description
    """
    if not activity_data:
        return f"No recent activity on {project_name}"

    from datetime import datetime

    activity_date = activity_data.get("date", "")
    activity_type = activity_data.get("type", "activity")

    if not activity_date:
        return f"Recent {activity_type} on {project_name}"

    try:
        dt = datetime.fromisoformat(activity_date.replace("Z", "+00:00"))
        days_ago = (datetime.now(dt.tzinfo) - dt).days

        age_text = _narrative_bridge.narrate_age(days_ago)

        if days_ago == 0:
            return f"Activity on {project_name} today ({activity_type})"
        elif days_ago == 1:
            return f"Activity on {project_name} yesterday ({activity_type})"
        else:
            return f"Last {activity_type} on {project_name} was {age_text}"
    except (ValueError, TypeError):
        return f"Recent {activity_type} on {project_name}"


def narrate_priority_issues(
    high_priority_issues: List[Dict[str, Any]],
    max_items: int = 3,
) -> str:
    """Narrate high-priority issues.

    Args:
        high_priority_issues: List of critical/high priority issues
        max_items: Max items to show

    Returns:
        Human-readable priority summary
    """
    if not high_priority_issues:
        return "No urgent issues right now."

    count = len(high_priority_issues)

    if count == 1:
        issue = high_priority_issues[0]
        title = issue.get("title", "Untitled")[:50]
        return f"One urgent item: {title}"

    # Multiple items
    lines = [f"{count} items need attention:"]
    for issue in high_priority_issues[:max_items]:
        ctx = GitHubResponseContext.from_issue_data(issue)
        narrative = _narrative_bridge.narrate_urgency(ctx)
        title = issue.get("title", "Untitled")[:50]
        if narrative:
            lines.append(f"  • {title} - {narrative.lower()}")
        else:
            lines.append(f"  • {title}")

    if count > max_items:
        lines.append(f"  ... and {count - max_items} more")

    return "\n".join(lines)
