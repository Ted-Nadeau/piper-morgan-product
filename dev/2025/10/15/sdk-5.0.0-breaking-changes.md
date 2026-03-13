# notion-client SDK Upgrade Analysis

**Date**: October 15, 2025, 12:30 PM
**Current SDK**: notion-client==2.2.1
**Target SDK**: notion-client==2.5.0 (NOT 5.0.0!)
**API Version**: 2025-09-03

---

## CRITICAL FINDING: SDK Version Confusion Resolved

### The Confusion
**Issue #165 Description Said**: "Required SDK: notion-client>=5.0.0"
**Reality**: Version 5.0.0 is for **TypeScript SDK**, not Python SDK

### Correct Information
- **TypeScript SDK**: Version 5.0.0 (mentioned in Notion upgrade guide)
- **Python SDK**: Latest is 2.5.0 (completely different versioning)
- **Our Upgrade**: notion-client==2.2.1 → notion-client==2.5.0

---

## Python SDK Version History

**Current**: 2.2.1 (Dec 28, 2023) - 21 months old
**Available Versions**:
- **2.3.0** (Dec 18, 2024)
  - Python 3.13 support
  - httpx security update
  - Added `in_trash` property
- **2.4.0** (Jun 17, 2025)
  - Added `column` param for block updates
  - Token format update (secret_ → ntn_)
  - Missing endpoint arguments added
- **2.5.0** (Aug 26, 2025) - **LATEST**
  - File upload support
  - Latest stable release

---

## API Version Support Discovery

### ✅ GOOD NEWS: Python SDK Already Supports API Versioning!

**ClientOptions Fields**:
```python
{
    'auth': Optional[str],
    'timeout_ms': int,
    'base_url': str,
    'log_level': int,
    'logger': Optional[logging.Logger],
    'notion_version': str  # ✅ API version support!
}
```

**How to Set API Version**:
```python
from notion_client import Client

# Current code (uses default API version):
client = Client(auth=api_key)

# Updated code (specifies API version 2025-09-03):
client = Client(
    auth=api_key,
    options={"notion_version": "2025-09-03"}
)
```

---

## Breaking Changes Analysis

### SDK Breaking Changes (2.2.1 → 2.5.0)

**2.3.0**:
- ✅ No breaking changes (additive features only)
- Python 3.13 support (we use 3.9, no impact)
- httpx minimum version update (security, should be compatible)

**2.4.0**:
- ⚠️ **Token format change**: `secret_` → `ntn_` prefix
  - Impact: **LOW** - Our tokens are loaded from env, format shouldn't matter to SDK
  - Verification needed: Check if our NOTION_API_KEY still works
- ✅ New `column` parameter (additive, no impact)

**2.5.0**:
- ✅ No breaking changes (adds file upload support)
- We don't use file uploads yet

**Overall SDK Risk**: 🟢 **LOW** - No major breaking changes

---

## API Breaking Changes (API version 2025-09-03)

From Notion upgrade guide and investigation:

### 1. Database/Data Source Separation 🔴 **CRITICAL**

**What Changed**:
- Database = container for one or more data sources
- Data Source = has properties (schema) and rows (pages)
- Must use `data_source_id` when creating pages in databases

**Current Code** (notion_adapter.py:398):
```python
response = self._notion_client.pages.create(
    parent={"database_id": database_id},  # ❌ Will break with multi-source
    properties=properties,
    children=initial_content
)
```

**Required for 2025-09-03**:
```python
response = self._notion_client.pages.create(
    parent={"type": "data_source_id", "data_source_id": data_source_id},
    properties=properties,
    children=initial_content
)
```

**Impact**:
- ✅ Works with single-source databases (current state)
- ❌ Breaks when user adds second data source to database
- 🔴 **CRITICAL** for ADR publishing

### 2. API Version Header Requirement

**Required**:
```python
Client(auth=api_key, options={"notion_version": "2025-09-03"})
```

**Impact**: 🟢 **EASY** - Just add `notion_version` to client initialization

---

## Compatibility Assessment

### What Works Without Changes
- ✅ Authentication (`users.me()`)
- ✅ Search operations
- ✅ Page operations (get, update)
- ✅ Block operations
- ✅ User operations
- ✅ Single-source database operations

### What Breaks (Eventually)
- ❌ Creating pages in multi-source databases
- ❌ Querying multi-source databases (may return incomplete data)
- ❌ Updating multi-source database schemas

### Migration Strategy
**Phase 1** (NOW): Upgrade SDK + Add API version header
**Phase 2-6** (LATER): Implement data_source_id support

---

## Migration Plan: Phase 1 Only (Revised)

### What We Can Do Now (Low Risk)

**1. Upgrade SDK**: 2.2.1 → 2.5.0
- ✅ No breaking changes in SDK
- ✅ Maintains backward compatibility
- ✅ Prepares for API version 2025-09-03

**2. Add API Version Support** (Optional)
- Add `notion_version` parameter to Client initialization
- Makes code ready for API version 2025-09-03
- **Does not require data_source_id changes yet**

**3. Verify Compatibility**
- Run all 78 Notion tests
- Test authentication with real API
- Verify database operations still work

### What We CANNOT Do Yet

- ❌ Cannot support multi-source databases
- ❌ Cannot use data_source_id (need Phase 2-6)
- ❌ Will still break if user adds second data source

### Why This is Safe

**Current State**:
- All our databases are single-source ✅
- Works fine with API version 2025-09-03 ✅
- No user has multi-source databases yet ✅

**After Phase 1**:
- SDK upgraded to latest ✅
- Code ready for API version ✅
- Still works with single-source ✅
- Breaking change deferred to Phases 2-6

---

## Recommended Phase 1 Scope (REDUCED)

### Step 1: Upgrade SDK
```bash
# requirements.txt line 67
notion-client==2.2.1  →  notion-client==2.5.0
```

### Step 2: Add API Version Support (Optional)
```python
# services/integrations/mcp/notion_adapter.py
# Line 72 and 84 (Client initialization)

# Before:
self._notion_client = Client(auth=api_key)

# After:
self._notion_client = Client(
    auth=api_key,
    options={"notion_version": "2025-09-03"}
)
```

### Step 3: Test Everything
- Run pytest (78 Notion tests)
- Test authentication
- Test database operations
- Verify no regressions

### Step 4: Commit
```
feat(notion): upgrade SDK from 2.2.1 to 2.5.0 with API version 2025-09-03

Changes:
- Updated notion-client: 2.2.1 → 2.5.0
- Added notion_version="2025-09-03" to Client initialization
- Verified all tests passing (78 Notion tests)
- Confirmed single-source database compatibility

Note: Full data_source_id support deferred to Phases 2-6
Part of: CORE-NOTN-UP #165, Phase 1 (revised scope)
```

---

## Time Estimate (Revised)

**Original Estimate**: 2-3 hours
**Revised Estimate**: 30-45 minutes

**Breakdown**:
- SDK upgrade: 5 min
- Add API version: 10 min
- Run tests: 10 min
- Test real API: 5 min
- Document findings: 5 min
- Commit: 5 min

**Why Faster**:
- No data_source_id implementation needed (Phase 2+)
- SDK upgrade is low-risk (no breaking changes)
- API version is optional parameter
- Tests should pass unchanged

---

## Success Criteria (Phase 1 Only)

**Must Have**:
- ✅ SDK upgraded to 2.5.0
- ✅ All 78 Notion tests passing
- ✅ Authentication working
- ✅ Database operations working
- ✅ No regressions

**Nice to Have**:
- ✅ API version 2025-09-03 configured
- ✅ Real API validation complete
- ✅ Documentation updated

**Deferred to Phase 2+**:
- ⏳ data_source_id support
- ⏳ Multi-source database handling
- ⏳ Configuration schema update

---

## Recommendation

**Proceed with reduced Phase 1**:
1. Upgrade SDK to 2.5.0 ✅
2. Add `notion_version="2025-09-03"` ✅
3. Test thoroughly ✅
4. Commit ✅
5. **STOP** - Don't implement data_source_id yet

**Why**:
- Low risk (SDK has no breaking changes)
- Quick win (30-45 minutes vs 2-3 hours)
- Prepares foundation for Phases 2-6
- Maintains current functionality
- Buys time to plan data_source_id migration

**Next Steps After Phase 1**:
- Phase 2: Update configuration schema (add data_source_id field)
- Phase 3: Implement data_source_id fetching
- Phase 4: Update database operations
- Phases 5-6: Testing and documentation

---

*"Upgrade the foundation incrementally, test thoroughly, defer complexity."*
*- Revised Migration Philosophy*
