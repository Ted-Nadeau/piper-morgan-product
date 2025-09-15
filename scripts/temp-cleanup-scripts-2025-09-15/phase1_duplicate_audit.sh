#!/bin/bash
echo "=== PHASE 1: Doc Cleanup - Duplicate File Consolidation ==="
echo "Finding potential duplicate files based on similar names and content..."
echo ""

# Find files with similar names
echo "=== SIMILAR FILENAMES ==="
echo "Files that might be duplicates based on naming patterns:"
echo ""

# Look for common duplicate patterns
find docs -name "*.md" -type f ! -path "*/archive/*" ! -path "*/session-logs/*" | while read file; do
    basename=$(basename "$file")
    dirname=$(dirname "$file")

    # Check for common duplicate patterns
    # - files with .old, .backup, .bak, .copy extensions
    # - files with dates in names
    # - files with v1, v2, etc.

    # Find similar files in same directory
    similar=$(find "$dirname" -name "${basename%.*}*" -type f | grep -v "^$file$" | head -5)
    if [ ! -z "$similar" ]; then
        echo "Potential duplicates of: $file"
        echo "$similar" | while read sim; do
            echo "  → $sim"
        done
        echo ""
    fi
done

echo "=== FILES WITH DUPLICATE MARKERS ==="
find docs -name "*.backup" -o -name "*.old" -o -name "*.bak" -o -name "*copy*" -o -name "*_v[0-9]*" | sort

echo ""
echo "=== CONTENT-BASED DUPLICATE DETECTION ==="
echo "Checking for files with very similar content (>90% similarity in first 50 lines)..."
echo ""

# Create temporary directory for hashes
TEMP_DIR=$(mktemp -d)

# Generate content hashes for first 50 lines of each file
find docs -name "*.md" -type f ! -path "*/archive/*" ! -path "*/session-logs/*" | while read file; do
    # Get first 50 lines, remove whitespace variations
    head -50 "$file" | tr -d ' \t' | md5 > "$TEMP_DIR/$(echo $file | md5).hash"
    echo "$file" > "$TEMP_DIR/$(echo $file | md5).path"
done

# Find files with identical hashes
echo "Files with nearly identical content (first 50 lines):"
find "$TEMP_DIR" -name "*.hash" -exec cat {} \; | sort | uniq -d | while read hash; do
    echo "Duplicate content hash: $hash"
    grep -l "$hash" "$TEMP_DIR"/*.hash | while read hashfile; do
        pathfile="${hashfile%.hash}.path"
        cat "$pathfile"
    done
    echo ""
done

# Cleanup
rm -rf "$TEMP_DIR"

echo "=== SUMMARY ==="
echo "Files with version markers: $(find docs -name "*_v[0-9]*" -o -name "*-v[0-9]*" | wc -l)"
echo "Backup files found: $(find docs -name "*.backup" -o -name "*.old" -o -name "*.bak" | wc -l)"
echo "Files with 'copy' in name: $(find docs -name "*copy*" | wc -l)"
