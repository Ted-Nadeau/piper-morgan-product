"""
LLM Domain Service

Domain service mediating all LLM access following DDD principles.
Provides clean interface for LLM operations across all consumers.
"""

from typing import Any, Dict, List, Optional

import structlog

from services.config.llm_config_service import LLMConfigService
from services.llm.provider_selector import ProviderSelector

logger = structlog.get_logger(__name__)


class LLMDomainService:
    """
    Domain service for LLM operations

    Mediates all LLM access following Domain-Driven Design principles.
    This is THE ONLY way to access LLM providers in the system.

    Usage:
        # Access via ServiceRegistry
        llm = ServiceRegistry.get_llm()

        # Generate completion
        response = await llm.complete(
            task_type="general",
            prompt="Hello"
        )
    """

    def __init__(
        self,
        config_service: Optional[LLMConfigService] = None,
        provider_selector: Optional[ProviderSelector] = None,
    ):
        """
        Initialize LLM domain service

        Args:
            config_service: Optional LLMConfigService for testing
            provider_selector: Optional ProviderSelector for testing
        """
        self._config_service = config_service
        self._provider_selector = provider_selector
        self._llm_client = None
        self._initialized = False

    async def initialize(self) -> None:
        """
        Initialize service (called from main.py at startup)

        Validates all providers and initializes clients.
        Must be called before any LLM operations.

        Raises:
            RuntimeError: If initialization fails
        """
        try:
            logger.info("Initializing LLM domain service...")

            # Initialize config service if not provided
            if not self._config_service:
                self._config_service = LLMConfigService()

            # Validate all providers
            logger.info("Validating LLM providers...")
            validation_results = await self._config_service.validate_all_providers()

            # Log validation results
            for provider, result in validation_results.items():
                if result.is_valid:
                    logger.info(f"✅ {provider}: Valid")
                else:
                    logger.warning(f"⚠️ {provider}: {result.error_message}")

            # Count valid providers
            valid_count = sum(1 for r in validation_results.values() if r.is_valid)
            logger.info(f"LLM providers validated: {valid_count}/{len(validation_results)}")

            # Initialize provider selector
            if not self._provider_selector:
                self._provider_selector = ProviderSelector(self._config_service)

            # Initialize LLM client
            self._initialize_client()

            self._initialized = True
            logger.info("LLM domain service initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize LLM domain service: {e}")
            raise RuntimeError(f"LLM domain service initialization failed: {e}")

    def _initialize_client(self) -> None:
        """Initialize LLM client"""
        try:
            # Import global llm_client instance
            from services.llm.clients import llm_client

            self._llm_client = llm_client
            logger.info("LLM client initialized")

        except Exception as e:
            logger.error(f"Failed to initialize LLM client: {e}")
            raise

    async def complete(
        self,
        task_type: str,
        prompt: str,
        context: Optional[Dict[str, Any]] = None,
        response_format: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Generate LLM completion

        Domain-level operation for LLM text generation.
        Delegates to underlying LLM client with proper error handling.

        Args:
            task_type: Type of task (intent_classification, reasoning, etc)
            prompt: Input prompt for generation
            context: Optional context to include
            response_format: Optional response format specification

        Returns:
            Generated text response

        Raises:
            RuntimeError: If service not initialized
            Exception: If LLM completion fails
        """
        if not self._initialized:
            raise RuntimeError(
                "LLMDomainService not initialized. " "Call initialize() before using."
            )

        logger.info("Generating LLM completion", task_type=task_type)

        try:
            # Delegate to LLM client
            response = await self._llm_client.complete(
                task_type=task_type, prompt=prompt, context=context, response_format=response_format
            )
            return response

        except Exception as e:
            logger.error(f"LLM completion failed", task_type=task_type, error=str(e))
            raise

    def get_available_providers(self) -> List[str]:
        """
        Get list of available providers

        Returns:
            List of provider names
        """
        if not self._initialized:
            raise RuntimeError("Service not initialized")

        return self._config_service.get_available_providers()

    def get_default_provider(self) -> str:
        """
        Get default provider

        Returns:
            Default provider name
        """
        if not self._initialized:
            raise RuntimeError("Service not initialized")

        return self._config_service.get_default_provider()

    def is_initialized(self) -> bool:
        """Check if service is initialized"""
        return self._initialized
