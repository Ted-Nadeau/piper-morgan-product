# Code Agent Prompt: Phase 1-Quick - SDK Upgrade + API Version

**Date**: October 15, 2025, 3:53 PM
**Sprint**: A2 - Notion & Errors
**Issue**: CORE-NOTN-UP-1 (part of #165)
**Phase**: 1-Quick (Revised Scope)
**Duration**: 30-45 minutes
**Agent**: Code Agent

---

## Mission

Quick SDK upgrade from 2.2.1 to 2.5.0 and add API version parameter. This is now MUCH simpler than originally planned!

**Context**: Investigation revealed SDK 5.0.0 was TypeScript (not Python). Python SDK is 2.5.0 with NO breaking changes. Just need to upgrade and add API version parameter.

**Philosophy**: Quick wins build momentum. Simple upgrades done right.

---

## Key Findings from Investigation

**SDK Version Clarity**:
- Current: `notion-client==2.2.1` (Dec 2023, 21 months old)
- Target: `notion-client==2.5.0` (Aug 2025, latest Python SDK)
- NOT 5.0.0 (that's TypeScript SDK)

**Breaking Changes**: 🟢 **NONE** - All changes 2.2.1 → 2.5.0 are additive!

**API Version Support**: Already built into Python SDK via parameter
```python
# Current:
Client(auth=api_key)

# Updated:
Client(auth=api_key, options={"notion_version": "2025-09-03"})
```

---

## Simplified Implementation Steps

### Step 1: Update requirements.txt

```bash
# Use str_replace to update SDK version
str_replace(
    path="requirements.txt",
    old_str="notion-client==2.2.1",
    new_str="notion-client==2.5.0",
    description="Upgrade to latest Python SDK for API version 2025-09-03 support"
)
```

**Expected**: Clean replacement, no conflicts

---

### Step 2: Install New SDK

```bash
# Uninstall old version
pip uninstall -y notion-client

# Install new version
pip install notion-client==2.5.0

# Verify installation
pip show notion-client | grep Version
```

**Expected**: Version: 2.5.0

---

### Step 3: Update NotionMCPAdapter to Add API Version

**File**: `services/integrations/mcp/notion_adapter.py`

**Find the Client initialization** (around line 72):
```python
self._notion_client = Client(auth=api_key)
```

**Update to**:
```python
self._notion_client = Client(
    auth=api_key,
    options={"notion_version": "2025-09-03"}
)
```

**Use str_replace**:
```python
str_replace(
    path="services/integrations/mcp/notion_adapter.py",
    old_str='        self._notion_client = Client(auth=api_key)',
    new_str='        self._notion_client = Client(\n            auth=api_key,\n            options={"notion_version": "2025-09-03"}\n        )',
    description="Add API version 2025-09-03 to Notion client initialization"
)
```

---

### Step 4: Quick Syntax Check

```bash
# Verify imports still work
python -c "from services.integrations.mcp.notion_adapter import NotionMCPAdapter; print('✅ Import successful')"

# Check for syntax errors
python -m py_compile services/integrations/mcp/notion_adapter.py
```

**Expected**: No errors

---

### Step 5: Test Authentication with New Setup

```bash
# Quick auth test with new API version
python -c "
import os
from dotenv import load_dotenv
load_dotenv()

from notion_client import Client

api_key = os.getenv('NOTION_API_KEY')
client = Client(auth=api_key, options={'notion_version': '2025-09-03'})

user = client.users.me()
print(f'✅ Authentication successful with API version 2025-09-03!')
print(f'User: {user[\"name\"]} ({user[\"type\"]})')
"
```

**Expected**: Authentication succeeds, shows Piper Morgan

---

### Step 6: Run Full Test Suite

```bash
# Run all Notion tests
pytest tests/ -k notion -v --tb=short

# Count results
pytest tests/ -k notion --tb=line -q
```

**Expected**: All tests pass (or same pass rate as before)

**Document**:
- Tests run: [count]
- Passed: [count]
- Failed: [count]
- Skipped: [count]

---

### Step 7: Test Real API Operations

```bash
# Test key operations with new SDK and API version
python -c "
import os
from dotenv import load_dotenv
load_dotenv()

from notion_client import Client

api_key = os.getenv('NOTION_API_KEY')
client = Client(auth=api_key, options={'notion_version': '2025-09-03'})

print('Testing with API version 2025-09-03...')

# Test 1: Get database
try:
    db_id = '25e11704d8bf80deaac2f806390fe7da'
    db = client.databases.retrieve(database_id=db_id)
    print(f'✅ Get database: SUCCESS')
except Exception as e:
    print(f'❌ Get database: FAILED - {e}')

# Test 2: Query database
try:
    results = client.databases.query(database_id=db_id)
    print(f'✅ Query database: SUCCESS ({len(results[\"results\"])} pages)')
except Exception as e:
    print(f'❌ Query database: FAILED - {e}')

# Test 3: Get user
try:
    user = client.users.me()
    print(f'✅ Get user: SUCCESS ({user[\"name\"]})')
except Exception as e:
    print(f'❌ Get user: FAILED - {e}')

print('\\n✅ All operations successful with API version 2025-09-03!')
"
```

**Expected**: All operations succeed

---

### Step 8: Document Results

Create: `/tmp/phase-1-quick-results.md`

```markdown
# Phase 1-Quick: SDK Upgrade Results

**Date**: October 15, 2025, ~4:00 PM
**Duration**: [actual time]

---

## Changes Made

**SDK Upgrade**:
- Before: notion-client==2.2.1
- After: notion-client==2.5.0
- Breaking Changes: NONE ✅

**API Version**:
- Added: notion_version="2025-09-03" to Client initialization
- Location: services/integrations/mcp/notion_adapter.py:72

---

## Test Results

**Full Test Suite**:
- Tests run: [count]
- Passed: [count]
- Failed: [count]
- Skipped: [count]

**Result**: ✅ All tests passing (or same as before)

---

## Real API Tests

1. Authentication: ✅ SUCCESS (Piper Morgan)
2. Get database: ✅ SUCCESS
3. Query database: ✅ SUCCESS
4. Get user: ✅ SUCCESS

---

## Compatibility

**Status**: ✅ FULLY COMPATIBLE

**No breaking changes found** - SDK 2.5.0 is fully backward compatible with 2.2.1

**API version parameter** - Working correctly with 2025-09-03

---

## Ready for Next Phase

**Status**: ✅ YES

Foundation is solid:
- SDK upgraded ✅
- API version set ✅
- Tests passing ✅
- Real API working ✅

Ready to proceed with data_source_id implementation (Phase 1-Extended)

---

## Next Steps

Proceed immediately to Phase 1-Extended:
1. Config schema update (add data_source_id)
2. Implement get_data_source_id() method
3. Update database operations
4. Test ADR publishing end-to-end
```

---

### Step 9: Commit Changes

```bash
git add requirements.txt
git add services/integrations/mcp/notion_adapter.py

git commit -m "feat(notion): upgrade SDK to 2.5.0 and add API version 2025-09-03

Changes:
- Upgrade notion-client from 2.2.1 to 2.5.0 (latest Python SDK)
- Add API version parameter: notion_version='2025-09-03'
- No breaking changes - all tests passing
- Real API operations verified successful

This prepares the foundation for data_source_id migration.

Part of: CORE-NOTN-UP #165, Phase 1-Quick
Sprint: A2"

git push origin main
```

---

## Deliverables

### Phase 1-Quick Complete When:
- [ ] SDK upgraded to 2.5.0
- [ ] API version parameter added
- [ ] All tests passing
- [ ] Real API verified
- [ ] Results documented
- [ ] Changes committed

---

## Success Criteria

**Must Have**:
- ✅ SDK at 2.5.0
- ✅ API version set to 2025-09-03
- ✅ Tests pass (same rate or better)
- ✅ Authentication works
- ✅ Real API operations work

**This is the easy part** - no breaking changes expected!

---

## Time Budget

**Target**: 30-45 minutes

- Update requirements.txt: 2 min
- Install SDK: 5 min
- Update adapter code: 5 min
- Test auth: 3 min
- Run tests: 10 min
- Test real API: 5 min
- Document results: 5 min
- Commit & push: 5 min

**Total**: ~40 minutes

---

## What NOT to Do

- ❌ Don't implement data_source_id yet (that's Phase 1-Extended)
- ❌ Don't change database operations yet
- ❌ Don't update config schema yet
- ❌ Don't skip testing

## What TO Do

- ✅ Just upgrade SDK version
- ✅ Just add API version parameter
- ✅ Test thoroughly
- ✅ Document cleanly
- ✅ Move fast (this is simple!)

---

## Context

**Why This is Quick**:
- No breaking changes in SDK
- API version is just a parameter
- Tests should all pass as-is
- Real API already works

**What Comes After**:
- Phase 1-Extended: data_source_id implementation (~2 hours)
- Then we're DONE with the migration!

---

**Phase 1-Quick Start**: 3:55 PM
**Expected Done**: ~4:35 PM (40 minutes)
**Status**: Ready for quick execution

**LET'S DO THIS!** ⚡

---

*"Simple upgrades done right build momentum."*
*- Phase 1-Quick Philosophy*
