#!/bin/bash
echo "=== Final Targeted Link Fixes ==="

# 1. Fix script paths that need ../../ instead of ../../../
echo "Fixing script paths in docs/architecture/..."
find docs/architecture -name "*.md" -exec sed -i '' 's|../../scripts/run_tests\.sh|../../../scripts/run_tests.sh|g' {} \;
find docs/architecture -name "*.md" -exec sed -i '' 's|../../scripts/deploy_multi_agent_coordinator\.sh|../../../scripts/deploy_multi_agent_coordinator.sh|g' {} \;
find docs/architecture -name "*.md" -exec sed -i '' 's|../../scripts/validate_multi_agent_operation\.sh|../../../scripts/validate_multi_agent_operation.sh|g' {} \;

# 2. Fix overly deep session-log-framework reference
echo "Fixing session-log-framework path..."
find docs -name "*.md" -exec sed -i '' 's|../../../development/session-logs/session-log-framework\.md|../../development/session-logs/session-log-framework.md|g' {} \;

# 3. Fix CONTRIBUTING.md reference
echo "Fixing CONTRIBUTING.md references..."
find docs -name "*.md" -exec sed -i '' 's|\.\./CONTRIBUTING\.md|../../CONTRIBUTING.md|g' {} \;

# 4. Fix weird formatting issue
echo "Fixing formatting artifact..."
find docs -name "*.md" -exec sed -i '' 's|\[0m".*||g' {} \;

# 5. Fix session logs directory reference
echo "Fixing session logs directory reference..."
find docs -name "*.md" -exec sed -i '' 's|development/session-logs/|../development/session-logs/|g' {} \;

# 6. Fix PIPER.md reference (should be PIPER.user.md)
echo "Fixing PIPER.md to PIPER.user.md..."
find docs -name "*.md" -exec sed -i '' 's|../config/PIPER\.md|../../config/PIPER.user.md|g' {} \;

# 7. Fix service file references (these are Python files, not docs)
echo "Removing Python service file references (not documentation)..."
find docs -name "*.md" -exec sed -i '' 's|\[User Preference Manager\](../services/domain/user_preference_manager.py)|User Preference Manager (see codebase)|g' {} \;
find docs -name "*.md" -exec sed -i '' 's|\[Session Persistence\](../services/orchestration/session_persistence.py)|Session Persistence (see codebase)|g' {} \;
find docs -name "*.md" -exec sed -i '' 's|\[Preference API Endpoints\](../services/api/preference_endpoints.py)|Preference API Endpoints (see codebase)|g' {} \;

# 8. Mark one-pager as coming soon
echo "Marking one-pager as coming soon..."
find docs -name "*.md" -exec sed -i '' 's|\[One-Page Summary\](../one-pager\.md)|One-Page Summary (coming soon)|g' {} \;

# 9. Fix orchestration testing methodology
echo "Fixing orchestration testing reference..."
find docs -name "*.md" -exec sed -i '' 's|orchestration-testing-methodology\.md|../development/orchestration-testing-methodology.md|g' {} \;

# 10. Fix troubleshooting guide reference
echo "Fixing troubleshooting guide..."
find docs -name "*.md" -exec sed -i '' 's|../user-guides/troubleshooting-guide\.md|../troubleshooting.md|g' {} \;

# 11. Fix roadmap reference
echo "Fixing roadmap reference..."
find docs -name "*.md" -exec sed -i '' 's|roadmap\.md|../planning/roadmap.md|g' {} \;

# 12. Remove presentation references (prototype era)
echo "Removing presentation references..."
find docs -name "*.md" -exec sed -i '' 's|\[presentations/team-demo\.html\](./presentations/team-demo\.html)|Team Demo (archived)|g' {} \;
find docs -name "*.md" -exec sed -i '' 's|\[presentations/stakeholder-brief\.html\](./presentations/stakeholder-brief\.html)|Stakeholder Brief (archived)|g' {} \;

# 13. Fix team migration guide
echo "Fixing team migration guide..."
find docs -name "*.md" -exec sed -i '' 's|./team-migration-guide\.md|../development/team-migration-guide.md|g' {} \;

# 14. Remove API design spec reference
echo "Removing api-design-spec references..."
find docs/architecture -name "*.md" -exec sed -i '' 's|See \[api-design-spec\.md\](./api-design-spec\.md) for comprehensive API contracts.*|For API details, see the implemented endpoints in this document.|g' {} \;

echo -e "\n=== Final Check with python3 ==="
python3 check_links.py | grep "Broken links found:"

echo -e "\n=== Remaining Real Issues (if any) ==="
python3 check_links.py 2>/dev/null | grep "❌" | grep -v "session-logs/2025-09-14" | grep -v "DOCUMENTATION_UPDATE_SUMMARY" | grep -v "mailto:" | head -10
