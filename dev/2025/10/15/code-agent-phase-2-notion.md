# Code Agent Prompt: Phase 2 - Add Tests for get_current_user()

**Date**: October 15, 2025, 8:49 AM
**Sprint**: A2 - Notion & Errors
**Issue**: CORE-NOTN #142 - API connectivity fix
**Phase**: 2 (Testing)
**Duration**: ~20 minutes
**Agent**: Code Agent

---

## Mission

Add comprehensive test coverage for the new `get_current_user()` method in NotionMCPAdapter.

**Context**: Phase 1 implemented the method in ~3-4 minutes (functionality already existed!). Now we need proper test coverage to ensure it works correctly and handles errors gracefully.

**Philosophy**: Test the happy path, test the sad paths, test edge cases.

---

## Testing Strategy

### Test File Location

**Primary test file**: `tests/unit/integrations/mcp/test_notion_adapter.py`

**Check if file exists**:
```bash
# Find the test file
find tests -name "*notion*adapter*.py" -type f | grep -v __pycache__
```

**If file doesn't exist**: Create it following existing adapter test patterns

---

## Tests to Add

### Test 1: Successful User Retrieval (Happy Path)

```python
@pytest.mark.asyncio
async def test_get_current_user_success(self):
    """Test successful retrieval of current user information."""
    # Mock the Notion client response
    mock_user = MagicMock()
    mock_user.id = "user-123"
    mock_user.name = "Test User"
    mock_user.type = "person"
    mock_user.person = MagicMock()
    mock_user.person.email = "test@example.com"

    self.adapter._notion_client.users.me.return_value = mock_user

    # Call the method
    result = await self.adapter.get_current_user()

    # Assertions
    assert result is not None
    assert result["id"] == "user-123"
    assert result["name"] == "Test User"
    assert result["type"] == "person"
    assert result["email"] == "test@example.com"
    assert "workspace" not in result  # person type doesn't have workspace
```

### Test 2: Bot User Type

```python
@pytest.mark.asyncio
async def test_get_current_user_bot_type(self):
    """Test retrieval of bot user with workspace info."""
    # Mock bot user
    mock_user = MagicMock()
    mock_user.id = "bot-456"
    mock_user.name = "Test Bot"
    mock_user.type = "bot"
    mock_user.bot = MagicMock()
    mock_user.bot.workspace_name = "Test Workspace"

    self.adapter._notion_client.users.me.return_value = mock_user

    result = await self.adapter.get_current_user()

    assert result is not None
    assert result["id"] == "bot-456"
    assert result["type"] == "bot"
    assert result["workspace"]["name"] == "Test Workspace"
```

### Test 3: API Error Handling

```python
@pytest.mark.asyncio
async def test_get_current_user_api_error(self):
    """Test handling of Notion API errors."""
    from notion_client.errors import APIResponseError

    # Mock API error
    self.adapter._notion_client.users.me.side_effect = APIResponseError(
        response=MagicMock(status_code=401),
        message="Unauthorized",
        code="unauthorized"
    )

    # Should raise APIResponseError
    with pytest.raises(APIResponseError):
        await self.adapter.get_current_user()
```

### Test 4: Timeout Error Handling

```python
@pytest.mark.asyncio
async def test_get_current_user_timeout(self):
    """Test handling of request timeout."""
    from notion_client.errors import RequestTimeoutError

    # Mock timeout
    self.adapter._notion_client.users.me.side_effect = RequestTimeoutError()

    # Should raise RequestTimeoutError
    with pytest.raises(RequestTimeoutError):
        await self.adapter.get_current_user()
```

### Test 5: Missing Email (Edge Case)

```python
@pytest.mark.asyncio
async def test_get_current_user_missing_email(self):
    """Test user without email field."""
    mock_user = MagicMock()
    mock_user.id = "user-789"
    mock_user.name = "No Email User"
    mock_user.type = "person"
    # No person.email attribute
    del mock_user.person

    self.adapter._notion_client.users.me.return_value = mock_user

    result = await self.adapter.get_current_user()

    assert result is not None
    assert result["id"] == "user-789"
    assert result.get("email") is None  # Should handle missing email gracefully
```

---

## Integration Test

### Test in config/notion_user_config.py Context

**File**: `tests/integration/config/test_notion_config_validation.py`

```python
@pytest.mark.asyncio
async def test_enhanced_validation_with_get_current_user(self):
    """Test that enhanced validation can now call get_current_user()."""
    # Mock NotionMCPAdapter
    mock_adapter = AsyncMock(spec=NotionMCPAdapter)
    mock_adapter.get_current_user.return_value = {
        "id": "user-123",
        "name": "Test User",
        "email": "test@example.com",
        "type": "person"
    }

    # Create config with enhanced validation
    config = NotionUserConfig(
        api_token="test-token",
        validation_level="enhanced"
    )

    # This should now work without AttributeError
    result = await config.validate_with_adapter(mock_adapter)

    assert result is True
    mock_adapter.get_current_user.assert_called_once()
```

---

## Implementation Steps

### Step 1: Find/Create Test File

```bash
# Check existing test structure
ls -la tests/unit/integrations/mcp/ 2>/dev/null || echo "Directory may not exist"

# If needed, create test file following existing patterns
```

---

### Step 2: Add Unit Tests

**If test file exists**: Add new test methods to existing test class

**If creating new file**: Follow this structure:

```python
"""Tests for NotionMCPAdapter.get_current_user() method."""
import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from services.integrations.mcp.notion_adapter import NotionMCPAdapter
from notion_client.errors import APIResponseError, RequestTimeoutError


class TestNotionAdapterGetCurrentUser:
    """Test suite for get_current_user() method."""

    def setup_method(self):
        """Set up test fixtures."""
        self.adapter = NotionMCPAdapter(api_token="test-token")
        # Mock the Notion client
        self.adapter._notion_client = MagicMock()

    # Add all test methods here...
```

---

### Step 3: Run Tests

```bash
# Run just the new tests
pytest tests/unit/integrations/mcp/test_notion_adapter.py::TestNotionAdapterGetCurrentUser -v

# Run all Notion adapter tests
pytest tests/unit/integrations/mcp/test_notion_adapter.py -v

# Run integration test
pytest tests/integration/config/test_notion_config_validation.py -v
```

**Expected**: All new tests pass ✅

---

### Step 4: Verify Coverage

```bash
# Quick coverage check (optional but nice)
pytest tests/unit/integrations/mcp/test_notion_adapter.py --cov=services.integrations.mcp.notion_adapter --cov-report=term-missing | grep get_current_user
```

**Goal**: High coverage on the new method

---

### Step 5: Commit Tests

```bash
git add tests/unit/integrations/mcp/test_notion_adapter.py
git add tests/integration/config/test_notion_config_validation.py  # if added

git commit -m "test(notion): add comprehensive tests for get_current_user()

Tests cover:
- Happy path (person and bot user types)
- Error handling (API errors, timeouts)
- Edge cases (missing email)
- Integration with config validation

All tests passing with good coverage.

Part of: CORE-NOTN #142, Sprint A2, Phase 2"

git push origin main
```

---

## Deliverables

### Phase 2 Complete When:
- [ ] Unit tests added (5 test cases minimum)
- [ ] Integration test added for config validation
- [ ] All tests pass
- [ ] Good coverage on new method
- [ ] Tests committed and pushed

---

## What NOT to Do

- ❌ Don't skip edge cases
- ❌ Don't forget error handling tests
- ❌ Don't test implementation details (test behavior)
- ❌ Don't modify the implementation (unless bug found)

## What TO Do

- ✅ Test happy path thoroughly
- ✅ Test all error scenarios
- ✅ Test edge cases (missing fields)
- ✅ Test integration with config validation
- ✅ Use proper mocks (AsyncMock for async methods)
- ✅ Clear test names and docstrings

---

## Success Criteria

**Testing is successful when**:
- All new tests pass
- Error handling verified
- Edge cases covered
- Integration test confirms fix works
- No regression in existing tests
- Tests committed to git

---

## Time Budget

**Target**: ~20 minutes
- Find/setup test file: 5 min
- Write unit tests: 10 min
- Write integration test: 3 min
- Run and verify: 2 min
- Git commit: 5 min (includes running full test suite)

---

## Context

**Why Testing Matters**:
- Method will be used by config validation (critical path)
- Error handling must be robust (API calls can fail)
- Edge cases matter (bots vs persons, missing fields)
- Prevents regressions in future changes

**What Comes After**:
- Phase 3: Verify enhanced validation works end-to-end
- Confirm issue #142 is fully resolved

---

**Phase 2 Start Time**: 8:49 AM
**Expected Completion**: ~9:09 AM (20 minutes)
**Status**: Ready for testing implementation

**LET'S TEST IT THOROUGHLY!** 🧪

---

*"If it's not tested, it's not done."*
*- Phase 2 Philosophy*
