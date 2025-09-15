# ADR-026: Notion Client Migration to Official Library

**Status:** Accepted
**Date:** 2025-08-28
**Context:** Notion Integration Cleanup and CLI Enhancement
**Decision Maker:** Lead Developer (Code Agent)
**Stakeholders:** Chief Architect, Integration Team

## Summary

Migrate from custom `aiohttp`-based Notion API implementation to the official `notion_client` Python library to improve reliability, maintainability, and feature completeness while eliminating custom HTTP request handling and authentication logic.

## Context

### Problem Statement

The existing Notion integration used a custom implementation with several limitations:

1. **Custom HTTP Implementation:**

   - Manual `aiohttp` request construction
   - Custom authentication header handling
   - Manual JSON parsing and error handling
   - No built-in rate limiting or retry logic

2. **Maintenance Burden:**

   - Custom code requires updates for API changes
   - Authentication token handling not standardized
   - Error handling inconsistent with official patterns

3. **Feature Limitations:**
   - Limited to basic CRUD operations
   - No access to advanced Notion API features
   - Manual pagination handling
   - No built-in validation

### Current State Analysis

**Files with Custom Implementation:**

- `services/integrations/mcp/notion_adapter.py` - Custom aiohttp client
- Manual request construction and response parsing
- Custom error handling and status code checking

**Integration Points:**

- CLI commands in `cli/commands/notion.py`
- MCP adapter for spatial intelligence
- Canonical query enhancement

## Decision

### Primary Decision

**Replace custom `aiohttp`-based Notion API implementation with the official `notion_client` library** to leverage official support, improved reliability, and enhanced features.

### Migration Strategy

1. **Library Selection:**

   ```bash
   # Official Notion Python client
   pip install notion-client
   ```

2. **Client Initialization:**

   ```python
   # BEFORE: Custom aiohttp client
   self.session = aiohttp.ClientSession()

   # AFTER: Official notion_client
   from notion_client import AsyncClient
   self.client = AsyncClient(auth=os.getenv("NOTION_API_KEY"))
   ```

3. **API Call Migration:**

   ```python
   # BEFORE: Custom HTTP requests
   async with self.session.get(url, headers=headers) as response:
       if response.status == 200:
           return await response.json()

   # AFTER: Official client methods
   result = await self.client.search(query=query, filter=filter_params)
   ```

4. **Error Handling:**

   ```python
   # BEFORE: Manual status code checking
   if response.status != 200:
       raise Exception(f"API error: {response.status}")

   # AFTER: Official exception handling
   try:
       result = await self.client.search(...)
   except APIResponseError as e:
       # Handle specific Notion API errors
   ```

## Implementation

### Migration Steps Completed

1. **Dependency Update:**

   - Added `notion-client` to requirements
   - Removed custom aiohttp Notion code

2. **Client Refactoring:**

   - Updated `NotionMCPAdapter` to use `AsyncClient`
   - Migrated all API methods to official client calls
   - Standardized error handling patterns

3. **CLI Enhancement:**

   - Added `create` command for page creation
   - Enhanced `pages` command with proper page listing
   - Improved error messages and user feedback

4. **Testing Verification:**
   - Full end-to-end CRUD testing completed
   - All CLI commands verified functional
   - Integration status confirmed stable

### Code Changes

**NotionMCPAdapter Updates:**

```python
# services/integrations/mcp/notion_adapter.py
from notion_client import AsyncClient

class NotionMCPAdapter:
    def __init__(self):
        self.client = AsyncClient(auth=os.getenv("NOTION_API_KEY"))

    async def search_notion(self, query: str, filter_type: str = None):
        filter_params = {"property": "object", "value": filter_type} if filter_type else {}
        return await self.client.search(query=query, filter=filter_params)

    async def create_page(self, parent_id: str, properties: dict):
        return await self.client.pages.create(
            parent={"page_id": parent_id},
            properties=properties
        )
```

**CLI Command Enhancements:**

```python
# cli/commands/notion.py
async def cmd_create(self, title: str, parent_id: Optional[str] = None):
    """Create a new Notion page"""
    # Smart parent selection and page creation
    result = await self.adapter.create_page(parent_id, properties)
```

## Consequences

### Positive Outcomes

1. **Improved Reliability:**

   - Official library handles API changes automatically
   - Built-in rate limiting and retry logic
   - Standardized error handling and status codes

2. **Enhanced Features:**

   - Access to all Notion API capabilities
   - Better pagination and filtering support
   - Improved type safety and validation

3. **Reduced Maintenance:**

   - No custom HTTP code to maintain
   - Automatic updates for API changes
   - Community support and documentation

4. **Better Integration:**
   - Consistent with Notion ecosystem
   - Easier debugging and troubleshooting
   - Future-proof for new API features

### Risks and Mitigation

1. **Dependency Risk:**

   - **Risk:** External library dependency
   - **Mitigation:** Official library with active maintenance

2. **Breaking Changes:**

   - **Risk:** Library updates may introduce breaking changes
   - **Mitigation:** Pin version requirements and test thoroughly

3. **Migration Complexity:**
   - **Risk:** API method signature changes
   - **Mitigation:** Comprehensive testing and validation

## Testing and Validation

### Test Coverage

- **Unit Tests:** All adapter methods tested with official client
- **Integration Tests:** Full CLI command validation
- **End-to-End Tests:** Complete CRUD cycle verification
- **Error Handling:** API error scenarios tested

### Validation Results

- ✅ **Connection:** Stable API connection established
- ✅ **Read Operations:** Search and page listing functional
- ✅ **Create Operations:** Page creation with smart parent selection
- ✅ **CLI Interface:** All commands working correctly
- ✅ **Error Handling:** Graceful degradation maintained

## Future Considerations

1. **Advanced Features:**

   - Database querying and filtering
   - Block-level content manipulation
   - Real-time synchronization

2. **Performance Optimization:**

   - Connection pooling for high-volume operations
   - Caching strategies for frequently accessed content
   - Batch operations for multiple pages

3. **Monitoring and Observability:**
   - API call metrics and performance tracking
   - Error rate monitoring and alerting
   - Usage analytics and optimization

## References

- [Notion API Documentation](https://developers.notion.com/)
- [notion-client Python Library](https://github.com/ramnes/notion-sdk-py)
- [ADR-017: Spatial MCP Integration](./adr-017-spatial-mcp.md)
- Notion Integration (coming soon)
