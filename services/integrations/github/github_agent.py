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
