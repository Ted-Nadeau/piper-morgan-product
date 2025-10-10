"""
Tests for ProviderSelector

Phase 2: Provider Exclusion & Selection Logic
"""

from unittest.mock import Mock

import pytest

from services.config.llm_config_service import LLMConfigService
from services.llm.provider_selector import ProviderSelector


class TestProviderSelector:
    """Test provider selection logic"""

    def test_select_with_preferred_provider(self):
        """Preferred provider is used if available"""
        mock_config = Mock(spec=LLMConfigService)
        mock_config.get_available_providers.return_value = ["openai", "gemini"]

        selector = ProviderSelector(mock_config)
        provider = selector.select_provider(preferred="gemini")

        assert provider == "gemini"

    def test_select_with_unavailable_preferred_provider(self):
        """Falls back if preferred not available"""
        mock_config = Mock(spec=LLMConfigService)
        mock_config.get_available_providers.return_value = ["openai"]
        mock_config.get_provider_with_fallback.return_value = "openai"

        selector = ProviderSelector(mock_config)
        provider = selector.select_provider(preferred="anthropic")

        assert provider == "openai"

    def test_select_for_general_task(self):
        """General tasks use OpenAI (cheap)"""
        mock_config = Mock(spec=LLMConfigService)
        mock_config.get_available_providers.return_value = ["openai", "gemini", "anthropic"]

        selector = ProviderSelector(mock_config)
        provider = selector.select_provider(task_type="general")

        assert provider == "openai"

    def test_select_for_coding_task(self):
        """Coding tasks prefer OpenAI"""
        mock_config = Mock(spec=LLMConfigService)
        mock_config.get_available_providers.return_value = ["openai", "gemini", "anthropic"]

        selector = ProviderSelector(mock_config)
        provider = selector.select_provider(task_type="coding")

        assert provider == "openai"

    def test_select_for_research_task(self):
        """Research tasks prefer Gemini/Perplexity"""
        mock_config = Mock(spec=LLMConfigService)
        mock_config.get_available_providers.return_value = ["gemini", "perplexity", "openai"]

        selector = ProviderSelector(mock_config)
        provider = selector.select_provider(task_type="research")

        assert provider in ["gemini", "perplexity"]

    def test_select_excludes_anthropic_in_dev(self):
        """Anthropic excluded during development"""
        mock_config = Mock(spec=LLMConfigService)
        mock_config.get_available_providers.return_value = [
            "openai",
            "gemini",
        ]  # Anthropic excluded
        mock_config.get_provider_with_fallback.return_value = "openai"

        selector = ProviderSelector(mock_config)
        provider = selector.select_provider()

        assert provider != "anthropic"
        assert provider == "openai"

    def test_get_available_providers(self):
        """Returns available providers from config"""
        mock_config = Mock(spec=LLMConfigService)
        mock_config.get_available_providers.return_value = ["openai", "gemini"]

        selector = ProviderSelector(mock_config)
        available = selector.get_available_providers()

        assert available == ["openai", "gemini"]

    def test_task_type_fallback_to_default(self):
        """Falls back to default if task preferences not available"""
        mock_config = Mock(spec=LLMConfigService)
        mock_config.get_available_providers.return_value = [
            "perplexity"
        ]  # Only perplexity available
        mock_config.get_provider_with_fallback.return_value = "perplexity"

        selector = ProviderSelector(mock_config)
        provider = selector.select_provider(task_type="general")  # Prefers openai/gemini

        # Since openai/gemini not available, should fall back to default
        assert provider == "perplexity"
