#!/bin/bash
# Fix end-of-file newlines for all text files
# This helps prevent pre-commit hook failures

set -e

echo "🔧 Fixing end-of-file newlines..."

# Find all text files (excluding binary, venv, node_modules, .git)
find . -type f \
  -not -path "./venv/*" \
  -not -path "./node_modules/*" \
  -not -path "./.git/*" \
  -not -path "*/\.*" \
  -not -name "*.pyc" \
  -not -name "*.png" \
  -not -name "*.jpg" \
  -not -name "*.jpeg" \
  -not -name "*.gif" \
  -not -name "*.ico" \
  -not -name "*.pdf" \
  \( -name "*.py" -o -name "*.md" -o -name "*.txt" -o -name "*.yml" -o -name "*.yaml" -o -name "*.json" \) \
  -exec sh -c '
    for file do
      # Check if file ends with newline
      if [ -n "$(tail -c 1 "$file")" ]; then
        echo "  Fixing: $file"
        echo "" >> "$file"
      fi
    done
  ' sh {} +

echo "✅ Done! Files should now pass pre-commit hooks on first try."
