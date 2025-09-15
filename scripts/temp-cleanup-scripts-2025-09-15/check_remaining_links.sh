#!/bin/bash
cd ~/Development/piper-morgan
echo "=== Current Broken Links Count ==="
python check_links.py | grep "Broken links found:"

echo -e "\n=== Remaining Broken Links (excluding session logs) ==="
python check_links.py 2>/dev/null | grep "❌" | grep -v "session-logs/2025-09-14" | grep -v "DOCUMENTATION_UPDATE_SUMMARY"

echo -e "\n=== Categories of Remaining Issues ==="
echo "Script paths:"
python check_links.py 2>/dev/null | grep "❌" | grep -v "session-logs" | grep -v "DOCUMENTATION_UPDATE" | grep "scripts/"

echo -e "\nConfig paths:"
python check_links.py 2>/dev/null | grep "❌" | grep -v "session-logs" | grep -v "DOCUMENTATION_UPDATE" | grep "config/"

echo -e "\nDevelopment paths:"
python check_links.py 2>/dev/null | grep "❌" | grep -v "session-logs" | grep -v "DOCUMENTATION_UPDATE" | grep "development/"

echo -e "\nOther paths:"
python check_links.py 2>/dev/null | grep "❌" | grep -v "session-logs" | grep -v "DOCUMENTATION_UPDATE" | grep -v "scripts/" | grep -v "config/" | grep -v "development/"
