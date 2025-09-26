#!/bin/bash
echo "=== Cleaning up git staging area ==="

# First, let's unstage everything and be selective
echo "1. Resetting staging area to be selective..."
git reset HEAD

# Now add ONLY the documentation we want
echo -e "\n2. Adding ONLY the recovered documentation..."

# OMNIBUS logs and synthesis docs
git add docs/development/session-logs/2025-09-*-OMNIBUS-chronological-log.md
git add docs/development/session-logs/GENESIS-DOCUMENTS-PACKAGE.md
git add docs/development/session-logs/OMNIBUS-*.md
git add docs/development/session-logs/PATTERNS-AND-INSIGHTS.md

# Weekly ships
git add docs/development/weekly-ship/weekly-ship-*.md

# Canonical queries (the gem we recovered)
git add docs/development/canonical-queries-architecture.md

# Team migration guide placeholder
git add docs/development/team-migration-guide.md

# Recent session logs from today
git add docs/development/session-logs/2025-09-15-*.md

echo -e "\n3. What's staged now (should be just docs):"
git status --short | grep "^A"

echo -e "\n=== NOW safe to commit with: ==="
echo 'git commit -m "Phase 2: Recover stranded docs - OMNIBUS logs, weekly ships, canonical queries"'

echo -e "\n=== Other files that showed up ==="
echo "Various testing guides, .claude settings, analysis files - these need separate review"
echo "Run 'git status' after commit to see what else needs attention"
