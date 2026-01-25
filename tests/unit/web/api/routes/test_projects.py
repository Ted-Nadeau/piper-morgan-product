"""
Tests for projects API routes.

Issue #672: MUX-WIRE-PROJECTS-PAGE - Ensures /projects endpoint
falls back to user preferences when projects table is empty.
"""

from dataclasses import dataclass
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@dataclass
class MockJWTClaims:
    """Minimal JWT claims mock for testing."""

    sub: str
    user_id: str = None
    user_email: str = "test@example.com"

    def __post_init__(self):
        if self.user_id is None:
            self.user_id = self.sub


class TestProjectsListRoute:
    """Tests for GET /api/v1/projects endpoint."""

    @pytest.fixture
    def mock_current_user(self):
        """Create mock JWT claims for authenticated user."""
        user_id = str(uuid4())
        return MockJWTClaims(sub=user_id)

    @pytest.fixture
    def mock_project(self, mock_current_user):
        """Create a mock project domain object."""
        project = MagicMock()
        project.id = str(uuid4())
        project.name = "Test Project"
        project.description = "A test project"
        project.owner_id = mock_current_user.sub
        project.created_at = None
        return project

    @pytest.fixture
    def mock_project_repo(self):
        """Create a mock project repository."""
        repo = MagicMock()
        repo.list_active_projects = AsyncMock(return_value=[])
        return repo

    @pytest.mark.smoke
    def test_list_projects_from_database(self, mock_current_user, mock_project, mock_project_repo):
        """Test that projects are returned from database when available."""
        from services.auth.auth_middleware import get_current_user
        from web.api.dependencies import get_project_repository
        from web.api.routes.projects import router

        # Configure mock to return a project
        mock_project_repo.list_active_projects = AsyncMock(return_value=[mock_project])

        # Create test app with mocked dependencies
        app = FastAPI()
        app.include_router(router)

        app.dependency_overrides[get_current_user] = lambda: mock_current_user
        app.dependency_overrides[get_project_repository] = lambda: mock_project_repo

        client = TestClient(app)

        response = client.get("/api/v1/projects")

        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 1
        assert data["projects"][0]["name"] == "Test Project"
        assert data["source"] == "database"

    @pytest.mark.smoke
    def test_list_projects_fallback_to_preferences(self, mock_current_user, mock_project_repo):
        """Test that projects fall back to user preferences when DB is empty - Issue #672."""
        from unittest.mock import patch

        from services.auth.auth_middleware import get_current_user
        from web.api.dependencies import get_project_repository
        from web.api.routes.projects import router

        # Mock empty database
        mock_project_repo.list_active_projects = AsyncMock(return_value=[])

        # Mock user context with projects from preferences
        mock_user_context = MagicMock()
        mock_user_context.projects = ["Project A", "Project B", "Project C"]

        # Create test app
        app = FastAPI()
        app.include_router(router)

        app.dependency_overrides[get_current_user] = lambda: mock_current_user
        app.dependency_overrides[get_project_repository] = lambda: mock_project_repo

        client = TestClient(app)

        with patch(
            "services.user_context_service.user_context_service.get_user_context",
            new_callable=AsyncMock,
            return_value=mock_user_context,
        ):
            response = client.get("/api/v1/projects")

        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 3
        assert data["source"] == "preferences"
        # Check project names
        names = [p["name"] for p in data["projects"]]
        assert "Project A" in names
        assert "Project B" in names
        assert "Project C" in names

    @pytest.mark.smoke
    def test_list_projects_empty_when_no_fallback(self, mock_current_user, mock_project_repo):
        """Test that empty list is returned when both DB and preferences are empty."""
        from unittest.mock import patch

        from services.auth.auth_middleware import get_current_user
        from web.api.dependencies import get_project_repository
        from web.api.routes.projects import router

        # Mock empty database
        mock_project_repo.list_active_projects = AsyncMock(return_value=[])

        # Mock user context with no projects
        mock_user_context = MagicMock()
        mock_user_context.projects = []

        # Create test app
        app = FastAPI()
        app.include_router(router)

        app.dependency_overrides[get_current_user] = lambda: mock_current_user
        app.dependency_overrides[get_project_repository] = lambda: mock_project_repo

        client = TestClient(app)

        with patch(
            "services.user_context_service.user_context_service.get_user_context",
            new_callable=AsyncMock,
            return_value=mock_user_context,
        ):
            response = client.get("/api/v1/projects")

        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 0
        assert data["projects"] == []
        # source is "database" because we didn't convert any preferences
        assert data["source"] == "database"

    @pytest.mark.smoke
    def test_database_projects_take_precedence(
        self, mock_current_user, mock_project, mock_project_repo
    ):
        """Test that database projects are used over preferences when both exist."""
        from unittest.mock import patch

        from services.auth.auth_middleware import get_current_user
        from web.api.dependencies import get_project_repository
        from web.api.routes.projects import router

        # Mock database with project
        mock_project_repo.list_active_projects = AsyncMock(return_value=[mock_project])

        # Mock user context with different projects (should be ignored)
        mock_user_context = MagicMock()
        mock_user_context.projects = ["Preference Project"]

        # Create test app
        app = FastAPI()
        app.include_router(router)

        app.dependency_overrides[get_current_user] = lambda: mock_current_user
        app.dependency_overrides[get_project_repository] = lambda: mock_project_repo

        client = TestClient(app)

        with patch(
            "services.user_context_service.user_context_service.get_user_context",
            new_callable=AsyncMock,
            return_value=mock_user_context,
        ):
            response = client.get("/api/v1/projects")

        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 1
        assert data["source"] == "database"
        assert data["projects"][0]["name"] == "Test Project"
