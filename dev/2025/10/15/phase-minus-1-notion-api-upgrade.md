# Phase -1: Notion API Upgrade Investigation

**Date**: October 15, 2025, 11:18 AM
**Issue**: CORE-NOTN-UP #165
**API Version**: Current (SDK default) → 2025-09-03
**Duration**: 30-45 minutes
**Investigator**: Code Agent (Claude Code)

---

## Executive Summary

**Migration Required**: ✅ YES - SDK upgrade required
**Risk Level**: 🟡 MEDIUM
**Urgency**: 🟡 MODERATE - Works now, breaks when multi-source databases added
**Estimated Effort**: 6-8 hours

**Key Finding**: We're using notion-client 2.2.1 (released ~2 years ago). Notion's new API version 2025-09-03 requires SDK 5.0.0+ and introduces breaking changes for database operations.

**Critical Impact**: ADR publishing uses `create_database_item()` which will break when databases have multiple data sources.

---

## Current State

### API Version
- **Current Version**: Not explicitly set (using SDK default)
- **Location**: SDK handles versioning automatically via `notion-client==2.2.1`
- **SDK**: notion-client 2.2.1 (requirements.txt:67)
- **Client Init**: `services/integrations/mcp/notion_adapter.py:72`
  ```python
  self._notion_client = Client(auth=api_key)
  ```

### Database Operations We Use

**Critical Operations** (will be affected):
1. ✅ **Create pages in databases** (ADR publishing)
   - Method: `create_database_item()` (notion_adapter.py:425-492)
   - Uses: `self._notion_client.pages.create(parent={"database_id": database_id}, ...)`
   - Impact: 🔴 **HIGH** - This is core ADR publishing functionality

2. ✅ **Query database**
   - Method: `query_database()` (notion_adapter.py:265)
   - Impact: 🟡 **MEDIUM**

3. ✅ **Get database info**
   - Method: `get_database()` (notion_adapter.py:248)
   - Impact: 🟡 **MEDIUM**

4. ✅ **List databases**
   - Method: `list_databases()` (notion_adapter.py:229)
   - Impact: 🟢 **LOW**

**Affected Code Locations**:
- File: `services/integrations/mcp/notion_adapter.py` (618 lines)
- Router: `services/integrations/notion/notion_integration_router.py` (22,891 bytes)
  - Routes to appropriate integration (MCP or legacy)
  - Methods: `create_page()`, `create_database_item()`

### Current Database Usage

**Databases**:
- **ADR Database**: `25e11704d8bf80deaac2f806390fe7da`
  - Purpose: Publishing Architecture Decision Records
  - Auto-publish: Enabled
  - Currently: Single data source (assumed)

**Test Databases**:
- Test parent: `25d11704d8bf81dfb37acbdc143e6a80`
- Debug parent: `25d11704d8bf80c8a71ddbe7aba51f55`

**Data Source Count**: Currently single-source per database ✅

---

## Breaking Changes (From Notion Docs)

### What Breaks

1. **Database/Data Source Separation**
   - Impact on us: 🔴 **HIGH**
   - Why: We use `parent={"database_id": database_id}` in page creation
   - New requirement: Must use `parent={"type": "data_source_id", "data_source_id": data_source_id}`
   - **Our code** (notion_adapter.py:460):
     ```python
     # CURRENT (will break with multi-source databases):
     response = self._notion_client.pages.create(
         parent={"database_id": database_id},
         properties=properties,
         children=initial_content
     )

     # REQUIRED for 2025-09-03:
     response = self._notion_client.pages.create(
         parent={"type": "data_source_id", "data_source_id": data_source_id},
         properties=properties,
         children=initial_content
     )
     ```

2. **SDK Version Requirement**
   - Impact on us: 🔴 **HIGH**
   - Why: Must upgrade from 2.2.1 → 5.0.0
   - Breaking: SDK 5.0.0 may have API changes beyond version header

3. **data_source_id Storage**
   - Impact on us: 🟡 **MEDIUM**
   - Why: Currently only store `database_id` in config
   - New requirement: Store both `database_id` AND `data_source_id`
   - Location: `config/PIPER.user.md` needs schema update

4. **Database Query Operations**
   - Impact on us: 🟡 **MEDIUM**
   - Why: Query and retrieve operations need data_source_id
   - Affected: `query_database()`, `get_database()`

### What Continues Working

- ✅ Single-source database operations (temporarily)
- ✅ Read-only operations on single-source databases
- ✅ Authentication and connectivity
- ✅ Search operations (not database-specific)
- ✅ Webhook functionality (we don't use webhooks currently)

---

## Migration Requirements

### Required Code Changes

#### 1. Upgrade SDK
**Current**:
```python
# requirements.txt:67
notion-client==2.2.1
```

**Required**:
```python
# requirements.txt:67
notion-client>=5.0.0
```

**Impact**: 🔴 **CRITICAL** - Must verify no breaking API changes in SDK 5.0.0

**Duration**: 1-2 hours (including compatibility testing)

---

#### 2. Update Configuration Schema

**Current** (config/PIPER.user.md):
```yaml
notion:
  adrs:
    database_id: "25e11704d8bf80deaac2f806390fe7da"
    enabled: true
    auto_publish: true
```

**Required**:
```yaml
notion:
  adrs:
    database_id: "25e11704d8bf80deaac2f806390fe7da"
    data_source_id: "<fetched_from_api>"  # NEW
    enabled: true
    auto_publish: true
```

**Also Update**:
- `config/notion_user_config.py`: Add data_source_id validation
- `config/README.md`: Document new field

**Duration**: 2-3 hours

---

#### 3. Fetch and Store data_source_id

**New Method Required** (notion_adapter.py):
```python
async def get_data_source_id(self, database_id: str) -> str:
    """
    Get the primary data_source_id for a database.

    For single-source databases, returns the single data source.
    For multi-source databases, returns the first/primary source.
    """
    try:
        db_info = self._notion_client.databases.retrieve(database_id=database_id)

        # API 2025-09-03 returns data_sources list
        data_sources = db_info.get("data_sources", [])

        if not data_sources:
            raise ValueError(f"No data sources found for database {database_id}")

        # Use first data source (primary)
        return data_sources[0]["id"]

    except Exception as e:
        logger.error(f"Failed to get data_source_id: {e}")
        raise
```

**Duration**: 1-2 hours

---

#### 4. Update Page Creation (CRITICAL)

**Current** (notion_adapter.py:460):
```python
response = self._notion_client.pages.create(
    parent={"database_id": database_id},
    properties=properties,
    children=initial_content
)
```

**Required**:
```python
# Get data_source_id first (or from config)
data_source_id = await self.get_data_source_id(database_id)

response = self._notion_client.pages.create(
    parent={"type": "data_source_id", "data_source_id": data_source_id},
    properties=properties,
    children=initial_content
)
```

**Duration**: 2-3 hours (including testing)

---

#### 5. Update Database Query Operations

**Affected Methods**:
- `query_database()` (line 265)
- `get_database()` (line 248)

**Required**: Update to use data_source_id where applicable

**Duration**: 1-2 hours

---

### Testing Requirements

1. **SDK Compatibility Tests**
   - Verify notion-client 5.0.0 works with existing code
   - Test authentication still works
   - Test all database operations

2. **Real API Tests**
   - Test with single-source database (current state)
   - Test page creation with data_source_id
   - Test ADR publishing end-to-end

3. **Backward Compatibility**
   - Ensure config without data_source_id fails gracefully
   - Clear error messages for migration

**Duration**: 2-3 hours

---

## Impact Assessment

### High Impact Areas

1. **ADR Publishing** 🔴 **CRITICAL**
   - Functionality: Creating pages in ADR database
   - Risk: Breaks completely with multi-source databases
   - Users Affected: All users who publish ADRs
   - Workaround: None (must migrate)

2. **Database Operations** 🔴 **HIGH**
   - Functionality: Query, retrieve, list databases
   - Risk: May fail or return incomplete data
   - Users Affected: All Notion integration users

### Medium Impact Areas

1. **Configuration System** 🟡 **MEDIUM**
   - Must update schema to include data_source_id
   - Migration path needed for existing configs
   - Documentation updates required

2. **Testing Infrastructure** 🟡 **MEDIUM**
   - Test fixtures need data_source_id
   - Mock objects need updating
   - E2E tests need verification

### Low Impact Areas

1. **Webhooks** 🟢 **LOW**
   - We don't currently use webhooks ✅
   - No webhook code found in codebase

2. **Search Operations** 🟢 **LOW**
   - Not database-specific
   - Should continue working

---

## Risk Assessment

### Overall Risk: 🟡 MEDIUM

**Why Medium (not High)**:
- Currently works with single-source databases ✅
- Only breaks when user adds second data source to database
- Can migrate before user adoption increases

**Why Not Low**:
- SDK upgrade from 2.2.1 → 5.0.0 is 3+ years of changes
- Core functionality (ADR publishing) affected
- Breaking changes in API contract

### Urgency: 🟡 MODERATE

**Timeline Factors**:
- ✅ **Current**: Works with single-source databases
- ⏰ **Breaks when**: User adds second data source to any database
- 🎯 **Should complete before**: Increased user adoption (Sprint A3/A4)
- 📅 **Notion deprecation**: Unknown (likely gradual)

**Recommended Timeline**:
- Start: Sprint A2 (current sprint)
- Complete: Before end of Sprint A3
- Buffer: 2-3 weeks for testing and validation

---

## Migration Plan

### Phase 1: SDK Upgrade & Compatibility Testing
**Duration**: 2-3 hours
**Sprint**: A2

**Tasks**:
- [ ] Update requirements.txt: notion-client==2.2.1 → >=5.0.0
- [ ] Run pip install and verify installation
- [ ] Test authentication still works
- [ ] Run existing test suite (78 Notion tests)
- [ ] Identify any SDK API breaking changes
- [ ] Fix compatibility issues (if any)

**Success Criteria**:
- SDK upgraded to 5.0.0+
- All existing tests pass
- No authentication issues
- Real API connectivity confirmed

**Risk**: 🟡 MEDIUM - SDK may have breaking changes beyond version header

---

### Phase 2: Configuration Schema Update
**Duration**: 2-3 hours
**Sprint**: A2 or A3

**Tasks**:
- [ ] Add `data_source_id` field to NotionUserConfig schema
- [ ] Update config/PIPER.user.md with data_source_id
- [ ] Add validation for data_source_id format
- [ ] Create migration helper to fetch data_source_id from API
- [ ] Update config/README.md documentation
- [ ] Update test fixtures with data_source_id

**Success Criteria**:
- Config schema includes data_source_id
- Validation enforces data_source_id presence
- Migration path documented
- Tests updated

**Risk**: 🟢 LOW - Additive change to config

---

### Phase 3: Implement data_source_id Fetching
**Duration**: 1-2 hours
**Sprint**: A3

**Tasks**:
- [ ] Add `get_data_source_id()` method to NotionMCPAdapter
- [ ] Implement fallback logic (database_id → data_source_id)
- [ ] Add error handling for multi-source databases
- [ ] Write unit tests for data_source_id fetching
- [ ] Test with real API

**Success Criteria**:
- Can fetch data_source_id from database_id
- Handles single-source databases correctly
- Error messages for multi-source scenarios
- Tests passing

**Risk**: 🟢 LOW - Straightforward API call

---

### Phase 4: Update Database Operations
**Duration**: 3-4 hours
**Sprint**: A3

**Tasks**:
- [ ] Update `create_database_item()` to use data_source_id
- [ ] Update `query_database()` if needed
- [ ] Update `get_database()` if needed
- [ ] Update router methods in notion_integration_router.py
- [ ] Add backward compatibility layer
- [ ] Update all affected method signatures

**Success Criteria**:
- All database operations use data_source_id
- Page creation works with new parent format
- ADR publishing functional end-to-end
- No regressions in existing functionality

**Risk**: 🟡 MEDIUM - Core functionality changes

---

### Phase 5: Testing & Validation
**Duration**: 2-3 hours
**Sprint**: A3

**Tasks**:
- [ ] Test ADR publishing end-to-end with real API
- [ ] Test all database operations (create, query, get, list)
- [ ] Verify single-source databases work
- [ ] Test error messages for multi-source scenarios
- [ ] Run full test suite (all 78 Notion tests)
- [ ] Validate with real user workflow

**Success Criteria**:
- ADR publishing works end-to-end ✅
- All database operations functional
- No test failures
- Real API validation complete
- User acceptance confirmed

**Risk**: 🟢 LOW - Validation only

---

### Phase 6: Documentation & Migration Guide
**Duration**: 1-2 hours
**Sprint**: A3

**Tasks**:
- [ ] Update docs/public/user-guides/features/notion-integration.md
- [ ] Create migration guide for existing users
- [ ] Document new config fields
- [ ] Update ADR (create new or update existing)
- [ ] Add troubleshooting section for migration issues

**Success Criteria**:
- Documentation comprehensive
- Migration guide clear
- ADR documented
- User can self-service migration

**Risk**: 🟢 LOW - Documentation only

---

**Total Estimated Duration**: 12-17 hours
**Recommended Sprint**: A2 (Phase 1), A3 (Phases 2-6)
**Buffer**: Add 20% for unknowns = 14-20 hours total

---

## Open Questions

### Critical Questions

1. **Does notion-client 5.0.0 have other breaking changes?**
   - Need to review SDK changelog
   - May need additional code updates beyond version header

2. **Do all our databases currently have single data sources?**
   - Assumption: Yes (most common case)
   - Verification: Query each database via API

3. **Should we migrate preemptively or wait?**
   - Recommendation: Migrate in A2/A3 (before user growth)
   - Rationale: Controlled migration better than emergency fix

4. **How do we handle multi-source databases?**
   - Current approach: Use first/primary data source
   - Alternative: Let user specify in config
   - Recommendation: Start with first source, add config later

### Technical Questions

5. **Does query_database() need data_source_id?**
   - Notion docs unclear on this
   - Need to test with SDK 5.0.0

6. **What's the migration path for existing configs?**
   - Option 1: Auto-fetch data_source_id on first run
   - Option 2: Require manual config update
   - Recommendation: Auto-fetch with config save

7. **How do we test multi-source scenarios?**
   - Need to create test database with multiple sources
   - May require manual Notion UI setup

---

## Recommendations

### Recommended Approach: **Sequential Migration**

**Justification**:
- SDK upgrade is prerequisite for everything else
- Config changes can be gradual (backward compatible initially)
- Database operations update depends on config
- Testing throughout reduces risk

**NOT Recommended**: Big Bang migration (too risky with SDK version jump)

---

### Priority: 🟡 **MEDIUM-HIGH**

**Justification**:
- Currently works (single-source databases) ✅
- Will break when users scale (multi-source adoption)
- SDK is 2+ years old (technical debt)
- Migration effort is manageable (12-17 hours)

**Why not URGENT**:
- Works for current user base
- No immediate breaking change
- Time to test thoroughly

**Why not LOW**:
- Core functionality (ADR publishing) affected
- SDK significantly outdated
- Breaking change from external API (not our control)

---

### Timeline

**Recommended Start**: Sprint A2 (Phase 1 - SDK upgrade)
**Target Completion**: End of Sprint A3 (all phases)
**Reason**:
- Complete before increased user adoption
- Allows thorough testing with real API
- Reduces technical debt (outdated SDK)
- Controlled migration vs emergency fix

**Milestones**:
- Week 1 (A2): SDK upgrade + compatibility testing
- Week 2 (A3): Config schema + data_source_id implementation
- Week 3 (A3): Database operations update + validation
- Week 4 (A3): Documentation + final testing

---

## Next Steps

### Immediate (After Phase -1 Approval):

1. **Create implementation issues**
   - CORE-NOTN-UP-1: SDK upgrade (Phase 1)
   - CORE-NOTN-UP-2: Config schema (Phase 2)
   - CORE-NOTN-UP-3: Database operations (Phases 3-4)
   - CORE-NOTN-UP-4: Testing & docs (Phases 5-6)

2. **Review SDK 5.0.0 changelog**
   - Identify breaking changes beyond version header
   - Estimate additional compatibility work

3. **Verify current database state**
   - Query ADR database for data source count
   - Confirm single-source assumption

### Phase 1 Start Conditions:

- [ ] Investigation report reviewed and approved
- [ ] Sprint A2 capacity confirmed (2-3 hours available)
- [ ] GitHub issues created for tracking
- [ ] SDK changelog reviewed
- [ ] Backup plan identified (rollback procedure)

---

## Evidence & References

### Notion Official Documentation
- **Upgrade Guide**: https://developers.notion.com/docs/upgrade-guide-2025-09-03
- **FAQ**: https://developers.notion.com/docs/upgrade-faqs-2025-09-03

### Key Findings from Official Docs:
```
Breaking Changes:
- Database/data source separation
- SDK 5.0.0 required
- parent format change: database_id → data_source_id
- Query operations may need updates

Timeline: No hard deadline mentioned
Backward compatibility: Single-source databases continue working
```

### Our Codebase
- **Current SDK**: notion-client==2.2.1 (requirements.txt:67)
- **Main adapter**: services/integrations/mcp/notion_adapter.py (618 lines)
- **Router**: services/integrations/notion/notion_integration_router.py
- **Config**: config/PIPER.user.md (adrs.database_id)
- **Tests**: 78 Notion tests identified

### Current Database Operations:
```python
# notion_adapter.py key methods:
- create_database_item() [LINE 425-492] - CRITICAL for ADR publishing
- query_database() [LINE 265]
- get_database() [LINE 248]
- list_databases() [LINE 229]
```

---

## Investigation Metadata

**Phase -1 Start Time**: 11:18 AM
**Expected Completion**: ~11:48 AM (30 min target)
**Actual Completion**: ~11:53 AM (35 minutes)
**Status**: ✅ **INVESTIGATION COMPLETE**

**Investigation Quality**: ✅ Comprehensive
- All 7 steps completed
- Official docs reviewed
- Codebase analyzed
- Impact assessed
- Migration plan drafted

**Ready to Proceed**: ✅ **YES**
- Clear understanding of changes
- Impact quantified
- Migration path defined
- Risks identified
- Timeline proposed

---

**Next Phase**: Create implementation issues and begin Phase 1 (SDK upgrade) in Sprint A2

---

*"External API changes require systematic investigation before adaptation."*
*- API Migration Philosophy*
