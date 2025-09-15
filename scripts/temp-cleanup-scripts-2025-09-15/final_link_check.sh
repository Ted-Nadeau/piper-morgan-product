#!/bin/bash
# Check what broken links remain after script and config fixes

cd ~/Development/piper-morgan

echo "=== Final Broken Links Check ==="
python check_links.py | grep "Broken links found:"

echo -e "\n=== Remaining Real Broken Links ==="
echo "(Excluding session logs and documentation summaries)"
python check_links.py 2>/dev/null | grep "❌" | grep -v "session-logs/2025-09-14" | grep -v "DOCUMENTATION_UPDATE_SUMMARY" | head -20

echo -e "\n=== Summary by File ==="
python check_links.py 2>/dev/null | grep "📁" | grep -v "session-logs/2025-09-14" | grep -v "DOCUMENTATION_UPDATE_SUMMARY" | head -10
