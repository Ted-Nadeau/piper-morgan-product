#!/bin/bash
echo "=== PHASE 2: Stranded Documentation Recovery ==="
echo "Searching for documentation in unmerged feature branches..."
echo ""

# Get current branch for reference
CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"
echo ""

# Fetch all branches to ensure we have latest
echo "Fetching latest branch information..."
git fetch --all --quiet

echo -e "\n=== LOCAL BRANCHES ==="
git branch | grep -v "$CURRENT_BRANCH" | while read branch; do
    branch=$(echo $branch | tr -d ' *')
    echo "Checking branch: $branch"

    # Check for markdown files different from main
    DIFF_FILES=$(git diff main..$branch --name-only 2>/dev/null | grep "\.md$" | head -10)
    if [ ! -z "$DIFF_FILES" ]; then
        echo "  Found documentation differences:"
        echo "$DIFF_FILES" | while read file; do
            # Check if file exists in main
            if git show main:$file &>/dev/null; then
                echo "    ✏️  Modified: $file"
            else
                echo "    ✨ New file: $file"
            fi
        done
    fi
    echo ""
done

echo "=== REMOTE BRANCHES ==="
git branch -r | grep -v HEAD | grep -v "$CURRENT_BRANCH" | while read branch; do
    # Skip if we already checked local version
    local_branch=$(echo $branch | sed 's/origin\///')
    if git branch | grep -q "$local_branch"; then
        continue
    fi

    echo "Checking remote branch: $branch"

    # Check for markdown files different from main
    DIFF_FILES=$(git diff main..$branch --name-only 2>/dev/null | grep "\.md$" | head -10)
    if [ ! -z "$DIFF_FILES" ]; then
        echo "  Found documentation differences:"
        echo "$DIFF_FILES" | while read file; do
            if git show main:$file &>/dev/null; then
                echo "    ✏️  Modified: $file"
            else
                echo "    ✨ New file: $file"
            fi
        done
    fi
    echo ""
done

echo "=== STASH CHECK ==="
STASH_COUNT=$(git stash list | wc -l)
if [ "$STASH_COUNT" -gt 0 ]; then
    echo "Found $STASH_COUNT stashed changes"
    git stash list | while read stash; do
        STASH_ID=$(echo $stash | cut -d: -f1)
        echo "Checking $STASH_ID..."
        git stash show $STASH_ID --name-only | grep "\.md$" | while read file; do
            echo "  📎 Stashed doc: $file"
        done
    done
else
    echo "No stashed changes found"
fi

echo -e "\n=== UNTRACKED FILES ==="
git status --porcelain | grep "^??" | grep "\.md$" | while read line; do
    file=$(echo $line | cut -d' ' -f2)
    echo "  🔍 Untracked: $file"
done

echo -e "\n=== RECOVERY RECOMMENDATIONS ==="
echo "To examine a specific branch's documentation:"
echo "  git checkout <branch-name>"
echo "  git diff main --name-only | grep '\.md'"
echo ""
echo "To cherry-pick specific documentation:"
echo "  git checkout main"
echo "  git checkout <branch-name> -- path/to/doc.md"
echo ""
echo "To see content of stranded file without switching:"
echo "  git show <branch-name>:path/to/file.md"
