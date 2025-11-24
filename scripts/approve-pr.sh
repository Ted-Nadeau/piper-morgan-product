#!/bin/bash
# Quick PR approver using piper-reviewer account
# Usage: ./scripts/approve-pr.sh <PR_NUMBER>

if [ -z "$1" ]; then
    echo "Usage: ./scripts/approve-pr.sh <PR_NUMBER>"
    echo "Example: ./scripts/approve-pr.sh 123"
    exit 1
fi

PR_NUMBER=$1

# Use piper-reviewer token (set as environment variable)
if [ -z "$PIPER_REVIEWER_TOKEN" ]; then
    echo "Error: PIPER_REVIEWER_TOKEN environment variable not set"
    echo "Please set: export PIPER_REVIEWER_TOKEN=your_token_here"
    exit 1
fi

echo "Approving PR #${PR_NUMBER} as piper-reviewer..."

# Use GitHub API directly
curl -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer ${PIPER_REVIEWER_TOKEN}" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/mediajunkie/piper-morgan-product/pulls/${PR_NUMBER}/reviews \
  -d '{"event":"APPROVE","body":"✅ Auto-approved by piper-reviewer bot"}'

echo ""
echo "Done! Check https://github.com/mediajunkie/piper-morgan-product/pull/${PR_NUMBER}"
