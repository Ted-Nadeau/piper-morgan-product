"""
Unit tests for Repository and ProjectRepositoryLink domain models.
Issue #866: Repository as first-class domain entity.
"""

from datetime import datetime

import pytest

from services.domain.models import Project, ProjectIntegration, ProjectRepositoryLink, Repository
from services.shared_types import IntegrationType

pytestmark = pytest.mark.unit


class TestRepositoryDomainModel:
    """Tests for Repository dataclass."""

    def test_repository_creation_defaults(self):
        """Should create with sensible defaults."""
        repo = Repository(
            owner_id="user-1",
            full_name="mediajunkie/piper-morgan-product",
        )
        assert repo.id  # UUID generated
        assert repo.provider == "github"
        assert repo.full_name == "mediajunkie/piper-morgan-product"
        assert repo.display_name == "piper-morgan-product"  # Auto-derived
        assert repo.is_active is True
        assert isinstance(repo.created_at, datetime)

    def test_repository_display_name_auto_derives(self):
        """Should derive display_name from full_name."""
        repo = Repository(full_name="org/my-awesome-repo")
        assert repo.display_name == "my-awesome-repo"

    def test_repository_display_name_explicit(self):
        """Should use explicit display_name when provided."""
        repo = Repository(
            full_name="org/repo",
            display_name="My Custom Name",
        )
        assert repo.display_name == "My Custom Name"

    def test_repository_display_name_no_slash(self):
        """Should handle full_name without slash."""
        repo = Repository(full_name="solo-repo")
        assert repo.display_name == "solo-repo"

    def test_repository_to_dict(self):
        """Should serialize to dict correctly."""
        repo = Repository(
            id="repo-1",
            owner_id="user-1",
            provider="github",
            full_name="owner/repo",
            url="https://github.com/owner/repo",
        )
        d = repo.to_dict()
        assert d["id"] == "repo-1"
        assert d["owner_id"] == "user-1"
        assert d["provider"] == "github"
        assert d["full_name"] == "owner/repo"
        assert d["url"] == "https://github.com/owner/repo"
        assert d["is_active"] is True
        assert "created_at" in d
        assert "updated_at" in d


class TestProjectRepositoryLinkDomainModel:
    """Tests for ProjectRepositoryLink dataclass."""

    def test_link_creation(self):
        """Should create with defaults."""
        link = ProjectRepositoryLink(
            project_id="proj-1",
            repository_id="repo-1",
            linked_by="user-1",
        )
        assert link.id  # UUID generated
        assert link.project_id == "proj-1"
        assert link.repository_id == "repo-1"
        assert link.is_primary is False
        assert link.linked_by == "user-1"

    def test_link_to_dict(self):
        """Should serialize to dict correctly."""
        link = ProjectRepositoryLink(
            id="link-1",
            project_id="proj-1",
            repository_id="repo-1",
            is_primary=True,
            linked_by="user-1",
        )
        d = link.to_dict()
        assert d["id"] == "link-1"
        assert d["is_primary"] is True
        assert "linked_at" in d


class TestProjectGetGithubRepositoryDualPath:
    """Tests for updated Project.get_github_repository() with #866 dual path."""

    def test_get_github_repository_from_repositories_list(self):
        """Should find repo via the new Repository entities."""
        project = Project(
            name="Test",
            repositories=[
                Repository(
                    provider="github",
                    full_name="owner/backend",
                    is_active=True,
                ),
            ],
        )
        assert project.get_github_repository() == "owner/backend"

    def test_get_github_repository_fallback_to_integration(self):
        """Should fall back to ProjectIntegration config when no Repository entities."""
        project = Project(
            name="Test",
            integrations=[
                ProjectIntegration(
                    type=IntegrationType.GITHUB,
                    config={"repository": "owner/legacy-repo"},
                    is_active=True,
                ),
            ],
        )
        assert project.get_github_repository() == "owner/legacy-repo"

    def test_get_github_repository_prefers_repository_over_integration(self):
        """New Repository entities should take priority over legacy integration."""
        project = Project(
            name="Test",
            repositories=[
                Repository(
                    provider="github",
                    full_name="owner/new-repo",
                    is_active=True,
                ),
            ],
            integrations=[
                ProjectIntegration(
                    type=IntegrationType.GITHUB,
                    config={"repository": "owner/old-repo"},
                    is_active=True,
                ),
            ],
        )
        assert project.get_github_repository() == "owner/new-repo"

    def test_get_github_repository_skips_inactive_repos(self):
        """Should skip inactive Repository entities."""
        project = Project(
            name="Test",
            repositories=[
                Repository(
                    provider="github",
                    full_name="owner/inactive-repo",
                    is_active=False,
                ),
            ],
            integrations=[
                ProjectIntegration(
                    type=IntegrationType.GITHUB,
                    config={"repository": "owner/active-integration"},
                    is_active=True,
                ),
            ],
        )
        assert project.get_github_repository() == "owner/active-integration"

    def test_get_github_repository_skips_non_github_providers(self):
        """Should only match github provider repos."""
        project = Project(
            name="Test",
            repositories=[
                Repository(
                    provider="gitlab",
                    full_name="owner/gitlab-repo",
                    is_active=True,
                ),
            ],
        )
        assert project.get_github_repository() is None

    def test_project_to_dict_includes_repositories(self):
        """Project.to_dict() should include repositories array."""
        project = Project(
            name="Test",
            repositories=[
                Repository(
                    id="repo-1",
                    provider="github",
                    full_name="owner/repo",
                ),
            ],
        )
        d = project.to_dict()
        assert "repositories" in d
        assert len(d["repositories"]) == 1
        assert d["repositories"][0]["id"] == "repo-1"
