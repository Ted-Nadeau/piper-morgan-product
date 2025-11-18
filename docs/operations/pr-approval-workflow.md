# PR Approval Workflow (Alpha Quick Hack)

**Version**: 1.0
**Created**: October 25, 2025
**Status**: Quick hack for alpha (will be replaced with GitHub App)

---

## Overview

GitHub requires PRs to be approved by someone other than the author. We use a bot account (`piper-reviewer`) to auto-approve safe PRs during alpha testing.

**Current Method**: Manual script with bot token (quick hack)
**Future Method**: GitHub App with auto-approve workflow (proper solution)

---

## How to Approve a PR

### Quick Command

```bash
./scripts/approve-pr.sh <PR_NUMBER>
```

**Example**:
```bash
./scripts/approve-pr.sh 270
```

### What It Does

1. Uses `piper-reviewer` bot account
2. Calls GitHub API to approve the PR
3. Adds comment: "✅ Auto-approved by piper-reviewer bot"

---

## Setup Details

### Bot Account

- **Username**: `piper-reviewer`
- **Email**: [configured in GitHub]
- **Role**: Collaborator with Write access
- **Token**: Stored in `scripts/approve-pr.sh`

### Token Permissions

The token has `repo` scope (full repository access):
- Read pull requests
- Write pull request reviews
- Comment on pull requests

### Security Notes

⚠️ **Token is in plaintext** in the script file
- This is intentional for the quick hack
- File is not committed (in .gitignore)
- Only works for this repository
- Will be replaced with GitHub App after alpha

---

## Workflow

### For Your PRs (Codewarrior1988)

1. Create PR as usual:
   ```bash
   gh pr create --title "..." --body "..."
   ```

2. Get PR number from output (e.g., #270)

3. Approve with bot:
   ```bash
   ./scripts/approve-pr.sh 270
   ```

4. Merge as usual:
   ```bash
   gh pr merge 270 --squash
   ```

### Safety Checks (Manual)

Before approving, verify:
- ✅ No secrets/API keys in diff
- ✅ No direct database schema changes
- ✅ Tests passing (CI green)
- ✅ You reviewed the code yourself

**The script doesn't check these automatically** - you're responsible for safety.

---

## Limitations

**What This Doesn't Do**:
- ❌ No automated safety checks
- ❌ No CI integration
- ❌ Doesn't auto-approve on PR creation
- ❌ Doesn't prevent unsafe merges

**This is purely a convenience tool** to bypass GitHub's "can't approve your own PR" restriction.

---

## Future: GitHub App (Post-Alpha)

After alpha testing, we'll replace this with a proper GitHub App that:

✅ Runs automated safety checks
✅ Auto-approves safe PRs on creation
✅ Adds safety labels
✅ Comments with check results
✅ Integrates with CI/CD

See `dev/active/bot-approver-setup.md` for implementation plan.

---

## Troubleshooting

### "404 Not Found"

**Problem**: PR doesn't exist or wrong number

**Solution**: Check PR number:
```bash
gh pr list
```

### "Token expired" or "401 Unauthorized"

**Problem**: Bot token expired or invalid

**Solution**: Regenerate token:
1. Login to GitHub as `piper-reviewer`
2. Go to Settings → Developer settings → Tokens
3. Generate new token with `repo` scope
4. Update `scripts/approve-pr.sh` with new token

### "piper-reviewer is not a collaborator"

**Problem**: Bot account doesn't have access

**Solution**: Re-invite as collaborator:
1. Go to repo Settings → Collaborators
2. Add `piper-reviewer` with Write access

---

## Files

**Script**: `scripts/approve-pr.sh` (executable)
**This Doc**: `docs/operations/pr-approval-workflow.md`
**Setup Plan**: `dev/active/bot-approver-setup.md` (for GitHub App)

---

## Example Session

```bash
# Create PR
$ gh pr create --title "feat: Add new feature" --body "Description"
https://github.com/mediajunkie/piper-morgan-product/pull/270

# Approve with bot
$ ./scripts/approve-pr.sh 270
Approving PR #270 as piper-reviewer...
{
  "id": 12345,
  "state": "APPROVED",
  ...
}
Done! Check https://github.com/mediajunkie/piper-morgan-product/pull/270

# Merge
$ gh pr merge 270 --squash
✓ Squashed and merged pull request #270
```

---

## Security Considerations

### Why This is OK for Alpha

- Small team (1 developer)
- Short timeframe (4-5 days)
- All PRs reviewed by you before bot approval
- Token expires in 90 days
- Private repository

### Why We'll Replace It

- Token in plaintext is not ideal
- No automated safety checks
- Manual approval step is annoying
- GitHub App is the "right" way

---

## Migration Plan

**Alpha (now)**: Use this quick hack
**Post-Alpha (next week)**: Set up GitHub App per `bot-approver-setup.md`

---

_Last Updated: October 25, 2025_
_Status: Active (quick hack)_
