from unittest.mock import AsyncMock, MagicMock

import pytest

from services.ui_messages.action_humanizer import ActionHumanizer
from services.ui_messages.templates import TemplateRenderer


class TestTemplateRenderer:
    """Test TemplateRenderer integration with ActionHumanizer"""

    @pytest.fixture
    def mock_humanizer(self):
        """Mock ActionHumanizer for testing"""
        humanizer = AsyncMock(spec=ActionHumanizer)
        return humanizer

    @pytest.fixture
    def template_renderer(self, mock_humanizer):
        """TemplateRenderer instance with mocked humanizer"""
        return TemplateRenderer(humanizer=mock_humanizer)

    @pytest.mark.asyncio
    async def test_template_renderer_calls_action_humanizer(
        self, template_renderer, mock_humanizer
    ):
        """Test that TemplateRenderer calls ActionHumanizer when {human_action} placeholder is present"""
        # Arrange
        template = (
            "I understand you want to {human_action}. I've started a workflow to handle this."
        )
        intent_action = "investigate_crash"
        intent_category = "analysis"
        mock_humanizer.humanize.return_value = "investigate a crash"

        # Act
        result = await template_renderer.render_template(
            template=template,
            intent_action=intent_action,
            intent_category=intent_category,
        )

        # Assert
        mock_humanizer.humanize.assert_called_once_with(intent_action, intent_category)
        assert (
            result
            == "I understand you want to investigate a crash. I've started a workflow to handle this."
        )

    @pytest.mark.asyncio
    async def test_human_action_placeholder_replacement(self, template_renderer, mock_humanizer):
        """Test that {human_action} placeholder gets replaced with humanized action"""
        # Arrange
        template = "Working on {human_action} for you."
        intent_action = "create_ticket"
        mock_humanizer.humanize.return_value = "create a ticket"

        # Act
        result = await template_renderer.render_template(
            template=template, intent_action=intent_action
        )

        # Assert
        assert result == "Working on create a ticket for you."

    @pytest.mark.asyncio
    async def test_fallback_when_humanizer_not_available(self):
        """Test fallback behavior when humanizer is not available"""
        # Arrange
        template = "Working on {human_action} for you."
        intent_action = "create_ticket"

        # Act - Create renderer without humanizer
        renderer = TemplateRenderer(humanizer=None)
        result = await renderer.render_template(template=template, intent_action=intent_action)

        # Assert - Should fall back to original action
        assert result == "Working on create_ticket for you."

    @pytest.mark.asyncio
    async def test_no_human_action_placeholder_no_humanizer_call(
        self, template_renderer, mock_humanizer
    ):
        """Test that humanizer is not called when {human_action} placeholder is not present"""
        # Arrange
        template = "Workflow completed successfully!"
        intent_action = "create_ticket"

        # Act
        result = await template_renderer.render_template(
            template=template, intent_action=intent_action
        )

        # Assert
        mock_humanizer.humanize.assert_not_called()
        assert result == "Workflow completed successfully!"

    @pytest.mark.asyncio
    async def test_preserves_original_action_placeholder(self, template_renderer, mock_humanizer):
        """Test that {action} placeholder is preserved and {human_action} is added"""
        # Arrange
        template = "Original: {action}, Humanized: {human_action}"
        intent_action = "investigate_crash"
        mock_humanizer.humanize.return_value = "investigate a crash"

        # Act
        result = await template_renderer.render_template(
            template=template, intent_action=intent_action
        )

        # Assert
        assert result == "Original: investigate_crash, Humanized: investigate a crash"

    @pytest.mark.asyncio
    async def test_additional_kwargs_passed_through(self, template_renderer, mock_humanizer):
        """Test that additional kwargs are passed through to template formatting"""
        # Arrange
        template = "Working on {human_action} for {user_name}."
        intent_action = "analyze_file"
        mock_humanizer.humanize.return_value = "analyze a file"

        # Act
        result = await template_renderer.render_template(
            template=template, intent_action=intent_action, user_name="Alice"
        )

        # Assert
        assert result == "Working on analyze a file for Alice."
