# Code Agent Prompt: VALID-1 - Serena Comprehensive Audit

**Date**: October 14, 2025, 2:17 PM  
**Phase**: VALID-1 (Serena Comprehensive Audit)  
**Duration**: 3-4 hours  
**Priority**: HIGH (Final verification phase)  
**Agent**: Code Agent

---

## Mission

Systematic verification of all GREAT epic completion claims using Serena MCP symbolic analysis. This is comprehensive validation that our 99%+ completion claims are accurate.

**Context**: Phase -1 confirmed system state stable. Now performing deep Serena audit of all GREAT epics to verify claims match reality.

**Philosophy**: "This is VALIDATION not DISCOVERY. We expect to confirm excellence, not find problems."

---

## Three-Part Structure

### Part 1.1: GREAT Epic Verification (2 hours)
Systematic audit of all 10 GREAT epics (1, 2, 3, 4A-F, 5)

### Part 1.2: Architectural Verification (1 hour)  
Verify key architectural patterns and integrations

### Part 1.3: Audit Report Generation (1 hour)
Create comprehensive verification report with findings

---

## Part 1.1: GREAT Epic Verification (2 hours)

### Epic List to Audit

1. **GREAT-1**: QueryRouter Resurrection
2. **GREAT-2**: Spatial Intelligence Integration  
3. **GREAT-3**: Plugin Architecture
4. **GREAT-4A**: Intent Classification (closed via #212)
5. **GREAT-4B**: Interface Enforcement
6. **GREAT-4C**: Multi-User Concurrent Sessions
7. **GREAT-4D**: Canonical Handler Implementation
8. **GREAT-4E**: Test Infrastructure  
9. **GREAT-4F**: Classification Accuracy
10. **GREAT-5**: Performance Optimization

### Verification Process for Each Epic

For each epic, perform the following using Serena MCP:

#### Step 1: Find Documentation Claims

```python
# Use Serena to find completion documentation
mcp__serena__search_project(
    query="GREAT-X complete AND GREAT-X finished",
    file_pattern="*.md",
    max_results=5
)

# Look for specific completion reports
mcp__serena__search_project(
    query="GREAT-X-epic-completion OR GREAT-X-COMPLETE",
    file_pattern="*.md"
)
```

**Extract from docs**:
- Claimed completion percentage
- Claimed file count
- Claimed test count  
- Claimed line count
- Key deliverables listed

#### Step 2: Verify Implementation

```python
# Find actual implementation files
mcp__serena__list_dir("services/")
mcp__serena__list_dir("tests/")

# For key components, verify structure
mcp__serena__find_symbol(
    name_regex="QueryRouter|SpatialIntelligence|PluginBase|etc",
    include_body=True
)

# Count actual files
# Use bash: find services/ -name "*router*" -o -name "*spatial*" | wc -l

# Count actual tests
# Use bash: grep -r "def test_" tests/ --include="*.py" | wc -l
```

**Measure actual**:
- Actual implementation files
- Actual test files
- Actual line counts (use `wc -l`)
- Actual classes/methods (Serena symbols)

#### Step 3: Compare Claims vs Reality

Create comparison table:

| Metric | Claimed | Actual | Match? | Gap % |
|--------|---------|--------|--------|-------|
| Completion | 99%+ | XX% | ✅/⚠️ | X% |
| Files | X | Y | ✅/⚠️ | - |
| Tests | X | Y | ✅/⚠️ | - |
| Lines | X | Y | ✅/⚠️ | - |

**Thresholds**:
- ✅ Match: Within 5% (claims accurate)
- ⚠️ Minor gap: 5-10% difference (note but acceptable)
- ❌ Major gap: >10% difference (investigate)

#### Step 4: Evidence Collection

For each epic, document:
- Documentation location (file paths)
- Implementation location (file paths)
- Serena query results
- Bash verification commands used
- Comparison results

---

### Epic-Specific Guidance

#### GREAT-1 (QueryRouter)
**Key claims to verify**:
- QueryRouter class exists (services/queries/query_router.py)
- ~935 lines total
- 9 lock tests in tests/regression/test_queryrouter_lock.py
- Integration with OrchestrationEngine

**Serena queries**:
```python
mcp__serena__find_symbol(name_regex="QueryRouter", include_body=True)
mcp__serena__find_symbol(name_regex="test_queryrouter.*", include_body=True)
```

#### GREAT-2 (Spatial)
**Key claims to verify**:
- 8 Slack spatial files (corrected from "20+")
- 21 spatial test files
- Spatial intelligence integration patterns

**Check**:
```bash
find services/integrations/slack/spatial/ -name "*.py" | wc -l  # Should be 8
find tests/spatial/ -name "test_*.py" | wc -l  # Should be ~21
```

#### GREAT-3 (Plugins)
**Key claims to verify**:
- 4 plugin wrappers (GitHub, Slack, Notion, Calendar)
- 92 contract tests (23 methods × 4 plugins)
- Plugin architecture documentation

**Serena queries**:
```python
mcp__serena__list_dir("services/integrations/")
# Should show: github/, slack/, notion/, calendar/

mcp__serena__search_project(
    query="contract test AND plugin",
    file_pattern="test_*.py"
)
```

#### GREAT-4 (Intent Classification - Multiple Sub-Epics)
**GREAT-4A**: Closed via #212 (just note status)
**GREAT-4B**: Interface enforcement (verify 100% claim)
**GREAT-4C**: Multi-user tests (verify 25+ tests, isolation)
**GREAT-4D**: 10 canonical handlers (verify all implemented)
**GREAT-4E**: Test infrastructure (verify 2,336 tests)
**GREAT-4F**: 98.62% accuracy (verify documented baseline)

**Priority checks**:
```python
# GREAT-4D: Count handlers
mcp__serena__list_dir("services/handlers/canonical/")
# Should show 10+ handler files

# GREAT-4C: Find multi-user tests  
mcp__serena__search_project(
    query="multi-user OR concurrent session",
    file_pattern="test_*.py"
)

# GREAT-4E: Verify test count
# Bash: pytest --collect-only -q | tail -1
```

#### GREAT-5 (Performance)
**Key claims to verify**:
- 602,907 req/sec throughput
- 4 benchmarks in scripts/benchmark_performance.py
- 33 pytest tests + 4 benchmarks = 37 total
- 1,365 lines of performance documentation

**Check**:
```bash
# Find performance docs
find dev/2025/10/07/ -name "*GREAT-5*" 

# Count lines
wc -l dev/2025/10/07/CORE-GREAT-5-COMPLETE-100-PERCENT.md

# Verify benchmark script
ls -lh scripts/benchmark_performance.py
```

---

## Part 1.2: Architectural Verification (1 hour)

### Verify Key Architectural Patterns

#### 1. Router Pattern Implementation
```python
# Verify QueryRouter is operational
mcp__serena__find_symbol(name_regex="QueryRouter", include_body=True)

# Check integration with OrchestrationEngine
mcp__serena__search_project(
    query="QueryRouter AND handle_query_intent",
    file_pattern="*.py"
)

# Verify no architectural violations (from PROOF-7)
# Bash: grep -r "from.*adapters" services/ --include="*.py" | wc -l
# Should be 13 (all legitimate Spatial/MCP patterns)
```

#### 2. Spatial Intelligence Integration
```python
# Verify spatial patterns exist
mcp__serena__list_dir("services/integrations/slack/spatial/")

# Check spatial test coverage
mcp__serena__search_project(
    query="spatial intelligence test",
    file_pattern="test_*.py"
)
```

#### 3. Plugin Architecture
```python
# Verify plugin base class
mcp__serena__find_symbol(name_regex="PluginBase", include_body=True)

# Count plugin implementations
mcp__serena__list_dir("services/integrations/")
# Should show: github/, slack/, notion/, calendar/

# Verify contract tests
# Bash: find tests/plugins/contract/ -name "test_*.py" | wc -l
```

#### 4. Multi-User Isolation
```python
# Find session isolation tests
mcp__serena__search_project(
    query="session isolation AND multi-user",
    file_pattern="test_*.py"
)

# Verify session management
mcp__serena__find_symbol(name_regex="SessionManager", include_body=True)
```

#### 5. Performance Optimizations
```python
# Verify canonical handler fast-path
mcp__serena__find_symbol(
    name_regex="canonical_handler OR fast_path",
    include_body=True
)

# Check performance benchmarks exist
mcp__serena__search_project(
    query="benchmark performance",
    file_pattern="*.py"
)
```

### Architectural Integrity Checklist

- [ ] Router pattern: Implemented and integrated
- [ ] Spatial intelligence: Patterns present
- [ ] Plugin architecture: 4 plugins operational
- [ ] Multi-user isolation: Tests and implementation verified
- [ ] Performance optimizations: Canonical fast-path implemented
- [ ] No architectural violations: Clean architecture maintained (13 legitimate imports)

---

## Part 1.3: Audit Report Generation (1 hour)

### Create Comprehensive Report

**File**: `dev/2025/10/14/valid-1-serena-audit-report.md`

**Structure**:

```markdown
# VALID-1: Serena Comprehensive Audit Report

**Date**: October 14, 2025
**Duration**: [X] hours
**Method**: Serena MCP symbolic analysis + bash verification
**Status**: [COMPLETE]

---

## Executive Summary

Overall verified completion: **XX.X%**

**Key Finding**: [One sentence summary - expect: "All claims verified accurate, system in excellent shape"]

**Recommendation**: [Proceed to VALID-2 / Address minor gaps first]

---

## Overall Completion by Epic

| Epic | Claimed | Verified | Gap | Status |
|------|---------|----------|-----|--------|
| GREAT-1 | 99%+ | XX.X% | ±X% | ✅/⚠️/❌ |
| GREAT-2 | 99%+ | XX.X% | ±X% | ✅/⚠️/❌ |
| GREAT-3 | 99%+ | XX.X% | ±X% | ✅/⚠️/❌ |
| GREAT-4A | Closed | N/A | N/A | ✅ |
| GREAT-4B | 100% | XX.X% | ±X% | ✅/⚠️/❌ |
| GREAT-4C | 99%+ | XX.X% | ±X% | ✅/⚠️/❌ |
| GREAT-4D | 100% | XX.X% | ±X% | ✅/⚠️/❌ |
| GREAT-4E | 99%+ | XX.X% | ±X% | ✅/⚠️/❌ |
| GREAT-4F | 98.62% | XX.X% | ±X% | ✅/⚠️/❌ |
| GREAT-5 | 99%+ | XX.X% | ±X% | ✅/⚠️/❌ |

**Weighted Average**: XX.X% verified completion

---

## Detailed Epic Analysis

### GREAT-1: QueryRouter Resurrection

**Documentation Claims**:
- Completion: 99%+
- Files: [X claimed]
- Tests: 9 lock tests
- Lines: ~935 lines QueryRouter

**Serena Verification**:
- Implementation found: [Yes/No]
- Actual files: [X]
- Actual tests: [X]
- Actual lines: [X]

**Comparison**:
| Metric | Claimed | Actual | Match? | Gap % |
|--------|---------|--------|--------|-------|
| Completion | 99%+ | XX% | ✅ | ±X% |
| Files | X | Y | ✅ | - |
| Tests | 9 | Z | ✅ | - |
| Lines | 935 | W | ✅ | - |

**Evidence**:
- Documentation: [file paths]
- Implementation: [file paths]
- Serena queries: [commands used]
- Bash verification: [commands used]

**Assessment**: ✅ Verified accurate / ⚠️ Minor discrepancy / ❌ Major gap

**Notes**: [Any observations or context]

---

[Repeat this structure for each of the 10 GREAT epics]

---

## Architectural Verification Results

### Router Pattern
**Status**: ✅ Verified / ⚠️ Partial / ❌ Issues
**Evidence**: [Serena queries + findings]

### Spatial Intelligence
**Status**: ✅ Verified / ⚠️ Partial / ❌ Issues
**Evidence**: [Serena queries + findings]

### Plugin Architecture
**Status**: ✅ Verified / ⚠️ Partial / ❌ Issues
**Evidence**: [Serena queries + findings]

### Multi-User Isolation
**Status**: ✅ Verified / ⚠️ Partial / ❌ Issues
**Evidence**: [Serena queries + findings]

### Performance Optimizations
**Status**: ✅ Verified / ⚠️ Partial / ❌ Issues
**Evidence**: [Serena queries + findings]

---

## Key Findings

### Strengths (What's Working)
1. [List verified strengths]
2. [Documentation accuracy highlights]
3. [Implementation quality observations]

### Discrepancies (If Any)
1. [Any gaps found between claims and reality]
2. [Context for discrepancies]
3. [Whether blocking or non-blocking]

### Recommendations
1. [Immediate actions if any gaps found]
2. [Optional improvements for future]
3. [Next steps for VALID-2]

---

## Verification Methodology

**Tools Used**:
- Serena MCP Server (symbolic code analysis)
- Bash commands (file counting, line counting)
- Direct file inspection (verification)

**Queries Executed**: [Total count]

**Files Analyzed**: [Total count]

**Time Invested**: [X] hours

---

## Confidence Assessment

**Overall Confidence**: High / Medium / Low

**Rationale**: [Why this confidence level - expect high based on Phase -1 results]

---

## Next Steps

### VALID-2 Preparation
- [ ] Verified completion ≥95% (if yes, proceed to VALID-2)
- [ ] Any critical gaps addressed
- [ ] MVP workflow list prepared for testing

### If Gaps Found
- [ ] Document gaps clearly
- [ ] Assess impact (blocking vs non-blocking)
- [ ] Create remediation plan if needed

---

## Appendix: Detailed Verification Data

[Include raw data tables, Serena query outputs, bash command results]

---

**Audit Complete**: October 14, 2025, [timestamp]
**Total Duration**: [X] hours
**Method**: Serena MCP + Bash verification
**Status**: VALID-1 Complete ✅

---

*"Trust, but verify. Then document the verification."*
*- VALID-1 Philosophy*
```

---

## Commit Strategy

```bash
# Stage the audit report
git add dev/2025/10/14/valid-1-serena-audit-report.md

# Commit
git commit -m "docs(VALID-1): Serena comprehensive audit complete

Systematic verification of all GREAT epic completion claims.

Results:
- Overall completion: XX.X% verified
- GREAT epics audited: 10 (1, 2, 3, 4A-F, 5)
- Architecture verified: [status]
- Key findings: [summary]

Method:
- Serena MCP symbolic analysis
- Bash verification commands
- Direct file inspection
- Cross-document validation

Evidence:
- [X] queries executed
- [Y] files analyzed
- [Z] hours invested

Status: ✅ VALID-1 Complete
Recommendation: [Proceed to VALID-2 / Address gaps]

Part of: CORE-CRAFT-VALID epic, Phase 1
Next: VALID-2 MVP integration testing"

# Push
git push origin main
```

---

## Success Criteria

### Part 1.1 Complete ✅
- [ ] All 10 GREAT epics audited
- [ ] Claims vs reality documented for each
- [ ] Completion percentages calculated
- [ ] Discrepancies noted (if any)

### Part 1.2 Complete ✅
- [ ] Architectural patterns verified
- [ ] Integration points checked
- [ ] Quality maintained
- [ ] No violations found

### Part 1.3 Complete ✅
- [ ] Comprehensive report created
- [ ] Evidence documented
- [ ] Findings summarized
- [ ] Recommendations provided

### VALID-1 Complete ✅
- [ ] ≥95% verified completion (target)
- [ ] No critical gaps blocking VALID-2
- [ ] All evidence compiled
- [ ] Clean commit made

---

## Time Budget

**Target**: 3-4 hours total

**Part 1.1** (Epic Verification): 2 hours
- ~10-15 min per epic × 10 epics = 2 hours
- Quick verification per epic, not deep dive

**Part 1.2** (Architecture): 1 hour
- ~10-15 min per pattern × 5 patterns = 1 hour

**Part 1.3** (Report): 1 hour
- Compile findings: 30 min
- Write report: 30 min

**Buffer**: None needed (generous time per phase)

**Target Completion**: ~5:30-6:30 PM

---

## What NOT to Do

- ❌ Don't get stuck on minor discrepancies (note and move on)
- ❌ Don't re-implement anything (this is verification only)
- ❌ Don't run tests (Phase -1 already verified)
- ❌ Don't run benchmarks (save for VALID-2)
- ❌ Don't investigate gaps deeply (just document them)

## What TO Do

- ✅ Systematic verification of all 10 epics
- ✅ Use Serena for code structure analysis
- ✅ Use bash for counts and measurements
- ✅ Document findings clearly
- ✅ Create comprehensive report
- ✅ Note any discrepancies without judgment
- ✅ Provide clear recommendation for VALID-2

---

## Context

**Why VALID-1 Matters**:
- Final systematic verification of CORE-CRAFT completion
- Confirm 99%+ completion claims are accurate
- Build confidence for VALID-2 integration testing
- Create evidence package for handoff

**What Comes After**:
- VALID-2: MVP integration testing (3-4 hours)
- VALID-3: Evidence compilation (2-3 hours)
- CORE-CRAFT epic closure! 🎉

**This Phase**: Deep dive verification to confirm excellence! ✅

---

**VALID-1 Start Time**: 2:17 PM  
**Expected Completion**: ~5:30-6:30 PM (3-4 hours)  
**Status**: Ready for Code Agent execution

**LET'S VERIFY OUR EXCELLENCE!** 🔍✨

---

*"Verification builds confidence. Confidence enables velocity."*  
*- VALID-1 Philosophy*
