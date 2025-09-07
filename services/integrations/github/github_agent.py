"""
GitHub Agent - Extended for PM-008: Issue Analysis
Adds issue fetching and URL parsing capabilities
"""

import os
import re
from typing import Any, Dict, List, Optional, Tuple

from github import (
    BadCredentialsException,
    Github,
    RateLimitExceededException,
    UnknownObjectException,
)
from github.Issue import Issue as GitHubIssue
from github.Repository import Repository

from services.api.errors import GitHubAuthFailedError, GitHubRateLimitError
from services.config.github_config import GitHubConfiguration
from services.configuration.piper_config_loader import PiperConfigLoader


class GitHubAgent:
    """GitHub API operations for issue management and analysis"""

    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GitHub token required - set GITHUB_TOKEN environment variable")

        try:
            self.client = Github(self.token)
            self.user = self.client.get_user()
        except BadCredentialsException as e:
            raise GitHubAuthFailedError(details={"reason": "Invalid GitHub token provided."}) from e

    def parse_github_url(self, url: str) -> Optional[Tuple[str, str, int]]:
        """
        Parse GitHub issue URL to extract owner, repo, and issue number

        Supports formats:
        - https://github.com/owner/repo/issues/123
        - github.com/owner/repo/issues/123
        - https://github.com/owner/repo/pull/123 (PRs are also issues)

        Returns:
            Tuple of (owner, repo, issue_number) or None if invalid
        """
        # Remove protocol and www if present
        clean_url = url.strip().lower()
        clean_url = re.sub(r"^https?://", "", clean_url)
        clean_url = re.sub(r"^www\.", "", clean_url)

        # Match GitHub issue/PR URL pattern
        pattern = r"github\.com/([^/]+)/([^/]+)/(?:issues|pull)/(\d+)"
        match = re.match(pattern, clean_url)

        if match:
            owner, repo, issue_num = match.groups()
            return (owner, repo, int(issue_num))

        return None

    async def get_issue_by_url(self, url: str) -> Dict[str, Any]:
        """
        Fetch GitHub issue by URL, raising exceptions on failure.
        """
        parsed = self.parse_github_url(url)
        if not parsed:
            raise ValueError(
                "Invalid GitHub URL format. Expected: https://github.com/owner/repo/issues/123"
            )

        owner, repo, issue_number = parsed
        return await self.get_issue(f"{owner}/{repo}", issue_number)

    async def get_issue(self, repo_name: str, issue_number: int) -> Dict[str, Any]:
        """
        Fetch GitHub issue, raising exceptions on failure.
        """
        try:
            repo = self.client.get_repo(repo_name)
            issue = repo.get_issue(issue_number)

            labels = [label.name for label in issue.labels]
            assignees = [assignee.login for assignee in issue.assignees]

            return {
                "id": issue.id,
                "number": issue.number,
                "title": issue.title,
                "body": issue.body or "",
                "state": issue.state,
                "labels": labels,
                "assignees": assignees,
                "created_at": issue.created_at.isoformat(),
                "updated_at": issue.updated_at.isoformat(),
                "url": issue.html_url,
                "user": {"login": issue.user.login, "name": issue.user.name},
                "repository": {
                    "name": repo.name,
                    "full_name": repo.full_name,
                    "private": repo.private,
                },
                "comments_count": issue.comments,
                "is_pull_request": issue.pull_request is not None,
            }
        except BadCredentialsException as e:
            raise GitHubAuthFailedError() from e
        except RateLimitExceededException as e:
            retry_after = e.headers.get("Retry-After", 60)  # Default to 60 seconds
            raise GitHubRateLimitError(retry_after=int(retry_after) // 60) from e
        except UnknownObjectException as e:
            raise ValueError(
                f"GitHub resource not found: {repo_name} or issue #{issue_number}"
            ) from e
        except Exception as e:
            # For other unexpected GitHub errors
            raise ConnectionError(f"An unexpected error occurred with the GitHub API: {e}") from e

    def list_repositories(self) -> List[Dict[str, Any]]:
        """List accessible repositories"""
        repos = []
        for repo in self.user.get_repos():
            repos.append(
                {
                    "name": repo.name,
                    "full_name": repo.full_name,
                    "private": repo.private,
                    "url": repo.html_url,
                }
            )
        return repos

    async def create_issue(
        self, repo_name: str, title: str, body: str, labels: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Create a GitHub issue, raising exceptions on failure."""
        try:
            repo = self.client.get_repo(repo_name)
            issue = repo.create_issue(title=title, body=body, labels=labels or [])

            return {
                "id": issue.id,
                "number": issue.number,
                "title": issue.title,
                "url": issue.html_url,
                "state": issue.state,
            }
        except BadCredentialsException as e:
            raise GitHubAuthFailedError() from e
        except RateLimitExceededException as e:
            retry_after = e.headers.get("Retry-After", 60)
            raise GitHubRateLimitError(retry_after=int(retry_after) // 60) from e
        except Exception as e:
            raise ConnectionError(f"Failed to create GitHub issue: {e}") from e

    async def create_issue_from_work_item(
        self, repo_name: str, work_item: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create GitHub issue from WorkItem domain model"""
        try:
            # Extract work item data
            title = work_item.get("title", "")
            description = work_item.get("description", "")
            labels = work_item.get("labels", [])
            assignee = work_item.get("assignee")

            # Validate required fields
            if not title:
                raise ValueError("WorkItem must have a title")

            # Create the issue
            repo = self.client.get_repo(repo_name)
            issue = repo.create_issue(title=title, body=description, labels=labels or [])

            # Add assignee if specified
            if assignee:
                try:
                    issue.add_to_assignees(assignee)
                except Exception as e:
                    # Log but don't fail the whole operation
                    print(f"Warning: Could not assign issue to {assignee}: {str(e)}")

            # Return result with additional work item context
            return {
                "id": issue.id,
                "number": issue.number,
                "title": issue.title,
                "url": issue.html_url,
                "state": issue.state,
                "work_item_id": work_item.get("id"),
                "work_item_type": work_item.get("type"),
                "work_item_priority": work_item.get("priority"),
                "labels": labels,
            }
        except BadCredentialsException as e:
            raise GitHubAuthFailedError() from e
        except RateLimitExceededException as e:
            retry_after = e.headers.get("Retry-After", 60)
            raise GitHubRateLimitError(retry_after=int(retry_after) // 60) from e
        except Exception as e:
            raise ConnectionError(f"Failed to create GitHub issue from work item: {e}") from e

    async def get_open_issues(
        self, project: Optional[str] = None, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get open issues from GitHub repository"""
        try:
            # Default to configured repository if no project specified
            config_loader = PiperConfigLoader()
            github_config = config_loader.load_github_config()
            repo_name = project or github_config.default_repository
            repo = self.client.get_repo(repo_name)

            issues = repo.get_issues(state="open", sort="updated", direction="desc")

            result = []
            count = 0
            for issue in issues:
                if count >= limit:
                    break

                # Skip pull requests (they appear as issues in GitHub API)
                if issue.pull_request:
                    continue

                labels = [label.name for label in issue.labels]
                assignee = (
                    {"login": issue.assignee.login, "name": issue.assignee.name}
                    if issue.assignee
                    else None
                )

                result.append(
                    {
                        "number": issue.number,
                        "title": issue.title,
                        "state": issue.state,
                        "labels": labels,
                        "assignee": assignee,
                        "created_at": issue.created_at.isoformat(),
                        "updated_at": issue.updated_at.isoformat(),
                        "url": issue.html_url,
                        "body": issue.body or "",
                    }
                )
                count += 1

            return result

        except Exception as e:
            raise ConnectionError(f"Failed to get open issues: {e}") from e

    async def get_recent_issues(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent issues (both open and closed) from GitHub repository"""
        try:
            config_loader = PiperConfigLoader()
            github_config = config_loader.load_github_config()
            repo_name = github_config.default_repository
            repo = self.client.get_repo(repo_name)

            issues = repo.get_issues(state="all", sort="updated", direction="desc")

            result = []
            count = 0
            for issue in issues:
                if count >= limit:
                    break

                # Skip pull requests
                if issue.pull_request:
                    continue

                labels = [label.name for label in issue.labels]
                assignee = (
                    {"login": issue.assignee.login, "name": issue.assignee.name}
                    if issue.assignee
                    else None
                )

                result.append(
                    {
                        "number": issue.number,
                        "title": issue.title,
                        "state": issue.state,
                        "labels": labels,
                        "assignee": assignee,
                        "created_at": issue.created_at.isoformat(),
                        "updated_at": issue.updated_at.isoformat(),
                        "url": issue.html_url,
                    }
                )
                count += 1

            return result

        except Exception as e:
            raise ConnectionError(f"Failed to get recent issues: {e}") from e

    async def get_issues_by_priority(self) -> List[Dict[str, Any]]:
        """Get issues filtered by priority labels"""
        try:
            config_loader = PiperConfigLoader()
            github_config = config_loader.load_github_config()
            repo_name = github_config.default_repository
            repo = self.client.get_repo(repo_name)

            # Get issues with priority labels
            issues = repo.get_issues(
                state="all",
                labels=["P0-critical", "P1-high", "P2-medium"],
                sort="updated",
                direction="desc",
            )

            result = []
            for issue in issues:
                # Skip pull requests
                if issue.pull_request:
                    continue

                labels = [label.name for label in issue.labels]
                assignee = (
                    {"login": issue.assignee.login, "name": issue.assignee.name}
                    if issue.assignee
                    else None
                )

                result.append(
                    {
                        "number": issue.number,
                        "title": issue.title,
                        "state": issue.state,
                        "labels": labels,
                        "assignee": assignee,
                        "created_at": issue.created_at.isoformat(),
                        "updated_at": issue.updated_at.isoformat(),
                        "url": issue.html_url,
                    }
                )

            return result

        except Exception as e:
            raise ConnectionError(f"Failed to get issues by priority: {e}") from e

    async def get_development_context(self) -> Dict[str, Any]:
        """Get development context including PRs, reviews, and commits"""
        try:
            config_loader = PiperConfigLoader()
            github_config = config_loader.load_github_config()
            repo_name = github_config.default_repository
            repo = self.client.get_repo(repo_name)

            # Get open pull requests
            open_prs = list(repo.get_pulls(state="open"))

            # Get recent commits (last 10)
            commits = list(repo.get_commits()[:10])

            # Count pending reviews (approximate by open PRs without reviews)
            pending_reviews = 0
            for pr in open_prs:
                reviews = list(pr.get_reviews())
                if not reviews:
                    pending_reviews += 1

            return {
                "active_prs": len(open_prs),
                "pending_reviews": pending_reviews,
                "recent_commits": len(commits),
            }

        except Exception as e:
            return {
                "active_prs": 0,
                "pending_reviews": 0,
                "recent_commits": 0,
                "error": f"Failed to get development context: {e}",
            }

    async def get_closed_issues(
        self, project: Optional[str] = None, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get recently closed issues from GitHub repository"""
        try:
            # Default to configured repository if no project specified
            config_loader = PiperConfigLoader()
            github_config = config_loader.load_github_config()
            repo_name = project or github_config.default_repository
            repo = self.client.get_repo(repo_name)

            issues = repo.get_issues(state="closed", sort="updated", direction="desc")

            result = []
            count = 0
            for issue in issues:
                if count >= limit:
                    break

                # Skip pull requests
                if issue.pull_request:
                    continue

                labels = [label.name for label in issue.labels]
                assignee = (
                    {"login": issue.assignee.login, "name": issue.assignee.name}
                    if issue.assignee
                    else None
                )

                result.append(
                    {
                        "number": issue.number,
                        "title": issue.title,
                        "state": issue.state,
                        "labels": labels,
                        "assignee": assignee,
                        "created_at": issue.created_at.isoformat(),
                        "updated_at": issue.updated_at.isoformat(),
                        "closed_at": issue.closed_at.isoformat() if issue.closed_at else None,
                        "url": issue.html_url,
                    }
                )
                count += 1

            return result

        except Exception as e:
            raise ConnectionError(f"Failed to get closed issues: {e}") from e

    def test_connection(self) -> Dict[str, Any]:
        """Test GitHub API connection, raising exceptions on failure."""
        try:
            user = self.client.get_user()
            return {
                "success": True,  # Keep success for simple health checks
                "user": user.login,
                "name": user.name,
                "repos_count": user.public_repos,
            }
        except (BadCredentialsException, RateLimitExceededException) as e:
            raise GitHubAuthFailedError(details={"reason": str(e)}) from e
        except Exception as e:
            raise ConnectionError(f"GitHub connection test failed: {e}") from e

    async def create_pm_issue(
        self,
        repo_name: str,
        pm_number: str,
        title: str,
        body: str,
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Create a GitHub issue with PM number integration.

        This method creates an issue and returns both GitHub and PM tracking information.
        The title should include the PM number (e.g., "PM-140: Feature Title").

        Args:
            repo_name: GitHub repository name (owner/repo)
            pm_number: PM number (e.g., "PM-140")
            title: Issue title including PM number
            body: Issue description/body
            labels: List of label names to apply
            assignees: List of usernames to assign

        Returns:
            Dictionary with GitHub issue details and PM tracking info
        """
        try:
            repo = self.client.get_repo(repo_name)

            # Create the issue
            issue = repo.create_issue(
                title=title, body=body, labels=labels or [], assignees=assignees or []
            )

            # Return enhanced result with PM tracking information
            return {
                "id": issue.id,
                "number": issue.number,
                "title": issue.title,
                "body": issue.body or "",
                "url": issue.html_url,
                "state": issue.state,
                "labels": [label.name for label in issue.labels],
                "assignees": [assignee.login for assignee in issue.assignees],
                "created_at": issue.created_at.isoformat(),
                "pm_number": pm_number,
                "pm_tracking": {
                    "pm_number": pm_number,
                    "github_issue": issue.number,
                    "title_includes_pm": pm_number in title,
                    "created_via_pm_command": True,
                },
            }
        except BadCredentialsException as e:
            raise GitHubAuthFailedError() from e
        except RateLimitExceededException as e:
            retry_after = e.headers.get("Retry-After", 60)
            raise GitHubRateLimitError(retry_after=int(retry_after) // 60) from e
        except Exception as e:
            raise ConnectionError(f"Failed to create PM issue {pm_number}: {e}") from e

    async def get_recent_activity(self, days: int = 7) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get recent GitHub activity for standup (commits, PRs, issues)

        Args:
            days: Number of days to look back for activity

        Returns:
            Dict with keys: commits, prs, issues_closed, issues_created
        """
        try:
            from datetime import datetime, timedelta

            config_loader = PiperConfigLoader()
            github_config = config_loader.load_github_config()
            repo_name = github_config.default_repository
            repo = self.client.get_repo(repo_name)

            since = datetime.now() - timedelta(days=days)

            # Get recent commits
            commits = []
            try:
                recent_commits = repo.get_commits(since=since)
                for commit in list(recent_commits)[:10]:  # Limit to 10 commits
                    commits.append(
                        {
                            "sha": commit.sha[:8],
                            "message": commit.commit.message.split("\n")[0],  # First line only
                            "author": commit.commit.author.name,
                            "date": commit.commit.author.date.isoformat(),
                            "url": commit.html_url,
                        }
                    )
            except Exception as e:
                print(f"Warning: Could not fetch commits: {e}")

            # Get recent pull requests
            prs = []
            try:
                recent_prs = repo.get_pulls(state="all", sort="updated", direction="desc")
                for pr in list(recent_prs)[:5]:  # Limit to 5 PRs
                    if pr.updated_at >= since:
                        prs.append(
                            {
                                "number": pr.number,
                                "title": pr.title,
                                "state": pr.state,
                                "author": pr.user.login,
                                "updated_at": pr.updated_at.isoformat(),
                                "url": pr.html_url,
                            }
                        )
            except Exception as e:
                print(f"Warning: Could not fetch PRs: {e}")

            # Get recent issues (created and closed)
            issues_created = []
            issues_closed = []
            try:
                recent_issues = repo.get_issues(state="all", sort="updated", direction="desc")
                for issue in list(recent_issues)[:10]:  # Limit to 10 issues
                    if issue.pull_request:  # Skip PRs (they appear as issues too)
                        continue

                    issue_data = {
                        "number": issue.number,
                        "title": issue.title,
                        "state": issue.state,
                        "author": issue.user.login,
                        "created_at": issue.created_at.isoformat(),
                        "url": issue.html_url,
                    }

                    if issue.created_at >= since:
                        issues_created.append(issue_data)
                    if issue.closed_at and issue.closed_at >= since:
                        issues_closed.append(issue_data)
            except Exception as e:
                print(f"Warning: Could not fetch issues: {e}")

            return {
                "commits": commits,
                "prs": prs,
                "issues_closed": issues_closed,
                "issues_created": issues_created,
            }

        except Exception as e:
            print(f"GitHub activity error: {e}")
            return {"commits": [], "prs": [], "issues_closed": [], "issues_created": []}
