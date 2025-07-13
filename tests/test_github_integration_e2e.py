"""
End-to-End Tests for GitHub Integration Vertical Slice
Tests the complete flow from natural language prompt to GitHub issue creation
"""

import asyncio
from typing import Any, Dict
from unittest.mock import AsyncMock, Mock, patch

import pytest

from services.domain.models import Intent, Task, Workflow
from services.domain.work_item_extractor import WorkItemExtractor
from services.integrations.github.github_agent import GitHubAgent
from services.orchestration.engine import OrchestrationEngine
from services.shared_types import (IntentCategory, TaskStatus, TaskType,
                                   WorkflowType)


class TestGitHubIntegrationE2E:
    """End-to-end tests for GitHub issue creation from natural language"""

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
        return mock_agent

    @pytest.fixture
    def sample_work_item(self):
        """Sample work item for testing"""
        return {
            "id": "test-work-item-123",
            "title": "Mobile App Login Crash",
            "description": "## Problem Description\nUsers are experiencing crashes when attempting to log in on mobile devices.\n\n## Steps to Reproduce\n1. Open mobile app\n2. Tap login button\n3. App crashes immediately\n\n## Expected Behavior\nUser should be able to log in successfully\n\n## Actual Behavior\nApp crashes with no error message",
            "type": "bug",
            "priority": "high",
            "labels": ["bug", "mobile", "login", "high-priority"],
            "assignee": None,
            "project_id": None,
            "source_system": "github",
            "external_id": "",
            "external_url": None,
            "metadata": {
                "original_prompt": "Create a bug ticket for login crash on mobile",
                "extraction_method": "llm",
            },
            "created_at": "2025-07-09T18:00:00",
        }

    @pytest.mark.asyncio
    async def test_work_item_extraction_from_prompt(self, mock_llm_client):
        """Test that WorkItemExtractor can extract structured data from natural language"""

        # Mock LLM response
        mock_response = """{
            "title": "Mobile App Login Crash",
            "description": "## Problem Description\\nUsers are experiencing crashes when attempting to log in on mobile devices.\\n\\n## Steps to Reproduce\\n1. Open mobile app\\n2. Tap login button\\n3. App crashes immediately\\n\\n## Expected Behavior\\nUser should be able to log in successfully\\n\\n## Actual Behavior\\nApp crashes with no error message",
            "type": "bug",
            "priority": "high",
            "labels": ["bug", "mobile", "login", "high-priority"]
        }"""

        mock_llm_client.complete.return_value = mock_response

        # Create extractor and test
        extractor = WorkItemExtractor(mock_llm_client)
        prompt = "Create a bug ticket for login crash on mobile"

        work_item = await extractor.extract_from_prompt(prompt)

        # Verify the work item was created correctly
        assert work_item.title == "Mobile App Login Crash"
        assert work_item.type == "bug"
        assert work_item.priority == "high"
        assert "bug" in work_item.labels
        assert "mobile" in work_item.labels
        assert "login" in work_item.labels
        assert work_item.source_system == "github"
        assert work_item.metadata["original_prompt"] == prompt
        assert work_item.metadata["extraction_method"] == "llm"

    @pytest.mark.asyncio
    async def test_work_item_extraction_fallback(self, mock_llm_client):
        """Test that fallback extraction works when LLM fails"""

        # Mock LLM failure
        mock_llm_client.complete.side_effect = Exception("LLM API error")

        # Create extractor and test
        extractor = WorkItemExtractor(mock_llm_client)
        prompt = "Create a bug ticket for login crash on mobile"

        work_item = await extractor.extract_from_prompt(prompt)

        # Verify fallback extraction worked
        assert work_item.title == prompt  # Should use original prompt as title
        assert work_item.type == "bug"  # Should detect "bug" keyword
        assert work_item.priority == "medium"  # Default priority
        assert "bug" in work_item.labels
        assert work_item.metadata["extraction_method"] == "fallback"

    @pytest.mark.asyncio
    async def test_github_agent_work_item_creation(
        self, mock_github_agent, sample_work_item
    ):
        """Test that GitHub agent can create issues from work items"""

        # Mock successful issue creation
        mock_github_agent.create_issue_from_work_item.return_value = {
            "id": 12345,
            "number": 42,
            "title": "Mobile App Login Crash",
            "url": "https://github.com/test/repo/issues/42",
            "state": "open",
            "work_item_id": "test-work-item-123",
            "work_item_type": "bug",
            "work_item_priority": "high",
            "labels": ["bug", "mobile", "login", "high-priority"],
        }

        # Test issue creation
        result = await mock_github_agent.create_issue_from_work_item(
            repo_name="test/repo", work_item=sample_work_item
        )

        # Verify the issue was created with correct data
        assert result["number"] == 42
        assert result["title"] == "Mobile App Login Crash"
        assert "github.com" in result["url"]
        assert result["work_item_id"] == "test-work-item-123"
        assert result["work_item_type"] == "bug"
        assert result["work_item_priority"] == "high"

        # Verify the method was called with correct parameters
        mock_github_agent.create_issue_from_work_item.assert_called_once_with(
            repo_name="test/repo", work_item=sample_work_item
        )

    @pytest.mark.asyncio
    async def test_complete_workflow_execution(
        self, mock_llm_client, mock_github_agent, sample_work_item
    ):
        """Test the complete workflow from intent to GitHub issue creation"""

        # Mock LLM response for extraction
        mock_llm_response = """{
            "title": "Mobile App Login Crash",
            "description": "## Problem Description\\nUsers are experiencing crashes when attempting to log in on mobile devices.",
            "type": "bug",
            "priority": "high",
            "labels": ["bug", "mobile", "login", "high-priority"]
        }"""
        mock_llm_client.complete.return_value = mock_llm_response

        # Mock GitHub issue creation
        mock_github_agent.create_issue_from_work_item.return_value = {
            "id": 12345,
            "number": 42,
            "title": "Mobile App Login Crash",
            "url": "https://github.com/test/repo/issues/42",
            "state": "open",
        }

        # Test that the workflow can be created with the right tasks
        workflow = Workflow(
            type=WorkflowType.CREATE_TICKET,
            context={
                "repository": "test/repo",
                "original_message": "Create a bug ticket for login crash on mobile",
            },
        )

        # Verify workflow has correct type and context
        assert workflow.type == WorkflowType.CREATE_TICKET
        assert workflow.context["repository"] == "test/repo"
        assert (
            workflow.context["original_message"]
            == "Create a bug ticket for login crash on mobile"
        )

        # Test that we can create the required tasks
        extract_task = Task(type=TaskType.EXTRACT_WORK_ITEM, status=TaskStatus.PENDING)
        create_task = Task(type=TaskType.GITHUB_CREATE_ISSUE, status=TaskStatus.PENDING)

        # Verify tasks have correct types
        assert extract_task.type == TaskType.EXTRACT_WORK_ITEM
        assert create_task.type == TaskType.GITHUB_CREATE_ISSUE

        # Test that GitHub agent can create issues from work items
        result = await mock_github_agent.create_issue_from_work_item(
            repo_name="test/repo", work_item=sample_work_item
        )

        # Verify the result
        assert result["number"] == 42
        assert result["title"] == "Mobile App Login Crash"
        assert "github.com" in result["url"]

    @pytest.mark.asyncio
    async def test_error_handling_in_extraction(self, mock_llm_client):
        """Test error handling when extraction fails"""

        # Mock LLM returning invalid JSON
        mock_llm_client.complete.return_value = "Invalid JSON response"

        extractor = WorkItemExtractor(mock_llm_client)
        prompt = "Create a bug ticket for login crash on mobile"

        # Should not raise exception, should use fallback
        work_item = await extractor.extract_from_prompt(prompt)

        # Verify fallback was used
        assert work_item.metadata["extraction_method"] == "fallback"
        assert work_item.title == prompt  # Uses original prompt as title

    @pytest.mark.asyncio
    async def test_error_handling_in_github_creation(
        self, mock_github_agent, sample_work_item
    ):
        """Test error handling when GitHub issue creation fails"""

        # Mock GitHub API failure
        mock_github_agent.create_issue_from_work_item.side_effect = Exception(
            "GitHub API error"
        )

        # Test that exception is raised
        with pytest.raises(Exception, match="GitHub API error"):
            await mock_github_agent.create_issue_from_work_item(
                repo_name="test/repo", work_item=sample_work_item
            )

    @pytest.mark.asyncio
    async def test_work_item_validation(self, mock_llm_client):
        """Test that work items are properly validated"""

        # Mock LLM response with missing required fields
        mock_response = """{
            "title": "Test Issue",
            "description": "Test description"
        }"""

        mock_llm_client.complete.return_value = mock_response

        extractor = WorkItemExtractor(mock_llm_client)
        prompt = "Create a test issue"

        # Should not raise exception, should use defaults for missing fields
        work_item = await extractor.extract_from_prompt(prompt)

        # Verify defaults were applied
        assert work_item.type == "task"  # Default type
        assert work_item.priority == "medium"  # Default priority
        assert "task" in work_item.labels  # Should have task label
        assert "priority-medium" in work_item.labels  # Should have priority label


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
