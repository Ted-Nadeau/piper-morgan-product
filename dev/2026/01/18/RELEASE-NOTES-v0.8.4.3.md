# Release Notes: v0.8.4.3

**Release Date**: January 18, 2026
**Release Type**: Patch Release (Fresh Install Fixes)

---

## Overview

Critical fixes for the fresh install experience discovered during alpha testing. New alpha testers should now have a smooth first-time user experience (FTUX).

**Key improvements in this release:**
- **Fresh install flow fixed**: Server now properly blocks startup until migrations are applied
- **Multi-user support**: `/setup` wizard accessible for new user registration
- **Web GUI routing**: Fresh installs route to web setup wizard (not CLI)
- **Migration validation**: Database schema validation prevents cryptic column errors
- **UI polish**: Auto-generated conversation titles, editable titles, cleaner resource cards

---

## Bug Fixes

### Fresh Install Flow (#605-#609)

These five issues were discovered sequentially during alpha testing on a fresh laptop clone.

#### Issue #605: Migration Validation at Startup
**Problem**: Fresh clones started with missing database columns, causing cryptic errors.

**Fix**: Added `check_pending_migrations()` to startup - server now displays pending migrations and exits cleanly.

**Commit**: `939d66f8`

#### Issue #606: Stale todo_lists Table Reference
**Problem**: Migration `44f5cd40b495` referenced `todo_lists` table that was dropped in Aug 2025.

**Fix**: Removed all `todo_lists` references from the migration file.

**Commit**: `20ef2ec3`

#### Issue #607: CLI Wizard Instead of Web GUI
**Problem**: Fresh installs showed CLI menu instead of routing to web setup.

**Fix**: Removed CLI wizard intercept in `main.py`, server now starts normally and displays setup URL.

**Commit**: `f84edaf3`

#### Issue #608: /setup Redirects to /login
**Problem**: Once any user existed, `/setup` redirected to `/login`, blocking multi-user registration.

**Fix**: Removed redirect logic in `setup.js` - setup wizard now always accessible for new user registration.

**Commit**: `89085061`

#### Issue #609: Fresh Database Bypasses Migration Check
**Problem**: Fresh databases (no `alembic_version` table) bypassed migration validation entirely.

**Fix**: Migration checker now returns all migrations as pending for fresh databases.

**Commit**: `06c86de1`

### UI/UX Improvements

#### Issue #597: Calendar Datetime Formatting
**Problem**: Calendar data displayed raw ISO timestamps and inconsistent formats.

**Fix**: Systematic datetime and data presentation fixes across calendar handlers.

**Commit**: `1535fa8b`

#### Issue #598: Auto-Generated Conversation Titles
**Problem**: New conversations showed generic "New Conversation" title.

**Fix**: Titles now auto-generate from first message content.

**Commit**: `39fe6703`

#### Issue #599: Null Field Placeholders
**Problem**: Resource cards showed "null" or undefined for missing fields.

**Fix**: Suppress null field placeholders for cleaner display.

**Commit**: `0ea21fee`

#### Issue #600: Redundant Owner Badge
**Problem**: Owner badge displayed in single-user context (unnecessary).

**Fix**: Hide Owner badge when only one user exists.

**Commit**: `a100096e`

#### Issue #604: Editable Conversation Titles
**Problem**: Conversation titles couldn't be edited after creation.

**Fix**: Added edit capability for conversation titles.

**Commit**: `818d5092`

---

## Testing & Infrastructure

### Issue #593: Frontend JavaScript Testing Framework
Added Jest + jsdom testing infrastructure for vanilla JavaScript:
- 45 tests for Toast and FormValidation modules
- `loadScript()` helper for testing ES5 modules
- Documentation in `docs/testing/frontend-testing.md`

**Commit**: `6a86b3d9`

### Issue #590, #591: Integration Test Fixtures
Fixed fixture issues causing integration test failures.

**Commit**: `5bbf8b41`

### Issue #603: Test Infrastructure Cleanup
Fixed `tests/load` import errors and cleaned up test infrastructure.

**Commit**: `a8e67f7d`

---

## Test Results

```
=============== 1763 passed, 26 skipped ================
```

- All unit tests passing
- Fresh clone tested successfully on alpha laptop
- PM manual verification of setup flow

---

## Upgrade Notes

### For Existing Users

```bash
git pull origin main
python -m alembic upgrade head  # Required - adds new columns
python main.py
```

### For New Alpha Testers

```bash
git clone https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
docker-compose up -d
python -m alembic upgrade head
python main.py
```

Visit http://localhost:8001/setup to create your account.

**Note**: The server will now block startup if migrations are pending, showing clear instructions.

---

## Related Issues

| Issue | Type | Description |
|-------|------|-------------|
| #605 | Bug | Add migration validation to startup |
| #606 | Bug | Remove todo_lists references from migration |
| #607 | Bug | Route fresh installs to web setup wizard |
| #608 | Bug | Allow /setup access for new user registration |
| #609 | Bug | Block startup for fresh databases without migrations |
| #597 | Bug | Systematic datetime fixes for calendar |
| #598 | Enhancement | Auto-generate conversation titles |
| #599 | Bug | Suppress null field placeholders |
| #600 | Bug | Hide redundant Owner badge |
| #604 | Enhancement | Add editable conversation titles |
| #593 | Enhancement | Frontend JavaScript testing framework |
| #590 | Bug | Fix integration test fixtures |
| #591 | Bug | Fix integration test fixtures |
| #603 | Bug | Fix tests/load import error |

---

## What's Next

- Continue alpha testing (Sprint A20)
- If no new blockers found, close A20 and proceed to MUX super epics
- New alpha testers joining this weekend

---

**Full Changelog**: [v0.8.4.2...v0.8.4.3](https://github.com/mediajunkie/piper-morgan-product/compare/v0.8.4.2...v0.8.4.3)
