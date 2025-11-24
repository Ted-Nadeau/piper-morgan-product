#!/bin/bash
# Check all services/ subdirectories have __init__.py
# Prevents Python 3.3+ namespace package issues

set -e

EXIT_CODE=0
MISSING_COUNT=0

# Find all directories under services/ that contain .py files but lack __init__.py
while IFS= read -r dir; do
    # Skip __pycache__ and test directories
    if [[ "$dir" == *"/__pycache__"* ]] || [[ "$dir" == *"/tests"* ]]; then
        continue
    fi

    # Check if directory contains any .py files (excluding __init__.py)
    py_count=$(find "$dir" -maxdepth 1 -name "*.py" -not -name "__init__.py" 2>/dev/null | wc -l)

    if [ "$py_count" -gt 0 ] && [ ! -f "$dir/__init__.py" ]; then
        echo "❌ Missing __init__.py: $dir"
        ((MISSING_COUNT++))
        EXIT_CODE=1
    fi
done < <(find services/ -type d 2>/dev/null)

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ All services/ directories have __init__.py"
else
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "❌ Found $MISSING_COUNT directories missing __init__.py"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Fix with:"
    echo "  ./scripts/create_missing_init_files.sh"
    echo ""
    echo "Or manually:"
    echo "  echo '# module_name module' > path/to/missing/__init__.py"
    echo ""
fi

exit $EXIT_CODE
