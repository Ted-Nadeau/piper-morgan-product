"""
LLM Adapters - Pattern-012 Implementation

Vendor-agnostic interface for multiple LLM providers.

This module implements Pattern-012 (LLM Adapter Pattern) to provide
a consistent interface across Anthropic, OpenAI, Gemini, and Perplexity.

Usage:
    # Via factory (recommended)
    from services.llm.adapters import LLMFactory
    from services.llm.config import LLMProvider

    adapter = LLMFactory.create(
        provider=LLMProvider.ANTHROPIC,
        api_key="sk-ant-...",
        model="claude-3-sonnet"
    )
    response = await adapter.complete("Hello, world!")

    # Direct instantiation
    from services.llm.adapters import ClaudeAdapter

    adapter = ClaudeAdapter(api_key="sk-ant-...", model="claude-3-sonnet")
    response = await adapter.complete("Hello, world!")

    # Streaming
    async for chunk in adapter.stream_complete("Tell me a story"):
        print(chunk, end='', flush=True)

    # Classification
    category, confidence = await adapter.classify(
        text="This app crashed",
        categories=["bug_report", "feature_request", "question"]
    )

Available Adapters:
    - ClaudeAdapter: Anthropic Claude models (Opus, Sonnet, Haiku)
    - OpenAIAdapter: OpenAI GPT models (GPT-4, GPT-3.5)
    - GeminiAdapter: Google Gemini models (Pro, Ultra)
    - PerplexityAdapter: Perplexity AI models (online search capable)

Pattern-012: LLM Adapter Pattern
See: docs/internal/architecture/current/patterns/pattern-012-llm-adapter.md
"""

from .base import LLMAdapter, LLMResponse
from .claude_adapter import ClaudeAdapter
from .openai_adapter import OpenAIAdapter
from .gemini_adapter import GeminiAdapter
from .perplexity_adapter import PerplexityAdapter
from .factory import LLMFactory

__all__ = [
    # Base classes
    "LLMAdapter",
    "LLMResponse",
    # Adapters
    "ClaudeAdapter",
    "OpenAIAdapter",
    "GeminiAdapter",
    "PerplexityAdapter",
    # Factory
    "LLMFactory",
]

# Version info
__version__ = "1.0.0"
__pattern__ = "pattern-012"
