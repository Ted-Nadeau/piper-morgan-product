#!/bin/bash
echo "=== PHASE 1 CLEANUP: Quick Wins ==="

# 1. Remove "copy" files
echo "Removing 'copy' files..."
rm -f "docs/development/decisions/chief-architect-decisions-log copy.md"
rm -f "docs/development/implementation-guides/PM-034-implementation-guide copy.md"
rm -f "docs/comms/blog/robot-hero copy.webp"
echo "✅ Removed 3 'copy' files"

# 2. Consolidate identical duplicates
echo -e "\nConsolidating duplicates..."

# Decision logs - keep the original
if [ -f "docs/development/decisions/decision-log-001-merge.md" ]; then
    echo "Removing decision-log-001-merge.md (duplicate of decision-log-001.md)"
    rm -f "docs/development/decisions/decision-log-001-merge.md"
fi

# Personality DDD model - keep in development/plans
if [ -f "docs/implementation/personality-ddd-model.md" ] && [ -f "docs/development/plans/personality-ddd-model.md" ]; then
    echo "Removing docs/implementation/personality-ddd-model.md (keeping development/plans version)"
    rm -f "docs/implementation/personality-ddd-model.md"
fi

# Pattern handbook - keep the one with better name
if [ -f "docs/piper-education/implementation-guides/pattern-handbook.md" ] && [ -f "docs/analysis/emergent-patterns-handbook.md" ]; then
    echo "Keeping emergent-patterns-handbook.md, removing pattern-handbook.md"
    rm -f "docs/piper-education/implementation-guides/pattern-handbook.md"
fi

echo "✅ Consolidated 3 duplicate files"

# 3. Fix methodology cross-references
echo -e "\nFixing methodology cross-references..."
if [ -f "docs/development/methodology-core/METHODOLOGY-DISCOVERY-GUIDE.md" ]; then
    # Fix the broken paths
    sed -i '' 's|\.\./session-logs/|../session-logs/|g' docs/development/methodology-core/METHODOLOGY-DISCOVERY-GUIDE.md
    sed -i '' 's|../../architecture/|../architecture/|g' docs/development/methodology-core/METHODOLOGY-DISCOVERY-GUIDE.md
    sed -i '' 's|../../planning/|../../planning/|g' docs/development/methodology-core/METHODOLOGY-DISCOVERY-GUIDE.md
    echo "✅ Fixed paths in METHODOLOGY-DISCOVERY-GUIDE.md"
fi

echo -e "\n=== SUMMARY ==="
echo "✅ Removed 3 'copy' files"
echo "✅ Consolidated 3 duplicate files"
echo "✅ Fixed methodology cross-references"
echo ""
echo "=== MANUAL REVIEW NEEDED ==="
echo "1. Consolidate troubleshooting docs (troubleshooting.md vs troubleshooting-guide.md)"
echo "2. Merge morning-standup docs (3 versions)"
echo "3. Review methodology files outside core:"
echo "   - orchestration-testing-methodology.md (placeholder)"
echo "   - methodology-integration-points.md (might belong in core?)"
