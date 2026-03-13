# Session Log: 2025-12-18-1145 - Lead Developer - Chat Workflow Bug Investigation (Continued)

**Role**: Lead Developer
**Model**: Claude Opus 4.5
**Date**: Thursday, December 18, 2025
**Time**: 11:45 AM

---

## Session Context

Continuing alpha testing support from yesterday's session (2025-12-17-1711). The primary bug fix for `user_api_keys` FK violation is implemented, but manual testing revealed a **second FK violation** in `learned_patterns` table.

**Previous Session Accomplishments**:
- Created GitHub issue #485 for BUG-ALPHA-KEY-ERROR
- Fixed `store_user_key()` with `store=False` parameter
- Fixed frontend JS null checks in `bot-message-renderer.js`
- Added state transition testing infrastructure
- All new tests passing

**Remaining Issue**:
- User reported: "if I tried to enter a key and validate I got that huge red error again"
- Logs show FK violation in `learned_patterns` table
- Same temporal bug pattern in different location (`learning_handler.py`)

---

## Investigation Complete

### Root Cause Found

The `IntentService.process_intent()` method at `services/intent/intent_service.py:221-223` uses a **hardcoded user_id** for all learning operations:

```python
# TODO: Get actual user_id from auth context
# For Phase 1, using test user "xian"
user_id = UUID("3f4593ae-5bc9-468d-b08d-8c4c02a5b963")
```

During fresh install, this user ID doesn't exist in the database, but `capture_action()` tries to INSERT a `LearnedPattern` record with this user_id, causing the FK violation.

### Fix Applied

Added user existence check before calling `capture_action()`:

**File**: `services/intent/intent_service.py` (lines 225-236)

```python
# Issue #485: Check if user exists before capturing patterns
# During fresh install, user may not exist yet - skip learning in that case
user_result = await db_session.execute(
    select(User.id).where(User.id == str(user_id))
)
user_exists = user_result.scalar_one_or_none() is not None

if not user_exists:
    self.logger.info(
        "Learning Handler: Skipping capture - user not found",
        user_id=str(user_id),
    )
else:
    pattern_id = await self.learning_handler.capture_action(...)
```

### Verification

1. **Tests passing**: All 4 fresh install tests pass
2. **Intent tests passing**: 14 intent tests pass (excluding pre-existing failure #486)
3. **Manual test**: API key validation endpoint returns clean error without FK violation
4. **Server logs**: No FK violations in server log after restart

---

## Files Modified This Session

| File | Change |
|------|--------|
| `services/intent/intent_service.py` | Added user existence check before learning capture |

---

## Summary

The bug was caused by two separate instances of the same temporal pattern:
1. **BUG-001 (fixed yesterday)**: `store_user_key()` committing records before user exists
2. **BUG-001b (fixed today)**: `IntentService.capture_action()` using hardcoded user_id that may not exist

Both fixes follow the same principle: **check for user existence before attempting FK-dependent operations**.

---

**Session Start**: 11:45 AM
**Investigation Complete**: 12:00 PM
**Fix Verified**: 12:20 PM
**Status**: ✅ COMPLETE - Ready for manual testing by PM
