#!/bin/bash
echo "=== FINAL BOSS REVEALED: The Real Broken Links ==="

echo "Wait - the session-log path WORKS! So what's actually broken?"
echo ""
echo "Let's check EACH file that supposedly has broken links:"

echo -e "\n1. Checking docs/piper-education/frameworks/README.md:"
python3 check_links.py 2>/dev/null | grep -A1 "piper-education/frameworks/README.md"

echo -e "\n2. Checking docs/development/CLI_STANDUP_IMPLEMENTATION.md:"
python3 check_links.py 2>/dev/null | grep -A1 "CLI_STANDUP_IMPLEMENTATION.md"

echo -e "\n3. Checking docs/architecture/architecture.md:"
python3 check_links.py 2>/dev/null | grep -A1 "architecture/architecture.md"

echo -e "\n4. Checking docs/architecture/domain-models.md:"
python3 check_links.py 2>/dev/null | grep -A1 "domain-models.md"

echo -e "\n5. Checking docs/architecture/api-reference.md:"
python3 check_links.py 2>/dev/null | grep -A2 "api-reference.md"

echo -e "\n6. Checking ADR-024:"
python3 check_links.py 2>/dev/null | grep -A1 "adr-024"

echo -e "\n7. Checking ADR-023 (should have 3 script links):"
python3 check_links.py 2>/dev/null | grep -A3 "adr-023"

echo -e "\n8. Checking ADR-026:"
python3 check_links.py 2>/dev/null | grep -A2 "adr-026"

echo -e "\n=== ACTUAL BROKEN LINKS (not in session logs) ==="
python3 check_links.py 2>/dev/null | grep "❌" | grep -v "session-logs/2025-09" | grep -v "DOCUMENTATION_UPDATE"
