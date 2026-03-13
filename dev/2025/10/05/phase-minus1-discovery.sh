#!/bin/bash
# GREAT-4C Phase -1: Handler Discovery
# Run this manually and report results back

echo "=== GREAT-4C Phase -1: Handler Discovery ==="
echo ""

echo "1. Count canonical handlers:"
grep -r "async def _handle" services/intent_service/canonical_handlers.py | wc -l
echo ""

echo "2. List all handler method names:"
grep -r "async def _handle" services/intent_service/canonical_handlers.py | sed 's/.*async def \(_handle_[^(]*\).*/\1/' | sort
echo ""

echo "3. Handler categories used:"
grep -r "IntentCategory\." services/intent_service/canonical_handlers.py | grep -o "IntentCategory\.[A-Z_]*" | sort -u
echo ""

echo "4. Check for generic/undefined responses:"
grep -r "I don't understand\|undefined\|generic\|not sure how to" services/intent_service/ --include="*.py" | head -20
echo ""

echo "5. Check for existing context tracking:"
grep -r "session\|context\|conversation" services/intent_service/ --include="*.py" | grep -v "# " | head -20
echo ""

echo "6. Check for existing monitoring/metrics:"
grep -r "metrics\|monitoring\|feedback" services/intent_service/ --include="*.py" | head -20
echo ""

echo "7. Find canonical_handlers.py file:"
find . -name "canonical_handlers.py" -type f
echo ""

echo "8. Check file size (estimate handler complexity):"
wc -l services/intent_service/canonical_handlers.py 2>/dev/null || echo "File not found at expected location"
echo ""

echo "=== Discovery Complete ==="
echo "Report these results back to continue Phase -1"
