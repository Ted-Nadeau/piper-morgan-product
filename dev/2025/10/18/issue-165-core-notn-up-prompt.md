# CORE-NOTN-UP: Notion Database API Upgrade - Issue #165

**Agent**: Claude Code (Programmer)
**Issue**: #165 - CORE-NOTN-UP (Notion Database API Upgrade Phase 2)
**Sprint**: A3 (final issue!)
**Date**: October 18, 2025, 5:30 PM
**Duration**: ~1.5-2 hours estimated (likely ~1 hour actual)

---

## Mission

Complete Phase 2 of Notion database API integration. This is straightforward plumbing work - implement database CRUD operations, test through MCP layer, and document.

**Cool Down Work**: After today's architectural decisions (MCP, Ethics, Knowledge Graph), this is refreshingly simple implementation.

---

## Context

**Sprint A2 Completed**:
- ✅ Phase 1: Basic Notion connectivity
- ✅ MCP adapter structure (from #198)

**Remaining (Phase 2)**:
- Database CRUD operations
- Integration testing
- Documentation

**This Completes Sprint A3!** 🎯

---

## Phase 0: Assessment (15 minutes)

### Discover Current State

**Use Serena to understand what exists**:

```python
# Find Notion integration files
mcp__serena__find_symbol(
    name_regex="NotionMCP.*|Notion.*Service",
    scope="services/integrations/notion"
)

# Check for database operations
mcp__serena__search_project(
    query="database.*query|create.*page|update.*page",
    file_pattern="**/notion/**/*.py"
)

# Find TODO markers
mcp__serena__search_project(
    query="TODO.*database|TODO.*Phase 2",
    file_pattern="**/notion/**/*.py"
)

# Review existing MCP tools
mcp__serena__get_symbols_overview(
    "services/integrations/notion/mcp_adapter.py"
)
```

### Expected Findings

**Likely Exists**:
- NotionService or NotionClient (basic API)
- NotionMCPAdapter (from #198)
- Basic connectivity/auth working
- Page operations (read/basic write)

**Likely Missing**:
- Database query with filters
- Database page creation
- Database page updates
- Database schema retrieval

### Create Assessment Report

**File**: `dev/2025/10/18/notion-phase-0-assessment.md`

```markdown
# Notion Database API - Phase 0 Assessment

## What Exists (Phase 1)

**Notion Service**: [location]
- Basic API connectivity: [YES/NO]
- Authentication working: [YES/NO]
- Page operations: [list methods]

**MCP Adapter**: [location]
- MCP integration: [YES/NO]
- Available tools: [list tools]

## What's Missing (Phase 2)

**Database Operations**:
- Query database: [MISSING/PARTIAL]
- Create page: [MISSING/PARTIAL]
- Update page: [MISSING/PARTIAL]
- Get schema: [MISSING/PARTIAL]

**Integration**:
- MCP database tools: [MISSING/PARTIAL]
- Tests: [MISSING/PARTIAL]

## Implementation Plan

Based on findings:
1. [Specific files to create/modify]
2. [Methods to implement]
3. [Tests to add]
4. [Documentation to update]

## Estimated Time

[Based on what's actually missing]
```

---

## Phase 1: Database Operations (45 minutes)

### Step 1.1: Database Query (15 minutes)

**File**: `services/integrations/notion/notion_service.py` (or similar)

```python
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class NotionDatabaseOperations:
    """Notion database CRUD operations."""

    def __init__(self, client):
        """
        Initialize database operations.

        Args:
            client: Notion API client instance
        """
        self.client = client

    async def query_database(
        self,
        database_id: str,
        filter_params: Optional[Dict[str, Any]] = None,
        sorts: Optional[List[Dict[str, str]]] = None,
        page_size: int = 100
    ) -> Dict[str, Any]:
        """
        Query Notion database with filters and sorting.

        Args:
            database_id: Notion database ID
            filter_params: Optional filter criteria
            sorts: Optional sorting parameters
            page_size: Number of results per page (max 100)

        Returns:
            Query results with pages and metadata

        Example:
            results = await query_database(
                database_id="abc123",
                filter_params={
                    "property": "Status",
                    "select": {"equals": "Active"}
                },
                sorts=[{"property": "Created", "direction": "descending"}]
            )
        """
        try:
            # Build query payload
            payload = {
                "page_size": min(page_size, 100)  # Notion max is 100
            }

            if filter_params:
                payload["filter"] = filter_params

            if sorts:
                payload["sorts"] = sorts

            # Query database
            response = await self.client.databases.query(
                database_id=database_id,
                **payload
            )

            logger.info(
                f"Queried database {database_id}: "
                f"{len(response.get('results', []))} results"
            )

            return {
                "success": True,
                "results": response.get("results", []),
                "has_more": response.get("has_more", False),
                "next_cursor": response.get("next_cursor"),
                "count": len(response.get("results", []))
            }

        except Exception as e:
            logger.error(f"Database query failed: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "results": []
            }
```

### Step 1.2: Create Database Page (15 minutes)

```python
    async def create_database_page(
        self,
        database_id: str,
        properties: Dict[str, Any],
        content: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Create new page in Notion database.

        Args:
            database_id: Target database ID
            properties: Page properties (database columns)
            content: Optional page content blocks

        Returns:
            Created page info

        Example:
            page = await create_database_page(
                database_id="abc123",
                properties={
                    "Name": {"title": [{"text": {"content": "New Task"}}]},
                    "Status": {"select": {"name": "Active"}},
                    "Priority": {"number": 1}
                }
            )
        """
        try:
            # Build page payload
            payload = {
                "parent": {"database_id": database_id},
                "properties": properties
            }

            if content:
                payload["children"] = content

            # Create page
            response = await self.client.pages.create(**payload)

            logger.info(f"Created page in database {database_id}: {response['id']}")

            return {
                "success": True,
                "page_id": response["id"],
                "url": response.get("url"),
                "created_time": response.get("created_time"),
                "properties": response.get("properties", {})
            }

        except Exception as e:
            logger.error(f"Page creation failed: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }
```

### Step 1.3: Update Database Page (10 minutes)

```python
    async def update_database_page(
        self,
        page_id: str,
        properties: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update existing database page.

        Args:
            page_id: Page ID to update
            properties: Properties to update (partial update supported)

        Returns:
            Updated page info

        Example:
            updated = await update_database_page(
                page_id="page123",
                properties={
                    "Status": {"select": {"name": "Complete"}}
                }
            )
        """
        try:
            # Update page
            response = await self.client.pages.update(
                page_id=page_id,
                properties=properties
            )

            logger.info(f"Updated page {page_id}")

            return {
                "success": True,
                "page_id": response["id"],
                "last_edited_time": response.get("last_edited_time"),
                "properties": response.get("properties", {})
            }

        except Exception as e:
            logger.error(f"Page update failed: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }
```

### Step 1.4: Get Database Schema (5 minutes)

```python
    async def get_database_schema(
        self,
        database_id: str
    ) -> Dict[str, Any]:
        """
        Retrieve database schema (properties and types).

        Args:
            database_id: Database ID

        Returns:
            Schema information
        """
        try:
            # Get database metadata
            response = await self.client.databases.retrieve(
                database_id=database_id
            )

            logger.info(f"Retrieved schema for database {database_id}")

            return {
                "success": True,
                "title": response.get("title", []),
                "properties": response.get("properties", {}),
                "description": response.get("description", []),
                "created_time": response.get("created_time")
            }

        except Exception as e:
            logger.error(f"Schema retrieval failed: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }
```

---

## Phase 2: Integration Testing (30 minutes)

### Step 2.1: Database Operation Tests (20 minutes)

**File**: `dev/2025/10/18/test-notion-database-ops.py`

```python
"""
Test Notion database operations.

Tests all CRUD operations for Notion databases.
"""

import asyncio
import os
from services.integrations.notion.notion_service import NotionDatabaseOperations


async def test_database_query():
    """Test querying a Notion database."""
    print("\n=== Test 1: Database Query ===")

    # This requires actual Notion API key and database ID
    # Use test database if available, otherwise skip
    database_id = os.getenv("NOTION_TEST_DATABASE_ID")

    if not database_id:
        print("⚠️  SKIP: No test database configured")
        print("   Set NOTION_TEST_DATABASE_ID to test")
        return True

    db_ops = NotionDatabaseOperations(notion_client)

    # Query without filters
    results = await db_ops.query_database(database_id)

    if results["success"]:
        print(f"✅ PASS: Query successful")
        print(f"   Found {results['count']} results")
        print(f"   Has more: {results['has_more']}")
    else:
        print(f"❌ FAIL: {results['error']}")
        return False

    # Query with filter
    filtered = await db_ops.query_database(
        database_id,
        filter_params={
            "property": "Status",
            "select": {"equals": "Active"}
        }
    )

    if filtered["success"]:
        print(f"✅ PASS: Filtered query successful")
        print(f"   Found {filtered['count']} active items")
    else:
        print(f"❌ FAIL: {filtered['error']}")
        return False

    return True


async def test_create_page():
    """Test creating a page in Notion database."""
    print("\n=== Test 2: Create Page ===")

    database_id = os.getenv("NOTION_TEST_DATABASE_ID")

    if not database_id:
        print("⚠️  SKIP: No test database configured")
        return True

    db_ops = NotionDatabaseOperations(notion_client)

    # Create test page
    result = await db_ops.create_database_page(
        database_id,
        properties={
            "Name": {
                "title": [
                    {"text": {"content": "Test Page - Auto Created"}}
                ]
            },
            "Status": {
                "select": {"name": "Active"}
            }
        }
    )

    if result["success"]:
        print(f"✅ PASS: Page created")
        print(f"   Page ID: {result['page_id']}")
        print(f"   URL: {result.get('url', 'N/A')}")
        return result["page_id"]  # Return for update test
    else:
        print(f"❌ FAIL: {result['error']}")
        return None


async def test_update_page(page_id: str):
    """Test updating a Notion page."""
    print("\n=== Test 3: Update Page ===")

    if not page_id:
        print("⚠️  SKIP: No page to update")
        return True

    db_ops = NotionDatabaseOperations(notion_client)

    # Update page status
    result = await db_ops.update_database_page(
        page_id,
        properties={
            "Status": {
                "select": {"name": "Complete"}
            }
        }
    )

    if result["success"]:
        print(f"✅ PASS: Page updated")
        print(f"   Last edited: {result.get('last_edited_time', 'N/A')}")
    else:
        print(f"❌ FAIL: {result['error']}")
        return False

    return True


async def test_get_schema():
    """Test retrieving database schema."""
    print("\n=== Test 4: Get Schema ===")

    database_id = os.getenv("NOTION_TEST_DATABASE_ID")

    if not database_id:
        print("⚠️  SKIP: No test database configured")
        return True

    db_ops = NotionDatabaseOperations(notion_client)

    result = await db_ops.get_database_schema(database_id)

    if result["success"]:
        print(f"✅ PASS: Schema retrieved")
        print(f"   Properties: {len(result['properties'])}")
        print(f"   Property types: {list(result['properties'].keys())[:5]}")
    else:
        print(f"❌ FAIL: {result['error']}")
        return False

    return True


async def main():
    """Run all database operation tests."""
    print("=" * 70)
    print("NOTION DATABASE OPERATIONS TESTS")
    print("=" * 70)

    # Initialize client (implementation depends on your setup)
    global notion_client
    # notion_client = NotionClient(api_key=os.getenv("NOTION_API_KEY"))

    tests = [
        ("Database Query", test_database_query),
        ("Get Schema", test_get_schema),
    ]

    # Create page and use for update test
    page_id = await test_create_page()
    if page_id:
        tests.append(("Update Page", lambda: test_update_page(page_id)))

    results = []
    for name, test_func in tests:
        try:
            result = await test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Test '{name}' crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    passed = sum(1 for _, r in results if r)
    total = len(results)
    print(f"\nPassed: {passed}/{total} ({100*passed//total if total else 0}%)")

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL/SKIP"
        print(f"{status}: {name}")


if __name__ == "__main__":
    asyncio.run(main())
```

### Step 2.2: MCP Integration Verification (10 minutes)

**Verify database tools in MCP adapter**:

```python
# Check if NotionMCPAdapter includes database tools
# If not, add them based on database operations

async def verify_mcp_database_tools():
    """Verify MCP adapter includes database tools."""
    print("\n=== MCP Database Tools Verification ===")

    # Import MCP adapter
    from services.integrations.notion.mcp_adapter import NotionMCPAdapter

    adapter = NotionMCPAdapter()
    tools = adapter.get_tools()

    expected_tools = [
        "query_database",
        "create_database_page",
        "update_database_page",
        "get_database_schema"
    ]

    tool_names = [t.name for t in tools]

    for expected in expected_tools:
        if expected in tool_names:
            print(f"✅ {expected}: Present")
        else:
            print(f"❌ {expected}: MISSING")

    print(f"\nTotal tools: {len(tools)}")
```

---

## Phase 3: Documentation & Cleanup (30 minutes)

### Step 3.1: API Documentation (15 minutes)

**File**: `docs/integrations/notion-database-api.md`

```markdown
# Notion Database API

## Overview

The Notion Database API provides CRUD operations for Notion databases, enabling:
- Query databases with filters and sorting
- Create new database pages
- Update existing pages
- Retrieve database schemas

**Status**: ✅ Phase 2 Complete (Issue #165)

## Configuration

```bash
# Required environment variable
NOTION_API_KEY=secret_xxxxx

# Optional: Notion API version
NOTION_VERSION=2022-06-28
```

## Supported Operations

### 1. Query Database

```python
results = await notion.query_database(
    database_id="abc123",
    filter_params={
        "property": "Status",
        "select": {"equals": "Active"}
    },
    sorts=[
        {"property": "Created", "direction": "descending"}
    ],
    page_size=50
)

# Returns:
# {
#     "success": True,
#     "results": [...],
#     "count": 50,
#     "has_more": True,
#     "next_cursor": "cursor_string"
# }
```

### 2. Create Database Page

```python
page = await notion.create_database_page(
    database_id="abc123",
    properties={
        "Name": {
            "title": [{"text": {"content": "New Task"}}]
        },
        "Status": {
            "select": {"name": "Active"}
        },
        "Priority": {
            "number": 1
        }
    }
)

# Returns:
# {
#     "success": True,
#     "page_id": "page_123",
#     "url": "https://notion.so/...",
#     "created_time": "2025-10-18T17:00:00Z"
# }
```

### 3. Update Database Page

```python
updated = await notion.update_database_page(
    page_id="page_123",
    properties={
        "Status": {
            "select": {"name": "Complete"}
        }
    }
)

# Returns:
# {
#     "success": True,
#     "page_id": "page_123",
#     "last_edited_time": "2025-10-18T17:30:00Z"
# }
```

### 4. Get Database Schema

```python
schema = await notion.get_database_schema("abc123")

# Returns:
# {
#     "success": True,
#     "title": [...],
#     "properties": {
#         "Name": {"type": "title"},
#         "Status": {"type": "select"},
#         "Priority": {"type": "number"}
#     }
# }
```

## Error Handling

All operations return a dictionary with `success` field:
- `success: True` - Operation completed
- `success: False` - Operation failed, check `error` field

```python
result = await notion.query_database(invalid_id)

if not result["success"]:
    print(f"Error: {result['error']}")
```

## Rate Limiting

Notion API has rate limits:
- 3 requests per second per integration
- Automatic retry with exponential backoff

## Testing

```bash
# Set test database
export NOTION_TEST_DATABASE_ID=your_test_db_id

# Run tests
python dev/2025/10/18/test-notion-database-ops.py
```

## Future Enhancements (Phase 3)

- Batch operations
- Advanced filtering
- Pagination helpers
- Webhooks integration
- Real-time sync

---

*Last Updated: October 18, 2025*
*Issue: #165 CORE-NOTN-UP*
*Status: Phase 2 Complete*
```

### Step 3.2: Completion Report (15 minutes)

**File**: `dev/2025/10/18/notion-phase-2-completion.md`

```markdown
# Notion Database API - Phase 2 Complete ✅

**Issue**: #165 - CORE-NOTN-UP
**Date**: October 18, 2025
**Duration**: [actual time]
**Status**: ✅ COMPLETE

## What Was Completed

### Database Operations Implemented

1. **query_database()** - Query with filters and sorting
2. **create_database_page()** - Create new pages
3. **update_database_page()** - Update existing pages
4. **get_database_schema()** - Retrieve database schema

### Integration

- ✅ MCP adapter includes database tools
- ✅ Integration tests created
- ✅ Documentation complete

## Test Results

**Database Operations**: [X/4 tests passing]
- Query database: [PASS/FAIL]
- Create page: [PASS/FAIL]
- Update page: [PASS/FAIL]
- Get schema: [PASS/FAIL]

**MCP Integration**: [PASS/FAIL]
- Database tools present in MCP adapter

## Files Created/Modified

**Created**:
1. dev/2025/10/18/notion-phase-0-assessment.md
2. dev/2025/10/18/test-notion-database-ops.py
3. docs/integrations/notion-database-api.md
4. dev/2025/10/18/notion-phase-2-completion.md

**Modified**:
1. services/integrations/notion/notion_service.py (database operations)
2. services/integrations/notion/mcp_adapter.py (if needed for database tools)

## Success Criteria

- [x] All database CRUD operations functional
- [x] Integration tests created (passing or documented as skipped)
- [x] MCP adapter includes database tools
- [x] Documentation updated
- [x] No regressions from Phase 1

## Next Steps

**Immediate**:
- Close Issue #165
- Mark Sprint A3 100% complete
- Celebrate! 🎉

**Future (Phase 3 - if needed)**:
- Batch operations
- Advanced filtering
- Pagination helpers
- Webhooks
- Real-time sync

---

*Completed: October 18, 2025*
*Sprint: A3 "Some Assembly Required"*
*Pattern: Straightforward plumbing work*
