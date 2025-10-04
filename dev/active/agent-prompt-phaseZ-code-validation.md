# Claude Code Agent Prompt: GREAT-3C Phase Z - Comprehensive Validation

## Session Log Management
Continue session log: `dev/2025/10/04/2025-10-04-[timestamp]-code-log.md`

Update with timestamped entries for Phase Z work.

## Mission
**Comprehensive Validation**: Test all acceptance criteria, run full regression suite, validate demo plugin integration, verify documentation accuracy, and prepare completion artifacts.

## Context

**GREAT-3C Phases 0-4 Complete**:
- Phase 1: Pattern documentation with Mermaid diagrams
- Phase 2: Developer guide (497 lines)
- Phase 3: Demo plugin implementation (5 files, 380 lines)
- Phase 4: Documentation integration + versioning policy

**Phase Z Goal**: Validate everything works, tests pass, documentation is accurate, and acceptance criteria met.

## Your Tasks

### Task 1: Regression Testing - Existing Plugins

**Verify no regressions from GREAT-3A/3B work**:

```bash
cd ~/Development/piper-morgan

# Run full plugin test suite
PYTHONPATH=. python3 -m pytest tests/plugins/ -v

# Expected: 48/48 tests passing (baseline from GREAT-3B)
```

**Document**:
- Total tests executed
- Pass/fail count
- Any warnings or failures
- Comparison to GREAT-3B baseline (48 tests)

**If any tests fail**: Flag for Phase 3 revision.

### Task 2: Demo Plugin Unit Tests

**Run demo plugin test suite**:

```bash
# Run demo plugin tests
PYTHONPATH=. python3 -m pytest services/integrations/demo/tests/ -v
```

**Expected**: 9/9 tests passing

**Document**:
- Test count
- Pass/fail status
- Execution time
- Any warnings

**If tests fail**: Phase 3 needs revision.

### Task 3: Demo Plugin Integration Test

**Test demo plugin in running application**:

```bash
# Start application in background
python3 main.py &
APP_PID=$!

# Wait for startup
sleep 3

# Test health endpoint
echo "Testing /health endpoint..."
curl -s http://localhost:8001/api/integrations/demo/health | python3 -m json.tool

# Test echo endpoint
echo "Testing /echo endpoint..."
curl -s "http://localhost:8001/api/integrations/demo/echo?message=Hello+World" | python3 -m json.tool

# Test status endpoint
echo "Testing /status endpoint..."
curl -s http://localhost:8001/api/integrations/demo/status | python3 -m json.tool

# Cleanup
kill $APP_PID
```

**Verify each endpoint returns**:
- Valid JSON
- Expected fields
- No errors

**Document**:
- Each endpoint's response
- HTTP status codes
- Any errors or issues

**If integration test fails**: Phase 3 needs revision.

### Task 4: Full Test Suite Run

**Run complete test suite**:

```bash
# Run all tests
PYTHONPATH=. python3 -m pytest tests/ -v

# Get summary
PYTHONPATH=. python3 -m pytest tests/ --tb=short
```

**Document**:
- Total test count
- Pass/fail breakdown
- Any new failures vs GREAT-3B baseline
- Execution time

### Task 5: Documentation Validation

**Check all documentation files exist**:

```bash
# Pattern documentation
ls -la docs/architecture/patterns/plugin-wrapper-pattern.md

# Developer guides
ls -la docs/guides/plugin-development-guide.md
ls -la docs/guides/plugin-versioning-policy.md
ls -la docs/guides/plugin-quick-reference.md

# Demo plugin
ls -la services/integrations/demo/*.py

# Navigation
ls -la docs/NAVIGATION.md
```

**Verify file sizes reasonable**:
```bash
wc -l docs/architecture/patterns/plugin-wrapper-pattern.md
wc -l docs/guides/plugin-development-guide.md
wc -l docs/guides/plugin-versioning-policy.md
wc -l docs/guides/plugin-quick-reference.md
```

**Expected**:
- Pattern doc: ~189 lines
- Developer guide: ~497 lines
- Versioning policy: ~202 lines
- Quick reference: ~85 lines

### Task 6: Verify Acceptance Criteria

**From GREAT-3C.md**:

```markdown
## GREAT-3C Acceptance Criteria Verification

- [ ] Wrapper pattern documented as intentional architecture
  * Status:
  * Evidence: docs/architecture/patterns/plugin-wrapper-pattern.md exists

- [ ] Developer guide complete with examples
  * Status:
  * Evidence: docs/guides/plugin-development-guide.md with 8-step tutorial

- [ ] Template plugin created and tested
  * Status:
  * Evidence: services/integrations/demo/ with 9/9 tests passing

- [ ] All 4 existing plugins have version metadata
  * Status:
  * Evidence: grep "version" services/integrations/*/[!test]*_plugin.py

- [ ] Architecture diagram shows plugin-router relationship
  * Status:
  * Evidence: Mermaid diagrams in services/plugins/README.md

- [ ] Migration path documented for future
  * Status:
  * Evidence: Migration section in plugin-wrapper-pattern.md
```

**For each criterion**:
1. Check if met
2. Provide file/line evidence
3. Mark ✅ or ❌

### Task 7: Plugin Version Verification

**Verify all plugins have version metadata**:

```bash
# Check all plugins for version
grep -n "version=" services/integrations/*/[!test]*_plugin.py
```

**Expected output**:
- calendar_plugin.py: version="1.0.0"
- github_plugin.py: version="1.0.0"
- notion_plugin.py: version="1.0.0"
- slack_plugin.py: version="1.0.0"
- demo_plugin.py: version="1.0.0"

### Task 8: Documentation Cross-Reference Check

**Verify key cross-references exist**:

```bash
# Pattern doc links to developer guide
grep -i "developer guide" docs/architecture/patterns/plugin-wrapper-pattern.md

# Developer guide links to pattern doc
grep -i "wrapper pattern" docs/guides/plugin-development-guide.md

# Developer guide references demo plugin
grep -i "demo" docs/guides/plugin-development-guide.md

# README links to docs
grep -i "docs/" services/plugins/README.md

# Navigation has all entries
grep -i "plugin" docs/NAVIGATION.md
```

### Task 9: Create Completion Summary

**File**: `dev/2025/10/04/GREAT-3C-COMPLETION-SUMMARY.md`

```markdown
# GREAT-3C Completion Summary

**Date**: October 4, 2025
**Epic**: GREAT-3C - Plugin Pattern Documentation & Enhancement
**Status**: ✅ COMPLETE

## Executive Summary

[2-3 sentence summary of accomplishments]

## Phases Completed

### Phase 0: Investigation (21 min)
- Both agents
- Key finding: [summary]

### Phase 1: Pattern Documentation (8 min)
- Cursor agent
- Deliverable: plugin-wrapper-pattern.md + Mermaid diagrams

### Phase 2: Developer Guide (9 min)
- Cursor agent
- Deliverable: 497-line step-by-step tutorial

### Phase 3: Demo Plugin (8 min)
- Code agent
- Deliverable: 5 files, 380 lines, 9/9 tests passing

### Phase 4: Documentation Integration (13 min)
- Cursor agent
- Deliverables: Versioning policy + quick reference + cross-linking

## Final Metrics

**Documentation Created**:
- Files Created: [count]
- Total Lines: [count]
- Cross-References: [count]

**Code Created**:
- Demo Plugin Files: 5
- Demo Plugin Lines: 380
- Test Coverage: 9 unit tests

**Test Results**:
- Regression Tests: 48/48 passing
- Demo Tests: 9/9 passing
- Integration Tests: 3/3 endpoints working
- Full Suite: [count] passing

**Documentation Files**:
- Pattern documentation: 1
- Developer guides: 3
- Updated files: 3

## Acceptance Criteria

[Copy verification from Task 6]

## Documentation Quality

- [ ] All files created
- [ ] Cross-references working
- [ ] Code examples tested
- [ ] Navigation updated

## Testing Summary

- [ ] No regressions
- [ ] Demo plugin works
- [ ] Integration tests pass
- [ ] Full suite green

## Next Steps

GREAT-3C complete. Ready for:
- GREAT-3D (if exists)
- Other work as directed

---

*Prepared by: Code Agent*
*Date: October 4, 2025*
```

### Task 10: Session Log Finalization

**Review your session log**:
- All phases documented?
- Timestamps accurate?
- Deliverables listed?

**Add final entries**:
- Phase Z completion time
- Total session duration
- Final test results
- Completion summary location

## Deliverable

Create: `dev/2025/10/04/phase-z-code-validation.md`

Include:
1. **Regression Test Results**: 48/48 tests status
2. **Demo Plugin Tests**: 9/9 tests status
3. **Integration Tests**: 3 endpoint results with response samples
4. **Full Suite Results**: Complete test execution summary
5. **Documentation Validation**: All files exist and verified
6. **Acceptance Criteria**: Complete verification with evidence
7. **Version Verification**: All 5 plugins have version metadata
8. **Cross-Reference Check**: All links verified
9. **Completion Summary**: Location and summary stats

## Success Criteria
- [ ] All regression tests passing (48/48)
- [ ] Demo plugin tests passing (9/9)
- [ ] Integration tests successful (3/3 endpoints)
- [ ] All documentation files exist
- [ ] All acceptance criteria met with evidence
- [ ] Version metadata verified on all plugins
- [ ] Cross-references validated
- [ ] Completion summary created
- [ ] Session log finalized
- [ ] Ready for git commit

## Important Notes

**If ANY tests fail**:
1. Document the failure clearly
2. Flag need for Phase 3 revision
3. Do NOT proceed with completion summary
4. Report to PM for decision

**Phase Z is the quality gate - be thorough.**

---

**Deploy at 2:18 PM**
**Final validation before GREAT-3C completion**
