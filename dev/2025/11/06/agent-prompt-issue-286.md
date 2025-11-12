# Claude Code Prompt: Issue #286 - CONVERSATION Handler Architecture Fix

## Your Identity
You are Claude Code, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

## Essential Context
Read these briefing documents first:
- `docs/briefing/PROJECT.md` - What Piper Morgan is
- `docs/briefing/BRIEFING-CURRENT-STATE.md` - Current epic and focus
- `docs/briefing/BRIEFING-ESSENTIAL-AGENT.md` - Your role requirements
- `docs/briefing/METHODOLOGY.md` - Inchworm Protocol

---

## Task Overview

**Issue**: #286 - CORE-ALPHA-CONVERSATION-PLACEMENT
**Priority**: P2 - Important (Architecture)
**Estimated Effort**: 2 hours
**Date**: November 6, 2025, 1:42 PM PT

**Problem**: CONVERSATION handler is architecturally misplaced in IntentService at line 199. Should be with other canonical handlers at lines 123-136.

**Goal**: Move handler to proper location, use enum comparison (not string), maintain existing functionality.

---

## Gameplan to Execute

**Source**: `gameplan-286-conversation-handler.md` (attached)

**Phases**:
- **Phase -1**: Verification (15 min) - Verify current state
- **Phase 0**: Setup (10 min) - Branch + baseline tests
- **Phase 1**: Move Handler (30 min) - Relocate to canonical section
- **Phase 2**: Test Impact (45 min) - Verify all tests pass
- **Phase 3**: Verify Architecture (20 min) - Check handler order
- **Phase 4**: Documentation (10 min) - Update comments
- **Phase Z**: Final Validation (15 min) - Complete test suite

**Total Estimated**: 2 hours

---

## Critical Requirements

### 1. Phase -1 MANDATORY
Before making any changes:
- Verify current handler location (line 199 area)
- Check canonical handler section (lines 123-136)
- Verify IntentCategory.CONVERSATION enum exists
- Document line numbers if different from gameplan

**STOP if**:
- Handler already moved
- Line numbers significantly different
- Major architectural changes detected

### 2. Changes Required
1. Move handler from line 199 to canonical section (lines 123-136)
2. Change comparison from `intent.category.value == "conversation"` to `intent.category == IntentCategory.CONVERSATION`
3. Remove old location completely
4. Update code comments

### 3. Testing Requirements
- Run conversation-specific tests
- Run all intent service tests
- Verify no duplicates
- Check performance (<100ms)
- Manual verification

### 4. Evidence Required
- [ ] Before/after line numbers documented
- [ ] Test results (all passing)
- [ ] No duplicate handler calls verified
- [ ] Performance check (<100ms)
- [ ] Git diff showing exact changes

---

## Success Criteria

**Must Achieve**:
- ✅ Handler in canonical section (lines 123-136 area)
- ✅ Uses `IntentCategory.CONVERSATION` enum (not string)
- ✅ Line 199 area no longer has conversation check
- ✅ All existing tests pass
- ✅ Performance maintained (<100ms)
- ✅ Architecture pattern consistent
- ✅ Single commit with clear message

**Test Requirements**:
- All conversation tests passing
- All intent service tests passing
- No regressions in other handlers
- Integration tests passing

---

## Anti-80% Safeguards

### MANDATORY Verification Steps

**Before declaring complete**:
1. Run FULL test suite (not just conversation tests)
2. Verify ZERO duplicate handler calls
3. Check line 199 area is CLEAN (no conversation check remains)
4. Performance test shows <100ms
5. Git diff reviewed (only expected changes)

**Evidence Package Required**:
```bash
# 1. Show handler moved
git diff services/intent_service/intent_service.py

# 2. Show tests passing
pytest tests/intent_service/ -v
pytest tests/integration/ -k conversation -v

# 3. Show no duplicates
grep -n "_handle_conversation_intent" services/intent_service/intent_service.py

# 4. Show performance
# (from test output)
```

---

## Methodology Reminders

### Inchworm Protocol
1. **Verify** current state (Phase -1)
2. **Setup** branch + tests (Phase 0)
3. **Implement** changes systematically (Phase 1)
4. **Test** thoroughly (Phase 2)
5. **Verify** architecture (Phase 3)
6. **Document** (Phase 4)
7. **Validate** completeness (Phase Z)

### Stop Conditions
Stop immediately if:
- Handler already in correct location
- Tests fail after changes
- Duplicates found
- Performance degrades
- Line numbers wildly different from gameplan

---

## Risk Assessment

**Risk Level**: Low ✅
- Simple code move
- No logic changes
- Well-tested area
- Easy to revert

**Mitigation**:
- Run tests at each phase
- Keep changes minimal
- Single purpose commit
- Clear rollback path

---

## Commit Message Template

```
fix(#286): Move CONVERSATION handler to canonical section

- Moved handler from line 199 to canonical section (lines 123-136)
- Changed from string to enum comparison (IntentCategory.CONVERSATION)
- Maintains same functionality with better architecture
- All tests passing (16/16)

Architecture: Canonical handlers now consistently grouped
Performance: No degradation (<100ms maintained)

Fixes #286
```

---

## Session Log Requirements

Create session log: `dev/2025/11/06/2025-11-06-[time]-code-issue-286-log.md`

**Must Include**:
- Start/end timestamps
- Phase completion times
- Test results (with counts)
- Evidence gathered
- Decisions made
- Issues encountered
- Final verification checklist

---

## Deliverables Checklist

Before declaring complete:
- [ ] Phase -1 verification documented
- [ ] Branch created
- [ ] Handler moved to canonical section
- [ ] Enum comparison used (not string)
- [ ] Old location removed
- [ ] All tests passing
- [ ] Performance verified (<100ms)
- [ ] Architecture verified (no duplicates)
- [ ] Code comments updated
- [ ] Session log created
- [ ] Commit made with proper message
- [ ] Evidence package complete

---

## Communication

**When complete**, provide PM with:
1. Session log link
2. Test results summary
3. Git commit hash
4. Evidence of completion
5. Any issues encountered

**If blocked**, notify immediately with:
- What you tried
- What failed
- Current state
- Recommendation

---

## Resources

**Gameplan**: `gameplan-286-conversation-handler.md`
**Template**: agent-prompt-template.md v10.2
**Methodology**: Inchworm Protocol (Phase -1 through Phase Z)

---

**Ready to Execute**: Follow gameplan phases systematically, gather evidence at each step, create comprehensive session log.

**Start Time**: November 6, 2025, 1:43 PM PT
**Expected Completion**: ~3:45 PM PT (2 hours)

🏰 **Execute with precision!**
