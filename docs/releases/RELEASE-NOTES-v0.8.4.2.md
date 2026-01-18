# Release Notes: v0.8.4.2

**Release Date**: January 15, 2026
**Release Type**: Patch Release (Bug Fixes)

---

## Overview

This patch release fixes critical calendar-related bugs discovered during alpha testing Sprint A20. The primary issue was the TEMPORAL handler showing incorrect calendar data ("No meetings") when users had multiple meetings scheduled.

**Key improvements in this release:**
- **TEMPORAL handler fixed**: "How about today?" now correctly shows calendar data
- **Tomorrow queries working**: Calendar queries for tomorrow display correct meeting times
- **Markdown rendering fixed**: Chat messages now render markdown properly
- **Sidebar ordering fixed**: Conversations display in correct chronological order

---

## Bug Fixes

### Issue #596: TEMPORAL Handler Stale Calendar Data
**Problem**: "How about today?" returned "No meetings - great day for deep work!" when user had 6 meetings scheduled.

**Root Cause**: Three compounding issues:
1. `user_id` not propagated through CalendarIntegrationRouter → GoogleCalendarMCPAdapter
2. Naive `datetime.now()` comparisons with timezone-aware API data caused errors
3. Error handler returned fallback data with 0 meetings

**Fix**:
- Added `user_id` parameter propagation through entire calendar stack
- Fixed timezone-aware datetime comparisons in `get_free_time_blocks()` and `_generate_recommendations()`
- Fixed field name mismatch (Google uses `summary`, handlers expected `title`)
- Added human-readable time formatting (ISO → "12:00 PM")

**Commits**: `ab7e2342`

### Issue #588: Tomorrow Calendar Intent
**Problem**: "What's on my agenda for tomorrow?" returned API errors and wrong format.

**Root Causes**:
- "agenda" patterns in wrong classifier list (TEMPORAL instead of CALENDAR_QUERY)
- API timestamp format error (`+00:00Z` invalid)
- `original_message` read from wrong context location
- Naive datetime used for local→UTC conversion

**Fix**:
- Added agenda patterns to CALENDAR_QUERY_PATTERNS
- Fixed timestamp format in `get_events_in_range()`
- Fixed `original_message` reading from `intent.context`
- Set `workflow_id=None` for direct responses (fixed timeout)

**Commits**: `74af42d0`, `1bd91b88`

### Issue #592: Markdown Rendering
**Problem**: Chat messages displayed raw markdown instead of formatted text.

**Fix**: Changed `renderBotMessage` type from "reply" to "success" to trigger markdown parsing via DDD domain service.

**Commits**: `73592af2`

### Issue #587: Sidebar Conversation Ordering
**Problem**: New conversations appeared below old ones in sidebar.

**Fix**: Corrected conversation ordering and timezone display.

**Commits**: `de57921e`

---

## Technical Debt Filed

### Issue #597: Systematic Calendar Issues
During #596 investigation, we identified systematic issues that were patched locally but need comprehensive fixes:

- **Inconsistent datetime handling**: Multiple `datetime.now()` calls should use `.astimezone()`
- **No presentation layer**: Adapter returns raw ISO timestamps, each handler formats independently
- **Misleading fallback message**: "No meetings" appears on errors, not just empty calendars

This issue tracks the architectural debt for future cleanup.

---

## Test Results

```
=============== 1730 passed, 26 skipped ================
```

- 42 calendar-specific tests passing
- All existing tests continue to pass
- PM manual verification of all fixes

---

## Upgrade Notes

- **Database migration required**: Run `python -m alembic upgrade head` (adds `orientation_seen` column)
- **No configuration changes required**
- **Server restart required** to pick up calendar fixes

### Migration Command

```bash
# If using virtual environment (recommended):
source venv/bin/activate
alembic upgrade head

# Or without activating venv:
python -m alembic upgrade head
```

**Note**: If you skip this step, account creation in the setup wizard will fail with a database error.

---

## Related Issues

| Issue | Type | Description |
|-------|------|-------------|
| #596 | Bug | TEMPORAL handler stale calendar data |
| #588 | Bug | Tomorrow calendar intent fixes |
| #592 | Bug | Markdown rendering in chat |
| #587 | Bug | Sidebar conversation ordering |
| #597 | Tech Debt | Systematic calendar datetime issues |
| #595 | Enhancement | Multi-intent handling (MUX - filed for future) |

---

## What's Next

- Continue alpha testing (Sprint A20)
- Address #597 systematic calendar issues in future sprint
- MUX work (#427, #595) for conversational coherence

---

**Full Changelog**: [v0.8.4.1...v0.8.4.2](https://github.com/mediajunkie/piper-morgan-product/compare/v0.8.4.1...v0.8.4.2)
