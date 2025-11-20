# System Prompt Integration - Completion Validator

## For claude.ai Project Instructions

**Add to the "Completion protocol" section** (after the existing STOP conditions):

```markdown
## Completion validation requirement

Before declaring ANY issue complete, you MUST run the completion validator:

```bash
python scripts/validate-completion.py <issue-number>
```

**If validator passes** (exit code 0):
- ✅ Proceed to mark issue complete
- Include validator success in completion report
- Provide terminal output as evidence

**If validator fails** (exit code 1):
- ❌ DO NOT mark issue complete
- Review unchecked acceptance criteria
- Complete missing work
- Re-run validator
- Iterate until passing

**Convergence detection**:
- If validator fails 3 times with SAME error → STOP and escalate to PM
- If validator fails 5 times total → STOP and escalate to PM
- This is semantic stop condition (not time-based)

**CRITICAL**: Validation failure is a STOP condition. You cannot rationalize it away as "minor" or "not blocking". The validator is the truth.
```

---

## For Code Agent CLAUDE.md

**Add new section after "Completion discipline"**:

```markdown
## Completion validation

Before marking any issue complete, YOU MUST run:

```bash
python scripts/validate-completion.py <issue-number>
```

**Success** (exit 0):
- All acceptance criteria met
- Proceed with completion

**Failure** (exit 1):
- Criteria incomplete
- Fix and re-run
- Iterate until passing

**Convergence failure**:
- Same error 3x → Escalate to Jesse
- Total 5 attempts → Escalate to Jesse

YOU CANNOT skip validation. It is not optional.
```

---

## For Cursor Agent .cursor/rules

**Add to completion-discipline.md**:

```markdown
## Validation tool

Before marking complete, run:

```bash
python scripts/validate-completion.py <issue-number>
```

Exit 0 = pass (proceed)
Exit 1 = fail (fix and retry)

Validator failure = STOP condition.
Cannot skip or rationalize.
```

---

## Testing the integration

### 1. Update prompts (10 min)

Update all three locations above with validation requirement.

### 2. Test in next session (5 min)

Start new development session and verify agent:
- Runs validator before declaring complete
- Reports validator results
- Stops if validation fails
- Iterates until passing

### 3. Monitor compliance (ongoing)

Track in session logs:
- Did agent run validator?
- Did validator catch incomplete work?
- Did agent iterate until passing?
- Any validation failures requiring PM escalation?

---

## Expected impact

**Before validator**:
- Agent declares "Issue complete"
- PM reviews days later
- Discovers unchecked criteria
- Flywheel drift accumulates

**After validator**:
- Agent runs validator
- Validator catches unchecked criteria immediately
- Agent fixes and retries
- PM reviews only validated-complete work
- Flywheel stays on track

**Multiplier effect**: Every issue gets validated, drift prevented systematically.

---

## Quick reference

**Run validator**:
```bash
python scripts/validate-completion.py 300
```

**Expected output**:
```
🔍 Validating issue #300...
📋 Acceptance Criteria Status:
   ✅ Checked: 12
   ⬜ Unchecked: 0
✅ SUCCESS: All 12 acceptance criteria met!
```

**Use in workflow**:
```bash
# Agent does this before marking complete
if python scripts/validate-completion.py 300; then
    echo "✅ Validation passed - marking complete"
    gh issue edit 300 --add-label "ready-for-review"
else
    echo "❌ Validation failed - completing criteria"
    # Agent fixes unchecked items and retries
fi
```

---

**Ready to integrate**: Copy the relevant snippets above into your system prompts and test!
