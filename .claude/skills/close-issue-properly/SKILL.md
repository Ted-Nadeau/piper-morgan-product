---
scope: cross-role
version: 1.0
created: 2026-01-21
---

# close-issue-properly

Ensure GitHub issues are closed with proper evidence, updated descriptions, and audit-ready records.

## When to Use

Use this skill when:
- You've completed work on a tracked GitHub issue
- PM asks you to "close the issue" or "mark complete"
- You're wrapping up a session with open issues

**Key Principle**: Closing an issue means updating BOTH the description AND adding a closing comment. The description is the source of truth.

## Procedure

### Step 1: Pre-Close Validation

**For epics** (check children first):
```bash
bd list --parent <issue-id>
# ALL children must be closed before closing epic
```

**For all issues** (verify completion):
- All acceptance criteria from gameplan met?
- Tests passing?
- No discovered work left unfiled?

**Stop if**: Tests failing, criteria unmet, or open children exist.

### Step 2: Update Issue Description

Update the issue description (via GitHub UI or `gh issue edit`):

1. **Check all completed boxes**: `[ ]` → `[x]`
2. **Update Completion Matrix** with evidence links
3. **Change status** to "COMPLETE"

Example command:
```bash
gh issue view 543  # See current state
gh issue edit 543 --body "$(cat <<'EOF'
[updated body with [x] checkboxes]
EOF
)"
```

**Practical tip**: For issues with complex descriptions, updating via GitHub web UI is often easier than CLI. Edit checkboxes in browser, then use CLI for comment and close.

### Step 3: Add Closing Comment

Add a comment with implementation evidence:

```bash
gh issue comment 543 --body "$(cat <<'EOF'
## Implementation Complete

### Summary
[1-2 sentence summary of what was done]

### Changes Made
- [File]: [What changed]
- [File]: [What changed]

### Test Results
[Test command and output summary]

### Verification
- Commit: [hash]
- Tests: [X] passing
EOF
)"
```

### Step 4: Close the Issue

```bash
# Option A: Direct close (after manual validation)
gh issue close 543

# Option B: Beads with validation (preferred if available)
./scripts/bd-safe close <issue-id>
```

**Note**: `bd-safe` validates that epic children are closed and acceptance criteria exist before allowing close.

### Step 5: Sync Database (if using Beads)

```bash
bd sync
git status  # Verify clean state
```

## Anti-Patterns to Avoid

| Don't Do This | Why | Do This Instead |
|---------------|-----|-----------------|
| Comment-Only Close | Description still shows unchecked boxes | Update description THEN comment |
| Close with failing tests | Incomplete work marked done | File P0 blocker, keep open |
| Close epic with open children | Work disappears from tracking | Complete children or get PM approval |
| Skip the evidence | Can't verify later | Include test output, commits |
| Rationalize gaps as "minor" | Expedience over discipline | Complete all criteria or escalate |

## Evidence Template

**Minimum required in closing comment**:
```markdown
## Implementation Complete

### Summary
[What was accomplished]

### Verification
- Commit: [hash or PR link]
- Tests: [count] passing
- Files: [list of modified files]
```

## Stop Conditions

**DO NOT close the issue if**:
1. Tests are failing
2. Epic has open children without PM approval
3. Acceptance criteria are not met
4. You cannot provide verification evidence
5. You're rationalizing incomplete work as "good enough"

Instead: File remaining work as issues, get PM guidance, or complete the work.

## Quality Checklist

Before closing any issue:
- [ ] All description checkboxes checked
- [ ] Completion Matrix updated with evidence
- [ ] Closing comment added with template
- [ ] Tests passing (if applicable)
- [ ] If epic: all children closed
- [ ] If Beads: `bd sync` completed

## Examples

### Example 1: Standard Task Closure

```bash
# 1. Verify work complete
pytest tests/unit/test_feature.py -v  # 5 passed

# 2. Update description checkboxes (via GitHub UI or CLI)

# 3. Add closing comment
gh issue comment 543 --body "## Implementation Complete

### Summary
Added input validation to user handler.

### Verification
- Commit: a1b2c3d
- Tests: 5 passing
- Files: services/handlers/input.py, tests/unit/test_input.py"

# 4. Close
gh issue close 543

# 5. Sync
bd sync
```

### Example 2: Epic Closure

```bash
# 1. Check all children closed
bd list --parent epic-42
# Shows: 3/3 children closed

# 2. Update epic description with summary

# 3. Add closing comment summarizing children

# 4. Close epic
./scripts/bd-safe close epic-42

# 5. Sync
bd sync
```

### Example 3: Blocked - Cannot Close

```bash
# Tests failing - DO NOT CLOSE
pytest tests/  # 2 failed

# Instead:
# 1. File P0 blocker issue for failing tests
bd create "P0: Fix failing tests in feature X" --type blocker
bd dep add <new-blocker> <original-issue> --type blocks

# 2. Keep original issue open
# 3. Report to PM
```
