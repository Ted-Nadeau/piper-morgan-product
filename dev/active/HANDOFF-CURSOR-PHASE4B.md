# Phase 4B Handoff to Cursor - Test UUID Conversions

**Date**: 2025-11-09 21:56
**From**: Code (Claude Code Agent)
**To**: Cursor Agent
**Issue**: #262 UUID Migration + #291 Token Blacklist FK

## Current Status

### ✅ COMPLETED (Phases -1 through 4A)

1. **Database Migration**: Successfully migrated users.id VARCHAR→UUID
2. **Model Updates**: 7 models updated to UUID
3. **Service Code**: 52 files with type hints updated
4. **Import Infrastructure**:
   - Fixed 34 service files with incorrect UUID imports
   - Created UUID fixtures in `tests/conftest.py`
   - Removed all AlphaUser references

### 🔄 IN PROGRESS (Phase 4B)

**Test UUID Conversions** - 76 test files need string IDs replaced with UUIDs

## What You Need to Do

### Step 1: Scan for Issues

Use the systematic scanner I created:

```bash
python /tmp/scan_test_uuid_issues.py
```

This will show:
- 54 files missing `from uuid import UUID`
- 76 files with hardcoded string IDs like `id="test_user_create"`

### Step 2: Fix Tests in Batches

**Batch Order** (recommended):
1. **Database tests** (10 files in `tests/database/`)
2. **Auth/Security tests** (15 files in `tests/auth/`, `tests/security/`)
3. **Integration tests** (20 files in `tests/integration/`)
4. **Remaining tests** (31 files in other directories)

**For Each File:**

1. Add UUID import:
   ```python
   from uuid import UUID, uuid4
   from tests.conftest import TEST_USER_ID, TEST_USER_ID_2
   ```

2. Replace hardcoded IDs:
   ```python
   # BEFORE:
   user = User(id="test_user_123", ...)

   # AFTER (option 1 - dynamic):
   user = User(id=uuid4(), ...)

   # AFTER (option 2 - fixture for reuse):
   user = User(id=TEST_USER_ID, ...)
   ```

3. Fix SELECT statements:
   ```python
   # BEFORE:
   result = await session.execute(select(User).where(User.id == "test_user_123"))

   # AFTER:
   result = await session.execute(select(User).where(User.id == user.id))
   ```

4. Test the file:
   ```bash
   python -m pytest tests/database/test_user_model.py -xvs
   ```

### Step 3: Example (Already Done)

I've completed `tests/database/test_user_model.py` as an example:

**Changes Made:**
- Added UUID imports
- Replaced 10 hardcoded string IDs with `uuid4()` or `TEST_USER_ID`
- Fixed SELECT statements to use `user.id` instead of hardcoded strings

**Test Status**: UUID conversion working correctly
**Note**: May have database cleanup issues (duplicate keys from previous runs) - these are pre-existing

### Step 4: Common Patterns to Replace

```python
# Pattern 1: User IDs
id="test_user_create"           → id=uuid4()
user_id="system"                 → user_id=TEST_USER_ID
owner_id="test"                  → owner_id=uuid4()

# Pattern 2: Session/Workflow IDs
session_id="test_session"        → session_id=str(uuid4())
workflow_id="test_workflow"      → workflow_id=str(uuid4())

# Pattern 3: Token IDs (string UUIDs)
token_id="test_token_123"        → token_id=str(uuid4())
```

## Tools Available

### Scanner Script
Location: `/tmp/scan_test_uuid_issues.py`
Purpose: Identifies all files needing UUID fixes

### Batch Fix Script Template
```python
#!/usr/bin/env python3
"""Fix UUID issues in batch of test files"""
from pathlib import Path

files = [
    "tests/database/test_file1.py",
    "tests/database/test_file2.py",
    # ... add more
]

for filepath in files:
    content = Path(filepath).read_text()

    # Add import if missing
    if 'from uuid import UUID' not in content:
        content = content.replace(
            'import pytest',
            'import pytest\nfrom uuid import UUID, uuid4'
        )

    # Replace IDs (customize per batch)
    content = content.replace('id="test_user_create"', 'id=uuid4()')

    Path(filepath).write_text(content)
```

## Testing Strategy

**After each batch:**
```bash
# Run specific test directory
python -m pytest tests/database/ -x

# Run full suite (at end)
python -m pytest tests/ -x
```

**Expected Issues:**
- Database cleanup (duplicate keys) - pre-existing, not your problem
- Some tests may need unique emails/usernames per run
- Focus on UUID conversion correctness

## UUID Fixtures Available

From `tests/conftest.py`:
```python
TEST_USER_ID = UUID("11111111-1111-1111-1111-111111111111")
TEST_USER_ID_2 = UUID("22222222-2222-2222-2222-222222222222")
TEST_SESSION_ID = UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
TEST_WORKFLOW_ID = UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")
XIAN_USER_ID = UUID("3f4593ae-5bc9-468d-b08d-8c4c02a5b963")
```

Use these when tests need consistent/reusable UUIDs.

## Success Criteria

Phase 4B complete when:
- [ ] All 76 test files have UUID imports
- [ ] All hardcoded string IDs replaced with UUIDs
- [ ] Test suite runs without UUID-related errors
- [ ] Document any remaining failures (if not UUID-related)

## Next Phase

After Phase 4B completion → **Phase 5: Integration Testing**
- E2E auth flow tests
- Issue #291 cascade delete verification
- Performance testing

## Questions?

Refer to:
- Session log: `/Users/xian/Development/piper-morgan/dev/active/2025-11-09-1303-prog-code-log.md`
- Scanner script: `/tmp/scan_test_uuid_issues.py`
- Completed example: `tests/database/test_user_model.py`

---

**Status**: Ready for systematic test file fixes
**Estimated Effort**: ~2-3 hours for 76 files in batches
**Risk**: Low - infrastructure complete, pattern is mechanical
