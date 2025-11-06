# Cursor Agent Prompt: Issue #287 - Temporal/Response Rendering Fixes

## Your Identity
You are Cursor, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

## Essential Context
Read these briefing documents first:
- `docs/briefing/PROJECT.md` - What Piper Morgan is
- `docs/briefing/BRIEFING-CURRENT-STATE.md` - Current epic and focus
- `docs/briefing/BRIEFING-ESSENTIAL-AGENT.md` - Your role requirements
- `docs/briefing/METHODOLOGY.md` - Inchworm Protocol

---

## Task Overview

**Issue**: #287 - CORE-ALPHA-TEMPORAL-BUGS
**Priority**: P2 - Important (UX)
**Estimated Effort**: 2 hours
**Date**: November 6, 2025, 1:43 PM PT

**Problems**: Response rendering has three UX issues:
1. Shows "Los Angeles" instead of "PT" for timezone
2. Displays contradictory meeting status messages
3. Doesn't validate calendar data freshness

**Goal**: Fix timezone display, prevent contradictions, add validation. Improve user trust and clarity in time-sensitive responses.

---

## Gameplan to Execute

**Source**: `gameplan-287-temporal-rendering.md` (attached)

**Phases**:
- **Phase -1**: Investigation (20 min) - Find affected files
- **Phase 0**: Setup (10 min) - Branch + test-first approach
- **Phase 1**: Fix Timezone Display (30 min) - Use abbreviations
- **Phase 2**: Fix Contradictory Messages (40 min) - Prevent conflicts
- **Phase 3**: Add Calendar Validation (30 min) - Freshness checks
- **Phase 4**: Integration Testing (20 min) - Test all fixes together
- **Phase Z**: Polish & PR (10 min) - Final verification

**Total Estimated**: 2 hours

---

## Critical Requirements

### 1. Phase -1 Investigation MANDATORY
Before implementing:
- Find all timezone display locations
- Find meeting status rendering code
- Find calendar integration points
- Document current behavior (screenshots/examples)

**Expected Locations**:
- `services/ui_messages/response_formatter.py`
- `services/integrations/calendar_service.py`
- `services/analysis/temporal_analyzer.py`

**STOP if**:
- Files don't exist as expected
- Already fixed
- Major refactor needed

### 2. Test-First Approach REQUIRED
Create tests BEFORE fixes:
```python
# tests/ui_messages/test_timezone_display.py
def test_timezone_abbreviation_display()
def test_contradictory_messages_prevented()
```

### 3. Three Fixes Required

**Fix 1: Timezone Abbreviations**
- Create timezone mapping (America/Los_Angeles → PT)
- Update all display points
- Support US + international timezones

**Fix 2: No Contradictions**
- Prevent "no meetings" + "you have meetings"
- Use if/elif/else properly (no code after)
- Add assertion guards

**Fix 3: Calendar Validation**
- Check data freshness (15 min threshold)
- Show confidence indicators
- Add retry logic

### 4. Evidence Required
- [ ] Before/after examples documented
- [ ] Test results (all passing)
- [ ] Manual testing checklist completed
- [ ] No regressions verified
- [ ] Screenshots of fixed UX

---

## Success Criteria

**Must Achieve**:
- ✅ Timezones show as abbreviations (PT, ET, etc.)
- ✅ No contradictory messages about meetings
- ✅ Calendar data freshness validated
- ✅ Users see confidence indicators
- ✅ All tests pass
- ✅ Better UX for time-sensitive information

**Test Requirements**:
- Timezone abbreviation tests passing
- Contradiction prevention tests passing
- Calendar validation tests passing
- Integration tests passing
- Manual verification complete

---

## Anti-80% Safeguards

### MANDATORY Verification Steps

**Before declaring complete**:
1. Test ALL three fixes together (integration)
2. Verify NO "Los Angeles" remains in any output
3. Test edge cases (0 meetings, multiple meetings, stale data)
4. Manual testing checklist 100% complete
5. Check for any other timezone display locations

**Manual Testing Checklist** (MUST complete):
- [ ] Check timezone displays as "PT" not "Los Angeles"
- [ ] Verify no contradictory messages with 0 meetings
- [ ] Verify no contradictory messages with multiple meetings
- [ ] Test stale data shows warning
- [ ] Test fresh data shows no warning
- [ ] Test all US timezones (PT, MT, CT, ET)
- [ ] Test international timezones (GMT, JST, etc.)

**Evidence Package Required**:
```bash
# 1. Show tests passing
pytest tests/ui_messages/test_timezone_display.py -v
pytest tests/ui_messages/test_meeting_formatter.py -v
pytest tests/integration/test_temporal_rendering_fixes.py -v

# 2. Show no "Los Angeles" remains
grep -r "Los Angeles" services/ --include="*.py"
# Should return 0 results

# 3. Manual test results
# Document in session log with examples
```

---

## Methodology Reminders

### Inchworm Protocol
1. **Investigate** affected files (Phase -1)
2. **Setup** branch + tests (Phase 0)
3. **Implement** timezone fix (Phase 1)
4. **Implement** contradiction fix (Phase 2)
5. **Implement** validation (Phase 3)
6. **Test** integration (Phase 4)
7. **Validate** completeness (Phase Z)

### Stop Conditions
Stop immediately if:
- Expected files don't exist
- Already fixed
- Tests reveal unexpected issues
- Calendar service unavailable
- Breaking changes required

---

## Risk Assessment

**Risk Level**: Low-Medium ⚠️
- UI changes visible to users
- Multiple touchpoints affected
- Calendar integration complexity

**Mitigation**:
- Comprehensive test coverage
- Fallback for unknown timezones
- Graceful handling of stale data
- Clear warning messages
- Test-first approach

---

## Implementation Details

### Timezone Mapping Structure
```python
TIMEZONE_ABBREVIATIONS = {
    "America/Los_Angeles": "PT",
    "America/New_York": "ET",
    "America/Chicago": "CT",
    "America/Denver": "MT",
    "Europe/London": "GMT",
    "Asia/Tokyo": "JST",
    # ... more
}
```

### Contradiction Prevention Pattern
```python
if meeting_count == 0:
    return "No meetings today."
elif meeting_count == 1:
    return f"One meeting: {meeting.title}"
else:
    return f"{meeting_count} meetings today."
# NO CODE AFTER if/elif/else!
```

### Validation Pattern
```python
validation = CalendarDataValidator.validate_calendar_data(data)
if validation["warnings"]:
    response.append("⚠️ " + ", ".join(validation["warnings"]))
```

---

## Commit Message Template

```
fix(#287): Fix temporal and response rendering issues

- Display timezone abbreviations (PT) instead of full names
- Prevent contradictory meeting status messages
- Add calendar data validation and freshness checks
- Show confidence indicators for stale data

UX Impact:
- "Los Angeles" → "PT" (all timezone displays)
- No contradictory "no meetings" + "you have meetings"
- Users see warnings for stale calendar data

Tests: 15/15 passing
Manual verification: Complete

Fixes #287
```

---

## Session Log Requirements

Create session log: `dev/2025/11/06/2025-11-06-[time]-cursor-issue-287-log.md`

**Must Include**:
- Start/end timestamps
- Phase completion times
- Test results (with counts)
- Manual testing results
- Before/after examples
- Edge cases tested
- Evidence gathered
- Decisions made
- Issues encountered
- Final verification checklist

---

## Deliverables Checklist

Before declaring complete:
- [ ] Phase -1 investigation documented
- [ ] Branch created
- [ ] Tests created (test-first)
- [ ] Timezone mapping created
- [ ] All timezone displays updated
- [ ] Contradiction prevention implemented
- [ ] Calendar validation implemented
- [ ] Integration tests passing
- [ ] Manual testing checklist complete
- [ ] No "Los Angeles" in codebase
- [ ] Session log created
- [ ] Commit made with proper message
- [ ] Evidence package complete

---

## Communication

**When complete**, provide PM with:
1. Session log link
2. Test results summary
3. Manual testing results
4. Before/after examples
5. Git commit hash
6. Evidence of completion
7. Any issues encountered

**If blocked**, notify immediately with:
- What you tried
- What failed
- Current state
- Recommendation

---

## Resources

**Gameplan**: `gameplan-287-temporal-rendering.md`
**Template**: agent-prompt-template.md v10.2
**Methodology**: Inchworm Protocol (Phase -1 through Phase Z)

---

## Special Notes

**UX Focus**: This is user-facing work. Quality matters more than speed.

**Test First**: Create tests before implementation. Verify fixes work.

**Edge Cases**: Test 0 meetings, 1 meeting, many meetings, stale data, fresh data.

**Manual Verification**: Automated tests aren't enough for UX. Actually test the experience.

---

**Ready to Execute**: Follow gameplan phases systematically, test thoroughly, gather comprehensive evidence.

**Start Time**: November 6, 2025, 1:43 PM PT
**Expected Completion**: ~3:45 PM PT (2 hours)

🏰 **Execute with UX excellence!**
