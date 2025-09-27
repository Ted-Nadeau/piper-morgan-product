# Cursor Agent Prompt: Excellence Flywheel & TODO Verification

## Your Identity
You are Cursor Agent, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

## Mission: Complete CORE-GREAT-2A Verification
**Objective**: Complete the final verification items for CORE-GREAT-2A investigation phase.

## Context from Lead Developer
- CORE-GREAT-2A gameplan requires checking Excellence Flywheel integration in agent configs
- Need to locate and assess specific TODO comments: TBD-API-01, TBD-LLM-01, TBD-SECURITY-02
- This completes the investigation phase before reporting to Chief Architect

## Verification Tasks

### 1. Excellence Flywheel Integration Check
**Gameplan requirement**: "Excellence Flywheel in all agent configs"

```bash
# Find agent configuration files
find . -name "*agent*config*" -type f
find . -name "*prompt*" -type f | grep -E "(agent|template)"
find . -path "*/.claude/*" -name "*.md" -o -name "*.txt"
find . -path "*/.cursor/*" -name "*.md" -o -name "*.txt"

# Search for Excellence Flywheel references
grep -r "Excellence Flywheel" . --include="*.md" --include="*.txt" --include="*.json"
grep -r "excellence.*flywheel" . --include="*.md" --include="*.txt" --include="*.json" -i
```

**Evidence Required**:
- Agent configuration file locations
- Current Excellence Flywheel integration status
- Missing integrations identified

### 2. TODO Comments Investigation
**Find specific TODO items**: TBD-API-01, TBD-LLM-01, TBD-SECURITY-02

```bash
# Search for the specific TBD items
grep -r "TBD-API-01" . --include="*.py" --include="*.md" --include="*.txt"
grep -r "TBD-LLM-01" . --include="*.py" --include="*.md" --include="*.txt"  
grep -r "TBD-SECURITY-02" . --include="*.py" --include="*.md" --include="*.txt"

# Search for general TBD pattern
grep -r "TBD-" . --include="*.py" --include="*.md" --include="*.txt"

# Search for TODO comments without issue numbers
grep -r "TODO" . --include="*.py" | grep -v "#[0-9]"
```

**Evidence Required**:
- Exact file locations and line numbers
- Current status of each TBD item
- Context around each TODO comment

### 3. Additional Documentation Investigation
Given PM's note about "chaos in docs tree" and "Code flubbed a merge":

```bash
# Check docs/NAVIGATION.md status
ls -la docs/NAVIGATION.md
head -50 docs/NAVIGATION.md

# Look for recently broken documentation structure
find docs/ -name "*.md" -type f | head -20
ls -la docs/
```

## Reporting Format

```markdown
# Excellence Flywheel & TODO Verification Results

## Excellence Flywheel Integration Status

### Agent Configuration Files Found
- [List with paths]

### Current Integration Status
- [✅/❌ for each agent config]
- [Missing integrations identified]

## TODO Comment Investigation

### TBD-API-01
- **Location**: [file:line]
- **Context**: [surrounding code/description]
- **Status**: [Active/Resolved/Deprecated]

### TBD-LLM-01  
- **Location**: [file:line]
- **Context**: [surrounding code/description]
- **Status**: [Active/Resolved/Deprecated]

### TBD-SECURITY-02
- **Location**: [file:line] 
- **Context**: [surrounding code/description]
- **Status**: [Active/Resolved/Deprecated]

### Additional TODO Comments
[Any other significant TODO comments without issue numbers]

## Documentation Structure Notes
[Any observations about docs/NAVIGATION.md or recent structural issues]
```

## Success Criteria
- ✅ All agent configuration files identified
- ✅ Excellence Flywheel integration status assessed
- ✅ All three TBD items located and assessed
- ✅ Evidence provided for all claims
- ✅ Clear recommendations for gaps

## Critical Notes
- **Focus on factual findings** - don't implement fixes
- **Document exact file paths and line numbers**
- **Note any patterns** in TODO comment distribution
- **Flag any critical security items** (TBD-SECURITY-02 is marked HIGH priority)

---

**Deploy immediately and report findings to Lead Developer for Chief Architect briefing.**
