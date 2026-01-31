# Omnibus Log: January 28, 2026

**Synthesized**: January 29, 2026
**Source Logs**: 4
**Day Rating**: MIXED-DAY (Release Polish + Alpha Testing Reality Check)

---

## Day Overview

A day of two halves: morning focused on documentation polish and release communication, afternoon revealed significant bugs during alpha testing. The v0.8.5 release notes went out to testers, but real-world testing exposed 11 bugs including a P0 (projects never save to database).

### Source Logs

| Time | Role | Duration | Lines | Focus |
|------|------|----------|-------|-------|
| 6:30 AM | Chief of Staff | ~1.5 hrs | 119 | Morning check-in, day planning |
| 6:44 AM | Docs Management | ~6 hrs | 140 | Omnibus, alpha docs audit, roster |
| 6:53 AM | Communications | ~40 min | 91 | Editorial planning, 5 drafts |
| 4:46 PM | Lead Developer | ~4 hrs | 379 | Bug triage, 11 issues, 10 fixes |

---

## Key Accomplishments

### 1. Alpha Documentation Ship-Ready

**Comprehensive audit completed** (Docs agent, 8:53 AM - 12:00 PM):
- Audited all 9 alpha-facing documents
- Found 13 categories of issues (4 critical, 5 important, 4 minor)
- Fixed all issues across 7 files
- Consolidated duplicate email templates into single canonical version
- Added "Returning Tester? Start Here" navigation to Testing Guide
- Updated test counts (602 → 5253), Python versions (3.9 → 3.11/3.12), branch names (main → production)

**Release runbook upgraded** (v1.4 → v1.5):
- Added Content Accuracy Audit section (goes beyond version number grep)
- Captures lessons learned: test counts, feature claims, screenshots

**Alpha tester roster created** (`dev/alpha/alpha-tester-roster.md`):
- 7 active cohort members (3 unblocked by 0.8.5)
- 8 interested prospects
- Status definitions for consistency

**PM sent release notes to testers at 11:59 AM.**

### 2. Communications Pipeline Loaded

**5 new drafts created** (Comms agent, ~40 min session):

| Piece | Type | Status |
|-------|------|--------|
| The Planning Caucus v2 | Narrative | Published to Medium |
| The CLAUDE.md Paradox | Narrative | Draft complete |
| Does the User Notice? | Narrative | Draft complete |
| The Cathedral Release | Narrative | Draft complete |
| Grammar as Decision Tool | Insight | Draft complete |
| The Paradox of Detail | Insight | Draft complete |

Publication sequence established with chained footers.

### 3. Alpha Testing Reality Check (P0 Bug Found)

**PM conducted E2E alpha testing** (4:46 PM - 8:35 PM):

11 bugs discovered and filed (#720-730):

| Issue | Title | Priority | Root Cause Found |
|-------|-------|----------|------------------|
| #728 | Portfolio never saves projects to DB | **P0** | ✅ No DB write in handler |
| #720 | Race condition on first load | P1 | Partial |
| #723 | Logout not working | P1 | ✅ JWTService missing blacklist |
| #724 | LLM API keys storage mismatch | P1 | ✅ Five Whys complete |
| #725 | Chat refresh doesn't show messages | P1 | Regression from #583 |
| #721 | Setup wizard unstyled | P2 | ✅ tokens.css not included |
| #726 | Sidebar not showing current chat | P2 | Regression |
| #729 | History button does nothing | P2 | ✅ Component not included |
| #722 | First-time user → login not setup | P3 | ✅ Exception handler |
| #727 | Text input triggers autofill | P3 | Missing autocomplete |
| #730 | Username shows email prefix | P3 | ✅ JWT missing username |

**Critical finding (#728)**: Portfolio onboarding has NEVER worked correctly. The conversation captures project names, Piper says "I've added them to your portfolio", but **no code ever writes to the database**. This is a fundamental feature gap, not a regression.

**10 of 11 fixes applied**, all tests passing (5253 passed, 24 skipped).

---

## GitHub Activity

### Issues Closed: 8

MUX-IMPLEMENT completion (carried over from Jan 27 release):
- #403: MUX-IMPLEMENT: UI Polish (super epic)
- #428: MUX-IMPLEMENT-ARIA: ARIA labels
- #429: MUX-IMPLEMENT-CONTRAST-TESTS: Contrast testing
- #430: MUX-IMPLEMENT-THEME-CONSISTENCY: Theme consistency
- #685: MUX-LIFECYCLE-OBJECTS: Define lifecycle tracking
- #710: MUX-WORKITEMS-VIEW: Create Work Items View
- #711: MUX-PROJECT-DETAIL-VIEW: Create Project Detail View
- #718: BUG: lifecycle_state columns missing

### Issues Created: 12

- #719: INFRA: RouterInitializer.ROUTERS list is dead code
- #720-730: Alpha testing bugs (11 issues, see table above)

---

## Patterns & Observations

### "The 75% Pattern" Strikes Again

**#728 (projects never save)** is a textbook example of the 75% pattern:
- UI flow works perfectly
- Conversation captures data correctly
- Success message displayed to user
- **But the final persistence step was never implemented**

This bug survived because:
1. No integration test verifies projects appear in database after onboarding
2. Manual testing never checked the projects page after onboarding
3. The conversation makes it *look* complete

**Lesson**: "Conversation says X happened" ≠ "X actually happened in database"

### Multi-User Isolation Gaps

Two bugs (#724, #728) revealed incomplete multi-user support:
- API keys stored with user prefix but retrieved without it
- Projects captured in session but never persisted per-user

The Oct 2025 multi-user commit was incomplete — storage side updated, retrieval side forgotten.

### Alpha Testing Value

11 bugs in one afternoon. Real user flows exposed what unit tests couldn't:
- Screenshot evidence drove investigations
- Fresh environment revealed configuration assumptions
- E2E paths exposed missing component includes

---

## Cross-Session Threads

### Chief of Staff Morning Planning

**Today's priorities set**:
1. Send v0.8.5 release notes ✅
2. Start E2E alpha testing ✅ (found 11 bugs)
3. Cindy Chastain call (2pm PT)
4. Ted Nadeau meeting

### Comms Gap Filled

Jan 20-27 had no drafted narratives. Now have:
- 3 narrative pieces drafted
- 2 insight pieces drafted
- Publication sequence established

---

## Files Changed

### Created
- `docs/omnibus-logs/2026-01-27-omnibus-log.md`
- `dev/2026/01/28/alpha-docs-audit-report.md`
- `dev/alpha/alpha-tester-roster.md`
- 5 draft articles in `docs/public/comms/drafts/`

### Modified (Alpha Docs)
- `docs/ALPHA_QUICKSTART.md` - Version refs, test counts
- `docs/ALPHA_TESTING_GUIDE.md` - Navigation, What's New
- `docs/ALPHA_KNOWN_ISSUES.md` - 0.8.5 sections, beta preview
- `docs/ALPHA_AGREEMENT_v2.md` - Python version
- `docs/releases/RELEASE-NOTES-v0.8.5.md` - Branch name
- `docs/operations/alpha-onboarding/email-template.md` - Version

### Modified (Bug Fixes)
- `templates/setup.html` - Added tokens.css (#721)
- `templates/login.html` - Added tokens.css (#721)
- `templates/home.html` - Include history sidebar (#729)
- `templates/components/chat-inline.html` - autocomplete off (#727)
- `templates/components/chat-widget.html` - autocomplete off (#727)
- `web/app.py` - AuthContainer for blacklist (#723)
- `web/api/routes/auth.py` - Cookie clear, username in JWT (#723, #730)
- `web/api/routes/ui.py` - Setup redirect on error (#722)
- `web/api/routes/setup.py` - Global key storage (#724)
- `services/auth/jwt_service.py` - Username field (#730)
- `services/database/repositories.py` - last_activity_at (#726)
- `services/process/adapters.py` - captured_projects context (#728)

### Deleted
- `docs/alpha/templates/alpha-tester-email-template.md` (duplicate)

### Runbook Updated
- `docs/internal/operations/release-runbook.md` (v1.4 → v1.5)

---

## Metrics

| Metric | Value |
|--------|-------|
| Issues Closed | 8 |
| Issues Created | 12 |
| Files Modified | 20+ |
| Bug Fixes Applied | 10 |
| Test Suite | 5253 passed, 24 skipped |
| Drafts Created | 5 |
| Alpha Docs Fixed | 7 |

---

## Tomorrow's Focus

1. **Retest bug fixes** - PM to verify #720-730 fixes in alpha environment
2. **#728 verification** - Confirm projects actually persist after onboarding
3. **Continue alpha testing** - More E2E flows to validate
4. **PPM roadmap review** - Before MVP super epics (flexible timing)

---

*Day rating: MIXED-DAY — morning polish succeeded, afternoon revealed depth of work remaining. The P0 bug finding demonstrates alpha testing value.*
