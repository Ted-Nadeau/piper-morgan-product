from unittest.mock import AsyncMock, Mock

import pytest

from services.domain.models import Intent, Project, ProjectIntegration
from services.orchestration.workflow_factory import WorkflowFactory
from services.shared_types import IntegrationType, IntentCategory


class TestWorkflowFactoryIntegration:
    """Test WorkflowFactory creates workflows with project context (per-call pattern)"""

    @pytest.mark.asyncio
    async def test_workflow_includes_project_context(self):
        """Created workflow should include full project context"""
        # GIVEN: Intent and project
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_github_issue",
            context={"original_message": "Bug report"},
        )

        project = Project(id="proj-123", name="Test Project")
        project.integrations.append(
            ProjectIntegration(
                type=IntegrationType.GITHUB,
                name="Main Repo",
                config={"repository": "owner/repo", "default_labels": ["bug"]},
            )
        )

        # AND: Mock context that returns project
        mock_context = Mock()
        mock_context.resolve_project = AsyncMock(return_value=(project, False))

        # WHEN: Creating workflow (per-call project_context)
        factory = WorkflowFactory()
        project_context = {
            "project_id": project.id,
            "project_name": project.name,
            "project_integrations": {
                "github": {"repository": "owner/repo", "default_labels": ["bug"]}
            },
        }
        workflow = await factory.create_from_intent(intent, project_context=project_context)

        # THEN: Workflow should have project context
        assert workflow is not None
        assert workflow.context["project_id"] == "proj-123"
        assert workflow.context["project_name"] == "Test Project"
        assert "github" in workflow.context["project_integrations"]
        assert workflow.context["project_integrations"]["github"]["repository"] == "owner/repo"
