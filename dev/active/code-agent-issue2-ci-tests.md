# Code Agent Prompt: Fix CI Tests Workflow (Issue 2)

**Date**: October 13, 2025, 8:10 AM
**Issue**: CI Tests Workflow Failure (LLM Client Initialization)
**Duration**: 1 hour (estimated)
**Priority**: CRITICAL (enables regression detection)
**Agent**: Code Agent

---

## Mission

Fix Tests workflow to run successfully in CI environment by:
1. Making LLMClient initialization graceful (warn instead of fail)
2. Adding pytest markers for LLM-dependent tests
3. Updating CI workflow to skip LLM tests
4. Documenting testing strategy

**Result**: CI can run tests, detect regressions, maintain quality

---

## Context

**Current Problem**:
- Tests workflow fails in CI environment
- Root cause: `LLMClient.__init__` fails when no API keys configured
- Cannot import LLMClient → Cannot run ANY tests
- Blocks: Regression detection, CI validation

**From Pattern-012 Investigation** (Code's findings):
- ✅ Graceful fallback EXISTS: Anthropic ↔ OpenAI (working)
- ✅ 4-provider config EXISTS: Anthropic, OpenAI, Gemini, Perplexity
- ⚠️ Only 2 providers IMPLEMENTED: Anthropic, OpenAI
- ⚠️ LLMClient.__init__ not graceful when keys missing

**Current LLM Architecture** (from investigation):
- Location: `services/llm/clients.py` (lines 79-117 have fallback logic)
- Config: `services/config/llm_config_service.py` (641 lines)
- Providers: Anthropic + OpenAI functional, Gemini + Perplexity configured

**Why This Matters**:
- Need to test without burning production API credits
- CI environment won't have API keys configured
- Tests should gracefully skip LLM calls when no keys available
- Real LLM tests run locally when keys are available

---

## Task 1: Make LLMClient Initialization Graceful (30 minutes)

### File to Modify
`services/llm/clients.py`

### Investigation Phase (10 min)

**Step 1: Locate Initialization Code**
```bash
# Find LLMClient class and __init__ method
grep -n "class LLMClient" services/llm/clients.py
grep -A 30 "def __init__" services/llm/clients.py | head -40

# Check what happens when no keys configured
grep -A 10 "_init_providers\|_validate_keys" services/llm/clients.py
```

**Step 2: Understand Current Failure**
- Where does initialization fail without keys?
- Is it in provider setup, key validation, or API client creation?
- What exception is raised?

**Step 3: Check Dependencies**
```bash
# See what else imports LLMClient
grep -r "from.*clients import LLMClient\|import.*LLMClient" services/ tests/
```

### Implementation Phase (20 min)

**Current Pattern** (expected):
```python
class LLMClient:
    def __init__(self):
        """Initialize LLM client with providers"""
        self._init_providers()  # Fails if no keys
        # Other initialization
```

**New Pattern** (graceful):
```python
class LLMClient:
    def __init__(self):
        """Initialize LLM client with providers"""
        self.providers_initialized = False
        try:
            self._init_providers()
            self.providers_initialized = True
            logger.info("LLM providers initialized successfully")
        except Exception as e:
            logger.warning(f"LLM providers not fully initialized: {e}")
            logger.warning("Some LLM functionality may be unavailable")
            logger.warning("Tests requiring LLM will be skipped")
            # Continue - allow import to succeed
            # Methods will fail gracefully when called
```

**Method Call Protection**:
```python
async def complete(self, prompt: str, **kwargs) -> str:
    """Generate completion from LLM"""
    if not self.providers_initialized:
        raise RuntimeError(
            "LLM providers not initialized. "
            "Ensure API keys are configured: ANTHROPIC_API_KEY or OPENAI_API_KEY"
        )
    # ... rest of implementation
```

**Key Principles**:
1. **Fail Late, Not Early**: Allow import/initialization to succeed
2. **Clear Error Messages**: Tell user what's needed (API keys)
3. **Graceful Degradation**: System works without LLM (reduced functionality)
4. **Test-Friendly**: Tests can check `providers_initialized` flag

### Testing Requirements

**Test 1: With API Keys** (normal operation)
```bash
# Should work normally
export ANTHROPIC_API_KEY="test-key"
python -c "from services.llm.clients import LLMClient; client = LLMClient(); print('✅ Init with keys works')"
```

**Test 2: Without API Keys** (graceful degradation)
```bash
# Should succeed with warnings
unset ANTHROPIC_API_KEY
unset OPENAI_API_KEY
python -c "from services.llm.clients import LLMClient; client = LLMClient(); print('✅ Init without keys works')"
```

**Test 3: Method Call Without Keys** (clear error)
```python
# Should fail gracefully with clear message
client = LLMClient()  # No keys
try:
    await client.complete("test")
except RuntimeError as e:
    assert "not initialized" in str(e)
    print("✅ Clear error message")
```

### Acceptance Criteria: Task 1
- [ ] LLMClient can be imported without API keys
- [ ] Initialization logs warning (not error) when keys missing
- [ ] `providers_initialized` flag tracks state
- [ ] Methods check flag before using providers
- [ ] Clear error messages when methods called without providers
- [ ] Existing functionality unchanged when keys present

---

## Task 2: Add Pytest Markers for LLM Tests (15 minutes)

### File to Modify
`pytest.ini` (or create if doesn't exist)

### Add Marker Configuration

**Create/Update pytest.ini**:
```ini
[pytest]
markers =
    llm: marks tests that require LLM API calls (deselect with '-m "not llm"')
    integration: marks integration tests (slow, may require external services)
    unit: marks unit tests (fast, no external dependencies)

# Optional: Add other pytest config
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

### Identify Tests to Mark

**Step 1: Find LLM-Dependent Tests**
```bash
# Search for tests that use LLMClient or make LLM calls
grep -r "LLMClient\|complete\|classify" tests/ --include="test_*.py" | grep -v "# comment"

# Find tests that use anthropic/openai directly
grep -r "anthropic\|openai" tests/ --include="test_*.py"

# Look for intent classification tests (likely use LLM)
find tests/ -name "*intent*.py" -o -name "*classification*.py"
```

**Step 2: Categorize Tests**

**Likely LLM-Dependent**:
- `tests/intent/test_execution_accuracy.py` (mentioned in investigation)
- Any test importing `LLMClient`
- Tests calling `complete()`, `classify()`, etc.
- Integration tests for intent classification

**Likely Safe (No LLM)**:
- Unit tests for data structures
- Config tests
- Router tests (unless testing LLM integration)
- Mock-based tests

### Mark Tests

**Pattern**:
```python
import pytest

@pytest.mark.llm
async def test_intent_classification_accuracy():
    """Test requiring real LLM API calls"""
    client = LLMClient()
    result = await client.complete("classify this")
    assert result
```

**Estimate**: 10-15 tests need marking

### Create Helper Fixture (Optional)

```python
# tests/conftest.py or tests/fixtures/llm_fixtures.py

import pytest
from services.llm.clients import LLMClient

@pytest.fixture
def llm_client():
    """Fixture for LLM client - automatically skips if not initialized"""
    client = LLMClient()
    if not client.providers_initialized:
        pytest.skip("LLM providers not initialized (no API keys)")
    return client

# Usage in tests:
@pytest.mark.llm
async def test_with_llm(llm_client):
    result = await llm_client.complete("test")
    assert result
```

### Acceptance Criteria: Task 2
- [ ] pytest.ini has `llm` marker defined
- [ ] 10-15 tests marked with `@pytest.mark.llm`
- [ ] Optional: llm_client fixture with auto-skip
- [ ] Tests can be selected: `pytest -m llm`
- [ ] Tests can be deselected: `pytest -m "not llm"`

---

## Task 3: Update CI Workflow (10 minutes)

### File to Modify
`.github/workflows/tests.yml`

### Investigation

**Step 1: Locate Current Test Command**
```bash
grep -A 5 "pytest" .github/workflows/tests.yml
```

**Step 2: Understand Current Setup**
- What Python version?
- How are dependencies installed?
- What's the current pytest command?

### Required Changes

**Update Pytest Command**:
```yaml
# OLD
- name: Run tests
  run: pytest tests/ -v

# NEW
- name: Run tests
  run: pytest tests/ -v -m "not llm"

# Optional: Add comment explaining
- name: Run tests (excluding LLM tests)
  run: |
    # Skip LLM tests in CI (no API keys configured)
    # LLM tests run locally when keys available
    pytest tests/ -v -m "not llm"
```

**Optional: Add Separate LLM Test Job** (for future):
```yaml
# Could add job that runs WITH API keys from secrets
# But not required for this issue - defer to future work

# test-llm:
#   runs-on: ubuntu-latest
#   if: github.event_name == 'push' && github.ref == 'refs/heads/main'
#   steps:
#     - name: Run LLM tests
#       env:
#         ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_CI_KEY }}
#       run: pytest tests/ -v -m llm
```

### Acceptance Criteria: Task 3
- [ ] `.github/workflows/tests.yml` updated
- [ ] Pytest command includes `-m "not llm"`
- [ ] Comment explains why LLM tests skipped
- [ ] Workflow would pass in CI (verified locally)

---

## Task 4: Update Documentation (5 minutes)

### Files to Create/Update

**Option 1: Update README.md**
```markdown
## Testing

### Running Tests Locally

```bash
# Run all tests (requires API keys for LLM tests)
export ANTHROPIC_API_KEY="your-key"
pytest tests/ -v

# Run only unit tests (no API keys needed)
pytest tests/ -v -m "not llm"

# Run only LLM tests (requires API keys)
pytest tests/ -v -m llm
```

### CI Testing

CI runs all non-LLM tests automatically. LLM tests are skipped in CI to avoid burning API credits. Run LLM tests locally before pushing changes that affect LLM functionality.
```

**Option 2: Create TESTING.md**
```markdown
# Testing Strategy

## Test Categories

- **Unit Tests**: Fast, no external dependencies, run in CI
- **Integration Tests**: May require external services, run in CI
- **LLM Tests**: Require API keys, run locally only

## Running Tests

### Locally (with API keys)
All tests including LLM functionality:
```bash
export ANTHROPIC_API_KEY="your-key"
pytest tests/ -v
```

### Locally (without API keys)
Skip LLM tests:
```bash
pytest tests/ -v -m "not llm"
```

### CI Environment
CI automatically skips LLM tests (no API keys configured).

## Current LLM Provider Support

- **Implemented**: Anthropic (primary), OpenAI (fallback)
- **Configured**: Gemini, Perplexity (not yet implemented)
- **Fallback**: Anthropic → OpenAI (automatic)

See `services/llm/clients.py` for implementation details.
```

### Acceptance Criteria: Task 4
- [ ] Documentation explains testing strategy
- [ ] Instructions for running with/without LLM tests
- [ ] CI behavior documented
- [ ] Current LLM provider status documented

---

## Overall Acceptance Criteria

### Technical Success
- [ ] LLMClient can be imported without API keys
- [ ] Tests can be imported without API keys
- [ ] CI workflow updated to skip LLM tests
- [ ] 10-15 tests marked with `@pytest.mark.llm`
- [ ] All non-LLM tests pass locally
- [ ] Workflow would pass in CI (verified)

### Functional Success
- [ ] LLM functionality works normally when keys present
- [ ] Graceful degradation when keys absent
- [ ] Clear error messages guide users
- [ ] Testing strategy documented

### Evidence Required
- [ ] Terminal output: Import test without keys
- [ ] Terminal output: pytest -m "not llm" passes
- [ ] Terminal output: pytest -m llm works with keys
- [ ] Git diff showing changes
- [ ] Commit message explaining approach

---

## Testing Checklist

### Local Testing (Before Push)

**Test 1: Import Without Keys**
```bash
unset ANTHROPIC_API_KEY
unset OPENAI_API_KEY
python -c "from services.llm.clients import LLMClient; print('✅ Import succeeds')"
```

**Test 2: Run Non-LLM Tests**
```bash
pytest tests/ -v -m "not llm"
# Should pass
```

**Test 3: Run LLM Tests (with keys)**
```bash
export ANTHROPIC_API_KEY="your-key"
pytest tests/ -v -m llm
# Should pass
```

**Test 4: Run All Tests (with keys)**
```bash
pytest tests/ -v
# Should pass all tests
```

**Test 5: Verify CI Command**
```bash
# Simulate CI environment
unset ANTHROPIC_API_KEY
unset OPENAI_API_KEY
pytest tests/ -v -m "not llm"
# Should pass (what CI will run)
```

---

## Common Issues & Solutions

### Issue 1: Too Many Tests Depend on LLM
**Symptom**: Most tests fail without API keys
**Solution**:
- Mock LLM responses in unit tests
- Use `llm_client` fixture with auto-skip
- Separate unit tests from integration tests

### Issue 2: Tests Import LLMClient Indirectly
**Symptom**: Test fails even though not marked as LLM test
**Solution**:
- Check import chain
- May need to mock LLMClient at module level
- Consider lazy loading of LLM client

### Issue 3: CI Still Fails
**Symptom**: Updated workflow but CI still red
**Solution**:
- Verify `.github/workflows/tests.yml` syntax
- Check pytest.ini is committed
- Ensure markers are properly defined
- Review CI logs for actual error

---

## Expected File Changes

### Modified Files
1. `services/llm/clients.py` (~20-30 lines changed)
2. `pytest.ini` (created or updated, ~10 lines)
3. `.github/workflows/tests.yml` (~5 lines changed)
4. `tests/conftest.py` or similar (optional fixture, ~15 lines)
5. 10-15 test files (add `@pytest.mark.llm` decorator)
6. `README.md` or `TESTING.md` (documentation)

### Commit Strategy
```bash
# Commit 1: LLM client graceful initialization
git commit -m "feat(llm): Make LLMClient initialization graceful without API keys"

# Commit 2: Test infrastructure
git commit -m "test: Add pytest markers for LLM-dependent tests"

# Commit 3: CI update
git commit -m "ci: Skip LLM tests in CI environment"

# Commit 4: Documentation
git commit -m "docs: Document testing strategy for LLM tests"
```

---

## Time Budget

- **Task 1** (LLMClient graceful init): 30 minutes
- **Task 2** (Pytest markers): 15 minutes
- **Task 3** (CI workflow): 10 minutes
- **Task 4** (Documentation): 5 minutes
- **Total**: 60 minutes (1 hour)

**If Exceeds 75 minutes**:
- Stop and report progress
- May need architectural review
- Can defer optional features

---

## Success Metrics

**Before**:
- ❌ Tests workflow: FAILING (can't import LLMClient)
- ❌ CI: Red (blocks all testing)
- ❌ Regression detection: BLOCKED

**After**:
- ✅ Tests workflow: PASSING (runs non-LLM tests)
- ✅ CI: Green (catches regressions)
- ✅ Regression detection: OPERATIONAL
- ✅ Local testing: Full suite available with keys

---

## Context for Code Agent

**This is Issue 2 of 3** blocking issues before GAP-3.

**Issue 1 Status**: ✅ COMPLETE (6 minutes, 24 min under estimate!)

**Why This Matters**:
- Unblocks CI testing capability
- Enables regression detection
- Foundation for GAP-3 quality validation
- Uses existing 2-provider fallback (defer 4-provider to future)

**PM's Mood**: Still excellent! Foundation-building day going well.

**Philosophy**: Make initialization graceful, not fragile. Fail late with clear messages, not early with cryptic errors.

---

## Next Steps After Completion

1. Report completion to Lead Developer
2. Provide evidence:
   - Import test results
   - Test run results (with/without keys)
   - CI workflow verification
3. Move to Issue 3: Document LLM architecture (30 min)
4. Then: GAP-3 (6-8 hours)

---

**Issue 2 Start Time**: 8:10 AM
**Expected Completion**: 9:10 AM
**Status**: Ready for Code Agent execution

**LET'S FIX TESTING! 🧪**
