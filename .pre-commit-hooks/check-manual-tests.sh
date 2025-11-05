#!/bin/bash
# Detect manual test scripts incorrectly named with test_ prefix
# Focus on tests with load_dotenv (environment setup) or hardcoded IDs

set -e

EXIT_CODE=0

# Check for obvious manual test patterns
find tests/ -name "test_*.py" -type f 2>/dev/null | while read -r test_file; do
    # Skip archive and tests/manual (correctly placed)
    if echo "$test_file" | grep -qE "/(archive|manual)/"; then
        continue
    fi

    # Check for load_dotenv (strong indicator of manual test)
    if grep -q "load_dotenv" "$test_file" 2>/dev/null; then
        echo "⚠️  Manual test with load_dotenv(): $test_file"
    fi
done

echo "✅ Manual test check complete (informational only)"
exit 0
