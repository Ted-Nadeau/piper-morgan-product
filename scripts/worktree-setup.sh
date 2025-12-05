#!/bin/bash
#
# worktree-setup.sh - Create an isolated git worktree for agent work
#
# Usage: ./scripts/worktree-setup.sh <prompt-id> <session-id>
#
# Creates:
#   - .trees/<prompt-id>-<short-session>/ directory
#   - New branch: claude/<prompt-title>-<session-id>
#   - Updates coordination/manifest.json with worktree metadata
#
# Example:
#   ./scripts/worktree-setup.sh 004 2025-12-04-0732-spec-code-opus
#   Creates: .trees/004-073253/
#   Branch:  claude/my-feature-2025-12-04-0732-spec-code-opus

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
    echo "Usage: $0 <prompt-id> <session-id>"
    echo ""
    echo "Arguments:"
    echo "  prompt-id   - ID from coordination/manifest.json (e.g., 004)"
    echo "  session-id  - Your agent session ID (e.g., 2025-12-04-0732-spec-code-opus)"
    echo ""
    echo "Example:"
    echo "  $0 004 2025-12-04-0732-spec-code-opus"
    exit 1
}

# Check arguments
if [ $# -ne 2 ]; then
    usage
fi

PROMPT_ID="$1"
SESSION_ID="$2"

# Extract short session (first 6 chars after date prefix, or last 6 if no date)
if [[ "$SESSION_ID" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}- ]]; then
    # Has date prefix: 2025-12-04-0732-spec-code-opus -> take chars after last date segment
    SHORT_SESSION="${SESSION_ID:11:6}"
else
    # No date prefix: take last 6 chars
    SHORT_SESSION="${SESSION_ID: -6}"
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
PROMPT_TITLE=$(jq -r ".prompts[] | select(.id==\"$PROMPT_ID\") | .title" "$MANIFEST")

if [ -z "$PROMPT_STATUS" ] || [ "$PROMPT_STATUS" = "null" ]; then
    echo -e "${RED}Error: Prompt '$PROMPT_ID' not found in manifest${NC}"
    exit 1
fi

if [ "$PROMPT_STATUS" != "available" ]; then
    echo -e "${RED}Error: Prompt '$PROMPT_ID' is not available (status: $PROMPT_STATUS)${NC}"
    exit 1
fi

# Sanitize title for branch name (lowercase, replace spaces with dashes, remove special chars)
SAFE_TITLE=$(echo "$PROMPT_TITLE" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-' | cut -c1-30)

# Construct names
WORKTREE_NAME="${PROMPT_ID}-${SHORT_SESSION}"
WORKTREE_PATH="$TREES_DIR/$WORKTREE_NAME"
BRANCH_NAME="claude/${SAFE_TITLE}-${SESSION_ID}"

# Check if worktree already exists
if [ -d "$WORKTREE_PATH" ]; then
    echo -e "${RED}Error: Worktree already exists at $WORKTREE_PATH${NC}"
    exit 1
fi

# Check if branch already exists
if git rev-parse --verify "$BRANCH_NAME" &>/dev/null; then
    echo -e "${YELLOW}Warning: Branch $BRANCH_NAME already exists, will use existing branch${NC}"
    CREATE_BRANCH=""
else
    CREATE_BRANCH="-b"
fi

# Ensure .trees directory exists
mkdir -p "$TREES_DIR"

echo -e "${GREEN}Creating worktree for prompt $PROMPT_ID...${NC}"
echo "  Worktree: $WORKTREE_PATH"
echo "  Branch:   $BRANCH_NAME"

# Create the worktree
cd "$PROJECT_ROOT"
if [ -n "$CREATE_BRANCH" ]; then
    git worktree add -b "$BRANCH_NAME" "$WORKTREE_PATH" main
else
    git worktree add "$WORKTREE_PATH" "$BRANCH_NAME"
fi

# Update manifest.json
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Create temporary file with updated manifest
jq --arg id "$PROMPT_ID" \
   --arg status "claimed" \
   --arg claimed_by "$SESSION_ID" \
   --arg claimed_at "$TIMESTAMP" \
   --arg branch "$BRANCH_NAME" \
   --arg worktree ".trees/$WORKTREE_NAME" \
   --arg worktree_created "$TIMESTAMP" \
   '(.prompts[] | select(.id == $id)) |= . + {
     status: $status,
     claimed_by: $claimed_by,
     claimed_at: $claimed_at,
     branch_name: $branch,
     worktree_path: $worktree,
     worktree_created_at: $worktree_created,
     cleanup_approved: false
   }' "$MANIFEST" > "${MANIFEST}.tmp"

# Also update last_updated timestamp
jq --arg ts "$TIMESTAMP" '.last_updated = $ts' "${MANIFEST}.tmp" > "${MANIFEST}.tmp2"
mv "${MANIFEST}.tmp2" "$MANIFEST"
rm -f "${MANIFEST}.tmp"

echo ""
echo -e "${GREEN}Worktree created successfully!${NC}"
echo ""
echo "Next steps:"
echo "  1. cd $WORKTREE_PATH"
echo "  2. Do your work in this isolated directory"
echo "  3. Commit and push to branch: $BRANCH_NAME"
echo "  4. When complete, update manifest status to 'complete'"
echo ""
echo "Your working directory is now isolated from other agents."
