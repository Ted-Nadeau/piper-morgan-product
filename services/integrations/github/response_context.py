"""
Grammar-conscious GitHub response context.

This module provides rich context for generating grammar-conscious
GitHub responses. It captures repository atmosphere, issue/PR
significance, and temporal framing needed to make Piper's GitHub
responses feel experiential rather than data-driven.

Issue #621: GRAMMAR-TRANSFORM: GitHub Integration
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class GitHubResponseContext:
    """
    Rich context for grammar-conscious GitHub responses.

    This captures everything Piper knows when discussing GitHub items:
    - Repository atmosphere (busy, quiet, hot)
    - Item significance (routine, notable, urgent)
    - Temporal framing (fresh, aging, stale)
    - Collaborative context (who's involved, who's waiting)

    In MUX grammar: this is the Situation for GitHub responses.
    """

    # Repository context
    repo_name: str
    repo_atmosphere: str = "normal"  # "active", "quiet", "hot", "normal"

    # Item context
    item_type: str = "issue"  # "issue", "pr", "commit"
    item_number: int = 0
    item_title: str = ""

    # Temporal context
    age_days: int = 0
    activity_level: str = "normal"  # "active", "recent", "moderate", "stale"
    last_activity_hours: float = 0.0

    # Priority context
    priority_level: str = "normal"  # "critical", "high", "normal", "low"
    attention_score: float = 0.5

    # Collaborative context
    author: str = ""
    assignees: List[str] = field(default_factory=list)
    reviewers: List[str] = field(default_factory=list)
    comment_count: int = 0

    # State context
    state: str = "open"  # "open", "closed", "merged"
    is_blocked: bool = False
    labels: List[str] = field(default_factory=list)

    # Timestamp
    timestamp: datetime = field(default_factory=datetime.now)

    @classmethod
    def from_issue_data(
        cls,
        issue_data: Dict[str, Any],
        spatial_analysis: Optional[Dict[str, Any]] = None,
    ) -> "GitHubResponseContext":
        """
        Build response context from GitHub issue data.

        Args:
            issue_data: Raw issue data from GitHub API
            spatial_analysis: Optional 8-dimensional spatial analysis

        Returns:
            GitHubResponseContext for grammar-conscious responses
        """
        # Extract basic info
        repo_name = issue_data.get("repository", "")
        if isinstance(repo_name, dict):
            repo_name = repo_name.get("full_name", "")

        # Determine item type
        is_pr = (
            issue_data.get("is_pull_request", False) or issue_data.get("pull_request") is not None
        )
        item_type = "pr" if is_pr else "issue"

        # Extract temporal info
        age_days = 0
        activity_level = "normal"
        last_activity_hours = 0.0

        if spatial_analysis and "TEMPORAL" in spatial_analysis:
            temporal = spatial_analysis["TEMPORAL"]
            age_days = temporal.get("age_days", 0)
            activity_level = temporal.get("activity_level", "normal")
            last_activity_hours = temporal.get("last_activity_hours", 0.0)
        elif "created_at" in issue_data:
            # Calculate from timestamps if no spatial analysis
            try:
                created = _parse_datetime(issue_data["created_at"])
                age_days = (datetime.now(created.tzinfo) - created).days
            except (ValueError, TypeError):
                pass

        # Extract priority info
        priority_level = "normal"
        attention_score = 0.5

        if spatial_analysis and "PRIORITY" in spatial_analysis:
            priority = spatial_analysis["PRIORITY"]
            priority_level = priority.get("priority_level", "normal")
            attention_score = priority.get("attention_score", 0.5)
        else:
            # Infer from labels
            labels = _extract_labels(issue_data)
            priority_level = _infer_priority_from_labels(labels)

        # Extract collaborative info
        author = ""
        if "user" in issue_data:
            user = issue_data["user"]
            author = user.get("login", "") if isinstance(user, dict) else str(user)

        assignees = issue_data.get("assignees", [])
        if assignees and isinstance(assignees[0], dict):
            assignees = [a.get("login", "") for a in assignees]

        reviewers = []
        if "requested_reviewers" in issue_data:
            reviewers = [r.get("login", "") for r in issue_data.get("requested_reviewers", [])]

        # Extract state
        state = issue_data.get("state", "open")
        is_blocked = _check_if_blocked(issue_data, spatial_analysis)

        return cls(
            repo_name=repo_name,
            item_type=item_type,
            item_number=issue_data.get("number", 0),
            item_title=issue_data.get("title", ""),
            age_days=age_days,
            activity_level=activity_level,
            last_activity_hours=last_activity_hours,
            priority_level=priority_level,
            attention_score=attention_score,
            author=author,
            assignees=assignees,
            reviewers=reviewers,
            comment_count=issue_data.get("comments", issue_data.get("comments_count", 0)),
            state=state,
            is_blocked=is_blocked,
            labels=_extract_labels(issue_data),
        )

    def is_stale(self) -> bool:
        """Check if item is stale."""
        return self.activity_level == "stale" or self.age_days > 14

    def is_urgent(self) -> bool:
        """Check if item needs urgent attention."""
        return self.priority_level in ("critical", "high") or self.attention_score > 0.8

    def needs_review(self) -> bool:
        """Check if PR needs reviewers."""
        return self.item_type == "pr" and not self.reviewers and self.state == "open"

    def has_discussion(self) -> bool:
        """Check if there's been discussion."""
        return self.comment_count > 0


def _parse_datetime(dt_string: str) -> datetime:
    """Parse ISO datetime string."""
    from datetime import timezone

    # Handle both Z suffix and +00:00 format
    dt_string = dt_string.replace("Z", "+00:00")
    return datetime.fromisoformat(dt_string)


def _extract_labels(issue_data: Dict[str, Any]) -> List[str]:
    """Extract label names from issue data."""
    labels = issue_data.get("labels", [])
    if not labels:
        return []
    if isinstance(labels[0], dict):
        return [label.get("name", "") for label in labels]
    return labels


def _infer_priority_from_labels(labels: List[str]) -> str:
    """Infer priority level from labels."""
    labels_lower = [label.lower() for label in labels]

    if any(kw in labels_lower for kw in ["critical", "urgent", "p0", "priority: critical"]):
        return "critical"
    if any(kw in labels_lower for kw in ["high-priority", "important", "p1", "priority: high"]):
        return "high"
    if any(kw in labels_lower for kw in ["low-priority", "nice-to-have", "p3", "priority: low"]):
        return "low"
    return "normal"


def _check_if_blocked(
    issue_data: Dict[str, Any],
    spatial_analysis: Optional[Dict[str, Any]],
) -> bool:
    """Check if item is blocked."""
    # Check spatial analysis
    if spatial_analysis and "FLOW" in spatial_analysis:
        flow = spatial_analysis["FLOW"]
        if flow.get("is_blocked", False):
            return True

    # Check labels
    labels = _extract_labels(issue_data)
    blocked_labels = ["blocked", "waiting", "on-hold", "needs-info"]
    return any(label.lower() in blocked_labels for label in labels)
