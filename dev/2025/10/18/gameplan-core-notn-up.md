# Gameplan: CORE-NOTN-UP - Notion Database API Upgrade

**Sprint**: A3 (completion)
**Issue**: #165 - Notion Database API Upgrade Phase 2
**Duration**: 1-2 hours estimated
**Context**: Postponed from Sprint A2, straightforward plumbing work

---

## Background

This is the remaining work from Sprint A2's Notion integration. Phase 1 was completed in A2, establishing basic connectivity. Phase 2 completes the database API functionality.

Unlike today's architectural work (MCP, Ethics, Knowledge Graph), this is pure implementation - the patterns are established, just need completion.

---

## Phase 0: Assessment (15 minutes)

**Discover what remains from A2**:
```python
# Check current Notion integration state
mcp__serena__find_symbol(
    name_regex="NotionMCP.*|notion.*database",
    scope="services/integrations/notion"
)

# Find TODO markers
mcp__serena__search_project(
    query="TODO database OR TODO notion",
    file_pattern="**/notion/*.py"
)

# Review what Phase 1 completed
mcp__serena__search_project(
    query="Phase 1 complete",
    file_pattern="**/notion/*.md"
)
```

**Expected findings**:
- Basic Notion API connectivity working (Phase 1)
- Database operations partially implemented
- MCP adapter exists (from #198)
- Just needs database CRUD operations

---

## Phase 1: Database Operations (45 minutes)

### Complete Database CRUD

**1.1 Database Query Operations**
```python
async def query_database(self, database_id: str, filter_params: dict):
    """Query Notion database with filters"""
    # Implementation for filtered queries
    # Pagination support
    # Result formatting
```

**1.2 Database Create/Update**
```python
async def create_database_page(self, database_id: str, properties: dict):
    """Create new page in database"""
    # Property mapping
    # Validation
    # Error handling

async def update_database_page(self, page_id: str, properties: dict):
    """Update existing database page"""
    # Partial updates
    # Property validation
    # Conflict resolution
```

**1.3 Database Schema Operations**
```python
async def get_database_schema(self, database_id: str):
    """Retrieve database properties schema"""
    # Schema extraction
    # Type mapping
    # Documentation generation
```

---

## Phase 2: Integration Testing (30 minutes)

### Test Database Operations

```python
async def test_notion_database_operations():
    """Test all database CRUD operations"""

    # Test query
    results = await notion.query_database(
        database_id="test_db",
        filter_params={"status": "active"}
    )
    assert results.success

    # Test create
    new_page = await notion.create_database_page(
        database_id="test_db",
        properties={"title": "Test Page"}
    )
    assert new_page.id

    # Test update
    updated = await notion.update_database_page(
        page_id=new_page.id,
        properties={"status": "complete"}
    )
    assert updated.success

    # Test schema
    schema = await notion.get_database_schema("test_db")
    assert "properties" in schema
```

### MCP Integration Verification

Verify database operations work through MCP layer (from #198):
```python
async def test_notion_mcp_database():
    """Verify MCP adapter includes database operations"""

    mcp_adapter = NotionMCPAdapter()
    tools = mcp_adapter.get_tools()

    # Verify database tools present
    assert "query_database" in [t.name for t in tools]
    assert "create_page" in [t.name for t in tools]
    assert "update_page" in [t.name for t in tools]
```

---

## Phase 3: Documentation & Cleanup (30 minutes)

### Update Documentation

**3.1 API Documentation**
```markdown
# Notion Database API

## Supported Operations
- Query database with filters
- Create database pages
- Update database pages
- Retrieve database schema

## Configuration
NOTION_API_KEY=your_key
NOTION_VERSION=2022-06-28

## Usage Examples
...
```

**3.2 Close Phase 2**
- Mark Phase 2 complete in tracking
- Update integration tests
- Document any limitations
- Note future enhancements (Phase 3 if needed)

---

## Success Criteria

Issue #165 complete when:
- [ ] All database CRUD operations functional
- [ ] Integration tests passing
- [ ] MCP adapter includes database tools
- [ ] Documentation updated
- [ ] No regressions from Phase 1

---

## Risk Assessment

### Low Risk (This is plumbing)
- Patterns established in Phase 1
- Notion API well-documented
- MCP integration already working
- Straightforward CRUD operations

### Potential Issues
- Rate limiting (mitigate with retry logic)
- API version changes (use stable version)
- Property type mapping (document edge cases)

---

## Time Estimate

**Total**: 1.5-2 hours

- Phase 0: Assessment (15 min)
- Phase 1: Implementation (45 min)
- Phase 2: Testing (30 min)
- Phase 3: Documentation (30 min)

Given today's velocity (37-70% faster), likely 1 hour actual.

---

## Notes

This is refreshingly straightforward after today's architectural decisions:
- No DDD violations to fix
- No service layer refactoring
- No universal coverage concerns
- Just implement, test, document

The "plumbing" characterization is perfect - we're just connecting pipes that already exist.

---

## Next Steps

1. Run Phase 0 assessment
2. Implement database operations
3. Test through MCP layer
4. Update documentation
5. Close Issue #165
6. **Sprint A3 100% COMPLETE!**

---

*Ready to finish Sprint A3 with solid plumbing work*
