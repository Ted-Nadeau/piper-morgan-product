#!/bin/bash
# Commit helper - Runs pre-commit fixes before allowing commit
# Usage: ./scripts/commit.sh "commit message"
#        OR
#        ./scripts/commit.sh  (then run git commit manually)

set -e

echo "🚀 Pre-Commit Routine Starting..."
echo ""

# Step 1: Fix newlines
echo "Step 1/3: Fixing end-of-file newlines..."
./scripts/fix-newlines.sh
echo ""

# Step 2: Stage all changes
echo "Step 2/3: Staging changes..."
git add -u
echo "✅ Changes staged"
echo ""

# Step 3: Commit (if message provided) or prompt user
if [ -n "$1" ]; then
    echo "Step 3/3: Committing with message: $1"
    git commit -m "$1"
    echo ""
    echo "✅ Commit complete!"
else
    echo "Step 3/3: Ready to commit!"
    echo ""
    echo "Run one of:"
    echo "  git commit -m 'your message'"
    echo "  git commit  (for multi-line message in editor)"
    echo ""
    echo "Or re-run with message:"
    echo "  ./scripts/commit.sh 'your commit message'"
fi
