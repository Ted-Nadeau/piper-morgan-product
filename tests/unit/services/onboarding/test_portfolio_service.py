"""
Tests for Portfolio Service.

Part of #569 MUX-INTERACT-PORTFOLIO-DEL.
Part of #567 MUX-INTERACT-CONV-SEARCH.

Tests cover:
- Archive project (soft delete)
- Restore archived project
- Permanent delete with confirmation
- Authorization (owner-only operations)
- Edge cases (not found, already archived, etc.)
- Conversation patterns for intent detection
- Search projects (partial match, typeahead)
"""

import re
from datetime import datetime
from typing import Dict, List, Optional
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from services.domain.models import Project
from services.onboarding.portfolio_service import (
    ARCHIVE_INSTEAD_PATTERNS,
    ARCHIVE_PATTERNS,
    DELETE_PATTERNS,
    PERMANENT_DELETE_PATTERNS,
    RESTORE_PATTERNS,
    PortfolioActionResult,
    PortfolioResult,
    PortfolioService,
)

# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def user_id():
    """Test user ID."""
    return str(uuid4())


@pytest.fixture
def other_user_id():
    """Different user ID for authorization tests."""
    return str(uuid4())


@pytest.fixture
def project(user_id):
    """A test project."""
    return Project(
        id=str(uuid4()),
        owner_id=user_id,
        name="HealthTrack",
        description="Fitness tracking app",
        is_archived=False,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture
def archived_project(user_id):
    """An archived test project."""
    return Project(
        id=str(uuid4()),
        owner_id=user_id,
        name="OldProject",
        description="An archived project",
        is_archived=True,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture
def mock_repository():
    """Mock project repository."""
    repo = MagicMock()
    repo.get_by_id = AsyncMock()
    repo.update = AsyncMock()
    repo.delete = AsyncMock()
    repo.list_active_projects = AsyncMock(return_value=[])
    repo.find_by_name = AsyncMock()
    repo.search_projects = AsyncMock(return_value=[])
    return repo


@pytest.fixture
def service(mock_repository):
    """Portfolio service with mock repository."""
    return PortfolioService(mock_repository)


# =============================================================================
# PortfolioResult Tests
# =============================================================================


class TestPortfolioResult:
    """Tests for PortfolioResult dataclass."""

    def test_success_property_true(self):
        """success property is True for SUCCESS status."""
        result = PortfolioResult(status=PortfolioActionResult.SUCCESS)
        assert result.success is True

    def test_success_property_false_for_other_statuses(self):
        """success property is False for non-SUCCESS statuses."""
        for status in PortfolioActionResult:
            if status != PortfolioActionResult.SUCCESS:
                result = PortfolioResult(status=status)
                assert result.success is False, f"Expected False for {status}"


# =============================================================================
# Archive Tests
# =============================================================================


class TestArchiveProject:
    """Tests for archive_project method."""

    async def test_archive_success(self, service, mock_repository, project, user_id):
        """Successfully archive an active project."""
        mock_repository.get_by_id.return_value = project

        # After update, return archived version
        archived = Project(**{**project.__dict__, "is_archived": True})
        mock_repository.get_by_id.side_effect = [project, archived]

        result = await service.archive_project(project.id, user_id)

        assert result.success is True
        assert result.status == PortfolioActionResult.SUCCESS
        assert "archived" in result.message.lower()
        assert project.name in result.message
        mock_repository.update.assert_called_once()

    async def test_archive_not_found(self, service, mock_repository, user_id):
        """Archive fails for non-existent project."""
        mock_repository.get_by_id.return_value = None

        result = await service.archive_project("nonexistent", user_id)

        assert result.success is False
        assert result.status == PortfolioActionResult.NOT_FOUND
        assert "couldn't find" in result.message.lower()

    async def test_archive_not_owner(self, service, mock_repository, project, other_user_id):
        """Archive fails if user doesn't own project."""
        mock_repository.get_by_id.return_value = project

        result = await service.archive_project(project.id, other_user_id)

        assert result.success is False
        assert result.status == PortfolioActionResult.NOT_OWNER
        assert "your own" in result.message.lower()

    async def test_archive_already_archived(
        self, service, mock_repository, archived_project, user_id
    ):
        """Archive fails if project is already archived."""
        mock_repository.get_by_id.return_value = archived_project

        result = await service.archive_project(archived_project.id, user_id)

        assert result.success is False
        assert result.status == PortfolioActionResult.ALREADY_ARCHIVED
        assert "already archived" in result.message.lower()


# =============================================================================
# Restore Tests
# =============================================================================


class TestRestoreProject:
    """Tests for restore_project method."""

    async def test_restore_success(self, service, mock_repository, archived_project, user_id):
        """Successfully restore an archived project."""
        mock_repository.get_by_id.return_value = archived_project

        # After update, return active version
        restored = Project(**{**archived_project.__dict__, "is_archived": False})
        mock_repository.get_by_id.side_effect = [archived_project, restored]

        result = await service.restore_project(archived_project.id, user_id)

        assert result.success is True
        assert result.status == PortfolioActionResult.SUCCESS
        assert "restored" in result.message.lower()
        mock_repository.update.assert_called_once()

    async def test_restore_not_found(self, service, mock_repository, user_id):
        """Restore fails for non-existent project."""
        mock_repository.get_by_id.return_value = None

        result = await service.restore_project("nonexistent", user_id)

        assert result.success is False
        assert result.status == PortfolioActionResult.NOT_FOUND

    async def test_restore_not_owner(
        self, service, mock_repository, archived_project, other_user_id
    ):
        """Restore fails if user doesn't own project."""
        mock_repository.get_by_id.return_value = archived_project

        result = await service.restore_project(archived_project.id, other_user_id)

        assert result.success is False
        assert result.status == PortfolioActionResult.NOT_OWNER

    async def test_restore_not_archived(self, service, mock_repository, project, user_id):
        """Restore fails if project is not archived."""
        mock_repository.get_by_id.return_value = project

        result = await service.restore_project(project.id, user_id)

        assert result.success is False
        assert result.status == PortfolioActionResult.NOT_ARCHIVED
        assert "isn't archived" in result.message.lower()


# =============================================================================
# Delete Tests
# =============================================================================


class TestDeleteProject:
    """Tests for delete_project method."""

    async def test_delete_requires_confirmation(self, service, mock_repository, project, user_id):
        """Delete without confirmation returns CONFIRMATION_REQUIRED."""
        mock_repository.get_by_id.return_value = project

        result = await service.delete_project(project.id, user_id, confirmed=False)

        assert result.success is False
        assert result.status == PortfolioActionResult.CONFIRMATION_REQUIRED
        assert "permanently delete" in result.message.lower()
        assert project.name in result.message
        assert "cannot be undone" in result.message.lower()
        mock_repository.delete.assert_not_called()

    async def test_delete_with_confirmation(self, service, mock_repository, project, user_id):
        """Delete with confirmation succeeds."""
        mock_repository.get_by_id.return_value = project

        result = await service.delete_project(project.id, user_id, confirmed=True)

        assert result.success is True
        assert result.status == PortfolioActionResult.SUCCESS
        assert "permanently deleted" in result.message.lower()
        assert project.name in result.message
        mock_repository.delete.assert_called_once_with(project.id)

    async def test_delete_not_found(self, service, mock_repository, user_id):
        """Delete fails for non-existent project."""
        mock_repository.get_by_id.return_value = None

        result = await service.delete_project("nonexistent", user_id, confirmed=True)

        assert result.success is False
        assert result.status == PortfolioActionResult.NOT_FOUND

    async def test_delete_not_owner(self, service, mock_repository, project, other_user_id):
        """Delete fails if user doesn't own project."""
        mock_repository.get_by_id.return_value = project

        result = await service.delete_project(project.id, other_user_id, confirmed=True)

        assert result.success is False
        assert result.status == PortfolioActionResult.NOT_OWNER

    async def test_confirmation_message_offers_archive_alternative(
        self, service, mock_repository, project, user_id
    ):
        """Confirmation message suggests archive as alternative."""
        mock_repository.get_by_id.return_value = project

        result = await service.delete_project(project.id, user_id, confirmed=False)

        assert "archive instead" in result.message.lower()


# =============================================================================
# Read Operation Tests
# =============================================================================


class TestReadOperations:
    """Tests for read operations."""

    async def test_get_project_success(self, service, mock_repository, project, user_id):
        """Get project returns project for owner."""
        mock_repository.get_by_id.return_value = project

        result = await service.get_project(project.id, user_id)

        assert result is not None
        assert result.id == project.id

    async def test_get_project_not_owner(self, service, mock_repository, project, other_user_id):
        """Get project returns None for non-owner."""
        mock_repository.get_by_id.return_value = project

        result = await service.get_project(project.id, other_user_id)

        assert result is None

    async def test_list_active_projects(self, service, mock_repository, project, user_id):
        """List active projects returns non-archived projects."""
        mock_repository.list_active_projects.return_value = [project]

        result = await service.list_active_projects(user_id)

        assert len(result) == 1
        assert result[0].id == project.id
        mock_repository.list_active_projects.assert_called_once_with(owner_id=user_id)

    async def test_find_project_by_name(self, service, mock_repository, project, user_id):
        """Find project by name works."""
        mock_repository.find_by_name.return_value = project

        result = await service.find_project_by_name("HealthTrack", user_id)

        assert result is not None
        assert result.name == "HealthTrack"

    async def test_find_excludes_archived_by_default(
        self, service, mock_repository, archived_project, user_id
    ):
        """Find by name excludes archived projects by default."""
        mock_repository.find_by_name.return_value = archived_project

        result = await service.find_project_by_name("OldProject", user_id)

        assert result is None

    async def test_find_includes_archived_when_requested(
        self, service, mock_repository, archived_project, user_id
    ):
        """Find by name includes archived when requested."""
        mock_repository.find_by_name.return_value = archived_project

        result = await service.find_project_by_name("OldProject", user_id, include_archived=True)

        assert result is not None
        assert result.name == "OldProject"


# =============================================================================
# Conversation Pattern Tests
# =============================================================================


class TestArchivePatterns:
    """Tests for archive intent detection patterns."""

    @pytest.mark.parametrize(
        "message,expected_project",
        [
            ("archive HealthTrack", "HealthTrack"),
            ("archive my project HealthTrack", "HealthTrack"),
            ("hide HealthTrack", "HealthTrack"),
            ("hide my project DataViz", "DataViz"),
            ("put HealthTrack away", "HealthTrack"),
            ("put DataViz aside", "DataViz"),
        ],
    )
    def test_archive_patterns_match(self, message, expected_project):
        """Archive patterns correctly extract project names."""
        matched = False
        for pattern in ARCHIVE_PATTERNS:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                assert match.group(1).strip() == expected_project
                matched = True
                break
        assert matched, f"No pattern matched: {message}"


class TestDeletePatterns:
    """Tests for delete intent detection patterns."""

    @pytest.mark.parametrize(
        "message,expected_project",
        [
            ("delete HealthTrack", "HealthTrack"),
            ("delete my project HealthTrack", "HealthTrack"),
            ("remove HealthTrack", "HealthTrack"),
            ("remove my project DataViz", "DataViz"),
            ("get rid of HealthTrack", "HealthTrack"),
        ],
    )
    def test_delete_patterns_match(self, message, expected_project):
        """Delete patterns correctly extract project names."""
        matched = False
        for pattern in DELETE_PATTERNS:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                assert match.group(1).strip() == expected_project
                matched = True
                break
        assert matched, f"No pattern matched: {message}"


class TestPermanentDeletePatterns:
    """Tests for permanent delete confirmation patterns."""

    @pytest.mark.parametrize(
        "message",
        [
            "permanently delete",
            "delete it forever",
            "yes, delete it",
            "yes delete it",
            "confirm delete",
        ],
    )
    def test_permanent_delete_patterns_match(self, message):
        """Permanent delete patterns match confirmation phrases."""
        matched = any(
            re.search(pattern, message, re.IGNORECASE) for pattern in PERMANENT_DELETE_PATTERNS
        )
        assert matched, f"No pattern matched: {message}"


class TestRestorePatterns:
    """Tests for restore intent detection patterns."""

    @pytest.mark.parametrize(
        "message,expected_project",
        [
            ("restore HealthTrack", "HealthTrack"),
            ("restore my project HealthTrack", "HealthTrack"),
            ("unarchive HealthTrack", "HealthTrack"),
            ("bring back HealthTrack", "HealthTrack"),
        ],
    )
    def test_restore_patterns_match(self, message, expected_project):
        """Restore patterns correctly extract project names."""
        matched = False
        for pattern in RESTORE_PATTERNS:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                assert match.group(1).strip() == expected_project
                matched = True
                break
        assert matched, f"No pattern matched: {message}"


class TestArchiveInsteadPatterns:
    """Tests for 'archive instead' response patterns."""

    @pytest.mark.parametrize(
        "message",
        [
            "archive instead",
            "just archive",
            "keep it recoverable",
        ],
    )
    def test_archive_instead_patterns_match(self, message):
        """Archive instead patterns match escape phrases."""
        matched = any(
            re.search(pattern, message, re.IGNORECASE) for pattern in ARCHIVE_INSTEAD_PATTERNS
        )
        assert matched, f"No pattern matched: {message}"


# =============================================================================
# Message Quality Tests (Consciousness-Preserving)
# =============================================================================


class TestMessageQuality:
    """Tests for consciousness-preserving message quality."""

    async def test_archive_message_is_reassuring(self, service, mock_repository, project, user_id):
        """Archive message reassures user it's recoverable."""
        mock_repository.get_by_id.return_value = project
        archived = Project(**{**project.__dict__, "is_archived": True})
        mock_repository.get_by_id.side_effect = [project, archived]

        result = await service.archive_project(project.id, user_id)

        assert "restore" in result.message.lower() or "anytime" in result.message.lower()

    async def test_restore_message_is_welcoming(
        self, service, mock_repository, archived_project, user_id
    ):
        """Restore message welcomes project back."""
        mock_repository.get_by_id.return_value = archived_project
        restored = Project(**{**archived_project.__dict__, "is_archived": False})
        mock_repository.get_by_id.side_effect = [archived_project, restored]

        result = await service.restore_project(archived_project.id, user_id)

        # Should feel warm, not transactional
        assert "welcome back" in result.message.lower() or "restored" in result.message.lower()

    async def test_delete_confirmation_is_clear_about_consequences(
        self, service, mock_repository, project, user_id
    ):
        """Delete confirmation clearly states irreversibility."""
        mock_repository.get_by_id.return_value = project

        result = await service.delete_project(project.id, user_id, confirmed=False)

        assert "cannot be undone" in result.message.lower()
        assert "permanently" in result.message.lower()


# =============================================================================
# Search Tests (#567 MUX-INTERACT-CONV-SEARCH)
# =============================================================================


class TestSearchProjects:
    """Tests for project search functionality (typeahead/partial match)."""

    async def test_search_partial_match(self, service, mock_repository, user_id):
        """Search finds projects by partial name match."""
        project1 = Project(
            id=str(uuid4()),
            owner_id=user_id,
            name="HealthTrack",
            description="Fitness app",
            is_archived=False,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        project2 = Project(
            id=str(uuid4()),
            owner_id=user_id,
            name="HealthDash",
            description="Health dashboard",
            is_archived=False,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        mock_repository.search_projects.return_value = [project1, project2]

        result = await service.search_projects("Health", user_id)

        assert len(result) == 2
        assert all("Health" in p.name for p in result)
        mock_repository.search_projects.assert_called_once_with(
            query="Health",
            owner_id=user_id,
            include_archived=False,
            limit=10,
        )

    async def test_search_empty_query_returns_active(
        self, service, mock_repository, project, user_id
    ):
        """Empty search query returns all active projects."""
        mock_repository.list_active_projects.return_value = [project]

        result = await service.search_projects("", user_id)

        assert len(result) == 1
        mock_repository.list_active_projects.assert_called_once_with(owner_id=user_id)

    async def test_search_whitespace_only_returns_active(
        self, service, mock_repository, project, user_id
    ):
        """Whitespace-only query returns all active projects."""
        mock_repository.list_active_projects.return_value = [project]

        result = await service.search_projects("   ", user_id)

        assert len(result) == 1

    async def test_search_excludes_archived_by_default(self, service, mock_repository, user_id):
        """Search excludes archived projects by default."""
        mock_repository.search_projects.return_value = []

        await service.search_projects("Health", user_id)

        mock_repository.search_projects.assert_called_once_with(
            query="Health",
            owner_id=user_id,
            include_archived=False,
            limit=10,
        )

    async def test_search_includes_archived_when_requested(self, service, mock_repository, user_id):
        """Search includes archived projects when requested."""
        mock_repository.search_projects.return_value = []

        await service.search_projects("Health", user_id, include_archived=True)

        mock_repository.search_projects.assert_called_once_with(
            query="Health",
            owner_id=user_id,
            include_archived=True,
            limit=10,
        )

    async def test_search_respects_limit(self, service, mock_repository, user_id):
        """Search respects the limit parameter."""
        mock_repository.search_projects.return_value = []

        await service.search_projects("Health", user_id, limit=5)

        mock_repository.search_projects.assert_called_once_with(
            query="Health",
            owner_id=user_id,
            include_archived=False,
            limit=5,
        )

    async def test_search_strips_query_whitespace(self, service, mock_repository, user_id):
        """Search strips leading/trailing whitespace from query."""
        mock_repository.search_projects.return_value = []

        await service.search_projects("  Health  ", user_id)

        mock_repository.search_projects.assert_called_once_with(
            query="Health",
            owner_id=user_id,
            include_archived=False,
            limit=10,
        )

    async def test_search_typeahead_style(self, service, mock_repository, user_id):
        """Search supports typeahead-style partial matching."""
        # Simulating user typing "He" then "Hea" then "Heal"
        project = Project(
            id=str(uuid4()),
            owner_id=user_id,
            name="HealthTrack",
            description="Fitness app",
            is_archived=False,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        mock_repository.search_projects.return_value = [project]

        # Each partial query should work
        for partial in ["He", "Hea", "Heal", "Health"]:
            result = await service.search_projects(partial, user_id)
            assert len(result) == 1

    async def test_empty_query_respects_limit(self, service, mock_repository, user_id):
        """Empty query with limit returns limited active projects."""
        projects = [
            Project(
                id=str(uuid4()),
                owner_id=user_id,
                name=f"Project{i}",
                description=f"Description {i}",
                is_archived=False,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            for i in range(20)
        ]
        mock_repository.list_active_projects.return_value = projects

        result = await service.search_projects("", user_id, limit=5)

        # Should return only first 5 projects
        assert len(result) == 5
