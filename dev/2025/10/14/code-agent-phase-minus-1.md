# Code Agent Prompt: VALID Phase -1 - Pre-Validation Check

**Date**: October 14, 2025, 1:51 PM  
**Phase**: VALID Phase -1 (Pre-Validation Check)  
**Duration**: 15 minutes  
**Priority**: HIGH (Gateway to VALID-1)  
**Agent**: Code Agent

---

## Mission

Quick verification that all claimed system states are accurate before beginning systematic VALID-1 audit. This is a sanity check to ensure we're starting from solid ground.

**Context**: About to begin final CORE-CRAFT-VALID phase. Need to verify current state claims before Serena comprehensive audit.

---

## Critical Checks (15 minutes)

### Check 1: Test Count Verification (3 min)

**Claim**: 2,336 tests total, 100% passing

```bash
# Count all tests
pytest --collect-only -q 2>/dev/null | tail -1

# Should show: "2336 tests collected" or similar

# Quick validation run (optional, may be slow)
# pytest tests/regression/ -v --tb=short
```

**Document**:
- Total test count: [X]
- Matches claim? [Yes/No]
- If different, note actual count

---

### Check 2: CI/CD Status Verification (3 min)

**Claim**: 13/13 workflows operational (100%)

```bash
# Count workflow files
find .github/workflows/ -name "*.yml" -type f | wc -l

# Should show: 13

# List all workflows
ls -1 .github/workflows/
```

**Document**:
- Total workflows: [X]
- Matches claim? [Yes/No]
- All workflow files listed

**Note**: Can't check GitHub Actions status from CLI, but file count verification is sufficient for Phase -1.

---

### Check 3: Serena MCP Operational (2 min)

**Verify Serena is working**:

```bash
# Check if Serena server is in system
which serena 2>/dev/null || echo "Serena not in PATH (may be in package)"

# Try to import in Python
python3 -c "from mcp_server_serena import mcp_serena_server; print('Serena: OK')" 2>/dev/null || echo "Import check skipped"

# Alternative: Check if we have the serena MCP files
find . -name "*serena*" -type f 2>/dev/null | head -5
```

**Document**:
- Serena accessible? [Yes/No/Unclear]
- Method: [PATH/Python import/Files found]

**Note**: Serena runs as MCP server, so basic check is sufficient. Will be tested properly in VALID-1.

---

### Check 4: Performance Baseline Check (3 min)

**Claim**: 602,907 req/sec baseline

```bash
# Check if benchmark script exists
ls -lh scripts/benchmark_performance.py

# Check recent benchmark results (if any)
find dev/2025/10/ -name "*benchmark*" -o -name "*performance*" | head -5

# Read most recent GREAT-5 completion report for baseline
grep -A5 "602,907\|req/sec" dev/2025/10/07/CORE-GREAT-5-COMPLETE-100-PERCENT.md | head -10
```

**Document**:
- Benchmark script exists? [Yes/No]
- Baseline documented? [Yes/No]
- Source: [File location]

**Note**: Not running actual benchmark (takes time), just verifying baseline is documented.

---

### Check 5: Documentation Accuracy Claims (2 min)

**Claim**: 99%+ accuracy across GREAT epics

```bash
# Check PROOF completion reports exist
find dev/2025/10/14/ -name "proof-*-completion.md" | wc -l

# Should show: 5 (PROOF-2,4,5,6,7)

# Check Stage 3 summary exists
ls -lh dev/2025/10/14/stage-3-precision-complete.md
```

**Document**:
- PROOF reports found: [X]
- Stage 3 summary exists? [Yes/No]
- Evidence trail complete? [Yes/No]

---

### Check 6: MVP Workflow Implementations (2 min)

**Quick check for key handlers**:

```bash
# Check greeting handler
grep -r "handle_greeting\|GREETING" services/handlers/ --include="*.py" | head -3

# Check GitHub integration
grep -r "handle_create_issue\|github" services/handlers/ --include="*.py" | head -3

# Check file operations
grep -r "handle_upload\|handle_analyze" services/handlers/ --include="*.py" | head -3

# Count total handlers
find services/handlers/ -name "handle_*.py" -o -name "*_handler.py" | wc -l
```

**Document**:
- Greeting handler: [Found/Not found]
- GitHub handler: [Found/Not found]
- File handlers: [Found/Not found]
- Total handler files: [X]

**Note**: Not testing execution, just verifying files exist for VALID-2.

---

## Quick Summary Report

Create quick summary:

```bash
# Create summary file
cat > /tmp/phase-minus-1-results.txt << 'EOF'
# Phase -1 Pre-Validation Results

## Date: October 14, 2025, ~2:05 PM

### Verification Results

1. **Test Count**: [X tests] - [Matches/Different from 2,336 claim]
2. **CI/CD Workflows**: [X files] - [Matches/Different from 13 claim]
3. **Serena MCP**: [Accessible/Not accessible/Unclear]
4. **Performance Baseline**: [Documented/Not found] at [location]
5. **Documentation**: [X PROOF reports] - [Complete/Incomplete]
6. **MVP Handlers**: [X handlers found] - [Key handlers present/missing]

### Overall Status: [READY/ISSUES FOUND]

### Notes:
- [Any discrepancies or concerns]
- [Any items needing attention before VALID-1]

### Recommendation:
- [Proceed to VALID-1 / Address issues first]

EOF

cat /tmp/phase-minus-1-results.txt
```

---

## Completion Report

Create actual report file:

```bash
# Move to proper location
cp /tmp/phase-minus-1-results.txt dev/2025/10/14/phase-minus-1-pre-validation-check.md

# Add timestamp
echo "" >> dev/2025/10/14/phase-minus-1-pre-validation-check.md
echo "**Completed**: $(date '+%Y-%m-%d %I:%M %p')" >> dev/2025/10/14/phase-minus-1-pre-validation-check.md
echo "**Duration**: ~15 minutes" >> dev/2025/10/14/phase-minus-1-pre-validation-check.md
echo "**Status**: Phase -1 Complete ✅" >> dev/2025/10/14/phase-minus-1-pre-validation-check.md
```

---

## Commit Strategy

```bash
# Stage the report
git add dev/2025/10/14/phase-minus-1-pre-validation-check.md

# Commit
git commit -m "docs(VALID): Phase -1 pre-validation check complete

Quick verification of system state before VALID-1 audit.

Verified:
- Test count: [X tests]
- CI/CD workflows: [X files]
- Serena MCP: [status]
- Performance baseline: [documented]
- Documentation trail: [complete]
- MVP handlers: [X found]

Overall Status: [READY/ISSUES]

Part of: CORE-CRAFT-VALID epic, Phase -1
Next: VALID-1 Serena comprehensive audit"

# Push
git push origin main
```

---

## Success Criteria

### Checks Complete ✅
- [ ] Test count verified
- [ ] CI/CD workflows verified
- [ ] Serena accessibility checked
- [ ] Performance baseline documented
- [ ] Documentation trail verified
- [ ] MVP handlers checked

### Report Created ✅
- [ ] Summary generated
- [ ] Results documented
- [ ] Status assessment made
- [ ] Recommendation provided

### Committed ✅
- [ ] Report file created
- [ ] Git commit made
- [ ] Pushed to main

### Ready for VALID-1 ✅
- [ ] All claims verified or discrepancies noted
- [ ] System state baseline established
- [ ] Green light to proceed or issues flagged

---

## Expected Results

**If Everything Matches**:
- Test count: 2,336 ✅
- CI/CD: 13 workflows ✅
- Serena: Accessible ✅
- Baselines: Documented ✅
- Documentation: Complete ✅
- Handlers: Present ✅
- **Status**: READY for VALID-1 ✅

**If Discrepancies Found**:
- Document clearly
- Note if blocking or non-blocking
- Recommend action (proceed or address first)

---

## Time Budget

**Target**: 15 minutes total
- Check 1 (Tests): 3 min
- Check 2 (CI/CD): 3 min
- Check 3 (Serena): 2 min
- Check 4 (Performance): 3 min
- Check 5 (Docs): 2 min
- Check 6 (Handlers): 2 min
- Summary: 5 min
- Commit: 5 min

**Buffer**: +5 min for any issues

**Target Completion**: ~2:10 PM

---

## What NOT to Do

- ❌ Don't run full test suite (too slow)
- ❌ Don't run actual benchmarks (save for VALID-2)
- ❌ Don't test handler execution (that's VALID-2)
- ❌ Don't run Serena audit yet (that's VALID-1)
- ❌ Don't investigate discrepancies deeply (just note them)

## What TO Do

- ✅ Quick file counts and greps
- ✅ Verify claims match reality
- ✅ Document what you find
- ✅ Make go/no-go recommendation
- ✅ Create clean commit

---

## Context

**Why Phase -1 Matters**:
- Ensures we're starting from accurate baseline
- Catches any drift since PROOF completion
- Validates readiness for comprehensive VALID-1 audit
- Quick confidence check before major work

**What Comes After**:
- VALID-1: Serena comprehensive audit (3-4 hours)
- VALID-2: MVP integration testing (3-4 hours)
- VALID-3: Evidence compilation (2-3 hours)

**This Phase**: Just the health check before the deep dive! ✅

---

**Phase -1 Start Time**: 1:51 PM  
**Expected Completion**: ~2:10 PM (15 minutes)  
**Status**: Ready for Code Agent execution

**LET'S VERIFY THE FOUNDATION!** 🔍✅

---

*"Measure twice, cut once. Verify first, audit second."*  
*- Phase -1 Philosophy*
