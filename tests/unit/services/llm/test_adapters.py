"""
Tests for LLM Adapters (Pattern-012)

Tests the adapter pattern implementation across all 4 providers:
Anthropic Claude, OpenAI GPT, Google Gemini, and Perplexity.

Test Coverage:
- Factory pattern (creation, registration, listing)
- Adapter initialization
- Model info retrieval
- Error handling
- Provider enum mapping
"""

import pytest

from services.llm.adapters import (
    ClaudeAdapter,
    GeminiAdapter,
    LLMAdapter,
    LLMFactory,
    LLMResponse,
    OpenAIAdapter,
    PerplexityAdapter,
)
from services.llm.config import LLMProvider


class TestLLMFactory:
    """Test LLM Factory pattern"""

    def test_factory_lists_providers(self):
        """Factory should list all 4 providers"""
        providers = LLMFactory.list_providers()
        assert len(providers) == 4, f"Expected 4 providers, got {len(providers)}"
        assert LLMProvider.ANTHROPIC in providers
        assert LLMProvider.OPENAI in providers
        assert LLMProvider.GEMINI in providers
        assert LLMProvider.PERPLEXITY in providers

    def test_factory_creates_claude_adapter(self):
        """Factory should create ClaudeAdapter for ANTHROPIC provider"""
        adapter = LLMFactory.create(
            provider=LLMProvider.ANTHROPIC,
            api_key="test-key-anthropic",
            model="claude-3-sonnet",
        )
        assert isinstance(adapter, ClaudeAdapter)
        assert adapter.model == "claude-3-sonnet"
        assert adapter.get_provider_name() == "claude"

    def test_factory_creates_openai_adapter(self):
        """Factory should create OpenAIAdapter for OPENAI provider"""
        adapter = LLMFactory.create(
            provider=LLMProvider.OPENAI, api_key="test-key-openai", model="gpt-4"
        )
        assert isinstance(adapter, OpenAIAdapter)
        assert adapter.model == "gpt-4"
        assert adapter.get_provider_name() == "openai"

    def test_factory_creates_gemini_adapter(self):
        """Factory should create GeminiAdapter for GEMINI provider"""
        try:
            adapter = LLMFactory.create(
                provider=LLMProvider.GEMINI,
                api_key="test-key-gemini",
                model="gemini-pro",
            )
            assert isinstance(adapter, GeminiAdapter)
            assert adapter.model == "gemini-pro"
            assert adapter.get_provider_name() == "gemini"
        except ImportError:
            pytest.skip("google-generativeai not installed")

    def test_factory_creates_perplexity_adapter(self):
        """Factory should create PerplexityAdapter for PERPLEXITY provider"""
        adapter = LLMFactory.create(
            provider=LLMProvider.PERPLEXITY,
            api_key="test-key-perplexity",
            model="pplx-70b-online",
        )
        assert isinstance(adapter, PerplexityAdapter)
        assert adapter.model == "pplx-70b-online"
        assert adapter.get_provider_name() == "perplexity"

    def test_factory_supports_provider_check(self):
        """Factory should correctly check provider support"""
        assert LLMFactory.supports_provider(LLMProvider.ANTHROPIC) is True
        assert LLMFactory.supports_provider(LLMProvider.OPENAI) is True
        assert LLMFactory.supports_provider(LLMProvider.GEMINI) is True
        assert LLMFactory.supports_provider(LLMProvider.PERPLEXITY) is True

    def test_factory_get_adapter_class(self):
        """Factory should return correct adapter classes"""
        assert LLMFactory.get_adapter_class(LLMProvider.ANTHROPIC) == ClaudeAdapter
        assert LLMFactory.get_adapter_class(LLMProvider.OPENAI) == OpenAIAdapter
        # Gemini and Perplexity
        try:
            assert LLMFactory.get_adapter_class(LLMProvider.GEMINI) == GeminiAdapter
        except ImportError:
            pass  # Skip if not installed
        assert LLMFactory.get_adapter_class(LLMProvider.PERPLEXITY) == PerplexityAdapter

    def test_factory_get_provider_info(self):
        """Factory should return provider information"""
        info = LLMFactory.get_provider_info()
        assert len(info) == 4
        assert "anthropic" in info
        assert "openai" in info
        assert "gemini" in info
        assert "perplexity" in info

        # Check structure
        assert "provider" in info["anthropic"]
        assert "adapter_class" in info["anthropic"]
        assert info["anthropic"]["adapter_class"] == "ClaudeAdapter"


class TestClaudeAdapter:
    """Test Claude adapter"""

    @pytest.mark.asyncio
    async def test_adapter_initialization(self):
        """Adapter should initialize with config"""
        adapter = ClaudeAdapter(api_key="test-key", model="claude-3-sonnet")

        assert adapter.model == "claude-3-sonnet"
        assert adapter.api_key == "test-key"
        assert adapter.supports_streaming() is True

    @pytest.mark.asyncio
    async def test_get_model_info(self):
        """Adapter should return model info"""
        adapter = ClaudeAdapter(api_key="test-key", model="claude-3-sonnet")
        info = await adapter.get_model_info()

        assert info["provider"] == "anthropic"
        assert info["model"] == "claude-3-sonnet"
        assert info["supports_streaming"] is True
        assert info["supports_vision"] is True
        assert info["max_tokens"] > 0

    def test_adapter_validation(self):
        """Adapter should validate required parameters"""
        # Empty API key should raise ValueError
        with pytest.raises(ValueError, match="API key is required"):
            ClaudeAdapter(api_key="", model="claude-3-sonnet")

        # Empty model should raise ValueError
        with pytest.raises(ValueError, match="Model name is required"):
            ClaudeAdapter(api_key="test-key", model="")

    def test_adapter_repr(self):
        """Adapter should have useful string representation"""
        adapter = ClaudeAdapter(api_key="test-key", model="claude-3-sonnet")
        repr_str = repr(adapter)

        assert "ClaudeAdapter" in repr_str
        assert "claude-3-sonnet" in repr_str
        assert "claude" in repr_str.lower()


class TestOpenAIAdapter:
    """Test OpenAI adapter"""

    @pytest.mark.asyncio
    async def test_adapter_initialization(self):
        """Adapter should initialize with config"""
        adapter = OpenAIAdapter(api_key="test-key", model="gpt-4")

        assert adapter.model == "gpt-4"
        assert adapter.api_key == "test-key"
        assert adapter.supports_streaming() is True

    @pytest.mark.asyncio
    async def test_get_model_info(self):
        """Adapter should return model info"""
        adapter = OpenAIAdapter(api_key="test-key", model="gpt-4-turbo-preview")
        info = await adapter.get_model_info()

        assert info["provider"] == "openai"
        assert info["model"] == "gpt-4-turbo-preview"
        assert info["supports_streaming"] is True
        assert info["supports_function_calling"] is True
        assert info["max_tokens"] > 0


class TestGeminiAdapter:
    """Test Gemini adapter"""

    @pytest.mark.asyncio
    async def test_adapter_initialization(self):
        """Adapter should initialize with config"""
        try:
            import google.generativeai

            adapter = GeminiAdapter(api_key="test-key", model="gemini-pro")

            assert adapter.model == "gemini-pro"
            assert adapter.api_key == "test-key"
            assert adapter.supports_streaming() is True
        except ImportError:
            pytest.skip("google-generativeai not installed")

    @pytest.mark.asyncio
    async def test_get_model_info(self):
        """Adapter should return model info"""
        try:
            import google.generativeai

            adapter = GeminiAdapter(api_key="test-key", model="gemini-pro")
            info = await adapter.get_model_info()

            assert info["provider"] == "gemini"
            assert info["model"] == "gemini-pro"
            assert info["supports_streaming"] is True
            assert info["max_tokens"] > 0
        except ImportError:
            pytest.skip("google-generativeai not installed")


class TestPerplexityAdapter:
    """Test Perplexity adapter"""

    @pytest.mark.asyncio
    async def test_adapter_initialization(self):
        """Adapter should initialize with config"""
        adapter = PerplexityAdapter(api_key="test-key", model="pplx-70b-online")

        assert adapter.model == "pplx-70b-online"
        assert adapter.api_key == "test-key"
        assert adapter.supports_streaming() is True

    @pytest.mark.asyncio
    async def test_get_model_info(self):
        """Adapter should return model info"""
        adapter = PerplexityAdapter(api_key="test-key", model="pplx-70b-online")
        info = await adapter.get_model_info()

        assert info["provider"] == "perplexity"
        assert info["model"] == "pplx-70b-online"
        assert info["supports_streaming"] is True
        assert info["supports_online_search"] is True
        assert "online" in info["model"]


class TestLLMResponse:
    """Test LLMResponse dataclass"""

    def test_llm_response_creation(self):
        """LLMResponse should be created with required fields"""
        response = LLMResponse(
            content="Hello, world!",
            model="claude-3-sonnet",
            provider="anthropic",
            usage={"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
            metadata={"finish_reason": "stop"},
        )

        assert response.content == "Hello, world!"
        assert response.model == "claude-3-sonnet"
        assert response.provider == "anthropic"
        assert response.usage["total_tokens"] == 15
        assert response.metadata["finish_reason"] == "stop"

    def test_llm_response_defaults(self):
        """LLMResponse should use empty dicts for optional fields"""
        response = LLMResponse(content="Test", model="test-model", provider="test-provider")

        assert response.usage == {}
        assert response.metadata == {}


class TestAdapterInterface:
    """Test that all adapters implement required interface"""

    def get_test_adapters(self):
        """Get list of adapters to test"""
        adapters = [
            ClaudeAdapter(api_key="test", model="claude-3-sonnet"),
            OpenAIAdapter(api_key="test", model="gpt-4"),
            PerplexityAdapter(api_key="test", model="pplx-70b-online"),
        ]

        # Add Gemini if available
        try:
            adapters.append(GeminiAdapter(api_key="test", model="gemini-pro"))
        except ImportError:
            pass

        return adapters

    def test_all_adapters_have_required_methods(self):
        """All adapters should implement required abstract methods"""
        required_methods = [
            "complete",
            "classify",
            "stream_complete",
            "supports_streaming",
            "get_model_info",
        ]

        for adapter in self.get_test_adapters():
            for method_name in required_methods:
                assert hasattr(
                    adapter, method_name
                ), f"{adapter.__class__.__name__} missing {method_name}"
                assert callable(getattr(adapter, method_name))

    def test_all_adapters_inherit_from_base(self):
        """All adapters should inherit from LLMAdapter"""
        for adapter in self.get_test_adapters():
            assert isinstance(adapter, LLMAdapter)

    def test_all_adapters_have_provider_name(self):
        """All adapters should return provider name"""
        for adapter in self.get_test_adapters():
            provider_name = adapter.get_provider_name()
            assert isinstance(provider_name, str)
            assert len(provider_name) > 0
