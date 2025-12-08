# November 16, 2025 - Sandbox Debugging Lessons

**Date**: Sunday, November 16, 2025
**Agents**: Cursor (brief check-in), Code Agent Haiku (6.5h debugging in sandbox)
**Duration**: 7:01 AM, 4:46 PM - 11:27 PM (brief morning + 6h 41m evening)
**Context**: Template path debugging from sandbox without testing ability

---

## Timeline

### Morning: Brief Check-In (7:01 AM)

**7:01 AM** - **Cursor** brief session start
- Context: Previous night's 403 home page bug handed to Code Agent
- Status check: User reports all bugs fixed overnight
- Ready to resume UX Tranche 3 testing
- Awaiting confirmation of working UI
- **Session**: Brief check-in only, no substantial work

### Evening: Sandbox Debugging Session (4:46 PM - 11:27 PM)

**4:46 PM** - **Code Agent** (Haiku, sandbox) begins debugging
- Branch: `claude/ux-tranche3-feedback-accessibility-polish-015W99syFQ7b9HrV2WoB9S48`
- Problem: Home page returns 403 error ("couldn't find what you're looking for")
- Context: Polish Sprint/Tranche 3 features added but templates not loading

**5:00 PM** - **Code Agent** Root Cause Analysis #1: Template path issue
- **Discovery**: Component files saved to `web/templates/` instead of `templates/`
- Jinja2Templates configured to look in `templates/` (per CLAUDE.md)
- TemplateNotFound exception → EnhancedErrorMiddleware → user-friendly 403
- Missing files: skip-link.html, page-transition.html, toast.html, session-timeout-modal.html, confirmation-dialog.html

**5:15 PM** - **Code Agent** Fix #1: Move component files
- Moved 10 component files from `web/templates/components/` → `templates/components/`
- **Commit**: afd4439a
- **Status**: ✅ Good fix (proper file location)

**5:30 PM** - **Code Agent** discovers Issue #2: Static files returning 404
- References to `/static/css/` and `/static/js/` in templates
- No mount exists for `/static/` route
- **Hypothesis**: Need to add app.mount("/static", ...)

**5:45 PM** - **Code Agent** Fix #2: Add static mount
- Added `app.mount("/static", StaticFiles(...), name="static")`
- **Commit**: 77499785 (initial mount addition)
- **Status**: ⏳ Untested (sandbox can't run uvicorn)

**6:00 PM** - **Code Agent** discovers Issue #3: Mount ordering
- FastAPI/Starlette require mounts AFTER route handlers
- Mounts were at lines 516-528 (middle of file)
- **Fix**: Moved mounts to end of file (lines 1005-1015)
- **Commit**: 77499785 (mount reordering)
- **Status**: ⏳ Untested

**6:30 PM** - **Code Agent** discovers Issue #4: Relative template path
- Template path "templates" breaks when app runs from `cd web` (per start-piper.sh)
- First attempt: `.parent` on string → AttributeError
- **Fix**: Changed to `os.path.join(os.path.dirname(__file__), "..", "templates")`
- **Commit**: 5f1924de
- **Status**: ⏳ Untested

**7:00 PM** - **User testing**: curl still returns 404 for `/static/` files
- Despite 3 attempted fixes, static files still not serving
- Code Agent unable to test in sandbox (no uvicorn, no dependencies)
- Pattern: Theory-based fixes without validation ability

**8:00 PM** - **Code Agent** completes alpha documentation updates
- Updated ALPHA_QUICKSTART.md to specify `-b production` branch
- Added branch info explaining production (stable) vs main (active development)
- **Commit**: afd1e319 (auto-merged with 4e71d1bf for empty-state.html)
- **Status**: ✅ Good fix (clear documentation)

**9:00 PM** - **Code Agent** reflection and learning
- Recognizes sandbox limitation: Cannot test web server changes
- Violated CLAUDE.md principle: "no guessing" - made 4 theory-based commits
- Should have escalated sooner to IDE-based debugging
- Pattern: TDD impossible in sandbox for web server issues

**11:27 PM** - **Code Agent** session complete
- **Recommendation**: DO NOT MERGE TO MAIN YET
- `/static` mount still broken (untested fixes don't actually work)
- Handoff created: Detailed debug prompt for IDE-based Claude Code
- Branch preserved: 2 good commits + 2 untested commits awaiting proper fix

---

## Executive Summary

### Core Themes

- **Sandbox Limitation Discovery**: Web server debugging requires actual runtime testing
- **Theory vs Practice**: 4 commits made without validation ability → incorrect approach
- **Learning Moment**: Recognizing when to escalate vs continuing blind attempts
- **Proper Handoff**: Detailed diagnostic prompt created for IDE debugging
- **Preservation Strategy**: Branch kept alive with good commits, untested commits to be replaced

### Technical Accomplishments

**Template Path Fix** - ✅ COMPLETE:
- Root cause identified: Component files in wrong directory (web/templates/ vs templates/)
- 10 component files moved to correct location
- Commit: afd4439a
- Status: Verified good fix

**Alpha Documentation** - ✅ COMPLETE:
- Updated ALPHA_QUICKSTART.md to specify `-b production` branch explicitly
- Added clear explanation: production = stable, main = active development
- Ensures alpha testers get working code
- Commit: afd1e319
- Status: Verified good fix

**Static Mount Debugging** - ⏳ INCOMPLETE:
- Attempted 3 different fixes:
  1. Added `/static` mount (Commit: 77499785)
  2. Moved mounts to end of file (Commit: 77499785)
  3. Made template path absolute (Commit: 5f1924de)
- All 3 fixes untested (sandbox limitation)
- User testing confirmed still returning 404
- Requires IDE-based debugging with actual server

### Impact Measurement

- **Commits**: 4 total (2 good, 2 untested)
- **Time spent**: 6.5 hours debugging
- **Dead ends**: ~4 hours on theory-based fixes without testing
- **Root causes found**: 3 (template location, mount ordering, path resolution)
- **Issues remaining**: 1 major (/static mount returning 404)
- **Documentation created**: Debug prompt for IDE handoff
- **Branch status**: Preserved (not merged), awaiting proper fix

### Session Learnings

- **Sandbox Unsuitability**: Cannot debug web server issues without runtime environment
- **TDD Requirement**: Test-Driven Development impossible when testing capability absent
- **Escalation Timing**: Should have stopped after first untested commit and escalated
- **Theory Trap**: Making multiple commits based on theory = time waste when can't validate
- **Handoff Quality**: Creating detailed diagnostic prompt for next session = good practice
- **Commit Discipline**: 4 commits without validation violated CLAUDE.md "no guessing" principle
- **Learning Recognition**: Agent acknowledged mistake pattern and documented better approach
- **Preservation Value**: Keeping branch alive preserves good work while fixing bad
- **Context Switching**: IDE debugging vs sandbox debugging require different approaches

---

## Strategic Decision Points

### Continue Debugging vs Escalate (9:00 PM)

**Context**: After 4 hours and 4 commits, `/static` mount still returning 404

**Options Considered**:
1. **Continue in sandbox**: Make more theory-based fixes
2. **Escalate to IDE**: Hand off to environment with testing capability

**Decision**: Escalate with detailed handoff prompt
- Recognized sandbox limitation (cannot run uvicorn)
- Acknowledged violation of "no guessing" principle
- Created comprehensive debug prompt for IDE-based Claude Code
- Recommended DO NOT MERGE until properly fixed

**Rationale**:
- Further sandbox attempts would waste time
- IDE environment can test immediately (verify each fix)
- Detailed prompt preserves context and hypotheses
- Better to admit limitation than continue guessing

**Impact**: Prevented additional wasted commits, proper handoff created, context preserved for successful debugging

### Branch Preservation vs Rollback (11:27 PM)

**Context**: Branch has 2 good commits + 2 untested commits

**Options Considered**:
1. **Rollback untested commits**: Keep only afd4439a and afd1e319
2. **Delete branch**: Start fresh
3. **Preserve entire branch**: Keep all work, fix in place

**Decision**: Preserve entire branch, clearly document status
- 2 commits definitely good (template moves, documentation)
- 2 commits untested but contain useful investigation
- Branch provides context for IDE debugging
- Recommends NOT merging to main until fixed

**Rationale**:
- Good commits shouldn't be lost
- Investigation commits show thinking process (helpful for debugging)
- Branch structure preserved for when fix is found
- Clear status prevents premature merge

**Impact**: Preserved 6.5 hours of work, maintained context, prevented broken code merge to main

---

## Context Notes

**UX Tranche 3 Status**: ⏸️ BLOCKED BY /STATIC MOUNT ISSUE
- Track A (Advanced Feedback): 3 features complete, code verified
- Track B (Accessibility): 4 features complete, code verified
- Track C (Micro-Interactions): 3 features complete, code verified
- Total: 10 features implemented, 27 files created
- Blocker: Static CSS/JS files not serving (modals invisible, transitions broken)

**Branch Status**: `claude/ux-tranche3-feedback-accessibility-polish-015W99syFQ7b9HrV2WoB9S48`
- **Do not merge to main yet** (explicitly recommended)
- 4 commits present (2 good, 2 untested)
- Awaiting IDE-based `/static` mount fix
- Once fixed: Merge to main → main to production for Monday alpha

**Alpha Launch Preparation**: ⏸️ BLOCKED
- Monday alpha launch planned
- Alpha documentation updated (✅ good)
- UX features need `/static` mount working
- Deployment checklist:
  - [ ] /static mount working (CSS/JS loading)
  - [ ] Modals hidden by default
  - [ ] Polish Sprint/Tranche 3 features tested
  - [ ] main → production merge complete

**Agent Coordination**:
- **Cursor** (Sonnet 4.5): Brief morning check-in (7:01 AM, <5 min)
- **Code Agent** (Haiku): Sandbox debugging session (4:46 PM - 11:27 PM, 6h 41m)

**Sandbox Limitations Identified**:
- Cannot run uvicorn (missing dependencies)
- Cannot test FastAPI routes/mounts
- Cannot validate web server configuration changes
- TDD impossible for web framework issues
- Theory-based fixes unreliable without runtime testing

**Human Story**:
- Sunday work session (weekend debugging)
- Code Agent in sandbox attempting fixes without testing ability
- User patiently testing each attempted fix (4 iterations)
- Agent eventually recognizes futility and escalates properly
- Handoff created for Monday IDE-based debugging
- "Ready for handoff to Claude Code in IDE for /static debugging"

**Quality Discipline**:
- Sandbox agent recognized CLAUDE.md violation ("no guessing")
- Self-documented mistake pattern and better approach
- Created detailed diagnostic prompt for next session
- Explicit recommendation: DO NOT MERGE until fixed
- Learning captured: "What worked" vs "What didn't work"

**Architecture Insights**:
- Jinja2Templates path resolution depends on working directory
- FastAPI/Starlette mount ordering matters (after routes, not before)
- StaticFiles mount requires correct path resolution from web/ subdirectory
- Template includes vs static file serving = different systems (both need fixing)
- start-piper.sh runs from `cd web` affecting path resolution

---

**Source Logs**:
- `dev/2025/11/16/2025-11-16-0701-prog-cursor-log.md` (78 lines) - Brief morning check-in
- `dev/2025/11/16/2025-11-16-2327-prog-code-log.md` (204 lines) - Evening sandbox debugging

**Total Source Material**: 282 lines compressed to Standard Day format

**Final Status**: Template path fixed (good), alpha documentation updated (good), /static mount debugging incomplete (requires IDE), branch preserved awaiting proper fix, Monday alpha launch blocked pending /static resolution
