#!/bin/bash
set -e

echo "🔍 Verifying Python version for PM-055 compliance..."

# Get Python version (compatible approach)
PYTHON_FULL_VERSION=$(python --version 2>&1)
PYTHON_VERSION=$(echo "$PYTHON_FULL_VERSION" | awk '{print $2}' | cut -d. -f1-2)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

echo "📋 Detected Python version: $PYTHON_VERSION"

# Check if version meets PM-055 requirements (Python 3.11+)
if [[ "$PYTHON_MAJOR" -lt 3 ]] || [[ "$PYTHON_MAJOR" -eq 3 && "$PYTHON_MINOR" -lt 11 ]]; then
    echo "❌ ERROR: Python version $PYTHON_VERSION does not meet PM-055 requirements (≥3.11)"
    echo "   Expected: Python 3.11 or higher"
    echo "   Found: Python $PYTHON_VERSION"
    exit 1
fi

echo "✅ Python version $PYTHON_VERSION meets PM-055 requirements (≥3.11)"

# Verify key dependencies are compatible with Python 3.11
echo "🔧 Verifying core dependencies compatibility..."
python -c "
import sys
try:
    import asyncio
    import fastapi
    import sqlalchemy
    import uvicorn
    print('✅ Core dependencies compatible with Python {}.{}'.format(sys.version_info.major, sys.version_info.minor))
except ImportError as e:
    print('❌ Dependency compatibility issue:', e)
    sys.exit(1)
" || exit 1

# Verify async patterns work (important for Python 3.11+ compatibility)
echo "🔄 Verifying async patterns..."
python -c "
import asyncio
import sys

async def test_async():
    return 'async_ok'

try:
    result = asyncio.run(test_async())
    if result == 'async_ok':
        print('✅ Async patterns working correctly with Python {}.{}'.format(sys.version_info.major, sys.version_info.minor))
    else:
        raise Exception('Async test failed')
except Exception as e:
    print('❌ Async pattern compatibility issue:', e)
    sys.exit(1)
"

echo "🚀 Docker container ready with Python 3.11 (PM-055 compliant)"
echo "📅 Version verification completed: $(date)"
