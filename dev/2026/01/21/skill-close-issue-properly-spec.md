# Skill Specification: close-issue-properly

**Date**: January 21, 2026
**Phase**: Specification
**Status**: Draft

---

## Skill Overview

| Attribute | Value |
|-----------|-------|
| **Name** | close-issue-properly |
| **Trigger** | Before closing any GitHub issue, "close issue", "mark complete" |
| **Frequency** | Multiple times per session (any time work completes) |
| **Scope** | Cross-role (all agents working on tracked issues) |
| **Complexity** | MEDIUM (~100 lines) |

---

## Purpose

Ensure GitHub issues are closed with proper evidence, updated descriptions, and audit-ready records. Prevents the "Comment-Only Close" anti-pattern where issues get closed without updating checkboxes.

**Key insight**: Closing an issue means updating BOTH the description AND adding a closing comment. The description is the source of truth; comments alone aren't enough.

---

## Inputs

| Input | Required | Source | Example |
|-------|----------|--------|---------|
| Issue number | Yes | Current work context | #543 |
| Tool type | Yes | Environment | GitHub (`gh`) or Beads (`bd`) |
| Completion evidence | Yes | Work results | Test output, commits, files changed |

---

## Outputs

1. **Updated issue description** with checked boxes
2. **Closing comment** with implementation evidence
3. **Closed issue** (only after validation)
4. **Synced database** (if using Beads)

---

## Dependencies

### Required Knowledge
- Issue types: task vs epic (epics need child check)
- Beads discipline: Pattern-046
- Evidence format requirements

### Tools
- `gh issue view/edit/comment/close` (GitHub CLI)
- `bd show/close/sync` (Beads CLI, if available)
- `./scripts/bd-safe close` (safer wrapper)

---

## Procedure

### Step 1: Pre-Close Validation

**For epics**: Check for open children first
```bash
bd list --parent <issue-id>  # All must be closed
```

**For all issues**: Verify completion
- All acceptance criteria from gameplan met?
- Tests passing?
- No discovered work left unfiled?

### Step 2: Update Issue Description

**Required updates**:
1. Check all completed boxes: `[ ]` → `[x]`
2. Update Completion Matrix with evidence
3. Change status to "COMPLETE"

```bash
gh issue edit <number> --body "$(updated_body)"
```

### Step 3: Add Closing Comment

**Template**:
```markdown
## Implementation Complete

### Summary
[1-2 sentence summary]

### Changes Made
- [File]: [What changed]

### Test Results
[Test command and output summary]

### Verification
- Commit: [hash]
- Tests: [X] passing
```

```bash
gh issue comment <number> --body "..."
```

### Step 4: Close Issue

```bash
# Option A: Direct close
gh issue close <number>

# Option B: Beads with validation (preferred)
./scripts/bd-safe close <issue-id>
```

### Step 5: Sync (Beads)

```bash
bd sync
git status  # Should show clean state
```

---

## Quality Criteria

1. **Description checkboxes updated** (not just comment added)
2. **Completion Matrix shows evidence**
3. **Closing comment follows template**
4. **Epic children all closed** (if applicable)
5. **Database synced** (if using Beads)

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It's Bad | Correct Behavior |
|--------------|--------------|------------------|
| Comment-Only Close | Description still shows unchecked boxes | Update description THEN add comment |
| Close with failing tests | Incomplete work marked done | File blocker, keep open |
| Close epic with open children | Work disappears from radar | Complete children first or get PM approval |
| Close without evidence | Can't verify later | Include test output, commits |
| Rationalize gaps as "minor" | Expedience over discipline | Complete all criteria or escalate |

---

## Examples

### Good: Full Closure Sequence

```bash
# 1. Verify tests pass
pytest tests/unit/test_feature.py -v
# All 5 tests pass

# 2. Update description (via UI or API)
gh issue view 543  # See current checkboxes
gh issue edit 543 --body "..."  # Update with [x] marks

# 3. Add closing comment
gh issue comment 543 --body "## Implementation Complete

### Summary
Added validation to user input handler.

### Changes Made
- services/handlers/input.py: Added ValidationError handling
- tests/unit/test_input.py: Added 5 test cases

### Test Results
pytest tests/unit/test_input.py -v
5 passed in 0.23s

### Verification
- Commit: a1b2c3d
- Tests: 5 passing"

# 4. Close
gh issue close 543

# 5. Sync
bd sync
```

### Bad: The Comment-Only Close

```bash
# ❌ WRONG - Description still shows unchecked boxes!
gh issue comment 543 --body "Done, tests pass"
gh issue close 543
```

---

## Stop Conditions

If ANY of these occur, DO NOT close the issue:

1. Tests failing → File P0 blocker, keep parent open
2. Epic has open children → Complete or get PM approval for each
3. Acceptance criteria not met → Complete them first
4. Can't provide evidence → Something isn't done
5. Rationalizing gaps → Escalate to PM

---

## Success Criteria

After skill execution:
- [ ] Issue description shows all boxes checked
- [ ] Completion Matrix updated with evidence links
- [ ] Closing comment follows template
- [ ] Issue status is "closed"
- [ ] If Beads: `bd sync` run successfully
- [ ] If epic: all children were closed first

---

*Specification complete. Ready for SKILL.md draft.*
