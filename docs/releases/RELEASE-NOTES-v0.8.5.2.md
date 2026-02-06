# Release Notes - v0.8.5.2

**Release Date**: February 6, 2026
**Type**: Bug Fix Release

---

## Summary

This release focuses on fixing critical alpha testing bugs related to chat persistence, date formatting, and calendar integration. Also includes model/database alignment fixes for timezone-aware datetimes.

---

## Bug Fixes

### Critical Fixes

- **#787 - Conversation not appearing in sidebar** - Fixed cross-user session bleed caused by localStorage session persistence across logout. Now properly clears user-specific localStorage on logout.

- **#788 - Invalid Date display** - Fixed JavaScript Date parsing by replacing `+00:00` with `Z` suffix in ISO date strings. PostgreSQL timestamptz returns `+00:00` format which JavaScript Date() doesn't parse correctly.

- **#789 - Calendar false positive** - Fixed Piper claiming "No meetings - great day for deep work!" when no calendar is connected. Now distinguishes "not connected" from "connected with no events" and stays silent when not connected.

### Additional Fixes

- **Timezone import fix** - Added missing `timezone` import to intent_service.py
- **DateTime model alignment** - Added `timezone=True` to all DateTime columns in models.py to match database schema after timestamptz migration
- **Test fixes** - Updated test_file_repository_migration.py to use timezone-aware datetimes

---

## Features

### History Sidebar Differentiation (#786)

The History sidebar now uses monthly grouping (January, February, etc.) instead of the same Today/Yesterday/This Week grouping as the Conversation List. Search functionality has been wired up to filter conversations by title.

---

## Issues Closed

- #786 - GLUE-HISTORY-DIFF: Differentiate History sidebar from Conversation list
- #787 - Conversation not appearing in sidebar after first chat
- #788 - Invalid Date shown for new conversations
- #789 - Piper claims "no meetings" without calendar connected

---

## Known Issues

- #766 - GLUE-MAINPROJ: "Is that your main project?" question repeats
- #790 - MVP: Trust-gated calendar integration behavior (enhancement for future release)

---

## Technical Notes

### Database Migration Required

If upgrading from v0.8.5.1, ensure the timestamptz migration has been applied:

```bash
alembic upgrade head
```

This converts all timestamp columns to timestamptz (timezone-aware).

### Breaking Changes

None

### Compatibility

- Python 3.11 or 3.12 required
- PostgreSQL with timestamptz support

---

## Upgrade Instructions

1. Pull the latest code from the `production` branch
2. Apply database migration: `alembic upgrade head`
3. Restart the server

---

**Full Changelog**: [v0.8.5.1...v0.8.5.2](https://github.com/mediajunkie/piper-morgan-product/compare/v0.8.5.1...v0.8.5.2)
