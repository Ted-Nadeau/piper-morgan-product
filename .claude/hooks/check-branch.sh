#!/usr/bin/env bash
# check-branch.sh — PreToolUse hook for git commit
#
# Warns when committing on a branch other than main.
# Runs before every git commit to prevent accidental commits on stale branches.
#
# Exit 0 = allow (with warning if not on main)
# Exit 2 = block

CURRENT_BRANCH=$(git branch --show-current 2>/dev/null)

if [ -z "$CURRENT_BRANCH" ]; then
    # Not in a git repo or detached HEAD — let it through
    exit 0
fi

if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "WARNING: You are on branch '$CURRENT_BRANCH', not 'main'."
    echo "Switch to main before committing: git checkout main"
    exit 2
fi

exit 0
