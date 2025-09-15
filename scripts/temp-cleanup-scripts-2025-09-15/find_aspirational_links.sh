#!/bin/bash
echo "=== Finding aspirational link references ==="

echo -e "\n1. API Design Spec references:"
grep -r "api-design-spec" docs/ --include="*.md" 2>/dev/null | head -5

echo -e "\n2. Dev Guide references:"
grep -r "dev-guide" docs/ --include="*.md" 2>/dev/null | head -5

echo -e "\n3. One-pager references:"
grep -r "one-pager" docs/ --include="*.md" 2>/dev/null | head -5

echo -e "\n4. Presentation references:"
grep -r "presentation" docs/ --include="*.md" -i 2>/dev/null | grep -E "\[.*\]\(" | head -5

echo -e "\n5. Advanced conversation references:"
grep -r "advanced.*conversation" docs/ --include="*.md" -i 2>/dev/null | grep -E "\[.*\]\(" | head -5
