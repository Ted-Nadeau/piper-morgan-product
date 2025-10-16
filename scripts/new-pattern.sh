#!/bin/bash
# Create a new pattern with auto-incremented number
# Usage: ./scripts/new-pattern.sh <pattern-name> [category]

set -e

PATTERNS_DIR="docs/internal/architecture/current/patterns"
TEMPLATE="$PATTERNS_DIR/pattern-000-template.md"

# Check if pattern name provided
if [ -z "$1" ]; then
    echo "Usage: ./scripts/new-pattern.sh <pattern-name> [category]"
    echo ""
    echo "Example: ./scripts/new-pattern.sh rate-limiting"
    echo "Creates: pattern-035-rate-limiting.md"
    echo ""
    echo "Categories (optional):"
    echo "  - core          (Core Architecture Patterns)"
    echo "  - data          (Data & Query Patterns)"
    echo "  - ai            (AI & Intelligence Patterns)"
    echo "  - integration   (Integration & Platform Patterns)"
    echo "  - development   (Development & Process Patterns)"
    exit 1
fi

PATTERN_NAME="$1"
CATEGORY="${2:-}"

# Find the next pattern number
NEXT_NUMBER=$(find "$PATTERNS_DIR" -name "pattern-[0-9][0-9][0-9]-*.md" \
    | sed 's/.*pattern-\([0-9][0-9][0-9]\)-.*/\1/' \
    | sort -n \
    | tail -1 \
    | awk '{print $1 + 1}')

# Pad to 3 digits
NEXT_NUMBER_PADDED=$(printf "%03d" "$NEXT_NUMBER")

# Create filename
FILENAME="pattern-${NEXT_NUMBER_PADDED}-${PATTERN_NAME}.md"
FILEPATH="$PATTERNS_DIR/$FILENAME"

# Check if file already exists
if [ -f "$FILEPATH" ]; then
    echo "❌ Error: $FILEPATH already exists!"
    exit 1
fi

# Copy template
cp "$TEMPLATE" "$FILEPATH"

# Update pattern number in file
sed -i '' "s/Pattern-000/Pattern-${NEXT_NUMBER_PADDED}/g" "$FILEPATH"
sed -i '' "s/Pattern 000/Pattern ${NEXT_NUMBER_PADDED}/g" "$FILEPATH"

echo "✅ Created: $FILEPATH"
echo ""
echo "Next steps:"
echo "1. Edit the pattern file: $FILEPATH"
echo "2. Add to README.md in appropriate category"
if [ -n "$CATEGORY" ]; then
    echo "   Suggested category: $CATEGORY"
fi
echo "3. Update total count in README.md header"
echo ""
echo "Current pattern number: $NEXT_NUMBER_PADDED"
