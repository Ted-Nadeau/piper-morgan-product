#!/bin/bash
echo "=== Final Documentation Link Cleanup ==="

# 1. Fix deployment references (Category E)
echo "Fixing deployment guide references..."
find docs -name "*.md" -exec sed -i '' 's|\.\.\/operations\/deployment\.md|deployment/deployment-summary.md|g' {} \;
find docs -name "*.md" -exec sed -i '' 's|deployment\.md|deployment/deployment-summary.md|g' {} \;

# 2. Remove abandoned aspirational links (Category G)
echo "Removing abandoned aspirational links..."
# API design spec - remove link but keep text
find docs -name "*.md" -exec sed -i '' 's|\[API Design Spec\]([^)]*api-design-spec\.md)|API Design Spec|g' {} \;

# Advanced conversation features - remove link
find docs -name "*.md" -exec sed -i '' 's|\[Advanced Conversation Features\]([^)]*advanced-conversation[^)]*)|Advanced Conversation Features|g' {} \;

# 3. Mark "coming soon" for relevant aspirational links
echo "Marking future documentation as coming soon..."
# Dev guide - add coming soon
find docs -name "*.md" -exec sed -i '' 's|\[Developer Guide\]([^)]*dev-guide\.md)|Developer Guide (coming soon)|g' {} \;
find docs -name "*.md" -exec sed -i '' 's|\[Dev Guide\]([^)]*dev-guide\.md)|Dev Guide (coming soon)|g' {} \;

# One-pager - add coming soon
find docs -name "*.md" -exec sed -i '' 's|\[One Pager\]([^)]*one-pager\.md)|One Pager (coming soon)|g' {} \;
find docs -name "*.md" -exec sed -i '' 's|\[One-Pager\]([^)]*one-pager\.md)|One-Pager (coming soon)|g' {} \;

# 4. Fix root file references
echo "Fixing root file references..."
find docs -name "*.md" -exec sed -i '' 's|\(^\|[^./]\)CONTRIBUTING\.md|../CONTRIBUTING.md|g' {} \;
find docs -name "*.md" -exec sed -i '' 's|\(^\|[^./]\)LICENSE|../LICENSE|g' {} \;

# 5. Create missing directories (Category F)
echo "Creating missing directories..."
mkdir -p docs/piper-education/decision-patterns/established/
mkdir -p docs/piper-education/methodologies/established/

# Add README placeholders
echo "# Established Decision Patterns

Documented patterns that have proven successful across multiple projects." > docs/piper-education/decision-patterns/established/README.md

echo "# Established Methodologies

Tested and proven methodologies with documented track records." > docs/piper-education/methodologies/established/README.md

echo "=== Final Check ==="
python check_links.py | grep "Broken links found:"

echo -e "\n=== Remaining Issues (if any) ==="
python check_links.py 2>/dev/null | grep "❌" | grep -v "session-logs/2025-09-14" | grep -v "DOCUMENTATION_UPDATE_SUMMARY" | head -10
