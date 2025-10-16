# Code Agent Prompt: Phase -1 - Quick Verification of Issue #136

**Date**: October 15, 2025, 10:43 AM
**Sprint**: A2 - Notion & Errors  
**Issue**: CORE-NOTN #136 - Refactor Notion hardcoded values
**Phase**: -1 (Quick Verification)
**Duration**: 15 minutes
**Agent**: Code Agent

---

## Mission

Quick verification to determine if Issue #136 is actually complete by checking acceptance criteria against existing evidence from child issues #139, #143, and #141.

**Context**: Issue #136 appears to have been completed through child issues, but never formally closed. We need to verify completion before closing.

**Philosophy**: Trust but verify. Reference existing evidence, don't redo work.

---

## Acceptance Criteria to Verify

From Issue #136 description:

### ✅ Criterion 1: All hardcoded Notion IDs identified and documented

**Evidence Sources**:
- Issue #143 mentions 5 files with hardcoded IDs
- Check: Are there any OTHER hardcoded IDs we missed?

**Verification Steps**:
```bash
# Search for Notion ID patterns (32-character hex strings)
# Look for the known IDs:
grep -r "25d11704d8bf80c8a71ddbe7aba51f55" . --include="*.py" | grep -v __pycache__ | grep -v ".pyc"
grep -r "25e11704d8bf80deaac2f806390fe7da" . --include="*.py" | grep -v __pycache__ | grep -v ".pyc"
grep -r "25d11704d8bf81dfb37acbdc143e6a80" . --include="*.py" | grep -v __pycache__ | grep -v ".pyc"

# Look for any other 32-char hex strings that might be Notion IDs
grep -rE "[0-9a-f]{32}" . --include="*.py" | grep -v __pycache__ | grep -v ".pyc" | grep -v "\.git" | head -20
```

**Expected**: Should find IDs only in:
- config/PIPER.user.md (config file - OK)
- Possibly in tests (if they're test fixtures - OK)
- NOT in production code (services/, cli/commands/)

---

### ✅ Criterion 2: Configuration schema designed and implemented (with ADR-027)

**Evidence Sources**:
- Issue #139 (PM-132) closed - NotionUserConfig implemented
- ADR-027 should exist in docs

**Verification Steps**:
```bash
# Check if NotionUserConfig exists
ls -la config/notion_user_config.py

# Check if ADR-027 exists
find docs -name "*027*" -o -name "*adr-027*"

# Quick check of config schema in PIPER.user.md
grep -A 20 "notion:" config/PIPER.user.md
```

**Expected**:
- ✅ NotionUserConfig class exists
- ✅ ADR-027 documented
- ✅ Schema in PIPER.user.md matches design

---

### ✅ Criterion 3: Code refactored to use configuration

**Evidence Sources**:
- Issue #143 claims 5 files refactored

**Verification Steps**:
```bash
# Check the 5 files mentioned in #143
# Should see config.get_database_id() or config.get_parent_id() calls

# fields.py
grep -n "get_database_id\|get_parent_id" services/integrations/notion/fields.py

# adr.py  
grep -n "get_database_id\|get_parent_id" services/integrations/notion/adr.py

# debug_parent.py
grep -n "get_database_id\|get_parent_id" tests/debug_parent.py

# test_publish_command.py
grep -n "get_database_id\|get_parent_id" tests/publishing/test_publish_command.py

# test_publish_gaps.py
grep -n "get_database_id\|get_parent_id" tests/integration/test_publish_gaps.py
```

**Expected**: Each file should have config lookups, not hardcoded IDs

---

### ✅ Criterion 4: Backward compatibility maintained

**Evidence Sources**:
- Issue #143 mentions "fallback logic implemented"

**Verification Steps**:
```bash
# Check NotionUserConfig for fallback logic
grep -A 10 -B 5 "fallback\|default" config/notion_user_config.py | head -30
```

**Expected**: Some kind of fallback or default handling

---

### ✅ Criterion 5: Documentation updated

**Evidence Sources**:
- Issue #141 mentions config/README.md and migration docs

**Verification Steps**:
```bash
# Check if Notion section exists in config/README.md
grep -A 5 "Notion" config/README.md

# Check for migration guide
ls -la docs/migration/notion* 2>/dev/null || echo "No migration docs found"

# Check for technical debt docs
ls -la docs/technical-debt/PM-132* 2>/dev/null || echo "No tech debt docs found"
```

**Expected**:
- ✅ Notion section in README
- ✅ Migration guide exists
- ✅ Technical debt documented

---

### ✅ Criterion 6: Full test coverage passing

**Evidence Sources**:
- Issue #141 claims "11/12 tests passed"

**Verification Steps**:
```bash
# Run the config tests
pytest tests/config/test_notion_user_config.py -v

# Check overall test status
pytest tests/ -k notion --co -q | wc -l  # Count notion-related tests
```

**Expected**: Tests should still be passing (or close to it)

---

## Quick Investigation Summary

Create: `/tmp/issue-136-verification.md`

```markdown
# Issue #136 Verification Results

**Date**: October 15, 2025, 10:45 AM  
**Duration**: 15 minutes  
**Mission**: Verify completion of Issue #136

## Acceptance Criteria Status

### ✅/❌ Criterion 1: All hardcoded Notion IDs identified and documented
**Status**: [✅ Complete / ❌ Gap Found / ⚠️ Partial]
**Evidence**: 
- Files checked: [list]
- Hardcoded IDs found: [list or "none"]
- Assessment: [brief note]

### ✅/❌ Criterion 2: Configuration schema designed and implemented
**Status**: [✅ Complete / ❌ Missing / ⚠️ Partial]
**Evidence**:
- NotionUserConfig: [exists/missing]
- ADR-027: [exists/missing]
- Schema in PIPER.user.md: [complete/incomplete]

### ✅/❌ Criterion 3: Code refactored to use configuration
**Status**: [✅ Complete / ❌ Not Done / ⚠️ Partial]
**Evidence**:
- Files refactored: [count/list]
- Config lookups found: [yes/no]
- Assessment: [brief note]

### ✅/❌ Criterion 4: Backward compatibility maintained
**Status**: [✅ Complete / ❌ Missing / ⚠️ Unknown]
**Evidence**:
- Fallback logic: [found/not found]
- Assessment: [brief note]

### ✅/❌ Criterion 5: Documentation updated
**Status**: [✅ Complete / ❌ Missing / ⚠️ Partial]
**Evidence**:
- config/README.md: [updated/missing]
- Migration guide: [exists/missing]
- Technical debt docs: [exists/missing]

### ✅/❌ Criterion 6: Full test coverage passing
**Status**: [✅ Passing / ❌ Failing / ⚠️ Some Issues]
**Evidence**:
- Test run results: [summary]
- Pass rate: [X/Y tests]

## Overall Assessment

**Completion Status**: [✅ Complete / ❌ Incomplete / ⚠️ Mostly Complete]

**Recommendation**:
- [ ] Close #136 as complete with evidence
- [ ] Address specific gaps: [list]
- [ ] Requires deeper investigation

## Evidence References

**Child Issues**:
- #139 (PM-132): Config loader - CLOSED ✅
- #143: Refactoring - [status]
- #141: Testing/Docs - [status]

## Next Steps

[Clear recommendation based on findings]
```

---

## Deliverables

### Verification Complete When:
- [ ] All 6 criteria checked
- [ ] Evidence documented
- [ ] Gaps identified (if any)
- [ ] Recommendation provided
- [ ] Summary report created

---

## Time Budget

**Target**: 15 minutes
- Criterion 1 (hardcoded IDs): 3 min
- Criterion 2 (schema): 2 min
- Criterion 3 (refactoring): 3 min
- Criterion 4 (compatibility): 2 min
- Criterion 5 (docs): 2 min
- Criterion 6 (tests): 2 min
- Summary report: 1 min

---

## What NOT to Do

- ❌ Don't fix anything (just verify)
- ❌ Don't run full test suite (just config tests)
- ❌ Don't read entire files (just grep/search)
- ❌ Don't implement missing pieces (just document gaps)

## What TO Do

- ✅ Quick searches for evidence
- ✅ Reference child issue claims
- ✅ Document what IS vs what SHOULD BE
- ✅ Clear recommendation
- ✅ Note any surprises

---

## Success Criteria

**Verification is successful when**:
- Clear answer: Is #136 complete or not?
- Evidence documented for each criterion
- Gaps identified if they exist
- Recommendation provided
- Can confidently close or continue

---

## Context

**Why This Matters**:
- Don't want to close issues without verification
- Don't want to redo work that's done
- Need evidence-based completion
- Sprint A2 time is valuable

**What Comes After**:
- If complete: Close #136 with evidence, move to #165
- If gaps: Address specific gaps quickly
- If drift: Deal with drift systematically

---

**Phase -1 Start Time**: 10:45 AM  
**Expected Completion**: ~11:00 AM (15 minutes)  
**Status**: Ready for quick verification

**LET'S VERIFY!** ✅

---

*"Trust the child issues, but verify the parent is complete."*
*- Verification Philosophy*
