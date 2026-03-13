# Sprint A7 Enhancement Issues (from #218 Testing)

These issues were identified during Issue #218 CORE-USERS-ONBOARD testing and user feedback.

## GitHub Issues Created

✅ **Issue #254**: CORE-UX-QUIET: Quiet Startup Mode for Human-Readable Output
- **URL**: https://github.com/mediajunkie/piper-morgan-product/issues/254
- **Priority**: Medium
- **Effort**: 2 hours
- **Labels**: enhancement, priority: medium, component: ui
- **Milestone**: Alpha

✅ **Issue #255**: CORE-UX-STATUS-USER: Status Checker Should Detect Current User
- **URL**: https://github.com/mediajunkie/piper-morgan-product/issues/255
- **Priority**: Medium
- **Effort**: 3 hours
- **Labels**: enhancement, priority: medium, component: api
- **Milestone**: Alpha

✅ **Issue #256**: CORE-UX-BROWSER: Auto-Launch Browser on Startup
- **URL**: https://github.com/mediajunkie/piper-morgan-product/issues/256
- **Priority**: Low
- **Effort**: 1 hour
- **Labels**: enhancement, priority: low, component: ui
- **Milestone**: Alpha

---

## Summary

**Total Issues**: 3
**Total Estimated Effort**: 6 hours
**Priority Breakdown**:
- High: 0
- Medium: 2
- Low: 1

**All issues added to**:
- ✅ Alpha milestone
- ✅ Sprint A7 (via issue descriptions)

---

## Issue 1: Quiet Startup Mode for Human-Readable Output (#254)

**Priority**: Medium
**Effort**: 2 hours
**Impact**: High (affects daily user experience)

### Problem
Startup output too verbose (~100+ lines of debug logs). Hard to see actionable information.

### Solution
Add quiet mode (default) with `--verbose` flag for debug output.

### Quiet Output Example
```
🚀 Starting Piper Morgan...
   ✓ Services initialized (3/3)
   ✓ LLM providers validated (4/4)
   ✓ Plugins loaded (4/4)
   ⚠ GitHub token not configured

🌐 Server ready at http://localhost:8001
```

### Files to modify
- `main.py` - Flag detection
- `web/app.py` - Conditional logging
- `services/container.py` - Respect quiet mode

---

## Issue 2: Status Checker Should Detect Current User (#255)

**Priority**: Medium
**Effort**: 3 hours
**Impact**: Medium (confusing for new users)

### Problem
Status checker shows first user's API keys (oldest), not current user's (newest from setup).

### Alpha Solution (Quick)
Query most recent user instead of first user:
```python
ORDER BY created_at DESC LIMIT 1
```

### Beta Solution (Full)
- Detect user from JWT token
- Support `--user` flag
- Show username in output

### Files to modify
- `scripts/status_checker.py` - User detection logic

---

## Issue 3: Auto-Launch Browser on Startup (#256)

**Priority**: Low
**Effort**: 1 hour
**Impact**: Low (nice-to-have convenience)

### Problem
Users must manually open browser and navigate to localhost:8001 after startup.

### Solution
Auto-open browser using Python's `webbrowser` module, with `--no-browser` flag to disable.

### Implementation
```python
import webbrowser
asyncio.create_task(open_browser_after_delay())
```

### Edge Cases
- Headless environments (CI/CD) - auto-detect and skip
- Multiple startups - don't open if port busy
- Non-startup commands - don't open for `setup`/`status`

### Files to modify
- `main.py` - Browser launch logic

---

## Recommendation for Sprint A7

**Must Have** (Medium Priority):
1. ✅ Issue #254: Quiet Startup Mode - Affects every user every startup
2. ✅ Issue #255: Status Checker User Detection - Alpha Wave 2 expects this to work

**Nice to Have** (Low Priority):
3. ⚠️ Issue #256: Auto-Launch Browser - Convenience feature, can defer to A8

**Total Effort if all 3**: 6 hours

**Recommended Sprint A7 Scope**: Issues #254 + #255 (5 hours)
- Defer Issue #256 to Sprint A8 or backlog

---

## User Feedback Source

All issues from Issue #218 CORE-USERS-ONBOARD testing (12:41 PM - 12:56 PM, Oct 22, 2025)

PM feedback:
- "should be considered a verbose mode and should be triggered with a flag"
- "did this launch a browser or do I now manually still need to go do that?"
- Status checker showing wrong user's keys

---

## Creation Details

**Created**: Oct 22, 2025 at 1:11 PM
**Created by**: Claude Code (prog-code)
**GitHub Issues**: #254, #255, #256
**Milestone**: Alpha
**Status**: All issues created and ready for Sprint A7 evaluation

---

## Next Steps

- Chief Architect and PM to evaluate for Alpha milestone
- Determine final Sprint A7 scope
- Assign issues to sprint board
- Begin implementation (estimated 5-6 hours total)
