from unittest.mock import AsyncMock

import pytest

from services.domain.models import ActionHumanization
from services.persistence.repositories.action_humanization_repository import (
    ActionHumanizationRepository,
)
from services.ui_messages.action_humanizer import ActionHumanizer
from services.ui_messages.templates import TemplateRenderer


class TestHumanizedWorkflowMessages:
    """Integration tests for humanized workflow messages"""

    @pytest.fixture
    def mock_repo(self):
        """Mock repository for testing"""
        repo = AsyncMock(spec=ActionHumanizationRepository)
        return repo

    @pytest.fixture
    def action_humanizer(self, mock_repo):
        """ActionHumanizer with mocked repository"""
        return ActionHumanizer()

    @pytest.fixture
    def template_renderer(self, action_humanizer):
        """TemplateRenderer with ActionHumanizer"""
        return TemplateRenderer(humanizer=action_humanizer)

    @pytest.mark.asyncio
    async def test_workflow_acknowledgment_uses_humanized_action(self, template_renderer):
        """Test that workflow acknowledgment messages use humanized actions"""
        # Arrange
        template = (
            "I understand you want to {human_action}. I've started a workflow to handle this."
        )
        intent_action = "investigate_crash"
        intent_category = "analysis"

        # Act
        result = await template_renderer.render_template(
            template=template,
            intent_action=intent_action,
            intent_category=intent_category,
        )

        # Assert - Should see humanized action, not technical string
        assert "investigate a crash" in result
        assert "investigate_crash" not in result
        assert (
            result
            == "I understand you want to investigate a crash. I've started a workflow to handle this."
        )

    @pytest.mark.asyncio
    async def test_create_ticket_workflow_message(self, template_renderer):
        """Test create ticket workflow acknowledgment"""
        # Arrange
        template = "✅ Successfully created GitHub issue for {human_action}."
        intent_action = "create_ticket"
        intent_category = "execution"

        # Act
        result = await template_renderer.render_template(
            template=template,
            intent_action=intent_action,
            intent_category=intent_category,
        )

        # Assert
        assert "create a ticket" in result
        assert result == "✅ Successfully created GitHub issue for create a ticket."

    @pytest.mark.asyncio
    async def test_analyze_file_workflow_message(self, template_renderer):
        """Test file analysis workflow acknowledgment"""
        # Arrange
        template = "I'm {human_action} for you."
        intent_action = "analyze_file"
        intent_category = "analysis"

        # Act
        result = await template_renderer.render_template(
            template=template,
            intent_action=intent_action,
            intent_category=intent_category,
        )

        # Assert
        assert "analyze a file" in result
        assert result == "I'm analyze a file for you."

    @pytest.mark.asyncio
    async def test_summarize_document_workflow_message(self, template_renderer):
        """Test document summarization workflow acknowledgment"""
        # Arrange
        template = "I'm {human_action} for you."
        intent_action = "summarize_document"
        intent_category = "synthesis"

        # Act
        result = await template_renderer.render_template(
            template=template,
            intent_action=intent_action,
            intent_category=intent_category,
        )

        # Assert
        assert "summarize a document" in result
        assert result == "I'm summarize a document for you."

    @pytest.mark.asyncio
    async def test_unknown_action_fallback(self, template_renderer):
        """Test fallback behavior for unknown actions"""
        # Arrange
        template = "Working on {human_action}."
        intent_action = "unknown_action"
        intent_category = "unknown"

        # Act
        result = await template_renderer.render_template(
            template=template,
            intent_action=intent_action,
            intent_category=intent_category,
        )

        # Assert - Should fall back to underscore replacement
        assert "unknown action" in result
        assert result == "Working on unknown action."

    @pytest.mark.asyncio
    async def test_action_without_underscores(self, template_renderer):
        """Test actions that don't have underscores"""
        # Arrange
        template = "Processing {human_action}."
        intent_action = "analyze"
        intent_category = "analysis"

        # Act
        result = await template_renderer.render_template(
            template=template,
            intent_action=intent_action,
            intent_category=intent_category,
        )

        # Assert - Should return action as-is
        assert "analyze" in result
        assert result == "Processing analyze."

    @pytest.mark.asyncio
    async def test_template_without_human_action_placeholder(self, template_renderer):
        """Test templates that don't use {human_action} placeholder"""
        # Arrange
        template = "Workflow completed successfully!"
        intent_action = "investigate_crash"
        intent_category = "analysis"

        # Act
        result = await template_renderer.render_template(
            template=template,
            intent_action=intent_action,
            intent_category=intent_category,
        )

        # Assert - Should return template as-is
        assert result == "Workflow completed successfully!"

    @pytest.mark.asyncio
    async def test_template_with_additional_context(self, template_renderer):
        """Test template rendering with additional context variables"""
        # Arrange
        template = "I'm {human_action} for {user_name} on {project_name}."
        intent_action = "review_code"
        intent_category = "analysis"

        # Act
        result = await template_renderer.render_template(
            template=template,
            intent_action=intent_action,
            intent_category=intent_category,
            user_name="Alice",
            project_name="Piper Morgan",
        )

        # Assert
        assert "review code" in result
        assert "Alice" in result
        assert "Piper Morgan" in result
        assert result == "I'm review code for Alice on Piper Morgan."
