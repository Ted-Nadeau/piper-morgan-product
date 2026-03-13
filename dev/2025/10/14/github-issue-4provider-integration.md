# GitHub Issue: Complete LLM Provider Integration (4-Provider Support)

**Labels**: `technical-debt`, `enhancement`, `llm`

---

## Overview

Complete the LLM provider integration by connecting existing infrastructure components and implementing missing adapters.

**Current State**: 2-provider fallback operational (Anthropic ↔ OpenAI)
**Goal**: Full 4-provider support with intelligent routing

---

## Background

- **Pattern**: Pattern-012 (LLM Adapter Pattern)
- **Implemented**: Oct 9, 2025 (commits d6b8aa09, 0fa00a29)
- **Status**: Architecture exists, partially implemented
- **Documentation**: `docs/architecture/llm-provider-status.md`

---

## What Exists (Already Built)

✅ **LLMConfigService** - 641 lines, comprehensive configuration
✅ **ProviderSelector** - Intelligent task-based provider selection
✅ **Anthropic Adapter** - Fully implemented
✅ **OpenAI Adapter** - Fully implemented
✅ **Graceful Fallback** - Anthropic → OpenAI working
✅ **Pattern Documentation** - Complete implementation guide

---

## What's Missing

### 1. Integrate ProviderSelector into LLMClient

**File**: `services/llm/clients.py`
**Current**: Hardcoded `Anthropic → OpenAI` fallback
**Goal**: Use `ProviderSelector.select_provider(task_type)` for intelligent routing

**Code Location**: Lines 79-117 in `clients.py`

**Change Needed**:
```python
# Current (hardcoded)
async def complete(self, prompt: str, **kwargs):
    try:
        return await self.anthropic_client.complete(prompt)
    except:
        return await self.openai_client.complete(prompt)

# Goal (intelligent selection)
async def complete(self, prompt: str, task_type: str = None, **kwargs):
    provider = self.selector.select_provider(task_type)
    try:
        return await self.get_provider(provider).complete(prompt)
    except:
        return await self.fallback_complete(prompt, exclude=[provider])
```

**Estimated Effort**: 1 hour

### 2. Implement Gemini Adapter Methods

**File**: `services/llm/clients.py`
**Current**: Config exists, no adapter
**Goal**: Add Gemini API integration

**Methods Needed**:
- `_init_gemini_client()`
- `_complete_gemini(prompt, **kwargs)`
- Error handling and logging

**API**: Google Gemini API (similar to other providers)

**Estimated Effort**: 30-45 minutes

### 3. Implement Perplexity Adapter Methods

**File**: `services/llm/clients.py`
**Current**: Config exists, no adapter
**Goal**: Add Perplexity API integration

**Methods Needed**:
- `_init_perplexity_client()`
- `_complete_perplexity(prompt, **kwargs)`
- Error handling and logging

**API**: Perplexity API (similar to other providers)

**Estimated Effort**: 30-45 minutes

### 4. Testing and Validation

**Test Files**: Create/update tests for:
- ProviderSelector integration
- Gemini adapter (with mocks for CI)
- Perplexity adapter (with mocks for CI)
- Full 4-provider fallback chain

**Estimated Effort**: 30 minutes

### 5. Documentation Updates

**Files to Update**:
- `docs/architecture/llm-provider-status.md`
- `docs/TESTING.md`
- `README.md` (if applicable)

**Estimated Effort**: 15 minutes

---

## Total Effort Estimation

**Engineering Time**: 2.5-3 hours
**Complexity**: Low-Medium (infrastructure exists, just integration)
**Priority**: Low (current 2-provider sufficient for production)

---

## Acceptance Criteria

- [ ] ProviderSelector integrated into LLMClient.complete()
- [ ] Gemini adapter implemented and tested
- [ ] Perplexity adapter implemented and tested
- [ ] Full 4-provider fallback chain working
- [ ] All tests passing (with LLM mocks for CI)
- [ ] Documentation updated
- [ ] `docs/architecture/llm-provider-status.md` reflects "4-provider operational"

---

## Benefits When Complete

✅ Task-optimized provider selection (coding→OpenAI, research→Gemini, etc.)
✅ Cost-aware provider routing
✅ More fallback options (4 providers instead of 2)
✅ Future-proof architecture (easy to add providers)

---

## References

- **Architecture Doc**: `docs/architecture/llm-provider-status.md`
- **Pattern**: `docs/patterns/pattern-012-llm-adapter.md`
- **Config Service**: `services/config/llm_config_service.py`
- **Provider Selector**: `services/llm/provider_selector.py`
- **LLM Client**: `services/llm/clients.py`

---

## Related Work

- CORE-CRAFT-GAP-2: CI testing infrastructure (completed Oct 13, 2025)
- Pattern-012 investigation (completed Oct 13, 2025)

---

**Created**: October 13, 2025
**Epic**: CORE (Post-GAP-3)
**Milestone**: Post-MVP (nice-to-have enhancement)
