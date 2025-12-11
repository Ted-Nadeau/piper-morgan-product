"""
Unit Tests for Create Endpoint API Contract (Issue #468)

These tests verify that create endpoints accept JSON body (not query params).

TDD: These tests are written FIRST and MUST FAIL against current code.

The bug: Backend endpoints define parameters like `name: str` which FastAPI
interprets as query parameters, but the frontend sends JSON body.

Frontend sends:
    POST /api/v1/lists
    Content-Type: application/json
    {"name": "My List", "description": "Optional"}

Backend currently expects (WRONG):
    POST /api/v1/lists?name=My%20List&description=Optional

These tests mock the repository to isolate the API contract issue from
database connectivity issues.

Run with: pytest tests/unit/web/api/routes/test_create_endpoints_contract.py -xvs
"""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from services.auth.jwt_service import JWTClaims


@pytest.fixture
def mock_current_user():
    """Mock authenticated user for route tests"""
    user_id = uuid4()
    return JWTClaims(
        iss="piper-morgan",
        aud="piper-morgan-api",
        sub=str(user_id),
        exp=9999999999,
        iat=1000000000,
        jti=str(uuid4()),
        user_id=user_id,
        user_email="test@example.com",
        scopes=["user"],
        token_type="access",
        session_id=None,
        workspace_id=None,
    )


@pytest.fixture
def mock_list_repository():
    """Mock list repository to avoid database issues"""
    mock_repo = AsyncMock()
    mock_repo.create_list = AsyncMock(
        return_value=MagicMock(
            id=str(uuid4()),
            name="Test List",
            description="Test Description",
            owner_id=str(uuid4()),
            created_at=None,
        )
    )
    mock_repo.get_lists_by_owner = AsyncMock(return_value=[])
    return mock_repo


@pytest.mark.unit
class TestListCreateContract:
    """
    Tests for POST /api/v1/lists API contract (Issue #468)

    These tests verify the endpoint accepts JSON body, not query params.
    """

    @pytest.mark.smoke
    def test_create_list_accepts_json_body(self, mock_current_user, mock_list_repository):
        """
        POST /api/v1/lists must accept JSON body with name and description.

        This is the core test for Issue #468. The frontend sends:
            body: JSON.stringify({ name, description })

        Current behavior: 422 Unprocessable Entity (expects query params)
        Expected behavior: 200 OK with created list
        """
        from fastapi import FastAPI

        from services.auth.auth_middleware import get_current_user
        from web.api.dependencies import get_list_repository
        from web.api.routes.lists import create_list, router

        # Create test app with mocked dependencies
        # Router already has prefix="/api/v1/lists", don't add it again
        app = FastAPI()
        app.include_router(router)

        # Override dependencies
        app.dependency_overrides[get_current_user] = lambda: mock_current_user
        app.dependency_overrides[get_list_repository] = lambda: mock_list_repository

        client = TestClient(app)

        # This is exactly what the frontend sends
        response = client.post(
            "/api/v1/lists", json={"name": "Test List", "description": "Created via JSON body"}
        )

        # MUST FAIL with current code (422 expected, proving the bug)
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}. "
            f"Response: {response.json()}. "
            "This proves Issue #468: endpoint expects query params but frontend sends JSON body."
        )

    @pytest.mark.smoke
    def test_create_list_name_only_json(self, mock_current_user, mock_list_repository):
        """
        POST /api/v1/lists with only name in JSON body (description optional).
        """
        from fastapi import FastAPI

        from services.auth.auth_middleware import get_current_user
        from web.api.dependencies import get_list_repository
        from web.api.routes.lists import router

        # Router already has prefix="/api/v1/lists"
        app = FastAPI()
        app.include_router(router)

        app.dependency_overrides[get_current_user] = lambda: mock_current_user
        app.dependency_overrides[get_list_repository] = lambda: mock_list_repository

        client = TestClient(app)

        response = client.post("/api/v1/lists", json={"name": "Minimal List"})

        assert (
            response.status_code == 200
        ), f"Expected 200, got {response.status_code}. Response: {response.json()}"


@pytest.mark.unit
class TestTodoCreateContract:
    """
    Tests for POST /api/v1/todos API contract (Issue #468)
    """

    @pytest.mark.smoke
    def test_create_todo_accepts_json_body(self, mock_current_user):
        """
        POST /api/v1/todos must accept JSON body with title and description.
        """
        from fastapi import FastAPI

        from services.auth.auth_middleware import get_current_user
        from web.api.dependencies import get_todo_repository
        from web.api.routes.todos import router

        # Mock todo repository
        mock_repo = AsyncMock()
        mock_repo.create_todo = AsyncMock(
            return_value=MagicMock(
                id=str(uuid4()),
                title="Test Todo",
                description="Test Description",
                owner_id=str(uuid4()),
                status="pending",
                priority="medium",
                created_at=None,
                due_date=None,
                list_id=None,
            )
        )

        # Router already has prefix="/api/v1/todos"
        app = FastAPI()
        app.include_router(router)

        app.dependency_overrides[get_current_user] = lambda: mock_current_user
        app.dependency_overrides[get_todo_repository] = lambda: mock_repo

        client = TestClient(app)

        response = client.post(
            "/api/v1/todos", json={"title": "Test Todo", "description": "Created via JSON body"}
        )

        # MUST FAIL with current code (proves the bug)
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}. "
            f"Response: {response.json()}. "
            "This proves Issue #468: endpoint expects query params but frontend sends JSON body."
        )


@pytest.mark.unit
class TestProjectCreateContract:
    """
    Tests for POST /api/v1/projects API contract (Issue #468)
    """

    @pytest.mark.smoke
    def test_create_project_accepts_json_body(self, mock_current_user):
        """
        POST /api/v1/projects must accept JSON body with name and description.
        """
        from fastapi import FastAPI

        from services.auth.auth_middleware import get_current_user
        from web.api.dependencies import get_project_repository
        from web.api.routes.projects import router

        # Mock project repository
        mock_repo = AsyncMock()
        mock_repo.create_project = AsyncMock(
            return_value=MagicMock(
                id=str(uuid4()),
                name="Test Project",
                description="Test Description",
                owner_id=str(uuid4()),
                created_at=None,
            )
        )

        # Router already has prefix="/api/v1/projects"
        app = FastAPI()
        app.include_router(router)

        app.dependency_overrides[get_current_user] = lambda: mock_current_user
        app.dependency_overrides[get_project_repository] = lambda: mock_repo

        client = TestClient(app)

        response = client.post(
            "/api/v1/projects",
            json={"name": "Test Project", "description": "Created via JSON body"},
        )

        # MUST FAIL with current code (proves the bug)
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}. "
            f"Response: {response.json()}. "
            "This proves Issue #468: endpoint expects query params but frontend sends JSON body."
        )
