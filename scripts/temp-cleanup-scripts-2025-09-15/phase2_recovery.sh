#!/bin/bash
echo "=== PHASE 2: Strategic Recovery of Valuable Stranded Docs ==="

# 1. Commit OMNIBUS logs (the valuable digested versions)
echo "1. Adding OMNIBUS logs to git..."
git add docs/development/session-logs/2025-09-*-OMNIBUS-chronological-log.md
git add docs/development/session-logs/GENESIS-DOCUMENTS-PACKAGE.md
git add docs/development/session-logs/OMNIBUS-*.md
git add docs/development/session-logs/PATTERNS-AND-INSIGHTS.md
echo "✅ Added OMNIBUS logs and synthesis docs"

# 2. Commit weekly ship docs
echo -e "\n2. Adding weekly ship docs..."
git add docs/development/weekly-ship/weekly-ship-*.md
echo "✅ Added weekly ship documentation"

# 3. Check DDD_FIX_TODO to see if it's still relevant
echo -e "\n3. Checking DDD_FIX_TODO content..."
if git show feature/pm-033d-core-coordination:DDD_FIX_TODO.md &>/dev/null; then
    echo "Content of DDD_FIX_TODO.md:"
    git show feature/pm-033d-core-coordination:DDD_FIX_TODO.md | head -20
    echo "..."
    echo "(If this is obsolete, we can ignore it)"
fi

# 4. Recovery from stash - Enhanced Autonomy docs
echo -e "\n4. Checking Enhanced Autonomy docs in stash..."
echo "Found in stash@{0}:"
git stash show stash@{0} --name-only | grep -E "enhanced-autonomy|canonical-queries" | while read file; do
    echo "  - $file"
done

echo -e "\nTo recover Enhanced Autonomy docs, run:"
echo "  git checkout stash@{0} -- docs/development/*enhanced-autonomy*"
echo "  git checkout stash@{0} -- docs/development/canonical-queries-architecture.md"

# 5. Clean up outdated branches (optional)
echo -e "\n5. Outdated branches that could be deleted:"
echo "  - demo-stable-0.1.1-restored (old demo)"
echo "  - origin/preserve-docs-20250622 (June preservation)"
echo "  - origin/gh-pages (if not using GitHub Pages)"
echo ""
echo "To delete local branch: git branch -d <branch-name>"
echo "To delete remote branch: git push origin --delete <branch-name>"

# 6. Commit other untracked valuable docs
echo -e "\n6. Other untracked docs to commit:"
echo "  - docs/development/team-migration-guide.md (placeholder we created)"
echo "  - Recent session logs from Sept 13-15"

echo -e "\n=== SUMMARY OF ACTIONS ==="
echo "Ready to commit:"
echo "  - OMNIBUS logs (Sept 2-12)"
echo "  - Weekly ship docs (004-008)"
echo "  - Recent session logs"
echo "  - Team migration guide"
echo ""
echo "Ready to recover from stash:"
echo "  - Enhanced autonomy docs (might inform 'coming soon' placeholders)"
echo "  - Canonical queries architecture"
echo ""
echo "Can be ignored/deleted:"
echo "  - Old branch versions of README.md, CLAUDE.md"
echo "  - DDD_FIX_TODO (if obsolete)"
echo "  - Old demo branches"
echo ""
echo "To proceed with commits, run: git status"
echo "Then: git commit -m 'Phase 2: Recovery of valuable stranded documentation'"
