"""
GitHub API Connection Integration Tests — Issue #914

These tests verify that the GitHub API is reachable and the configured token
has the required scopes. They run ONLY when GITHUB_TOKEN is available
(loaded from keychain or environment by conftest.py).

To store a GitHub token in keychain:
    from services.infrastructure.keychain_service import get_keychain_service
    keychain = get_keychain_service()
    keychain.store_api_key("github_token", "ghp_your_token_here")

Required token scopes: repo (read/write for issue operations)
"""

import os

import aiohttp
import pytest

GITHUB_API_BASE = "https://api.github.com"

pytestmark = [pytest.mark.github, pytest.mark.integration]


@pytest.fixture
def github_token():
    """Get GitHub token from environment (loaded by conftest from keychain)."""
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        pytest.skip("GITHUB_TOKEN not available")
    return token


@pytest.fixture
def test_repo():
    """Get test repository for GitHub API tests."""
    return os.environ.get("GITHUB_DEFAULT_REPO", "mediajunkie/test-piper-morgan")


class TestGitHubAPIConnection:
    """Verify GitHub API connectivity and token validity."""

    @pytest.mark.asyncio
    async def test_token_authenticates_successfully(self, github_token):
        """Token should authenticate against GitHub API."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{GITHUB_API_BASE}/user",
                headers={
                    "Authorization": f"token {github_token}",
                    "Accept": "application/vnd.github.v3+json",
                },
            ) as resp:
                assert resp.status == 200, (
                    f"GitHub authentication failed (HTTP {resp.status}). "
                    "Check token validity and scopes."
                )
                data = await resp.json()
                assert "login" in data, "Response missing 'login' field"
                print(f"  [github] Authenticated as: {data['login']}")

    @pytest.mark.asyncio
    async def test_token_has_repo_scope(self, github_token):
        """Token should have 'repo' scope for issue operations."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{GITHUB_API_BASE}/user",
                headers={
                    "Authorization": f"token {github_token}",
                    "Accept": "application/vnd.github.v3+json",
                },
            ) as resp:
                assert resp.status == 200
                scopes = resp.headers.get("X-OAuth-Scopes", "")
                # 'repo' scope includes issue read/write
                assert "repo" in scopes, (
                    f"Token missing 'repo' scope. Current scopes: '{scopes}'. "
                    "Create token at: https://github.com/settings/tokens "
                    "with 'repo' scope enabled."
                )

    @pytest.mark.asyncio
    async def test_can_access_configured_repo(self, github_token, test_repo):
        """Token should be able to access the configured test repository."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{GITHUB_API_BASE}/repos/{test_repo}",
                headers={
                    "Authorization": f"token {github_token}",
                    "Accept": "application/vnd.github.v3+json",
                },
            ) as resp:
                assert resp.status == 200, (
                    f"Cannot access repo '{test_repo}' (HTTP {resp.status}). "
                    "Set GITHUB_DEFAULT_REPO to a repo the token can access."
                )
                data = await resp.json()
                print(f"  [github] Repo accessible: {data['full_name']}")

    @pytest.mark.asyncio
    async def test_can_list_issues(self, github_token, test_repo):
        """Token should be able to list issues on the configured repo."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{GITHUB_API_BASE}/repos/{test_repo}/issues",
                headers={
                    "Authorization": f"token {github_token}",
                    "Accept": "application/vnd.github.v3+json",
                },
                params={"state": "open", "per_page": 1},
            ) as resp:
                assert resp.status == 200, (
                    f"Cannot list issues on '{test_repo}' (HTTP {resp.status}). "
                    "Token may lack 'repo' scope."
                )
                # Just verify we got a list back (may be empty)
                data = await resp.json()
                assert isinstance(data, list)


class TestGitHubTokenFromKeychain:
    """Verify the keychain → env var loading pipeline works."""

    def test_github_token_is_available(self, github_token):
        """GITHUB_TOKEN should be loaded (from keychain or env)."""
        assert github_token, "GITHUB_TOKEN is empty"
        # Verify it looks like a GitHub token
        assert github_token.startswith(("ghp_", "github_pat_", "gho_")), (
            f"Token doesn't match expected GitHub token format "
            f"(starts with '{github_token[:4]}...'). "
            "Expected 'ghp_', 'github_pat_', or 'gho_' prefix."
        )
