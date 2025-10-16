#!/bin/bash
# Create a new ADR with auto-incremented number
# Usage: ./scripts/new-adr.sh <adr-title>

set -e

ADRS_DIR="docs/internal/architecture/current/adrs"
TEMPLATE="$ADRS_DIR/adr-000-template.md"

# Check if ADR title provided
if [ -z "$1" ]; then
    echo "Usage: ./scripts/new-adr.sh <adr-title>"
    echo ""
    echo "Example: ./scripts/new-adr.sh use-redis-for-caching"
    echo "Creates: adr-044-use-redis-for-caching.md"
    echo ""
    echo "Title format: kebab-case (lowercase with hyphens)"
    exit 1
fi

ADR_TITLE="$1"

# Find the next ADR number
NEXT_NUMBER=$(find "$ADRS_DIR" -name "adr-[0-9][0-9][0-9]-*.md" \
    | sed 's/.*adr-\([0-9][0-9][0-9]\)-.*/\1/' \
    | sort -n \
    | tail -1 \
    | awk '{print $1 + 1}')

# Pad to 3 digits
NEXT_NUMBER_PADDED=$(printf "%03d" "$NEXT_NUMBER")

# Create filename
FILENAME="adr-${NEXT_NUMBER_PADDED}-${ADR_TITLE}.md"
FILEPATH="$ADRS_DIR/$FILENAME"

# Check if file already exists
if [ -f "$FILEPATH" ]; then
    echo "❌ Error: $FILEPATH already exists!"
    exit 1
fi

# Check if template exists
if [ ! -f "$TEMPLATE" ]; then
    echo "❌ Error: Template not found at $TEMPLATE"
    exit 1
fi

# Copy template
cp "$TEMPLATE" "$FILEPATH"

# Update ADR number in file
sed -i '' "s/ADR-000/ADR-${NEXT_NUMBER_PADDED}/g" "$FILEPATH"
sed -i '' "s/ADR 000/ADR ${NEXT_NUMBER_PADDED}/g" "$FILEPATH"

# Update date
TODAY=$(date +"%Y-%m-%d")
sed -i '' "s/YYYY-MM-DD/$TODAY/g" "$FILEPATH"

echo "✅ Created: $FILEPATH"
echo ""
echo "Next steps:"
echo "1. Edit the ADR file: $FILEPATH"
echo "2. Fill in the decision context and alternatives"
echo "3. Document the decision and consequences"
echo "4. Commit when ready"
echo ""
echo "Current ADR number: $NEXT_NUMBER_PADDED"
echo "Date: $TODAY"
