#!/bin/bash
echo "=== PHASE 1: Doc Cleanup - Cross-Reference Verification ==="
echo "Verifying all references in methodology-core files..."
echo ""

METHODOLOGY_DIR="docs/development/methodology-core"

if [ ! -d "$METHODOLOGY_DIR" ]; then
    echo "ERROR: Methodology directory not found at $METHODOLOGY_DIR"
    echo "Searching for methodology files..."
    find docs -name "*methodology*" -type d
    exit 1
fi

echo "Checking references in $METHODOLOGY_DIR..."
echo ""

# Check each markdown file in methodology-core
for file in "$METHODOLOGY_DIR"/*.md; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        echo "=== Checking: $filename ==="

        # Extract all markdown links
        grep -o '\[.*\]([^)]*)' "$file" | while read -r link; do
            # Extract the path from the link
            path=$(echo "$link" | sed 's/.*(\(.*\))/\1/')

            # Skip external links and anchors
            if [[ "$path" == http* ]] || [[ "$path" == "#"* ]] || [[ "$path" == mailto:* ]]; then
                continue
            fi

            # Resolve the path relative to the file's directory
            resolved_path="$METHODOLOGY_DIR/$path"
            resolved_path=$(echo "$resolved_path" | sed 's|/./|/|g') # Remove /./

            # Check if the file exists
            if [ ! -f "$resolved_path" ]; then
                echo "  ❌ Broken reference: $path"
                echo "     Expected at: $resolved_path"
            fi
        done

        # Also check for methodology files referenced outside methodology-core
        grep -o 'methodology[^)]*.md' "$file" | while read -r ref; do
            if [[ ! "$ref" == *"methodology-core"* ]]; then
                echo "  ⚠️  Methodology file referenced outside core: $ref"
            fi
        done

        echo ""
    fi
done

echo "=== CHECKING FOR METHODOLOGY FILES OUTSIDE CORE ==="
find docs -name "*methodology*.md" -type f ! -path "*/methodology-core/*" ! -path "*/session-logs/*" ! -path "*/archive/*" | while read file; do
    echo "  Found: $file"
    echo "    Size: $(wc -l < "$file") lines"
    echo "    Modified: $(stat -f "%Sm" -t "%Y-%m-%d" "$file" 2>/dev/null || stat -c "%y" "$file" | cut -d' ' -f1)"
done

echo ""
echo "=== SUMMARY ==="
echo "Methodology files in core: $(find "$METHODOLOGY_DIR" -name "*.md" -type f | wc -l)"
echo "Methodology files outside core: $(find docs -name "*methodology*.md" -type f ! -path "*/methodology-core/*" ! -path "*/session-logs/*" ! -path "*/archive/*" | wc -l)"
echo ""
echo "Note: Some references might be false positives if they use complex relative paths."
echo "Manual verification recommended for critical references."
