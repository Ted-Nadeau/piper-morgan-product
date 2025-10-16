# Code Agent Prompt: Phase 1 - SDK Upgrade & Compatibility Testing

**Date**: October 15, 2025, 12:06 PM
**Sprint**: A2 - Notion & Errors
**Issue**: CORE-NOTN-UP-1 (part of #165)
**Phase**: 1 (SDK Upgrade & Compatibility Testing)
**Duration**: 2-3 hours
**Agent**: Code Agent

---

## Mission

Upgrade notion-client SDK from 2.2.1 to 5.0.0+ and verify compatibility with existing code.

**Context**: Notion API version 2025-09-03 requires SDK 5.0.0+. We need to upgrade the SDK and ensure no breaking changes affect our existing integration.

**Philosophy**: Upgrade first, test thoroughly, fix issues immediately.

---

## Current State

**From Investigation**:
- Current SDK: `notion-client==2.2.1` (requirements.txt:67)
- Affected code: `services/integrations/mcp/notion_adapter.py` (618 lines)
- Test count: 78 Notion-related tests
- Critical operations: ADR publishing, database queries

---

## Implementation Steps

### Step 1: Review SDK Changelog (Important!)

```bash
# First, check what's new in SDK 5.0.0
# Look for breaking changes beyond just the version header
```

**Research**:
- Visit: https://github.com/ramnes/notion-sdk-py/releases
- Or check: https://pypi.org/project/notion-client/5.0.0/
- Document breaking changes found

**Create**: `/tmp/sdk-5.0.0-breaking-changes.md` with findings

---

### Step 2: Backup Current State

```bash
# Create backup of requirements.txt
cp requirements.txt requirements.txt.backup.$(date +%Y%m%d)

# Document current test results
pytest tests/ -k notion --co -q > /tmp/tests-before-upgrade.txt
```

**Safety first**: Can rollback if needed

---

### Step 3: Update requirements.txt

```bash
# Current line (requirements.txt:67):
# notion-client==2.2.1

# Update to:
# notion-client>=5.0.0
```

**Use str_replace**:
```python
str_replace(
    path="requirements.txt",
    old_str="notion-client==2.2.1",
    new_str="notion-client>=5.0.0",
    description="Upgrade notion-client SDK for API version 2025-09-03 support"
)
```

---

### Step 4: Install New SDK

```bash
# Uninstall old version first
pip uninstall -y notion-client

# Install new version
pip install notion-client>=5.0.0

# Verify installation
pip show notion-client | grep Version
```

**Expected**: Should show version 5.0.0 or higher

**Document**: Actual version installed

---

### Step 5: Quick Syntax Check

```bash
# Verify imports still work
python -c "from services.integrations.mcp.notion_adapter import NotionMCPAdapter; print('Import successful')"

# Check for any obvious syntax errors
python -m py_compile services/integrations/mcp/notion_adapter.py
python -m py_compile services/integrations/notion/notion_integration_router.py
```

**If errors**: Document and fix before proceeding

---

### Step 6: Test Authentication

```bash
# Quick test that authentication still works with new SDK
# Use the real API test script from earlier

python -c "
import os
import sys
from pathlib import Path

# Load environment
from dotenv import load_dotenv
load_dotenv()

from notion_client import Client

api_key = os.getenv('NOTION_API_KEY')
if not api_key:
    print('ERROR: NOTION_API_KEY not found')
    sys.exit(1)

client = Client(auth=api_key)
user = client.users.me()

print(f'✅ Authentication successful!')
print(f'User: {user[\"name\"]} ({user[\"type\"]})')
print(f'SDK working with new version')
"
```

**Expected**: Authentication succeeds, user info returned

**If fails**: This is a critical blocker - document error and investigate

---

### Step 7: Run Notion Test Suite

```bash
# Run all Notion-related tests
pytest tests/ -k notion -v --tb=short

# Capture results
pytest tests/ -k notion -v --tb=short > /tmp/tests-after-upgrade.txt 2>&1

# Quick summary
echo "Test Summary:"
pytest tests/ -k notion --tb=line | tail -20
```

**Expected**: All tests should pass (or same pass rate as before)

**Document**:
- Number of tests run
- Pass/fail/skip counts
- Any new failures (these are breaking changes)

---

### Step 8: Identify Breaking Changes

```bash
# Compare test results
diff /tmp/tests-before-upgrade.txt /tmp/tests-after-upgrade.txt > /tmp/test-diff.txt

# If tests fail, identify the specific failures
pytest tests/ -k notion -v | grep FAILED
```

**If failures found**:
- Document each failure
- Identify the breaking API change
- Plan fix (don't implement yet - just document)

---

### Step 9: Test Real API Operations

**Only if authentication and tests pass**, test key operations:

```python
# Create test script: /tmp/test_sdk_operations.py
import os
from dotenv import load_dotenv
load_dotenv()

from notion_client import Client

api_key = os.getenv('NOTION_API_KEY')
client = Client(auth=api_key)

print("Testing SDK 5.0.0+ operations...")

# Test 1: Get database (should still work)
try:
    db_id = "25e11704d8bf80deaac2f806390fe7da"  # ADR database
    db = client.databases.retrieve(database_id=db_id)
    print(f"✅ Get database: SUCCESS")
    print(f"   Database: {db.get('title', [{}])[0].get('plain_text', 'N/A')}")
except Exception as e:
    print(f"❌ Get database: FAILED - {e}")

# Test 2: Query database (should still work)
try:
    results = client.databases.query(database_id=db_id)
    print(f"✅ Query database: SUCCESS ({len(results['results'])} pages)")
except Exception as e:
    print(f"❌ Query database: FAILED - {e}")

# Test 3: List databases (should still work)
try:
    search = client.search(filter={"property": "object", "value": "database"})
    print(f"✅ List databases: SUCCESS ({len(search['results'])} found)")
except Exception as e:
    print(f"❌ List databases: FAILED - {e}")

print("\n✅ All SDK operations tested successfully!")
```

**Run**:
```bash
python /tmp/test_sdk_operations.py
```

**Expected**: All operations succeed

---

### Step 10: Document Findings

Create: `/tmp/phase-1-sdk-upgrade-results.md`

```markdown
# Phase 1: SDK Upgrade Results

**Date**: October 15, 2025, 12:XX PM  
**Duration**: [actual time]

---

## SDK Upgrade

**Before**: notion-client==2.2.1  
**After**: notion-client==[installed version]  
**Status**: ✅ Installed successfully

---

## Breaking Changes Found

### From SDK Changelog:
[List breaking changes from SDK 5.0.0 release notes]

### From Testing:
[List any failures or issues found]

---

## Test Results

**Before Upgrade**:
- Tests run: [count]
- Passed: [count]
- Failed: [count]
- Skipped: [count]

**After Upgrade**:
- Tests run: [count]
- Passed: [count]
- Failed: [count]
- Skipped: [count]

**New Failures**: [list or "none"]

---

## Authentication Test

**Status**: [✅ SUCCESS / ❌ FAILED]  
**User**: [name if success]  
**Type**: [person/bot if success]

---

## Real API Tests

1. Get database: [✅/❌]
2. Query database: [✅/❌]
3. List databases: [✅/❌]

---

## Compatibility Assessment

**Overall**: [✅ COMPATIBLE / ⚠️ MINOR ISSUES / ❌ MAJOR ISSUES]

**Issues Found**: [count]

### Critical Issues (Block Phase 2):
[List or "none"]

### Non-Critical Issues (Can defer):
[List or "none"]

---

## Fixes Needed

### Immediate (Required for Phase 2):
- [ ] [Fix 1]
- [ ] [Fix 2]

### Later (Can defer to Phase 4):
- [ ] [Fix 1]

---

## Recommendation

**Proceed to Phase 2**: [YES / NO / WITH FIXES]

**Rationale**: [explanation]

---

## Next Steps

[What to do next based on results]
```

---

### Step 11: Fix Critical Issues (If Any)

**Only if critical issues found**:

```bash
# Fix each critical issue identified
# Document each fix
# Re-run tests after each fix
```

**Goal**: Get to clean test pass before moving to Phase 2

---

### Step 12: Commit Changes

**If successful**:

```bash
git add requirements.txt
git add requirements.txt.backup.*  # Include backup

git commit -m "feat(notion): upgrade notion-client SDK from 2.2.1 to 5.0.0+

Upgrade required for Notion API version 2025-09-03 support.

Changes:
- Updated notion-client==2.2.1 → notion-client>=5.0.0
- Verified authentication works with new SDK
- Confirmed all 78 Notion tests passing
- No breaking changes affecting current integration

Part of: CORE-NOTN-UP #165, Phase 1
Sprint: A2"

git push origin main
```

**If issues found**:

```bash
# Create separate commit for each fix
git commit -m "fix(notion): [specific fix for SDK 5.0.0 compatibility]"
```

---

## Deliverables

### Phase 1 Complete When:
- [ ] SDK upgraded to 5.0.0+
- [ ] Breaking changes documented
- [ ] All tests passing (or issues documented)
- [ ] Authentication verified
- [ ] Real API operations tested
- [ ] Findings documented
- [ ] Changes committed

---

## Success Criteria

**Minimum for Success**:
- ✅ SDK upgraded to 5.0.0+
- ✅ Authentication works
- ✅ No critical breaking changes
- ✅ Test pass rate maintained or improved
- ✅ Can proceed to Phase 2

**Ideal Success**:
- ✅ All above
- ✅ 100% test pass rate
- ✅ No issues found
- ✅ Clean commit

---

## Risk Mitigation

### If Tests Fail:
1. Document exact failures
2. Check if failures are SDK-related or pre-existing
3. Fix SDK-related issues before proceeding
4. If too many issues: Consider rollback and re-plan

### If Authentication Fails:
1. **STOP** - This is critical
2. Check SDK changelog for auth changes
3. Review API key format requirements
4. May need to regenerate API key

### If Rollback Needed:
```bash
# Restore backup
cp requirements.txt.backup.* requirements.txt
pip uninstall -y notion-client
pip install notion-client==2.2.1
# Verify rollback works
pytest tests/ -k notion -v
```

---

## Time Budget

**Target**: 2-3 hours

- SDK changelog review: 15 min
- Backup & update: 10 min
- Install & verify: 10 min
- Test authentication: 5 min
- Run test suite: 20 min
- Test real API: 10 min
- Document findings: 20 min
- Fix issues (if any): 30-60 min
- Commit & push: 10 min

**Buffer**: 20 min for unexpected issues

---

## What NOT to Do

- ❌ Don't skip the changelog review
- ❌ Don't skip backing up requirements.txt
- ❌ Don't proceed if authentication fails
- ❌ Don't ignore test failures
- ❌ Don't implement Phase 2 changes yet
- ❌ Don't commit without documenting

## What TO Do

- ✅ Review SDK changelog thoroughly
- ✅ Test each step before proceeding
- ✅ Document all findings
- ✅ Fix critical issues immediately
- ✅ Maintain test pass rate
- ✅ Commit with clear message

---

## Context

**Why Phase 1 Matters**:
- SDK upgrade is foundation for everything else
- Breaking changes must be identified now
- Can't proceed to Phase 2 without stable SDK
- Rollback is easy now, harder later

**What Comes After**:
- Phase 2: Config schema update (add data_source_id)
- Phase 3: Implement data_source_id fetching
- Phase 4: Update database operations
- Phases 5-6: Testing and documentation

---

**Phase 1 Start Time**: 12:10 PM  
**Expected Completion**: ~2:10-3:10 PM (2-3 hours)  
**Status**: Ready to begin SDK upgrade

**LET'S UPGRADE!** 🚀

---

*"Upgrade the foundation first, build on stability."*
*- Phase 1 Philosophy*
