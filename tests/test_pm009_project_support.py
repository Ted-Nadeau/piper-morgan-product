# tests/test_pm009_project_support.py
"""
Test-first specification for PM-009 multi-project support.
These tests define the complete behavior expected from the implementation.
"""
import pytest
from unittest.mock import Mock, AsyncMock
from datetime import datetime
from uuid import uuid4

# Domain imports (these will need to be implemented)
from services.project_context import ProjectContext, AmbiguousProjectError, ProjectNotFoundError
from services.domain.models import Project, ProjectIntegration, Intent, IntentCategory
from services.database.repositories import ProjectRepository
from services.shared_types import IntegrationType, WorkflowType, WorkflowStatus

class TestProjectDomainModel:
    """Test the Project domain model behaves correctly"""
    
    def test_project_creation_with_defaults(self):
        """Project should initialize with sensible defaults"""
        project = Project(name="Mobile App", description="iOS and Android apps")
        
        assert project.id is not None
        assert project.name == "Mobile App"
        assert project.description == "iOS and Android apps"
        assert project.is_default is False
        assert project.is_archived is False
        assert len(project.integrations) == 0
        assert isinstance(project.created_at, datetime)
    
    def test_get_github_integration(self):
        """Should retrieve GitHub integration when present"""
        # GIVEN: Project with GitHub integration
        project = Project(name="Test Project")
        github_integration = ProjectIntegration(
            type=IntegrationType.GITHUB,
            name="Main Repo",
            config={"repository": "owner/repo"}
        )
        project.integrations.append(github_integration)
        
        # WHEN: Getting GitHub integration
        integration = project.get_integration(IntegrationType.GITHUB)
        
        # THEN: Should return the integration
        assert integration is not None
        assert integration.type == IntegrationType.GITHUB
        assert integration.config["repository"] == "owner/repo"
    
    def test_get_github_repository_shortcut(self):
        """Should provide easy access to GitHub repository"""
        # GIVEN: Project with GitHub integration
        project = Project(name="Test Project")
        project.integrations.append(ProjectIntegration(
            type=IntegrationType.GITHUB,
            name="Main Repo",
            config={"repository": "mediajunkie/piper-morgan-test"}
        ))
        
        # WHEN/THEN: Should return repository directly
        assert project.get_github_repository() == "mediajunkie/piper-morgan-test"
    
    def test_validate_integrations(self):
        """Should validate all integration configurations"""
        # GIVEN: Project with valid and invalid integrations
        project = Project(name="Test Project")
        
        # Valid GitHub integration
        project.integrations.append(ProjectIntegration(
            type=IntegrationType.GITHUB,
            name="Valid GitHub",
            config={"repository": "owner/repo"}
        ))
        
        # Invalid GitHub integration (missing repository)
        project.integrations.append(ProjectIntegration(
            type=IntegrationType.GITHUB,
            name="Invalid GitHub",
            config={}
        ))
        
        # WHEN: Validating integrations
        errors = project.validate_integrations()
        
        # THEN: Should report invalid integration
        assert len(errors) == 1
        assert "github" in errors[0].lower()


class TestProjectContext:
    """Test ProjectContext resolution logic"""
    
    @pytest.fixture
    def mock_repo(self):
        """Provides a mock ProjectRepository"""
        repo = Mock(spec=ProjectRepository)
        repo.get_by_id = AsyncMock()
        repo.get_default_project = AsyncMock()
        repo.list_active_projects = AsyncMock()
        repo.count_active_projects = AsyncMock()
        repo.find_by_name = AsyncMock()
        return repo
    
    @pytest.fixture
    def mock_llm(self):
        """Provides a mock LLM client"""
        llm = Mock()
        llm.complete = AsyncMock()
        return llm
    
    @pytest.mark.asyncio
    async def test_explicit_project_id_takes_precedence(self, mock_repo, mock_llm):
        """Explicit project ID should always win"""
        # GIVEN: Intent with explicit project_id
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_ticket",
            context={"project_id": "explicit-123"}
        )
        
        # AND: Repository returns the project
        expected_project = Project(id="explicit-123", name="Explicit Project")
        mock_repo.get_by_id.return_value = expected_project
        
        # WHEN: Resolving project
        context = ProjectContext(mock_repo, mock_llm)
        project, needs_confirmation = await context.resolve_project(
            intent, session_id="test-session"
        )
        
        # THEN: Should return explicit project without confirmation
        assert project.id == "explicit-123"
        assert project.name == "Explicit Project"
        assert needs_confirmation is False
        mock_repo.get_by_id.assert_called_once_with("explicit-123")
    
    @pytest.mark.asyncio
    async def test_uses_last_project_from_session(self, mock_repo, mock_llm):
        """Should remember and use last project from session"""
        # GIVEN: Previous project selection in session
        context = ProjectContext(mock_repo, mock_llm)
        context._session_last_used["session-1"] = "last-used-123"
        
        # AND: Intent without project specification
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_ticket",
            context={"original_message": "Create a bug ticket"}
        )
        
        # AND: Repository returns the last used project
        last_project = Project(id="last-used-123", name="Last Used Project")
        mock_repo.get_by_id.return_value = last_project
        
        # WHEN: Resolving with confirmed session
        project, needs_confirmation = await context.resolve_project(
            intent, session_id="session-1", confirmed_this_session=True
        )
        
        # THEN: Should use last project without confirmation
        assert project.id == "last-used-123"
        assert needs_confirmation is False
    
    @pytest.mark.asyncio
    async def test_infers_project_from_message_context(self, mock_repo, mock_llm):
        """Should use LLM to infer project from message"""
        # GIVEN: Intent mentioning a project
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_ticket",
            context={"original_message": "Bug in the mobile app login"}
        )
        
        # AND: Multiple projects exist
        projects = [
            Project(id="web-123", name="Web Platform", description="Main website"),
            Project(id="mobile-123", name="Mobile App", description="iOS and Android")
        ]
        mock_repo.list_active_projects.return_value = projects
        
        # AND: LLM identifies the mobile project
        mock_llm.complete.return_value = "Mobile App"
        
        # WHEN: Resolving project
        context = ProjectContext(mock_repo, mock_llm)
        project, needs_confirmation = await context.resolve_project(
            intent, session_id="new-session"
        )
        
        # THEN: Should return mobile project
        assert project.name == "Mobile App"
        assert project.id == "mobile-123"
    
    @pytest.mark.asyncio
    async def test_needs_confirmation_when_ambiguous(self, mock_repo, mock_llm):
        """Should request confirmation when project is ambiguous"""
        # GIVEN: Session has different project than inferred
        context = ProjectContext(mock_repo, mock_llm)
        context._session_last_used["session-1"] = "project-1"
        
        # Mock the last used project
        last_project = Project(id="project-1", name="Web App")
        mock_repo.get_by_id.return_value = last_project
        
        # AND: Message suggests different project
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_ticket",
            context={"original_message": "Critical bug in mobile app"}
        )
        
        # Mock inference returning different project
        inferred_project = Project(id="project-2", name="Mobile App")
        mock_repo.list_active_projects.return_value = [last_project, inferred_project]
        mock_llm.complete.return_value = "Mobile App"
        
        # WHEN: Resolving without confirmation
        project, needs_confirmation = await context.resolve_project(
            intent, session_id="session-1", confirmed_this_session=False
        )
        
        # THEN: Should return inferred project but need confirmation
        assert project.name == "Mobile App"
        assert needs_confirmation is True
    
    @pytest.mark.asyncio
    async def test_falls_back_to_default_project(self, mock_repo, mock_llm):
        """Should use default project when no other context available"""
        # GIVEN: No session history or context
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_ticket",
            context={"original_message": "Create a ticket"}
        )
        
        # AND: Only one project exists (the default)
        mock_repo.count_active_projects.return_value = 1
        default_project = Project(id="default-123", name="Default Project", is_default=True)
        mock_repo.get_default_project.return_value = default_project
        
        # WHEN: Resolving project
        context = ProjectContext(mock_repo, mock_llm)
        project, needs_confirmation = await context.resolve_project(
            intent, session_id="new-session"
        )
        
        # THEN: Should return default without confirmation
        assert project.id == "default-123"
        assert project.is_default is True
        assert needs_confirmation is False
    
    @pytest.mark.asyncio
    async def test_raises_ambiguous_error_when_unclear(self, mock_repo, mock_llm):
        """Should raise error when can't determine project among many"""
        # GIVEN: Multiple projects exist
        mock_repo.count_active_projects.return_value = 3
        
        # AND: No context to determine which one
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_ticket",
            context={"original_message": "Create a ticket"}
        )
        
        # AND: No inference possible
        mock_repo.list_active_projects.return_value = [
            Project(name="Project A"),
            Project(name="Project B"),
            Project(name="Project C")
        ]
        mock_llm.complete.return_value = "UNCLEAR"
        
        # WHEN/THEN: Should raise AmbiguousProjectError
        context = ProjectContext(mock_repo, mock_llm)
        with pytest.raises(AmbiguousProjectError) as exc_info:
            await context.resolve_project(intent, session_id="new-session")
        
        assert "Multiple projects available" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_handles_project_not_found_error(self, mock_repo, mock_llm):
        """Should handle gracefully when explicit project doesn't exist"""
        # GIVEN: Intent with non-existent project_id
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_ticket",
            context={"project_id": "non-existent-123"}
        )
        
        # AND: Repository returns None (not found)
        mock_repo.get_by_id.return_value = None
        
        # WHEN/THEN: Should raise clear error
        context = ProjectContext(mock_repo, mock_llm)
        with pytest.raises(ProjectNotFoundError) as exc_info:
            await context.resolve_project(intent, session_id="test-session")
        
        assert "non-existent-123" in str(exc_info.value)
        assert "not found" in str(exc_info.value).lower()


class TestWorkflowFactoryIntegration:
    """Test WorkflowFactory creates workflows with project context"""
    
    @pytest.mark.asyncio
    async def test_workflow_includes_project_context(self):
        """Created workflow should include full project context"""
        # GIVEN: Intent and project
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_github_issue",
            context={"original_message": "Bug report"}
        )
        
        project = Project(id="proj-123", name="Test Project")
        project.integrations.append(ProjectIntegration(
            type=IntegrationType.GITHUB,
            name="Main Repo",
            config={"repository": "owner/repo", "default_labels": ["bug"]}
        ))
        
        # AND: Mock context that returns project
        mock_context = Mock(spec=ProjectContext)
        mock_context.resolve_project = AsyncMock(return_value=(project, False))
        
        # Import after mocks are set up
        from services.orchestration.workflow_factory import WorkflowFactory
        
        # WHEN: Creating workflow
        factory = WorkflowFactory(project_context=mock_context)
        workflow = await factory.create_from_intent(intent, session_id="test")
        
        # THEN: Workflow should have project context
        assert workflow is not None
        assert workflow.context["project_id"] == "proj-123"
        assert workflow.context["project_name"] == "Test Project"
        assert "github" in workflow.context["project_integrations"]
        assert workflow.context["project_integrations"]["github"]["repository"] == "owner/repo"


class TestGitHubAgentProjectIntegration:
    """Test GitHub agent uses project configuration"""
    
    @pytest.mark.asyncio
    async def test_uses_project_github_configuration(self):
        """Should use repository and labels from project config"""
        # This is more of an integration test but important for PM-009
        from services.domain.models import Workflow
        
        # GIVEN: Workflow with project context
        workflow = Workflow(
            type=WorkflowType.CREATE_TICKET,
            status=WorkflowStatus.PENDING,
            context={
                "project_id": "proj-123",
                "project_name": "Mobile App",
                "project_integrations": {
                    "github": {
                        "repository": "mediajunkie/mobile-app",
                        "default_labels": ["mobile", "ai-generated"]
                    }
                }
            }
        )
        
        # AND: Issue data
        issue_data = {
            "title": "Login crash on iOS",
            "body": "Users report app crashes when logging in",
            "labels": ["bug"]
        }
        
        # WHEN: GitHub agent processes the workflow
        # (This would be mocked in a unit test, but shows expected behavior)
        # The agent should:
        # 1. Extract repository from workflow context
        # 2. Merge default labels with issue labels
        # 3. Create issue in correct repository
        
        # Expected behavior to test:
        # - Repository: "mediajunkie/mobile-app" (from project)
        # - Labels: ["bug", "mobile", "ai-generated"] (merged)


# Anti-pattern prevention tests
class TestNoHardcodedValues:
    """Ensure implementation follows patterns"""
    
    def test_uses_enum_not_strings_for_integration_type(self):
        """Must use IntegrationType enum, not string literals"""
        # This is a meta-test that would inspect the actual implementation
        # Include it to prevent "if integration.type == 'github':" anti-pattern
        pass
    
    def test_repository_pattern_for_database_operations(self):
        """Database operations must go through repositories"""
        # Ensure ProjectContext doesn't directly use SQLAlchemy
        # Should only use ProjectRepository methods
        pass