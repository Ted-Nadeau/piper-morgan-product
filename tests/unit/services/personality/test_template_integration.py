"""
Integration tests for personality enhancement in TemplateRenderer
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.personality.personality_profile import (
    ActionLevel,
    ConfidenceDisplayStyle,
    EnhancedResponse,
    PersonalityProfile,
    TechnicalPreference,
)
from services.ui_messages.action_humanizer import ActionHumanizer
from services.ui_messages.templates import TemplateRenderer


class TestTemplatePersonalityIntegration:
    """Test TemplateRenderer personality enhancement integration"""

    @pytest.fixture
    def mock_humanizer(self):
        """Mock ActionHumanizer"""
        humanizer = AsyncMock(spec=ActionHumanizer)
        humanizer.humanize.return_value = "create a ticket"
        return humanizer

    @pytest.fixture
    def template_renderer(self, mock_humanizer):
        """TemplateRenderer with mocked humanizer"""
        return TemplateRenderer(humanizer=mock_humanizer)

    @pytest.fixture
    def test_profile(self):
        """Test PersonalityProfile"""
        return PersonalityProfile(
            warmth_level=0.8,
            confidence_style=ConfidenceDisplayStyle.NUMERIC,
            action_orientation=ActionLevel.HIGH,
            technical_depth=TechnicalPreference.BALANCED,
        )

    @pytest.mark.asyncio
    async def test_template_rendering_without_personality(self, template_renderer, mock_humanizer):
        """Test template rendering without user_id (no personality enhancement)"""
        # Act
        result = await template_renderer.render_template(
            "I understand you want to {human_action}.",
            intent_action="create_ticket",
            intent_category="execution",
            # No user_id provided
        )

        # Assert
        assert result == "I understand you want to create a ticket."
        mock_humanizer.humanize.assert_called_once_with("create_ticket", "execution")

    @pytest.mark.asyncio
    @patch("services.ui_messages.templates.PERSONALITY_AVAILABLE", True)
    async def test_template_rendering_with_personality_success(
        self, template_renderer, mock_humanizer
    ):
        """Test successful personality enhancement integration"""
        # Arrange
        enhanced_response = EnhancedResponse(
            original_content="I understand you want to create a ticket.",
            enhanced_content="Great! I understand you want to create a ticket. I'm confident this will work well.",
            personality_profile_used=MagicMock(),
            confidence_displayed=0.8,
            enhancements_applied=["warmth", "confidence"],
            processing_time_ms=50.0,
            context=MagicMock(),
            success=True,
        )

        with patch(
            "services.personality.response_enhancer.ResponsePersonalityEnhancer"
        ) as mock_enhancer_class:
            mock_enhancer = AsyncMock()
            mock_enhancer.enhance_response.return_value = enhanced_response
            mock_enhancer_class.return_value = mock_enhancer

            with patch("services.personality.repository.PersonalityProfileRepository"):
                with patch("services.personality.cache.ProfileCache"):
                    # Act
                    result = await template_renderer.render_template(
                        "I understand you want to {human_action}.",
                        intent_action="create_ticket",
                        intent_category="execution",
                        user_id="test_user",
                    )

        # Assert
        assert (
            result
            == "Great! I understand you want to create a ticket. I'm confident this will work well."
        )
        mock_enhancer.enhance_response.assert_called_once()

    @pytest.mark.asyncio
    @patch("services.ui_messages.templates.PERSONALITY_AVAILABLE", True)
    async def test_template_rendering_with_personality_failure_fallback(
        self, template_renderer, mock_humanizer
    ):
        """Test fallback when personality enhancement fails"""
        # Arrange
        enhanced_response = EnhancedResponse(
            original_content="I understand you want to create a ticket.",
            enhanced_content="I understand you want to create a ticket.",  # Same as original
            personality_profile_used=MagicMock(),
            confidence_displayed=0.8,
            enhancements_applied=[],
            processing_time_ms=150.0,  # Timeout
            context=MagicMock(),
            success=False,
            error_message="Enhancement timeout",
        )

        with patch(
            "services.personality.response_enhancer.ResponsePersonalityEnhancer"
        ) as mock_enhancer_class:
            mock_enhancer = AsyncMock()
            mock_enhancer.enhance_response.return_value = enhanced_response
            mock_enhancer_class.return_value = mock_enhancer

            with patch("services.personality.repository.PersonalityProfileRepository"):
                with patch("services.personality.cache.ProfileCache"):
                    # Act
                    result = await template_renderer.render_template(
                        "I understand you want to {human_action}.",
                        intent_action="create_ticket",
                        intent_category="execution",
                        user_id="test_user",
                    )

        # Assert - should fallback to original rendered content
        assert result == "I understand you want to create a ticket."
        mock_enhancer.enhance_response.assert_called_once()

    @pytest.mark.asyncio
    @patch("services.ui_messages.templates.PERSONALITY_AVAILABLE", True)
    async def test_template_rendering_with_personality_exception_fallback(
        self, template_renderer, mock_humanizer
    ):
        """Test graceful fallback when personality enhancement throws exception"""

        with patch(
            "services.personality.response_enhancer.ResponsePersonalityEnhancer"
        ) as mock_enhancer_class:
            mock_enhancer_class.side_effect = Exception("Database connection failed")

            # Act
            result = await template_renderer.render_template(
                "I understand you want to {human_action}.",
                intent_action="create_ticket",
                intent_category="execution",
                user_id="test_user",
            )

        # Assert - should fallback to original content
        assert result == "I understand you want to create a ticket."

    @pytest.mark.asyncio
    async def test_response_type_determination(self, template_renderer):
        """Test ResponseType determination from intent categories"""
        renderer = template_renderer

        # Test various category mappings
        assert renderer._determine_response_type("analysis", "investigate") is not None
        assert renderer._determine_response_type("execution", "create_ticket") is not None
        assert renderer._determine_response_type("synthesis", "generate_report") is not None
        assert renderer._determine_response_type(None, "unknown_action") is not None

    @pytest.mark.asyncio
    @patch("services.ui_messages.templates.PERSONALITY_AVAILABLE", False)
    async def test_template_rendering_personality_not_available(
        self, template_renderer, mock_humanizer
    ):
        """Test template rendering when personality system not available"""
        # Act
        result = await template_renderer.render_template(
            "I understand you want to {human_action}.",
            intent_action="create_ticket",
            intent_category="execution",
            user_id="test_user",  # user_id provided but personality not available
        )

        # Assert - should render normally without personality
        assert result == "I understand you want to create a ticket."
        mock_humanizer.humanize.assert_called_once_with("create_ticket", "execution")
