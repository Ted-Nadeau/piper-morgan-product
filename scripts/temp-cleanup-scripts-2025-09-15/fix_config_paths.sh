#!/bin/bash
# Fix config paths based on document location

echo "=== Fixing Config Paths ==="

# Fix config paths that should point to ../config/ or ../../config/
echo "Finding and fixing config path references..."

# From docs/ level
find docs -maxdepth 1 -name "*.md" -exec sed -i '' 's|config/PIPER\.user\.md|../config/PIPER.user.md|g' {} \;

# From docs/development/ level
find docs/development -name "*.md" -exec sed -i '' 's|config/PIPER\.user\.md|../../config/PIPER.user.md|g' {} \;

# From docs/architecture/ level
find docs/architecture -name "*.md" -exec sed -i '' 's|config/PIPER\.user\.md|../../config/PIPER.user.md|g' {} \;

echo "Config path fixes complete!"
