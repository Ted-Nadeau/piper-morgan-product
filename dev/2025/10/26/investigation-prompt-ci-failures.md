# Investigation Prompt: CI/CD Test Failures - PR Merge Blockers

**Date**: Sunday, October 26, 2025, 7:20 AM PT
**Priority**: HIGH - Blocking PR merge
**Recommended Agent**: Cursor (systematic investigation) or Code (quick fixes)

---

## Context

Sprint A8 completed successfully yesterday with all 5 issues done and 76+ tests passing locally. However, the PR from `piper-reviewer` account is failing 5 CI/CD checks. We need to investigate and fix these failures before approving the merge.

**Local Testing Status**: All tests passing ✅
**CI/CD Status**: 5 failures ❌

---

## Your Mission

Investigate each failing CI/CD check, identify root causes, and propose fixes. Work systematically through each failure, providing evidence and solutions.

---

## Failing Checks to Investigate

### 1. Configuration Validation (Failed after 16s)

**Check**: `Validate Service Configurations`

**Investigation Steps**:
```bash
# Find the workflow file
find .github/workflows -name "*config*" -o -name "*validation*"
cat .github/workflows/[relevant-file].yml

# Check what this validates
grep -r "Validate Service" .github/workflows/

# Look for configuration files that might be invalid
find . -name "config.yml" -o -name "*.config.json" -o -name "PIPER.*.md"

# Test configuration validation locally
# [command from workflow]
```

**Questions**:
- What configuration files does this check validate?
- What validation rules are failing?
- Did Sprint A8 changes introduce new config requirements?

---

### 2. Docker Build (Failed after 23s)

**Check**: `docker (pull_request)`

**Investigation Steps**:
```bash
# Find Docker workflow
cat .github/workflows/docker*.yml

# Check Dockerfile
cat Dockerfile

# Look for Docker-related changes in recent commits
git log --oneline -20 --all -- Dockerfile docker-compose.yml

# Try building locally
docker build -t piper-morgan-test .

# Check for missing dependencies or syntax errors
docker-compose config
```

**Questions**:
- What changed in Docker configuration?
- Are there missing dependencies?
- Are there syntax errors in Dockerfile?
- Did new dependencies get added without updating requirements?

---

### 3. Documentation Link Checker (Failed after 3s)

**Check**: `Check documentation links`

**Investigation Steps**:
```bash
# Find link checker workflow
cat .github/workflows/*doc*.yml

# Find the link checker script
find . -name "*link*check*" -o -name "*doc*check*"

# Check recent documentation changes
git log --oneline -20 --all -- docs/

# Look for broken links
grep -r "\[.*\](.*)" docs/ | grep -E "(http|\.md)" > /tmp/links.txt

# Common broken link patterns
grep -r "]\(" docs/ | grep -E "(TODO|FIXME|XXX)"
```

**Questions**:
- Which links are broken?
- Are they internal (relative) or external links?
- Did Sprint A8 add new documentation with bad links?

**Common Issues**:
- Renamed files without updating links
- Dead external URLs
- Incorrect relative paths
- Case sensitivity issues

---

### 4. Router Pattern Enforcement (Failed after 13s)

**Check**: `Architectural Protection Checks`

**Investigation Steps**:
```bash
# Find the enforcement workflow
cat .github/workflows/*router*.yml

# Check what this enforces
find . -name "*router*enforcement*" -o -name "*architectural*check*"

# Look for router-related changes
git log --oneline -20 --all -- "*router*" "*route*"

# Check for direct imports that might be forbidden
grep -r "from.*router.*import" --include="*.py" | grep -v test

# Check router patterns
find . -path "*/routers/*" -name "*.py"
```

**Questions**:
- What architectural patterns is this enforcing?
- Did Sprint A8 introduce router changes?
- Are there forbidden import patterns?
- Is this related to the QueryRouter mentioned in recent ADRs?

**Context from Sprint A8**:
- ADR-036 mentions QueryRouter resurrection
- Check if recent changes violate router patterns

---

### 5. Tests / test (Failed after 40s)

**Check**: `test (pull_request)`

**Investigation Steps**:
```bash
# Find the test workflow
cat .github/workflows/test*.yml

# Run the exact CI test command locally
# (extract from workflow file)

# Check for test failures
pytest --tb=short --maxfail=5

# Look for new tests added in Sprint A8
git diff origin/main-old..origin/main -- tests/

# Check for import errors or missing dependencies
pytest --collect-only

# Check for database/environment issues
pytest tests/ -v --tb=short 2>&1 | grep -A 5 "FAILED\|ERROR"
```

**Questions**:
- Which specific tests are failing?
- Are they new tests from Sprint A8?
- Environment differences (CI vs local)?
- Missing CI environment variables?

**Sprint A8 Tests Added**:
- Issue #268: 4 tests (key validation)
- Issue #269: 17 tests (personality preferences)
- Issue #271: 15 tests (cost tracking)
- Issue #278: 40 tests (knowledge graph)

---

## Investigation Protocol

### Step 1: Gather Evidence

For EACH failing check:

1. **Find the workflow file**:
   ```bash
   ls -la .github/workflows/
   cat .github/workflows/[relevant-file].yml
   ```

2. **Extract the exact command that's failing**:
   - Look in the workflow YAML
   - Note any environment variables
   - Note any setup steps

3. **Run locally**:
   ```bash
   # Try to reproduce the failure
   [exact command from workflow]
   ```

4. **Capture output**:
   ```bash
   # Save failure output to file
   [command] 2>&1 | tee /tmp/ci-failure-[check-name].log
   ```

### Step 2: Analyze Root Cause

For each failure, determine:

- **What changed?** (Git diff analysis)
- **Why is CI different from local?** (Environment, dependencies, etc.)
- **Is it a real issue or CI configuration problem?**

### Step 3: Propose Fix

For each failure, provide:

```markdown
## Fix for: [Check Name]

**Root Cause**: [Clear explanation]

**Evidence**:
- [Log output]
- [Git diff showing relevant changes]
- [File references]

**Proposed Fix**:
```bash
# Exact commands or file changes
```

**Testing**:
```bash
# How to verify the fix works
```

**Risk Assessment**: [Low/Medium/High]
```

---

## Systematic Investigation Order

**Recommended Order** (fastest to slowest):

1. **Documentation Link Checker** (3s failure - quick to fix)
   - Usually just broken links
   - Easy to identify and fix

2. **Configuration Validation** (16s - likely config syntax)
   - Check YAML/JSON syntax
   - Validate against schemas

3. **Router Pattern Enforcement** (13s - architectural check)
   - Check import patterns
   - Verify router structure

4. **Docker Build** (23s - dependency or syntax issue)
   - Check Dockerfile syntax
   - Verify dependencies

5. **Tests / test** (40s - most complex)
   - Run specific failing tests
   - Check environment differences

---

## Tools and Commands

### Git Investigation
```bash
# See what changed in Sprint A8
git diff origin/main-old..origin/main --stat

# Files changed in last 10 commits
git diff --name-only origin/main~10..origin/main

# Search for specific patterns
git log --all --grep="config\|docker\|router" --oneline
```

### Workflow Debugging
```bash
# List all workflows
ls -la .github/workflows/

# Check workflow syntax
actionlint .github/workflows/*.yml

# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('.github/workflows/test.yml'))"
```

### Local CI Simulation
```bash
# Install act (GitHub Actions locally)
brew install act  # or appropriate package manager

# Run specific workflow locally
act -j test
act -j docker
```

### Test Debugging
```bash
# Run with verbose output
pytest tests/ -v --tb=long

# Run specific test file
pytest tests/integration/test_knowledge_graph_enhancement.py -v

# Show which tests are collected
pytest --collect-only

# Run with pdb on failure
pytest --pdb
```

---

## Common CI/CD Issues and Solutions

### Issue: Environment Variables Missing

**Symptom**: Tests pass locally, fail in CI

**Fix**:
```yaml
# Add to workflow file
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
  ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

### Issue: Dependencies Missing

**Symptom**: Import errors in CI

**Fix**:
```bash
# Update requirements
pip freeze > requirements.txt

# Or update pyproject.toml
poetry export -f requirements.txt --output requirements.txt
```

### Issue: Python Version Mismatch

**Symptom**: Syntax or feature not supported

**Fix**:
```yaml
# Check workflow Python version matches local
python-version: '3.9'  # Match to local version
```

### Issue: Database Not Running

**Symptom**: Database connection errors

**Fix**:
```yaml
# Add service container to workflow
services:
  postgres:
    image: postgres:15
    env:
      POSTGRES_PASSWORD: postgres
```

### Issue: File Path Issues

**Symptom**: File not found errors

**Fix**:
```bash
# Use absolute paths in tests
# Or ensure working directory is correct
```

---

## Expected Deliverables

### 1. Investigation Report

```markdown
# CI/CD Failure Investigation Report

## Summary
- Total failures: 5
- Root causes identified: X
- Fixes proposed: X
- Estimated fix time: X minutes

## Detailed Findings

### [Check 1 Name]
**Status**: ❌ Failing
**Root Cause**: [Explanation]
**Evidence**: [Logs/diffs]
**Fix**: [Solution]
**Testing**: [Verification steps]

[Repeat for each check]

## Recommended Action Plan
1. [Fix in priority order]
2. [...]
```

### 2. Fix Implementation

For each failure, provide:
- Exact file changes (diffs)
- Commands to run
- Verification steps
- Commit message

### 3. Testing Verification

```bash
# Commands to verify all fixes work
[list of verification commands]

# Expected output
[what success looks like]
```

---

## Success Criteria

- [ ] All 5 failing checks identified and understood
- [ ] Root cause determined for each failure
- [ ] Fixes proposed with evidence
- [ ] Local reproduction of failures (if possible)
- [ ] Local verification of fixes
- [ ] PR ready to merge after fixes applied

---

## Notes

**Sprint A8 Context**:
- All tests passing locally (76+ tests)
- Recent changes:
  - Issue #268: Key validation
  - Issue #269: Personality preferences (semantic bridge)
  - Issue #271: Cost tracking integration
  - Issue #278: Knowledge graph enhancement
- Git history cleaned (removed secrets)
- Main branch renamed (main-old → main)

**Time Constraint**: Need to fix before PR can be merged

**Priority**: HIGH - Blocking production deployment

---

*Investigation Protocol Version: 1.0*
*Created: Sunday, October 26, 2025, 7:20 AM PT*
*For: Cursor or Code Agent*
