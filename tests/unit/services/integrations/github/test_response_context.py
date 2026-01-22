"""
Tests for GitHubResponseContext.

Issue #621: GRAMMAR-TRANSFORM: GitHub Integration
Phase 1: GitHubResponseContext dataclass
"""

from datetime import datetime, timedelta, timezone

import pytest

from services.integrations.github.response_context import (
    GitHubResponseContext,
    _extract_labels,
    _infer_priority_from_labels,
)


class TestGitHubResponseContext:
    """Test GitHubResponseContext dataclass."""

    def test_basic_creation(self):
        """Can create with minimal fields."""
        ctx = GitHubResponseContext(
            repo_name="owner/repo",
            item_number=123,
        )
        assert ctx.repo_name == "owner/repo"
        assert ctx.item_number == 123
        assert ctx.item_type == "issue"

    def test_full_creation(self):
        """Can create with all fields."""
        ctx = GitHubResponseContext(
            repo_name="owner/repo",
            repo_atmosphere="hot",
            item_type="pr",
            item_number=456,
            item_title="Fix critical bug",
            age_days=7,
            activity_level="active",
            priority_level="critical",
            attention_score=0.9,
            author="alex",
            assignees=["alex", "sam"],
            reviewers=["chris"],
            comment_count=5,
            state="open",
            is_blocked=False,
        )
        assert ctx.repo_atmosphere == "hot"
        assert ctx.item_type == "pr"
        assert ctx.priority_level == "critical"
        assert len(ctx.assignees) == 2


class TestFromIssueData:
    """Test from_issue_data factory method."""

    def test_basic_issue(self):
        """Creates context from basic issue data."""
        issue_data = {
            "number": 123,
            "title": "Fix login bug",
            "state": "open",
            "user": {"login": "alex"},
            "labels": [],
            "assignees": [],
            "comments": 3,
            "repository": "owner/repo",
        }
        ctx = GitHubResponseContext.from_issue_data(issue_data)

        assert ctx.item_number == 123
        assert ctx.item_title == "Fix login bug"
        assert ctx.state == "open"
        assert ctx.author == "alex"
        assert ctx.comment_count == 3

    def test_pr_detection(self):
        """Detects PR from pull_request field."""
        issue_data = {
            "number": 456,
            "title": "Add feature",
            "pull_request": {"url": "..."},
            "repository": "owner/repo",
        }
        ctx = GitHubResponseContext.from_issue_data(issue_data)

        assert ctx.item_type == "pr"

    def test_pr_detection_explicit(self):
        """Detects PR from is_pull_request field."""
        issue_data = {
            "number": 789,
            "title": "Refactor",
            "is_pull_request": True,
            "repository": "owner/repo",
        }
        ctx = GitHubResponseContext.from_issue_data(issue_data)

        assert ctx.item_type == "pr"

    def test_priority_from_labels(self):
        """Extracts priority from labels."""
        issue_data = {
            "number": 1,
            "title": "Urgent fix",
            "labels": [{"name": "critical"}, {"name": "bug"}],
            "repository": "owner/repo",
        }
        ctx = GitHubResponseContext.from_issue_data(issue_data)

        assert ctx.priority_level == "critical"

    def test_blocked_from_labels(self):
        """Detects blocked state from labels."""
        issue_data = {
            "number": 2,
            "title": "Waiting on API",
            "labels": [{"name": "blocked"}],
            "repository": "owner/repo",
        }
        ctx = GitHubResponseContext.from_issue_data(issue_data)

        assert ctx.is_blocked is True

    def test_with_spatial_analysis(self):
        """Uses spatial analysis when provided."""
        issue_data = {
            "number": 3,
            "title": "Stale issue",
            "repository": "owner/repo",
        }
        spatial = {
            "TEMPORAL": {
                "age_days": 30,
                "activity_level": "stale",
                "last_activity_hours": 720,
            },
            "PRIORITY": {
                "priority_level": "high",
                "attention_score": 0.8,
            },
        }
        ctx = GitHubResponseContext.from_issue_data(issue_data, spatial)

        assert ctx.age_days == 30
        assert ctx.activity_level == "stale"
        assert ctx.priority_level == "high"
        assert ctx.attention_score == 0.8


class TestHelperMethods:
    """Test helper methods."""

    def test_is_stale_by_activity(self):
        """Detects stale by activity level."""
        ctx = GitHubResponseContext(
            repo_name="r",
            activity_level="stale",
        )
        assert ctx.is_stale() is True

    def test_is_stale_by_age(self):
        """Detects stale by age."""
        ctx = GitHubResponseContext(
            repo_name="r",
            age_days=20,
        )
        assert ctx.is_stale() is True

    def test_not_stale(self):
        """Normal items are not stale."""
        ctx = GitHubResponseContext(
            repo_name="r",
            age_days=5,
            activity_level="active",
        )
        assert ctx.is_stale() is False

    def test_is_urgent_by_priority(self):
        """Detects urgent by priority."""
        ctx = GitHubResponseContext(
            repo_name="r",
            priority_level="critical",
        )
        assert ctx.is_urgent() is True

    def test_is_urgent_by_score(self):
        """Detects urgent by attention score."""
        ctx = GitHubResponseContext(
            repo_name="r",
            attention_score=0.9,
        )
        assert ctx.is_urgent() is True

    def test_needs_review(self):
        """Detects PR needing review."""
        ctx = GitHubResponseContext(
            repo_name="r",
            item_type="pr",
            state="open",
            reviewers=[],
        )
        assert ctx.needs_review() is True

    def test_does_not_need_review_with_reviewers(self):
        """PR with reviewers doesn't need more."""
        ctx = GitHubResponseContext(
            repo_name="r",
            item_type="pr",
            state="open",
            reviewers=["chris"],
        )
        assert ctx.needs_review() is False

    def test_has_discussion(self):
        """Detects discussion from comments."""
        ctx = GitHubResponseContext(
            repo_name="r",
            comment_count=5,
        )
        assert ctx.has_discussion() is True

    def test_no_discussion(self):
        """Detects no discussion."""
        ctx = GitHubResponseContext(
            repo_name="r",
            comment_count=0,
        )
        assert ctx.has_discussion() is False


class TestLabelHelpers:
    """Test label helper functions."""

    def test_extract_labels_dict_format(self):
        """Extracts labels from dict format."""
        issue = {"labels": [{"name": "bug"}, {"name": "urgent"}]}
        labels = _extract_labels(issue)
        assert labels == ["bug", "urgent"]

    def test_extract_labels_string_format(self):
        """Extracts labels from string format."""
        issue = {"labels": ["bug", "urgent"]}
        labels = _extract_labels(issue)
        assert labels == ["bug", "urgent"]

    def test_extract_labels_empty(self):
        """Handles empty labels."""
        issue = {"labels": []}
        labels = _extract_labels(issue)
        assert labels == []

    def test_infer_priority_critical(self):
        """Infers critical priority."""
        assert _infer_priority_from_labels(["critical"]) == "critical"
        assert _infer_priority_from_labels(["urgent"]) == "critical"
        assert _infer_priority_from_labels(["p0"]) == "critical"

    def test_infer_priority_high(self):
        """Infers high priority."""
        assert _infer_priority_from_labels(["high-priority"]) == "high"
        assert _infer_priority_from_labels(["important"]) == "high"
        assert _infer_priority_from_labels(["p1"]) == "high"

    def test_infer_priority_low(self):
        """Infers low priority."""
        assert _infer_priority_from_labels(["low-priority"]) == "low"
        assert _infer_priority_from_labels(["nice-to-have"]) == "low"

    def test_infer_priority_normal(self):
        """Defaults to normal priority."""
        assert _infer_priority_from_labels(["bug"]) == "normal"
        assert _infer_priority_from_labels([]) == "normal"
