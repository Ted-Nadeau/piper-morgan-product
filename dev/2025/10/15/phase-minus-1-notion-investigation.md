# Phase -1: NotionMCPAdapter Investigation

**Date**: October 15, 2025, 8:20 AM
**Sprint**: A2 - Notion & Errors
**Issue**: CORE-NOTN #142 - API connectivity fix
**Duration**: 25 minutes
**Status**: ✅ COMPLETE

---

## Executive Summary

**Problem**: Enhanced validation in `config/notion_user_config.py:373` calls `adapter.get_current_user()` but this method doesn't exist in NotionMCPAdapter.

**Good News**: The adapter already uses `self._notion_client.users.me()` internally (lines 110, 135) for connection testing. We just need to expose this functionality as a public method.

**Implementation**: Simple - extract existing pattern into public method.

---

## Current State

### NotionMCPAdapter Location
- **File**: `services/integrations/mcp/notion_adapter.py`
- **Lines**: 544 total
- **Class Structure**: Inherits from `BaseSpatialAdapter`
- **Purpose**: Notion MCP spatial adapter for external system integration

### Existing Methods (27 total)

**Connection & Configuration**:
- `__init__(config_service)` - Initialize with config service injection
- `_initialize_client()` - Internal client initialization
- `connect(integration_token)` - Connect to Notion with token
- `test_connection()` - Test API connection (uses users.me() internally!)
- `is_configured()` - Check if properly configured

**Workspace & User Operations**:
- `get_workspace_info()` - Get workspace info (uses users.me() internally!)
- `get_user(user_id)` - Get specific user by ID
- `list_users()` - List workspace users

**Database Operations**:
- `fetch_databases(page_size)` - Fetch accessible databases (alias)
- `list_databases(page_size)` - List all databases
- `get_database(database_id)` - Get specific database
- `query_database(database_id, filter_params, sorts, page_size)` - Query database
- `create_database_item(database_id, properties, content)` - Create database item

**Page Operations**:
- `get_page(page_id)` - Get page content and properties
- `get_page_blocks(page_id, page_size)` - Get page content blocks
- `update_page(page_id, properties)` - Update page
- `create_page(parent_id, properties, content)` - Create new page
- `_validate_parent_exists(parent_id)` - Validate parent exists

**Search Operations**:
- `search_notion(query, filter_type, page_size)` - Search workspace

**Utility Methods**:
- `get_mapping_stats()` - Get mapping statistics
- `close()` - Clean up resources
- `__del__()` - Destructor

### Missing Method

**Method Needed**: `get_current_user()`

**Called From**: `config/notion_user_config.py:373`

**Context** (from notion_user_config.py:353-380):
```python
async def validate_async(self, level: Optional[ValidationLevel] = None) -> ValidationResult:
    """Asynchronous validation supporting all levels"""
    validation_level = level or self.validation_level

    # Start with basic validation
    result = self.validate(validation_level)

    if not result.format_valid or not result.environment_valid:
        return result

    # Enhanced validation: API connectivity
    if validation_level in [ValidationLevel.ENHANCED, ValidationLevel.FULL]:
        if self.validation_connectivity_check:
            try:
                from services.integrations.mcp.notion_adapter import NotionMCPAdapter

                adapter = NotionMCPAdapter()
                await adapter.connect()

                # Test connectivity by getting user info
                user_info = await adapter.get_current_user()  # <-- LINE 373: MISSING METHOD
                result.connectivity_tested = True
                result.connectivity_result = bool(user_info)

            except Exception as e:
                result.connectivity_tested = True
                result.connectivity_result = False
                result.errors.append(f"API connectivity failed: {e}")
```

**Expected Behavior**:
- Get current authenticated user from Notion API
- Return user information (id, name, email, etc.)
- Support async operation
- Raise appropriate exceptions on failure

---

## Similar Patterns

### Existing users.me() Usage in NotionMCPAdapter

**Pattern 1: test_connection() method** (lines 101-124):
```python
async def test_connection(self) -> bool:
    """Test Notion API connection and authentication"""
    try:
        if not self._notion_client:
            logger.error("Notion client not initialized")
            return False

        # Test with a simple API call to retrieve user info
        try:
            user_info = self._notion_client.users.me()  # <-- EXISTING USAGE
            logger.info(
                f"Notion API connection successful - User: {user_info.get('name', 'Unknown')}"
            )
            return True
        except APIResponseError as e:
            logger.error(f"Notion API authentication failed: {e}")
            return False
        except RequestTimeoutError as e:
            logger.error(f"Notion API request timeout: {e}")
            return False

    except Exception as e:
        logger.error(f"Error testing Notion connection: {e}")
        return False
```

**Pattern 2: get_workspace_info() method** (lines 130-148):
```python
async def get_workspace_info(self) -> Optional[Dict[str, Any]]:
    """Get Notion workspace information using notion_client"""
    try:
        # Note: Notion doesn't have a direct workspace endpoint
        # We'll use the user info as a proxy for workspace access
        user_info = self._notion_client.users.me()  # <-- EXISTING USAGE
        if user_info:
            return {
                "workspace_id": user_info.get("bot", {}).get("workspace", {}).get("id"),
                "workspace_name": user_info.get("bot", {}).get("workspace", {}).get("name"),
                "user_id": user_info.get("id"),
                "user_name": user_info.get("name"),
                "user_email": user_info.get("person", {}).get("email"),
            }
        return None

    except Exception as e:
        logger.error(f"Error getting workspace info: {e}")
        return None
```

### Other Adapter Patterns

**SlackAdapter** - `get_user_info(user)`:
```python
# services/integrations/slack/slack_integration_router.py:205
async def get_user_info(self, user: str) -> SlackResponse:
```

**SlackClient** - `get_user_info(user)`:
```python
# services/integrations/slack/slack_client.py:230
async def get_user_info(self, user: str) -> SlackResponse:
```

### Key Insight

The adapter **already has the functionality** - it just needs to be exposed as a public method! Both `test_connection()` and `get_workspace_info()` successfully call `self._notion_client.users.me()`.

---

## Notion API Context

### Current API Usage

**Notion Client**: `notion_client` library
- Imported: `from notion_client import Client`
- Error types: `APIResponseError`, `RequestTimeoutError`
- User endpoint: `client.users.me()` - **already in use!**

### Authentication

**Pattern**: Token-based authentication
```python
self._notion_client = Client(auth=api_key)
```

**Sources**:
1. Environment variable: `NOTION_API_KEY`
2. Configuration: `self.config.get_api_key()`
3. Direct injection: `integration_token` parameter

### Available Capabilities

**Users API** (from notion_client):
- `users.me()` - Get current authenticated user (**already used!**)
- `users.retrieve(user_id)` - Get specific user (implemented as `get_user()`)
- `users.list()` - List workspace users (implemented as `list_users()`)

**Current User Response Format** (from existing usage):
```python
{
    "id": "user_id",
    "name": "User Name",
    "type": "person",  # or "bot"
    "person": {
        "email": "user@example.com"
    },
    "bot": {  # if bot integration
        "workspace": {
            "id": "workspace_id",
            "name": "Workspace Name"
        }
    }
}
```

---

## Implementation Approach

### Recommended Method Signature

```python
async def get_current_user(self) -> Optional[Dict[str, Any]]:
    """
    Get current authenticated Notion user.

    Returns user information from the Notion API to verify authentication
    and provide user context for operations.

    Returns:
        Dict with user information:
        {
            "id": str,          # User ID
            "name": str,        # User name
            "email": str,       # User email (if person)
            "type": str,        # "person" or "bot"
            "workspace": {      # Workspace info (if bot)
                "id": str,
                "name": str
            }
        }
        Returns None if not authenticated or connection fails.

    Raises:
        APIResponseError: If Notion API returns an error
        RequestTimeoutError: If API request times out

    Example:
        >>> adapter = NotionMCPAdapter()
        >>> await adapter.connect()
        >>> user = await adapter.get_current_user()
        >>> print(f"Authenticated as: {user['name']}")
    """
    try:
        if not self._notion_client:
            logger.error("Notion client not initialized")
            return None

        # Get current user info from Notion API
        user_info = self._notion_client.users.me()

        if not user_info:
            logger.warning("Notion API returned empty user info")
            return None

        # Extract and normalize user information
        result = {
            "id": user_info.get("id"),
            "name": user_info.get("name"),
            "type": user_info.get("type"),
        }

        # Add email for person users
        if user_info.get("person"):
            result["email"] = user_info.get("person", {}).get("email")

        # Add workspace info for bot users
        if user_info.get("bot"):
            result["workspace"] = {
                "id": user_info.get("bot", {}).get("workspace", {}).get("id"),
                "name": user_info.get("bot", {}).get("workspace", {}).get("name"),
            }

        logger.info(f"Retrieved current user: {result.get('name')} ({result.get('id')})")
        return result

    except APIResponseError as e:
        logger.error(f"Notion API error getting current user: {e}")
        raise
    except RequestTimeoutError as e:
        logger.error(f"Notion API timeout getting current user: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error getting current user: {e}")
        return None
```

### Why This Approach?

1. **Reuses Existing Pattern**: Mirrors `test_connection()` and `get_workspace_info()` usage
2. **Consistent Error Handling**: Follows adapter's error handling patterns
3. **Proper Logging**: Matches adapter's logging style
4. **Returns Optional**: Allows None return for non-critical failures
5. **Raises Exceptions**: Critical errors (API errors) are raised for caller handling
6. **Normalized Response**: Extracts relevant fields consistently
7. **Documentation**: Clear docstring with examples

### Dependencies Needed

**None!** All imports already present:
- ✅ `from notion_client import Client`
- ✅ `from notion_client.errors import APIResponseError, RequestTimeoutError`
- ✅ `import logging`

### Where to Insert

**Location**: After `list_users()` method (line 514), before `get_mapping_stats()` (line 516)

**Rationale**:
- Groups with other user-related methods (`get_user()`, `list_users()`)
- Before utility methods section
- Maintains logical organization

---

## Testing Approach

### Unit Testing

**Test File**: `tests/unit/integrations/test_notion_mcp_adapter.py` (create if needed)

**Test Cases**:
```python
@pytest.mark.asyncio
async def test_get_current_user_success():
    """Test successful current user retrieval"""
    adapter = NotionMCPAdapter()
    adapter._notion_client = Mock()
    adapter._notion_client.users.me.return_value = {
        "id": "user_123",
        "name": "Test User",
        "type": "person",
        "person": {"email": "test@example.com"}
    }

    result = await adapter.get_current_user()

    assert result is not None
    assert result["id"] == "user_123"
    assert result["name"] == "Test User"
    assert result["email"] == "test@example.com"

@pytest.mark.asyncio
async def test_get_current_user_no_client():
    """Test behavior when client not initialized"""
    adapter = NotionMCPAdapter()
    adapter._notion_client = None

    result = await adapter.get_current_user()

    assert result is None

@pytest.mark.asyncio
async def test_get_current_user_api_error():
    """Test API error handling"""
    adapter = NotionMCPAdapter()
    adapter._notion_client = Mock()
    adapter._notion_client.users.me.side_effect = APIResponseError(...)

    with pytest.raises(APIResponseError):
        await adapter.get_current_user()
```

### Integration Testing

**Test File**: `tests/integration/test_notion_configuration_integration.py` (already exists)

**Add Test**:
```python
@pytest.mark.asyncio
async def test_enhanced_validation_with_get_current_user():
    """Test that enhanced validation can use get_current_user()"""
    from config.notion_user_config import NotionUserConfig, ValidationLevel

    config = NotionUserConfig.load_from_user_config()
    result = await config.validate_async(ValidationLevel.ENHANCED)

    assert result.connectivity_tested
    # Don't assert connectivity_result True in CI (no API key)
    # Just verify method exists and doesn't crash
```

### Manual Testing

**After Implementation**:
```bash
# Test 1: Direct method call
python -c "
import asyncio
from services.integrations.mcp.notion_adapter import NotionMCPAdapter

async def test():
    adapter = NotionMCPAdapter()
    await adapter.connect()
    user = await adapter.get_current_user()
    print(f'User: {user}')

asyncio.run(test())
"

# Test 2: Via config validation
python -c "
import asyncio
from config.notion_user_config import NotionUserConfig, ValidationLevel

async def test():
    config = NotionUserConfig.load_from_user_config()
    result = await config.validate_async(ValidationLevel.ENHANCED)
    print(f'Validation result: {result.is_valid()}')
    print(f'Connectivity: {result.connectivity_result}')

asyncio.run(test())
"
```

---

## Open Questions

### ✅ Resolved

1. **Q**: Should the method be async?
   **A**: Yes - follows adapter pattern and config expects async.

2. **Q**: What should the method return?
   **A**: `Optional[Dict[str, Any]]` - consistent with other get methods.

3. **Q**: Should it raise exceptions or return None?
   **A**: Both - raise for API errors (caller can handle), return None for non-critical failures.

4. **Q**: Is this feature already implemented elsewhere?
   **A**: No - but the underlying API call (`users.me()`) is already used internally.

### No Open Questions

All implementation details are clear from existing code patterns.

---

## Next Steps

### Phase 1: Implement `get_current_user()` Method

**Tasks**:
1. Add method to `NotionMCPAdapter` (after `list_users()`, ~50 lines)
2. Follow existing patterns from `test_connection()` and `get_workspace_info()`
3. Add proper error handling and logging
4. Add comprehensive docstring

**Duration**: 15-20 minutes

### Phase 2: Update Tests

**Tasks**:
1. Add unit tests to existing test file
2. Update integration test to verify method works
3. Test with mocked responses (no API key needed)

**Duration**: 15-20 minutes

### Phase 3: Verify Enhanced Validation

**Tasks**:
1. Run config validation with BASIC level (should work)
2. Run with ENHANCED level (should work with API key)
3. Verify error handling without API key
4. Test all validation levels

**Duration**: 10 minutes

**Total Estimated Time**: 40-50 minutes for complete implementation and testing

---

## Risk Assessment

### Very Low Risk

**Why**:
1. ✅ **Method already works** - just needs exposure as public method
2. ✅ **No new dependencies** - all imports already present
3. ✅ **Pattern established** - identical to `test_connection()` usage
4. ✅ **Error handling proven** - using same exception types
5. ✅ **Backward compatible** - adding method, not changing existing ones

### Potential Issues

**None identified** - this is a straightforward extraction of existing functionality.

---

## Conclusion

This is an **extremely low-risk, high-confidence implementation**.

**Why We're Confident**:
1. The underlying API call (`users.me()`) already works in the adapter
2. We're just exposing existing functionality as a public method
3. All patterns, error handling, and dependencies are already established
4. Similar methods exist and work correctly
5. Clear use case with existing caller

**Recommended Approach**:
1. Copy pattern from `test_connection()` method
2. Extract user info normalization from `get_workspace_info()`
3. Combine into new public method
4. Add tests mirroring existing user method tests
5. Verify config validation works

**Time to Implementation**: ~45 minutes total (including tests)

**Next Agent Prompt**: Phase 1 - Implement `get_current_user()` Method

---

## Files to Modify

### Primary Implementation
- `services/integrations/mcp/notion_adapter.py` - Add `get_current_user()` method

### Testing
- `tests/unit/integrations/test_notion_mcp_adapter.py` - Add unit tests (create if needed)
- `tests/integration/test_notion_configuration_integration.py` - Add integration test

### Documentation
- Update session log with implementation results

---

**Investigation Status**: ✅ COMPLETE
**Implementation Ready**: ✅ YES
**Next Phase**: Phase 1 - Implementation
**Confidence Level**: VERY HIGH

---

*"Understand first, implement second. This investigation reveals we're 80% done - just need to expose what's already there!"*
