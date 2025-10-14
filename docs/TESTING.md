# Testing Strategy

## Overview

Piper Morgan uses pytest with marker-based test categorization to support flexible testing strategies for different environments.

## Test Categories

- **Unit Tests** (`@pytest.mark.unit`): Fast tests with no external dependencies
- **Integration Tests** (`@pytest.mark.integration`): Tests that may require external services
- **LLM Tests** (`@pytest.mark.llm`): Tests that require LLM API calls (Anthropic/OpenAI)
- **Contract Tests** (`@pytest.mark.contract`): Plugin interface compliance tests
- **Performance Tests** (`@pytest.mark.performance`): Performance benchmark tests

## Running Tests

### Locally (with API keys)

Run all tests including LLM functionality:

```bash
# Ensure API keys are configured (stored in system keychain)
pytest tests/ -v

# Or with specific markers
pytest tests/ -v -m "unit or integration or llm"
```

### Locally (without API keys)

Skip LLM tests to avoid API calls:

```bash
pytest tests/ -v -m "not llm"
```

### CI Environment

CI automatically skips LLM tests (no API keys configured):

```bash
# What CI runs (see .github/workflows/test.yml)
pytest tests/ --tb=short -v -m "not llm"
```

### Run Only LLM Tests

When testing LLM functionality specifically:

```bash
# Requires API keys in keychain
pytest tests/ -v -m llm
```

### Run Specific Categories

```bash
# Unit tests only
pytest tests/ -v -m unit

# Integration tests only
pytest tests/ -v -m integration

# Contract tests only
pytest tests/ -v -m contract
```

## LLM Provider Configuration

### Current Provider Support

- **Implemented**: Anthropic (primary), OpenAI (fallback)
- **Configured**: Gemini, Perplexity (not yet implemented)
- **Fallback**: Anthropic → OpenAI (automatic when primary fails)

---

## LLM Provider Architecture Status

**Implementation Status**: 2 of 4 providers operational

**Fully Implemented**:
- ✅ **Anthropic (Claude)** - Primary provider
  - Models: claude-sonnet-4-20250514, claude-opus-4-20250514
  - Usage: Intent classification, content generation, analysis
  - Status: Fully operational with graceful initialization

- ✅ **OpenAI (GPT)** - Automatic fallback
  - Models: gpt-4, gpt-4-turbo
  - Usage: Fallback when Anthropic unavailable
  - Status: Fully operational

**Configured but Not Implemented**:
- ⏳ **Gemini** - Config exists, adapter pending
  - Intended use: Research, web search integration
  - Status: Environment variables supported, implementation deferred

- ⏳ **Perplexity** - Config exists, adapter pending
  - Intended use: Real-time information, current events
  - Status: Environment variables supported, implementation deferred

**Current Behavior**:
- **Primary**: Anthropic (Claude) for all LLM operations
- **Fallback**: OpenAI (GPT) if Anthropic fails or unavailable
- **Graceful**: System continues without LLM if no keys configured
- **CI**: Tests skip LLM operations automatically (no API keys in CI)

**Future Enhancement**: Complete 4-provider integration tracked as technical debt. See `docs/architecture/llm-provider-status.md` for complete architectural details and implementation roadmap.

---

## Instructions

1. Open `docs/TESTING.md`
2. Locate the section "Current LLM Provider Support"
3. Add the above content immediately after that section
4. Verify formatting and links
5. Commit with message: "docs: Update TESTING.md with provider architecture status"

### API Key Storage

API keys are stored securely in the system keychain (macOS Keyring) via `KeychainService`. Environment variables are supported for migration but not recommended.

### Graceful Degradation

The `LLMClient` supports graceful initialization:
- Can be imported without API keys
- `providers_initialized` property indicates if LLM is available
- Clear error messages when LLM calls attempted without providers
- Tests automatically skip when `providers_initialized` is False

## CI Testing Strategy

### Why LLM Tests are Skipped in CI

1. **No API Keys**: CI environment doesn't have keychain-stored keys
2. **Cost Preservation**: Avoid burning API credits on every commit
3. **Test Reliability**: External API calls can be slow/flaky
4. **Coverage**: Most functionality testable without real LLM calls

### Local Testing Workflow

1. **Before Pushing**: Run full test suite locally with API keys
   ```bash
   pytest tests/ -v  # Includes LLM tests
   ```

2. **Quick Validation**: Run non-LLM tests for faster feedback
   ```bash
   pytest tests/ -v -m "not llm"
   ```

3. **LLM-Specific Changes**: Run only LLM tests
   ```bash
   pytest tests/ -v -m llm
   ```

## Test Fixture Patterns

### LLM Client Fixture

Tests requiring LLM access can use:

```python
import pytest
from services.llm.clients import LLMClient

@pytest.fixture
def llm_client():
    """Fixture that auto-skips if LLM not available"""
    client = LLMClient()
    if not client.providers_initialized:
        pytest.skip("LLM providers not initialized (no API keys)")
    return client

@pytest.mark.llm
async def test_with_llm(llm_client):
    """Test that requires real LLM calls"""
    result = await llm_client.complete("reasoning", "test prompt")
    assert result
```

## Common Patterns

### Marking Tests

```python
import pytest

# Single test
@pytest.mark.llm
async def test_llm_classification():
    pass

# Entire test class
@pytest.mark.llm
class TestLLMFeatures:
    async def test_feature_1(self):
        pass

    async def test_feature_2(self):
        pass
```

### Conditional Skipping

```python
from services.llm.clients import LLMClient

client = LLMClient()

@pytest.mark.skipif(
    not client.providers_initialized,
    reason="LLM providers not available"
)
async def test_llm_feature():
    pass
```

## Performance Considerations

- **Unit tests**: Target <30 seconds total
- **Integration tests**: Allow up to 2 minutes
- **LLM tests**: May take several minutes (external API latency)
- **Performance tests**: Benchmark-specific timeout thresholds

## Troubleshooting

### "LLM providers not initialized"

**Cause**: No API keys configured
**Solution**: Configure keys in system keychain or export environment variables:
```bash
export ANTHROPIC_API_KEY="your-key-here"
export OPENAI_API_KEY="your-key-here"
```

### Tests Pass Locally but Fail in CI

**Possible Causes**:
1. Test depends on LLM but not marked with `@pytest.mark.llm`
2. Test depends on local files not committed to repo
3. Test depends on specific Python version (local vs CI)

**Solution**: Run local test with `-m "not llm"` to simulate CI

### Import Errors in CI

**Cause**: LLMClient import fails when no providers initialized
**Status**: **FIXED** (Oct 13, 2025) - LLMClient now initializes gracefully

## References

- Configuration: `pytest.ini`
- LLM Client: `services/llm/clients.py`
- CI Workflow: `.github/workflows/test.yml`
- Test Constants: `tests/intent/test_constants.py`

## Future Enhancements

- [ ] Add LLM test job in CI with secrets (for main branch only)
- [ ] Implement Gemini and Perplexity adapters
- [ ] Add performance baseline tracking for LLM tests
- [ ] Create mock LLM responses for unit testing

---

**Last Updated**: October 13, 2025
**Issue**: CORE-CRAFT-GAP Phase 0, Issue 2
