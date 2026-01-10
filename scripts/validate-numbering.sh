#!/bin/bash
# Validate that new patterns and ADRs have proper consecutive numbering
# Used as pre-commit hook to catch numbering errors

set -e

EXIT_CODE=0

# Check patterns
PATTERNS_DIR="docs/internal/architecture/current/patterns"
if git diff --cached --name-only --diff-filter=A | grep -q "^$PATTERNS_DIR/pattern-.*\.md$"; then
    echo "🔍 Checking new pattern numbering..."

    # Get highest existing pattern number
    HIGHEST_PATTERN=$(find "$PATTERNS_DIR" -name "pattern-[0-9][0-9][0-9]-*.md" \
        | sed 's/.*pattern-\([0-9][0-9][0-9]\)-.*/\1/' \
        | sort -n \
        | tail -1)

    # Strip leading zeros for arithmetic (bash treats 08/09 as invalid octal)
    HIGHEST_PATTERN=$((10#$HIGHEST_PATTERN))

    # Check each new pattern file
    git diff --cached --name-only --diff-filter=A | grep "^$PATTERNS_DIR/pattern-.*\.md$" | while read -r file; do
        # Extract number from filename
        PATTERN_NUM=$(echo "$file" | sed 's/.*pattern-\([0-9][0-9][0-9]\)-.*/\1/')

        # Check if properly formatted
        if ! echo "$file" | grep -qE "pattern-[0-9]{3}-.*\.md$"; then
            echo "❌ Error: Pattern file has invalid format: $file"
            echo "   Expected format: pattern-NNN-name.md (where NNN is 3 digits)"
            EXIT_CODE=1
            continue
        fi

        # Check if it's the next consecutive number
        EXPECTED=$((HIGHEST_PATTERN + 1))
        EXPECTED_PADDED=$(printf "%03d" "$EXPECTED")

        if [ "$PATTERN_NUM" != "$EXPECTED_PADDED" ]; then
            echo "❌ Error: Pattern number should be $EXPECTED_PADDED, found $PATTERN_NUM"
            echo "   File: $file"
            echo "   Tip: Use ./scripts/new-pattern.sh to auto-number patterns"
            EXIT_CODE=1
        else
            echo "✅ Pattern $PATTERN_NUM is correctly numbered"
        fi
    done
fi

# Check ADRs
ADRS_DIR="docs/internal/architecture/current/adrs"
if git diff --cached --name-only --diff-filter=A | grep -q "^$ADRS_DIR/adr-.*\.md$"; then
    echo "🔍 Checking new ADR numbering..."

    # Get highest existing ADR number (use 10# prefix to force decimal interpretation)
    HIGHEST_ADR=$(find "$ADRS_DIR" -name "adr-[0-9][0-9][0-9]-*.md" \
        | sed 's/.*adr-\([0-9][0-9][0-9]\)-.*/\1/' \
        | sort -n \
        | tail -1)
    # Strip leading zeros for arithmetic (bash treats 08/09 as invalid octal)
    HIGHEST_ADR=$((10#$HIGHEST_ADR))

    # Check each new ADR file
    git diff --cached --name-only --diff-filter=A | grep "^$ADRS_DIR/adr-.*\.md$" | while read -r file; do
        # Extract number from filename
        ADR_NUM=$(echo "$file" | sed 's/.*adr-\([0-9][0-9][0-9]\)-.*/\1/')

        # Check if properly formatted
        if ! echo "$file" | grep -qE "adr-[0-9]{3}-.*\.md$"; then
            echo "❌ Error: ADR file has invalid format: $file"
            echo "   Expected format: adr-NNN-title.md (where NNN is 3 digits)"
            EXIT_CODE=1
            continue
        fi

        # Check if it's the next consecutive number
        EXPECTED=$((HIGHEST_ADR + 1))
        EXPECTED_PADDED=$(printf "%03d" "$EXPECTED")

        if [ "$ADR_NUM" != "$EXPECTED_PADDED" ]; then
            echo "❌ Error: ADR number should be $EXPECTED_PADDED, found $ADR_NUM"
            echo "   File: $file"
            echo "   Tip: Use ./scripts/new-adr.sh to auto-number ADRs"
            EXIT_CODE=1
        else
            echo "✅ ADR $ADR_NUM is correctly numbered"
        fi
    done
fi

exit $EXIT_CODE
