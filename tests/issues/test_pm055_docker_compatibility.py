"""
PM-055 Step 4: Docker Python 3.11 Compatibility Test
Test that all key dependencies work correctly in Python 3.11 environment
"""

import asyncio
import sys


def test_dependencies():
    """Test that all key dependencies can be imported"""
    print("🧪 Testing dependency imports...")

    try:
        import fastapi

        print("✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False

    try:
        import sqlalchemy

        print("✅ SQLAlchemy imported successfully")
    except ImportError as e:
        print(f"❌ SQLAlchemy import failed: {e}")
        return False

    try:
        import uvicorn

        print("✅ Uvicorn imported successfully")
    except ImportError as e:
        print(f"❌ Uvicorn import failed: {e}")
        return False

    try:
        import asyncpg

        print("✅ AsyncPG imported successfully")
    except ImportError as e:
        print(f"❌ AsyncPG import failed: {e}")
        return False

    return True


async def test_asyncio_functionality():
    """Test asyncio functionality including timeout feature"""
    print("🧪 Testing asyncio functionality...")

    # Test basic asyncio
    await asyncio.sleep(0.001)
    print("✅ Basic asyncio working")

    # Test asyncio.timeout (key PM-055 feature)
    if not hasattr(asyncio, "timeout"):
        print("❌ asyncio.timeout not available")
        return False

    try:
        async with asyncio.timeout(0.01):
            await asyncio.sleep(0.02)  # Should timeout
        print("❌ asyncio.timeout should have triggered")
        return False
    except asyncio.TimeoutError:
        print("✅ asyncio.timeout working correctly")

    return True


def main():
    """Main test execution"""
    print("🚀 PM-055 Step 4: Docker Python 3.11 Compatibility Test")
    print(f"🐍 Python version: {'.'.join(map(str, sys.version_info[:3]))}")

    # Test dependency imports
    deps_ok = test_dependencies()

    # Test asyncio functionality
    asyncio_ok = asyncio.run(test_asyncio_functionality())

    overall_success = deps_ok and asyncio_ok

    if overall_success:
        print("🎉 PM-055 Docker Compatibility: SUCCESS")
        print("✅ Python 3.11 ready for production deployment")
    else:
        print("❌ PM-055 Docker Compatibility: FAILED")
        print("⚠️  Python 3.11 deployment not ready")

    return overall_success


if __name__ == "__main__":
    result = main()
    sys.exit(0 if result else 1)
