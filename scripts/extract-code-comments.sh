#!/bin/bash
# extract-code-comments.sh
# Extract warning/caution/hack comments from Python code
# High feasibility strategy (50% precision) from Phase 2 experiment
#
# Usage: ./scripts/extract-code-comments.sh [directory]
# Example: ./scripts/extract-code-comments.sh services/

set -e

SEARCH_DIR=${1:-services/}
OUTPUT_FILE="dev/active/emergent-comment-candidates.md"

echo "# Emergent Anti-Pattern Candidates: Code Comments"
echo ""
echo "**Generated**: $(date +%Y-%m-%d)"
echo "**Directory**: $SEARCH_DIR"
echo ""
echo "---"
echo ""

# Comment patterns (from Phase 2 experiment - 50% precision)
echo "## WARNING Comments"
echo ""
echo '```'
grep -rn "# WARNING" "$SEARCH_DIR" --include="*.py" 2>/dev/null || echo "No WARNING comments found"
echo '```'
echo ""

echo "## CAUTION Comments"
echo ""
echo '```'
grep -rn "# CAUTION" "$SEARCH_DIR" --include="*.py" 2>/dev/null || echo "No CAUTION comments found"
echo '```'
echo ""

echo "## HACK Comments"
echo ""
echo '```'
grep -rn "# HACK" "$SEARCH_DIR" --include="*.py" 2>/dev/null || echo "No HACK comments found"
echo '```'
echo ""

echo "## XXX Comments"
echo ""
echo '```'
grep -rn "# XXX" "$SEARCH_DIR" --include="*.py" 2>/dev/null || echo "No XXX comments found"
echo '```'
echo ""

echo "## FIXME Comments"
echo ""
echo '```'
grep -rn "# FIXME" "$SEARCH_DIR" --include="*.py" 2>/dev/null || echo "No FIXME comments found"
echo '```'
echo ""

echo "## TODO with Warning Language"
echo ""
echo '```'
grep -rn "# TODO.*[Dd]on't\|# TODO.*[Aa]void\|# TODO.*[Nn]ever" "$SEARCH_DIR" --include="*.py" 2>/dev/null || echo "No TODO warnings found"
echo '```'
echo ""

echo "---"
echo ""
echo "## Classification Template"
echo ""
echo "| Candidate | File:Line | Classification | Notes |"
echo "|-----------|-----------|----------------|-------|"
echo "| [description] | [file:line] | TRUE EMERGENT / VARIATION / FALSE POSITIVE | [notes] |"
echo ""
echo "---"
echo ""
echo "*Run classification manually, then update anti-pattern-index.md with TRUE EMERGENT entries*"
