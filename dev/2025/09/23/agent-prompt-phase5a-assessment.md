# Agent Prompt: Rapid GREAT-1C Phase Assessment

## Mission
Quickly assess status of Locking, Documentation, and Verification phases (30 minutes total). Find what's complete, what's missing, what's easy wins.

## Context
Chief Architect ruling: Focus on infrastructure completion and regression fixes. Test quality improvements are separate work.

**Already Complete**:
- ✅ Testing Phase infrastructure (tests collect and execute)
- ✅ Import debt cleared
- ✅ Constructor bugs fixed

**Need to assess**: Locking, Documentation, Verification phases

## Assessment Tasks

### LOCKING PHASE (5 checkboxes)

**Checkbox 1: CI/CD pipeline fails if QueryRouter disabled**
```bash
# Check CI/CD workflows
ls -la .github/workflows/
cat .github/workflows/*.yml | grep -i "test\|pytest" -A 5

# Do QueryRouter regression tests run in CI?
grep -r "test_queryrouter_lock" .github/workflows/
```
Status: [EXISTS | MISSING | PARTIAL]

**Checkbox 2: Initialization test prevents commented-out code**
```bash
# We know these exist from earlier work
grep -l "test.*commented.*out\|test.*initialization" tests/regression/test_queryrouter_lock.py
```
Status: [EXISTS ✅ | MISSING]

**Checkbox 3: Performance regression test alerts on degradation**
```bash
# Check for performance regression tests
grep -r "test.*performance.*regression\|test.*degradation" tests/ --include="*.py" -l
grep -r "<500ms\|threshold" tests/performance/ --include="*.py"
```
Status: [EXISTS | MISSING | PARTIAL]

**Checkbox 4: Required test coverage for orchestration module**
```bash
# Check coverage config
cat .coveragerc 2>/dev/null
cat pyproject.toml | grep -A 10 coverage 2>/dev/null

# Check if coverage is enforced
grep -r "coverage" .github/workflows/ 2>/dev/null
```
Status: [EXISTS | MISSING | PARTIAL]

**Checkbox 5: Pre-commit hooks catch disabled components**
```bash
# Check pre-commit setup
ls -la .pre-commit-config.yaml .git/hooks/pre-commit 2>/dev/null
cat .pre-commit-config.yaml 2>/dev/null | head -20
```
Status: [EXISTS | MISSING | NOT_SETUP]

### DOCUMENTATION PHASE (5 checkboxes)

**Checkbox 1: Update architecture.md with current flow**
```bash
# Check if architecture.md reflects QueryRouter
grep -i "queryrouter\|orchestration.*engine" docs/*/architecture*.md
git log --oneline -- docs/*/architecture*.md | head -5
```
Status: [UPDATED | NEEDS_UPDATE | UNKNOWN]

**Checkbox 2: Remove or update misleading TODO comments**
```bash
# Count TODOs without issue numbers
grep -r "TODO" . --include="*.py" | grep -v "#[0-9]" | wc -l
grep -r "TODO.*queryrouter\|TODO.*orchestration" . --include="*.py"
```
Status: [CLEAN | NEEDS_WORK] (count: X)

**Checkbox 3: Document initialization sequence**
```bash
# Check for initialization docs
find docs/ -name "*init*" -o -name "*startup*" -o -name "*sequence*"
grep -r "initialization.*sequence\|startup.*flow" docs/
```
Status: [EXISTS | MISSING]

**Checkbox 4: Update ADR-032 implementation status**
```bash
# Check ADR-032 content
find docs/ -name "*ADR-032*" -o -name "*032*"
grep -i "implementation.*status\|status.*complete" docs/*/adrs/*032* 2>/dev/null
```
Status: [UPDATED | NEEDS_UPDATE | UNKNOWN]

**Checkbox 5: Add troubleshooting guide for common issues**
```bash
# Check for troubleshooting docs
find docs/ -name "*troubleshoot*"
grep -i "queryrouter\|orchestration" docs/troubleshoot* 2>/dev/null
```
Status: [EXISTS | MISSING | PARTIAL]

### VERIFICATION PHASE (5 checkboxes)

**Checkbox 1: Fresh clone and setup works without issues**
```bash
# Check setup documentation
ls -la README.md INSTALL.md setup.py requirements.txt
grep -i "install\|setup\|clone" README.md | head -10
```
Status: [DOCUMENTED | NEEDS_TEST | UNKNOWN]

**Checkbox 2: New developer can understand orchestration flow**
```bash
# Check for developer documentation
find docs/ -name "*developer*" -o -name "*onboard*" -o -name "*getting*start*"
grep -r "orchestration.*flow\|queryrouter.*usage" docs/
```
Status: [DOCUMENTED | NEEDS_WORK | MISSING]

**Checkbox 3: All tests pass in CI/CD pipeline**
```bash
# Check latest CI run status
gh run list --limit 5 2>/dev/null || echo "GitHub CLI not available"
cat .github/workflows/*.yml | grep -i "fail\|success" | head -5
```
Status: [PASSING | FAILING | UNKNOWN]

**Checkbox 4: No remaining TODO comments without issue numbers**
```bash
# Already checked in Documentation Phase
# Report same count
```
Status: [CLEAN | NEEDS_WORK] (count: X)

**Checkbox 5: Performance benchmarks documented**
```bash
# Check for benchmark documentation
find docs/ -name "*performance*" -o -name "*benchmark*"
grep -r "benchmark.*result\|performance.*baseline" docs/
```
Status: [DOCUMENTED | MISSING]

## Evidence Format

For each phase, provide:

**LOCKING PHASE**:
```
Checkbox 1 (CI/CD): [EXISTS ✅ | MISSING ❌ | PARTIAL ⚠️]
Checkbox 2 (Init test): [EXISTS ✅ | MISSING ❌]
Checkbox 3 (Perf regression): [EXISTS ✅ | MISSING ❌ | PARTIAL ⚠️]
Checkbox 4 (Coverage): [EXISTS ✅ | MISSING ❌ | PARTIAL ⚠️]
Checkbox 5 (Pre-commit): [EXISTS ✅ | MISSING ❌]

Quick wins: [list any easy completions]
Blockers: [list any hard requirements]
```

**DOCUMENTATION PHASE**:
```
Checkbox 1 (architecture.md): [UPDATED ✅ | NEEDS_UPDATE ❌]
Checkbox 2 (TODOs): [CLEAN ✅ | NEEDS_WORK ❌] (X without issues)
Checkbox 3 (Init sequence): [EXISTS ✅ | MISSING ❌]
Checkbox 4 (ADR-032): [UPDATED ✅ | NEEDS_UPDATE ❌]
Checkbox 5 (Troubleshooting): [EXISTS ✅ | MISSING ❌ | PARTIAL ⚠️]

Quick wins: [list any easy completions]
Effort needed: [estimate for missing work]
```

**VERIFICATION PHASE**:
```
Checkbox 1 (Fresh clone): [DOCUMENTED ✅ | NEEDS_TEST ❌]
Checkbox 2 (Developer docs): [DOCUMENTED ✅ | NEEDS_WORK ❌]
Checkbox 3 (CI passing): [PASSING ✅ | FAILING ❌]
Checkbox 4 (TODOs): [same as Documentation]
Checkbox 5 (Benchmarks): [DOCUMENTED ✅ | MISSING ❌]

Quick wins: [list any easy completions]
Blockers: [list any dependencies]
```

## Success Criteria
- Fast assessment (30 min total)
- Clear status for each checkbox
- Identify low-hanging fruit
- Spot major blockers

## Time Management
- Locking: 10 minutes
- Documentation: 10 minutes
- Verification: 10 minutes
- Don't deep dive - just assess status

Report findings with checkbox tallies and recommended next actions.
