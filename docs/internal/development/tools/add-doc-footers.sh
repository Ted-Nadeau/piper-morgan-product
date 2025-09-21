#!/bin/bash
# add-doc-footers.sh

DATE=$(date +"%B %d, %Y")

find docs/ -name "*.md" -type f | while read file; do
    # Check if footer already exists
    if ! grep -q "Last Updated:" "$file"; then
        echo "" >> "$file"
        echo "---" >> "$file"
        echo "*Last Updated: $DATE*" >> "$file"
        echo "" >> "$file"
        echo "## Revision Log" >> "$file"
        echo "- **$DATE**: Added systematic documentation dating and revision tracking" >> "$file"
        echo "Added footer to: $file"
    else
        echo "Footer exists in: $file"
    fi
done
