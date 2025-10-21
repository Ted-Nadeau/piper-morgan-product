"""
Google Gemini LLM Adapter

Wraps Google Gemini SDK in Pattern-012 compliant interface for vendor-agnostic access.
Uses Google's generativeai Python SDK for Gemini Pro and Ultra models.

Pattern-012: LLM Adapter Pattern
See: docs/internal/architecture/current/patterns/pattern-012-llm-adapter.md
"""

from typing import List, Tuple, AsyncIterator, Dict, Any
import structlog

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None

from .base import LLMAdapter, LLMResponse

logger = structlog.get_logger()


class GeminiAdapter(LLMAdapter):
    """
    Adapter for Google's Gemini models.

    Provides Pattern-012 compliant interface on top of the Google Generative AI SDK.
    Supports Gemini Pro, Gemini Pro Vision, and Gemini Ultra.

    Supported models:
        - gemini-pro (text generation)
        - gemini-pro-vision (multimodal with vision)
        - gemini-ultra (most capable, limited access)

    Features:
        - Streaming support
        - Vision capabilities (Pro Vision model)
        - Function/tool calling
        - 32K token context window
        - Fast inference

    Example:
        adapter = GeminiAdapter(
            api_key="AIza...",
            model="gemini-pro"
        )
        response = await adapter.complete("Explain quantum computing")
        print(response.content)

    Note:
        Requires google-generativeai package:
        pip install google-generativeai>=0.3.0
    """

    def __init__(self, api_key: str, model: str = "gemini-pro", **kwargs):
        """
        Initialize Gemini adapter.

        Args:
            api_key: Google AI API key
            model: Gemini model identifier
            **kwargs: Additional config (timeout, etc.)

        Raises:
            ImportError: If google-generativeai not installed
            ValueError: If API key or model is invalid
        """
        if not GEMINI_AVAILABLE:
            raise ImportError(
                "google-generativeai package not installed. "
                "Install with: pip install google-generativeai>=0.3.0"
            )

        super().__init__(api_key, model, **kwargs)

        # Configure Gemini SDK with API key
        genai.configure(api_key=api_key)

        # Initialize model
        self._model = genai.GenerativeModel(model)

        # Store config
        self._generation_config = genai.types.GenerationConfig(
            temperature=kwargs.get("temperature", 0.7),
            top_p=kwargs.get("top_p", 0.95),
            top_k=kwargs.get("top_k", 40),
            max_output_tokens=kwargs.get("max_output_tokens", 1000),
        )

        logger.info("gemini_adapter_initialized", model=model)

    async def complete(self, prompt: str, **kwargs) -> LLMResponse:
        """
        Generate completion using Gemini.

        Args:
            prompt: Input prompt
            **kwargs:
                max_tokens: Max tokens to generate (default: 1000)
                temperature: Sampling temperature 0.0-1.0 (default: 0.7)
                top_p: Nucleus sampling (default: 0.95)
                top_k: Top-k sampling (default: 40)
                stop_sequences: List of stop sequences (default: None)

        Returns:
            LLMResponse with completion

        Raises:
            ValueError: If prompt is empty
            RuntimeError: If API call fails
        """
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        try:
            # Build generation config
            generation_config = genai.types.GenerationConfig(
                temperature=kwargs.get("temperature", 0.7),
                top_p=kwargs.get("top_p", 0.95),
                top_k=kwargs.get("top_k", 40),
                max_output_tokens=kwargs.get("max_tokens", 1000),
            )

            # Add stop sequences if provided
            if kwargs.get("stop_sequences"):
                generation_config.stop_sequences = kwargs["stop_sequences"]

            logger.debug("gemini_api_request", model=self.model, prompt_length=len(prompt))

            # Make API call (sync - Gemini SDK doesn't have async by default)
            # We'll run it in executor to avoid blocking
            response = await self._model.generate_content_async(
                prompt, generation_config=generation_config
            )

            # Extract usage metadata
            usage = {}
            if hasattr(response, "usage_metadata") and response.usage_metadata:
                usage = {
                    "prompt_tokens": response.usage_metadata.prompt_token_count,
                    "completion_tokens": response.usage_metadata.candidates_token_count,
                    "total_tokens": response.usage_metadata.total_token_count,
                }

            # Log usage
            logger.info(
                "gemini_completion",
                model=self.model,
                prompt_tokens=usage.get("prompt_tokens", 0),
                completion_tokens=usage.get("completion_tokens", 0),
            )

            # Extract finish reason
            finish_reason = "unknown"
            if response.candidates and len(response.candidates) > 0:
                finish_reason = str(response.candidates[0].finish_reason)

            # Convert to standardized format
            return LLMResponse(
                content=response.text,
                model=self.model,
                provider="gemini",
                usage=usage,
                metadata={
                    "finish_reason": finish_reason,
                    "safety_ratings": (
                        str(response.candidates[0].safety_ratings)
                        if response.candidates
                        else None
                    ),
                },
            )

        except Exception as e:
            logger.error("gemini_completion_failed", error=str(e), model=self.model)
            raise RuntimeError(f"Gemini API call failed: {str(e)}") from e

    async def classify(self, text: str, categories: List[str]) -> Tuple[str, float]:
        """
        Classify text using Gemini with confidence score.

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
                    "gemini_classification_parse_failed",
                    response=response.content,
                    expected_format="category:score",
                )
                return categories[0], 0.1

            category = parts[0].strip()
            try:
                confidence = float(parts[1].strip())
                confidence = max(0.0, min(1.0, confidence))
            except ValueError:
                logger.warning("gemini_confidence_parse_failed", confidence_str=parts[1])
                confidence = 0.5

            # Validate category
            if category not in categories:
                logger.warning(
                    "gemini_invalid_category", category=category, valid_categories=categories
                )
                category = categories[0]
                confidence = 0.3

            return category, confidence

        except Exception as e:
            logger.error("gemini_classification_failed", error=str(e))
            return categories[0], 0.0

    async def stream_complete(self, prompt: str, **kwargs) -> AsyncIterator[str]:
        """
        Stream completion from Gemini in real-time.

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
            # Build generation config
            generation_config = genai.types.GenerationConfig(
                temperature=kwargs.get("temperature", 0.7),
                top_p=kwargs.get("top_p", 0.95),
                top_k=kwargs.get("top_k", 40),
                max_output_tokens=kwargs.get("max_tokens", 1000),
            )

            if kwargs.get("stop_sequences"):
                generation_config.stop_sequences = kwargs["stop_sequences"]

            logger.debug("gemini_stream_request", model=self.model)

            # Stream the response
            response = await self._model.generate_content_async(
                prompt, generation_config=generation_config, stream=True
            )

            async for chunk in response:
                if chunk.text:
                    yield chunk.text

            logger.info("gemini_stream_complete", model=self.model)

        except Exception as e:
            logger.error("gemini_stream_failed", error=str(e))
            raise RuntimeError(f"Gemini streaming failed: {str(e)}") from e

    def supports_streaming(self) -> bool:
        """Gemini supports streaming responses."""
        return True

    async def get_model_info(self) -> Dict[str, Any]:
        """
        Get Gemini model capabilities.

        Returns:
            Dict with model metadata
        """
        # Determine capabilities based on model name
        model_lower = self.model.lower()

        if "ultra" in model_lower:
            max_tokens = 32000
            tier = "ultra"
            supports_vision = False
        elif "vision" in model_lower:
            max_tokens = 16000
            tier = "pro_vision"
            supports_vision = True
        elif "pro" in model_lower:
            max_tokens = 32000
            tier = "pro"
            supports_vision = False
        else:
            max_tokens = 32000
            tier = "standard"
            supports_vision = False

        return {
            "provider": "gemini",
            "model": self.model,
            "max_tokens": max_tokens,
            "supports_streaming": True,
            "supports_vision": supports_vision,
            "supports_function_calling": True,  # Gemini supports function calling
            "tier": tier,
            "context_window": max_tokens,
        }

    async def health_check(self) -> bool:
        """
        Verify Gemini API connectivity.

        Returns:
            True if API is accessible
        """
        try:
            response = await self.complete("test", max_tokens=5, temperature=0.0)
            return len(response.content) > 0
        except Exception as e:
            logger.warning("gemini_health_check_failed", error=str(e))
            return False
