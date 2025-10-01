# Claude Code Prompt: Phase 2 - Notion Integration Router Implementation

## Mission: Implement NotionIntegrationRouter

**Context**: Phase 1 validated the Calendar router pattern works perfectly. Notion adapter has 22+ methods (vs Calendar's 7), making this router larger but following the same proven pattern.

**Objective**: Create NotionIntegrationRouter following the established pattern, enabling feature flag control for Notion MCP adapter.

## Phase 0 Key Findings Reference

From your investigation:
- **Adapter**: `services/integrations/mcp/notion_adapter.py` (20,631 bytes)
- **Base Class**: `BaseSpatialAdapter`
- **Auth**: API token authentication (NotionConfig)
- **Methods**: 22+ methods (connect, get_workspace_info, fetch_databases, query_database, get_page, create_page, etc.)
- **Pattern**: MCP Integration (similar to Calendar's MCP Consumer)

## Implementation Tasks

### Task 1: Create Router File Structure

```bash
# Create integration directory if needed
mkdir -p services/integrations/notion

# Create router file
touch services/integrations/notion/notion_integration_router.py

# Verify directory structure
ls -la services/integrations/notion/
```

### Task 2: Implement Router Class

Following CalendarIntegrationRouter pattern exactly:

```python
# services/integrations/notion/notion_integration_router.py
"""
NotionIntegrationRouter - Feature flag controlled access to Notion integrations

Provides unified interface for Notion operations with support for:
- Spatial intelligence (MCP-based NotionAdapter)
- Legacy basic Notion operations (if future implementation exists)
- Feature flag control via USE_SPATIAL_NOTION
"""

import os
import warnings
from typing import Optional, List, Dict, Any, Tuple

class NotionIntegrationRouter:
    """
    Router for Notion integration with spatial/legacy delegation.

    Follows pattern established in CalendarIntegrationRouter.
    Delegates to NotionMCPAdapter (spatial) or future legacy implementation.
    """

    def __init__(self):
        """Initialize router with feature flag checking"""
        # Check feature flags (following Calendar router pattern)
        self.use_spatial = os.getenv('USE_SPATIAL_NOTION', 'true').lower() == 'true'
        self.allow_legacy = os.getenv('ALLOW_LEGACY_NOTION', 'false').lower() == 'false'

        # Initialize spatial integration
        self.spatial_notion = None
        if self.use_spatial:
            try:
                from services.integrations.mcp.notion_adapter import NotionMCPAdapter
                self.spatial_notion = NotionMCPAdapter()
            except ImportError as e:
                warnings.warn(f"Spatial Notion unavailable: {e}")

        # Initialize legacy integration (placeholder for future)
        self.legacy_notion = None
        if self.allow_legacy:
            # Future: Import legacy Notion client if exists
            # For now, no legacy implementation exists
            pass

    def _get_preferred_integration(self, operation: str) -> Tuple[Optional[Any], bool]:
        """
        Get preferred integration based on feature flags.

        Args:
            operation: Name of operation being performed

        Returns:
            Tuple of (integration_instance, is_legacy_bool)
        """
        # Try spatial first if enabled
        if self.use_spatial and self.spatial_notion:
            return self.spatial_notion, False

        # Fall back to legacy if allowed (future)
        elif self.allow_legacy and self.legacy_notion:
            return self.legacy_notion, True

        # No integration available
        else:
            return None, False

    def _warn_deprecation_if_needed(self, operation: str, is_legacy: bool):
        """Warn about legacy usage for future migration"""
        if is_legacy:
            warnings.warn(
                f"Using legacy Notion for {operation}. "
                "Consider enabling USE_SPATIAL_NOTION=true for spatial intelligence.",
                DeprecationWarning,
                stacklevel=3
            )

    # Delegate all 22+ NotionMCPAdapter methods
    # Group by functionality for clarity

    # Connection methods
    async def connect(self) -> bool:
        """Connect to Notion API"""
        integration, is_legacy = self._get_preferred_integration("connect")
        if integration:
            self._warn_deprecation_if_needed("connect", is_legacy)
            return await integration.connect()
        else:
            raise RuntimeError("No Notion integration available")

    async def test_connection(self) -> bool:
        """Test Notion API connection"""
        integration, is_legacy = self._get_preferred_integration("test_connection")
        if integration:
            self._warn_deprecation_if_needed("test_connection", is_legacy)
            return await integration.test_connection()
        else:
            raise RuntimeError("No Notion integration available")

    def is_configured(self) -> bool:
        """Check if Notion is configured"""
        integration, is_legacy = self._get_preferred_integration("is_configured")
        if integration:
            self._warn_deprecation_if_needed("is_configured", is_legacy)
            return integration.is_configured()
        else:
            raise RuntimeError("No Notion integration available")

    # Workspace methods
    async def get_workspace_info(self) -> Dict[str, Any]:
        """Get Notion workspace information"""
        integration, is_legacy = self._get_preferred_integration("get_workspace_info")
        if integration:
            self._warn_deprecation_if_needed("get_workspace_info", is_legacy)
            return await integration.get_workspace_info()
        else:
            raise RuntimeError("No Notion integration available")

    async def list_users(self) -> List[Dict[str, Any]]:
        """List users in Notion workspace"""
        integration, is_legacy = self._get_preferred_integration("list_users")
        if integration:
            self._warn_deprecation_if_needed("list_users", is_legacy)
            return await integration.list_users()
        else:
            raise RuntimeError("No Notion integration available")

    async def get_user(self, user_id: str) -> Dict[str, Any]:
        """Get specific user information"""
        integration, is_legacy = self._get_preferred_integration("get_user")
        if integration:
            self._warn_deprecation_if_needed("get_user", is_legacy)
            return await integration.get_user(user_id)
        else:
            raise RuntimeError("No Notion integration available")

    # Database methods
    async def fetch_databases(self) -> List[Dict[str, Any]]:
        """Fetch all accessible databases"""
        integration, is_legacy = self._get_preferred_integration("fetch_databases")
        if integration:
            self._warn_deprecation_if_needed("fetch_databases", is_legacy)
            return await integration.fetch_databases()
        else:
            raise RuntimeError("No Notion integration available")

    async def list_databases(self) -> List[Dict[str, Any]]:
        """List databases (alias for fetch_databases)"""
        integration, is_legacy = self._get_preferred_integration("list_databases")
        if integration:
            self._warn_deprecation_if_needed("list_databases", is_legacy)
            return await integration.list_databases()
        else:
            raise RuntimeError("No Notion integration available")

    async def get_database(self, database_id: str) -> Dict[str, Any]:
        """Get specific database"""
        integration, is_legacy = self._get_preferred_integration("get_database")
        if integration:
            self._warn_deprecation_if_needed("get_database", is_legacy)
            return await integration.get_database(database_id)
        else:
            raise RuntimeError("No Notion integration available")

    async def query_database(self, database_id: str,
                            filter_obj: Optional[Dict] = None,
                            sorts: Optional[List[Dict]] = None) -> List[Dict[str, Any]]:
        """Query database with filters and sorting"""
        integration, is_legacy = self._get_preferred_integration("query_database")
        if integration:
            self._warn_deprecation_if_needed("query_database", is_legacy)
            return await integration.query_database(database_id, filter_obj, sorts)
        else:
            raise RuntimeError("No Notion integration available")

    # Page methods
    async def get_page(self, page_id: str) -> Dict[str, Any]:
        """Get specific page"""
        integration, is_legacy = self._get_preferred_integration("get_page")
        if integration:
            self._warn_deprecation_if_needed("get_page", is_legacy)
            return await integration.get_page(page_id)
        else:
            raise RuntimeError("No Notion integration available")

    async def get_page_blocks(self, page_id: str) -> List[Dict[str, Any]]:
        """Get blocks from a page"""
        integration, is_legacy = self._get_preferred_integration("get_page_blocks")
        if integration:
            self._warn_deprecation_if_needed("get_page_blocks", is_legacy)
            return await integration.get_page_blocks(page_id)
        else:
            raise RuntimeError("No Notion integration available")

    async def update_page(self, page_id: str, properties: Dict[str, Any]) -> Dict[str, Any]:
        """Update page properties"""
        integration, is_legacy = self._get_preferred_integration("update_page")
        if integration:
            self._warn_deprecation_if_needed("update_page", is_legacy)
            return await integration.update_page(page_id, properties)
        else:
            raise RuntimeError("No Notion integration available")

    async def create_page(self, parent: Dict[str, Any],
                         properties: Dict[str, Any],
                         children: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """Create new page"""
        integration, is_legacy = self._get_preferred_integration("create_page")
        if integration:
            self._warn_deprecation_if_needed("create_page", is_legacy)
            return await integration.create_page(parent, properties, children)
        else:
            raise RuntimeError("No Notion integration available")

    # Item methods
    async def create_database_item(self, database_id: str,
                                   properties: Dict[str, Any]) -> Dict[str, Any]:
        """Create item in database"""
        integration, is_legacy = self._get_preferred_integration("create_database_item")
        if integration:
            self._warn_deprecation_if_needed("create_database_item", is_legacy)
            return await integration.create_database_item(database_id, properties)
        else:
            raise RuntimeError("No Notion integration available")

    # Search methods
    async def search_notion(self, query: str,
                           filter_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search Notion workspace"""
        integration, is_legacy = self._get_preferred_integration("search_notion")
        if integration:
            self._warn_deprecation_if_needed("search_notion", is_legacy)
            return await integration.search_notion(query, filter_type)
        else:
            raise RuntimeError("No Notion integration available")

    # Utility methods
    def get_mapping_stats(self) -> Dict[str, Any]:
        """Get spatial mapping statistics"""
        integration, is_legacy = self._get_preferred_integration("get_mapping_stats")
        if integration:
            self._warn_deprecation_if_needed("get_mapping_stats", is_legacy)
            return integration.get_mapping_stats()
        else:
            raise RuntimeError("No Notion integration available")

    async def close(self):
        """Close Notion connection"""
        integration, is_legacy = self._get_preferred_integration("close")
        if integration:
            self._warn_deprecation_if_needed("close", is_legacy)
            await integration.close()
        # No error if no integration - closing is optional
```

### Task 3: Add Feature Flag Methods

Update FeatureFlags service:

```python
# In services/infrastructure/config/feature_flags.py
# Add after should_use_spatial_calendar()

@staticmethod
def should_use_spatial_notion() -> bool:
    """Check if spatial Notion integration should be used"""
    return FeatureFlags._get_boolean_flag("USE_SPATIAL_NOTION", True)

@staticmethod
def is_legacy_notion_allowed() -> bool:
    """Check if legacy Notion integration is allowed"""
    return FeatureFlags._get_boolean_flag("ALLOW_LEGACY_NOTION", False)
```

### Task 4: Verify Router Implementation

Test the router before proceeding:

```python
# Test router initialization
python -c "
import asyncio
from services.integrations.notion.notion_integration_router import NotionIntegrationRouter

async def test_router():
    router = NotionIntegrationRouter()
    print(f'✅ Router initialized')
    print(f'   Use spatial: {router.use_spatial}')
    print(f'   Spatial notion: {router.spatial_notion is not None}')

    # Test method availability
    methods = ['connect', 'test_connection', 'is_configured', 'get_workspace_info',
               'list_users', 'get_user', 'fetch_databases', 'list_databases',
               'get_database', 'query_database', 'get_page', 'get_page_blocks',
               'update_page', 'create_page', 'create_database_item',
               'search_notion', 'get_mapping_stats', 'close']

    print(f'\n   Methods available: {len(methods)}')
    for method in methods:
        has_method = hasattr(router, method) and callable(getattr(router, method))
        if not has_method:
            print(f'   ❌ Missing: {method}')

asyncio.run(test_router())
"
```

### Task 5: Test Feature Flag Control

```bash
# Test spatial mode
USE_SPATIAL_NOTION=true python -c "
import asyncio
from services.integrations.notion.notion_integration_router import NotionIntegrationRouter

async def test():
    router = NotionIntegrationRouter()
    integration, is_legacy = router._get_preferred_integration('test')
    print(f'Spatial mode - Integration: {type(integration).__name__ if integration else None}')

asyncio.run(test())
"

# Test with spatial disabled
USE_SPATIAL_NOTION=false python -c "
import asyncio
from services.integrations.notion.notion_integration_router import NotionIntegrationRouter

async def test():
    router = NotionIntegrationRouter()
    integration, is_legacy = router._get_preferred_integration('test')
    print(f'Disabled mode - Integration: {type(integration).__name__ if integration else None}')

asyncio.run(test())
"
```

### Task 6: Test API Token Preservation

Verify NotionConfig authentication works through router:

```python
# Test configuration checking
python -c "
import asyncio
from services.integrations.notion.notion_integration_router import NotionIntegrationRouter

async def test_config():
    router = NotionIntegrationRouter()

    # Test is_configured (synchronous method)
    try:
        configured = router.is_configured()
        print(f'✅ is_configured works: {configured}')
    except Exception as e:
        print(f'❌ is_configured failed: {e}')

asyncio.run(test_config())
"
```

## Evidence Requirements

Document in Phase 2 completion report:

```markdown
# Phase 2: Notion Router Implementation Report

## Router File Created
**Location**: services/integrations/notion/notion_integration_router.py
**Size**: [line count]
**Pattern**: Follows CalendarIntegrationRouter pattern

## Implementation Completeness

### Methods Implemented: X/18 minimum
Connection: connect, test_connection, is_configured
Workspace: get_workspace_info, list_users, get_user
Database: fetch_databases, list_databases, get_database, query_database
Page: get_page, get_page_blocks, update_page, create_page
Item: create_database_item
Search: search_notion
Utility: get_mapping_stats, close

[Mark each completed]

## Testing Results

### Router Initialization
[Output showing spatial notion loaded]

### Method Availability
[Output showing all methods callable]

### Feature Flag Control
[Output from spatial/disabled tests]

### Configuration Preservation
[Output showing is_configured works]

## Pattern Compliance with Calendar Router
- Same __init__ structure
- Same _get_preferred_integration logic
- Same _warn_deprecation_if_needed
- Same RuntimeError pattern

## Services Ready for Migration
[List from Phase 0: domain_notion_service, publisher, notion_spatial]

## Ready for Phase 3: [YES/NO]
```

## Update Requirements

1. **Update Session Log**: Add Phase 2 completion with evidence
2. **Update GitHub Issue #199**: Add comment with Notion router completion
3. **Tag Cursor**: Request verification before Phase 3

## Critical Success Factors

- **Pattern Consistency**: Follow Calendar router pattern exactly
- **All Methods Delegated**: NotionMCPAdapter has 22+ methods - implement all
- **API Token Preservation**: NotionConfig must work through router
- **Async Patterns**: Most methods are async - preserve signatures
- **Mixed Sync/Async**: Some methods (is_configured, get_mapping_stats) are synchronous

## STOP Conditions

- If NotionConfig doesn't work through router
- If method signatures mismatch adapter
- If feature flags don't control behavior

---

**Your Mission**: Implement NotionIntegrationRouter following proven Calendar pattern. Larger method count but same delegation approach.

**Quality Standard**: Complete pattern compliance and all methods working before Phase 3.
