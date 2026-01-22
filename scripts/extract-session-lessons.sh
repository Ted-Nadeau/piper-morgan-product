#!/bin/bash
# extract-session-lessons.sh
# Extract potential anti-patterns from session log "lessons learned" sections
# Best performing strategy (60% precision) from Phase 2 experiment
#
# Usage: ./scripts/extract-session-lessons.sh [start_date] [end_date]
# Example: ./scripts/extract-session-lessons.sh 2026-01-01 2026-01-21

set -e

START_DATE=${1:-$(date -v-30d +%Y-%m-%d)}
END_DATE=${2:-$(date +%Y-%m-%d)}
OUTPUT_FILE="dev/active/emergent-lesson-candidates.md"

echo "# Emergent Anti-Pattern Candidates: Session Log Lessons"
echo ""
echo "**Generated**: $(date +%Y-%m-%d)"
echo "**Period**: $START_DATE to $END_DATE"
echo ""
echo "---"
echo ""

# Search patterns (from Phase 2 experiment - 60% precision)
PATTERNS=(
    "lesson learned"
    "should have"
    "in retrospect"
    "mistake was"
    "next time"
    "root cause"
    "what went wrong"
)

echo "## Candidates by Pattern"
echo ""

for pattern in "${PATTERNS[@]}"; do
    echo "### Pattern: \"$pattern\""
    echo ""
    # Search omnibus logs
    grep -rn -i "$pattern" docs/omnibus-logs/ 2>/dev/null | head -20 || echo "_No matches in omnibus logs_"
    echo ""
    # Search session logs (dev/YYYY/MM/)
    grep -rn -i "$pattern" dev/2026/ dev/2025/ 2>/dev/null | head -20 || echo "_No matches in session logs_"
    echo ""
    echo "---"
    echo ""
done

echo "## Classification Template"
echo ""
echo "| Candidate | File:Line | Classification | Notes |"
echo "|-----------|-----------|----------------|-------|"
echo "| [description] | [file:line] | TRUE EMERGENT / VARIATION / FALSE POSITIVE | [notes] |"
echo ""
echo "---"
echo ""
echo "*Run classification manually, then update anti-pattern-index.md with TRUE EMERGENT entries*"
