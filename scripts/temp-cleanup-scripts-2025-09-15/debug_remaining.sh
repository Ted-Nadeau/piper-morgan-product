#!/bin/bash
echo "=== Checking PIPER configuration files ==="
ls -la config/PIPER* 2>/dev/null

echo -e "\n=== Finding references to each ==="
echo "References to PIPER.md:"
grep -r "PIPER\.md" docs/ --include="*.md" | grep -v "PIPER.user.md" | wc -l

echo "References to PIPER.user.md:"
grep -r "PIPER\.user\.md" docs/ --include="*.md" | wc -l

echo -e "\n=== Finding the remaining stubborn issues ==="

echo -e "\nContributing.md references (what depth are they at?):"
grep -r "CONTRIBUTING" docs/ --include="*.md" | grep "../../CONTRIBUTING" | head -2

echo -e "\nScript references still broken (what depth?):"
grep -r "../../scripts/" docs/ --include="*.md" | head -2

echo -e "\nSession-log-framework ultra-deep reference:"
grep -r "../../../development/session-logs/" docs/ --include="*.md" | head -2

echo -e "\nWeird formatting artifacts:"
grep -r "\[1m\"" docs/ --include="*.md" | head -2
grep -r "\[0m\"" docs/ --include="*.md" | head -2

echo -e "\nOrchestration testing reference:"
find . -name "*orchestration-testing*" -type f 2>/dev/null
