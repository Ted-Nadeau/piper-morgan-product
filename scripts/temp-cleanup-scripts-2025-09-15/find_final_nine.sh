#!/bin/bash
echo "=== Final 9 Stubborn Links - Let's Find and Fix Them ==="

# 1. Find where the script references are that are still broken
echo "1. Finding broken script references..."
grep -r "../../scripts/run_tests.sh" docs/ --include="*.md" | head -2
grep -r "../../scripts/deploy_multi_agent" docs/ --include="*.md" | head -2

# 2. Find the Contributing Guide reference that's still broken
echo -e "\n2. Finding broken CONTRIBUTING reference..."
grep -r "../../CONTRIBUTING.md" docs/ --include="*.md" | grep -v "session-logs/2025-09" | head -2

# 3. Find the weird development/session-logs/ reference
echo -e "\n3. Finding development/session-logs/ directory reference..."
grep -r "\[development/session-logs/\]" docs/ --include="*.md" | head -2
grep -r "../../development/session-logs/" docs/ --include="*.md" | grep -v ".md" | head -2

# 4. Find the ultra-deep session-log-framework reference
echo -e "\n4. Finding ../../../development/session-logs/session-log-framework.md..."
grep -r "../../../development/session-logs/session-log-framework.md" docs/ --include="*.md" | head -2

# 5. The [1m formatting issue - let's see where it is
echo -e "\n5. Finding [1m formatting artifact..."
grep -r '\[1m"' docs/ --include="*.md" | head -2

# 6. Find PIPER.user.md reference that's broken
echo -e "\n6. Finding broken PIPER.user.md reference..."
grep -r "../../config/PIPER.user.md" docs/ --include="*.md" | head -2

# 7. Find orchestration testing reference
echo -e "\n7. Finding orchestration testing reference..."
grep -r "Orchestration Testing Methodology" docs/ --include="*.md" | grep "../development" | head -2

# 8. Find team migration guide reference
echo -e "\n8. Finding team migration guide..."
grep -r "Team Migration Guide" docs/ --include="*.md" | head -2
find . -name "*team-migration*" -type f 2>/dev/null | head -2

echo -e "\n=== Let me check the actual files to understand the depth ==="
echo "Files with these issues:"
python3 check_links.py 2>/dev/null | grep "📁" | grep -v "session-logs/2025-09-14" | grep -v "DOCUMENTATION_UPDATE" | head -5
