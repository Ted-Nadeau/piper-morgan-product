# Prevention System: Ephemeral File Loss in /tmp

**Date**: November 1, 2025
**Reason**: Multiple agent session reports (verification, analysis, findings) were accidentally created in `/tmp/` and risked permanent loss
**Solution**: Automated pre-commit hook to block commits when work files detected in `/tmp/`

---

## Problem Statement

Cursor Agent was writing work products to `/tmp/` instead of `dev/active/`:
- `/tmp/issue-281-verification.md` (5.8K)
- `/tmp/issue-281-final-report.md` (2.6K)
- Earlier orphaned files from October sessions (not yet recovered/audited)

**Risk**: `/tmp/` is ephemeral storage automatically cleaned by OS. Files would be permanently lost.

**Root Cause**: Habit from local development using `/tmp/` as "working directory" without understanding sandbox/filesystem implications.

---

## Solution: Pre-Commit Hook

### What It Does
- **Runs at every commit** (pre-commit stage)
- **Scans `/tmp/` for work files** matching patterns:
  - `*report*.md`, `*verification*.md`, `*analysis*.md`
  - `*evidence*.md`, `*findings*.md`, `*summary*.md`
  - `*issue*.md`, `*sprint*.md`
- **Blocks commit** if files found
- **Displays clear remediation steps** to user

### Implementation

**Script**: `scripts/check-tmp-work-files.sh`
- Exit code 1 (blocks commit) if work files detected
- Exit code 0 (allows commit) if clean
- Provides actionable error message with file names and sizes

**Config**: `.pre-commit-config.yaml` updated with new hook

---

## How to Use

### Normal Workflow (Recommended)
Always output work to `dev/active/`:

```bash
# Correct approach
cat > dev/active/issue-281-verification.md << 'EOF'
...content...
EOF
```

### If Files End Up in /tmp

1. **Pre-commit hook will block your commit** with a clear message
2. **Follow the steps** displayed (copy files to dev/active/, add, commit)
3. **Commit succeeds** once /tmp is clean

---

## Testing the Hook

```bash
# Hook automatically runs before each commit
# Returns success (0) if no work files in /tmp
# Returns error (1) if files detected - blocks commit

./scripts/check-tmp-work-files.sh  # Manual test
```

---

## Auditing Orphaned Files

If you find orphaned work files:

```bash
ls -lh /tmp/*report* /tmp/*verification* /tmp/*analysis* 2>/dev/null

# Recover each one
cp /tmp/filename.md dev/active/
git add dev/active/filename.md
git commit -m "docs: Recover orphaned work file"
```

---

## Configuration

The hook is configured in `.pre-commit-config.yaml` and runs automatically.

To bypass (not recommended):
```bash
git commit --no-verify
```

---

## Why This Matters

- Work products are precious evidence of development
- Easy to lose in ephemeral storage
- Hook prevents mistakes before damage occurs
- Ensures all work is preserved in Git

---

## Related

- Commit: 4ed018b8
- Memory ID: 10632391

**Created**: November 1, 2025 by Cursor Agent
