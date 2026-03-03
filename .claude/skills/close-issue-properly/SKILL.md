---
name: close-issue-properly
description: Close GitHub issues with proper evidence and audit-ready records. Use when completing work on a tracked issue, when PM says "close the issue", or before ending a session with completed work. Updates description checkboxes and adds closing comment.
scope: cross-role
version: 1.1
created: 2026-01-21
updated: 2026-02-09
---

# close-issue-properly

Ensure GitHub issues are closed with proper evidence, updated descriptions, and audit-ready records.

## When to Use

Use this skill when:
- You've completed work on a tracked GitHub issue
- PM asks you to "close the issue" or "mark complete"
- You're wrapping up a session with open issues

## Pre-Flight Checklist (VERIFY BEFORE STARTING)

> **CRITICAL**: The #1 failure mode is skipping the description update and only adding a comment. This leaves unchecked boxes that make the issue look incomplete forever.

Before closing ANY issue, confirm:
- [ ] I have read the full issue description (`gh issue view <id>`)
- [ ] I have identified ALL checkboxes that need updating
- [ ] I will update the description FIRST, comment SECOND

**Key Principle**: The description is the permanent record. Comments are supplementary. An issue with unchecked boxes looks incomplete regardless of comments.

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

### Step 2: Analyze the Description (MANDATORY)

> **DO NOT SKIP THIS STEP.** This is where most closure failures happen.

```bash
# Get the full issue body
gh issue view <id> --json body -q '.body' > /tmp/issue-body.md

# Review the body and identify:
# 1. Every [ ] checkbox
# 2. Any status fields
# 3. Any completion matrices
```

For each checkbox, determine its status:
- ✅ **Done** → Change to `[x]`
- ⏭️ **Deferred** → Keep as `[ ]` but add note: `[ ] Item - *Deferred: [reason]*`
- ❌ **Not applicable** → Keep as `[ ]` but add note: `[ ] Item - *N/A: [reason]*`

**Every unchecked box must have an explanation.** No unexplained unchecked boxes.

### Step 3: Update Issue Description (BEFORE COMMENTING)

> **WARNING**: If you skip to Step 4 without doing this, you've created a Comment-Only Close anti-pattern.

Update the issue description with all checkbox changes:

**For simple issues** (few checkboxes):
```bash
gh issue edit <id> --body "$(cat <<'EOF'
[Full updated body with [x] checkboxes and status changes]
EOF
)"
```

**For complex issues** (many checkboxes):
```bash
# Save updated body to file
gh issue view <id> --json body -q '.body' > /tmp/issue-body.md
# Edit /tmp/issue-body.md with all updates
gh issue edit <id> --body-file /tmp/issue-body.md
```

**What to update**:
1. All completed checkboxes: `[ ]` → `[x]`
2. Add status banner if not present: `**Status**: ✅ COMPLETE`
3. Add deferred items table if any items were skipped
4. Update any completion matrices with evidence links

### Step 4: Add Closing Comment

**Only after Step 3 is complete**, add a comment with implementation evidence:

```bash
gh issue comment <id> --body "$(cat <<'EOF'
## Implementation Complete

### Summary
[1-2 sentence summary of what was done]

### Changes Made
- [File]: [What changed]
- [File]: [What changed]

### Verification
- Evidence doc: [path if applicable]
- Tests: [count] passing (if applicable)
- Files modified: [list]

### Deferred Items (if any)
| Item | Reason |
|------|--------|
| [Item] | [Why deferred] |
EOF
)"
```

### Step 5: Close the Issue

```bash
# Option A: Direct close (after completing Steps 2-4)
gh issue close <id>

# Option B: Beads with validation (preferred if available)
./scripts/bd-safe close <issue-id>
```

**Note**: `bd-safe` validates that epic children are closed and acceptance criteria exist before allowing close.

### Step 6: Sync Database (if using Beads)

```bash
bd sync
git status  # Verify clean state
```

## Pattern Families

This skill applies patterns from the **Completion Theater Family** (045/046/047/049):

- **Pattern-045**: Diagnoses gap between "tests pass" and "users succeed" — verify real completion
- **Pattern-046**: Enforces 100% completion criteria — no rationalizing gaps as "minor"
- **Pattern-049**: Audit at phase boundaries — closing an issue is a phase boundary

If issue closure involved bug investigation, also consider the **Investigation Family** (006/041-043/060).

See [PATTERN-FAMILIES.md](../../../docs/internal/architecture/current/patterns/PATTERN-FAMILIES.md) for full family index.

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It's Bad | Correct Approach |
|--------------|--------------|------------------|
| **Comment-Only Close** | Description still shows unchecked boxes; looks incomplete forever | Update description FIRST, then comment |
| Close with failing tests | Incomplete work marked done | File P0 blocker, keep open |
| Close epic with open children | Work disappears from tracking | Complete children or get PM approval |
| Skip the evidence | Can't verify later | Include test output, commits |
| Rationalize gaps as "minor" | Expedience over discipline | Complete all criteria or escalate |
| Unexplained unchecked boxes | Future readers can't tell if skipped or forgotten | Add note to every unchecked box |

## Stop Conditions

**DO NOT close the issue if**:
1. Tests are failing
2. Epic has open children without PM approval
3. Acceptance criteria are not met
4. You cannot provide verification evidence
5. You're rationalizing incomplete work as "good enough"
6. **You haven't updated the description checkboxes**

Instead: File remaining work as issues, get PM guidance, or complete the work.

## Quality Checklist (Final Verification)

Before closing, verify:
- [ ] **Description updated** with all checkboxes marked appropriately
- [ ] **No unexplained unchecked boxes** - every `[ ]` has a note
- [ ] **Status banner** shows COMPLETE
- [ ] **Closing comment** added with evidence template
- [ ] Tests passing (if applicable)
- [ ] If epic: all children closed
- [ ] If Beads: `bd sync` completed

## Examples

### Example 1: Standard Task Closure (Full Flow)

```bash
# Step 1: Verify work complete
pytest tests/unit/test_feature.py -v  # 5 passed

# Step 2: Analyze description
gh issue view 543 --json body -q '.body' > /tmp/issue-543.md
cat /tmp/issue-543.md  # Review all checkboxes

# Step 3: Update description (the critical step!)
# Edit /tmp/issue-543.md:
#   - Change [ ] to [x] for completed items
#   - Add "**Status**: ✅ COMPLETE" at top
#   - Add notes to any unchecked items
gh issue edit 543 --body-file /tmp/issue-543.md

# Step 4: Add closing comment
gh issue comment 543 --body "## Implementation Complete

### Summary
Added input validation to user handler.

### Verification
- Commit: a1b2c3d
- Tests: 5 passing
- Files: services/handlers/input.py, tests/unit/test_input.py"

# Step 5: Close
gh issue close 543

# Step 6: Sync
bd sync
```

### Example 2: Issue with Deferred Items

```bash
# After updating description with:
#   [x] Implement core feature
#   [x] Add unit tests
#   [ ] Update documentation - *Deferred: will address in #567*
#   [ ] Performance optimization - *N/A: not needed for MVP*

gh issue comment 543 --body "## Implementation Complete

### Summary
Core feature implemented with tests. Documentation deferred to #567.

### Verification
- Commit: a1b2c3d
- Tests: 8 passing

### Deferred Items
| Item | Reason |
|------|--------|
| Update documentation | Separate issue #567 |
| Performance optimization | Not needed for MVP scope |"

gh issue close 543
```

### Example 3: Epic Closure

```bash
# Step 1: Check all children closed
bd list --parent epic-42
# Shows: 3/3 children closed

# Step 2-3: Update epic description with summary of children
gh issue view epic-42 --json body -q '.body' > /tmp/epic-42.md
# Edit to mark all child references as [x] complete
gh issue edit epic-42 --body-file /tmp/epic-42.md

# Step 4: Add closing comment summarizing children
gh issue comment epic-42 --body "## Epic Complete

### Children Completed
- #43: Feature A ✅
- #44: Feature B ✅
- #45: Feature C ✅

### Verification
All 3 child issues closed with evidence."

# Step 5: Close epic
gh issue close epic-42

# Step 6: Sync
bd sync
```

### Example 4: Blocked - Cannot Close

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

---

## Changelog

- **v1.1** (2026-02-09): Added Pre-Flight Checklist, expanded Step 2 with mandatory analysis, added warnings about Comment-Only Close anti-pattern, improved examples with full flow
- **v1.0** (2026-01-21): Initial version
