"""
Claude/Anthropic LLM Adapter

Wraps Anthropic SDK in Pattern-012 compliant interface for vendor-agnostic access.
Uses native Anthropic Python SDK for Claude models (Opus, Sonnet, Haiku).

Pattern-012: LLM Adapter Pattern
See: docs/internal/architecture/current/patterns/pattern-012-llm-adapter.md
"""

from typing import Any, AsyncIterator, Dict, List, Tuple

import structlog
from anthropic import Anthropic, AsyncAnthropic

from .base import LLMAdapter, LLMResponse

logger = structlog.get_logger()


class ClaudeAdapter(LLMAdapter):
    """
    Adapter for Anthropic's Claude models.

    Provides Pattern-012 compliant interface on top of the Anthropic SDK.
    Supports all Claude 3 models: Opus, Sonnet, and Haiku.

    Supported models:
        - claude-3-opus-20240229 (most capable)
        - claude-sonnet-4-20250514 (best balance, newest)
        - claude-3-5-sonnet-20241022 (previous version, deprecated)
        - claude-3-haiku-20240307 (fastest, most affordable)

    Features:
        - Streaming support
        - Vision capabilities (image input)
        - Function/tool calling
        - JSON mode via prompt engineering
        - 200K token context window (Claude 3.5)

    Example:
        adapter = ClaudeAdapter(
            api_key="sk-ant-...",
            model="claude-sonnet-4-20250514"
        )
        response = await adapter.complete("Explain quantum computing")
        print(response.content)
    """

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514", **kwargs):
        """
        Initialize Claude adapter.

        Args:
            api_key: Anthropic API key (starts with sk-ant-)
            model: Claude model identifier
            **kwargs: Additional config (timeout, max_retries, etc.)

        Raises:
            ValueError: If API key or model is invalid
        """
        super().__init__(api_key, model, **kwargs)

        # Initialize Anthropic async client
        self._client = AsyncAnthropic(
            api_key=api_key,
            timeout=kwargs.get("timeout", 60.0),
            max_retries=kwargs.get("max_retries", 2),
        )

        logger.info(
            "claude_adapter_initialized",
            model=model,
            timeout=kwargs.get("timeout", 60.0),
        )

    async def complete(self, prompt: str, **kwargs) -> LLMResponse:
        """
        Generate completion using Claude.

        Args:
            prompt: Input prompt
            **kwargs:
                max_tokens: Max tokens to generate (default: 1000)
                temperature: Sampling temperature 0.0-1.0 (default: 0.7)
                top_p: Nucleus sampling (default: None)
                stop_sequences: List of stop sequences (default: None)
                system: System prompt (default: None)

        Returns:
            LLMResponse with completion

        Raises:
            ValueError: If prompt is empty
            RuntimeError: If API call fails
        """
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        try:
            # Build messages list
            messages = [{"role": "user", "content": prompt}]

            # Extract system prompt if provided
            system_prompt = kwargs.pop("system", None)

            # Create API request
            request_params = {
                "model": self.model,
                "max_tokens": kwargs.get("max_tokens", 1000),
                "temperature": kwargs.get("temperature", 0.7),
                "messages": messages,
            }

            # Add optional parameters
            if system_prompt:
                request_params["system"] = system_prompt
            if kwargs.get("top_p"):
                request_params["top_p"] = kwargs["top_p"]
            if kwargs.get("stop_sequences"):
                request_params["stop_sequences"] = kwargs["stop_sequences"]

            logger.debug("claude_api_request", model=self.model, prompt_length=len(prompt))

            # Make API call
            response = await self._client.messages.create(**request_params)

            # Log usage
            logger.info(
                "claude_completion",
                model=self.model,
                input_tokens=response.usage.input_tokens,
                output_tokens=response.usage.output_tokens,
                stop_reason=response.stop_reason,
            )

            # Convert to standardized format
            return LLMResponse(
                content=response.content[0].text,
                model=self.model,
                provider="anthropic",
                usage={
                    "prompt_tokens": response.usage.input_tokens,
                    "completion_tokens": response.usage.output_tokens,
                    "total_tokens": response.usage.input_tokens + response.usage.output_tokens,
                },
                metadata={
                    "finish_reason": response.stop_reason,
                    "response_id": response.id,
                    "model_version": response.model,
                },
            )

        except Exception as e:
            logger.error("claude_completion_failed", error=str(e), model=self.model)
            raise RuntimeError(f"Claude API call failed: {str(e)}") from e

    async def classify(self, text: str, categories: List[str]) -> Tuple[str, float]:
        """
        Classify text using Claude with confidence score.

        Args:
            text: Text to classify
            categories: List of possible categories

        Returns:
            Tuple of (category_name, confidence_score)

        Raises:
            ValueError: If text or categories empty
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        if not categories:
            raise ValueError("Categories list cannot be empty")

        prompt = f"""Classify the following text into exactly one of these categories: {', '.join(categories)}

Text to classify:
{text}

Respond with ONLY this format (no other text):
category_name:confidence_score

Where confidence_score is a number between 0.0 and 1.0.
Example: bug_report:0.92"""

        try:
            response = await self.complete(prompt, max_tokens=50, temperature=0.0)
            parts = response.content.strip().split(":")

            if len(parts) != 2:
                logger.warning(
                    "claude_classification_parse_failed",
                    response=response.content,
                    expected_format="category:score",
                )
                # Return first category with low confidence as fallback
                return categories[0], 0.1

            category = parts[0].strip()
            try:
                confidence = float(parts[1].strip())
                # Clamp confidence to valid range
                confidence = max(0.0, min(1.0, confidence))
            except ValueError:
                logger.warning("claude_confidence_parse_failed", confidence_str=parts[1])
                confidence = 0.5

            # Validate category is in the list
            if category not in categories:
                logger.warning(
                    "claude_invalid_category", category=category, valid_categories=categories
                )
                # Find closest match or use first category
                category = categories[0]
                confidence = 0.3

            return category, confidence

        except Exception as e:
            logger.error("claude_classification_failed", error=str(e))
            # Return fallback
            return categories[0], 0.0

    async def stream_complete(self, prompt: str, **kwargs) -> AsyncIterator[str]:
        """
        Stream completion from Claude in real-time.

        Args:
            prompt: Input prompt
            **kwargs: Same as complete() method

        Yields:
            Text chunks as they arrive

        Raises:
            ValueError: If prompt is empty
            RuntimeError: If API call fails
        """
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        try:
            # Build request (same as complete())
            messages = [{"role": "user", "content": prompt}]
            system_prompt = kwargs.pop("system", None)

            request_params = {
                "model": self.model,
                "max_tokens": kwargs.get("max_tokens", 1000),
                "temperature": kwargs.get("temperature", 0.7),
                "messages": messages,
                "stream": True,  # Enable streaming
            }

            if system_prompt:
                request_params["system"] = system_prompt
            if kwargs.get("top_p"):
                request_params["top_p"] = kwargs["top_p"]
            if kwargs.get("stop_sequences"):
                request_params["stop_sequences"] = kwargs["stop_sequences"]

            logger.debug("claude_stream_request", model=self.model)

            # Stream the response
            async with self._client.messages.stream(**request_params) as stream:
                async for text in stream.text_stream:
                    yield text

            logger.info("claude_stream_complete", model=self.model)

        except Exception as e:
            logger.error("claude_stream_failed", error=str(e))
            raise RuntimeError(f"Claude streaming failed: {str(e)}") from e

    def supports_streaming(self) -> bool:
        """Claude supports streaming responses."""
        return True

    async def get_model_info(self) -> Dict[str, Any]:
        """
        Get Claude model capabilities.

        Returns:
            Dict with model metadata
        """
        # Determine context window based on model
        if "opus" in self.model.lower():
            max_tokens = 200000
            tier = "most_capable"
        elif "sonnet" in self.model.lower():
            max_tokens = 200000
            tier = "balanced"
        elif "haiku" in self.model.lower():
            max_tokens = 200000
            tier = "fastest"
        else:
            max_tokens = 200000
            tier = "unknown"

        return {
            "provider": "anthropic",
            "model": self.model,
            "max_tokens": max_tokens,
            "supports_streaming": True,
            "supports_vision": True,  # All Claude 3 models support vision
            "supports_function_calling": True,  # Tool use supported
            "tier": tier,
            "context_window": max_tokens,
        }

    async def health_check(self) -> bool:
        """
        Verify Claude API connectivity.

        Returns:
            True if API is accessible
        """
        try:
            response = await self.complete("test", max_tokens=5, temperature=0.0)
            return len(response.content) > 0
        except Exception as e:
            logger.warning("claude_health_check_failed", error=str(e))
            return False
