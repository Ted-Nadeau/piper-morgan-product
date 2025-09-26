# Phase 1: Documentation Gap Specification & TODO Audit

## Mission
Specify exactly what documentation updates are missing AND audit TODO comments for cleanup scope.

## Context from Verification
- ✅ Lock tests exist
- ❌ Zero git commits to docs since completion claims
- ❌ 100 TODOs without issue numbers (not 4!)
- Need: Precise specifications for missing documentation work

## Part A: Documentation Gap Analysis

### 1. Architecture.md Requirements
```bash
# Check current state
cat docs/internal/architecture/current/architecture.md | grep -i "queryrouter\|orchestration" -A 5 -B 5

# Check git history since GREAT-1C started
git log --oneline --since="2025-09-22" -- docs/internal/architecture/current/architecture.md

# Specify what's needed
cat > /tmp/architecture-update-spec.md << 'EOF'
# Architecture.md Update Specification

## Missing Sections Required

### QueryRouter Integration Section
**Location**: After OrchestrationEngine section
**Content Needed**:
- QueryRouter initialization flow
- Session management with AsyncSessionFactory
- Integration with handle_query_intent method
- Performance characteristics (<500ms)

### Current Orchestration Flow Diagram
**Update Required**: Add QueryRouter to flow diagram
- Intent Detection → OrchestrationEngine → QueryRouter
- Show async initialization pattern
- Document session-aware wrapper

### Code References to Add
```python
# services/orchestration/engine.py lines 78-101
# Show actual initialization pattern
```

## Estimated Effort
- Writing: 45 minutes
- Review: 15 minutes
EOF

cat /tmp/architecture-update-spec.md
```

### 2. ADR-032 Update Requirements
```bash
# Check current ADR-032 state
find docs/internal/architecture/current/adrs -name "*032*" -exec cat {} \;

# Specify implementation status update
cat > /tmp/adr032-update-spec.md << 'EOF'
# ADR-032 Implementation Status Update

## Current ADR-032 State
- Defines QUERY intent classification
- Does not reflect current implementation

## Required Updates

### Implementation Status Section (NEW)
**Add to ADR-032**:
```markdown
## Implementation Status (Updated: 2025-09-23)

### Completed (GREAT-1A/1B)
- QueryRouter enabled in OrchestrationEngine
- handle_query_intent bridge method implemented
- AsyncSessionFactory pattern for session management
- Integration tests passing

### Lock Mechanisms (GREAT-1C)
- Regression prevention tests: tests/regression/test_queryrouter_lock.py
- 9 lock tests prevent accidental disabling
- Performance requirements enforced (<500ms)
```

## Git Commit Required
- Title: "docs: Update ADR-032 with QueryRouter implementation status"
- Files: docs/internal/architecture/current/adrs/ADR-032*
EOF

cat /tmp/adr032-update-spec.md
```

### 3. Troubleshooting Guide Creation
```bash
# Check if troubleshooting guide exists
find docs -name "*troubleshoot*" -o -name "*queryrouter*" | grep -i trouble

# Specify new guide requirements
cat > /tmp/troubleshooting-guide-spec.md << 'EOF'
# QueryRouter Troubleshooting Guide Specification

## File Location
docs/troubleshooting/queryrouter-issues.md (NEW FILE)

## Required Sections

### Common Issues
1. QueryRouter returns None
   - Symptom: Orchestration fails silently
   - Cause: Initialization not awaited
   - Fix: Ensure async get_query_router() is called

2. Session management errors
   - Symptom: Database session errors
   - Cause: Missing AsyncSessionFactory
   - Fix: Check engine initialization pattern

3. Performance degradation
   - Symptom: Queries take >500ms
   - Cause: [TBD - would need investigation]
   - Fix: Check lock test thresholds

### Debugging Steps
- How to verify QueryRouter is enabled
- How to check session management
- How to run lock tests locally

## Estimated Effort
- Creation: 30 minutes
- Validation: 15 minutes
EOF

cat /tmp/troubleshooting-guide-spec.md
```

## Part B: TODO Audit

### 4. Comprehensive TODO Analysis
```bash
# Full TODO scan (verify 100 count)
echo "=== TODO Count by Directory ==="
for dir in services api web tests; do
  count=$(grep -r "TODO" $dir --include="*.py" | grep -v "#[0-9]" | wc -l)
  echo "$dir: $count TODOs without issue numbers"
done

# Sample TODOs by file
echo "=== TODO Sample (first 10) ==="
grep -r "TODO" services api --include="*.py" | grep -v "#[0-9]" | head -10

# Categorize by urgency
echo "=== Critical TODOs (disabled/broken) ==="
grep -r "TODO.*disable\|TODO.*broken\|TODO.*fix" services api --include="*.py" | grep -v "#[0-9]"

# Create cleanup specification
cat > /tmp/todo-cleanup-spec.md << 'EOF'
# TODO Cleanup Specification

## Audit Results
- Total TODOs without issue numbers: [COUNT]
- By directory:
  - services/: [COUNT]
  - api/: [COUNT]
  - web/: [COUNT]
  - tests/: [COUNT]

## Cleanup Strategy

### Immediate (Critical TODOs)
[List TODOs about disabled/broken features with file:line]

### Standard (Should have issues)
[List TODOs that need GitHub issues created]

### Remove (Obsolete)
[List TODOs that are outdated and can be deleted]

## Effort Estimate
- Issue creation: ~5 min per TODO × [COUNT] = [TIME]
- Obsolete removal: ~2 min per TODO × [COUNT] = [TIME]
- Total: [TOTAL TIME]

## Pre-commit Hook Specification
```bash
# Prevent new TODOs without issue numbers
TODO_PATTERN="TODO(?!.*#\d+)"
# Implementation needed in .pre-commit-config.yaml
```
EOF

cat /tmp/todo-cleanup-spec.md
```

## Documentation Specification Summary

Create comprehensive spec:
```markdown
## Documentation Work Required

### 1. architecture.md Updates
- QueryRouter integration section
- Orchestration flow diagram update
- Code reference additions
- Effort: 1 hour

### 2. ADR-032 Implementation Status
- Add implementation status section
- Document lock mechanisms
- Git commit required
- Effort: 30 minutes

### 3. Troubleshooting Guide Creation
- New file: docs/troubleshooting/queryrouter-issues.md
- Common issues and debugging steps
- Effort: 45 minutes

### 4. TODO Cleanup
- [COUNT] TODOs without issue numbers
- Categorized by urgency
- Pre-commit hook specification
- Effort: [CALCULATED]

### Total Documentation Effort
~[SUM] hours to complete all documentation work

### Files That Need Git Commits
1. docs/internal/architecture/current/architecture.md
2. docs/internal/architecture/current/adrs/ADR-032*
3. docs/troubleshooting/queryrouter-issues.md (new)
4. [Files with TODO cleanup]
```

## Success Criteria
- Every missing doc item has precise specification
- Effort estimates for each piece of work
- File paths and sections clearly identified
- PM can decide: accept partial or complete docs

## STOP Conditions
- If doc structure unclear
- If ADR-032 file not found
- If TODO categorization needs PM input

---

**Deliver complete documentation gap specifications for PM decision**
