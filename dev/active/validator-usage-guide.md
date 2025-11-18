# Completion Validator v1.0 - Usage Guide

## What it does

Validates that all acceptance criteria checkboxes in a GitHub issue are checked.

**Purpose**: Prevents agents from declaring issues "complete" when acceptance criteria remain unchecked.

**Philosophy**: Automated enforcement beats manual vigilance.

---

## Installation

1. **Copy to your repo**:
   ```bash
   cp validate-completion.py ~/Development/piper-morgan/scripts/
   chmod +x ~/Development/piper-morgan/scripts/validate-completion.py
   ```

2. **Verify GitHub CLI is installed**:
   ```bash
   gh --version
   # If not installed: brew install gh (macOS) or see https://cli.github.com
   ```

3. **Test it**:
   ```bash
   python scripts/validate-completion.py 300
   ```

---

## Usage

### Basic usage

```bash
python scripts/validate-completion.py <issue-number>
```

### Examples

```bash
# Validate Issue #300
python scripts/validate-completion.py 300

# Use in scripts (check exit code)
if python scripts/validate-completion.py 300; then
    echo "✅ Ready for PM review"
else
    echo "❌ Incomplete - fix criteria first"
fi
```

### Exit codes

- `0` = All criteria met (success)
- `1` = Criteria incomplete (failure)
- `2` = Error (GitHub CLI not found, issue not found, etc.)

---

## Output examples

### Success (all criteria met)

```
🔍 Validating issue #300...

📋 Acceptance Criteria Status:
   ✅ Checked: 12
   ⬜ Unchecked: 0
   📊 Total: 12

✅ SUCCESS: All 12 acceptance criteria met!
```

### Failure (criteria incomplete)

```
🔍 Validating issue #300...

📋 Acceptance Criteria Status:
   ✅ Checked: 10
   ⬜ Unchecked: 2
   📊 Total: 12

❌ INCOMPLETE: 2 criteria remaining:

   1. Documentation updated for new feature
   2. Cross-validation report added to issue

```

### No criteria section

```
🔍 Validating issue #300...

⚠️  No 'Acceptance Criteria' section found in issue
   (This might be okay if issue doesn't use acceptance criteria)
```

---

## Integration into workflows

### 1. Agent prompts

Add to all agent prompts (Code, Cursor, etc.):

```markdown
## Completion protocol

Before marking any issue as "complete":

1. Run the completion validator:
   ```bash
   python scripts/validate-completion.py <issue-number>
   ```

2. If validator fails:
   - Review unchecked criteria
   - Complete missing work
   - Re-run validator
   - Iterate until passing

3. Only mark "complete" after validator passes

**STOP condition**: If validator fails 3 times with same error, escalate to PM.
```

### 2. System prompts (claude.ai project)

Add to project instructions:

```markdown
## Validation requirement

YOU MUST run the completion validator before declaring any issue complete:

```bash
python scripts/validate-completion.py <issue-number>
```

If validation fails, you MUST complete the missing criteria before proceeding.

Validation failure is a STOP condition - do not rationalize or skip.
```

### 3. GitHub workflow (future)

Create `.github/workflows/validate-completion.yml`:

```yaml
name: Validate Issue Completion

on:
  issues:
    types: [labeled]

jobs:
  validate:
    if: github.event.label.name == 'ready-for-review'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Validate completion
        run: python scripts/validate-completion.py ${{ github.event.issue.number }}
      - name: Comment result
        uses: actions/github-script@v6
        with:
          script: |
            const result = ${{ job.status }};
            const message = result === 'success' 
              ? '✅ Validation passed - ready for PM review'
              : '❌ Validation failed - see workflow logs';
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.name,
              body: message
            });
```

---

## How it works

1. **Fetches issue** from GitHub using `gh issue view`
2. **Finds "Acceptance Criteria" section** (case-insensitive)
3. **Parses checkboxes**:
   - Checked: `- [x] Criterion text`
   - Unchecked: `- [ ] Criterion text`
4. **Reports status**:
   - Lists unchecked items
   - Shows counts
   - Returns appropriate exit code

---

## Escalation path (future enhancements)

### v1.1 - Evidence link validation
Check that checked criteria have evidence links (commits, test outputs, screenshots)

### v1.2 - Completion matrix validation
Verify completion matrix is 100% complete with all ✅ statuses

### v1.3 - Cross-validation check
Confirm cross-validation report exists for multi-agent issues

### v1.4 - Convergence detection
Track validation attempts, detect if agent is stuck (same error 3x)

### v2.0 - Full methodology validator
Comprehensive check of all completion requirements

---

## Testing the validator

### Test with Issue #300

```bash
# Should work if #300 has acceptance criteria
python scripts/validate-completion.py 300
```

### Test with completed issue

```bash
# Find a completed issue with all boxes checked
python scripts/validate-completion.py <completed-issue-number>
# Should show: ✅ SUCCESS
```

### Test with incomplete issue

```bash
# Find an in-progress issue with unchecked boxes
python scripts/validate-completion.py <incomplete-issue-number>
# Should show: ❌ INCOMPLETE with list of remaining items
```

---

## Troubleshooting

**"gh: command not found"**
- Install GitHub CLI: `brew install gh` (macOS) or https://cli.github.com
- Authenticate: `gh auth login`

**"Error fetching issue"**
- Verify issue number exists
- Check GitHub authentication: `gh auth status`
- Ensure you're in the repo directory

**"No acceptance criteria section found"**
- This is okay if issue doesn't use acceptance criteria
- Validator passes by default (some issues don't have criteria)

**Exit code 2 (error)**
- Check GitHub CLI is installed and authenticated
- Verify you're in the correct repository
- Check issue number is valid

---

## Philosophy

**Simon Willison's insight**: "The art of using agents well is to carefully design the tools and loop for them to use."

**This validator**:
- Provides agents a **tool to verify their own work**
- Creates a **clear success criteria** (all boxes checked)
- Enables **automatic iteration** (fail → fix → retry)
- **Eliminates judgment calls** (binary pass/fail)

**Result**: Flywheel stays in motion without constant PM vigilance.

---

## Next steps

1. **Test it**: Run on Issues #290, #300, #262
2. **Update prompts**: Add validation requirement to agent instructions
3. **Monitor usage**: Track how often it catches incomplete work
4. **Iterate**: Add evidence validation (v1.1) once basic validation proves valuable

---

**Version**: 1.0  
**Created**: November 15, 2025  
**Author**: Chief of Staff + PM (xian)  
**Purpose**: Down payment on methodology enforcement automation
