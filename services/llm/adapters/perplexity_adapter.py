"""
Perplexity AI LLM Adapter

Wraps Perplexity AI API in Pattern-012 compliant interface for vendor-agnostic access.
Uses OpenAI-compatible API with Perplexity endpoint.

Pattern-012: LLM Adapter Pattern
See: docs/internal/architecture/current/patterns/pattern-012-llm-adapter.md
"""

from typing import List, Tuple, AsyncIterator, Dict, Any
import structlog
from openai import AsyncOpenAI

from .base import LLMAdapter, LLMResponse

logger = structlog.get_logger()


class PerplexityAdapter(LLMAdapter):
    """
    Adapter for Perplexity AI models.

    Provides Pattern-012 compliant interface on top of Perplexity's API.
    Perplexity uses OpenAI-compatible endpoints, so this adapter leverages
    the OpenAI SDK with a custom base URL.

    Supported models:
        - pplx-70b-online (70B with web search)
        - pplx-7b-online (7B with web search)
        - pplx-70b-chat (70B chat only)
        - pplx-7b-chat (7B chat only)

    Features:
        - Online models search the web in real-time
        - Up-to-date information retrieval
        - Streaming support
        - Citations and sources
        - Conversational interface

    Example:
        adapter = PerplexityAdapter(
            api_key="pplx-...",
            model="pplx-70b-online"
        )
        response = await adapter.complete("What happened today in tech?")
        print(response.content)  # Includes recent web-sourced info

    Note:
        - Online models can access current web information
        - Responses may include citations
        - Rate limits may differ from OpenAI
    """

    def __init__(self, api_key: str, model: str = "pplx-70b-online", **kwargs):
        """
        Initialize Perplexity adapter.

        Args:
            api_key: Perplexity API key (starts with pplx-)
            model: Perplexity model identifier
            **kwargs: Additional config (timeout, max_retries, etc.)

        Raises:
            ValueError: If API key or model is invalid
        """
        super().__init__(api_key, model, **kwargs)

        # Initialize OpenAI client with Perplexity endpoint
        self._client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://api.perplexity.ai",
            timeout=kwargs.get("timeout", 60.0),
            max_retries=kwargs.get("max_retries", 2),
        )

        logger.info(
            "perplexity_adapter_initialized",
            model=model,
            online_search="online" in model.lower(),
        )

    async def complete(self, prompt: str, **kwargs) -> LLMResponse:
        """
        Generate completion using Perplexity.

        Args:
            prompt: Input prompt
            **kwargs:
                max_tokens: Max tokens to generate (default: 1000)
                temperature: Sampling temperature 0.0-2.0 (default: 0.7)
                top_p: Nucleus sampling (default: None)
                return_citations: Include sources (default: False)
                return_images: Include images in response (default: False)

        Returns:
            LLMResponse with completion

        Raises:
            ValueError: If prompt is empty
            RuntimeError: If API call fails

        Note:
            For online models, the response may include web search results
            and citations in the metadata.
        """
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        try:
            # Build messages
            messages = [{"role": "user", "content": prompt}]

            # Build request parameters
            request_params = {
                "model": self.model,
                "messages": messages,
                "max_tokens": kwargs.get("max_tokens", 1000),
                "temperature": kwargs.get("temperature", 0.7),
            }

            # Add optional parameters
            if kwargs.get("top_p") is not None:
                request_params["top_p"] = kwargs["top_p"]
            if kwargs.get("return_citations"):
                request_params["return_citations"] = True
            if kwargs.get("return_images"):
                request_params["return_images"] = True

            logger.debug(
                "perplexity_api_request",
                model=self.model,
                prompt_length=len(prompt),
                online="online" in self.model.lower(),
            )

            # Make API call
            response = await self._client.chat.completions.create(**request_params)

            # Extract citations if present
            citations = []
            if hasattr(response, "citations") and response.citations:
                citations = response.citations

            # Log usage
            logger.info(
                "perplexity_completion",
                model=self.model,
                prompt_tokens=response.usage.prompt_tokens if response.usage else 0,
                completion_tokens=response.usage.completion_tokens if response.usage else 0,
                has_citations=len(citations) > 0,
            )

            # Convert to standardized format
            return LLMResponse(
                content=response.choices[0].message.content or "",
                model=self.model,
                provider="perplexity",
                usage={
                    "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                    "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                    "total_tokens": response.usage.total_tokens if response.usage else 0,
                },
                metadata={
                    "finish_reason": response.choices[0].finish_reason,
                    "response_id": response.id,
                    "model_version": response.model,
                    "citations": citations,
                    "online_search": "online" in self.model.lower(),
                },
            )

        except Exception as e:
            logger.error("perplexity_completion_failed", error=str(e), model=self.model)
            raise RuntimeError(f"Perplexity API call failed: {str(e)}") from e

    async def classify(self, text: str, categories: List[str]) -> Tuple[str, float]:
        """
        Classify text using Perplexity with confidence score.

        Args:
            text: Text to classify
            categories: List of possible categories

        Returns:
            Tuple of (category_name, confidence_score)

        Raises:
            ValueError: If text or categories empty

        Note:
            For classification, chat models (non-online) are recommended
            for faster, cheaper responses.
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
                    "perplexity_classification_parse_failed",
                    response=response.content,
                    expected_format="category:score",
                )
                return categories[0], 0.1

            category = parts[0].strip()
            try:
                confidence = float(parts[1].strip())
                confidence = max(0.0, min(1.0, confidence))
            except ValueError:
                logger.warning("perplexity_confidence_parse_failed", confidence_str=parts[1])
                confidence = 0.5

            # Validate category
            if category not in categories:
                logger.warning(
                    "perplexity_invalid_category", category=category, valid_categories=categories
                )
                category = categories[0]
                confidence = 0.3

            return category, confidence

        except Exception as e:
            logger.error("perplexity_classification_failed", error=str(e))
            return categories[0], 0.0

    async def stream_complete(self, prompt: str, **kwargs) -> AsyncIterator[str]:
        """
        Stream completion from Perplexity in real-time.

        Args:
            prompt: Input prompt
            **kwargs: Same as complete() method

        Yields:
            Text chunks as they arrive

        Raises:
            ValueError: If prompt is empty
            RuntimeError: If API call fails

        Note:
            Streaming is supported but citations may not be available
            until the full response is complete.
        """
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        try:
            messages = [{"role": "user", "content": prompt}]

            request_params = {
                "model": self.model,
                "messages": messages,
                "max_tokens": kwargs.get("max_tokens", 1000),
                "temperature": kwargs.get("temperature", 0.7),
                "stream": True,  # Enable streaming
            }

            # Add optional parameters
            if kwargs.get("top_p") is not None:
                request_params["top_p"] = kwargs["top_p"]

            logger.debug("perplexity_stream_request", model=self.model)

            # Stream the response
            stream = await self._client.chat.completions.create(**request_params)

            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

            logger.info("perplexity_stream_complete", model=self.model)

        except Exception as e:
            logger.error("perplexity_stream_failed", error=str(e))
            raise RuntimeError(f"Perplexity streaming failed: {str(e)}") from e

    def supports_streaming(self) -> bool:
        """Perplexity supports streaming responses."""
        return True

    async def get_model_info(self) -> Dict[str, Any]:
        """
        Get Perplexity model capabilities.

        Returns:
            Dict with model metadata
        """
        # Determine capabilities based on model name
        model_lower = self.model.lower()

        if "70b" in model_lower:
            size = "70B"
            max_tokens = 4096  # Perplexity context window
        elif "7b" in model_lower:
            size = "7B"
            max_tokens = 4096
        else:
            size = "unknown"
            max_tokens = 4096

        is_online = "online" in model_lower

        return {
            "provider": "perplexity",
            "model": self.model,
            "max_tokens": max_tokens,
            "supports_streaming": True,
            "supports_vision": False,  # Perplexity doesn't support vision
            "supports_function_calling": False,  # No function calling
            "supports_online_search": is_online,  # Key differentiator
            "size": size,
            "context_window": max_tokens,
            "online_model": is_online,
        }

    async def health_check(self) -> bool:
        """
        Verify Perplexity API connectivity.

        Returns:
            True if API is accessible
        """
        try:
            response = await self.complete("test", max_tokens=5, temperature=0.0)
            return len(response.content) > 0
        except Exception as e:
            logger.warning("perplexity_health_check_failed", error=str(e))
            return False
