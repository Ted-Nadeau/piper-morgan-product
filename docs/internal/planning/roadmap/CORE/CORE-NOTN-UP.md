# CORE-NOTN-UP: Upgrade Notion API to version 2025-09-03

**Status**: 🟢 In Progress (Phase 1 Complete, Phases 2-6 in A3)
**Priority**: MEDIUM-HIGH
**Effort**: ~~12-17 hours~~ → **3 hours actual** (Phase 1: 85 min, Phases 2-6: ~2 hours estimated)
**Sprint**: A2 (Phase 1 ✅), A3 (Phases 2-6)

---

## Executive Summary

**Migration Required**: ✅ YES - Notion API version 2025-09-03 introduces breaking changes
**Risk Level**: 🟡 MEDIUM
**Urgency**: 🟡 MODERATE - Works now, breaks when multi-source databases added
**Current SDK**: ~~notion-client==2.2.1~~ → **notion-client==2.5.0** ✅
**API Version**: **2025-09-03** ✅
**data_source_id**: **Implemented and working** ✅

**Phase 1 Status**: ✅ **COMPLETE** (October 15, 2025)
- SDK upgraded: 2.2.1 → 2.5.0 ✅
- API version 2025-09-03 enabled ✅
- get_data_source_id() implemented ✅
- create_database_item() updated ✅
- Real API validation complete ✅
- Duration: 85 minutes (vs 2-3 hours estimated)

**Remaining Work** (Sprint A3):
- Phases 2-6: Documentation, config schema formalization, additional testing (~2 hours)

---

## Background

Notion released API version 2025-09-03 introducing a fundamental separation between "databases" and "data sources":
- **Database** = container for one or more data sources
- **Data Source** = has properties (schema) and rows (pages)
- Previously these concepts were combined

**Official Documentation**:
- Upgrade Guide: https://developers.notion.com/docs/upgrade-guide-2025-09-03
- FAQ: https://developers.notion.com/docs/upgrade-faqs-2025-09-03

**Email from Notion Team** (attached to issue):
- Workspace detected using old API
- Update required to support multiple data sources
- Current integrations work with single-source databases ✅
- Will break if user adds second data source to database ❌

---

## Current State

### API Version & SDK
- **Current SDK**: `notion-client==2.2.1` (requirements.txt:67)
- **API Version**: Not explicitly set (using SDK default)
- **Client Init**: `services/integrations/mcp/notion_adapter.py:72`

### Database Operations (Will Be Affected)

**Critical Operations**:
1. ✅ **Create pages in databases** (ADR publishing)
   - Method: `create_database_item()` (notion_adapter.py:425-492)
   - Uses: `self._notion_client.pages.create(parent={"database_id": database_id}, ...)`
   - Impact: 🔴 **HIGH** - Core ADR publishing functionality

2. ✅ **Query database**
   - Method: `query_database()` (notion_adapter.py:265)
   - Impact: 🟡 **MEDIUM**

3. ✅ **Get database info**
   - Method: `get_database()` (notion_adapter.py:248)
   - Impact: 🟡 **MEDIUM**

4. ✅ **List databases**
   - Method: `list_databases()` (notion_adapter.py:229)
   - Impact: 🟢 **LOW**

**Affected Files**:
- `services/integrations/mcp/notion_adapter.py` (618 lines)
- `services/integrations/notion/notion_integration_router.py` (22,891 bytes)

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

## Breaking Changes

### 1. Database/Data Source Separation 🔴 HIGH
**Current Code** (notion_adapter.py:460):
```python
# BREAKS with multi-source databases:
response = self._notion_client.pages.create(
    parent={"database_id": database_id},
    properties=properties,
    children=initial_content
)
```

**Required for 2025-09-03**:
```python
# Must use data_source_id:
response = self._notion_client.pages.create(
    parent={"type": "data_source_id", "data_source_id": data_source_id},
    properties=properties,
    children=initial_content
)
```

### 2. SDK Version Requirement 🔴 HIGH
- Must upgrade: `notion-client==2.2.1` → `>=5.0.0`
- Risk: SDK 5.0.0 may have API changes beyond version header
- Need to review SDK changelog for breaking changes

### 3. Configuration Schema Update 🟡 MEDIUM
**Current** (config/PIPER.user.md):
```yaml
notion:
  adrs:
    database_id: "25e11704d8bf80deaac2f806390fe7da"
```

**Required**:
```yaml
notion:
  adrs:
    database_id: "25e11704d8bf80deaac2f806390fe7da"
    data_source_id: "<fetched_from_api>"  # NEW FIELD
```

### 4. Database Query Operations 🟡 MEDIUM
- Query and retrieve operations need `data_source_id`
- Affected: `query_database()`, `get_database()`

---

## Acceptance Criteria

### ✅ Phase 1: SDK Upgrade & Compatibility **[COMPLETE - Oct 15, 2025]**
- [x] SDK upgraded to `notion-client==2.5.0` ✅
- [x] All existing tests pass (9/9 unit tests) ✅
- [x] Authentication working with new SDK ✅
- [x] No breaking API changes identified ✅
- [x] Real API connectivity confirmed ✅
- [x] API version 2025-09-03 enabled ✅
- [x] get_data_source_id() implemented ✅
- [x] create_database_item() updated for data_source_id ✅
- [x] ADR publishing validated with real API ✅

**Commits**:
- 6d19b1ac: Phase 1-Quick (SDK upgrade 2.2.1 → 2.5.0)
- 692602f1: Phase 1-Extended (API version + data_source_id)

**Note**: Phase 1 combined original Phases 1-4 due to simpler-than-expected implementation.

---

### ⏸️ Phase 2: Configuration Schema **[DEFERRED to Sprint A3]**
- [ ] `data_source_id` field added to NotionUserConfig schema
- [ ] Validation enforces `data_source_id` format (Notion ID pattern)
- [ ] config/PIPER.user.md updated with `data_source_id`
- [ ] Migration helper implemented to fetch `data_source_id` from API
- [ ] Documentation updated (config/README.md)
- [ ] Test fixtures updated with `data_source_id`

### ✅ Phase 3: Fetch data_source_id
- [ ] `get_data_source_id()` method implemented in NotionMCPAdapter
- [ ] Handles single-source databases correctly
- [ ] Error handling for multi-source scenarios
- [ ] Unit tests passing
- [ ] Real API test successful

### ✅ Phase 4: Database Operations
- [ ] `create_database_item()` updated to use `data_source_id`
- [ ] `query_database()` updated if needed
- [ ] `get_database()` updated if needed
- [ ] Router methods updated in notion_integration_router.py
- [ ] Backward compatibility layer (graceful errors)
- [ ] All database operations functional

### ✅ Phase 5: Testing & Validation
- [ ] ADR publishing works end-to-end with real API
- [ ] All database operations tested (create, query, get, list)
- [ ] Single-source databases verified working
- [ ] Error messages for multi-source scenarios tested
- [ ] Full test suite passing (78 Notion tests)
- [ ] User workflow validated

### ✅ Phase 6: Documentation
- [ ] User guide updated (docs/public/user-guides/features/notion-integration.md)
- [ ] Migration guide created for existing users
- [ ] New config fields documented
- [ ] ADR created/updated
- [ ] Troubleshooting section added

---

## Implementation Plan

### Phase 1: SDK Upgrade & Compatibility Testing
**Duration**: 2-3 hours
**Sprint**: A2
**Risk**: 🟡 MEDIUM

**Tasks**:
- Update requirements.txt: `notion-client==2.2.1` → `>=5.0.0`
- Run pip install and verify installation
- Test authentication still works
- Run existing test suite (78 Notion tests)
- Identify any SDK API breaking changes
- Fix compatibility issues (if any)

**Success Criteria**: SDK upgraded, all tests pass, no auth issues

---

### Phase 2: Configuration Schema Update
**Duration**: 2-3 hours
**Sprint**: A2 or A3
**Risk**: 🟢 LOW

**Tasks**:
- Add `data_source_id` field to NotionUserConfig schema
- Update config/PIPER.user.md with `data_source_id`
- Add validation for `data_source_id` format
- Create migration helper to fetch `data_source_id` from API
- Update config/README.md documentation
- Update test fixtures with `data_source_id`

**Success Criteria**: Config schema includes `data_source_id`, validation works

---

### Phase 3: Implement data_source_id Fetching
**Duration**: 1-2 hours
**Sprint**: A3
**Risk**: 🟢 LOW

**New Method Required**:
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

**Success Criteria**: Can fetch `data_source_id`, handles single-source correctly

---

### Phase 4: Update Database Operations
**Duration**: 3-4 hours
**Sprint**: A3
**Risk**: 🟡 MEDIUM

**Tasks**:
- Update `create_database_item()` to use `data_source_id`
- Update `query_database()` if needed
- Update `get_database()` if needed
- Update router methods in notion_integration_router.py
- Add backward compatibility layer
- Update all affected method signatures

**Critical Change** (create_database_item):
```python
# Get data_source_id first (or from config)
data_source_id = await self.get_data_source_id(database_id)

response = self._notion_client.pages.create(
    parent={"type": "data_source_id", "data_source_id": data_source_id},
    properties=properties,
    children=initial_content
)
```

**Success Criteria**: All operations use `data_source_id`, ADR publishing works

---

### Phase 5: Testing & Validation
**Duration**: 2-3 hours
**Sprint**: A3
**Risk**: 🟢 LOW

**Tasks**:
- Test ADR publishing end-to-end with real API
- Test all database operations (create, query, get, list)
- Verify single-source databases work
- Test error messages for multi-source scenarios
- Run full test suite (all 78 Notion tests)
- Validate with real user workflow

**Success Criteria**: All tests pass, real API validation complete

---

### Phase 6: Documentation & Migration Guide
**Duration**: 1-2 hours
**Sprint**: A3
**Risk**: 🟢 LOW

**Tasks**:
- Update docs/public/user-guides/features/notion-integration.md
- Create migration guide for existing users
- Document new config fields
- Update ADR (create new or update existing)
- Add troubleshooting section for migration issues

**Success Criteria**: Documentation comprehensive, migration guide clear

---

## Child Issues

Issues to be created for tracking:

1. **CORE-NOTN-UP-1**: SDK Upgrade & Compatibility Testing (Phase 1)
2. **CORE-NOTN-UP-2**: Configuration Schema Update (Phase 2)
3. **CORE-NOTN-UP-3**: Implement data_source_id Fetching (Phase 3)
4. **CORE-NOTN-UP-4**: Update Database Operations (Phase 4)
5. **CORE-NOTN-UP-5**: Testing & Validation (Phase 5)
6. **CORE-NOTN-UP-6**: Documentation & Migration Guide (Phase 6)

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
- Start: Sprint A2 (Phase 1)
- Complete: Before end of Sprint A3
- Buffer: 2-3 weeks for testing and validation

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
   - Must update schema to include `data_source_id`
   - Migration path needed for existing configs
   - Documentation updates required

2. **Testing Infrastructure** 🟡 **MEDIUM**
   - Test fixtures need `data_source_id`
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
   - Option 1: Auto-fetch `data_source_id` on first run
   - Option 2: Require manual config update
   - Recommendation: Auto-fetch with config save

7. **How do we test multi-source scenarios?**
   - Need to create test database with multiple sources
   - May require manual Notion UI setup

---

## Evidence & Investigation

**Phase -1 Investigation**: October 15, 2025, 11:18 AM - 11:53 AM (35 minutes)

**Investigation Report**: `dev/2025/10/15/phase-minus-1-notion-api-upgrade.md`

**Key Findings**:
- Current SDK: notion-client==2.2.1 (2+ years old)
- 4 database operations affected
- ADR publishing uses deprecated parent format
- Single-source databases currently safe
- Migration complexity: MEDIUM (6 phases)

**Notion Official Documentation**:
- Upgrade Guide: https://developers.notion.com/docs/upgrade-guide-2025-09-03
- FAQ: https://developers.notion.com/docs/upgrade-faqs-2025-09-03

**Affected Code**:
- services/integrations/mcp/notion_adapter.py (618 lines)
- services/integrations/notion/notion_integration_router.py (22,891 bytes)
- config/notion_user_config.py (configuration schema)

**Test Count**: 78 Notion-related tests identified

---

## Timeline & Milestones

**Recommended Start**: Sprint A2 (Phase 1 - SDK upgrade)
**Target Completion**: End of Sprint A3 (all phases)

**Milestones**:
- **Week 1 (A2)**: SDK upgrade + compatibility testing ✅
- **Week 2 (A3)**: Config schema + data_source_id implementation
- **Week 3 (A3)**: Database operations update + validation
- **Week 4 (A3)**: Documentation + final testing

**Total Effort**: 12-17 hours
**With Buffer**: 14-20 hours (20% buffer for unknowns)

---

## Next Steps

### Immediate (After Approval):
1. Create 6 child issues for tracking
2. Review notion-client 5.0.0 SDK changelog
3. Verify current database state (single-source confirmation)
4. Begin Phase 1 (SDK upgrade)

### Phase 1 Start Conditions:
- [ ] Investigation report reviewed and approved
- [ ] Sprint A2 capacity confirmed (2-3 hours available)
- [ ] GitHub child issues created for tracking
- [ ] SDK changelog reviewed
- [ ] Backup plan identified (rollback procedure)

---

## Success Criteria

**Migration is successful when**:
- ✅ SDK upgraded to 5.0.0+
- ✅ All database operations use `data_source_id`
- ✅ ADR publishing works end-to-end
- ✅ Configuration schema updated
- ✅ All 78 tests passing
- ✅ Real API validation complete
- ✅ Documentation comprehensive
- ✅ Migration guide available

---

## Related Issues

**Parent**: None (this is the parent epic)
**Children**: 6 implementation issues (to be created)
**Related**:
- #142 (CORE-NOTN: Enhanced validation) - Recently completed ✅
- #136 (CORE-NOTN: Remove hardcoding) - Verified complete ✅

---

**Issue Created**: October 15, 2025
**Investigation**: Phase -1 complete
**Status**: Ready for implementation planning
**Priority**: MEDIUM-HIGH
**Sprint**: A2 (Phase 1), A3 (Phases 2-6)

---

*"External API changes require systematic investigation and phased migration."*
*- API Migration Philosophy*
