#!/bin/bash
echo "=== FIXING LARGE IMAGE FILE ISSUE ==="

echo "Current situation:"
echo "- 20 robot-*.png files (2-3MB each)"
echo "- Blocking commits every time"
echo "- Used for blog posts"
echo ""

echo "=== OPTION 1: Add to .gitignore (Recommended) ==="
echo "Move images to cloud storage and ignore locally:"
echo ""
echo "# Add to .gitignore:"
echo "docs/comms/blog/*.png"
echo "docs/comms/blog/*.jpg"
echo "docs/comms/blog/*.jpeg"
echo ""

echo "=== OPTION 2: Compress images ==="
echo "Reduce file sizes to under 500KB:"
find docs/comms/blog -name "*.png" -size +500k | while read file; do
    size=$(du -h "$file" | cut -f1)
    echo "  $file ($size) - needs compression"
done

echo ""
echo "=== OPTION 3: Use Git LFS ==="
echo "Track large files with Git Large File Storage:"
echo "  git lfs track '*.png'"
echo "  git lfs track '*.jpg'"
echo ""

echo "=== OPTION 4: Move to separate repo ==="
echo "Create piper-morgan-assets repo for media files"
echo ""

echo "=== QUICK FIX FOR NOW ==="
echo "1. Remove from staging:"
echo "   git reset HEAD docs/comms/blog/*.png"
echo ""
echo "2. Add to .gitignore:"
echo "   echo 'docs/comms/blog/*.png' >> .gitignore"
echo "   echo 'docs/comms/blog/*.jpg' >> .gitignore"
echo ""
echo "3. Commit .gitignore change:"
echo "   git add .gitignore"
echo "   git commit -m 'Exclude large blog images from git'"
echo ""
echo "4. Then commit your other changes:"
echo "   git commit -am 'Mixed updates: configs, DB migration, analysis work, doc recovery'"
