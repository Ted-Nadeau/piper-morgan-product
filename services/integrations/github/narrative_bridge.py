"""
GitHub Narrative Bridge - Transform data to experiential narratives.

This module transforms GitHub data structures into human-readable
narratives that pass the Contractor Test. Instead of "age_days: 14",
Piper says "waiting for two weeks."

Issue #621: GRAMMAR-TRANSFORM: GitHub Integration
Phase 2: Narrative Bridge
"""

from dataclasses import dataclass
from typing import Optional

from services.integrations.github.response_context import GitHubResponseContext


@dataclass
class GitHubNarrativeBridge:
    """Transform GitHub data into experiential narratives.

    In MUX grammar: this bridges Situation data to human expression.
    The goal is responses that sound like a colleague, not a database.
    """

    # Temporal narratives
    ACTIVITY_NARRATIVES = {
        "active": "has lots of activity",
        "recent": "had some recent activity",
        "moderate": "has been pretty quiet",
        "stale": "has been quiet for a while",
        "normal": "",  # Don't mention normal activity
    }

    PRIORITY_NARRATIVES = {
        "critical": "needs attention right away",
        "high": "is high priority",
        "normal": "",  # Don't mention normal priority
        "low": "is lower priority",
    }

    STATE_NARRATIVES = {
        "waiting_review": "waiting for someone to review",
        "blocked": "is stuck on something",
        "ready_merge": "is ready to merge",
        "needs_work": "needs some work",
    }

    def narrate_age(self, age_days: int) -> str:
        """Convert age to human-readable form.

        Examples:
            0 -> "just created"
            1 -> "created yesterday"
            7 -> "waiting for a week"
            14 -> "waiting for two weeks"
            30 -> "around for a month"
        """
        if age_days == 0:
            return "just created"
        elif age_days == 1:
            return "created yesterday"
        elif age_days < 7:
            return f"open for {age_days} days"
        elif age_days < 14:
            return "waiting for about a week"
        elif age_days < 21:
            return "waiting for two weeks"
        elif age_days < 28:
            return "waiting for about three weeks"
        elif age_days < 45:
            return "around for about a month"
        elif age_days < 75:
            return "around for a couple months"
        else:
            months = age_days // 30
            return f"around for {months} months"

    def narrate_activity(self, activity_level: str) -> str:
        """Convert activity level to narrative.

        Examples:
            "active" -> "has lots of activity"
            "stale" -> "has been quiet for a while"
        """
        return self.ACTIVITY_NARRATIVES.get(activity_level, "")

    def narrate_priority(self, priority_level: str) -> str:
        """Convert priority to narrative.

        Examples:
            "critical" -> "needs attention right away"
            "high" -> "is high priority"
        """
        return self.PRIORITY_NARRATIVES.get(priority_level, "")

    def narrate_state(self, ctx: GitHubResponseContext) -> str:
        """Convert state to narrative based on full context.

        Examples:
            PR with no reviewers -> "waiting for someone to review"
            Blocked item -> "is stuck on something"
        """
        if ctx.is_blocked:
            return self.STATE_NARRATIVES["blocked"]

        if ctx.item_type == "pr":
            if ctx.state == "open" and not ctx.reviewers:
                return self.STATE_NARRATIVES["waiting_review"]

        return ""

    def narrate_collaboration(self, ctx: GitHubResponseContext) -> str:
        """Describe collaborative context.

        Examples:
            No comments -> "no one's weighed in yet"
            5 comments -> "has some discussion"
            Many assignees -> "a few people are working on it"
        """
        parts = []

        if ctx.comment_count == 0:
            parts.append("no one's weighed in yet")
        elif ctx.comment_count == 1:
            parts.append("has one comment")
        elif ctx.comment_count < 5:
            parts.append("has some discussion")
        elif ctx.comment_count < 10:
            parts.append("has a good amount of discussion")
        else:
            parts.append("has lots of discussion")

        if len(ctx.assignees) > 1:
            parts.append("a few people are working on it")
        elif len(ctx.assignees) == 1:
            parts.append(f"{ctx.assignees[0]} is working on it")

        return " and ".join(parts) if parts else ""

    def narrate_issue(
        self,
        ctx: GitHubResponseContext,
        include_title: bool = True,
        include_age: bool = True,
        include_activity: bool = True,
        include_priority: bool = True,
        include_state: bool = True,
    ) -> str:
        """Create full narrative for an issue/PR.

        Combines all relevant aspects into a natural sentence.
        Only includes non-empty narratives.

        Example output:
            "Fix login bug has been waiting for two weeks and is quiet lately.
             It's high priority and waiting for someone to review."
        """
        parts = []

        # Opening with title and type
        if include_title and ctx.item_title:
            item_type_label = "PR" if ctx.item_type == "pr" else "Issue"
            parts.append(f'{item_type_label} "{ctx.item_title}"')
        elif ctx.item_number:
            item_type_label = "PR" if ctx.item_type == "pr" else "Issue"
            parts.append(f"{item_type_label} #{ctx.item_number}")

        # Age narrative
        if include_age and ctx.age_days > 0:
            age_narrative = self.narrate_age(ctx.age_days)
            if age_narrative:
                if parts:
                    parts.append(f"has been {age_narrative}")
                else:
                    parts.append(age_narrative)

        # Activity narrative
        if include_activity:
            activity_narrative = self.narrate_activity(ctx.activity_level)
            if activity_narrative:
                parts.append(activity_narrative)

        # Priority narrative
        if include_priority:
            priority_narrative = self.narrate_priority(ctx.priority_level)
            if priority_narrative:
                parts.append(priority_narrative)

        # State narrative (waiting for review, blocked, etc.)
        if include_state:
            state_narrative = self.narrate_state(ctx)
            if state_narrative:
                parts.append(state_narrative)

        # Combine naturally
        if not parts:
            return ""

        # Join with appropriate connectors
        if len(parts) == 1:
            return parts[0]
        elif len(parts) == 2:
            return f"{parts[0]} and {parts[1]}"
        else:
            # First part, then "and" for the last two with commas between
            main_parts = parts[:-1]
            last_part = parts[-1]
            return f"{', '.join(main_parts)}, and {last_part}"

    def narrate_list_summary(
        self,
        contexts: list,
        max_items: int = 5,
    ) -> str:
        """Create narrative for a list of issues/PRs.

        Example:
            "You have 3 items that need attention:
             - Fix login bug has been waiting for two weeks
             - Add feature X is high priority
             - Update docs is just created"
        """
        if not contexts:
            return "Nothing to show here."

        total = len(contexts)
        showing = min(total, max_items)

        if total == 1:
            opener = "There's one item:"
        else:
            opener = f"There are {total} items"
            if total > max_items:
                opener += f" (showing {showing})"
            opener += ":"

        items = []
        for ctx in contexts[:max_items]:
            narrative = self.narrate_issue(
                ctx,
                include_title=True,
                include_age=True,
                include_activity=False,  # Keep list items shorter
                include_priority=True,
                include_state=False,
            )
            if narrative:
                items.append(f"• {narrative}")

        return f"{opener}\n" + "\n".join(items)

    def narrate_urgency(self, ctx: GitHubResponseContext) -> str:
        """Describe why something is urgent.

        Used when highlighting items that need attention.
        """
        reasons = []

        if ctx.priority_level == "critical":
            reasons.append("it's marked critical")
        elif ctx.priority_level == "high":
            reasons.append("it's high priority")

        if ctx.attention_score > 0.8:
            reasons.append("it's getting a lot of attention")

        if ctx.is_stale():
            reasons.append("it's been waiting a while")

        if ctx.item_type == "pr" and ctx.needs_review():
            reasons.append("it needs a reviewer")

        if not reasons:
            return ""

        if len(reasons) == 1:
            return f"This needs attention because {reasons[0]}."
        else:
            return f"This needs attention because {reasons[0]} and {reasons[1]}."
