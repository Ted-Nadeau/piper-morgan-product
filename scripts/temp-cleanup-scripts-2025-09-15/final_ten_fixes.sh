#!/bin/bash
echo "=== Final 10 Broken Links - Precision Fixes ==="

# 1. Fix CONTRIBUTING.md in troubleshooting.md (needs just ../ not ../../)
echo "Fix 1: CONTRIBUTING in troubleshooting.md..."
sed -i '' 's|../../CONTRIBUTING\.md|../CONTRIBUTING.md|g' docs/troubleshooting.md

# 2. Fix script paths in DATABASE_INTEGRATION_GUIDE.md (extra ./ in front)
echo "Fix 2: Script path in DATABASE_INTEGRATION_GUIDE..."
sed -i '' 's|\./../../scripts/|../../scripts/|g' docs/development/DATABASE_INTEGRATION_GUIDE.md

# 3. Fix session-log-framework paths from piper-education (needs to go up one more level)
echo "Fix 3: Session-log-framework from piper-education..."
sed -i '' 's|../../../development/session-logs/session-log-framework\.md|../../../../docs/development/session-logs/session-log-framework.md|g' docs/piper-education/decision-patterns/emergent/verification-first-pattern.md
sed -i '' 's|../../../development/session-logs/session-log-framework\.md|../../../../docs/development/session-logs/session-log-framework.md|g' docs/piper-education/methodologies/emergent/human-ai-collaboration-referee.md

# Actually, let's try the correct relative path
sed -i '' 's|../../../../docs/development/session-logs/session-log-framework\.md|../../../development/session-logs/session-log-framework.md|g' docs/piper-education/decision-patterns/emergent/verification-first-pattern.md
sed -i '' 's|../../../../docs/development/session-logs/session-log-framework\.md|../../../development/session-logs/session-log-framework.md|g' docs/piper-education/methodologies/emergent/human-ai-collaboration-referee.md

# Actually that's still wrong. Let me think about the path:
# From: docs/piper-education/decision-patterns/emergent/
# To: docs/development/session-logs/
# Path: ../../../development/session-logs/ (up 3, then down into development)
# That should be correct. Let's check if the file exists:
echo "Checking if session-log-framework.md exists..."
ls -la docs/development/session-logs/session-log-framework.md 2>/dev/null || echo "File doesn't exist at expected location"

# 4. The formatting artifacts are NOT broken links - they're color codes in code blocks
echo "Fix 4: Formatting artifacts are in code blocks, not links - skipping..."

# 5. Fix orchestration-testing-methodology (need to find where it actually is)
echo "Fix 5: Looking for orchestration-testing file..."
find . -name "*orchestration*testing*" -type f 2>/dev/null | grep -v node_modules | head -5

# 6. Fix PIPER.md vs PIPER.user.md confusion
echo "Fix 6: Checking which PIPER references are wrong..."
grep -r "PIPER\.md" docs/ --include="*.md" | grep -v "PIPER\.user" | grep -v "PIPER\.defaults" | grep "config" | head -3

# Let's leave PIPER references as-is since both files exist

echo -e "\n=== Checking What Actually Needs Fixing ==="

# The REAL remaining broken links
echo "Actual broken links that need fixing:"
python3 check_links.py 2>/dev/null | grep "❌" | grep -v "session-logs/2025-09" | grep -v "DOCUMENTATION_UPDATE" | grep -v "\[1m" | grep -v "\[0m"

echo -e "\n=== Final Count ==="
python3 check_links.py | grep "Broken links found:"
