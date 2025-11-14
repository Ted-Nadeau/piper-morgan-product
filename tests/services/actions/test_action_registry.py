"""Tests for Action Registry and Command Pattern"""

import pytest

from services.actions import ActionRegistry
from services.actions.commands import BaseCommand, GithubIssueCommand


class TestActionRegistry:
    """Test ActionRegistry functionality"""

    @pytest.mark.asyncio
    async def test_github_issue_command(self):
        """Test GitHub issue creation command"""
        params = {
            "title": "Test issue from unit test",
            "labels": ["test", "automated"],
            "assignee": "xian",
        }
        context = {"user_id": "test-user-123", "session_id": "test-session-456"}

        result = await ActionRegistry.execute("create_github_issue", params, context)

        assert result["status"] == "success"
        assert result["action"] == "create_github_issue"
        assert result["title"] == "Test issue from unit test"
        assert result["labels"] == ["test", "automated"]
        assert "message" in result
        # For alpha, this is mock - verify mock structure
        assert result["issue_id"] == "mock-123"

    @pytest.mark.asyncio
    async def test_github_issue_command_defaults(self):
        """Test GitHub issue creation with default parameters"""
        params = {}
        context = {"user_id": "test-user-123"}

        result = await ActionRegistry.execute("create_github_issue", params, context)

        assert result["status"] == "success"
        assert result["title"] == "Action item from standup"
        assert result["labels"] == ["standup", "action-item"]

    @pytest.mark.asyncio
    async def test_unknown_action(self):
        """Test unknown action raises ValueError"""
        params = {}
        context = {"user_id": "test-user-123"}

        with pytest.raises(ValueError) as exc_info:
            await ActionRegistry.execute("unknown_action", params, context)

        assert "Unknown action type: unknown_action" in str(exc_info.value)
        assert "Available: create_github_issue" in str(exc_info.value)

    def test_is_registered(self):
        """Test checking if action is registered"""
        assert ActionRegistry.is_registered("create_github_issue") is True
        assert ActionRegistry.is_registered("unknown_action") is False

    def test_list_actions(self):
        """Test listing all registered actions"""
        actions = ActionRegistry.list_actions()
        assert isinstance(actions, list)
        assert "create_github_issue" in actions
        assert len(actions) >= 1  # At least one action registered


class TestGithubIssueCommand:
    """Test GithubIssueCommand directly"""

    @pytest.mark.asyncio
    async def test_execute_success(self):
        """Test successful execution"""
        params = {"title": "Direct test", "labels": ["direct"]}
        context = {"user_id": "test-123"}

        command = GithubIssueCommand(params, context)
        result = await command.execute()

        assert result["status"] == "success"
        assert result["title"] == "Direct test"
        assert result["labels"] == ["direct"]

    @pytest.mark.asyncio
    async def test_validate_params(self):
        """Test parameter validation (currently no-op but should not raise)"""
        params = {}
        context = {}

        command = GithubIssueCommand(params, context)
        # Should not raise
        command.validate_params()

    @pytest.mark.asyncio
    async def test_rollback_not_implemented(self):
        """Test rollback raises NotImplementedError for alpha"""
        params = {}
        context = {}

        command = GithubIssueCommand(params, context)

        with pytest.raises(NotImplementedError) as exc_info:
            await command.rollback()

        assert "Rollback not implemented in alpha" in str(exc_info.value)


class TestBaseCommand:
    """Test BaseCommand abstract class"""

    def test_cannot_instantiate_directly(self):
        """Test that BaseCommand cannot be instantiated directly"""
        with pytest.raises(TypeError):
            BaseCommand({}, {})

    def test_subclass_must_implement_execute(self):
        """Test that subclass must implement execute()"""

        class IncompleteCommand(BaseCommand):
            pass

        with pytest.raises(TypeError):
            IncompleteCommand({}, {})
