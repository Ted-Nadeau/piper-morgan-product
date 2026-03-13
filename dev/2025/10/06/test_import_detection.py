#!/usr/bin/env python3
"""Test import detection and web.app availability"""
import sys

sys.path.insert(0, ".")

print("=" * 80)
print("IMPORT ERROR DETECTION TEST")
print("=" * 80)

# Test 1: Can we import web.app?
print("\n1. Testing web.app import:")
try:
    from web.app import app

    print("✅ web.app imports successfully")
    print(f"   App type: {type(app)}")
    print(f"   App routes count: {len(app.routes)}")
except ImportError as e:
    print(f"❌ web.app import fails: {e}")
except Exception as e:
    print(f"⚠️  web.app import error: {type(e).__name__}: {e}")

# Test 2: Do tests actually use web.app?
print("\n2. Checking which tests import web.app:")
import subprocess

result = subprocess.run(
    ["grep", "-r", "from web.app import", "tests/"], capture_output=True, text=True
)
if result.stdout:
    print(f"Tests importing web.app:\n{result.stdout}")
else:
    print("❌ No tests import web.app directly")

# Test 3: Check for /health endpoint
print("\n3. Checking for /health endpoint:")
try:
    from web.app import app

    routes = [
        (r.path, list(r.methods))
        for r in app.routes
        if hasattr(r, "path") and hasattr(r, "methods")
    ]
    health_routes = [r for r in routes if "health" in r[0].lower()]
    if health_routes:
        print(f"✅ Found health endpoint(s):")
        for path, methods in health_routes:
            print(f"   {path}: {methods}")
    else:
        print("❌ No /health endpoint found")
        print("\n   Available routes:")
        for path, methods in sorted(routes)[:10]:
            print(f"   {path}: {methods}")
except Exception as e:
    print(f"⚠️  Error checking routes: {e}")

# Test 4: Check test files for /health tests
print("\n4. Checking tests for /health endpoint tests:")
result = subprocess.run(
    ["grep", "-r", "/health", "tests/", "--include=*.py"], capture_output=True, text=True
)
if result.stdout:
    lines = result.stdout.strip().split("\n")
    print(f"Found {len(lines)} references to /health in tests:")
    for line in lines[:5]:  # Show first 5
        print(f"   {line}")
else:
    print("❌ No test references to /health found")

# Test 5: Check for tests that allow 404
print("\n5. Checking for tests that allow 404 responses:")
result = subprocess.run(
    ["grep", "-r", "\\[200, 404\\]\\|404.*200", "tests/", "--include=*.py"],
    capture_output=True,
    text=True,
)
if result.stdout:
    lines = result.stdout.strip().split("\n")
    print(f"Found {len(lines)} tests that allow 404:")
    for line in lines:
        print(f"   {line}")
else:
    print("✅ No tests explicitly allow 404 responses")

print("\n" + "=" * 80)
print("IMPORT DETECTION TEST COMPLETE")
print("=" * 80)
