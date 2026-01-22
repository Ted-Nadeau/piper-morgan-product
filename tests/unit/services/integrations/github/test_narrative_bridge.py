"""
Tests for GitHubNarrativeBridge.

Issue #621: GRAMMAR-TRANSFORM: GitHub Integration
Phase 2: Narrative Bridge Tests
"""

import pytest

from services.integrations.github.narrative_bridge import GitHubNarrativeBridge
from services.integrations.github.response_context import GitHubResponseContext


class TestNarrateAge:
    """Test age narration."""

    def test_just_created(self):
        """0 days -> just created."""
        bridge = GitHubNarrativeBridge()
        assert bridge.narrate_age(0) == "just created"

    def test_yesterday(self):
        """1 day -> created yesterday."""
        bridge = GitHubNarrativeBridge()
        assert bridge.narrate_age(1) == "created yesterday"

    def test_few_days(self):
        """2-6 days -> open for X days."""
        bridge = GitHubNarrativeBridge()
        assert bridge.narrate_age(3) == "open for 3 days"
        assert bridge.narrate_age(6) == "open for 6 days"

    def test_about_a_week(self):
        """7-13 days -> waiting for about a week."""
        bridge = GitHubNarrativeBridge()
        assert bridge.narrate_age(7) == "waiting for about a week"
        assert bridge.narrate_age(10) == "waiting for about a week"

    def test_two_weeks(self):
        """14-20 days -> waiting for two weeks."""
        bridge = GitHubNarrativeBridge()
        assert bridge.narrate_age(14) == "waiting for two weeks"
        assert bridge.narrate_age(18) == "waiting for two weeks"

    def test_three_weeks(self):
        """21-27 days -> waiting for about three weeks."""
        bridge = GitHubNarrativeBridge()
        assert bridge.narrate_age(21) == "waiting for about three weeks"

    def test_about_a_month(self):
        """28-44 days -> around for about a month."""
        bridge = GitHubNarrativeBridge()
        assert bridge.narrate_age(30) == "around for about a month"
        assert bridge.narrate_age(40) == "around for about a month"

    def test_couple_months(self):
        """45-74 days -> around for a couple months."""
        bridge = GitHubNarrativeBridge()
        assert bridge.narrate_age(60) == "around for a couple months"

    def test_many_months(self):
        """75+ days -> around for X months."""
        bridge = GitHubNarrativeBridge()
        assert bridge.narrate_age(90) == "around for 3 months"
        assert bridge.narrate_age(180) == "around for 6 months"


class TestNarrateActivity:
    """Test activity level narration."""

    def test_active(self):
        """Active -> has lots of activity."""
        bridge = GitHubNarrativeBridge()
        assert bridge.narrate_activity("active") == "has lots of activity"

    def test_recent(self):
        """Recent -> had some recent activity."""
        bridge = GitHubNarrativeBridge()
        assert bridge.narrate_activity("recent") == "had some recent activity"

    def test_moderate(self):
        """Moderate -> has been pretty quiet."""
        bridge = GitHubNarrativeBridge()
        assert bridge.narrate_activity("moderate") == "has been pretty quiet"

    def test_stale(self):
        """Stale -> has been quiet for a while."""
        bridge = GitHubNarrativeBridge()
        assert bridge.narrate_activity("stale") == "has been quiet for a while"

    def test_normal_empty(self):
        """Normal -> empty (don't mention)."""
        bridge = GitHubNarrativeBridge()
        assert bridge.narrate_activity("normal") == ""

    def test_unknown_empty(self):
        """Unknown -> empty."""
        bridge = GitHubNarrativeBridge()
        assert bridge.narrate_activity("unknown") == ""


class TestNarratePriority:
    """Test priority narration."""

    def test_critical(self):
        """Critical -> needs attention right away."""
        bridge = GitHubNarrativeBridge()
        assert bridge.narrate_priority("critical") == "needs attention right away"

    def test_high(self):
        """High -> is high priority."""
        bridge = GitHubNarrativeBridge()
        assert bridge.narrate_priority("high") == "is high priority"

    def test_normal_empty(self):
        """Normal -> empty (don't mention)."""
        bridge = GitHubNarrativeBridge()
        assert bridge.narrate_priority("normal") == ""

    def test_low(self):
        """Low -> is lower priority."""
        bridge = GitHubNarrativeBridge()
        assert bridge.narrate_priority("low") == "is lower priority"


class TestNarrateState:
    """Test state narration."""

    def test_blocked(self):
        """Blocked item -> is stuck on something."""
        bridge = GitHubNarrativeBridge()
        ctx = GitHubResponseContext(
            repo_name="r",
            is_blocked=True,
        )
        assert bridge.narrate_state(ctx) == "is stuck on something"

    def test_pr_no_reviewers(self):
        """PR without reviewers -> waiting for someone to review."""
        bridge = GitHubNarrativeBridge()
        ctx = GitHubResponseContext(
            repo_name="r",
            item_type="pr",
            state="open",
            reviewers=[],
        )
        assert bridge.narrate_state(ctx) == "waiting for someone to review"

    def test_pr_with_reviewers(self):
        """PR with reviewers -> empty."""
        bridge = GitHubNarrativeBridge()
        ctx = GitHubResponseContext(
            repo_name="r",
            item_type="pr",
            state="open",
            reviewers=["alex"],
        )
        assert bridge.narrate_state(ctx) == ""

    def test_issue_normal(self):
        """Normal issue -> empty."""
        bridge = GitHubNarrativeBridge()
        ctx = GitHubResponseContext(
            repo_name="r",
            item_type="issue",
            state="open",
        )
        assert bridge.narrate_state(ctx) == ""


class TestNarrateCollaboration:
    """Test collaboration narration."""

    def test_no_comments(self):
        """No comments -> no one's weighed in yet."""
        bridge = GitHubNarrativeBridge()
        ctx = GitHubResponseContext(
            repo_name="r",
            comment_count=0,
        )
        assert "no one's weighed in yet" in bridge.narrate_collaboration(ctx)

    def test_one_comment(self):
        """One comment -> has one comment."""
        bridge = GitHubNarrativeBridge()
        ctx = GitHubResponseContext(
            repo_name="r",
            comment_count=1,
        )
        assert "has one comment" in bridge.narrate_collaboration(ctx)

    def test_some_comments(self):
        """2-4 comments -> has some discussion."""
        bridge = GitHubNarrativeBridge()
        ctx = GitHubResponseContext(
            repo_name="r",
            comment_count=3,
        )
        assert "has some discussion" in bridge.narrate_collaboration(ctx)

    def test_good_discussion(self):
        """5-9 comments -> has a good amount of discussion."""
        bridge = GitHubNarrativeBridge()
        ctx = GitHubResponseContext(
            repo_name="r",
            comment_count=7,
        )
        assert "has a good amount of discussion" in bridge.narrate_collaboration(ctx)

    def test_lots_of_discussion(self):
        """10+ comments -> has lots of discussion."""
        bridge = GitHubNarrativeBridge()
        ctx = GitHubResponseContext(
            repo_name="r",
            comment_count=15,
        )
        assert "has lots of discussion" in bridge.narrate_collaboration(ctx)

    def test_one_assignee(self):
        """One assignee -> alex is working on it."""
        bridge = GitHubNarrativeBridge()
        ctx = GitHubResponseContext(
            repo_name="r",
            comment_count=0,
            assignees=["alex"],
        )
        assert "alex is working on it" in bridge.narrate_collaboration(ctx)

    def test_multiple_assignees(self):
        """Multiple assignees -> a few people are working on it."""
        bridge = GitHubNarrativeBridge()
        ctx = GitHubResponseContext(
            repo_name="r",
            comment_count=0,
            assignees=["alex", "sam"],
        )
        assert "a few people are working on it" in bridge.narrate_collaboration(ctx)


class TestNarrateIssue:
    """Test full issue narration."""

    def test_simple_issue(self):
        """Simple issue with title."""
        bridge = GitHubNarrativeBridge()
        ctx = GitHubResponseContext(
            repo_name="r",
            item_type="issue",
            item_title="Fix login bug",
        )
        narrative = bridge.narrate_issue(ctx)
        assert 'Issue "Fix login bug"' in narrative

    def test_pr_with_title(self):
        """PR shows as PR."""
        bridge = GitHubNarrativeBridge()
        ctx = GitHubResponseContext(
            repo_name="r",
            item_type="pr",
            item_title="Add feature",
        )
        narrative = bridge.narrate_issue(ctx)
        assert 'PR "Add feature"' in narrative

    def test_issue_with_age(self):
        """Issue with age."""
        bridge = GitHubNarrativeBridge()
        ctx = GitHubResponseContext(
            repo_name="r",
            item_type="issue",
            item_title="Fix bug",
            age_days=14,
        )
        narrative = bridge.narrate_issue(ctx)
        assert "two weeks" in narrative

    def test_issue_with_priority(self):
        """Issue with high priority."""
        bridge = GitHubNarrativeBridge()
        ctx = GitHubResponseContext(
            repo_name="r",
            item_type="issue",
            item_title="Fix bug",
            priority_level="critical",
        )
        narrative = bridge.narrate_issue(ctx)
        assert "needs attention right away" in narrative

    def test_pr_waiting_review(self):
        """PR needing review."""
        bridge = GitHubNarrativeBridge()
        ctx = GitHubResponseContext(
            repo_name="r",
            item_type="pr",
            item_title="Add feature",
            state="open",
            reviewers=[],
        )
        narrative = bridge.narrate_issue(ctx)
        assert "waiting for someone to review" in narrative

    def test_combined_narrative(self):
        """Multiple aspects combined naturally."""
        bridge = GitHubNarrativeBridge()
        ctx = GitHubResponseContext(
            repo_name="r",
            item_type="pr",
            item_title="Fix critical bug",
            age_days=14,
            activity_level="stale",
            priority_level="high",
            state="open",
            reviewers=[],
        )
        narrative = bridge.narrate_issue(ctx)
        # Should contain multiple elements
        assert "PR" in narrative
        assert "Fix critical bug" in narrative
        assert "two weeks" in narrative
        assert "quiet" in narrative
        assert "high priority" in narrative

    def test_number_fallback(self):
        """Falls back to number if no title."""
        bridge = GitHubNarrativeBridge()
        ctx = GitHubResponseContext(
            repo_name="r",
            item_type="issue",
            item_number=123,
        )
        narrative = bridge.narrate_issue(ctx, include_title=True)
        assert "Issue #123" in narrative

    def test_empty_context(self):
        """Empty context returns empty."""
        bridge = GitHubNarrativeBridge()
        ctx = GitHubResponseContext(repo_name="r")
        narrative = bridge.narrate_issue(
            ctx,
            include_title=False,
            include_age=False,
            include_activity=False,
            include_priority=False,
            include_state=False,
        )
        assert narrative == ""


class TestNarrateListSummary:
    """Test list summary narration."""

    def test_empty_list(self):
        """Empty list -> nothing to show."""
        bridge = GitHubNarrativeBridge()
        assert bridge.narrate_list_summary([]) == "Nothing to show here."

    def test_single_item(self):
        """Single item -> There's one item."""
        bridge = GitHubNarrativeBridge()
        ctx = GitHubResponseContext(
            repo_name="r",
            item_title="Fix bug",
        )
        narrative = bridge.narrate_list_summary([ctx])
        assert "There's one item:" in narrative
        assert "Fix bug" in narrative

    def test_multiple_items(self):
        """Multiple items -> There are X items."""
        bridge = GitHubNarrativeBridge()
        contexts = [
            GitHubResponseContext(repo_name="r", item_title="Fix bug"),
            GitHubResponseContext(repo_name="r", item_title="Add feature"),
        ]
        narrative = bridge.narrate_list_summary(contexts)
        assert "There are 2 items:" in narrative
        assert "Fix bug" in narrative
        assert "Add feature" in narrative

    def test_truncation(self):
        """More than max_items shows truncation note."""
        bridge = GitHubNarrativeBridge()
        contexts = [GitHubResponseContext(repo_name="r", item_title=f"Item {i}") for i in range(10)]
        narrative = bridge.narrate_list_summary(contexts, max_items=3)
        assert "There are 10 items (showing 3):" in narrative
        # Should have exactly 3 bullet points
        assert narrative.count("•") == 3


class TestNarrateUrgency:
    """Test urgency narration."""

    def test_critical_priority(self):
        """Critical priority explains urgency."""
        bridge = GitHubNarrativeBridge()
        ctx = GitHubResponseContext(
            repo_name="r",
            priority_level="critical",
        )
        assert "it's marked critical" in bridge.narrate_urgency(ctx)

    def test_high_priority(self):
        """High priority explains urgency."""
        bridge = GitHubNarrativeBridge()
        ctx = GitHubResponseContext(
            repo_name="r",
            priority_level="high",
        )
        assert "it's high priority" in bridge.narrate_urgency(ctx)

    def test_high_attention(self):
        """High attention score explains urgency."""
        bridge = GitHubNarrativeBridge()
        ctx = GitHubResponseContext(
            repo_name="r",
            attention_score=0.9,
        )
        assert "getting a lot of attention" in bridge.narrate_urgency(ctx)

    def test_stale_item(self):
        """Stale item explains urgency."""
        bridge = GitHubNarrativeBridge()
        ctx = GitHubResponseContext(
            repo_name="r",
            age_days=20,  # > 14 days = stale
        )
        assert "been waiting a while" in bridge.narrate_urgency(ctx)

    def test_pr_needs_review(self):
        """PR needing review explains urgency."""
        bridge = GitHubNarrativeBridge()
        ctx = GitHubResponseContext(
            repo_name="r",
            item_type="pr",
            state="open",
            reviewers=[],
        )
        assert "needs a reviewer" in bridge.narrate_urgency(ctx)

    def test_multiple_reasons(self):
        """Multiple reasons combined."""
        bridge = GitHubNarrativeBridge()
        ctx = GitHubResponseContext(
            repo_name="r",
            priority_level="critical",
            age_days=20,
        )
        narrative = bridge.narrate_urgency(ctx)
        assert "critical" in narrative
        assert "waiting" in narrative

    def test_no_urgency(self):
        """No urgent factors -> empty."""
        bridge = GitHubNarrativeBridge()
        ctx = GitHubResponseContext(
            repo_name="r",
            priority_level="normal",
            age_days=5,
        )
        assert bridge.narrate_urgency(ctx) == ""


class TestContractorTest:
    """Verify narratives pass the Contractor Test.

    Would a competent contractor you hired talk this way?
    No technical jargon. Professional but human.
    """

    def test_no_raw_data_terms(self):
        """Narratives don't use raw data terms."""
        bridge = GitHubNarrativeBridge()
        ctx = GitHubResponseContext(
            repo_name="r",
            item_title="Fix bug",
            age_days=14,
            activity_level="stale",
            priority_level="high",
        )
        narrative = bridge.narrate_issue(ctx)

        # Should NOT contain these data-y terms
        assert "age_days" not in narrative
        assert "activity_level" not in narrative
        assert "priority_level" not in narrative
        assert "14" not in narrative  # Should say "two weeks"

    def test_natural_language(self):
        """Narratives use natural language."""
        bridge = GitHubNarrativeBridge()

        # Each narrative should read naturally
        assert "just created" == bridge.narrate_age(0)
        assert "has lots of activity" == bridge.narrate_activity("active")
        assert "needs attention right away" == bridge.narrate_priority("critical")

        # Not like a database
        assert "0 days" != bridge.narrate_age(0)
        assert "activity=active" not in bridge.narrate_activity("active")

    def test_professional_tone(self):
        """Narratives maintain professional tone."""
        bridge = GitHubNarrativeBridge()
        ctx = GitHubResponseContext(
            repo_name="r",
            item_type="pr",
            item_title="Critical fix",
            priority_level="critical",
            state="open",
            reviewers=[],
        )
        narrative = bridge.narrate_issue(ctx)

        # Professional but not robotic
        assert "!!!" not in narrative  # Not overly excited
        assert "URGENT" not in narrative.upper() or "urgent" in narrative  # Not shouty
        assert narrative[0].isupper()  # Proper capitalization
