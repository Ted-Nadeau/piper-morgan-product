#!/bin/bash

# Branch Management Quick Guidance Script
# Run this when you need help with branch decisions

echo "🌿 Piper Morgan Branch Management Quick Reference"
echo "=================================================="
echo ""

# Get current branch
CURRENT_BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "📍 Current Branch: $CURRENT_BRANCH"
else
    echo "❌ Not in a git repository"
    exit 1
fi

echo ""

# Show branch type and recommendations
if [[ "$CURRENT_BRANCH" == "main" ]]; then
    echo "🎯 MAIN BRANCH DETECTED"
    echo "   ✅ Good for: Major milestones, infrastructure, critical fixes"
    echo "   ⚠️  Consider: Feature branch for new development work"
    echo ""
    echo "📋 Quick Actions:"
    echo "   git checkout -b feature/your-feature-name"
    echo "   git checkout -b dev/your-experiment"
    echo ""
elif [[ "$CURRENT_BRANCH" == feature/* ]]; then
    echo "🚀 FEATURE BRANCH DETECTED"
    echo "   ✅ Good for: New features, major changes, user-facing work"
    echo "   📋 When complete: Create PR or merge to main"
    echo ""
    echo "📋 Quick Actions:"
    echo "   git push origin $CURRENT_BRANCH  # Push for PR"
    echo "   git checkout main && git merge $CURRENT_BRANCH  # Merge when ready"
    echo ""
elif [[ "$CURRENT_BRANCH" == dev/* ]]; then
    echo "🔬 DEVELOPMENT BRANCH DETECTED"
    echo "   ✅ Good for: Experiments, research, work in progress"
    echo "   ⚠️  Note: Usually stays on development, not merged to main"
    echo ""
    echo "📋 Quick Actions:"
    echo "   git checkout main  # Switch to main when done"
    echo "   git branch -d $CURRENT_BRANCH  # Clean up when finished"
    echo ""
else
    echo "❓ UNKNOWN BRANCH TYPE"
    echo "   📋 Check: docs/development/BRANCH-MANAGEMENT.md"
    echo ""
fi

# Show branch health
echo "🏥 Branch Health Check:"
echo "========================"

# Check if branch is up to date with main
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "Checking if branch is up to date with main..."
    git fetch origin main >/dev/null 2>&1

    COMMITS_AHEAD=$(git rev-list --count main..HEAD 2>/dev/null)
    COMMITS_BEHIND=$(git rev-list --count HEAD..main 2>/dev/null)

    if [ "$COMMITS_AHEAD" -gt 0 ]; then
        echo "   📤 Commits ahead of main: $COMMITS_AHEAD"
    fi

    if [ "$COMMITS_BEHIND" -gt 0 ]; then
        echo "   📥 Commits behind main: $COMMITS_BEHIND"
        echo "   ⚠️  Consider: git rebase main or git merge main"
    fi

    if [ "$COMMITS_AHEAD" -eq 0 ] && [ "$COMMITS_BEHIND" -eq 0 ]; then
        echo "   ✅ Branch is up to date with main"
    fi
fi

echo ""
echo "📚 Full Documentation: docs/development/BRANCH-MANAGEMENT.md"
echo "🔧 Quick Commands:"
echo "   ./scripts/branch-guidance.sh  # This script"
echo "   git branch -v                  # Show all branches"
echo "   git checkout -b feature/name   # Create feature branch"
echo "   git checkout -b dev/name       # Create dev branch"
echo ""

# Show current branch status
echo "📊 Current Repository Status:"
echo "=============================="
git status --porcelain | head -10
if [ $(git status --porcelain | wc -l) -gt 10 ]; then
    echo "   ... and more files"
fi

echo ""
echo "🌿 Happy branching! Remember: docs/development/BRANCH-MANAGEMENT.md"
