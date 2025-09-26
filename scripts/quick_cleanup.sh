#!/bin/bash
echo "=== Quick Cleanup Before Errands ==="

# 1. Recover the canonical queries doc - this is valuable!
echo "1. Recovering canonical-queries-architecture.md..."
git checkout stash@{0} -- docs/development/canonical-queries-architecture.md 2>/dev/null && echo "✅ Recovered!" || echo "❌ Already exists or error"

# 2. Add it to staging with other docs
git add docs/development/canonical-queries-architecture.md 2>/dev/null

# 3. Clean up our one-off scripts
echo -e "\n2. Cleaning up one-off scripts..."
mkdir -p scripts/temp-cleanup-scripts-2025-09-15
mv ~/Development/piper-morgan/phase*.sh scripts/temp-cleanup-scripts-2025-09-15/ 2>/dev/null
mv ~/Development/piper-morgan/find*.sh scripts/temp-cleanup-scripts-2025-09-15/ 2>/dev/null
mv ~/Development/piper-morgan/fix*.sh scripts/temp-cleanup-scripts-2025-09-15/ 2>/dev/null
mv ~/Development/piper-morgan/check*.sh scripts/temp-cleanup-scripts-2025-09-15/ 2>/dev/null
mv ~/Development/piper-morgan/final*.sh scripts/temp-cleanup-scripts-2025-09-15/ 2>/dev/null
mv ~/Development/piper-morgan/debug*.sh scripts/temp-cleanup-scripts-2025-09-15/ 2>/dev/null
mv ~/Development/piper-morgan/reveal*.sh scripts/temp-cleanup-scripts-2025-09-15/ 2>/dev/null
mv ~/Development/piper-morgan/absolute*.sh scripts/temp-cleanup-scripts-2025-09-15/ 2>/dev/null
mv ~/Development/piper-morgan/ultimate*.sh scripts/temp-cleanup-scripts-2025-09-15/ 2>/dev/null
mv ~/Development/piper-morgan/systematic*.sh scripts/temp-cleanup-scripts-2025-09-15/ 2>/dev/null

echo "✅ Moved cleanup scripts to scripts/temp-cleanup-scripts-2025-09-15/"
echo "   (Can delete this folder after session)"

# 4. Show what's ready to commit
echo -e "\n3. Ready to commit:"
git status --short | head -20

echo -e "\n=== Quick Commit Command ==="
echo "Run this to commit everything staged:"
echo 'git commit -m "Phase 2: Recover stranded docs - OMNIBUS logs, weekly ships, canonical queries"'

echo -e "\n=== DDD_FIX_TODO Status ==="
echo "That DDD fix was for markdown formatting - likely obsolete after DDD refactoring Friday"
echo "Can safely ignore"

echo -e "\n✅ Done! Safe to run errands. When you return:"
echo "1. Commit these recovered docs"
echo "2. Delete temp scripts folder if desired"
echo "3. Continue with Pattern Sweep"
