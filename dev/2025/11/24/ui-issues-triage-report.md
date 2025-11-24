# UI Issues Triage Report - v0.8.1 Alpha Testing
**Date**: November 24, 2025 - 10:45 AM
**Agent**: Claude Code (Programmer)
**Source**: [dev/active/UI-issues.csv](../active/UI-issues.csv)

## Executive Summary

Investigated 14 reported UI issues from alpha testing. Root cause analysis shows:
- **6 HIGH severity** - Integration gaps (routes exist but not working)
- **4 MEDIUM severity** - Incomplete implementation (UI exists, behavior missing)
- **4 LOW severity** - Polish/cosmetic issues

**Primary Pattern**: The classic **75% complete pattern** - features were built but not fully integrated or tested end-to-end.

---

## HIGH SEVERITY ISSUES (P0 Candidates)

### #4: Standup - Generate Button Hangs
**Category**: Integration Gap
**Root Cause**: Button calls `/api/v1/standup/generate` but likely:
- Missing error handling for unconfigured API keys
- No graceful degradation for first-time users
- Backend may require OpenAI key that's not validated

**Evidence**:
- `templates/standup.html` exists with button
- `web/api/routes/standup.py` exists (24KB file)
- Route mounted in web/app.py:204

**Fix Estimate**: 30 min
- Add frontend error handling
- Backend: Return clear error if API key missing
- Show setup guidance instead of hanging

---

### #6: Lists - "Create New List" Button Fails
**Category**: Integration Gap
**Root Cause**: Frontend calls `/api/v1/lists` POST endpoint, backend exists but may have:
- Auth/permission issues
- Missing `owner_id` in request
- SEC-RBAC validation failing

**Evidence**:
- `templates/lists.html:226` - calls `POST /api/v1/lists`
- `web/api/routes/lists.py` exists (23KB file)
- JavaScript dialog exists (`createNewList()` function at line 201)

**Fix Estimate**: 15 min
- Debug actual error (check browser console)
- Likely missing authentication or SEC-RBAC owner_id

---

### #7: Todos - Equivalent Issues (Breadcrumb, "My", Button Fails)
**Category**: Incomplete Implementation
**Root Cause**: Same as Lists issue + cosmetic problems

**Evidence**:
- `templates/todos.html:4` - Title says "My Todos" (should be "Todos")
- `templates/todos.html:69` - Breadcrumb says "Todos" (correct)
- `templates/todos.html:74` - Button calls `createNewTodo()` which posts to `/api/v1/todos`

**Issues**:
1. Title inconsistency ("My Todos" vs "Todos")
2. H1 label has emoji but should match nav ("Todos" not "My Todos")
3. Create button likely has same auth issue as Lists

**Fix Estimate**: 20 min (15 min for button fix + 5 min for label fix)

---

### #8: Files - Page Says "Coming Soon" But Feature Exists
**Category**: Misunderstood/Incomplete
**Root Cause**: UI route returns "Coming Soon" template, but Files API exists

**Evidence**:
- `web/api/routes/ui.py:@router.get("/files")` - serves "Coming Soon"
- `web/api/routes/files.py` - Full Files API exists (18KB, includes list_files)
- `templates/files.html` exists (10KB)

**Reality Check**: Files feature IS built and should be wired up

**Fix Estimate**: 10 min
- Change `ui.py` to serve `files.html` instead of "Coming Soon"
- Verify authentication context is passed

---

### #13: Settings/Integrations - Says "Coming Soon" But Features Exist
**Category**: Misunderstood
**Root Cause**: Multiple integration APIs exist (Slack, GitHub, Notion, Calendar) but settings page shows "Coming Soon"

**Evidence**:
- `web/api/routes/ui.py:161` - `/settings/integrations` serves "Coming Soon" placeholder
- Integration routers exist and are mounted:
  - Slack integration
  - GitHub integration
  - Notion integration
  - Calendar integration

**Issues User Reported**: "clicking it causes an error"

**Fix Estimate**: 45 min
- Create proper integrations settings page
- List available integrations
- Show connection status
- Provide connect/disconnect buttons
- Handle errors gracefully

---

### #14: User Menu - Shows "user", Logout Doesn't Work
**Category**: Integration Gap
**Root Cause**: User context not being passed from server to navigation component

**Evidence**:
- `templates/components/navigation.html:324` - Hardcoded "User" fallback
- `templates/components/navigation.html:468-474` - Checks for `window.currentUser`
- `templates/components/navigation.html:482` - Logout posts to `/auth/logout`

**Issues**:
1. `window.currentUser` not being set by server
2. Username not displaying (using fallback "User")
3. Logout endpoint may not exist or authentication not working

**Fix Estimate**: 30 min
- Ensure all templates pass user context to nav
- Verify `/auth/logout` endpoint exists
- Test authentication flow

---

## MEDIUM SEVERITY ISSUES (P1 Candidates)

### #5: Lists - No Breadcrumb, Label Should Be "Lists" Not "My Lists"
**Category**: Incomplete Implementation
**Root Cause**: UI inconsistency

**Evidence**:
- `templates/lists.html:4` - Title says "My Lists"
- `templates/lists.html:69` - Breadcrumb says "Lists" (correct)
- Navigation says "Lists"

**Fix Estimate**: 2 min - Change title and H1 to "Lists"

---

### #9: Learning - Cosmetic Issues (Dark Mode, Layout)
**Category**: Incomplete Implementation
**Root Cause**: Dark mode fix was applied but may have missed some elements

**Issues Reported**:
- Inappropriate/inconsistent night mode
- Weird icon taking up third of screen
- Boxes reposition themselves

**Fix Estimate**: 30 min
- Review CSS variables application
- Fix icon sizing
- Stabilize layout (check for JavaScript repositioning)

---

### #11: Personality - Layout Issues, Night Mode, Inconsistent Breadcrumb
**Category**: Incomplete Implementation
**Root Cause**: Page not updated with theme fixes

**Issues**:
- Weird layout
- Night mode not working
- Breadcrumb should show "Settings > Personality"

**Evidence**:
- `templates/personality-preferences.html` exists (22KB)
- Already has dark mode fix (commit 24572f82)

**Fix Estimate**: 20 min
- Review layout CSS
- Add proper breadcrumb
- Verify theme variables

---

### #12: Settings/Privacy - Better Messaging Needed
**Category**: Product Decision
**Root Cause**: "Coming Soon" page needs better interim messaging

**User Ask**: "What is safe, private, link to policies? When are we making a UI?"

**Fix Estimate**: 15 min
- Write clear interim message
- Explain current data handling
- Link to privacy policy (if exists)
- Set expectations for alpha

---

## LOW SEVERITY ISSUES (P2 - Backlog)

### #1: Home Page - Add Menu/Help Shortcut
**Category**: Feature Request
**Root Cause**: Not requested in original work

**Fix Estimate**: 10 min - Add help link to shortcuts section

---

### #2: Home Page - Old Doc Upload UI Still Present
**Category**: Product Decision
**Root Cause**: Need to discuss if old UI should be removed

**Fix Estimate**: TBD - Requires PM decision

---

### #3: Standup - Breadcrumb Cropped by Box Below
**Category**: CSS Issue
**Root Cause**: Layout overlap

**Fix Estimate**: 10 min - Fix CSS z-index or margins

---

### #10: Settings - Not on Same Grid as Other Pages
**Category**: Cosmetic
**Root Cause**: Settings page uses different layout

**Fix Estimate**: 15 min - Apply consistent grid layout

---

## Summary by Category

### Category Breakdown
- **Integration Gaps**: 5 issues (#4, #6, #7, #8, #14)
- **Incomplete Implementation**: 5 issues (#5, #7, #9, #11, #12)
- **Product Decisions**: 2 issues (#2, #12)
- **Cosmetic**: 2 issues (#3, #10)
- **Feature Requests**: 1 issue (#1)

### Severity Distribution
- **HIGH (6)**: #4, #6, #7, #8, #13, #14
- **MEDIUM (4)**: #5, #9, #11, #12
- **LOW (4)**: #1, #2, #3, #10

### Estimated Fix Time
- **Quick (<15 min)**: 7 issues
- **Medium (15-30 min)**: 5 issues
- **Longer (30-45 min)**: 2 issues

**Total Estimated Time**: ~3.5 hours for all issues

---

## Recommended P0 Issues for Immediate Fix

### Must-Fix for v0.8.1.1 (Alpha User Experience)

1. **#14 - User Menu (30 min)**: Critical for authentication UX
2. **#6 - Lists Button (15 min)**: Core functionality broken
3. **#7 - Todos Button (20 min)**: Core functionality broken
4. **#8 - Files Page (10 min)**: Feature exists, just needs wiring
5. **#4 - Standup Button (30 min)**: Error handling needed

**Subtotal P0**: ~2 hours

### Can Defer to v0.8.2

- **#13 - Integrations**: More complex, needs proper UI design (45 min)
- All MEDIUM/LOW issues: Polish and product decisions

---

## Root Cause Analysis

**The Classic 75% Pattern**:
1. Features were built (APIs exist, templates exist)
2. Individual pieces work in isolation
3. End-to-end integration was not tested
4. Error handling was not implemented
5. User authentication context not consistently passed

**Lessons**:
- Need E2E manual testing before declaring "done"
- Need error handling for all user-facing actions
- Need consistent authentication context across all pages
- Completion matrices should include "tested in UI" criterion

---

## Next Steps

1. **PM Prioritization**: Review this report and confirm P0 list
2. **Execute P0 Fixes**: ~2 hours of focused work
3. **Test Each Fix**: Manual testing in browser after each fix
4. **Create v0.8.1.1**: Push P0 fixes as patch release
5. **Defer Rest**: Medium/Low issues go to v0.8.2 backlog

---

**Generated**: 2025-11-24 10:47 AM
**By**: Claude Code (Programmer)
**Session**: [2025-11-24-0516-prog-code-log.md](2025-11-24-0516-prog-code-log.md)
