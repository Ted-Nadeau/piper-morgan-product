"""
LLM Provider Selection Service

Handles intelligent provider selection with fallbacks,
exclusions, and environment-aware routing.

Phase 2: Provider Exclusion & Selection Logic
"""

from typing import List, Optional

import structlog

from services.config.llm_config_service import LLMConfigService

logger = structlog.get_logger(__name__)


class ProviderSelector:
    """
    Service for selecting appropriate LLM provider

    Usage:
        selector = ProviderSelector()
        provider = selector.select_provider(task_type="general")
    """

    def __init__(self, config_service: Optional[LLMConfigService] = None):
        """Initialize with config service"""
        self._config = config_service or LLMConfigService()

    def select_provider(
        self, task_type: Optional[str] = None, preferred: Optional[str] = None
    ) -> str:
        """
        Select appropriate provider for task

        Args:
            task_type: Type of task (general, coding, research)
            preferred: Explicitly preferred provider

        Returns:
            Provider name to use
        """

        # If preferred specified and available, use it
        if preferred:
            if self._is_available(preferred):
                logger.debug(f"Using preferred provider: {preferred}")
                return preferred
            else:
                logger.warning(f"Preferred provider {preferred} not available, falling back")

        # Task-specific routing
        if task_type:
            provider = self._select_for_task(task_type)
            if provider:
                return provider

        # Use default with fallback
        provider = self._config.get_provider_with_fallback(preferred)
        logger.debug(f"Selected provider: {provider}")
        return provider

    def _select_for_task(self, task_type: str) -> Optional[str]:
        """
        Select provider based on task type

        Task-specific preferences (cost-optimized):
        - general: OpenAI (cheap, reliable)
        - coding: OpenAI (good at code)
        - research: Gemini (good for search/research)
        """

        task_preferences = {
            "general": ["openai", "gemini", "anthropic"],
            "coding": ["openai", "anthropic", "gemini"],
            "research": ["gemini", "perplexity", "openai"],
        }

        preferences = task_preferences.get(task_type, [])
        available = self._config.get_available_providers()

        # Return first preferred provider that's available
        for provider in preferences:
            if provider in available:
                logger.debug(f"Task {task_type}: selected {provider}")
                return provider

        return None

    def _is_available(self, provider: str) -> bool:
        """Check if provider is available"""
        available = self._config.get_available_providers()
        return provider in available

    def get_available_providers(self) -> List[str]:
        """Get list of available providers"""
        return self._config.get_available_providers()
