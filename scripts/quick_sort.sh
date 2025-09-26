#!/bin/bash
echo "=== QUICK SORT FOR STAGED FILES ==="

# 1. Testing guides - likely duplicates, stash for later consolidation
echo "1. Stashing testing guides for later review..."
git reset HEAD COMPREHENSIVE_PM_TESTING_GUIDE.md
git reset HEAD ENHANCED_PM_MANUAL_TESTING_GUIDE.md
git reset HEAD PM_MANUAL_TESTING_PACKAGE.md
git reset HEAD SYNTHESIZED_PM_MANUAL_TESTING_GUIDE_COMPLETE.md
echo "   ✅ Unstaged testing guides (review for duplicates later)"

# 2. Keep config changes - these are your working setup
echo -e "\n2. Keeping .claude and .cursor configs (your working setup)"

# 3. Remove PID files from staging - these shouldn't be in git
echo -e "\n3. Removing PID files from staging..."
git reset HEAD .piper-backend.pid
git reset HEAD .piper-frontend.pid
echo "   ✅ Unstaged PID files"

# 4. Remove temp work artifacts
echo -e "\n4. Removing temporary work files..."
git reset HEAD ab_testing_ux.txt
git reset HEAD docs/archives/working-docs/all_internal_links.txt
echo "   ✅ Unstaged temp files"

# 5. Keep database migration - important!
echo -e "\n5. Keeping database migration (important)"

# 6. Keep analysis files - part of pattern work
echo -e "\n6. Keeping analysis files (pattern work)"

# 7. Keep CLAUDE.md updates
echo -e "\n7. Keeping CLAUDE.md updates"

echo -e "\n=== WHAT'S LEFT STAGED (the good stuff) ==="
git status --short | grep "^[AM]" | head -20

echo -e "\n=== READY TO COMMIT ==="
echo "Commit command:"
echo 'git commit -m "Mixed updates: configs, DB migration, analysis work, doc recovery"'

echo -e "\n=== AFTER COMMIT ==="
echo "1. Push to GitHub"
echo "2. Review testing guides later for consolidation"
echo "3. Add PIDs to .gitignore"
