# Code Agent Prompt: PROOF-3 - GREAT-3 Plugin Polish Documentation

**Date**: October 13, 2025, 4:33 PM
**Phase**: PROOF-3 (GREAT-3 Plugin Documentation)
**Duration**: 2-4 hours estimated
**Priority**: MEDIUM (Stage 2: Documentation track)
**Agent**: Code Agent

---

## Mission

Verify and update GREAT-3 (Plugin Architecture) documentation using Serena-based verification. Apply lessons from PROOF-1: verify claims AND correct any discrepancies found.

**From PROOF-0**: GREAT-3 documentation is "exemplary" with "production-grade" quality - verify this is accurate and update with precise metrics.

---

## Critical Reminder: Post-Compaction Protocol

**AFTER ANY COMPACTION/SUMMARY**:
1. ✅ Re-verify the actual assignment before concluding
2. ✅ If discrepancies found during verification, MUST FIX THEM
3. ✅ Don't decide corrections are "optional" or "minor" - that's PM's call
4. ✅ Complete the assigned work fully

**Assignment**: Verify claims AND correct incorrect documentation

---

## Context from PROOF-0

### Current State
**From reconnaissance report** (`proof-0-gap-inventory.md`):
- Documentation: "exemplary - detailed metrics, evidence, timeline"
- 240+ lines of completion documentation
- ADR-034: 280 lines (claimed 281 - off by 1 line)
- Contract tests: Exist in multiple locations
- Performance overhead: 0.000041ms claimed
- Test count: "92 tests" claimed

### What Needs Verification
1. **Actual test count** (claimed 92)
2. **ADR-034 line count** (claimed 281, actual 280)
3. **Developer guide completeness**
4. **Performance overhead metrics**
5. **Plugin catalog accuracy**
6. **Contract test locations and counts**

---

## Investigation Phase (30 minutes)

### Step 1: Locate All GREAT-3 Documentation

Using Serena, find ALL GREAT-3 related documentation:

```python
# Find GREAT-3 docs
# Expected locations based on PROOF-0:
# - dev/2025/10/ (October 2-4 timeframe based on patterns)
# - docs/architecture/ (plugin architecture)
# - docs/internal/architecture/current/adrs/ (ADR-034)
```

**Documents to locate**:
- GREAT-3 epic completion report (GREAT-3-EPIC-COMPLETE.md or similar)
- ADR-034 (Plugin Architecture)
- Developer guide (if separate)
- Plugin catalog (if exists)
- Contract test documentation
- Performance documentation

### Step 2: Extract Current Claims

From each document found, extract **all quantifiable claims**:

**Create claims inventory**:
```markdown
| Document | Claim Type | Claimed Value | Section/Line |
|----------|------------|---------------|--------------|
| GREAT-3-EPIC-COMPLETE | Contract tests | 92 tests | Line X |
| GREAT-3-EPIC-COMPLETE | Performance overhead | 0.000041ms | Line Y |
| ADR-034 | File size | 281 lines | Mentioned |
| ... | ... | ... | ... |
```

**Focus on**:
- Test counts (claimed 92)
- File sizes (ADR-034: 280 vs 281)
- Performance metrics (0.000041ms)
- Integration counts (4 plugin wrappers?)
- Line counts and file counts

### Step 3: Verify Each Claim with Serena

For each claim, use Serena to verify actual state:

**Test counts**:
```python
# Find contract test files
# Use Serena to search for test files in:
# - tests/plugins/contract/
# - tests/intent/contracts/
# Count actual test functions
```

**ADR-034 line count**:
```python
# Use Serena or wc -l to verify exact line count
# Current known: 280 lines actual vs 281 claimed
```

**Plugin wrappers**:
```python
# Verify 4 plugin wrappers exist:
# - GitHub
# - Slack
# - Notion
# - Calendar (Google Calendar)
```

**Performance metrics**:
```python
# Check for benchmark files
# Look for performance test results
# Verify 0.000041ms claim has source
```

---

## Documentation Update Phase (45 minutes)

### Step 1: Update GREAT-3 Completion Report

**File**: Likely `dev/2025/10/XX/GREAT-3-EPIC-COMPLETE.md` or similar

**Updates needed** (based on verification):

**If test count needs correction**:
```markdown
### Test Coverage
**Contract Tests**: [ACTUAL COUNT] tests (verified October 13, 2025)
**Locations**:
- tests/plugins/contract/ - [COUNT] tests
- tests/intent/contracts/ - [COUNT] tests

[Previous claim: 92 tests - update if different]
```

**If performance metrics need source**:
```markdown
### Performance Overhead
**Measured**: 0.000041ms per request
**Source**: [Benchmark file or test that measured this]
**Date**: [When measurement was taken]
**Method**: [How it was measured]
```

### Step 2: Update/Complete ADR-034

**File**: `docs/internal/architecture/current/adrs/adr-034-plugin-architecture.md`

**Check sections**:
- ✅ Context complete?
- ✅ Decision clear?
- ✅ Consequences detailed?
- ✅ Examples present?

**Add verification section** (like we did in PROOF-1):
```markdown
## Verification (October 13, 2025)

### Implementation Status
- Plugin Architecture: ✅ Complete (October 2-4, 2025)
- File size: 280 lines (previously claimed 281)
- Contract tests: [ACTUAL] tests
- Plugin wrappers: [ACTUAL COUNT] implemented
- Performance overhead: 0.000041ms per request

### Evidence
- Completion report: dev/2025/10/XX/GREAT-3-EPIC-COMPLETE.md
- Contract tests: tests/plugins/contract/, tests/intent/contracts/
- Benchmark: [location if found]

### Plugin Implementations
1. GitHub plugin: ✅ Operational
2. Slack plugin: ✅ Operational
3. Notion plugin: ✅ Operational
4. Calendar plugin: ✅ Operational
```

### Step 3: Verify Developer Guide

**From PROOF-0**: "Developer guide examples" need verification

**Locate developer guide**:
```python
# Use Serena to find:
# - Plugin development guide
# - Developer documentation
# - Integration patterns doc
```

**If exists, verify**:
- Are examples working/accurate?
- Do they match current API?
- Are there code samples?
- Is it complete?

**If incomplete**: Document what's missing

### Step 4: Verify Plugin Catalog

**From PROOF-0**: "Plugin catalog completeness" needs checking

**Locate plugin catalog**:
```python
# Likely in:
# - docs/plugins/ or
# - docs/architecture/plugins/ or
# - Within ADR-034
```

**Verify catalog includes**:
- All 4 plugin wrappers listed
- Status of each (operational/in-progress)
- Integration methods documented
- Examples or usage notes

**If missing**: Note what should be added

### Step 5: Update Contract Test Documentation

**Verify test locations are documented**:
- tests/plugins/contract/ - [purpose]
- tests/intent/contracts/ - [purpose]

**Update test counts** if different from claimed 92

**Document test structure**:
```markdown
### Contract Test Structure

**Total Tests**: [ACTUAL] contract tests (verified October 13, 2025)

**Test Locations**:
1. `tests/plugins/contract/` - [COUNT] tests
   - Purpose: [what these test]

2. `tests/intent/contracts/` - [COUNT] tests
   - Purpose: [what these test]

**Test Coverage**:
- [Test category 1]: [count]
- [Test category 2]: [count]
- etc.
```

---

## Verification Phase (30 minutes)

### Cross-Reference Check

**Ensure consistency across documents**:
1. Test counts match everywhere
2. ADR-034 line count corrected (280, not 281)
3. Performance metrics cited consistently
4. Plugin wrapper counts match

**Create consistency matrix**:
```markdown
| Metric | GREAT-3 Report | ADR-034 | Dev Guide | Actual | Status |
|--------|----------------|---------|-----------|--------|--------|
| Contract tests | 92 | [check] | [check] | [ACTUAL] | ✅/⚠️ |
| ADR-034 lines | 281 | N/A | N/A | 280 | ⚠️ |
| Plugin wrappers | 4 | [check] | [check] | [ACTUAL] | ✅/⚠️ |
| Performance | 0.000041ms | [check] | [check] | [ACTUAL] | ✅/⚠️ |
```

### Evidence Collection

**Gather proof for all claims**:
- Test file listings
- Test function counts
- Plugin wrapper verification
- Performance benchmark results
- ADR line count proof

**Create evidence file**:
`dev/2025/10/13/proof-3-great-3-evidence.md`

---

## Output Phase (15 minutes)

### Create PROOF-3 Completion Report

**File**: `dev/2025/10/13/proof-3-great-3-completion.md`

**Structure** (similar to PROOF-1):
```markdown
# PROOF-3: GREAT-3 Plugin Polish Documentation

**Date**: October 13, 2025, 4:33 PM
**Agent**: Code Agent
**Duration**: [Actual time]
**Epic**: GREAT-3 (Plugin Architecture)

---

## Mission Accomplished

Updated GREAT-3 documentation to 100% Serena-verified accuracy.

---

## Documents Updated

### 1. GREAT-3 Completion Report
**Location**: [path]
**Changes**: [what was updated]
**Verification**: [how verified]

### 2. ADR-034
**Status**: [Complete/Updated]
**Changes**: [Line count corrected, verification section added, etc.]

### 3. [Developer Guide]
**Status**: [Verified/Updated/Not Found]
**Changes**: [if any]

### 4. [Plugin Catalog]
**Status**: [Verified/Updated/Not Found]
**Changes**: [if any]

---

## Verification Results

### Claims Verified

| Claim | Original | Verified | Status | Notes |
|-------|----------|----------|--------|-------|
| Contract tests | 92 tests | [ACTUAL] | ✅/⚠️ | [notes] |
| ADR-034 lines | 281 lines | 280 lines | ⚠️ | Off by 1 |
| Performance | 0.000041ms | [SOURCE] | ✅/⚠️ | [notes] |
| Plugin wrappers | 4 wrappers | [ACTUAL] | ✅/⚠️ | [notes] |

### Documentation Accuracy

**Before PROOF-3**: ~98% accurate (PROOF-0: "exemplary")
**After PROOF-3**: 99%+ accurate (Serena-verified)

**Gaps Closed**: [number] claims verified and corrected

---

## Files Modified

- [x] dev/2025/10/XX/GREAT-3-EPIC-COMPLETE.md
- [x] docs/internal/architecture/current/adrs/adr-034-*.md
- [x] [other files if any]

**Total Changes**: [number] files, [number] corrections made

---

## Evidence Package

**Evidence File**: dev/2025/10/13/proof-3-great-3-evidence.md

**Contains**:
- Test count verification
- ADR line count proof
- Plugin wrapper verification
- Performance metric sources
- Cross-reference matrix

---

## Next Steps

- [ ] Commit documentation updates
- [ ] Ready for PROOF-8 (ADR Completion) or PROOF-9 (Doc Sync)
- [ ] GREAT-3 documentation: 100% complete ✅

---

**Completion Time**: [timestamp]
**Status**: PROOF-3 Complete ✅
```

---

## Commit Strategy

### Create Clean Commit

```bash
# Stage all documentation updates
git add dev/2025/10/
git add docs/internal/architecture/current/adrs/adr-034-*.md
git add dev/2025/10/13/proof-3-*.md
git add [any other modified files]

# Commit with clear message
git commit -m "docs(PROOF-3): Complete GREAT-3 plugin documentation verification

Updated GREAT-3 (Plugin Architecture) documentation to 100% Serena-verified accuracy.

Changes:
- Verified contract test counts with actual measurements
- Corrected ADR-034 line count (281 → 280)
- Verified plugin wrapper implementations
- Confirmed performance overhead metrics
- Added verification sections to ADR-034
- Created evidence package

Verification method: Serena MCP systematic audit
Accuracy: ~98% → 99%+ (exemplary → verified)

Files updated: [list]
Claims verified: [count]

Part of: CORE-CRAFT-PROOF epic, Stage 2 (Documentation)"

# Push
git push origin main
```

---

## Success Criteria

### Investigation Complete ✅
- [ ] All GREAT-3 docs located
- [ ] All claims extracted
- [ ] All claims verified with Serena
- [ ] Discrepancies identified

### Documentation Updated ✅
- [ ] GREAT-3 completion report accurate
- [ ] ADR-034 line count corrected (280, not 281)
- [ ] Developer guide verified/updated
- [ ] Plugin catalog verified/updated
- [ ] Contract test docs accurate

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

**Optimistic** (If docs are as good as PROOF-0 says): 2 hours
- Investigation: 30 min
- Updates: 45 min
- Verification: 30 min
- Output: 15 min

**Realistic** (If more issues found): 3 hours
- Investigation: 45 min
- Updates: 75 min
- Verification: 45 min
- Output: 15 min

**Pessimistic** (If significant gaps): 4 hours
- Investigation: 60 min
- Updates: 120 min
- Verification: 60 min
- Output: 20 min

**Target Completion**: 6:33 PM (optimistic) to 8:33 PM (pessimistic)

---

## What NOT to Do

- ❌ Don't decide corrections are "optional" after compaction
- ❌ Don't skip fixing discrepancies found
- ❌ Don't accept "close enough" for metrics
- ❌ Don't modify plugin code - documentation only
- ❌ Don't guess at test counts - verify with Serena

## What TO Do

- ✅ Apply post-compaction protocol rigorously
- ✅ Use Serena for all verifications
- ✅ Fix ALL discrepancies found (not just document them)
- ✅ Document verification method
- ✅ Create complete evidence trail
- ✅ Ensure cross-document consistency

---

## Context

**PM Quote**: "Let's try for PROOF-3. If it really takes 4 hrs I'll finish after dinner." (4:33 PM)

**Why PROOF-3 Now**:
- PROOF-1 pattern established (verify AND correct)
- Post-compaction protocol in place
- Stage 2 (Documentation) track continues
- PROOF-0 says GREAT-3 is "exemplary" - let's verify
- No code changes needed

**What This Achieves**:
- GREAT-3 documentation: 100% verified
- Pattern reinforced from PROOF-1
- ADR-034 corrected (line count)
- Evidence-based completion continues

**What Comes After**:
- If <2 hours: Continue with PROOF-8 or PROOF-9 today
- If 2-4 hours: Break for dinner, continue if energized
- PROOF epic progressing well

---

**PROOF-3 Start Time**: 4:33 PM
**Expected Completion**: 6:33-8:33 PM (2-4 hours)
**Status**: Ready for Code Agent execution

**LET'S GET GREAT-3 DOCS TO 100%! 🔌✅**

---

*"Exemplary documentation verified becomes proven excellence."*
*- PROOF-3 Philosophy*
