#!/bin/bash
echo "=== PHASE 1: Doc Cleanup - Stale Content Audit ==="
echo "Finding all markdown files older than 30 days..."
echo ""

# Set the date 30 days ago
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    CUTOFF_DATE=$(date -v-30d '+%Y-%m-%d')
else
    # Linux
    CUTOFF_DATE=$(date -d '30 days ago' '+%Y-%m-%d')
fi

echo "Cutoff date: $CUTOFF_DATE"
echo "Files not modified since this date may need updating:"
echo ""

# Find stale docs (excluding session logs and archives)
echo "=== STALE DOCUMENTATION (>30 days old) ==="
find docs -name "*.md" -type f ! -path "*/session-logs/*" ! -path "*/archive/*" ! -path "*/prompts/*" -mtime +30 | while read file; do
    # Get last modified date
    if [[ "$OSTYPE" == "darwin"* ]]; then
        MOD_DATE=$(stat -f "%Sm" -t "%Y-%m-%d" "$file")
    else
        MOD_DATE=$(stat -c "%y" "$file" | cut -d' ' -f1)
    fi

    # Get line count for context
    LINES=$(wc -l < "$file")

    echo "  $MOD_DATE | $LINES lines | $file"
done | sort

echo ""
echo "=== POTENTIALLY OBSOLETE (>60 days) ==="
find docs -name "*.md" -type f ! -path "*/session-logs/*" ! -path "*/archive/*" ! -path "*/prompts/*" -mtime +60 | while read file; do
    if [[ "$OSTYPE" == "darwin"* ]]; then
        MOD_DATE=$(stat -f "%Sm" -t "%Y-%m-%d" "$file")
    else
        MOD_DATE=$(stat -c "%y" "$file" | cut -d' ' -f1)
    fi
    echo "  $MOD_DATE | $file"
done | sort

echo ""
echo "=== SUMMARY ==="
echo "Stale docs (30+ days): $(find docs -name "*.md" -type f ! -path "*/session-logs/*" ! -path "*/archive/*" ! -path "*/prompts/*" -mtime +30 | wc -l)"
echo "Very stale (60+ days): $(find docs -name "*.md" -type f ! -path "*/session-logs/*" ! -path "*/archive/*" ! -path "*/prompts/*" -mtime +60 | wc -l)"
echo "Total docs checked: $(find docs -name "*.md" -type f ! -path "*/session-logs/*" ! -path "*/archive/*" ! -path "*/prompts/*" | wc -l)"
