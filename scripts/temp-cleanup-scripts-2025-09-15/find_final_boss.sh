#!/bin/bash
echo "=== THE FINAL BOSS: Finding the Last Real Broken Link ==="

echo "Looking at the remaining 13 broken links..."
echo "12 should be documentation artifacts (session logs documenting broken links)"
echo "1 is our mystery link!"

echo -e "\nLet's find which file has the real broken link:"
python3 check_links.py 2>/dev/null | grep "📁" | grep -v "session-logs/2025-09-14" | grep -v "DOCUMENTATION_UPDATE"

echo -e "\n=== Analyzing each remaining broken link ==="

echo -e "\n1. Session-log-framework deep path:"
echo "   Still showing as broken but file exists. Let's test the path manually:"
cd docs/piper-education/decision-patterns/emergent/
ls -la ../../../development/session-logs/session-log-framework.md 2>/dev/null || echo "   PATH IS WRONG!"
cd ../../../../

echo -e "\n2. [1m formatting - NOT A REAL LINK (ANSI code in code block)"

echo -e "\n3. PIPER.md Configuration - checking:"
grep -n "PIPER.md Configuration" docs/**/*.md 2>/dev/null | grep "../../config"

echo -e "\n4-10. These look like they're IN the documentation artifacts:"
echo "   Checking if these are in session logs or summary docs..."
grep -l "MCP Connection Pool - 642x" docs/development/session-logs/*.md 2>/dev/null | head -1
grep -l "api-design-spec.md" docs/development/session-logs/*.md 2>/dev/null | head -1
grep -l "dev-guide.md" docs/development/session-logs/*.md 2>/dev/null | head -1

echo -e "\n=== THE REAL CULPRIT ==="
echo "Based on the file list, the ONE real broken link is likely:"
echo "The session-log-framework path that STILL doesn't work from piper-education"

echo -e "\n=== Let's fix it once and for all ==="
echo "The path from docs/piper-education/decision-patterns/emergent/ to docs/development/session-logs/"
echo "Should be: ../../../../development/session-logs/session-log-framework.md"
echo "(Up 4 levels to root, then down into development/session-logs/)"
