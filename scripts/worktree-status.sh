#!/bin/bash
#
# worktree-status.sh - Show status of all git worktrees and their coordination mapping
#
# Usage: ./scripts/worktree-status.sh
#
# Shows:
#   - All active worktrees
#   - Their prompt associations from manifest.json
#   - Branch status
#   - Disk usage
#   - Time since creation

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MANIFEST="$PROJECT_ROOT/coordination/manifest.json"
TREES_DIR="$PROJECT_ROOT/.trees"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}=== Git Worktrees Status ===${NC}"
echo ""

# Show git worktree list
echo -e "${BLUE}Git Worktrees:${NC}"
cd "$PROJECT_ROOT"
git worktree list
echo ""

# Check if manifest exists
if [ ! -f "$MANIFEST" ]; then
    echo -e "${YELLOW}Warning: Manifest not found at $MANIFEST${NC}"
    exit 0
fi

# Check if jq is available
if ! command -v jq &> /dev/null; then
    echo -e "${YELLOW}Warning: jq not installed, skipping manifest details${NC}"
    exit 0
fi

echo -e "${BLUE}Coordination Queue Worktrees:${NC}"
echo ""

# Get all prompts with worktree paths
PROMPTS_WITH_WORKTREES=$(jq -r '.prompts[] | select(.worktree_path != null and .worktree_path != "") | "\(.id)|\(.title)|\(.status)|\(.worktree_path)|\(.branch_name)|\(.claimed_by)|\(.worktree_created_at)|\(.cleanup_approved)"' "$MANIFEST" 2>/dev/null || echo "")

if [ -z "$PROMPTS_WITH_WORKTREES" ]; then
    echo "  No worktrees currently assigned to prompts."
    echo ""
else
    printf "%-6s %-25s %-10s %-20s %s\n" "ID" "TITLE" "STATUS" "WORKTREE" "CLEANUP"
    printf "%-6s %-25s %-10s %-20s %s\n" "------" "-------------------------" "----------" "--------------------" "-------"

    echo "$PROMPTS_WITH_WORKTREES" | while IFS='|' read -r id title status worktree branch claimed_by created_at cleanup_approved; do
        # Truncate title if too long
        short_title="${title:0:25}"

        # Format cleanup status
        if [ "$cleanup_approved" = "true" ]; then
            cleanup_status="${GREEN}approved${NC}"
        else
            cleanup_status="${YELLOW}pending${NC}"
        fi

        # Check if worktree directory exists
        full_path="$PROJECT_ROOT/$worktree"
        if [ -d "$full_path" ]; then
            exists="${GREEN}exists${NC}"
        else
            exists="${RED}missing${NC}"
        fi

        printf "%-6s %-25s %-10s %-20s %b\n" "$id" "$short_title" "$status" "$worktree" "$cleanup_status"
    done
    echo ""
fi

# Show disk usage if .trees exists and has content
if [ -d "$TREES_DIR" ] && [ "$(ls -A "$TREES_DIR" 2>/dev/null)" ]; then
    echo -e "${BLUE}Disk Usage:${NC}"
    du -sh "$TREES_DIR"/* 2>/dev/null | while read -r size path; do
        dirname=$(basename "$path")
        echo "  $size  $dirname"
    done
    echo ""

    total=$(du -sh "$TREES_DIR" 2>/dev/null | cut -f1)
    echo "  Total: $total"
    echo ""
fi

# Summary
echo -e "${BLUE}Summary:${NC}"
total_worktrees=$(git worktree list | wc -l | tr -d ' ')
trees_count=$(ls -d "$TREES_DIR"/*/ 2>/dev/null | wc -l | tr -d ' ' || echo "0")
echo "  Git worktrees: $total_worktrees (including main)"
echo "  Agent worktrees in .trees/: $trees_count"

# Check for orphaned worktrees
orphaned=$(git worktree list --porcelain | grep -c "prunable" 2>/dev/null || true)
orphaned=${orphaned:-0}
if [ "$orphaned" -gt 0 ] 2>/dev/null; then
    echo -e "  ${YELLOW}Orphaned references: $orphaned (run 'git worktree prune' to clean)${NC}"
fi

echo ""
