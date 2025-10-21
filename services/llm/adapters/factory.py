"""
LLM Adapter Factory

Creates appropriate adapter based on provider configuration.
Implements factory pattern from Pattern-012 for clean provider instantiation.

Pattern-012: LLM Adapter Pattern
See: docs/internal/architecture/current/patterns/pattern-012-llm-adapter.md
"""

from typing import Dict, Type, List
import structlog

from .base import LLMAdapter
from .claude_adapter import ClaudeAdapter
from .openai_adapter import OpenAIAdapter
from .gemini_adapter import GeminiAdapter
from .perplexity_adapter import PerplexityAdapter
from services.llm.config import LLMProvider

logger = structlog.get_logger()


class LLMFactory:
    """
    Factory for creating LLM adapters.

    Implements factory pattern from Pattern-012 to create appropriate
    adapter based on provider configuration. Supports all 4 providers:
    Anthropic, OpenAI, Gemini, and Perplexity.

    Usage:
        # Create adapter for specific provider
        adapter = LLMFactory.create(
            provider=LLMProvider.ANTHROPIC,
            api_key="sk-ant-...",
            model="claude-3-sonnet"
        )

        # Check if provider is supported
        if LLMFactory.supports_provider(LLMProvider.GEMINI):
            adapter = LLMFactory.create(LLMProvider.GEMINI, api_key, model)

        # List all available providers
        providers = LLMFactory.list_providers()

        # Register custom adapter
        LLMFactory.register_adapter(LLMProvider.CUSTOM, CustomAdapter)

    Thread Safety:
        Factory is thread-safe for reading. Registering adapters
        at runtime should be done during initialization.
    """

    # Map of providers to adapter classes
    _adapters: Dict[LLMProvider, Type[LLMAdapter]] = {
        LLMProvider.ANTHROPIC: ClaudeAdapter,
        LLMProvider.OPENAI: OpenAIAdapter,
        LLMProvider.GEMINI: GeminiAdapter,
        LLMProvider.PERPLEXITY: PerplexityAdapter,
    }

    @classmethod
    def create(
        cls, provider: LLMProvider, api_key: str, model: str, **kwargs
    ) -> LLMAdapter:
        """
        Create adapter for specified provider.

        Args:
            provider: LLM provider enum (ANTHROPIC, OPENAI, GEMINI, PERPLEXITY)
            api_key: API key for the provider
            model: Model name/identifier
            **kwargs: Additional provider-specific configuration
                     (timeout, max_retries, temperature, etc.)

        Returns:
            Configured LLMAdapter instance

        Raises:
            ValueError: If provider not supported or invalid parameters
            ImportError: If required SDK not installed (e.g., google-generativeai)

        Example:
            # Create Claude adapter
            adapter = LLMFactory.create(
                provider=LLMProvider.ANTHROPIC,
                api_key="sk-ant-...",
                model="claude-3-5-sonnet-20241022",
                timeout=30.0
            )

            # Create Gemini adapter
            adapter = LLMFactory.create(
                provider=LLMProvider.GEMINI,
                api_key="AIza...",
                model="gemini-pro",
                temperature=0.7
            )
        """
        if provider not in cls._adapters:
            available = ", ".join(p.value for p in cls._adapters.keys())
            raise ValueError(
                f"Unknown provider: {provider.value}. Available providers: {available}"
            )

        adapter_class = cls._adapters[provider]

        try:
            logger.debug(
                "factory_creating_adapter", provider=provider.value, model=model, adapter_class=adapter_class.__name__
            )

            adapter = adapter_class(api_key=api_key, model=model, **kwargs)

            logger.info(
                "factory_adapter_created",
                provider=provider.value,
                model=model,
                adapter_type=adapter_class.__name__,
            )

            return adapter

        except ImportError as e:
            logger.error(
                "factory_import_error",
                provider=provider.value,
                error=str(e),
                help="Install required package (e.g., google-generativeai)",
            )
            raise

        except Exception as e:
            logger.error(
                "factory_creation_failed",
                provider=provider.value,
                model=model,
                error=str(e),
            )
            raise ValueError(
                f"Failed to create {provider.value} adapter: {str(e)}"
            ) from e

    @classmethod
    def register_adapter(
        cls, provider: LLMProvider, adapter_class: Type[LLMAdapter]
    ):
        """
        Register custom adapter.

        Allows extending factory with new providers at runtime.
        Useful for:
        - Custom LLM integrations
        - Testing with mock adapters
        - Plugin systems

        Args:
            provider: Provider enum (can be custom)
            adapter_class: Adapter class (must inherit from LLMAdapter)

        Raises:
            TypeError: If adapter_class doesn't inherit from LLMAdapter

        Example:
            class CustomAdapter(LLMAdapter):
                # ... implementation ...

            LLMFactory.register_adapter(
                LLMProvider.CUSTOM,
                CustomAdapter
            )
        """
        if not issubclass(adapter_class, LLMAdapter):
            raise TypeError(
                f"{adapter_class.__name__} must inherit from LLMAdapter"
            )

        logger.info(
            "factory_registering_adapter",
            provider=provider.value if isinstance(provider, LLMProvider) else str(provider),
            adapter_class=adapter_class.__name__,
        )

        cls._adapters[provider] = adapter_class

    @classmethod
    def list_providers(cls) -> List[LLMProvider]:
        """
        List all available providers.

        Returns:
            List of LLMProvider enums for registered adapters

        Example:
            providers = LLMFactory.list_providers()
            for provider in providers:
                print(f"Available: {provider.value}")
        """
        return list(cls._adapters.keys())

    @classmethod
    def supports_provider(cls, provider: LLMProvider) -> bool:
        """
        Check if provider is supported.

        Args:
            provider: Provider enum to check

        Returns:
            True if provider has registered adapter

        Example:
            if LLMFactory.supports_provider(LLMProvider.GEMINI):
                adapter = LLMFactory.create(LLMProvider.GEMINI, key, model)
            else:
                print("Gemini not supported")
        """
        return provider in cls._adapters

    @classmethod
    def get_adapter_class(cls, provider: LLMProvider) -> Type[LLMAdapter]:
        """
        Get adapter class for provider.

        Useful for inspection or advanced use cases.

        Args:
            provider: Provider enum

        Returns:
            Adapter class

        Raises:
            ValueError: If provider not supported
        """
        if provider not in cls._adapters:
            raise ValueError(f"Provider {provider.value} not supported")

        return cls._adapters[provider]

    @classmethod
    def get_provider_info(cls) -> Dict[str, Dict[str, any]]:
        """
        Get information about all registered providers.

        Returns:
            Dict mapping provider names to their metadata

        Example:
            info = LLMFactory.get_provider_info()
            for name, data in info.items():
                print(f"{name}: {data['adapter_class']}")
        """
        return {
            provider.value: {
                "provider": provider,
                "adapter_class": adapter_class.__name__,
                "module": adapter_class.__module__,
            }
            for provider, adapter_class in cls._adapters.items()
        }
