# Gameplan: CORE-GREAT-1C Evidence Gathering

**Date**: September 23, 2025
**Issue**: #187 - CORE-GREAT-1C (Evidence Collection)
**Architect**: Claude Opus 4.1
**Lead Developer**: [To be assigned]

---

## Context: Missing Evidence Problem

### Situation
GREAT-1C was marked complete but lacks evidence for most checkboxes. This violates our GitHub Progress Discipline where PM validates based on evidence.

### Mission
Gather evidence for completed work OR complete missing work, then provide evidence.

---

## Infrastructure Verification Checkpoint

### Expected from GREAT-1C Completion
```yaml
Expected Artifacts:
- Test files: tests/test_queryrouter.py or similar
- CI config: .github/workflows/ or .gitlab-ci.yml
- Pre-commit: .pre-commit-config.yaml
- Docs: Updated architecture.md, ADR-032
- Coverage: htmlcov/ or coverage reports
```

### PM Verification Required
```bash
# Check for test files
find tests/ -name "*queryrouter*" -o -name "*orchestration*" 2>/dev/null

# Check for CI configuration
ls -la .github/workflows/ .gitlab-ci.yml .circleci/ 2>/dev/null

# Check for pre-commit hooks
ls -la .pre-commit-config.yaml .git/hooks/pre-commit 2>/dev/null

# Check for coverage reports
ls -la htmlcov/ coverage.xml .coverage 2>/dev/null
```

---

## Phase 0: Investigation

### Both Agents
1. **Search for Created Tests**
   ```bash
   # Find any new test files
   find . -name "*.py" -newer /dev/null -mtime -2 | grep -i test

   # Look for lock tests
   grep -r "QueryRouter.*None" tests/ --include="*.py"
   grep -r "commented.*out" tests/ --include="*.py"
   ```

2. **Run Existing Tests**
   ```bash
   # Run orchestration tests
   PYTHONPATH=. python -m pytest tests/ -k orchestration -v

   # Check coverage
   PYTHONPATH=. python -m pytest tests/unit/services/test_orchestration.py --cov=services/orchestration --cov-report=term
   ```

---

## Phase 1: Evidence Collection OR Creation

### Deploy: Both Agents

#### If Tests EXIST - Claude Code
```markdown
For each test found:
1. Run it and capture output
2. Verify it actually tests QueryRouter locks
3. Generate coverage report
4. Document what it prevents

Provide full terminal output as evidence.
```

#### If Tests DON'T EXIST - Cursor
```markdown
Create the missing lock tests:

1. In tests/unit/services/test_orchestration_locks.py:
   - Test QueryRouter cannot be None
   - Test initialization cannot be commented
   - Test performance <500ms
   - Test coverage requirements

2. Run tests and capture output
3. Generate coverage report
```

---

## Phase 2: Documentation Evidence

### Both Agents

1. **Check Documentation Updates**
   ```bash
   # Check if architecture.md updated
   git diff HEAD~5 docs/internal/architecture/current/architecture.md

   # Check ADR-032
   git diff HEAD~5 docs/internal/architecture/current/adrs/ADR-032*

   # Count TODOs without issue numbers
   grep -r "TODO" . --include="*.py" | grep -v "#[0-9]"
   ```

2. **Find or Create Troubleshooting Guide**
   ```bash
   find docs/ -name "*troubleshoot*" -o -name "*queryrouter*"
   ```

---

## Phase 3: CI/CD Configuration

### If CI Config EXISTS - Verify
```bash
# Show relevant sections
cat .github/workflows/*.yml | grep -A 10 -B 10 queryrouter
```

### If CI Config MISSING - Document
```markdown
Create CI configuration requirements:
- What tests should run
- When to fail build
- Coverage requirements
- Performance thresholds
```

---

## Phase Z: Evidence Compilation

### GitHub Update Format
```markdown
## GREAT-1C Evidence Report

### Testing Phase Evidence
- [x] Unit tests: tests/unit/services/test_orchestration_locks.py
  ```
  [paste test run output]
  ```
- [x] Integration tests: [file location]
  ```
  [paste output]
  ```
- [x] Performance tests: [benchmark results]
- [ ] Error scenario tests: NOT FOUND
- [ ] End-to-end test: NOT IMPLEMENTED

### Locking Phase Evidence
- [x] Test lock preventing QueryRouter=None:
  ```python
  [show test code]
  ```
- [ ] CI/CD configuration: NOT FOUND - needs creation
- [ ] Pre-commit hooks: NOT FOUND

### Documentation Phase Evidence
- [x] architecture.md updated: [git diff]
- [ ] TODOs without issues: 4 FOUND
  ```
  [list them]
  ```
- [ ] Troubleshooting guide: NOT CREATED

### Verification Phase Evidence
- [ ] Fresh clone test: NOT PERFORMED (need to do)
- [x] Coverage report: 78% (below 80% target)
  ```
  [coverage output]
  ```

### Work Still Required
1. Create missing error scenario tests
2. Add CI/CD configuration
3. Fix 4 TODOs
4. Create troubleshooting guide
5. Achieve 80% coverage
```

---

## Success Criteria

Evidence gathered OR created for:
- [ ] All test files identified or created (PM will validate)
- [ ] Test output provided (PM will validate)
- [ ] Coverage report generated (PM will validate)
- [ ] Documentation updates verified (PM will validate)
- [ ] TODOs counted and listed (PM will validate)
- [ ] CI/CD status determined (PM will validate)

---

## STOP Conditions

- If no tests exist at all (bigger problem)
- If tests exist but don't actually test locks
- If coverage tools not installed
- If CI/CD uses unknown system

---

## Next Steps

Based on findings:
1. **If work complete**: Close boxes with evidence links
2. **If work incomplete**: Create GREAT-1C-COMPLETION issue
3. **Either way**: Document what was actually done vs claimed

---

*Evidence before checkboxes - that's the discipline.*
