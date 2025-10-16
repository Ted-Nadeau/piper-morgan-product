# Code Agent Prompt: PROOF-0 - Full Reconnaissance (Both Tracks)

**Date**: October 13, 2025, 2:47 PM
**Phase**: PROOF-0 (Full Reconnaissance)
**Duration**: 2-3 hours
**Priority**: HIGH
**Agent**: Code Agent

---

## Mission

Execute complete PROOF-0 reconnaissance on TWO parallel tracks:

**Track 1**: Documentation audit with Serena (90 minutes)
**Track 2**: CI/CD investigation and fixes (60 minutes)

**PM Context**: "I have plenty of time today! Don't postpone anything."

---

## Track 1: Documentation Reconnaissance (90 minutes)

### Objective
Create comprehensive gap inventory: What do docs CLAIM vs what code ACTUALLY HAS?

### Using Serena MCP

You have full access to Serena's tools:
- `list_dir` - Directory listings
- `find_file` - Locate specific files
- `search_for_pattern` - Pattern matching
- `get_symbols_overview` - Code structure
- `find_symbol` - Specific symbol location
- All other symbolic analysis tools

### Systematic Audit Process

**For Each GREAT Epic** (GREAT-1 through GREAT-5):

1. **Find All Documentation**
```
Use Serena to locate:
- Epic completion reports
- Gameplan files
- Description files
- Any other GREAT-X related docs
```

2. **Extract Claims**
Look for statements like:
- "Added X tests"
- "X lines of code"
- "Achieved X% accuracy"
- "Created X files"
- "X handlers implemented"
- Any quantifiable claims

3. **Verify Against Code**
```
For each claim:
- Use Serena to count actual files
- Use Serena to count actual tests
- Use Serena to measure actual lines
- Document: CLAIMED vs ACTUAL vs GAP
```

4. **Document Drift**
```
Create table:
| Epic | Claim | Claimed Value | Actual Value | Gap | Severity |
```

### Specific Areas to Audit

**GREAT-1 (QueryRouter)**:
- Claimed test count
- Claimed line count
- Architecture.md accuracy
- ADR-032 completeness
- Troubleshooting guide status

**GREAT-2 (Spatial Intelligence)**:
- Claimed 92 tests vs actual
- Router test count
- ConfigValidator integration claims
- File inventory accuracy

**GREAT-3 (Plugin Architecture)**:
- Claimed 92 tests vs actual
- Developer guide completeness
- Performance overhead claims
- Plugin catalog accuracy

**GREAT-4 (Complex, multiple sub-epics)**:
- 4A: Claims from completion
- 4B: Interface enforcement claims (GAP-2 updated)
- 4C: Multi-user test claims
- 4D: Handler implementation claims (GAP-1 updated)
- 4E: Test infrastructure claims
- 4F: Classification accuracy (GAP-3 just updated to 98.62%)

**GREAT-5 (CI/CD & Performance)**:
- Line count precision
- Benchmark claims
- CI/CD pipeline time claims
- Quality gate documentation

### ADR Audit

**For All 41 ADRs**:
1. Check completion status (Introduction, Context, Decision, Consequences)
2. Identify incomplete ADRs
3. Check for outdated information
4. Verify references are valid
5. Note which need updates

**From Chief Architect Report**, we know these need attention:
- ADR-032: QueryRouter (needs revision)
- ADR-039: Classification accuracy (needs update to 98.62%)
- 4-6 others identified in earlier tracking

### Output Format

**Create**: `dev/2025/10/13/proof-0-gap-inventory.md`

```markdown
# PROOF-0: Gap Inventory Report

**Date**: October 13, 2025
**Agent**: Code Agent
**Tracks**: Documentation + CI/CD
**Duration**: [Actual time]

---

## Executive Summary

**Total Claims Audited**: X
**Gaps Found**: X
**Documentation Drift**: X% average
**Critical Issues**: X
**Ready for PROOF execution**: [Yes/No/Partial]

---

## GREAT-1 Documentation Audit

### Claims vs Reality

| Claim Type | Document Location | Claimed | Actual | Gap | Severity |
|------------|------------------|---------|--------|-----|----------|
| Test count | GREAT-1-completion.md | 45 | 52 | -7 | Medium |
| Line count | architecture.md | 2000 | 2347 | -347 | Low |
| ... | ... | ... | ... | ... | ... |

### Findings
[Detailed analysis]

### Recommendations
[What needs updating]

---

[Repeat for GREAT-2 through GREAT-5]

---

## ADR Audit

### Completion Status

| ADR | Title | Status | Completion % | Issues Found | Priority |
|-----|-------|--------|--------------|--------------|----------|
| ADR-032 | QueryRouter | Outdated | 60% | Needs revision | High |
| ADR-039 | Classification | Needs update | 95% | Update to 98.62% | Medium |
| ... | ... | ... | ... | ... | ... |

### Incomplete ADRs
[List ADRs that need completion]

### Outdated ADRs
[List ADRs that need updates]

---

## Documentation Drift Patterns

**Common Issues**:
1. [Pattern 1]
2. [Pattern 2]
3. [Pattern 3]

**Root Causes**:
1. [Cause 1]
2. [Cause 2]

**Recommendations**:
1. [Fix 1]
2. [Fix 2]

---

## Test Precision Issues

**Permissive Patterns Found**: X tests
**Examples**:
```python
# Example 1: Permissive assertion
assert response.status_code in [200, 404]  # Should be: == 200

# Example 2: Structural check only
assert "error" in response  # Should check: response["error"] == expected_message
```

**Files with Issues**:
- [List files needing precision fixes]

---

## Summary Statistics

**Documentation Claims Audited**: X
**Code Verification Checks**: X
**Gaps Identified**: X
**Critical Gaps**: X
**Medium Gaps**: X
**Minor Gaps**: X

**Estimated Fix Time**:
- Critical gaps: X hours
- Medium gaps: X hours
- Minor gaps: X hours
- **Total**: X hours

---

[CI/CD findings from Track 2 below]
```

---

## Track 2: CI/CD Investigation (60 minutes)

### Current State (from Phase -1)

**Failing Workflows** (4 total):
1. Tests workflow
2. CI workflow
3. Code Quality workflow
4. PM-034 LLM Intent Classification CI/CD

**Need to understand**:
- WHY each is failing
- WHEN each started failing
- HOW to fix each
- WHETHER fixes are quick or complex

### Investigation Process

**For Each Failing Workflow**:

1. **Find Workflow File**
```bash
# Locate in .github/workflows/
ls -la .github/workflows/
```

2. **Check Recent Run Logs**
```
Use whatever tools available:
- GitHub CLI if available
- Check .github/workflows/X.yml for clues
- Look at workflow configuration
```

3. **Identify Failure Cause**
```
Common causes:
- Missing API keys (expected for LLM tests)
- Linting issues (flake8, black)
- Import errors
- Test failures
- Configuration issues
```

4. **Assess Fix Complexity**
```
Quick fixes (< 30 min):
- Linting issues
- Simple configuration
- Test markers

Complex fixes (> 1 hour):
- Architectural violations
- Test infrastructure
- Major refactoring
```

### Specific Investigations

**Tests Workflow Failure**:
- Check if LLM tests running despite `-m "not llm"` marker
- Verify test discovery issues
- Check for import errors
- Assess: Quick fix or complex?

**CI Workflow Failure**:
- Identify what CI workflow does
- Check configuration vs reality
- Assess: Quick fix or complex?

**Code Quality Failure**:
- Likely flake8/black linting issues
- Check which files failing
- Run locally: `flake8 . && black --check .`
- Assess: Quick fix or complex?

**PM-034 Failure**:
- Expected if missing API keys
- Check if this is known/acceptable
- Assess: Fix now or document as expected?

### Repository Cleanup

**Uncommitted Changes** (118 files):
- 46 modified (mostly venv)
- 40 deleted (dev/active/ reorganization)
- 72 untracked (dev/2025/ new files)

**Actions**:
1. **Identify Intention**
   - File reorganization: dev/active/ → dev/2025/MM/DD/
   - Venv changes: Should be in .gitignore
   - ADR deletion: Verify intentional

2. **Clean Commit Plan**
```bash
# Stage file reorganization
git add dev/2025/
git rm dev/active/*

# Verify venv ignored
grep -r "venv" .gitignore

# Commit cleanly
git commit -m "chore: Reorganize dev/ files by date structure"
```

3. **Verify Clean State**
```bash
git status
# Should show: "working tree clean"
```

### CI/CD Output Format

**Add to**: `dev/2025/10/13/proof-0-gap-inventory.md`

```markdown
---

## CI/CD Investigation Results

### Workflow Analysis

#### 1. Tests Workflow ❌

**Status**: FAILING
**Last Run**: [Date/time]
**Failure Cause**: [Root cause identified]
**Fix Complexity**: [Quick/Medium/Complex]
**Recommended Action**: [Specific fix or defer]

**Investigation Details**:
- [What you found]
- [Why it's failing]
- [How to fix it]

**Code to Fix** (if quick):
```python
# Show the fix if straightforward
```

---

#### 2. CI Workflow ❌

[Same format as above]

---

#### 3. Code Quality Workflow ❌

[Same format as above]

---

#### 4. PM-034 LLM Classification ❌

[Same format as above]

---

### Repository Cleanup Results

**Status**: [Clean/In Progress/Blocked]

**Actions Taken**:
- [x] Staged file reorganization
- [x] Verified venv ignored
- [ ] Committed changes (awaiting review)

**Working Directory**: [Clean/Has changes]

---

### CI/CD Readiness Assessment

**Quick Wins Available**: [Yes/No]
**Estimated Time to Green**: [X hours]
**Blockers to Code Changes**: [None/Some/Many]

**Recommendation**: [Proceed/Fix CI first/Defer]

---

## Combined Recommendation

**Documentation Work**: [Ready now]
**Code Precision Work**: [Ready after CI fixes / Ready now]
**Estimated Time to Full Readiness**: [X hours]

**Suggested Approach for PROOF Execution**:
1. [Step 1]
2. [Step 2]
3. [Step 3]
```

---

## Success Criteria

### Track 1 Complete ✅
- [ ] All GREAT epics audited
- [ ] Claims extracted and verified
- [ ] Gaps documented with severity
- [ ] ADRs reviewed for completeness
- [ ] Test precision issues identified
- [ ] Drift patterns analyzed
- [ ] Fix time estimated

### Track 2 Complete ✅
- [ ] All 4 CI failures investigated
- [ ] Root causes identified
- [ ] Fix complexity assessed
- [ ] Repository cleanup completed
- [ ] Quick wins implemented (if any)
- [ ] Readiness for code work assessed

### Overall PROOF-0 Complete ✅
- [ ] Gap inventory comprehensive
- [ ] No hidden surprises remaining
- [ ] Clear path forward for PROOF-1 through PROOF-9
- [ ] Scope validated or adjusted
- [ ] Timeline refined based on findings

---

## Time Management

**Track 1** (Documentation): 90 minutes
- GREAT-1: 15 minutes
- GREAT-2: 15 minutes
- GREAT-3: 20 minutes
- GREAT-4: 25 minutes (complex, multiple sub-epics)
- GREAT-5: 10 minutes
- ADRs: 15 minutes (high-level review)
- Analysis & report: 15 minutes

**Track 2** (CI/CD): 60 minutes
- Investigation: 30 minutes (4 workflows = 7-8 min each)
- Repository cleanup: 15 minutes
- Quick fixes (if any): 15 minutes
- Documentation: 10 minutes

**Total**: 150 minutes (2.5 hours)

**Buffer**: 30 minutes for unexpected discoveries

**Target Completion**: ~5:30 PM

---

## What NOT to Do

- ❌ Don't spend > 30 minutes on any single CI fix (timebox it)
- ❌ Don't restructure documentation (work with what exists)
- ❌ Don't fix every gap found (just document them)
- ❌ Don't make architectural decisions (flag for review)
- ❌ Don't commit without PM review (stage but don't push)

## What TO Do

- ✅ Be systematic and thorough
- ✅ Document everything found
- ✅ Provide evidence for claims
- ✅ Prioritize findings (Critical/Medium/Low)
- ✅ Give time estimates for fixes
- ✅ Flag anything unexpected
- ✅ Create clear, actionable report

---

## Context

**PM Quote**: "I have plenty of time today! Don't postpone anything."

**What This Means**:
- Execute FULL reconnaissance (both tracks)
- Implement quick CI fixes if found
- Don't artificially defer work
- Be thorough but efficient
- Complete gap inventory today

**What Comes After**:
- Review gap inventory with PM
- Decide PROOF-1 through PROOF-9 execution order
- Start addressing gaps (could be today or tomorrow)
- Maintain momentum from GAP success

---

**PROOF-0 Start Time**: 2:47 PM
**Expected Completion**: ~5:30 PM (2.5-3 hours)
**Status**: Ready for full reconnaissance deployment

**LET'S DISCOVER ALL THE GAPS! 🔍**

---

*"Reconnaissance before action. Discovery before fixing. Evidence before claims."*
*- PROOF Philosophy*
