# Audit: Issue #734 against bug_report_alpha.md

**Issue**: #734 - CRITICAL: Calendar and integration tokens leak between users (multi-tenancy broken)
**Template**: `.github/ISSUE_TEMPLATE/bug_report_alpha.md`
**Auditor**: Lead Developer (Opus)
**Date**: 2026-01-30 11:29 AM

---

## Audit Matrix

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| **Bug Description** | ✅ | Clear: "Calendar data from one user is visible to another user" with specific example |
| **Steps to Reproduce** | ❌ | Missing numbered steps - only scenario described, no actionable reproduction steps |
| **Expected Behavior** | ⚠️ | Implicit in "Verification" section but not explicitly stated |
| **Actual Behavior** | ✅ | Clear: "New alpha user (alfamux) sees calendar event '🐉 Decision Reviews Retro' despite NOT connecting their calendar" |
| **Environment** | ❌ | Missing entirely - no browser, OS, or version info |
| **Screenshots/Logs** | ⚠️ | Code snippets provided but no actual screenshots or runtime logs |
| **Severity** | ✅ | "CRITICAL - Data Privacy Violation" clearly stated |
| **Additional Context** | ✅ | Extensive - root cause, evidence, fix plan, workaround, related issues |

---

## Summary

- ✅ Present: 4/8
- ⚠️ Partial: 2/8
- ❌ Missing: 2/8

---

## Action Required

Before proceeding to gameplan phase, fix the following:

### 1. Add Steps to Reproduce (❌ → ✅)

```markdown
## Steps to Reproduce

1. Log in as User A (e.g., "previoususer")
2. Go to Settings → Integrations → Calendar
3. Connect Google Calendar (OAuth flow)
4. Verify User A sees their calendar events in Piper
5. Log out as User A
6. Log in as User B (e.g., "alfamux") - a fresh user
7. Go to Home or any page that shows calendar
8. Observe: User B sees User A's calendar events despite never connecting calendar
```

### 2. Add Expected Behavior section (⚠️ → ✅)

```markdown
## Expected Behavior

User B (who has not connected their calendar) should see:
- "Calendar not connected" message
- No calendar events from any other user
- Prompt to connect their own calendar
```

### 3. Add Environment section (❌ → ✅)

```markdown
## Environment

- **Browser**: Chrome (version not specified)
- **OS**: macOS (development environment)
- **Piper Morgan Version**: Current main branch (alpha)
- **Database**: PostgreSQL via Docker
```

### 4. Clarify Screenshots/Logs (⚠️ → ✅)

The code snippets are good for root cause, but for alpha testing bug reports, actual screenshots or terminal output showing the leak would strengthen the report. However, given this is a security issue with clear code evidence, this can be marked acceptable.

**PM Decision Needed**: Is the code evidence sufficient, or do we need actual screenshots of the calendar leak?

---

## Audit Result

**Status**: ⚠️ NEEDS FIXES before proceeding to gameplan

**Blocking items**:
1. Steps to Reproduce - Missing
2. Expected Behavior - Not explicit
3. Environment - Missing

**PM Input Needed**:
- Screenshots requirement - acceptable to skip given code evidence?

---

## Next Steps

1. Update issue #734 with missing sections
2. Re-audit to confirm all items ✅
3. Proceed to gameplan phase
