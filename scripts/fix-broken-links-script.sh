#!/bin/bash

# Fix Broken Documentation Links for GitHub Pages Compatibility
# This script fixes links in docs/ that break when served via GitHub Pages at pmorgan.tech

echo "==================================================="
echo "Fixing Broken Documentation Links for GitHub Pages"
echo "==================================================="

# Change to docs directory
cd /Users/xian/Development/piper-morgan/docs

# Create backups before making changes
echo "Creating backup files (.bak)..."

# Fix 1: Remove 'docs/' prefix from links in README.md
echo ""
echo "Fixing docs/README.md..."
echo "  Removing 'docs/' prefix from internal links..."

# Pattern: [text](docs/path) → [text](path)
sed -i.bak 's|\](docs/|\](|g' README.md

# Pattern: [text](./docs/path) → [text](./path)
sed -i.bak 's|\](./docs/|\](./|g' README.md

# Fix 2: Fix LICENSE and CONTRIBUTING references
echo "  Fixing root-level file references..."

# LICENSE references - needs ../ prefix from docs/
sed -i.bak 's|\[LICENSE\](LICENSE)|[LICENSE](../LICENSE)|g' README.md

# CONTRIBUTING references - needs ../ prefix from docs/
sed -i.bak 's|\[CONTRIBUTING\](CONTRIBUTING.md)|[CONTRIBUTING](../CONTRIBUTING.md)|g' README.md

# Fix 3: Check and report on all markdown files
echo ""
echo "Scanning all markdown files for similar patterns..."

# Find all markdown files with problematic patterns
for file in $(find . -name "*.md" -type f); do
  # Check if file contains docs/ patterns
  if grep -q '\](docs/\|](./docs/' "$file" 2>/dev/null; then
    echo "  Found patterns in: $file"
    # Apply same fixes
    sed -i.bak 's|\](docs/|\](|g' "$file"
    sed -i.bak 's|\](./docs/|\](./|g' "$file"
  fi
done

# Verify changes
echo ""
echo "Verification:"
echo "============="

# Count remaining problematic patterns
docs_pattern_count=$(grep -r '\](docs/' . --include="*.md" 2>/dev/null | wc -l)
dot_docs_pattern_count=$(grep -r '\](./docs/' . --include="*.md" 2>/dev/null | wc -l)

echo "Remaining 'docs/' patterns: $docs_pattern_count"
echo "Remaining './docs/' patterns: $dot_docs_pattern_count"

# Show diff for README.md as example
echo ""
echo "Sample changes in README.md:"
echo "============================"
diff -u README.md.bak README.md | head -30

echo ""
echo "==================================================="
echo "Fix Complete!"
echo "==================================================="
echo ""
echo "Next steps:"
echo "1. Review the changes with: diff -u [file].bak [file]"
echo "2. Test locally if possible"
echo "3. Commit the fixes: git add -A && git commit -m 'Fix broken documentation links for GitHub Pages'"
echo "4. Push to trigger GitHub Pages rebuild"
echo ""
echo "To revert if needed: find . -name '*.bak' -exec sh -c 'mv {} ${0%.bak}' {} \;"
