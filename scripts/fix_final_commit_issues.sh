#!/bin/bash
echo "=== Fixing BOTH pre-commit issues ==="

# 1. The OMNIBUS logs need to be staged with their whitespace fixes
echo "1. Adding the whitespace-fixed OMNIBUS logs..."
git add docs/development/session-logs/*OMNIBUS*.md
git add docs/development/session-logs/GENESIS-DOCUMENTS-PACKAGE.md
git add docs/development/session-logs/PATTERNS-AND-INSIGHTS.md
git add docs/development/canonical-queries-architecture.md

# 2. Deal with the large session log
echo -e "\n2. Checking the large session log..."
ls -lh docs/development/session-logs/2025-09--part-1.md

echo -e "\n3. This file is too large (687KB). Options:"
echo "   a) Split it into smaller parts"
echo "   b) Move to archive"
echo "   c) Add to .gitignore"
echo "   d) Compress it"

# Let's check what it is
echo -e "\n4. First few lines of the large file:"
head -20 docs/development/session-logs/2025-09--part-1.md

echo -e "\n=== RECOMMENDED FIX ==="
echo "Since it's already processed into OMNIBUS logs, we can:"
echo "1. Move it to archive (off-site storage)"
echo "2. Or add session logs over 500KB to .gitignore"
echo ""
echo "Quick fix - move to archive:"
echo "  mkdir -p archive/large-logs/"
echo "  mv docs/development/session-logs/2025-09--part-1.md archive/large-logs/"
echo ""
echo "Then commit everything else:"
echo "  git add -A"
echo "  git commit -m 'Fix whitespace and add recovered docs'"
echo "  git push origin main"
