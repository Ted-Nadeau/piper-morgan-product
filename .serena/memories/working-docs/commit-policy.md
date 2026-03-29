# Working Documents Must Be Committed

## Rule
All working documents in `dev/YYYY/MM/DD/` — session logs, test harnesses, reports, results CSVs — **must be committed and pushed**, not left as untracked local files.

## Why
- Session logs and reports are used to create **synthesized logs** and **team briefings**
- Other agents and team members need access to working docs for context
- Worktrees are ephemeral — untracked files in worktrees will be lost when the worktree is cleaned up
- The PM uses session logs to brief all team members on project updates

## Critical: Merge to Main

Working docs on worktree branches are NOT accessible to the team. Session wrap-up MUST include:
1. Commit working docs to the worktree branch
2. **Merge the worktree branch to main** (or cherry-pick the docs commits)
3. Verify files exist at `/Users/xian/Development/piper-morgan/dev/YYYY/MM/DD/`

The PM and other agents expect to find session logs on `main`, not on feature branches.

## History
Previously `dev/` was in `.gitignore` (removed in commit `75045a5e`). Normal `git add` now works — no `git add -f` needed.

## When to Commit
- At session wrap-up (always)
- After generating test reports or artifacts
- Before ending any session where working docs were created or updated

## What to Commit
- Session logs (`YYYY-MM-DD-HHMM-{role}-{tool}-{model}-log.md`)
- Test harness scripts
- Test results (CSV, reports)
- Any other working documents in `dev/`

Do NOT commit:
- Temporary scratch files clearly marked as disposable
- Large binary artifacts (screenshots, etc.)
