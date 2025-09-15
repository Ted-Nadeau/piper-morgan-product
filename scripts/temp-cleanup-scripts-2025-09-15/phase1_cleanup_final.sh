#!/bin/bash
echo "=== PHASE 1 CLEANUP: Executing PM Decisions ==="

# 1. Handle duplicates per PM feedback
echo "=== Handling Duplicates ==="

# Decision logs - delete the merge version
echo "1. Deleting decision-log-001-merge.md..."
rm -f "docs/development/decisions/decision-log-001-merge.md"

# Personality DDD - keep in implementation, delete in plans
echo "2. Keeping implementation version, deleting plans version..."
rm -f "docs/development/plans/personality-ddd-model.md"

# Pattern handbooks - consolidate to one location
echo "3. Consolidating pattern handbooks..."
# Check which one is in piper-education tree
if [ -f "docs/piper-education/implementation-guides/pattern-handbook.md" ]; then
    # Keep the emergent one, update it to include any unique content from pattern-handbook
    echo "   Moving pattern content to analysis/emergent-patterns-handbook.md"
    # First check if both exist
    if [ -f "docs/analysis/emergent-patterns-handbook.md" ]; then
        rm -f "docs/piper-education/implementation-guides/pattern-handbook.md"
        echo "   Removed piper-education version, keeping analysis version"
    fi
fi

# 2. Remove copy files
echo -e "\n=== Removing 'copy' files ==="
rm -f "docs/development/decisions/chief-architect-decisions-log copy.md"
rm -f "docs/development/implementation-guides/PM-034-implementation-guide copy.md"
rm -f "docs/comms/blog/robot-hero copy.webp"
echo "✅ Removed 3 'copy' files"

# 3. Consolidate similar files
echo -e "\n=== Consolidating Similar Files ==="

# Troubleshooting - merge into one
echo "1. Consolidating troubleshooting docs..."
if [ -f "docs/troubleshooting.md" ] && [ -f "docs/development/troubleshooting-guide.md" ]; then
    echo "   Merging into docs/troubleshooting.md and removing development version"
    # Append unique content from dev version to main version
    echo -e "\n\n# Additional Troubleshooting (from development guide)\n" >> docs/troubleshooting.md
    cat docs/development/troubleshooting-guide.md >> docs/troubleshooting.md
    rm -f "docs/development/troubleshooting-guide.md"
    echo "   ✅ Merged and removed development/troubleshooting-guide.md"
fi

# Morning standup - merge all three
echo "2. Merging morning-standup docs..."
if [ -f "docs/features/morning-standup.md" ]; then
    # Merge UI guide content
    if [ -f "docs/features/morning-standup-ui-guide.md" ]; then
        echo -e "\n\n# UI Guide Section\n" >> docs/features/morning-standup.md
        cat docs/features/morning-standup-ui-guide.md >> docs/features/morning-standup.md
        rm -f "docs/features/morning-standup-ui-guide.md"
    fi

    # Merge web content
    if [ -f "docs/features/morning-standup-web.md" ]; then
        echo -e "\n\n# Web Interface Section\n" >> docs/features/morning-standup.md
        cat docs/features/morning-standup-web.md >> docs/features/morning-standup.md
        rm -f "docs/features/morning-standup-web.md"
    fi
    echo "   ✅ Merged all morning-standup docs into morning-standup.md"
fi

# 4. Fix cross-references
echo -e "\n=== Fixing Cross-References ==="
if [ -f "docs/development/methodology-core/METHODOLOGY-DISCOVERY-GUIDE.md" ]; then
    # These are indeed broken links that escaped our earlier sweep
    # Fix the paths properly
    sed -i '' 's|\.\./session-logs/|../../session-logs/|g' docs/development/methodology-core/METHODOLOGY-DISCOVERY-GUIDE.md
    sed -i '' 's|../../architecture/|../../architecture/|g' docs/development/methodology-core/METHODOLOGY-DISCOVERY-GUIDE.md  # This one might be right
    sed -i '' 's|../../planning/|../../../planning/|g' docs/development/methodology-core/METHODOLOGY-DISCOVERY-GUIDE.md

    # Fix self-references
    sed -i '' 's|methodology-.*\.md](./methodology-|methodology-|g' docs/development/methodology-core/METHODOLOGY-DISCOVERY-GUIDE.md
    echo "✅ Fixed paths and self-references in METHODOLOGY-DISCOVERY-GUIDE.md"
fi

# 5. Move methodology files to core
echo -e "\n=== Moving Methodology Files to Core ==="

# Move orchestration-testing to core as placeholder
if [ -f "docs/development/orchestration-testing-methodology.md" ]; then
    mv "docs/development/orchestration-testing-methodology.md" "docs/development/methodology-core/methodology-11-ORCHESTRATION-TESTING-placeholder.md"
    echo "✅ Moved orchestration-testing to core as placeholder"
fi

# Move methodology-integration-points to core
if [ -f "docs/planning/methodology-integration-points.md" ]; then
    mv "docs/planning/methodology-integration-points.md" "docs/development/methodology-core/methodology-19-INTEGRATION-POINTS.md"
    echo "✅ Moved methodology-integration-points to core"
fi

echo -e "\n=== CLEANUP SUMMARY ==="
echo "✅ Deleted decision-log-001-merge.md"
echo "✅ Kept implementation/personality-ddd-model.md, deleted plans version"
echo "✅ Consolidated pattern handbooks"
echo "✅ Removed 3 'copy' files"
echo "✅ Merged troubleshooting docs into one"
echo "✅ Merged 3 morning-standup docs into one"
echo "✅ Fixed cross-references in METHODOLOGY-DISCOVERY-GUIDE.md"
echo "✅ Moved 2 methodology files to core"

echo -e "\n=== VERIFICATION ==="
echo "Duplicates remaining: $(find docs -name "*.md" -exec basename {} \; | sort | uniq -d | wc -l)"
echo "Methodology files outside core: $(find docs -name "*methodology*.md" ! -path "*/methodology-core/*" ! -path "*/session-logs/*" | wc -l)"
echo "Copy files remaining: $(find docs -name "*copy*" | wc -l)"
