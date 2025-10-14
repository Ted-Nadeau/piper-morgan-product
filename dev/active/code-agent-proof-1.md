# Code Agent Prompt: PROOF-1 - GREAT-1 Documentation Completion

**Date**: October 13, 2025, 4:04 PM
**Phase**: PROOF-1 (GREAT-1 Documentation)
**Duration**: 1-2 hours
**Priority**: MEDIUM (Stage 2: Documentation track)
**Agent**: Code Agent

---

## Mission

Complete and verify GREAT-1 (QueryRouter) documentation using findings from PROOF-0 reconnaissance. Update documentation to reflect actual implementation state with Serena-verified accuracy.

**From PROOF-0**: GREAT-1 documentation is "generally accurate with minor discrepancies" - we need to make it 100% accurate.

---

## Context from PROOF-0

### Current State
**From reconnaissance report** (`proof-0-gap-inventory.md`):
- Claims are "reasonable estimates" but not verified
- QueryRouter exists at `services/queries/query_router.py` (lines 39-934) ✅
- Lock tests exist at `tests/regression/test_queryrouter_lock.py` ✅
- Performance claims (248s → 40s) not re-verified
- Line counts (~2,500) not independently verified
- Coverage (80%) not measured

### What Needs Verification
1. **Exact file locations and sizes**
2. **Actual line counts** (not estimates)
3. **Test counts** (actual, not claimed)
4. **Performance metrics** (current, not historical)
5. **Architecture.md accuracy**
6. **ADR-032 completeness**

---

## Investigation Phase (20 minutes)

### Step 1: Locate All GREAT-1 Documentation

Using Serena, find ALL GREAT-1 related documentation:

```python
# Find GREAT-1 docs
# Use Serena to search for "GREAT-1" in markdown files
# Expected locations based on PROOF-0:
# - dev/2025/09/22/ or similar (completion reports)
# - docs/architecture/
# - docs/internal/architecture/current/adrs/ (ADR-032)
```

**Documents to locate**:
- GREAT-1 completion report
- Architecture.md (QueryRouter section)
- ADR-032 (QueryRouter restoration)
- ADR-036 (QueryRouter resurrection strategy)
- Troubleshooting guide (if exists)
- Performance documentation

### Step 2: Extract Current Claims

From each document found, extract **all quantifiable claims**:
- Line counts
- File counts
- Test counts
- Performance metrics
- Coverage percentages
- Time improvements

**Create claims inventory**:
```markdown
| Document | Claim Type | Claimed Value | Section/Line |
|----------|------------|---------------|--------------|
| GREAT-1-completion.md | Lines changed | ~2,500 | Line 45 |
| ADR-032 | Test count | 9 lock tests | Line 120 |
| ... | ... | ... | ... |
```

### Step 3: Verify Each Claim with Serena

For each claim, use Serena to verify actual state:

**File and line counts**:
```python
# Example: Verify QueryRouter lines
# Use Serena to count actual lines in query_router.py
# Compare to claimed ~2,500 lines across 47 files
```

**Test counts**:
```python
# Count lock tests
# Use Serena to find all test files related to QueryRouter
# Count actual test functions
```

**Performance metrics**:
```python
# Check if benchmarks exist
# Look for performance test results
# Note: Historical metrics (248s → 40s) may not be re-runnable
```

---

## Documentation Update Phase (30 minutes)

### Step 1: Update Architecture.md

**File**: `docs/architecture/` or `docs/internal/architecture/`

**Updates needed** (based on verification):
- Exact file locations for QueryRouter
- Accurate line counts
- Current test coverage
- Performance characteristics
- Integration points

**Format**:
```markdown
### QueryRouter Architecture

**Location**: `services/queries/query_router.py` (lines 39-934)
**Total Size**: [ACTUAL] lines across [ACTUAL] files
**Test Coverage**: [ACTUAL]% ([ACTUAL] tests)
**Performance**: [ACTUAL measurements]

**Integration Points**:
- Intent Classification → QueryRouter → [actual flow]
- OrchestrationEngine integration: [actual state]

**Locking Mechanisms**:
- Lock tests: `tests/regression/test_queryrouter_lock.py` ([ACTUAL] tests)
- Purpose: [actual purpose]
```

### Step 2: Update/Complete ADR-032

**File**: `docs/internal/architecture/current/adrs/adr-032-intent-classification-universal-entry.md`

**Check completion** (from PROOF-0: mentioned needs revision):
- Is Context section complete?
- Is Decision section clear?
- Is Consequences section detailed?
- Is Evidence section present?

**If incomplete, add**:
```markdown
## Evidence
[From GREAT-1 implementation]

### Implementation Status
- QueryRouter: ✅ Complete (September 22, 2025)
- Line count: [ACTUAL] lines
- Test coverage: [ACTUAL] tests
- Performance: [ACTUAL] metrics

### Session Logs
- Implementation: dev/2025/09/22/2025-09-22-1649-prog-code-log.md
- Completion: dev/2025/09/22/final-session-report-CORE-GREAT-1-complete.md

### GitHub Issues
- #185 (QueryRouter Investigation)
- #186 (Integration)
- #188 (Locking)
```

### Step 3: Verify ADR-036

**File**: ADR-036 (QueryRouter resurrection strategy)

From project knowledge search, this exists and is marked "✅ Completed".

**Check for updates needed**:
- Does it reference actual completion date?
- Are implementation results documented?
- Is status current?

**Update if needed** with actual metrics from verification.

### Step 4: Check for Troubleshooting Guide

**From PROOF-0**: "Troubleshooting guide completion" mentioned

**Locate**:
```python
# Use Serena to find troubleshooting docs
# Likely in docs/architecture/ or docs/guides/
```

**If exists**: Verify accuracy and completeness
**If missing**: Note in findings (may not be required)

### Step 5: Update Performance Documentation

**Locate performance claims**:
- GREAT-1 completion report mentions 248s → 40s improvement
- GAP-3 work shows 0.454ms classification average
- GREAT-1C mentions sub-millisecond QueryRouter access

**Verify current state**:
```python
# Check for benchmark files
# Look in scripts/ or tests/performance/
# Verify claims match current measurements
```

**Update with accurate metrics**:
- If benchmarks exist: Run and record results
- If historical only: Note as "Historical baseline: X, not re-verified"
- If no benchmarks: Note as "Claimed: X, verification method: [describe]"

---

## Verification Phase (20 minutes)

### Cross-Reference Check

**Ensure consistency across documents**:
1. Line counts match between docs
2. Test counts consistent
3. Performance claims cross-referenced
4. File locations accurate everywhere

**Create consistency matrix**:
```markdown
| Metric | GREAT-1 Report | Architecture.md | ADR-032 | Status |
|--------|----------------|-----------------|---------|--------|
| QueryRouter lines | ~2,500 | [check] | [check] | ✅/❌ |
| Lock tests | 9 | [check] | [check] | ✅/❌ |
| ... | ... | ... | ... | ... |
```

### Evidence Collection

**Gather proof for all claims**:
- Screenshots of Serena counts (if helpful)
- File tree showing structure
- Test output showing counts
- Any benchmark results

**Create evidence file**:
`dev/2025/10/13/proof-1-great-1-evidence.md`

---

## Output Phase (10 minutes)

### Create PROOF-1 Completion Report

**File**: `dev/2025/10/13/proof-1-great-1-completion.md`

**Structure**:
```markdown
# PROOF-1: GREAT-1 Documentation Completion

**Date**: October 13, 2025, 4:04 PM
**Agent**: Code Agent
**Duration**: [Actual time]
**Epic**: GREAT-1 (QueryRouter)

---

## Mission Accomplished

Updated GREAT-1 documentation to 100% Serena-verified accuracy.

---

## Documents Updated

### 1. Architecture.md
**Location**: [path]
**Changes**: [what was updated]
**Verification**: [how verified]

### 2. ADR-032
**Location**: docs/internal/architecture/current/adrs/adr-032-*.md
**Status**: [Complete/Updated/No changes needed]
**Changes**: [if any]

### 3. ADR-036
**Status**: [Verified complete/Updated]
**Changes**: [if any]

### 4. [Other docs]
[...]

---

## Verification Results

### Claims Verified

| Claim | Original | Verified | Status | Notes |
|-------|----------|----------|--------|-------|
| QueryRouter lines | ~2,500 | [ACTUAL] | ✅/⚠️ | [notes] |
| Lock tests | 9 tests | [ACTUAL] | ✅/⚠️ | [notes] |
| Performance | 248s→40s | [CURRENT] | ✅/⚠️ | [notes] |
| ... | ... | ... | ... | ... |

### Documentation Accuracy

**Before PROOF-1**: ~95% accurate (reasonable estimates)
**After PROOF-1**: 99%+ accurate (Serena-verified)

**Gaps Closed**: [number] claims verified and updated

---

## Files Modified

- [x] docs/architecture/[filename]
- [x] docs/internal/architecture/current/adrs/adr-032-*.md
- [x] [other files]

**Total Changes**: [number] files, [number] lines modified

---

## Evidence Package

**Evidence File**: dev/2025/10/13/proof-1-great-1-evidence.md

**Contains**:
- Serena verification outputs
- File structure snapshots
- Test count verifications
- Cross-reference matrix

---

## Next Steps

- [ ] Commit documentation updates
- [ ] Ready for PROOF-3 (GREAT-3 Plugin Polish)
- [ ] GREAT-1 documentation: 100% complete ✅

---

**Completion Time**: [timestamp]
**Status**: PROOF-1 Complete ✅
```

---

## Commit Strategy

### Create Clean Commit

```bash
# Stage all documentation updates
git add docs/architecture/
git add docs/internal/architecture/current/adrs/adr-032-*.md
git add docs/internal/architecture/current/adrs/adr-036-*.md
git add dev/2025/10/13/proof-1-*.md

# Commit with clear message
git commit -m "docs(PROOF-1): Complete GREAT-1 documentation verification

Updated GREAT-1 (QueryRouter) documentation to 100% Serena-verified accuracy.

Changes:
- Verified all quantifiable claims with actual measurements
- Updated architecture.md with precise metrics
- Completed ADR-032 evidence section
- Verified ADR-036 status
- Created evidence package

Verification method: Serena MCP systematic audit
Accuracy: 95% → 99%+ (estimated → verified)

Files updated: [list]
Claims verified: [count]

Part of: CORE-CRAFT-PROOF epic, Stage 2 (Documentation)"

# Push
git push origin main
```

---

## Success Criteria

### Investigation Complete ✅
- [ ] All GREAT-1 docs located
- [ ] All claims extracted
- [ ] All claims verified with Serena
- [ ] Discrepancies identified

### Documentation Updated ✅
- [ ] Architecture.md accurate
- [ ] ADR-032 complete/verified
- [ ] ADR-036 verified
- [ ] Troubleshooting guide checked
- [ ] Performance docs accurate

### Verification Complete ✅
- [ ] Cross-reference check done
- [ ] Consistency matrix created
- [ ] Evidence collected
- [ ] 99%+ accuracy achieved

### Committed ✅
- [ ] All changes staged
- [ ] Descriptive commit message
- [ ] Pushed to main
- [ ] Completion report created

---

## Time Budget

- **Investigation**: 20 minutes (locate docs, extract claims, verify)
- **Updates**: 30 minutes (architecture, ADRs, other docs)
- **Verification**: 20 minutes (cross-check, evidence collection)
- **Output**: 10 minutes (completion report, commit)
- **Total**: 80 minutes (1 hour 20 minutes)

**Target Completion**: 5:24 PM

---

## What NOT to Do

- ❌ Don't guess at metrics - verify with Serena
- ❌ Don't accept "reasonable estimates" - get actual numbers
- ❌ Don't skip cross-references - ensure consistency
- ❌ Don't modify code - documentation only
- ❌ Don't re-run historical benchmarks if not needed

## What TO Do

- ✅ Use Serena for all verifications
- ✅ Document verification method
- ✅ Note when historical claims can't be re-verified
- ✅ Create evidence trail
- ✅ Ensure cross-document consistency

---

## Context

**PM Quote**: "Let's work on PROOF-1" (4:04 PM after fixing CI)

**Why PROOF-1 Now**:
- PROOF-0 complete (gap inventory done)
- CI mostly clean (architectural bypass fixed)
- Stage 2 (Documentation) track is safe to proceed
- No code changes needed
- Clear, focused scope

**What This Achieves**:
- GREAT-1 documentation: 100% verified
- Pattern established for PROOF-3 (GREAT-3)
- Evidence-based completion (not estimates)
- Sets standard for remaining PROOF work

**What Comes After**:
- PROOF-3: GREAT-3 documentation
- PROOF-8: ADR completion
- PROOF-9: Documentation sync process

---

**PROOF-1 Start Time**: 4:04 PM
**Expected Completion**: ~5:24 PM (80 minutes)
**Status**: Ready for Code Agent execution

**LET'S GET GREAT-1 DOCS TO 100%! 📋✅**
