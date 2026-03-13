# Cursor Task: Investigate and Clean Up pytest Command Instructions

**Date**: October 26, 2025, 5:48 PM PT
**Priority**: Low (cleanup/maintenance)
**Estimated Time**: 15-20 minutes

---

## Context

During Haiku 4.5 testing today, we noticed different pytest command patterns between agents:

**Haiku's Behavior** (Issues #268, #269):
```bash
python -m pytest tests/ -v
# Runs freely, no permission check
```

**Sonnet's Usual Behavior**:
```bash
PYTHONPATH=. pytest tests/ -v
# Triggers permission check
```

**Hypothesis**: There may be outdated instructions in our documentation or prompt templates that reference the old `PYTHONPATH=...` pattern, which is either:
1. No longer needed (pytest works fine without it)
2. Inconsistently documented (some agents see it, some don't)

---

## Your Mission

Investigate where pytest command patterns are documented and clean up any outdated or inconsistent instructions.

---

## Phase 1: Discovery (Search for References)

### Search Documentation
```bash
# Find all pytest-related documentation
grep -r "pytest" docs/ --include="*.md"
grep -r "PYTHONPATH" docs/ --include="*.md"

# Check prompt templates
grep -r "pytest" docs/prompts/ --include="*.md" 2>/dev/null
grep -r "PYTHONPATH" docs/prompts/ --include="*.md" 2>/dev/null

# Check briefings
grep -r "pytest" docs/briefing/ --include="*.md"
grep -r "PYTHONPATH" docs/briefing/ --include="*.md"

# Check guidelines
grep -r "pytest" docs/guidelines/ --include="*.md" 2>/dev/null
grep -r "pytest" architectural-guidelines.md 2>/dev/null
grep -r "pytest" dev-guidelines.md 2>/dev/null
```

### Search Agent Templates
```bash
# Check agent prompt templates
find . -name "*agent*prompt*" -o -name "*template*" | grep -v node_modules
grep -r "pytest" . --include="*agent*" --include="*template*"
grep -r "PYTHONPATH" . --include="*agent*" --include="*template*"

# Check session log templates
grep -r "pytest" session-log-template* 2>/dev/null
```

### Search Python Test Infrastructure
```bash
# Check test configuration
cat pytest.ini 2>/dev/null
cat pyproject.toml | grep -A 10 "\[tool.pytest" 2>/dev/null
cat setup.py 2>/dev/null | grep -A 5 "pytest"

# Check any test runner scripts
find . -name "*test*" -name "*.sh" -o -name "run_tests*"
cat scripts/run_tests.sh 2>/dev/null
```

### Search Recent Changes
```bash
# Check git history for pytest-related changes
git log --all --grep="pytest" --oneline -20
git log --all --grep="PYTHONPATH" --oneline -20

# Check recent documentation changes
git log -10 --oneline -- docs/
```

---

## Phase 2: Analysis

### Document Your Findings

Create a report with:

**1. Where pytest is Referenced**:
```
Location: [file path]
Current instruction: [exact text]
Context: [where/how used]
Status: [Needed/Outdated/Inconsistent]
```

**2. PYTHONPATH Usage Patterns**:
- Is it actually needed? (test if pytest works without it)
- Is it consistently documented?
- Does it serve a specific purpose?

**3. Permission Check Behavior**:
- Why does Sonnet trigger permission checks?
- Why doesn't Haiku trigger them?
- Is this related to PYTHONPATH or something else?

**4. Current Best Practice**:
```bash
# What SHOULD agents use?
# Option A: python -m pytest tests/ -v
# Option B: PYTHONPATH=. pytest tests/ -v
# Option C: pytest tests/ -v
# Option D: ./scripts/run_tests.sh

# Rationale: [why this is best]
```

---

## Phase 3: Recommendations

Based on your findings, recommend:

### Cleanup Actions

**If PYTHONPATH is NOT needed**:
- [ ] Remove PYTHONPATH references from documentation
- [ ] Update agent prompt templates to use `python -m pytest`
- [ ] Document why this changed (if it was needed before)

**If PYTHONPATH IS needed**:
- [ ] Document WHY it's needed (what breaks without it?)
- [ ] Ensure all templates use it consistently
- [ ] Add comment explaining its purpose

**If inconsistently documented**:
- [ ] Standardize on one approach
- [ ] Update all references
- [ ] Add to testing guidelines

### Documentation Updates

List specific files that need updating:
```
File: [path]
Current: [problematic instruction]
Proposed: [corrected instruction]
Reason: [why change is needed]
```

---

## Phase 4: Implementation (If Approved)

After PM reviews your recommendations:

### Make Changes
- Update identified documentation files
- Update agent prompt templates
- Update testing guidelines

### Verify
```bash
# Test that pytest works with recommended command
[your recommended command]

# Verify in clean environment if possible
```

### Document
- Add note to session log
- Update any testing documentation
- Create PR or commit with changes

---

## Testing the Difference

### Experiment: Does PYTHONPATH Matter?

```bash
# Test 1: Without PYTHONPATH
python -m pytest tests/services/test_key_storage_validation.py -v

# Test 2: With PYTHONPATH
PYTHONPATH=. pytest tests/services/test_key_storage_validation.py -v

# Test 3: Just pytest
pytest tests/services/test_key_storage_validation.py -v

# Compare results - are they identical?
```

### Check Import Behavior
```python
# Does PYTHONPATH affect imports?
# Try running: python -c "import services.security.key_validator"

# With PYTHONPATH
PYTHONPATH=. python -c "import services.security.key_validator"

# Without PYTHONPATH
python -c "import services.security.key_validator"
```

---

## Expected Findings (Hypotheses)

**Hypothesis 1**: PYTHONPATH was needed in old setup, no longer needed
- Evidence to look for: Old commit adding PYTHONPATH
- Evidence to look for: Python path configuration changes

**Hypothesis 2**: PYTHONPATH only needed for certain test types
- Evidence to look for: Integration tests vs unit tests
- Evidence to look for: Different test directories

**Hypothesis 3**: It's a documentation artifact that can be removed
- Evidence to look for: Works fine without it
- Evidence to look for: Inconsistent usage already

**Hypothesis 4**: Permission check is unrelated to PYTHONPATH
- Evidence to look for: Permission check logic in agent code
- Evidence to look for: Different between Haiku/Sonnet behavior

---

## Deliverable

Create a markdown report: `pytest-command-investigation-report.md`

**Include**:
1. **Discovery**: All locations where pytest/PYTHONPATH documented
2. **Analysis**: Whether PYTHONPATH is needed and why
3. **Testing**: Results of running tests with/without PYTHONPATH
4. **Recommendations**: Specific cleanup actions
5. **Implementation Plan**: Files to update (if approved)

---

## Success Criteria

- [ ] Found all pytest command references in documentation
- [ ] Determined if PYTHONPATH is actually needed
- [ ] Identified inconsistencies in documentation
- [ ] Tested both command patterns
- [ ] Provided clear recommendations
- [ ] Listed specific files to update

---

## Notes

**Low Priority**: This is cleanup/consistency work, not urgent

**Context**: Noticed during Sprint A8 Haiku testing (Issues #268, #269)

**Goal**: Consistent, correct pytest instructions for all agents

---

## Questions to Answer

1. **Is PYTHONPATH needed?** YES/NO/SOMETIMES - explain
2. **Why the difference between agents?** [your theory]
3. **What should be our standard?** [recommended command]
4. **Which files need updating?** [list]
5. **Any breaking changes?** [impact assessment]

---

**Ready to investigate!** Start with Phase 1 (Discovery), then report findings.

---

*Task Created: October 26, 2025, 5:48 PM PT*
*For: Cursor*
*Priority: Low*
*Estimated Time: 15-20 minutes*
