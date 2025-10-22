# Implementation Prompt: CORE-LLM-SUPPORT (#237)

**Agent**: Claude Code (Programmer)
**Task**: Implement Pattern-012 LLM Adapter layer for 4-provider integration
**Issue**: #237 CORE-LLM-SUPPORT
**Estimated Duration**: 3.5 hours
**Date**: October 21, 2025, 12:14 PM

---

## CRITICAL: Read Discovery Report First

**Before starting ANY implementation**:
1. Read: `dev/2025/10/21/core-llm-support-discovery-report.md`
2. Understand what EXISTS (90% infrastructure)
3. Understand what's MISSING (adapter layer only)
4. Review Pattern-012 documentation

**Do NOT skip this step!** The discovery report shows most infrastructure exists.

---

## Mission

Implement Pattern-012 (LLM Adapter Pattern) to provide a vendor-agnostic interface for 4 LLM providers (Anthropic, OpenAI, Gemini, Perplexity) while leveraging extensive existing infrastructure.

**Key Principle**: We're building an ADAPTER LAYER on top of existing services, not rebuilding the LLM system!

---

## What Already Exists (DO NOT REBUILD)

**Existing Infrastructure** (985+ lines - discovered by Cursor):
- ✅ `services/llm/clients.py` (185 lines) - LLMClient with dual provider
- ✅ `services/config/llm_config_service.py` (640 lines) - 4-provider config
- ✅ `services/llm/provider_selector.py` (99 lines) - selection logic
- ✅ `services/llm/config.py` (51 lines) - enums and types
- ✅ `services/domain/llm_domain_service.py` - DDD mediator
- ✅ 20+ integration points throughout codebase
- ✅ Secure API key management
- ✅ Fallback mechanisms

**DO NOT modify these files unless absolutely necessary for adapter integration!**

---

## Implementation Plan

### Phase 1: LLMAdapter Interface (30 minutes)

**File**: `services/llm/adapters/base.py` (NEW)

**Create the abstract base class**:

```python
"""
LLM Adapter Pattern - Base Interface
Implements Pattern-012 for vendor-agnostic LLM access
"""
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Dict, Any, AsyncIterator
from dataclasses import dataclass


@dataclass
class LLMResponse:
    """Standardized LLM response"""
    content: str
    model: str
    provider: str
    usage: Dict[str, int]
    metadata: Dict[str, Any]


class LLMAdapter(ABC):
    """
    Abstract base class for LLM provider adapters.

    Implements Pattern-012 to provide vendor-agnostic interface
    for multiple LLM providers while maintaining provider-specific
    capabilities through optional methods.

    See: docs/internal/architecture/current/patterns/pattern-012-llm-adapter.md
    """

    def __init__(self, api_key: str, model: str, **kwargs):
        """Initialize adapter with provider credentials"""
        self.api_key = api_key
        self.model = model
        self.config = kwargs

    @abstractmethod
    async def complete(self, prompt: str, **kwargs) -> LLMResponse:
        """
        Generate text completion.

        Args:
            prompt: Input prompt
            **kwargs: Provider-specific options (max_tokens, temperature, etc)

        Returns:
            LLMResponse with standardized format
        """
        pass

    @abstractmethod
    async def classify(self, text: str, categories: List[str]) -> Tuple[str, float]:
        """
        Classify text into categories with confidence.

        Args:
            text: Text to classify
            categories: List of possible categories

        Returns:
            Tuple of (category_name, confidence_score)
        """
        pass

    @abstractmethod
    async def stream_complete(self, prompt: str, **kwargs) -> AsyncIterator[str]:
        """
        Stream completion responses.

        Args:
            prompt: Input prompt
            **kwargs: Provider-specific options

        Yields:
            Text chunks as they arrive
        """
        pass

    @abstractmethod
    def supports_streaming(self) -> bool:
        """Check if provider supports streaming responses"""
        pass

    @abstractmethod
    async def get_model_info(self) -> Dict[str, Any]:
        """
        Get model capabilities and limits.

        Returns:
            Dict with provider, model, max_tokens, capabilities
        """
        pass

    def get_provider_name(self) -> str:
        """Get provider name (override if needed)"""
        return self.__class__.__name__.replace("Adapter", "").lower()
```

**Success Criteria**:
- [ ] File created: `services/llm/adapters/base.py`
- [ ] LLMAdapter ABC defined with all required methods
- [ ] LLMResponse dataclass defined
- [ ] Type hints complete
- [ ] Docstrings follow project style
- [ ] Imports work correctly

---

### Phase 2: ClaudeAdapter (30 minutes)

**File**: `services/llm/adapters/claude_adapter.py` (NEW)

**Wrap existing Anthropic client**:

```python
"""
Claude/Anthropic LLM Adapter
Wraps existing Anthropic client in Pattern-012 interface
"""
from typing import List, Tuple, AsyncIterator, Dict, Any
from .base import LLMAdapter, LLMResponse

# Import existing LLM client
from services.llm.clients import LLMClient
from services.llm.config import LLMProvider


class ClaudeAdapter(LLMAdapter):
    """
    Adapter for Anthropic's Claude models.

    Wraps the existing LLMClient Anthropic implementation
    to provide Pattern-012 compliant interface.
    """

    def __init__(self, api_key: str, model: str = "claude-sonnet-3-5-20240620", **kwargs):
        super().__init__(api_key, model, **kwargs)

        # Use existing LLMClient infrastructure
        self._client = LLMClient(
            provider=LLMProvider.ANTHROPIC,
            model=model,
            api_key=api_key
        )

    async def complete(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate completion using Anthropic API"""
        # Delegate to existing client
        response = await self._client.complete(prompt, **kwargs)

        # Convert to standardized format
        return LLMResponse(
            content=response.get("content", ""),
            model=self.model,
            provider="anthropic",
            usage=response.get("usage", {}),
            metadata=response.get("metadata", {})
        )

    async def classify(self, text: str, categories: List[str]) -> Tuple[str, float]:
        """Classify text using Claude"""
        prompt = f"""
        Classify this text into one of these categories: {', '.join(categories)}

        Text: {text}

        Respond with ONLY: category_name:confidence_score
        Example: feature_request:0.95
        """

        response = await self.complete(prompt, max_tokens=50)
        parts = response.content.strip().split(':')

        if len(parts) != 2:
            return categories[0], 0.0

        return parts[0].strip(), float(parts[1].strip())

    async def stream_complete(self, prompt: str, **kwargs) -> AsyncIterator[str]:
        """Stream completion from Claude"""
        # Use existing client's streaming if available
        async for chunk in self._client.stream_complete(prompt, **kwargs):
            yield chunk

    def supports_streaming(self) -> bool:
        """Claude supports streaming"""
        return True

    async def get_model_info(self) -> Dict[str, Any]:
        """Get Claude model information"""
        return {
            "provider": "anthropic",
            "model": self.model,
            "max_tokens": 200000,  # Claude 3.5 Sonnet context
            "supports_streaming": True,
            "supports_vision": True,
            "supports_function_calling": True
        }
```

**Success Criteria**:
- [ ] File created: `services/llm/adapters/claude_adapter.py`
- [ ] ClaudeAdapter wraps existing LLMClient
- [ ] All abstract methods implemented
- [ ] Uses existing Anthropic infrastructure
- [ ] Response format standardized
- [ ] No breaking changes to existing code

---

### Phase 3: OpenAIAdapter (30 minutes)

**File**: `services/llm/adapters/openai_adapter.py` (NEW)

**Similar structure to ClaudeAdapter** but for OpenAI:

```python
"""
OpenAI LLM Adapter
Wraps existing OpenAI client in Pattern-012 interface
"""
from typing import List, Tuple, AsyncIterator, Dict, Any
from .base import LLMAdapter, LLMResponse
from services.llm.clients import LLMClient
from services.llm.config import LLMProvider


class OpenAIAdapter(LLMAdapter):
    """
    Adapter for OpenAI models (GPT-4, etc).

    Wraps the existing LLMClient OpenAI implementation
    to provide Pattern-012 compliant interface.
    """

    def __init__(self, api_key: str, model: str = "gpt-4-turbo-preview", **kwargs):
        super().__init__(api_key, model, **kwargs)

        self._client = LLMClient(
            provider=LLMProvider.OPENAI,
            model=model,
            api_key=api_key
        )

    async def complete(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate completion using OpenAI API"""
        response = await self._client.complete(prompt, **kwargs)

        return LLMResponse(
            content=response.get("content", ""),
            model=self.model,
            provider="openai",
            usage=response.get("usage", {}),
            metadata=response.get("metadata", {})
        )

    async def classify(self, text: str, categories: List[str]) -> Tuple[str, float]:
        """Classify text using GPT-4"""
        # Similar to Claude implementation
        prompt = f"""
        Classify this text into one of these categories: {', '.join(categories)}

        Text: {text}

        Respond with ONLY: category_name:confidence_score
        """

        response = await self.complete(prompt, max_tokens=50)
        parts = response.content.strip().split(':')

        if len(parts) != 2:
            return categories[0], 0.0

        return parts[0].strip(), float(parts[1].strip())

    async def stream_complete(self, prompt: str, **kwargs) -> AsyncIterator[str]:
        """Stream completion from OpenAI"""
        async for chunk in self._client.stream_complete(prompt, **kwargs):
            yield chunk

    def supports_streaming(self) -> bool:
        """OpenAI supports streaming"""
        return True

    async def get_model_info(self) -> Dict[str, Any]:
        """Get OpenAI model information"""
        return {
            "provider": "openai",
            "model": self.model,
            "max_tokens": 128000,  # GPT-4 Turbo context
            "supports_streaming": True,
            "supports_vision": True,
            "supports_function_calling": True
        }
```

**Success Criteria**:
- [ ] File created: `services/llm/adapters/openai_adapter.py`
- [ ] OpenAIAdapter wraps existing LLMClient
- [ ] All abstract methods implemented
- [ ] Consistent with ClaudeAdapter pattern

---

### Phase 4: GeminiAdapter (30 minutes)

**File**: `services/llm/adapters/gemini_adapter.py` (NEW)

**Note**: Config exists in LLMConfigService, need to add client implementation

```python
"""
Google Gemini LLM Adapter
Implements Pattern-012 interface for Gemini models
"""
from typing import List, Tuple, AsyncIterator, Dict, Any
import google.generativeai as genai
from .base import LLMAdapter, LLMResponse


class GeminiAdapter(LLMAdapter):
    """
    Adapter for Google's Gemini models.

    Implements Pattern-012 interface for Gemini Pro and Ultra.
    Configuration already exists in LLMConfigService.
    """

    def __init__(self, api_key: str, model: str = "gemini-pro", **kwargs):
        super().__init__(api_key, model, **kwargs)

        # Configure Gemini SDK
        genai.configure(api_key=api_key)
        self._model = genai.GenerativeModel(model)

    async def complete(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate completion using Gemini API"""
        response = await self._model.generate_content_async(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=kwargs.get("max_tokens", 1000),
                temperature=kwargs.get("temperature", 0.7)
            )
        )

        return LLMResponse(
            content=response.text,
            model=self.model,
            provider="gemini",
            usage={
                "prompt_tokens": response.usage_metadata.prompt_token_count,
                "completion_tokens": response.usage_metadata.candidates_token_count,
                "total_tokens": response.usage_metadata.total_token_count
            },
            metadata={"finish_reason": str(response.candidates[0].finish_reason)}
        )

    async def classify(self, text: str, categories: List[str]) -> Tuple[str, float]:
        """Classify text using Gemini"""
        prompt = f"""
        Classify this text into one of these categories: {', '.join(categories)}

        Text: {text}

        Respond with ONLY: category_name:confidence_score
        """

        response = await self.complete(prompt, max_tokens=50)
        parts = response.content.strip().split(':')

        if len(parts) != 2:
            return categories[0], 0.0

        return parts[0].strip(), float(parts[1].strip())

    async def stream_complete(self, prompt: str, **kwargs) -> AsyncIterator[str]:
        """Stream completion from Gemini"""
        response = await self._model.generate_content_async(
            prompt,
            stream=True,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=kwargs.get("max_tokens", 1000),
                temperature=kwargs.get("temperature", 0.7)
            )
        )

        async for chunk in response:
            if chunk.text:
                yield chunk.text

    def supports_streaming(self) -> bool:
        """Gemini supports streaming"""
        return True

    async def get_model_info(self) -> Dict[str, Any]:
        """Get Gemini model information"""
        return {
            "provider": "gemini",
            "model": self.model,
            "max_tokens": 32000,  # Gemini Pro context
            "supports_streaming": True,
            "supports_vision": "pro-vision" in self.model,
            "supports_function_calling": True
        }
```

**Dependencies**:
- Add to requirements.txt: `google-generativeai>=0.3.0`

**Success Criteria**:
- [ ] File created: `services/llm/adapters/gemini_adapter.py`
- [ ] Gemini SDK integrated
- [ ] All abstract methods implemented
- [ ] Dependency added to requirements.txt

---

### Phase 5: PerplexityAdapter (30 minutes)

**File**: `services/llm/adapters/perplexity_adapter.py` (NEW)

**Note**: Perplexity uses OpenAI-compatible API

```python
"""
Perplexity LLM Adapter
Implements Pattern-012 interface for Perplexity models
"""
from typing import List, Tuple, AsyncIterator, Dict, Any
import openai
from .base import LLMAdapter, LLMResponse


class PerplexityAdapter(LLMAdapter):
    """
    Adapter for Perplexity AI models.

    Uses OpenAI-compatible API with Perplexity endpoint.
    Configuration already exists in LLMConfigService.
    """

    def __init__(self, api_key: str, model: str = "pplx-70b-online", **kwargs):
        super().__init__(api_key, model, **kwargs)

        # Configure client for Perplexity endpoint
        self._client = openai.AsyncOpenAI(
            api_key=api_key,
            base_url="https://api.perplexity.ai"
        )

    async def complete(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate completion using Perplexity API"""
        response = await self._client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=kwargs.get("max_tokens", 1000),
            temperature=kwargs.get("temperature", 0.7)
        )

        return LLMResponse(
            content=response.choices[0].message.content,
            model=self.model,
            provider="perplexity",
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            },
            metadata={"finish_reason": response.choices[0].finish_reason}
        )

    async def classify(self, text: str, categories: List[str]) -> Tuple[str, float]:
        """Classify text using Perplexity"""
        prompt = f"""
        Classify this text into one of these categories: {', '.join(categories)}

        Text: {text}

        Respond with ONLY: category_name:confidence_score
        """

        response = await self.complete(prompt, max_tokens=50)
        parts = response.content.strip().split(':')

        if len(parts) != 2:
            return categories[0], 0.0

        return parts[0].strip(), float(parts[1].strip())

    async def stream_complete(self, prompt: str, **kwargs) -> AsyncIterator[str]:
        """Stream completion from Perplexity"""
        stream = await self._client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=kwargs.get("max_tokens", 1000),
            temperature=kwargs.get("temperature", 0.7),
            stream=True
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    def supports_streaming(self) -> bool:
        """Perplexity supports streaming"""
        return True

    async def get_model_info(self) -> Dict[str, Any]:
        """Get Perplexity model information"""
        return {
            "provider": "perplexity",
            "model": self.model,
            "max_tokens": 4096,  # Perplexity context
            "supports_streaming": True,
            "supports_vision": False,
            "supports_function_calling": False,
            "supports_online": "online" in self.model  # Online models search web
        }
```

**Success Criteria**:
- [ ] File created: `services/llm/adapters/perplexity_adapter.py`
- [ ] Perplexity API integrated
- [ ] OpenAI-compatible client used
- [ ] All abstract methods implemented

---

### Phase 6: LLMFactory (30 minutes)

**File**: `services/llm/adapters/factory.py` (NEW)

**Create adapter factory**:

```python
"""
LLM Adapter Factory
Creates appropriate adapter based on provider configuration
"""
from typing import Dict, Type
from .base import LLMAdapter
from .claude_adapter import ClaudeAdapter
from .openai_adapter import OpenAIAdapter
from .gemini_adapter import GeminiAdapter
from .perplexity_adapter import PerplexityAdapter
from services.llm.config import LLMProvider


class LLMFactory:
    """
    Factory for creating LLM adapters.

    Implements factory pattern from Pattern-012 to create
    appropriate adapter based on provider configuration.
    """

    _adapters: Dict[LLMProvider, Type[LLMAdapter]] = {
        LLMProvider.ANTHROPIC: ClaudeAdapter,
        LLMProvider.OPENAI: OpenAIAdapter,
        LLMProvider.GEMINI: GeminiAdapter,
        LLMProvider.PERPLEXITY: PerplexityAdapter
    }

    @classmethod
    def create(cls, provider: LLMProvider, api_key: str, model: str, **kwargs) -> LLMAdapter:
        """
        Create adapter for specified provider.

        Args:
            provider: LLM provider enum
            api_key: API key for provider
            model: Model name
            **kwargs: Additional provider-specific config

        Returns:
            Configured LLMAdapter instance

        Raises:
            ValueError: If provider not supported
        """
        if provider not in cls._adapters:
            available = ", ".join(p.value for p in cls._adapters.keys())
            raise ValueError(
                f"Unknown provider: {provider}. Available: {available}"
            )

        adapter_class = cls._adapters[provider]
        return adapter_class(api_key=api_key, model=model, **kwargs)

    @classmethod
    def register_adapter(cls, provider: LLMProvider, adapter_class: Type[LLMAdapter]):
        """
        Register custom adapter.

        Allows extending factory with new providers at runtime.
        """
        cls._adapters[provider] = adapter_class

    @classmethod
    def list_providers(cls) -> list[LLMProvider]:
        """List available providers"""
        return list(cls._adapters.keys())

    @classmethod
    def supports_provider(cls, provider: LLMProvider) -> bool:
        """Check if provider is supported"""
        return provider in cls._adapters
```

**Success Criteria**:
- [ ] File created: `services/llm/adapters/factory.py`
- [ ] LLMFactory implemented
- [ ] All 4 providers registered
- [ ] create() method works
- [ ] Error handling for unknown providers

---

### Phase 7: Update Module Exports (5 minutes)

**File**: `services/llm/adapters/__init__.py` (NEW)

```python
"""
LLM Adapters - Pattern-012 Implementation
Vendor-agnostic interface for multiple LLM providers
"""
from .base import LLMAdapter, LLMResponse
from .claude_adapter import ClaudeAdapter
from .openai_adapter import OpenAIAdapter
from .gemini_adapter import GeminiAdapter
from .perplexity_adapter import PerplexityAdapter
from .factory import LLMFactory

__all__ = [
    "LLMAdapter",
    "LLMResponse",
    "ClaudeAdapter",
    "OpenAIAdapter",
    "GeminiAdapter",
    "PerplexityAdapter",
    "LLMFactory"
]
```

---

### Phase 8: Integration with LLMDomainService (15 minutes)

**File**: `services/domain/llm_domain_service.py` (MODIFY)

**Add adapter support to existing domain service**:

```python
# Add to imports
from services.llm.adapters import LLMFactory, LLMAdapter
from services.llm.config import LLMProvider

class LLMDomainService:
    """Existing domain service - ADD adapter support"""

    def __init__(self, config_service: LLMConfigService):
        self.config_service = config_service
        # Existing client
        self._client = LLMClient(...)

        # NEW: Add adapter support
        self._adapters: Dict[LLMProvider, LLMAdapter] = {}
        self._initialize_adapters()

    def _initialize_adapters(self):
        """Initialize adapters for configured providers"""
        for provider in [LLMProvider.ANTHROPIC, LLMProvider.OPENAI,
                        LLMProvider.GEMINI, LLMProvider.PERPLEXITY]:
            try:
                config = self.config_service.get_provider_config(provider)
                if config and config.get("api_key"):
                    adapter = LLMFactory.create(
                        provider=provider,
                        api_key=config["api_key"],
                        model=config["model"]
                    )
                    self._adapters[provider] = adapter
            except Exception as e:
                logger.warning(f"Failed to initialize {provider} adapter: {e}")

    async def complete_with_adapter(self, prompt: str, provider: LLMProvider, **kwargs):
        """NEW: Complete using specific adapter"""
        if provider not in self._adapters:
            raise ValueError(f"Provider {provider} not configured")

        adapter = self._adapters[provider]
        return await adapter.complete(prompt, **kwargs)
```

**Success Criteria**:
- [ ] LLMDomainService updated with adapter support
- [ ] Adapters initialized on service creation
- [ ] New method: complete_with_adapter()
- [ ] Backward compatibility maintained
- [ ] Existing code still works

---

### Phase 9: Testing (45 minutes)

**File**: `tests/services/llm/test_adapters.py` (NEW)

**Create comprehensive tests**:

```python
"""
Tests for LLM Adapters (Pattern-012)
"""
import pytest
from services.llm.adapters import (
    LLMFactory, ClaudeAdapter, OpenAIAdapter,
    GeminiAdapter, PerplexityAdapter, LLMResponse
)
from services.llm.config import LLMProvider


class TestLLMFactory:
    """Test adapter factory"""

    def test_factory_lists_providers(self):
        """Factory should list all 4 providers"""
        providers = LLMFactory.list_providers()
        assert len(providers) == 4
        assert LLMProvider.ANTHROPIC in providers
        assert LLMProvider.OPENAI in providers
        assert LLMProvider.GEMINI in providers
        assert LLMProvider.PERPLEXITY in providers

    def test_factory_creates_claude_adapter(self):
        """Factory should create ClaudeAdapter"""
        adapter = LLMFactory.create(
            provider=LLMProvider.ANTHROPIC,
            api_key="test-key",
            model="claude-3-sonnet"
        )
        assert isinstance(adapter, ClaudeAdapter)

    def test_factory_creates_openai_adapter(self):
        """Factory should create OpenAIAdapter"""
        adapter = LLMFactory.create(
            provider=LLMProvider.OPENAI,
            api_key="test-key",
            model="gpt-4"
        )
        assert isinstance(adapter, OpenAIAdapter)

    def test_factory_rejects_unknown_provider(self):
        """Factory should raise error for unknown provider"""
        with pytest.raises(ValueError, match="Unknown provider"):
            LLMFactory.create(
                provider="unknown",
                api_key="test-key",
                model="test-model"
            )


@pytest.mark.asyncio
class TestClaudeAdapter:
    """Test Claude adapter"""

    async def test_adapter_initialization(self):
        """Adapter should initialize with config"""
        adapter = ClaudeAdapter(
            api_key="test-key",
            model="claude-3-sonnet"
        )
        assert adapter.model == "claude-3-sonnet"
        assert adapter.supports_streaming()

    async def test_get_model_info(self):
        """Adapter should return model info"""
        adapter = ClaudeAdapter(api_key="test-key", model="claude-3-sonnet")
        info = await adapter.get_model_info()

        assert info["provider"] == "anthropic"
        assert info["model"] == "claude-3-sonnet"
        assert info["supports_streaming"] is True
        assert info["max_tokens"] > 0


# Similar tests for OpenAI, Gemini, Perplexity adapters...
```

**Success Criteria**:
- [ ] Test file created
- [ ] Factory tests passing
- [ ] Adapter initialization tests passing
- [ ] All 4 adapters have basic tests
- [ ] Integration tests with domain service

---

## Evidence Requirements

**Create**: `dev/2025/10/21/core-llm-support-implementation-evidence.md`

**Include**:
1. **Files Created**: List with line counts
2. **Test Results**: pytest output showing all passing
3. **Import Verification**: Python can import all adapters
4. **Integration Check**: LLMDomainService loads adapters
5. **Pattern Compliance**: Checklist from Pattern-012

**Example**:
```markdown
## Implementation Evidence

### Files Created
- services/llm/adapters/base.py (120 lines)
- services/llm/adapters/claude_adapter.py (95 lines)
- services/llm/adapters/openai_adapter.py (92 lines)
- services/llm/adapters/gemini_adapter.py (105 lines)
- services/llm/adapters/perplexity_adapter.py (98 lines)
- services/llm/adapters/factory.py (75 lines)
- services/llm/adapters/__init__.py (15 lines)
- tests/services/llm/test_adapters.py (180 lines)

Total: ~780 new lines

### Test Results
```
pytest tests/services/llm/test_adapters.py -v
================================ test session starts =================================
collected 12 items

tests/services/llm/test_adapters.py::TestLLMFactory::test_factory_lists_providers PASSED
tests/services/llm/test_adapters.py::TestLLMFactory::test_factory_creates_claude_adapter PASSED
...
================================ 12 passed in 2.45s ==================================
```

### Integration Verification
```
python -c "
from services.llm.adapters import LLMFactory
from services.llm.config import LLMProvider
print('Factory providers:', LLMFactory.list_providers())
print('✅ All adapters importable')
"
```
```

---

## STOP Conditions

**STOP and ask PM if**:

1. **Existing infrastructure doesn't match discovery report**
   - Expected: LLMClient, LLMConfigService exist
   - If missing: Ask PM before rebuilding

2. **API incompatibilities found**
   - Provider SDK doesn't work as expected
   - Breaking changes in existing code needed

3. **Tests fail in unexpected ways**
   - Existing tests break
   - Integration issues

4. **Dependencies missing**
   - Can't install google-generativeai
   - SDK versions incompatible

5. **Time estimate significantly exceeded**
   - Phase takes 2x longer than estimated
   - Unexpected complexity discovered

**DO NOT proceed past 4 hours** without PM check-in!

---

## Success Criteria

Implementation is complete when:

- [x] All 6 adapter files created (base + 4 providers + factory)
- [x] All adapters implement LLMAdapter interface
- [x] LLMFactory creates all 4 providers
- [x] Tests pass for all adapters
- [x] Integration with LLMDomainService works
- [x] Existing code continues to function
- [x] Evidence document created
- [x] No breaking changes
- [x] Pattern-012 compliance verified

---

## Post-Implementation Tasks

After Code completes:

1. **Verify with PM** - Show evidence document
2. **Manual testing** - Try each adapter
3. **Update documentation** - Pattern-012 marked implemented
4. **Close issue** - Mark #237 complete
5. **Commit** - Push to Git with proper message

---

## Notes for Code Agent

- **Read discovery report first!** Most infrastructure exists
- **DO NOT rebuild** existing LLMClient or LLMConfigService
- **Wrap, don't replace** - adapters wrap existing clients
- **Test as you go** - verify each adapter works
- **Stop if blocked** - don't guess, ask PM
- **Evidence matters** - document everything

---

**Ready to implement!** Follow phases in order, test thoroughly, stop if uncertain.
