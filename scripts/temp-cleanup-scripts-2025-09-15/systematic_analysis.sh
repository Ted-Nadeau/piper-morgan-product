#!/bin/bash
echo "=== SYSTEMATIC ANALYSIS OF REMAINING 19 BROKEN LINKS ==="

echo -e "\n1. BACKUP FILES TO REMOVE (not real broken links):"
echo "Removing .bak and .bak2 files..."
find docs -name "*.bak" -o -name "*.bak2" | while read file; do
    echo "  Removing: $file"
    rm "$file"
done

echo -e "\n2. BACKUP DIRECTORY TO REMOVE:"
if [ -d "docs_backup_20250915_090423" ]; then
    echo "Removing backup directory: docs_backup_20250915_090423/"
    rm -rf docs_backup_20250915_090423/
fi

echo -e "\n=== After cleanup, checking again ==="
python3 check_links.py | grep "Broken links found:"

echo -e "\n3. ANALYZING EACH REMAINING BROKEN LINK SYSTEMATICALLY:"

echo -e "\n--- ADR-023 Script References (3 links) ---"
echo "File: docs/architecture/adr/adr-023-test-infrastructure-activation.md"
echo "Current references: ../../scripts/"
echo "From docs/architecture/adr/ to scripts/ needs: ../../../scripts/"
echo "FIX NEEDED: Add one more ../"

echo -e "\n--- API Design Spec Reference ---"
echo "File: docs/architecture/api-reference.md"
echo "Reference: ./api-design-spec.md#error-handling"
echo "File was deleted, reference should be removed or updated"
echo "FIX NEEDED: Remove reference or point to actual API docs"

echo -e "\n--- Orchestration Testing ---"
echo "File: docs/development/testing/README.md"
echo "Reference: ../development/orchestration-testing-methodology.md"
echo "Should be: ../orchestration-testing-methodology.md (same directory level)"
echo "FIX NEEDED: Remove extra 'development/'"

echo -e "\n--- MCP Case Study ---"
echo "Referenced from: docs/architecture/adr/adr-026-notion-client-migration.md"
grep -n "mcp-connection-pool" docs/architecture/adr/adr-026-notion-client-migration.md
echo "Target exists at: docs/piper-education/case-studies/mcp-connection-pool-642x.md"
echo "FIX NEEDED: Correct the path"

echo -e "\n--- Shared Types ---"
echo "Referenced from: docs/architecture/adr/adr-026-notion-client-migration.md"
grep -n "shared-types" docs/architecture/adr/adr-026-notion-client-migration.md
echo "FIX NEEDED: Determine if this should point to services/shared_types.py or remove"

echo -e "\n--- Session Log Framework Deep Path ---"
echo "Still broken in: docs/piper-education/(decision-patterns|methodologies)/emergent/"
echo "FIX NEEDED: Complex path calculation"

echo -e "\n=== SYSTEMATIC FIX PLAN ==="
echo "1. Remove backup files (.bak, .bak2) - DONE ABOVE"
echo "2. Remove backup directory - DONE ABOVE"
echo "3. Fix ADR-023 script paths (3 links)"
echo "4. Fix/remove api-design-spec reference (1 link)"
echo "5. Fix orchestration testing path (1 link)"
echo "6. Fix ADR-026 references (2 links)"
echo "7. Fix session-log-framework paths (2 links)"
echo "8. Fix remaining CONTRIBUTING/PIPER references"
