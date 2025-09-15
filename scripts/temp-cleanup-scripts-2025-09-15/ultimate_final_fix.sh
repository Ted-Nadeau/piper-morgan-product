#!/bin/bash
echo "=== ULTIMATE FINAL FIX - 13 Remaining Links ==="
echo "Run this when you return to achieve 100% victory!"

# 1. Fix ADR paths missing ../../ prefix
echo "1. Fixing ADR paths that are missing ../../ prefix..."
sed -i '' 's|\[Persistent Context Research\](development/PERSISTENT_CONTEXT_RESEARCH\.md)|[Persistent Context Research](../../development/PERSISTENT_CONTEXT_RESEARCH.md)|g' docs/architecture/adr/adr-024-persistent-context-architecture.md
sed -i '' 's|\[Test Infrastructure Guide\](development/TEST-GUIDE\.md)|[Test Infrastructure Guide](../../development/TEST-GUIDE.md)|g' docs/architecture/adr/adr-023-test-infrastructure-activation.md
sed -i '' 's|\[Excellence Flywheel Methodology\](development/methodology-core/methodology-00-EXCELLENCE-FLYWHEEL\.md)|[Excellence Flywheel Methodology](../../development/methodology-core/methodology-00-EXCELLENCE-FLYWHEEL.md)|g' docs/architecture/adr/adr-023-test-infrastructure-activation.md
sed -i '' 's|\[ADR-017: Spatial MCP Integration\](architecture/adr/adr-017-spatial-mcp\.md)|[ADR-017: Spatial MCP Integration](./adr-017-spatial-mcp.md)|g' docs/architecture/adr/adr-026-notion-client-migration.md

# 2. Fix MCP case study path from architecture.md
echo "2. Fixing MCP case study path..."
sed -i '' 's|\.\./case-studies/mcp-connection-pool-642x\.md|../piper-education/case-studies/mcp-connection-pool-642x.md|g' docs/architecture/architecture.md

# 3. Remove or fix non-existent references
echo "3. Removing non-existent file references..."
sed -i '' 's|\[Shared Types\](\.\./architecture/shared-types\.md)|Shared Types (see services/shared_types.py)|g' docs/architecture/domain-models.md
sed -i '' 's|\[api-design-spec\.md\](./api-design-spec\.md)|API specifications in this document|g' docs/architecture/api-reference.md
sed -i '' 's|\[Notion Integration Feature Documentation\](features/notion-integration\.md)|Notion Integration (coming soon)|g' docs/architecture/adr/adr-026-notion-client-migration.md

# 4. Fix the ultra-deep script reference (5 levels!)
echo "4. Finding and fixing ultra-deep script reference..."
grep -n "../../../../../scripts/run_tests.sh" docs/**/**/*.md 2>/dev/null | while read line; do
    file=$(echo "$line" | cut -d: -f1)
    echo "   Fixing in: $file"
    sed -i '' 's|../../../../../scripts/run_tests\.sh|../../../scripts/run_tests.sh|g' "$file"
done

# 5. Fix session-log-framework path (the path works but link checker is confused)
echo "5. Session-log-framework - path works, might be link checker bug"
# The path ../../../development/session-logs/session-log-framework.md from
# docs/piper-education/frameworks/README.md actually works!
# This might be a false positive

# 6. Fix PIPER.md vs PIPER.user.md confusion
echo "6. Finding PIPER.md references that should be PIPER.user.md..."
grep -l "PIPER.md Configuration" docs/**/*.md 2>/dev/null | while read file; do
    echo "   Fixing in: $file"
    sed -i '' 's|PIPER\.md Configuration|PIPER.user.md Configuration|g' "$file"
done

# 7. Mark dev-guide.md as coming soon
echo "7. Marking dev-guide as coming soon..."
find docs -name "*.md" -exec sed -i '' 's|\[dev-guide\.md\]([^)]*dev-guide\.md)|Developer Guide (coming soon)|g' {} \;

echo -e "\n=== FINAL VERIFICATION ==="
python3 check_links.py | grep "Broken links found:"

echo -e "\n=== What Should Be Left ==="
echo "1. [1m ANSI code - FALSE POSITIVE from code block"
echo "2. Maybe 1-2 edge cases"
echo ""
echo "If we're down to <5, we've achieved 98%+ success!"
echo "From 254 → <5 broken links!"
