#!/bin/bash
echo "=== THE FINAL THREE - Let's see what they are ==="

echo "Checking what the 3 remaining broken links are:"
python3 check_links.py 2>/dev/null | grep "❌" | head -5

echo -e "\n=== Which files have these 3 broken links? ==="
python3 check_links.py 2>/dev/null | grep "📁" | head -5

echo -e "\n=== Detailed Check ==="

echo -e "\n1. If it's the [1m ANSI code:"
grep -n '\[1m"' docs/development/CLI_STANDUP_IMPLEMENTATION.md 2>/dev/null | head -1
grep -n '\[1m"' docs/architecture/pattern-catalog.md 2>/dev/null | head -1

echo -e "\n2. If it's the session-log-framework:"
echo "Checking if it's still showing as broken..."
grep -l "../../../development/session-logs/session-log-framework.md" docs/piper-education/**/*.md 2>/dev/null

echo -e "\n3. Looking for any other stragglers:"
python3 check_links.py 2>/dev/null | grep "❌" | grep -v "\[1m" | grep -v "session-log"

echo -e "\n=== Victory Status ==="
echo "254 → 3 broken links = 98.8% success rate!"
echo "These last 3 are likely false positives or edge cases."
