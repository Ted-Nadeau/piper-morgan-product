#!/bin/bash
# update-doc-footers.sh
# Enhanced script that can both add footers and update revision logs

DATE=$(date +"%B %d, %Y")
UPDATE_MESSAGE="${1:-Documentation update}"  # Allow custom revision message

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Documentation Footer Update ===${NC}"
echo -e "Date: $DATE"
echo -e "Update message: $UPDATE_MESSAGE\n"

# Track statistics
added_footers=0
updated_revisions=0
skipped_files=0

# Process all markdown files
find docs/ -name "*.md" -type f | while read file; do
    # Check if file has been modified (git status)
    if git diff --name-only "$file" 2>/dev/null | grep -q "$file" || \
       git diff --cached --name-only "$file" 2>/dev/null | grep -q "$file"; then
        file_modified=true
    else
        file_modified=false
    fi
    
    # Check if footer exists
    if ! grep -q "Last Updated:" "$file"; then
        # Add new footer
        echo "" >> "$file"
        echo "---" >> "$file"
        echo "*Last Updated: $DATE*" >> "$file"
        echo "" >> "$file"
        echo "## Revision Log" >> "$file"
        echo "- **$DATE**: $UPDATE_MESSAGE" >> "$file"
        echo -e "${GREEN}✓ Added footer to: $file${NC}"
        ((added_footers++))
    else
        # Footer exists - check if we should update it
        if [ "$file_modified" = true ]; then
            # Update the Last Updated date
            sed -i.bak "s/\*Last Updated: .*/\*Last Updated: $DATE\*/" "$file"
            
            # Add new revision entry (insert after "## Revision Log" line)
            # This handles both cases: empty log and existing entries
            awk -v date="$DATE" -v msg="$UPDATE_MESSAGE" '
                /^## Revision Log/ { 
                    print $0
                    print "- **" date "**: " msg
                    revision_added=1
                    next
                }
                { print }
            ' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
            
            # Clean up backup
            rm -f "$file.bak"
            
            echo -e "${YELLOW}↻ Updated revision log: $file${NC}"
            ((updated_revisions++))
        else
            echo -e "⊝ No changes in: $file"
            ((skipped_files++))
        fi
    fi
done

# Summary
echo -e "\n${BLUE}=== Summary ===${NC}"
echo -e "${GREEN}Added footers: $added_footers${NC}"
echo -e "${YELLOW}Updated revisions: $updated_revisions${NC}"
echo -e "Skipped (unchanged): $skipped_files"
echo -e "\nTotal files processed: $((added_footers + updated_revisions + skipped_files))"

# Offer to show the changes
echo -e "\n${BLUE}Review changes with:${NC} git diff docs/"
echo -e "${BLUE}Stage changes with:${NC} git add docs/"
