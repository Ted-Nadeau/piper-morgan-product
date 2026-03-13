# Gameplan: CORE-GREAT-1A - QueryRouter Investigation & Fix

**Date**: September 22, 2025
**Issue**: #185 (Part 1 of 3 for CORE-GREAT-1 epic #180)
**Architect**: Claude Opus 4.1
**Lead Developer**: [To be assigned]

---

## Strategic Context: The Great Refactor

### Where We Are
We're beginning the Great Refactor - a systematic completion of partially-built components following our discovery of the "75% pattern" where most features were abandoned at 75% completion.

### CORE-GREAT Sequence
This is CORE-GREAT-1, the first of 5 epics to reach system stability:
1. **CORE-GREAT-1**: Orchestration Core (This epic)
2. **CORE-GREAT-2**: Integration Cleanup
3. **CORE-GREAT-3**: Query Operations
4. **CORE-GREAT-4**: Learning System
5. **CORE-GREAT-5**: Workflow Orchestra

### This Epic's Structure
CORE-GREAT-1 has been decomposed into three sequential issues:
- **#185 GREAT-1A**: QueryRouter Investigation & Fix (THIS GAMEPLAN)
- **#186 GREAT-1B**: Orchestration Connection & Integration
- **#187 GREAT-1C**: Testing, Locking & Documentation

**Critical**: Each issue must be 100% complete before moving to the next (Inchworm Protocol).

---

## Infrastructure Verification Checkpoint

### My Understanding (Based on Architecture Docs)
```yaml
Expected Structure:
- Entry Point: main.py
- Web Framework: FastAPI in web/app.py (933 lines)
- Port: 8001
- Services: services/orchestration/engine.py contains QueryRouter
- Pattern: QueryRouter is commented out with TODO
- Database: PostgreSQL on port 5433
```

### PM Verification Required
Before agents begin, please verify:
```bash
# Verify file structure
ls -la services/orchestration/
ls -la web/

# Verify QueryRouter exists but is disabled
grep -n "QueryRouter" services/orchestration/engine.py
grep -n "TODO.*QueryRouter" services/orchestration/engine.py

# Check if it's just commented out
grep -n "#.*QueryRouter" services/orchestration/engine.py

# Verify current state
curl -X POST http://localhost:8001/api/intent \
  -H "Content-Type: application/json" \
  -d '{"message": "create github issue test"}'
```

**Expected**: QueryRouter exists but is disabled, causing intent operations to fail.

---

## The 75% Pattern Context

QueryRouter represents our first encounter with the 75% pattern:
- **Built**: Class exists, methods implemented
- **Integrated**: Referenced in multiple places
- **Disabled**: Single line commented out
- **Abandoned**: TODO without issue number

This gameplan addresses the pattern by COMPLETING existing work, not replacing it.

---

## Phase 0: GitHub & Pattern Investigation

### Both Agents Together
1. **Verify Issue Exists**
   ```bash
   gh issue view 185
   ```

2. **Find All QueryRouter References**
   ```bash
   grep -r "QueryRouter" . --include="*.py" | grep -v ".pyc"
   find . -name "*.py" -exec grep -l "QueryRouter" {} \;
   ```

3. **Check Git History**
   ```bash
   cd services/orchestration/
   git log -p --follow engine.py | grep -A 5 -B 5 "QueryRouter"
   git blame engine.py | grep "QueryRouter"
   ```

4. **Document Current State**
   - Screenshot/copy the disabled code
   - Note the TODO comment
   - Find when it was disabled
   - Look for related commits

---

## Phase 1: Root Cause Investigation

### Deploy: Both Agents (Different Approaches)

#### Claude Code Instructions
**Broad Investigation Approach**
```markdown
Investigate why QueryRouter was disabled:
1. Search for all error messages mentioning QueryRouter
2. Check test files for failing QueryRouter tests
3. Look for ADRs or docs mentioning QueryRouter issues
4. Search for similar disabled components (pattern check)
5. Check for missing dependencies

Deploy subagents if needed to investigate:
- Database schema issues
- Import/dependency problems
- Session management conflicts
```

#### Cursor Instructions
**Focused File Analysis**
```markdown
In services/orchestration/engine.py:
1. Analyze the commented QueryRouter line
2. Check what initialization it needs
3. Verify all imports are present
4. Check if QueryRouter class is complete
5. Look for exception handling around it

Specific files to check:
- services/orchestration/engine.py
- services/orchestration/query_router.py (if exists)
- tests/test_orchestration.py
```

### STOP Conditions for Investigation
- If QueryRouter class doesn't exist at all
- If it requires missing dependencies
- If the TODO references a different issue number
- If git history shows it never worked

---

## Phase 2: Fix Implementation

### Only After Root Cause Is Known

#### Decision Point
Based on investigation, one of:
1. **Simple Fix**: Uncomment and fix initialization
2. **Dependency Fix**: Add missing imports/services
3. **Logic Fix**: Complete unfinished implementation
4. **Session Fix**: Fix session/context management

#### Both Agents Implement Fix
- Code: Broad changes across files
- Cursor: Specific targeted fixes
- Cross-validate: Different approaches, same goal

### Fix Requirements
- Fix root cause, not symptoms
- No workarounds
- Maintain existing patterns
- Keep performance <500ms target

---

## Phase 3: Verification

### Required Evidence
1. **QueryRouter Initializes**
   ```bash
   python -c "from services.orchestration.engine import OrchestrationEngine; print('Success')"
   ```

2. **No Errors on Startup**
   ```bash
   python main.py
   # Should see: "QueryRouter initialized" in logs
   ```

3. **Existing Tests Pass**
   ```bash
   PYTHONPATH=. python -m pytest tests/test_orchestration.py -xvs
   ```

4. **No Regressions**
   ```bash
   PYTHONPATH=. python -m pytest tests/ -x
   ```

---

## Success Criteria Checklist

Lead Developer must verify:
- [ ] Root cause identified and documented
- [ ] Fix implemented (not workaround)
- [ ] QueryRouter initializes without error
- [ ] All existing tests still pass
- [ ] Git history shows clear fix commit
- [ ] TODO comment updated with issue #185
- [ ] Evidence provided for all above

---

## Handoff to GREAT-1B

After this issue is complete:
1. Update issue #185 with all evidence
2. Close #185 with completion comment
3. Lead Developer proceeds to #186 (GREAT-1B)
4. Same agents continue with context

**Note**: Do not start #186 until #185 is 100% complete with evidence.

---

## STOP Conditions for Entire Gameplan

Stop and escalate if:
- QueryRouter is completely missing (not just disabled)
- Enabling it requires architectural changes beyond this scope
- Performance degrades below acceptable levels
- Critical production features break

---

## Phase Z: Final Bookending & Handoff

### Purpose
Complete final verification, update all documentation, prepare for PM approval to close #185.

### Required Actions

#### 1. GitHub Final Update
```bash
gh issue edit 185 --body "
## Status: Complete - Awaiting PM Approval

### Evidence Summary
- [x] Root cause identified: [summary]
- [x] Fix implemented: [commit hash]
- [x] QueryRouter initializes: [terminal output]
- [x] Tests passing: [test output]
- [x] No regressions: [full test suite confirmation]

### Investigation Findings
[Document what was discovered about why it was disabled]

### Ready for PM Review
All acceptance criteria met. Evidence provided above.
"
```

#### 2. Documentation Updates
- [ ] Update any misleading TODO comments with issue #185
- [ ] Document the fix approach for future reference
- [ ] Update architecture.md if initialization sequence changed
- [ ] Note in CURRENT-STATE.md that GREAT-1A is complete

#### 3. Evidence Compilation
- [ ] Git diff showing the actual fix
- [ ] Before: Error/disabled state output
- [ ] After: Successful initialization output
- [ ] Test results showing QueryRouter works
- [ ] Confirmation that existing features still work

#### 4. Handoff to GREAT-1B (#186)
Document for next phase:
- [ ] How QueryRouter initializes now
- [ ] Any unexpected discoveries about OrchestrationEngine
- [ ] Any performance considerations found
- [ ] Session context that would help

#### 5. Session Completion
- [ ] Run satisfaction assessment per BRIEFING-METHODOLOGY
- [ ] Update session log with completion status
- [ ] Note any methodology improvements discovered

#### 6. PM Approval Request
```markdown
@xian - Issue #185 (CORE-GREAT-1A) complete and ready for review:
- QueryRouter investigation complete ✓
- Root cause identified and fixed ✓
- Initialization working ✓
- All tests passing ✓
- Evidence in issue description ✓

Please review and close if satisfied. Ready to proceed to #186 (GREAT-1B).
```

### CRITICAL: Do Not Close Issue
**Agents must NOT close issues. Only PM closes after approval.**

---

## Lead Developer Reminders

1. **Read First**: Check `00-START-HERE-LEAD-DEV.md` in knowledge
2. **Deploy Both**: Use both Code and Cursor by default
3. **Evidence Required**: No claims without proof
4. **Update GitHub**: Use issue description checkboxes
5. **75% Pattern**: Complete what exists, don't replace

---

## Final Note on Epic Completion

Once all three issues (#185, #186, #187) are complete:
- Lead Developer verifies parent epic #180
- North Star test must work: "Create GitHub issue through chat"
- All evidence compiled in epic #180
- Then and only then, move to CORE-GREAT-2

---

*Remember: We complete things. That's what makes this The Great Refactor.*
