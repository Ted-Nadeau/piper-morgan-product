# Code Agent Prompt: Phase 3 - Enhanced Validation Verification

**Date**: October 15, 2025, 9:37 AM
**Sprint**: A2 - Notion & Errors
**Issue**: CORE-NOTN #142 - API connectivity fix
**Phase**: 3 (Final Validation)
**Duration**: ~10 minutes
**Agent**: Code Agent

---

## Mission

Verify that enhanced validation in the Notion configuration loader now works end-to-end with the new `get_current_user()` method.

**Context**:
- Phase 1 implemented the method ✅
- Phase 2 tested comprehensively (including real API) ✅
- Phase 3: Confirm the original issue is resolved ✅

**Philosophy**: Test end-to-end, not just unit tests. Verify the actual use case works.

---

## Original Issue Context

**Error Location**: `config/notion_user_config.py:373` (or nearby)
**Original Error**: `AttributeError: 'NotionMCPAdapter' object has no attribute 'get_current_user'`
**Expected Now**: Enhanced validation should call `adapter.get_current_user()` successfully

---

## Verification Steps

### Step 1: Review the Config Validation Code

```bash
# Find where enhanced validation uses get_current_user()
grep -n "get_current_user" config/notion_user_config.py

# View the context around the call
view config/notion_user_config.py -r [365, 385]
```

**Document**:
- Exact line where `get_current_user()` is called
- Validation level that triggers it (should be "enhanced" or "full")
- How the result is used

---

### Step 2: Create End-to-End Validation Test

**File**: `tests/integration/config/test_notion_enhanced_validation.py` (or add to existing)

```python
"""End-to-end test for enhanced Notion configuration validation."""
import pytest
from unittest.mock import AsyncMock, MagicMock
from config.notion_user_config import NotionUserConfig
from services.integrations.mcp.notion_adapter import NotionMCPAdapter


@pytest.mark.asyncio
async def test_enhanced_validation_calls_get_current_user():
    """
    Test that enhanced validation successfully calls adapter.get_current_user().

    This is the end-to-end test that verifies CORE-NOTN #142 is fixed.
    The original error was AttributeError at line 373 (approx).
    """
    # Create a real NotionMCPAdapter (or mock if no API key)
    # Mock the underlying Notion client
    mock_adapter = AsyncMock(spec=NotionMCPAdapter)
    mock_adapter.get_current_user = AsyncMock(return_value={
        "id": "test-user-123",
        "name": "Test User",
        "email": "test@example.com",
        "type": "person"
    })

    # Create config with enhanced validation level
    config = NotionUserConfig(
        api_token="test-token-123",
        validation_level="enhanced"  # This triggers get_current_user() call
    )

    # Run validation - this should NOT raise AttributeError anymore
    try:
        # If there's a validate() method that takes an adapter
        result = await config.validate(adapter=mock_adapter)

        # Verify get_current_user() was called
        mock_adapter.get_current_user.assert_called_once()

        # Validation should succeed
        assert result is True or result.get("valid") is True

        print("✅ Enhanced validation successfully called get_current_user()")
        print(f"✅ Original issue CORE-NOTN #142 is RESOLVED")

    except AttributeError as e:
        if "get_current_user" in str(e):
            pytest.fail(f"FAILED: get_current_user() still missing! Error: {e}")
        else:
            raise


@pytest.mark.asyncio
async def test_full_validation_calls_get_current_user():
    """
    Test that full validation also calls get_current_user().

    Full validation should include everything from enhanced validation.
    """
    mock_adapter = AsyncMock(spec=NotionMCPAdapter)
    mock_adapter.get_current_user = AsyncMock(return_value={
        "id": "bot-456",
        "name": "Piper Morgan",
        "type": "bot"
    })

    config = NotionUserConfig(
        api_token="test-token-456",
        validation_level="full"  # Full validation should also work
    )

    result = await config.validate(adapter=mock_adapter)

    # Should call get_current_user()
    mock_adapter.get_current_user.assert_called()

    print("✅ Full validation successfully called get_current_user()")
```

---

### Step 3: Run the Validation Test

```bash
# Run the new end-to-end test
pytest tests/integration/config/test_notion_enhanced_validation.py -v -s

# Should see output like:
# ✅ Enhanced validation successfully called get_current_user()
# ✅ Original issue CORE-NOTN #142 is RESOLVED
```

**Expected Result**: Test passes, confirming the fix works ✅

---

### Step 4: Test with Real API (If Possible)

If we can safely test with real Notion API:

```python
@pytest.mark.skipif(
    not os.getenv("NOTION_API_KEY"),
    reason="Requires NOTION_API_KEY"
)
@pytest.mark.asyncio
async def test_enhanced_validation_with_real_api():
    """Test enhanced validation with real Notion API."""
    api_key = os.getenv("NOTION_API_KEY")

    # Create real adapter
    adapter = NotionMCPAdapter(api_token=api_key)

    # Create config with enhanced validation
    config = NotionUserConfig(
        api_token=api_key,
        validation_level="enhanced"
    )

    # This should work without errors
    result = await config.validate(adapter=adapter)

    print(f"✅ Real API enhanced validation successful!")
    print(f"✅ User authenticated: {result.get('user_name', 'N/A')}")
```

Run with real key:
```bash
# Load .env and run
source .env
pytest tests/integration/config/test_notion_enhanced_validation.py::test_enhanced_validation_with_real_api -v -s
```

---

### Step 5: Verify All Validation Levels Still Work

```bash
# Quick test to ensure we didn't break basic validation
pytest tests/unit/config/ -k notion -v

# Check integration tests still pass
pytest tests/integration/config/ -k notion -v
```

**Expected**: All existing tests still pass (no regressions)

---

### Step 6: Final Documentation Update

Create a completion summary: `/tmp/phase-3-validation-complete.md`

```markdown
# Phase 3: Enhanced Validation Verification - COMPLETE ✅

## Issue Resolution Confirmed

**Original Issue**: CORE-NOTN #142
**Error**: AttributeError: NotionMCPAdapter missing get_current_user()
**Location**: config/notion_user_config.py:373 (approx)

**Resolution**: ✅ VERIFIED WORKING

## What We Verified

1. ✅ get_current_user() method exists and works
2. ✅ Enhanced validation successfully calls the method
3. ✅ No AttributeError raised
4. ✅ Validation completes successfully
5. ✅ All existing tests still pass (no regressions)
6. ✅ Real API test confirms production readiness

## Test Results

- End-to-end validation test: PASSED ✅
- Enhanced validation tier: FUNCTIONAL ✅
- Full validation tier: FUNCTIONAL ✅
- Real API test (optional): PASSED ✅
- Existing tests: ALL PASSING ✅

## Acceptance Criteria Status

- [x] Add get_current_user() method to NotionMCPAdapter
- [x] Enhanced validation level successfully tests API connectivity
- [x] All validation tiers (basic/enhanced/full) functional
- [x] Integration tests verify enhanced validation working

## Issue #142: RESOLVED ✅

**Total Time**: ~50 minutes (vs 2-3 hours estimated)
- Phase -1: Investigation (25 min)
- Phase 1: Implementation (3 min)
- Phase 2: Testing (10 min + real API)
- Phase 3: Validation (10 min)

**Efficiency**: 70%+ time savings due to finding existing functionality

## Ready for Closure

Issue CORE-NOTN #142 is complete and ready to close! 🎉
```

---

## Deliverables

### Phase 3 Complete When:
- [ ] End-to-end validation test created and passing
- [ ] Enhanced validation confirmed working
- [ ] Full validation confirmed working
- [ ] Real API test (if possible) passes
- [ ] No regressions in existing tests
- [ ] Completion summary created
- [ ] Tests committed and pushed

---

## Git Commit

```bash
git add tests/integration/config/test_notion_enhanced_validation.py
git add dev/2025/10/15/phase-3-validation-complete.md  # completion summary

git commit -m "test(notion): verify enhanced validation end-to-end

End-to-end validation confirms CORE-NOTN #142 is fully resolved.

Tests confirm:
- Enhanced validation calls get_current_user() successfully
- Full validation also works
- No AttributeError raised
- All validation tiers functional

Issue CORE-NOTN #142: RESOLVED ✅

Part of: Sprint A2, Phase 3 (Final Validation)"

git push origin main
```

---

## What NOT to Do

- ❌ Don't skip the end-to-end test (unit tests aren't enough!)
- ❌ Don't forget to test both enhanced and full validation
- ❌ Don't ignore existing test regressions
- ❌ Don't forget to create completion summary

## What TO Do

- ✅ Test the actual use case (enhanced validation)
- ✅ Verify original error is gone
- ✅ Check all validation levels work
- ✅ Run existing tests to ensure no regressions
- ✅ Document completion clearly
- ✅ Celebrate the fix! 🎉

---

## Success Criteria

**Phase 3 is successful when**:
- Enhanced validation works without AttributeError
- End-to-end test passes
- All acceptance criteria met
- Issue #142 can be closed with confidence
- Ready to move to next issue (#136)

---

## Time Budget

**Target**: ~10 minutes
- Review config code: 2 min
- Create e2e test: 4 min
- Run tests: 2 min
- Document completion: 2 min

---

## Context

**Why This Matters**:
- This is the ACTUAL fix validation
- Unit tests alone don't prove the integration works
- Need to confirm original error is resolved
- Gives confidence to close the issue

**What Comes After**:
- Close issue #142 ✅
- Move to CORE-NOTN #136 (remove hardcoding)
- Continue Sprint A2

---

**Phase 3 Start Time**: 9:37 AM
**Expected Completion**: ~9:47 AM (10 minutes)
**Status**: Ready for final validation

**LET'S VERIFY THE FIX!** ✅

---

*"Trust, but verify. Always test end-to-end."*
*- Phase 3 Philosophy*
