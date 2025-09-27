# Methodology Improvements from CORE-GREAT-1 Session
**Date**: September 22, 2025
**Source**: Combined observations from PM, Lead Dev, and Chief Architect

## Issues to Fix

### 1. Session Log Naming Bug
**Problem**: Year shows as 2005 instead of 2025 in the command
```bash
# Current (WRONG):
echo "# $(date +%Y-%m-%d-%H%M) Code Log" > dev/2005/$(date +%m)/$(date +%d)/...

# Should be:
echo "# $(date +%Y-%m-%d-%H%M) Code Log" > dev/$(date +%Y)/$(date +%m)/$(date +%d)/...
```
**Fix Location**:
- CLAUDE.md
- PROGRAMMER.md
- Any templates with this command

### 2. Document Creation Location Guidelines
**Problem**: Unclear where docs will be created (sandbox vs artifacts vs filesystem)

**Proposed Standard**:
```markdown
## Document Creation Guidelines

### Use Artifacts When:
- Creating prompts for agents
- Creating final deliverables for PM
- Creating reusable templates
- Want it visible in project artifacts

### Use Filesystem When:
- Creating session logs
- Creating working documents
- Need permanent record
- Multiple files in sequence

### Use Sandbox When:
- Quick temporary calculations
- Testing code snippets
- Throwaway explorations
```

**Fix Location**: Add to METHODOLOGY.md

### 3. Prompt Template Flexibility
**Problem**: Templates too prescriptive, need more adaptability

**Solution**: Add flexibility clause to templates
```markdown
## Template Adaptation
This template provides structure but should be adapted to context:
- Skip irrelevant sections
- Combine phases if appropriate
- Add detail where needed
- Focus on evidence over format
```

### 4. GitHub Progress Standardization
**Problem**: Inconsistent checkbox update format

**Proposed Standard**:
```markdown
## GitHub Progress Format

### In Issue Description (Not Comments):
- [ ] Task started
- [x] Task complete - [evidence link or summary]

### Evidence Format:
- Terminal output: paste key lines
- Test results: link to full output
- Commits: include hash
- Performance: include metrics
```

**Fix Location**: Add to METHODOLOGY.md

### 5. Test Scope Specification
**Lead Dev Innovation**: Specify test types in acceptance criteria

**Standard**:
```markdown
## Test Scope in Acceptance Criteria

Always specify:
- [ ] Unit tests: [what they test]
- [ ] Integration tests: [what they verify]
- [ ] Performance tests: [metrics required]
- [ ] Regression tests: [what they prevent]
```

**Fix Location**: Add to gameplan-template-v8.md

## Quick Fixes Needed

### In CLAUDE.md:
- Fix year in session log command
- Add document location guidelines

### In PROGRAMMER.md:
- Fix year in session log command
- Add document location guidelines

### In METHODOLOGY.md:
- Add document creation guidelines
- Add GitHub progress format
- Add flexibility principle

### In gameplan-template-v8.md:
- Add test scope specification
- Add template adaptation clause

### In agent-prompt-template.md:
- Add flexibility statement
- Reduce prescriptive language

## Process Improvements to Discuss

### From Lead Dev:
1. **Prompt template modules** - Create reusable components
2. **Session state management** - For 8+ hour sessions
3. **Pre-deployment checklists** - Scope clarity

### From PM:
1. **Document trail visibility** - Make clear what persists where
2. **Flexibility over rigidity** - Templates as guides not rules

### From Chief Architect:
1. **Service disruption protocols** - How to handle outages
2. **"Simpler than expected" pattern** - Document this discovery pattern

## Next Actions

1. Fix session log year bug (URGENT)
2. Add document location guidelines
3. Create GitHub progress standard
4. Add flexibility statements to templates
5. Document in METHODOLOGY.md

---

*These improvements will be incorporated after CORE-GREAT-1 completion*
