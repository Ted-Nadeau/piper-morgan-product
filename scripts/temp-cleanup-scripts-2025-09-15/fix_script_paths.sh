#!/bin/bash
# Fix script paths based on document location

echo "=== Fixing Script Paths ==="

# Fix in docs/ root (need ../scripts/)
echo "Fixing script paths in docs/ root..."
find docs -maxdepth 1 -name "*.md" -exec sed -i '' 's|scripts/run_tests\.sh|../scripts/run_tests.sh|g' {} \;
find docs -maxdepth 1 -name "*.md" -exec sed -i '' 's|scripts/deploy_multi_agent|../scripts/deploy_multi_agent|g' {} \;
find docs -maxdepth 1 -name "*.md" -exec sed -i '' 's|scripts/validate_multi_agent|../scripts/validate_multi_agent|g' {} \;

# Fix in docs/development/ (need ../../scripts/)
echo "Fixing script paths in docs/development/..."
find docs/development -name "*.md" -exec sed -i '' 's|scripts/run_tests\.sh|../../scripts/run_tests.sh|g' {} \;
find docs/development -name "*.md" -exec sed -i '' 's|scripts/deploy_multi_agent|../../scripts/deploy_multi_agent|g' {} \;
find docs/development -name "*.md" -exec sed -i '' 's|scripts/validate_multi_agent|../../scripts/validate_multi_agent|g' {} \;

# Fix in docs/architecture/ (need ../../scripts/)
echo "Fixing script paths in docs/architecture/..."
find docs/architecture -name "*.md" -exec sed -i '' 's|scripts/run_tests\.sh|../../scripts/run_tests.sh|g' {} \;

echo "Script path fixes complete!"
