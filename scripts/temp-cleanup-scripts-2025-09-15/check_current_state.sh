#!/bin/bash
cd ~/Development/piper-morgan

echo "=== Using python3 explicitly ==="
python3 check_links.py | grep "Broken links found:"

echo -e "\n=== Real Remaining Issues (excluding artifacts) ==="
python3 check_links.py 2>/dev/null | grep "❌" | grep -v "session-logs/2025-09-14" | grep -v "DOCUMENTATION_UPDATE_SUMMARY" | head -20

echo -e "\n=== Check if directories were created ==="
ls -la docs/piper-education/decision-patterns/established/ 2>/dev/null || echo "Directory not created yet"
ls -la docs/piper-education/methodologies/established/ 2>/dev/null || echo "Directory not created yet"

echo -e "\n=== Look for api-design-spec references to remove ==="
grep -r "api-design-spec" docs/ --include="*.md" 2>/dev/null | wc -l
echo "API design spec references found (if any):"
grep -r "api-design-spec" docs/ --include="*.md" 2>/dev/null | head -3
