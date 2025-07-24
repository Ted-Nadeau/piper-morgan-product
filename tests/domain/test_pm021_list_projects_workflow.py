"""
Test-first specification for PM-021 LIST_PROJECTS workflow.
Tests the complete workflow from natural language to project listing.
"""

from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

import pytest

from services.database.repositories import ProjectRepository
from services.domain.models import Intent, IntentCategory, Project, ProjectIntegration
from services.orchestration.engine import OrchestrationEngine
from services.orchestration.workflow_factory import WorkflowFactory
from services.shared_types import (
    IntegrationType,
    TaskStatus,
    TaskType,
    WorkflowStatus,
    WorkflowType,
)


@pytest.fixture
def mock_project_repository():
    """Mock project repository for testing"""
    repo = Mock()
    repo.list_active_projects = AsyncMock()
    repo.get_all = AsyncMock()
    return repo


@pytest.fixture
def sample_projects():
    """Sample projects for testing"""
    return [
        Project(
            id="project-1",
            name="Test Project 1",
            description="First test project",
            is_default=True,
            integrations=[
                ProjectIntegration(
                    type=IntegrationType.GITHUB,
                    name="Main Repository",
                    config={"repository": "test-org/test-repo-1"},
                )
            ],
        ),
        Project(
            id="project-2",
            name="Test Project 2",
            description="Second test project",
            is_default=False,
            integrations=[
                ProjectIntegration(
                    type=IntegrationType.GITHUB,
                    name="Secondary Repository",
                    config={"repository": "test-org/test-repo-2"},
                )
            ],
        ),
    ]


class TestPM021ListProjectsWorkflow:
    """Test PM-021 LIST_PROJECTS workflow implementation"""

    @pytest.mark.asyncio
    async def test_workflow_factory_creates_list_projects_workflow(self):
        """Test that WorkflowFactory creates correct LIST_PROJECTS workflow"""
        # Arrange
        factory = WorkflowFactory()
        intent = Intent(
            action="list_projects",
            category=IntentCategory.QUERY,
            context={"original_message": "list all projects"},
        )

        # Act
        workflow = await factory.create_from_intent(intent)

        # Assert
        assert workflow is not None
        assert workflow.type == WorkflowType.LIST_PROJECTS
        assert workflow.status == WorkflowStatus.PENDING
        assert len(workflow.tasks) == 1
        assert workflow.tasks[0].type == TaskType.LIST_PROJECTS
        assert workflow.tasks[0].name == "List Projects"
        assert workflow.tasks[0].status == TaskStatus.PENDING

    @pytest.mark.asyncio
    async def test_list_projects_workflow_execution(self, mock_project_repository, sample_projects):
        """Test complete workflow execution for listing projects"""
        # Arrange
        mock_project_repository.list_active_projects.return_value = sample_projects

        factory = WorkflowFactory()
        engine = OrchestrationEngine()

        intent = Intent(
            action="list_projects",
            category=IntentCategory.QUERY,
            context={"original_message": "show me all projects"},
        )

        # Create workflow
        workflow = await factory.create_from_intent(intent)
        engine.workflows[workflow.id] = workflow

        # Act
        with patch(
            "services.database.repositories.ProjectRepository", return_value=mock_project_repository
        ):
            result = await engine.execute_workflow(workflow.id)

        # Assert
        assert result["status"] == "completed"
        assert "projects" in result["context"]
        assert len(result["context"]["projects"]) == 2

        # Verify project data structure
        project1 = result["context"]["projects"][0]
        assert project1["name"] == "Test Project 1"
        assert project1["is_default"] is True
        assert len(project1["integrations"]) == 1

    @pytest.mark.asyncio
    async def test_list_projects_empty_result(self, mock_project_repository):
        """Test workflow execution when no projects exist"""
        # Arrange
        mock_project_repository.list_active_projects.return_value = []

        factory = WorkflowFactory()
        engine = OrchestrationEngine()

        intent = Intent(
            action="list_projects",
            category=IntentCategory.QUERY,
            context={"original_message": "list projects"},
        )

        # Create workflow
        workflow = await factory.create_from_intent(intent)
        engine.workflows[workflow.id] = workflow

        # Act
        with patch(
            "services.database.repositories.ProjectRepository", return_value=mock_project_repository
        ):
            result = await engine.execute_workflow(workflow.id)

        # Assert
        assert result["status"] == "completed"
        assert "projects" in result["context"]
        assert result["context"]["projects"] == []

    @pytest.mark.asyncio
    async def test_list_projects_intent_mapping(self):
        """Test that various intent actions map to LIST_PROJECTS workflow"""
        # Arrange
        factory = WorkflowFactory()

        test_cases = [
            ("list_projects", "list all projects"),
            ("list_all_projects", "show me all projects"),
            ("show_projects", "display projects"),
        ]

        # Act & Assert
        for action, message in test_cases:
            intent = Intent(
                action=action, category=IntentCategory.QUERY, context={"original_message": message}
            )

            workflow = await factory.create_from_intent(intent)
            assert workflow is not None
            assert workflow.type == WorkflowType.LIST_PROJECTS

    @pytest.mark.asyncio
    async def test_list_projects_error_handling(self, mock_project_repository):
        """Test error handling when project repository fails"""
        # Arrange
        mock_project_repository.list_active_projects.side_effect = Exception(
            "Database connection failed"
        )
        factory = WorkflowFactory()
        engine = OrchestrationEngine()
        intent = Intent(
            action="list_projects",
            category=IntentCategory.QUERY,
            context={"original_message": "list projects"},
        )
        workflow = await factory.create_from_intent(intent)
        engine.workflows[workflow.id] = workflow
        from services.api.errors import TaskFailedError

        with patch(
            "services.database.repositories.ProjectRepository", return_value=mock_project_repository
        ):
            with pytest.raises(TaskFailedError) as exc_info:
                await engine.execute_workflow(workflow.id)
            # Check the details dict for the original error message
            assert (
                "Project listing error: Database connection failed"
                in exc_info.value.details["error"]
            )

    @pytest.mark.asyncio
    async def test_list_projects_workflow_context_preservation(
        self, mock_project_repository, sample_projects
    ):
        """Test that workflow context is preserved during execution"""
        # Arrange
        mock_project_repository.list_active_projects.return_value = sample_projects

        factory = WorkflowFactory()
        engine = OrchestrationEngine()

        intent = Intent(
            action="list_projects",
            category=IntentCategory.QUERY,
            context={
                "original_message": "list all projects",
                "user_id": "test-user-123",
                "session_id": "session-456",
            },
        )

        # Create workflow
        workflow = await factory.create_from_intent(intent)
        engine.workflows[workflow.id] = workflow

        # Act
        with patch(
            "services.database.repositories.ProjectRepository", return_value=mock_project_repository
        ):
            result = await engine.execute_workflow(workflow.id)

        # Assert
        assert result["status"] == "completed"
        assert result["context"]["original_message"] == "list all projects"
        assert result["context"]["user_id"] == "test-user-123"
        assert result["context"]["session_id"] == "session-456"
