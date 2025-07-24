"""
PM-012: Comprehensive Test Scenarios for Real GitHub Integration
Tests the complete production flow from natural language to GitHub issue creation
"""

import asyncio
import json
from typing import Any, Dict, Optional
from unittest.mock import AsyncMock, Mock, patch

import pytest

from services.api.errors import GitHubAuthFailedError, GitHubRateLimitError
from services.domain.models import Intent, Project, ProjectIntegration, Task, Workflow, WorkItem
from services.domain.work_item_extractor import WorkItemExtractor
from services.integrations.github.github_agent import GitHubAgent
from services.integrations.github.issue_generator import IssueContentGenerator
from services.orchestration.engine import OrchestrationEngine
from services.orchestration.workflow_factory import WorkflowFactory
from services.shared_types import (
    IntegrationType,
    IntentCategory,
    TaskStatus,
    TaskType,
    WorkflowType,
)


class TestPM012GitHubProductionScenarios:
    """Comprehensive test scenarios for real GitHub integration"""

    # ============================================================================
    async def create_and_store_workflow(self, intent, engine, project_context=None):
        """Helper function to create workflow and store it in engine registry"""
        factory = WorkflowFactory()
        workflow = await factory.create_from_intent(intent, project_context)
        engine.workflows[workflow.id] = workflow
        return workflow

    # FIXTURES
    # ============================================================================

    @pytest.fixture
    def mock_llm_client(self):
        """Mock LLM client for testing"""
        mock_client = Mock()
        mock_client.complete = AsyncMock()
        return mock_client

    @pytest.fixture
    def mock_github_agent(self):
        """Mock GitHub agent for testing"""
        mock_agent = Mock()
        mock_agent.create_issue_from_work_item = AsyncMock()
        mock_agent.create_issue = AsyncMock()
        mock_agent.test_connection = AsyncMock()
        return mock_agent

    @pytest.fixture
    def sample_project(self):
        """Sample project with GitHub integration"""
        github_integration = ProjectIntegration(
            type=IntegrationType.GITHUB,
            name="Main Repository",
            config={"repository": "test-org/test-repo"},
        )

        return Project(
            id="test-project-123",
            name="Test Project",
            description="A test project for GitHub integration",
            integrations=[github_integration],
            is_default=True,
        )

    @pytest.fixture
    def sample_work_item(self):
        """Sample work item for testing"""
        return WorkItem(
            id="test-work-item-123",
            title="Mobile App Login Crash",
            description="## Problem Description\nUsers are experiencing crashes when attempting to log in on mobile devices.\n\n## Steps to Reproduce\n1. Open mobile app\n2. Tap login button\n3. App crashes immediately\n\n## Expected Behavior\nUser should be able to log in successfully\n\n## Actual Behavior\nApp crashes with no error message",
            type="bug",
            priority="high",
            labels=["bug", "mobile", "login", "high-priority"],
            source_system="github",
            metadata={
                "original_prompt": "Create a bug ticket for login crash on mobile",
                "extraction_method": "llm",
            },
        )

    # ============================================================================
    # 1. HAPPY PATH TESTING
    # ============================================================================

    @pytest.mark.asyncio
    async def test_create_issue_from_natural_language(
        self, mock_llm_client, mock_github_agent, sample_project
    ):
        """Test: 'create a ticket for login bug with high priority'"""

        # Mock LLM response for work item extraction
        mock_llm_response = """{
            "title": "Mobile App Login Bug",
            "description": "## Problem Description\\nUsers are experiencing login failures on mobile devices.\\n\\n## Steps to Reproduce\\n1. Open mobile app\\n2. Enter credentials\\n3. Tap login\\n4. Error occurs\\n\\n## Expected Behavior\\nUser should be able to log in successfully\\n\\n## Actual Behavior\\nLogin fails with error message",
            "type": "bug",
            "priority": "high",
            "labels": ["bug", "mobile", "login", "high-priority"]
        }"""
        mock_llm_client.complete.return_value = mock_llm_response

        # Mock GitHub issue creation
        mock_github_agent.create_issue_from_work_item.return_value = {
            "id": 12345,
            "number": 42,
            "title": "Mobile App Login Bug",
            "url": "https://github.com/test-org/test-repo/issues/42",
            "state": "open",
            "work_item_id": "test-work-item-123",
            "work_item_type": "bug",
            "work_item_priority": "high",
            "labels": ["bug", "mobile", "login", "high-priority"],
        }

        # Create intent
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_ticket",
            context={
                "original_message": "create a ticket for login bug with high priority",
                "project_id": sample_project.id,
            },
        )

        # Create workflow factory and engine
        factory = WorkflowFactory()
        engine = OrchestrationEngine()

        # Mock the GitHub agent in the engine
        engine.github_agent = mock_github_agent

        # Create workflow
        workflow = await self.create_and_store_workflow(intent, engine, sample_project.to_dict())
        assert workflow is not None
        assert workflow.type == WorkflowType.CREATE_TICKET
        assert (
            len(workflow.tasks) == 3
        )  # EXTRACT_WORK_ITEM + GENERATE_GITHUB_ISSUE_CONTENT + GITHUB_CREATE_ISSUE

        # Execute workflow
        result = await engine.execute_workflow(workflow.id)

        # Verify success
        assert result["success"] is True
        assert "issue_number" in result["data"]
        assert "issue_url" in result["data"]
        assert result["data"]["issue_number"] == 42
        assert "github.com" in result["data"]["issue_url"]

        # Verify GitHub agent was called correctly
        mock_github_agent.create_issue_from_work_item.assert_called_once()
        call_args = mock_github_agent.create_issue_from_work_item.call_args
        assert call_args[1]["repo_name"] == "test-org/test-repo"

        work_item_arg = call_args[1]["work_item"]
        assert work_item_arg["title"] == "Mobile App Login Bug"
        assert work_item_arg["type"] == "bug"
        assert work_item_arg["priority"] == "high"

    @pytest.mark.asyncio
    async def test_issue_content_generation(self, mock_llm_client):
        """Test: Natural language → professional issue content"""

        # Mock LLM response for content generation
        mock_llm_response = """{
            "title": "Fix User Authentication Flow",
            "body": "## Description\\n\\nThe user authentication flow needs to be updated to support OAuth 2.0.\\n\\n## Acceptance Criteria\\n\\n- [ ] Implement OAuth 2.0 flow\\n- [ ] Add proper error handling\\n- [ ] Update documentation\\n\\n## Additional Context\\n\\nThis is part of the security enhancement initiative.",
            "labels": ["enhancement", "security", "authentication"]
        }"""
        mock_llm_client.complete.return_value = mock_llm_response

        # Create issue content generator
        generator = IssueContentGenerator()
        generator.llm_client = mock_llm_client  # Inject mock client

        # Test content generation
        description = "We need to fix the user authentication flow to support OAuth 2.0"
        context = {"repository": "test-org/test-repo", "user_impact": "Improved security"}

        content = await generator.generate_issue_content(description, context)

        # Verify professional content generation
        assert content.title == "Fix User Authentication Flow"
        assert "OAuth 2.0" in content.body
        assert "Acceptance Criteria" in content.body
        assert "enhancement" in content.labels
        assert "security" in content.labels

    @pytest.mark.asyncio
    async def test_complete_workflow_with_project_context(
        self, mock_llm_client, mock_github_agent, sample_project
    ):
        """Test complete workflow with project context and repository mapping"""

        # Mock LLM response
        mock_llm_response = """{
            "title": "Add Dark Mode Support",
            "description": "## Description\\n\\nUsers have requested dark mode support for the mobile app.\\n\\n## Requirements\\n\\n- Dark theme implementation\\n- Theme switching capability\\n- User preference storage\\n\\n## Acceptance Criteria\\n\\n- [ ] Dark mode works on all screens\\n- [ ] Users can toggle between light and dark\\n- [ ] Preference persists across app sessions",
            "type": "feature",
            "priority": "medium",
            "labels": ["feature", "ui", "mobile", "enhancement"]
        }"""
        mock_llm_client.complete.return_value = mock_llm_response

        # Mock GitHub issue creation
        mock_github_agent.create_issue_from_work_item.return_value = {
            "id": 12346,
            "number": 43,
            "title": "Add Dark Mode Support",
            "url": "https://github.com/test-org/test-repo/issues/43",
            "state": "open",
            "labels": ["feature", "ui", "mobile", "enhancement"],
        }

        # Create intent with project context
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_ticket",
            context={
                "original_message": "Add dark mode support to the mobile app",
                "project_id": sample_project.id,
            },
        )

        # Create and execute workflow
        factory = WorkflowFactory()
        engine = OrchestrationEngine()
        engine.github_agent = mock_github_agent

        workflow = await self.create_and_store_workflow(intent, engine, sample_project.to_dict())
        result = await engine.execute_workflow(workflow.id)

        # Verify success with project context
        assert result["success"] is True
        assert workflow.context["repository"] == "test-org/test-repo"
        assert workflow.context["project_id"] == sample_project.id

    # ============================================================================
    # 2. EDGE CASE COVERAGE
    # ============================================================================

    @pytest.mark.asyncio
    async def test_missing_project_context(self, mock_llm_client, mock_github_agent):
        """Test edge case: Missing project context"""

        # Mock LLM response
        mock_llm_response = """{
            "title": "Fix Login Bug",
            "description": "Users cannot log in",
            "type": "bug",
            "priority": "high",
            "labels": ["bug", "login"]
        }"""
        mock_llm_client.complete.return_value = mock_llm_response

        # Create intent without project context
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_ticket",
            context={
                "original_message": "Fix the login bug",
                "repository": "fallback-org/fallback-repo",  # Direct repository
            },
        )

        # Create and execute workflow
        factory = WorkflowFactory()
        engine = OrchestrationEngine()
        engine.github_agent = mock_github_agent

        workflow = await self.create_and_store_workflow(intent, engine)
        result = await engine.execute_workflow(workflow.id)

        # Should still work with direct repository specification
        assert result["success"] is True
        assert workflow.context["repository"] == "fallback-org/fallback-repo"

    @pytest.mark.asyncio
    async def test_malformed_user_request(self, mock_llm_client):
        """Test edge case: Malformed user requests"""

        # Test with very short/incomplete request
        short_prompt = "bug"

        # Mock LLM response for malformed input
        mock_llm_response = """{
            "title": "Bug Report",
            "description": "A bug was reported. Please provide more details.",
            "type": "bug",
            "priority": "medium",
            "labels": ["bug", "needs-info"]
        }"""
        mock_llm_client.complete.return_value = mock_llm_response

        extractor = WorkItemExtractor(mock_llm_client)
        work_item = await extractor.extract_from_prompt(short_prompt)

        # Should handle gracefully with defaults
        assert work_item.title == "Bug Report"
        assert work_item.type == "bug"
        assert work_item.priority == "medium"
        assert "needs-info" in work_item.labels

    @pytest.mark.asyncio
    async def test_special_characters_in_issue_content(self, mock_llm_client, mock_github_agent):
        """Test edge case: Special characters in issue content"""

        # Mock LLM response with special characters
        mock_llm_response = """{
            "title": "Fix SQL Injection in User Input",
            "description": "## Problem\\n\\nUser input like `'; DROP TABLE users; --` is not being sanitized.\\n\\n## Code Example\\n\\n```sql\\nSELECT * FROM users WHERE name = '${userInput}';\\n```\\n\\n## Expected\\n\\n```sql\\nSELECT * FROM users WHERE name = ?;\\n```",
            "type": "bug",
            "priority": "critical",
            "labels": ["bug", "security", "sql-injection", "critical"]
        }"""
        mock_llm_client.complete.return_value = mock_llm_response

        # Mock GitHub issue creation
        mock_github_agent.create_issue_from_work_item.return_value = {
            "id": 12347,
            "number": 44,
            "title": "Fix SQL Injection in User Input",
            "url": "https://github.com/test-org/test-repo/issues/44",
            "state": "open",
        }

        # Create intent with special characters
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_ticket",
            context={
                "original_message": "Fix SQL injection vulnerability in user input handling",
                "repository": "test-org/test-repo",
            },
        )

        # Create and execute workflow
        factory = WorkflowFactory()
        engine = OrchestrationEngine()
        engine.github_agent = mock_github_agent

        workflow = await self.create_and_store_workflow(intent, engine)
        result = await engine.execute_workflow(workflow.id)

        # Should handle special characters gracefully
        assert result["success"] is True

        # Verify GitHub agent received properly escaped content
        call_args = mock_github_agent.create_issue_from_work_item.call_args
        work_item_arg = call_args[1]["work_item"]
        assert "SQL Injection" in work_item_arg["title"]
        assert "DROP TABLE" in work_item_arg["description"]

    @pytest.mark.asyncio
    async def test_repository_resolution_edge_cases(self, mock_llm_client, mock_github_agent):
        """Test edge case: Repository resolution edge cases"""

        # Test with various repository formats
        test_cases = [
            "owner/repo",
            "owner/repo-name",
            "owner/repo_name",
            "owner/repo.name",
            "owner/repo-name.with.dots",
        ]

        for repo_name in test_cases:
            # Mock LLM response
            mock_llm_response = """{
                "title": "Test Issue",
                "description": "Test description",
                "type": "task",
                "priority": "medium",
                "labels": ["task"]
            }"""
            mock_llm_client.complete.return_value = mock_llm_response

            # Mock GitHub issue creation
            mock_github_agent.create_issue_from_work_item.return_value = {
                "id": 12348,
                "number": 45,
                "title": "Test Issue",
                "url": f"https://github.com/{repo_name}/issues/45",
                "state": "open",
            }

            # Create intent with repository
            intent = Intent(
                category=IntentCategory.EXECUTION,
                action="create_ticket",
                context={"original_message": "Create a test issue", "repository": repo_name},
            )

            # Create and execute workflow
            factory = WorkflowFactory()
            engine = OrchestrationEngine()
            engine.github_agent = mock_github_agent

            workflow = await self.create_and_store_workflow(intent, engine)
            result = await engine.execute_workflow(workflow.id)

            # Should handle all repository formats
            assert result["success"] is True
            assert workflow.context["repository"] == repo_name

    # ============================================================================
    # 3. ERROR SCENARIO TESTING
    # ============================================================================

    @pytest.mark.asyncio
    async def test_github_api_auth_failure(self, mock_llm_client, mock_github_agent):
        """Test error scenario: GitHub API authentication failure"""

        # Mock LLM response
        mock_llm_response = """{
            "title": "Test Issue",
            "description": "Test description",
            "type": "task",
            "priority": "medium",
            "labels": ["task"]
        }"""
        mock_llm_client.complete.return_value = mock_llm_response

        # Mock GitHub authentication failure
        mock_github_agent.create_issue_from_work_item.side_effect = GitHubAuthFailedError(
            details={"reason": "Invalid token"}
        )

        # Create intent
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_ticket",
            context={"original_message": "Create a test issue", "repository": "test-org/test-repo"},
        )

        # Create and execute workflow
        factory = WorkflowFactory()
        engine = OrchestrationEngine()
        engine.github_agent = mock_github_agent

        workflow = await self.create_and_store_workflow(intent, engine)
        result = await engine.execute_workflow(workflow.id)

        # Should handle authentication failure gracefully
        assert result["success"] is False
        assert "GitHub API error" in result["error"]
        assert "authentication" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_github_api_rate_limit(self, mock_llm_client, mock_github_agent):
        """Test error scenario: GitHub API rate limit exceeded"""

        # Mock LLM response
        mock_llm_response = """{
            "title": "Test Issue",
            "description": "Test description",
            "type": "task",
            "priority": "medium",
            "labels": ["task"]
        }"""
        mock_llm_client.complete.return_value = mock_llm_response

        # Mock GitHub rate limit error
        mock_github_agent.create_issue_from_work_item.side_effect = GitHubRateLimitError(
            retry_after=5
        )

        # Create intent
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_ticket",
            context={"original_message": "Create a test issue", "repository": "test-org/test-repo"},
        )

        # Create and execute workflow
        factory = WorkflowFactory()
        engine = OrchestrationEngine()
        engine.github_agent = mock_github_agent

        workflow = await self.create_and_store_workflow(intent, engine)
        result = await engine.execute_workflow(workflow.id)

        # Should handle rate limit gracefully
        assert result["success"] is False
        assert "GitHub API error" in result["error"]
        assert "rate limit" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_llm_service_unavailable(self, mock_llm_client, mock_github_agent):
        """Test error scenario: LLM service unavailable"""

        # Mock LLM service failure
        mock_llm_client.complete.side_effect = Exception("LLM service unavailable")

        # Create intent
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_ticket",
            context={
                "original_message": "Create a bug ticket for login crash",
                "repository": "test-org/test-repo",
            },
        )

        # Create and execute workflow
        factory = WorkflowFactory()
        engine = OrchestrationEngine()
        engine.github_agent = mock_github_agent

        workflow = await self.create_and_store_workflow(intent, engine)

        # Should use fallback extraction when LLM fails
        extractor = WorkItemExtractor(mock_llm_client)
        work_item = await extractor.extract_from_prompt("Create a bug ticket for login crash")

        # Verify fallback behavior
        assert work_item.metadata["extraction_method"] == "fallback"
        assert work_item.title == "Create a bug ticket for login crash"  # Uses original prompt
        assert work_item.type == "bug"  # Detects "bug" keyword
        assert work_item.priority == "medium"  # Default priority

    @pytest.mark.asyncio
    async def test_configuration_missing(self, mock_llm_client):
        """Test error scenario: Configuration missing"""

        # Test GitHub agent initialization without token
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError, match="GitHub token required"):
                GitHubAgent()

    @pytest.mark.asyncio
    async def test_repository_access_denied(self, mock_llm_client, mock_github_agent):
        """Test error scenario: Repository access denied"""

        # Mock LLM response
        mock_llm_response = """{
            "title": "Test Issue",
            "description": "Test description",
            "type": "task",
            "priority": "medium",
            "labels": ["task"]
        }"""
        mock_llm_client.complete.return_value = mock_llm_response

        # Mock repository access denied
        mock_github_agent.create_issue_from_work_item.side_effect = ValueError(
            "GitHub resource not found: test-org/private-repo or access denied"
        )

        # Create intent
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_ticket",
            context={
                "original_message": "Create a test issue",
                "repository": "test-org/private-repo",
            },
        )

        # Create and execute workflow
        factory = WorkflowFactory()
        engine = OrchestrationEngine()
        engine.github_agent = mock_github_agent

        workflow = await self.create_and_store_workflow(intent, engine)
        result = await engine.execute_workflow(workflow.id)

        # Should handle access denied gracefully
        assert result["success"] is False
        assert "GitHub API error" in result["error"]

    # ============================================================================
    # 4. INTEGRATION VALIDATION
    # ============================================================================

    @pytest.mark.asyncio
    async def test_project_context_repository_mapping(
        self, mock_llm_client, mock_github_agent, sample_project
    ):
        """Test integration: Project context → repository mapping"""

        # Mock LLM response
        mock_llm_response = """{
            "title": "Test Issue",
            "description": "Test description",
            "type": "task",
            "priority": "medium",
            "labels": ["task"]
        }"""
        mock_llm_client.complete.return_value = mock_llm_response

        # Mock GitHub issue creation
        mock_github_agent.create_issue_from_work_item.return_value = {
            "id": 12349,
            "number": 46,
            "title": "Test Issue",
            "url": "https://github.com/test-org/test-repo/issues/46",
            "state": "open",
        }

        # Create intent with project context
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_ticket",
            context={"original_message": "Create a test issue", "project_id": sample_project.id},
        )

        # Create and execute workflow
        factory = WorkflowFactory()
        engine = OrchestrationEngine()
        engine.github_agent = mock_github_agent

        workflow = await self.create_and_store_workflow(intent, engine, sample_project.to_dict())
        result = await engine.execute_workflow(workflow.id)

        # Verify project context was properly mapped to repository
        assert result["success"] is True
        assert workflow.context["repository"] == "test-org/test-repo"
        assert workflow.context["project_id"] == sample_project.id

        # Verify GitHub agent was called with correct repository
        call_args = mock_github_agent.create_issue_from_work_item.call_args
        assert call_args[1]["repo_name"] == "test-org/test-repo"

    @pytest.mark.asyncio
    async def test_workflow_orchestration_end_to_end(self, mock_llm_client, mock_github_agent):
        """Test integration: Workflow orchestration end-to-end"""

        # Mock LLM response
        mock_llm_response = """{
            "title": "Implement User Dashboard",
            "description": "## Description\\n\\nCreate a comprehensive user dashboard with analytics and settings.\\n\\n## Features\\n\\n- User profile management\\n- Analytics overview\\n- Settings panel\\n\\n## Acceptance Criteria\\n\\n- [ ] Dashboard loads within 2 seconds\\n- [ ] All user data is displayed correctly\\n- [ ] Settings can be modified and saved",
            "type": "feature",
            "priority": "high",
            "labels": ["feature", "ui", "dashboard", "high-priority"]
        }"""
        mock_llm_client.complete.return_value = mock_llm_response

        # Mock GitHub issue creation
        mock_github_agent.create_issue_from_work_item.return_value = {
            "id": 12350,
            "number": 47,
            "title": "Implement User Dashboard",
            "url": "https://github.com/test-org/test-repo/issues/47",
            "state": "open",
            "labels": ["feature", "ui", "dashboard", "high-priority"],
        }

        # Create intent
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_ticket",
            context={
                "original_message": "Implement a comprehensive user dashboard with analytics and settings",
                "repository": "test-org/test-repo",
            },
        )

        # Create and execute workflow
        factory = WorkflowFactory()
        engine = OrchestrationEngine()
        engine.github_agent = mock_github_agent

        workflow = await self.create_and_store_workflow(intent, engine)

        # Verify workflow structure
        assert workflow.type == WorkflowType.CREATE_TICKET
        assert (
            len(workflow.tasks) == 3
        )  # EXTRACT_WORK_ITEM + GENERATE_GITHUB_ISSUE_CONTENT + GITHUB_CREATE_ISSUE

        # Verify task types
        task_types = [task.type for task in workflow.tasks]
        assert TaskType.EXTRACT_WORK_ITEM in task_types
        assert TaskType.GITHUB_CREATE_ISSUE in task_types

        # Execute workflow
        result = await engine.execute_workflow(workflow.id)

        # Verify end-to-end success
        assert result["success"] is True
        assert "issue_number" in result["data"]
        assert "issue_url" in result["data"]
        assert result["data"]["issue_number"] == 47

        # Verify task execution order and results
        completed_tasks = [task for task in workflow.tasks if task.status == TaskStatus.COMPLETED]
        assert len(completed_tasks) == 2

    @pytest.mark.asyncio
    async def test_real_api_vs_mock_switching(self, mock_llm_client):
        """Test integration: Real API vs. mock switching"""

        # Test with mock GitHub agent
        with patch("services.integrations.github.github_agent.GitHubAgent") as mock_github_class:
            mock_agent_instance = Mock()
            mock_agent_instance.create_issue_from_work_item = AsyncMock()
            mock_agent_instance.create_issue_from_work_item.return_value = {
                "id": 12351,
                "number": 48,
                "title": "Mock Test Issue",
                "url": "https://github.com/test-org/test-repo/issues/48",
                "state": "open",
            }
            mock_github_class.return_value = mock_agent_instance

            # Create intent
            intent = Intent(
                category=IntentCategory.EXECUTION,
                action="create_ticket",
                context={
                    "original_message": "Create a test issue",
                    "repository": "test-org/test-repo",
                },
            )

            # Mock LLM response
            mock_llm_response = """{
                "title": "Mock Test Issue",
                "description": "Test description",
                "type": "task",
                "priority": "medium",
                "labels": ["task"]
            }"""
            mock_llm_client.complete.return_value = mock_llm_response

            # Create and execute workflow
            factory = WorkflowFactory()
            engine = OrchestrationEngine()

            workflow = await self.create_and_store_workflow(intent, engine)
            result = await engine.execute_workflow(workflow.id)

            # Verify mock behavior
            assert result["success"] is True
            assert result["data"]["issue_number"] == 48

            # Verify mock was called
            mock_agent_instance.create_issue_from_work_item.assert_called_once()

    @pytest.mark.asyncio
    async def test_multiple_issue_creation_workflow(self, mock_llm_client, mock_github_agent):
        """Test integration: Multiple issue creation in sequence"""

        # Test creating multiple issues in sequence
        test_cases = [
            {
                "prompt": "Create a bug ticket for login crash",
                "expected_title": "Login Crash Bug",
                "expected_type": "bug",
                "expected_priority": "high",
            },
            {
                "prompt": "Add dark mode feature",
                "expected_title": "Add Dark Mode Feature",
                "expected_type": "feature",
                "expected_priority": "medium",
            },
            {
                "prompt": "Update documentation",
                "expected_title": "Update Documentation",
                "expected_type": "task",
                "expected_priority": "low",
            },
        ]

        for i, test_case in enumerate(test_cases):
            # Mock LLM response for each test case
            mock_llm_response = f"""{{
                "title": "{test_case['expected_title']}",
                "description": "Test description for {test_case['expected_title']}",
                "type": "{test_case['expected_type']}",
                "priority": "{test_case['expected_priority']}",
                "labels": ["{test_case['expected_type']}"]
            }}"""
            mock_llm_client.complete.return_value = mock_llm_response

            # Mock GitHub issue creation
            mock_github_agent.create_issue_from_work_item.return_value = {
                "id": 12352 + i,
                "number": 49 + i,
                "title": test_case["expected_title"],
                "url": f"https://github.com/test-org/test-repo/issues/{49 + i}",
                "state": "open",
            }

            # Create intent
            intent = Intent(
                category=IntentCategory.EXECUTION,
                action="create_ticket",
                context={
                    "original_message": test_case["prompt"],
                    "repository": "test-org/test-repo",
                },
            )

            # Create and execute workflow
            factory = WorkflowFactory()
            engine = OrchestrationEngine()
            engine.github_agent = mock_github_agent

            workflow = await self.create_and_store_workflow(intent, engine)
            result = await engine.execute_workflow(workflow.id)

            # Verify each issue creation
            assert result["success"] is True
            assert result["data"]["issue_number"] == 49 + i

            # Verify GitHub agent was called with correct data
            call_args = mock_github_agent.create_issue_from_work_item.call_args
            work_item_arg = call_args[1]["work_item"]
            assert work_item_arg["title"] == test_case["expected_title"]
            assert work_item_arg["type"] == test_case["expected_type"]
            assert work_item_arg["priority"] == test_case["expected_priority"]


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
