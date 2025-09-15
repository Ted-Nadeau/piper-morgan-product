#!/bin/bash
echo "=== Debugging Why These Links Are Still Broken ==="

echo "1. Script references - let's find the EXACT location:"
echo "Looking for files with ../../scripts/ references..."
grep -l "../../scripts/run_tests.sh" docs/**/*.md 2>/dev/null | while read file; do
    echo "  File: $file"
    # Count how many ../ we need from this file to reach scripts/
    depth=$(echo "$file" | tr '/' '\n' | grep -c .)
    echo "    Depth from root: $depth levels"
    echo "    Current reference: ../../scripts/"
    echo "    Should be: $(printf '../%.0s' $(seq 1 $((depth-1))))scripts/"
done

echo -e "\n2. Session-log-framework - let's verify the file exists:"
ls -la docs/development/session-logs/session-log-framework.md 2>/dev/null || echo "  FILE DOESN'T EXIST!"

echo -e "\n3. CONTRIBUTING.md - where is it still broken?"
grep -n "Contributing.*\.\./CONTRIBUTING" docs/**/*.md 2>/dev/null | head -3

echo -e "\n4. PIPER.user.md still broken - where?"
grep -n "../../config/PIPER.user.md" docs/**/*.md 2>/dev/null | head -3

echo -e "\n5. Orchestration testing - the reference is wrong:"
echo "  File is at: docs/development/orchestration-testing-methodology.md"
echo "  Referenced from: docs/development/testing/README.md"
echo "  Current reference: ../development/orchestration-testing-methodology.md"
echo "  Should be: ../../development/orchestration-testing-methodology.md (up 2, then down 1)"

echo -e "\n6. New broken links appeared! Let's find them:"
echo "  MCP Connection Pool:"
find . -name "*mcp-connection-pool*" -type f 2>/dev/null
echo "  Shared Types:"
find . -name "*shared-types*" -type f 2>/dev/null | grep docs
echo "  API Design Spec:"
grep -n "api-design-spec.md#error-handling" docs/**/*.md 2>/dev/null

echo -e "\n=== Let's see WHICH files have broken links ==="
python3 check_links.py 2>/dev/null | grep "📁" | grep -v "session-logs/2025-09-14" | grep -v "DOCUMENTATION_UPDATE"
