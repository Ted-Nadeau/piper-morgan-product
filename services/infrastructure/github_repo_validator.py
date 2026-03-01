"""
GitHub Repository Validator — soft validation via GitHub REST API.

Issue #867: Optionally validate repos exist and pull metadata when linking.
Soft validation: if token unavailable or API fails, warn but don't block.
"""

import os
from dataclasses import dataclass
from typing import Optional

import aiohttp
import structlog

logger = structlog.get_logger()

GITHUB_API_BASE = "https://api.github.com"


@dataclass
class RepoValidationResult:
    """Result of a GitHub API repo validation attempt."""

    validated: bool  # True if API call was attempted
    exists: bool  # True if repo was found (HTTP 200)
    accessible: bool  # True if token has read access
    error: Optional[str] = None
    # Metadata — populated only on success
    description: Optional[str] = None
    language: Optional[str] = None
    visibility: Optional[str] = None  # "public", "private", "internal"
    default_branch: Optional[str] = None

    @property
    def metadata_available(self) -> bool:
        """True if we got metadata from the API."""
        return self.validated and self.exists and self.accessible


def get_github_token() -> Optional[str]:
    """Resolve GitHub token from environment."""
    return os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")


async def validate_github_repo(
    full_name: str,
    token: Optional[str] = None,
) -> RepoValidationResult:
    """Validate a GitHub repo exists and pull metadata.

    Args:
        full_name: Repository in "owner/repo" format.
        token: GitHub token. If None, attempts to resolve from environment.
               If still None, returns unvalidated result (soft skip).

    Returns:
        RepoValidationResult with validation status and optional metadata.
    """
    resolved_token = token or get_github_token()

    if not resolved_token:
        logger.info("github_repo_validation_skipped", full_name=full_name, reason="no_token")
        return RepoValidationResult(validated=False, exists=False, accessible=False)

    url = f"{GITHUB_API_BASE}/repos/{full_name}"
    headers = {
        "Authorization": f"token {resolved_token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "piper-morgan",
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    logger.info(
                        "github_repo_validation_success",
                        full_name=full_name,
                        visibility=data.get("visibility"),
                    )
                    return RepoValidationResult(
                        validated=True,
                        exists=True,
                        accessible=True,
                        description=data.get("description"),
                        language=data.get("language"),
                        visibility=data.get("visibility"),
                        default_branch=data.get("default_branch"),
                    )
                elif resp.status == 404:
                    logger.warning("github_repo_validation_not_found", full_name=full_name)
                    return RepoValidationResult(
                        validated=True,
                        exists=False,
                        accessible=False,
                        error=f"Repository '{full_name}' not found on GitHub",
                    )
                elif resp.status == 401:
                    logger.warning("github_repo_validation_auth_failed", full_name=full_name)
                    return RepoValidationResult(
                        validated=True,
                        exists=False,
                        accessible=False,
                        error="GitHub token is invalid or expired",
                    )
                elif resp.status == 403:
                    logger.warning(
                        "github_repo_validation_forbidden",
                        full_name=full_name,
                        status=403,
                    )
                    return RepoValidationResult(
                        validated=True,
                        exists=True,
                        accessible=False,
                        error="GitHub API rate limit or insufficient permissions",
                    )
                else:
                    logger.warning(
                        "github_repo_validation_unexpected_status",
                        full_name=full_name,
                        status=resp.status,
                    )
                    return RepoValidationResult(
                        validated=True,
                        exists=False,
                        accessible=False,
                        error=f"GitHub API returned status {resp.status}",
                    )

    except aiohttp.ClientError as e:
        logger.warning("github_repo_validation_network_error", full_name=full_name, error=str(e))
        return RepoValidationResult(
            validated=False, exists=False, accessible=False, error=f"Network error: {e}"
        )
    except Exception as e:
        logger.error("github_repo_validation_unexpected_error", full_name=full_name, error=str(e))
        return RepoValidationResult(
            validated=False, exists=False, accessible=False, error=f"Unexpected error: {e}"
        )


def apply_validation_metadata(repo, result: RepoValidationResult):
    """Merge validated metadata into a Repository domain entity.

    Modifies the repo in place. Only applies metadata if the validation succeeded.
    """
    if result.metadata_available:
        repo.description = result.description
        repo.language = result.language
        repo.visibility = result.visibility
        repo.default_branch = result.default_branch
