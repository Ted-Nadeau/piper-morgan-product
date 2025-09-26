# Gameplan Template v6.0 - With Infrastructure Verification

## Context
- **Issue**: [GitHub issue number and title]
- **Complexity**: [Low/Medium/High]
- **Lead Developer**: [Who will execute]
- **Agents**: [Which agents will be deployed]

## Phase -1: MANDATORY Infrastructure Verification

### Part A: What I Think Exists
Document your understanding BEFORE verification:
1. **What files/services exist?**
2. **What's the current implementation?**
3. **What needs to be built vs modified?**

### Part B: PM Verification Required
```bash
# Commands for PM to run:
ls -la [relevant directories]
grep -r "[feature]" [location] --include="*.py"
cat [specific file] | grep -A 20 "[function]"
```

### Part C: Proceed/Revise Decision
After PM verification:
- [ ] PROCEED - Understanding correct
- [ ] REVISE - Major assumptions wrong
- [ ] CLARIFY - Need more context

**If REVISE or CLARIFY, STOP and create new gameplan**

## Phase 0: Investigation & GitHub Setup (MANDATORY)

### All Agents Must
1. Verify GitHub issue exists
2. Check for existing implementations
3. Search for related patterns
4. Update issue with findings

```bash
# Standard investigation commands
gh issue view [NUMBER]
grep -r "[feature]" services/ --include="*.py"
find . -name "*[related]*" -type f
```

## Phase 1: [Main Implementation Phase]

### Multi-Agent Division (DEFAULT)
**Claude Code** - [Responsibilities]
**Cursor Agent** - [Responsibilities]

### Coordination Points
- Check-in at logical junctures
- Cross-validate after major changes
- GitHub issue updates every phase

## Phase 2: [Validation Phase]

### Cross-Validation Protocol
- Code validates Cursor's UI changes
- Cursor validates Code's backend changes
- Both verify no regressions

## STOP Conditions
- Infrastructure doesn't match plan → STOP
- Complexity exceeds estimate → STOP
- Agents disagree on approach → STOP

## Success Criteria
- [ ] All tests passing
- [ ] Feature working end-to-end
- [ ] Cross-validation complete
- [ ] GitHub issue updated with evidence

## Time Estimate
- Phase 0: X minutes
- Phase 1: X minutes
- Phase 2: X minutes
- Total: X minutes

---
*Template v6.0 - Infrastructure verification mandatory*
