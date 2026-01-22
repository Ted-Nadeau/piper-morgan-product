"""
Tests for GitHub narrative helpers.

Issue #621: GRAMMAR-TRANSFORM: GitHub Integration
Phase 3: Canonical Handler Integration Tests
"""

import pytest

from services.integrations.github.narrative_helpers import (
    narrate_issue_preview,
    narrate_issues_list,
    narrate_last_activity,
    narrate_open_issues_count,
    narrate_priority_issues,
    narrate_project_health,
)


class TestNarrateIssuePreview:
    """Test issue preview narration."""

    def test_basic_issue(self):
        """Basic issue with title and number."""
        issue = {"title": "Fix login bug", "number": 123}
        result = narrate_issue_preview(issue)
        assert "Fix login bug" in result
        assert "#123" in result

    def test_issue_with_age(self):
        """Issue with age gets age narrative."""
        issue = {"title": "Old issue", "number": 1, "created_at": "2025-01-01T00:00:00Z"}
        # Simulate age_days through spatial analysis
        spatial = {"TEMPORAL": {"age_days": 14}}
        result = narrate_issue_preview(issue, spatial_analysis=spatial)
        assert "Old issue" in result
        assert "two weeks" in result.lower()

    def test_issue_with_high_priority(self):
        """High priority issue gets priority narrative."""
        issue = {"title": "Critical bug", "number": 1, "labels": [{"name": "critical"}]}
        result = narrate_issue_preview(issue)
        assert "Critical bug" in result
        assert "attention" in result.lower()

    def test_pr_waiting_review(self):
        """PR without reviewers gets state narrative."""
        issue = {
            "title": "Add feature",
            "number": 1,
            "pull_request": {"url": "..."},
        }
        result = narrate_issue_preview(issue)
        assert "Add feature" in result
        # Note: needs reviewers context from spatial

    def test_truncates_long_title(self):
        """Long titles are truncated."""
        long_title = "A" * 100
        issue = {"title": long_title, "number": 1}
        result = narrate_issue_preview(issue)
        # Title should be max 60 chars
        assert len(result.split("(")[0].strip()) <= 60


class TestNarrateIssuesList:
    """Test issues list narration."""

    def test_empty_list(self):
        """Empty list returns appropriate message."""
        result = narrate_issues_list([])
        assert "No issues" in result

    def test_single_issue(self):
        """Single issue in list."""
        issues = [{"title": "Fix bug", "number": 1}]
        result = narrate_issues_list(issues)
        assert "Fix bug" in result
        assert "•" in result

    def test_multiple_issues(self):
        """Multiple issues formatted."""
        issues = [
            {"title": "Bug 1", "number": 1},
            {"title": "Bug 2", "number": 2},
            {"title": "Bug 3", "number": 3},
        ]
        result = narrate_issues_list(issues)
        assert "Bug 1" in result
        assert "Bug 2" in result
        assert "Bug 3" in result

    def test_truncation(self):
        """List truncates at max_items."""
        issues = [{"title": f"Issue {i}", "number": i} for i in range(10)]
        result = narrate_issues_list(issues, max_items=3)
        assert "Issue 0" in result
        assert "Issue 1" in result
        assert "Issue 2" in result
        assert "Issue 9" not in result
        assert "7 more" in result


class TestNarrateOpenIssuesCount:
    """Test issue count narration."""

    def test_zero_issues(self):
        """Zero issues."""
        result = narrate_open_issues_count(0)
        assert "No open issues" in result

    def test_one_issue(self):
        """One issue is singular."""
        result = narrate_open_issues_count(1)
        assert "1 open issue" in result
        assert "issues" not in result  # No plural

    def test_few_issues(self):
        """Few issues."""
        result = narrate_open_issues_count(5)
        assert "5 open issues" in result

    def test_many_issues_needs_attention(self):
        """Many issues suggests attention."""
        result = narrate_open_issues_count(15)
        assert "15 open issues" in result
        assert "attention" in result

    def test_lots_of_issues_needs_triage(self):
        """Lots of issues suggests triage."""
        result = narrate_open_issues_count(30)
        assert "30 open issues" in result
        assert "triage" in result


class TestNarrateProjectHealth:
    """Test project health narration."""

    def test_unknown_no_data(self):
        """Unknown health with no data."""
        result = narrate_project_health("My Project", None, "unknown")
        assert "My Project" in result
        assert "No recent" in result

    def test_healthy_project(self):
        """Healthy project."""
        github_data = {"open_issues_count": 3}
        result = narrate_project_health("My Project", github_data, "healthy")
        assert "My Project" in result
        assert "Looking good" in result
        assert "3 open issues" in result

    def test_at_risk_project(self):
        """At-risk project."""
        github_data = {"open_issues_count": 8, "age_days": 20}
        result = narrate_project_health("My Project", github_data, "at-risk")
        assert "My Project" in result
        assert "8 open issues" in result

    def test_stalled_project(self):
        """Stalled project."""
        github_data = {"open_issues_count": 5}
        result = narrate_project_health("My Project", github_data, "stalled")
        assert "My Project" in result
        assert "quiet" in result


class TestNarrateLastActivity:
    """Test last activity narration."""

    def test_no_activity(self):
        """No activity data."""
        result = narrate_last_activity("My Project", None)
        assert "No recent activity" in result
        assert "My Project" in result

    def test_no_date(self):
        """Activity without date."""
        activity = {"type": "commit"}
        result = narrate_last_activity("My Project", activity)
        assert "Recent commit" in result

    def test_today(self):
        """Activity today."""
        from datetime import datetime, timezone

        activity = {
            "type": "commit",
            "date": datetime.now(timezone.utc).isoformat(),
        }
        result = narrate_last_activity("My Project", activity)
        assert "today" in result.lower()

    def test_yesterday(self):
        """Activity yesterday."""
        from datetime import datetime, timedelta, timezone

        yesterday = datetime.now(timezone.utc) - timedelta(days=1)
        activity = {
            "type": "PR",
            "date": yesterday.isoformat(),
        }
        result = narrate_last_activity("My Project", activity)
        assert "yesterday" in result.lower()

    def test_older_activity(self):
        """Activity from weeks ago."""
        from datetime import datetime, timedelta, timezone

        two_weeks_ago = datetime.now(timezone.utc) - timedelta(days=14)
        activity = {
            "type": "issue",
            "date": two_weeks_ago.isoformat(),
        }
        result = narrate_last_activity("My Project", activity)
        assert "two weeks" in result.lower() or "weeks" in result.lower()


class TestNarratePriorityIssues:
    """Test priority issues narration."""

    def test_no_urgent_issues(self):
        """No urgent issues."""
        result = narrate_priority_issues([])
        assert "No urgent issues" in result

    def test_single_urgent_issue(self):
        """Single urgent issue."""
        issues = [{"title": "Critical bug", "number": 1, "labels": [{"name": "critical"}]}]
        result = narrate_priority_issues(issues)
        assert "One urgent item" in result
        assert "Critical bug" in result

    def test_multiple_urgent_issues(self):
        """Multiple urgent issues."""
        issues = [
            {"title": "Bug 1", "number": 1, "labels": [{"name": "critical"}]},
            {"title": "Bug 2", "number": 2, "labels": [{"name": "urgent"}]},
        ]
        result = narrate_priority_issues(issues)
        assert "2 items need attention" in result
        assert "Bug 1" in result
        assert "Bug 2" in result

    def test_truncation(self):
        """Truncates at max_items."""
        issues = [
            {"title": f"Bug {i}", "number": i, "labels": [{"name": "critical"}]} for i in range(5)
        ]
        result = narrate_priority_issues(issues, max_items=2)
        assert "Bug 0" in result
        assert "Bug 1" in result
        assert "Bug 4" not in result
        assert "3 more" in result


class TestContractorTest:
    """Verify helpers pass Contractor Test."""

    def test_no_raw_data_in_issue_preview(self):
        """Issue preview uses natural language."""
        issue = {"title": "Fix bug", "number": 123, "labels": [{"name": "critical"}]}
        result = narrate_issue_preview(issue)

        # No raw data terms
        assert "priority_level" not in result
        assert "labels:" not in result.lower()

    def test_no_raw_data_in_count(self):
        """Count uses natural language."""
        result = narrate_open_issues_count(15)

        # Natural phrasing
        assert "open_issues_count" not in result
        assert "15 open issues" in result

    def test_professional_health_narrative(self):
        """Health narrative is professional."""
        github_data = {"open_issues_count": 5}
        result = narrate_project_health("Test", github_data, "healthy")

        # Professional but not robotic
        assert "Looking good" in result
        assert "status:" not in result.lower()
        assert "HEALTHY" not in result  # Not shouty
