"""
LLM Adapter Pattern - Base Interface

Implements Pattern-012 for vendor-agnostic LLM access across multiple providers.
This adapter layer provides a consistent interface while allowing provider-specific
capabilities and optimizations.

Pattern-012: LLM Adapter Pattern
See: docs/internal/architecture/current/patterns/pattern-012-llm-adapter.md
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Dict, Any, AsyncIterator
from dataclasses import dataclass, field


@dataclass
class LLMResponse:
    """
    Standardized LLM response format.

    Provides consistent response structure across all providers while
    preserving provider-specific metadata.

    Attributes:
        content: The generated text response
        model: Model name used for generation
        provider: Provider name (anthropic, openai, gemini, perplexity)
        usage: Token usage statistics
        metadata: Provider-specific metadata (finish_reason, etc.)
    """

    content: str
    model: str
    provider: str
    usage: Dict[str, int] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class LLMAdapter(ABC):
    """
    Abstract base class for LLM provider adapters.

    Implements Pattern-012 to provide vendor-agnostic interface for multiple
    LLM providers while maintaining provider-specific capabilities through
    optional methods.

    The adapter pattern allows:
    - Easy switching between providers
    - A/B testing different models
    - Graceful fallback between providers
    - Consistent error handling
    - Standardized response formats

    Usage:
        # Via factory
        adapter = LLMFactory.create(LLMProvider.ANTHROPIC, api_key, model)
        response = await adapter.complete("Hello, world!")

        # Direct instantiation
        adapter = ClaudeAdapter(api_key="sk-...", model="claude-3-sonnet")
        response = await adapter.complete("Generate a summary")

    See: docs/internal/architecture/current/patterns/pattern-012-llm-adapter.md
    """

    def __init__(self, api_key: str, model: str, **kwargs):
        """
        Initialize adapter with provider credentials.

        Args:
            api_key: API key for the provider
            model: Model name/identifier
            **kwargs: Additional provider-specific configuration

        Raises:
            ValueError: If required configuration missing
        """
        if not api_key:
            raise ValueError("API key is required")
        if not model:
            raise ValueError("Model name is required")

        self.api_key = api_key
        self.model = model
        self.config = kwargs

    @abstractmethod
    async def complete(self, prompt: str, **kwargs) -> LLMResponse:
        """
        Generate text completion.

        Args:
            prompt: Input prompt for the model
            **kwargs: Provider-specific options:
                max_tokens: Maximum tokens to generate
                temperature: Sampling temperature (0.0-1.0)
                top_p: Nucleus sampling parameter
                stop: Stop sequences
                stream: Whether to stream response (use stream_complete instead)

        Returns:
            LLMResponse with standardized format

        Raises:
            ValueError: If prompt is empty or invalid
            RuntimeError: If API call fails
        """
        pass

    @abstractmethod
    async def classify(self, text: str, categories: List[str]) -> Tuple[str, float]:
        """
        Classify text into categories with confidence score.

        Args:
            text: Text to classify
            categories: List of possible categories

        Returns:
            Tuple of (category_name, confidence_score)
            confidence_score is between 0.0 and 1.0

        Raises:
            ValueError: If categories is empty or text is invalid
        """
        pass

    @abstractmethod
    async def stream_complete(self, prompt: str, **kwargs) -> AsyncIterator[str]:
        """
        Stream completion responses in real-time.

        Args:
            prompt: Input prompt
            **kwargs: Provider-specific options (same as complete())

        Yields:
            Text chunks as they arrive from the provider

        Raises:
            NotImplementedError: If provider doesn't support streaming
            ValueError: If prompt is empty or invalid
            RuntimeError: If API call fails

        Example:
            async for chunk in adapter.stream_complete("Write a story"):
                print(chunk, end='', flush=True)
        """
        pass

    @abstractmethod
    def supports_streaming(self) -> bool:
        """
        Check if provider supports streaming responses.

        Returns:
            True if streaming is supported, False otherwise
        """
        pass

    @abstractmethod
    async def get_model_info(self) -> Dict[str, Any]:
        """
        Get model capabilities and limits.

        Returns:
            Dict with provider metadata:
                provider: Provider name
                model: Model identifier
                max_tokens: Maximum context window
                supports_streaming: Boolean
                supports_vision: Boolean (if applicable)
                supports_function_calling: Boolean (if applicable)

        Example:
            {
                "provider": "anthropic",
                "model": "claude-3-sonnet",
                "max_tokens": 200000,
                "supports_streaming": True,
                "supports_vision": True,
                "supports_function_calling": True
            }
        """
        pass

    def get_provider_name(self) -> str:
        """
        Get provider name from adapter class.

        Default implementation extracts from class name.
        Override if custom naming needed.

        Returns:
            Provider name in lowercase (e.g., "anthropic", "openai")
        """
        return self.__class__.__name__.replace("Adapter", "").lower()

    async def health_check(self) -> bool:
        """
        Verify provider connectivity and credentials.

        Optional method that adapters can override for health checks.
        Default implementation attempts a minimal completion.

        Returns:
            True if provider is healthy, False otherwise
        """
        try:
            response = await self.complete("test", max_tokens=1)
            return bool(response.content)
        except Exception:
            return False

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"{self.__class__.__name__}(model={self.model}, provider={self.get_provider_name()})"
