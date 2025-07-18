#!/bin/bash

# Check if backlog or roadmap changed
if git diff --cached --name-only | grep -qE "(backlog|roadmap)\.md"; then
    echo "📋 Planning docs changed - analyzing GitHub sync status..."
    echo ""

    # Check if backlog.md specifically changed
    if git diff --cached --name-only | grep -q "backlog\.md"; then
        echo "🔍 Checking for new/modified PM tickets..."

        # Run the GitHub issue generator in check mode to see what's missing
        if python scripts/generate_github_issues.py --check-existing 2>/dev/null; then
            echo ""
            echo "💡 To create missing GitHub issues:"
            echo "   python scripts/generate_github_issues.py --dry-run  # Preview commands"
            echo "   python scripts/generate_github_issues.py            # Create issues"
        else
            echo "⚠️  Could not check GitHub (gh CLI may need setup)"
            echo "   Manual check: gh issue list --search 'PM-'"
        fi

        # Check for completed items (✅ status changes)
        if git diff --cached docs/planning/backlog.md | grep -q "✅ COMPLETE"; then
            echo ""
            echo "✅ Detected completed PM tickets - remember to close in GitHub:"
            echo "   gh issue close <issue-number> --comment 'Completed: <details>'"
        fi

        # Check for status changes
        if git diff --cached docs/planning/backlog.md | grep -q "Status.*:"; then
            echo ""
            echo "🔄 Status changes detected - consider updating GitHub issue labels/status"
        fi
    fi

    echo ""
    echo "📝 General reminders:"
    echo "   • New PM-XXX items → Create GitHub issues"
    echo "   • Completed items → Close GitHub issues"
    echo "   • Status changes → Update GitHub labels"
fi

# Always pass (this is just a reminder)
exit 0
