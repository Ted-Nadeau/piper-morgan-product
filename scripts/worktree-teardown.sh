#!/bin/bash
#
# worktree-teardown.sh - Remove a git worktree after PM approval
#
# Usage: ./scripts/worktree-teardown.sh <prompt-id> [--force]
#
# Removes:
#   - .trees/<prompt-id>-*/ directory
#   - Cleans up git worktree references
#
# Requires:
#   - cleanup_approved: true in manifest.json (unless --force)
#
# Example:
#   ./scripts/worktree-teardown.sh 004
#   ./scripts/worktree-teardown.sh 004 --force  # Skip approval check

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MANIFEST="$PROJECT_ROOT/coordination/manifest.json"
TREES_DIR="$PROJECT_ROOT/.trees"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

usage() {
    echo "Usage: $0 <prompt-id> [--force]"
    echo ""
    echo "Arguments:"
    echo "  prompt-id   - ID from coordination/manifest.json (e.g., 004)"
    echo "  --force     - Skip PM approval check (use with caution)"
    echo ""
    echo "Example:"
    echo "  $0 004"
    echo "  $0 004 --force"
    exit 1
}

# Check arguments
if [ $# -lt 1 ]; then
    usage
fi

PROMPT_ID="$1"
FORCE=""

if [ "$2" = "--force" ]; then
    FORCE="true"
fi

# Check if manifest exists
if [ ! -f "$MANIFEST" ]; then
    echo -e "${RED}Error: Manifest not found at $MANIFEST${NC}"
    exit 1
fi

# Check if jq is available
if ! command -v jq &> /dev/null; then
    echo -e "${RED}Error: jq is required but not installed${NC}"
    echo "Install with: brew install jq"
    exit 1
fi

# Get prompt info from manifest
PROMPT_STATUS=$(jq -r ".prompts[] | select(.id==\"$PROMPT_ID\") | .status" "$MANIFEST")
WORKTREE_PATH=$(jq -r ".prompts[] | select(.id==\"$PROMPT_ID\") | .worktree_path" "$MANIFEST")
CLEANUP_APPROVED=$(jq -r ".prompts[] | select(.id==\"$PROMPT_ID\") | .cleanup_approved" "$MANIFEST")

if [ -z "$PROMPT_STATUS" ] || [ "$PROMPT_STATUS" = "null" ]; then
    echo -e "${RED}Error: Prompt '$PROMPT_ID' not found in manifest${NC}"
    exit 1
fi

if [ -z "$WORKTREE_PATH" ] || [ "$WORKTREE_PATH" = "null" ]; then
    echo -e "${RED}Error: No worktree path found for prompt '$PROMPT_ID'${NC}"
    exit 1
fi

# Check cleanup approval (unless --force)
if [ -z "$FORCE" ]; then
    if [ "$CLEANUP_APPROVED" != "true" ]; then
        echo -e "${RED}Error: Cleanup not approved for prompt '$PROMPT_ID'${NC}"
        echo ""
        echo "To approve cleanup, update manifest.json:"
        echo "  Set \"cleanup_approved\": true for prompt $PROMPT_ID"
        echo ""
        echo "Or use --force to skip this check (not recommended)"
        exit 1
    fi
fi

# Resolve full path
FULL_WORKTREE_PATH="$PROJECT_ROOT/$WORKTREE_PATH"

# Check if worktree exists
if [ ! -d "$FULL_WORKTREE_PATH" ]; then
    echo -e "${YELLOW}Warning: Worktree directory not found at $FULL_WORKTREE_PATH${NC}"
    echo "It may have already been removed."
else
    echo -e "${GREEN}Removing worktree for prompt $PROMPT_ID...${NC}"
    echo "  Path: $FULL_WORKTREE_PATH"

    # Remove the worktree directory
    rm -rf "$FULL_WORKTREE_PATH"
    echo "  Directory removed."
fi

# Prune git worktree references
cd "$PROJECT_ROOT"
git worktree prune
echo "  Git worktree references pruned."

# Update manifest.json - clear worktree fields
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

jq --arg id "$PROMPT_ID" \
   --arg cleaned_at "$TIMESTAMP" \
   '(.prompts[] | select(.id == $id)) |= . + {
     worktree_cleaned_at: $cleaned_at
   }' "$MANIFEST" > "${MANIFEST}.tmp"

jq --arg ts "$TIMESTAMP" '.last_updated = $ts' "${MANIFEST}.tmp" > "${MANIFEST}.tmp2"
mv "${MANIFEST}.tmp2" "$MANIFEST"
rm -f "${MANIFEST}.tmp"

echo ""
echo -e "${GREEN}Worktree cleaned up successfully!${NC}"
echo ""
echo "Prompt $PROMPT_ID worktree has been removed."
echo "The branch still exists and can be checked out if needed."
