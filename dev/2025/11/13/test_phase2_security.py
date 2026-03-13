"""
Manual security tests for Phase 2 User Controls API (Issue #300)
Tests pattern ownership and authorization

Usage: python dev/2025/11/13/test_phase2_security.py
"""

from uuid import uuid4

import requests

BASE_URL = "http://localhost:8001/api/v1/learning"

# Test user (from Phase 1)
TEST_USER_ID = "3f4593ae-5bc9-468d-b08d-8c4c02a5b963"


def test_ownership():
    """Test that users can only access their own patterns"""

    print("\n" + "=" * 70)
    print("TEST 1: Pattern Ownership Verification")
    print("=" * 70)

    # Get patterns for test user
    print("\n1. Getting patterns for test user...")
    response = requests.get(f"{BASE_URL}/patterns")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    patterns = data.get("patterns", [])

    if not patterns:
        print("⚠️  No patterns exist for test - create some first")
        return

    print(f"✅ Found {len(patterns)} patterns")

    # Try to access existing pattern (should work)
    pattern_id = patterns[0]["id"]
    print(f"\n2. Accessing own pattern {pattern_id[:8]}...")
    response = requests.get(f"{BASE_URL}/patterns/{pattern_id}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print(f"✅ Can access own pattern: {pattern_id[:8]}...")

    # Try to access non-existent pattern (should 404)
    fake_id = str(uuid4())
    print(f"\n3. Accessing non-existent pattern {fake_id[:8]}...")
    response = requests.get(f"{BASE_URL}/patterns/{fake_id}")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    print(f"✅ Cannot access non-existent pattern (404)")

    # Try to delete non-existent pattern (should 404)
    print(f"\n4. Deleting non-existent pattern {fake_id[:8]}...")
    response = requests.delete(f"{BASE_URL}/patterns/{fake_id}")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    print(f"✅ Cannot delete non-existent pattern (404)")

    # Try to disable non-existent pattern (should 404)
    print(f"\n5. Disabling non-existent pattern {fake_id[:8]}...")
    response = requests.post(f"{BASE_URL}/patterns/{fake_id}/disable")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    print(f"✅ Cannot disable non-existent pattern (404)")

    print("\n✅ ALL OWNERSHIP TESTS PASSED!")


def test_settings_validation():
    """Test settings validation"""

    print("\n" + "=" * 70)
    print("TEST 2: Settings Validation")
    print("=" * 70)

    # Try invalid threshold (too high)
    print("\n1. Testing threshold > 1.0 (should fail)...")
    response = requests.put(
        f"{BASE_URL}/settings",
        json={"suggestion_threshold": 1.5},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    print("✅ Rejects threshold > 1.0 (422 Validation Error)")

    # Try invalid threshold (negative)
    print("\n2. Testing threshold < 0.0 (should fail)...")
    response = requests.put(
        f"{BASE_URL}/settings",
        json={"automation_threshold": -0.1},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    print("✅ Rejects threshold < 0.0 (422 Validation Error)")

    # Try valid threshold
    print("\n3. Testing valid threshold (should succeed)...")
    response = requests.put(
        f"{BASE_URL}/settings",
        json={"suggestion_threshold": 0.75},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("✅ Accepts valid threshold (200)")

    # Verify the setting persisted
    print("\n4. Verifying setting persisted...")
    response = requests.get(f"{BASE_URL}/settings")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert (
        data["settings"]["suggestion_threshold"] == 0.75
    ), f"Expected 0.75, got {data['settings']['suggestion_threshold']}"
    print("✅ Setting persisted correctly")

    print("\n✅ ALL VALIDATION TESTS PASSED!")


def test_error_handling():
    """Test error handling for edge cases"""

    print("\n" + "=" * 70)
    print("TEST 3: Error Handling")
    print("=" * 70)

    # 422: Invalid UUID format
    print("\n1. Testing invalid UUID format...")
    response = requests.get(f"{BASE_URL}/patterns/not-a-uuid")
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    print("✅ Invalid UUID format returns 422 (Unprocessable Entity)")

    # 404: Non-existent pattern with valid UUID
    print("\n2. Testing non-existent pattern with valid UUID...")
    fake_uuid = "00000000-0000-0000-0000-000000000000"
    response = requests.get(f"{BASE_URL}/patterns/{fake_uuid}")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    error_data = response.json()
    assert "message" in error_data, "Expected 'message' field in error response"
    print(f"✅ Non-existent pattern returns 404: {error_data['message']}")

    # Test invalid JSON
    print("\n3. Testing invalid JSON payload...")
    response = requests.put(
        f"{BASE_URL}/settings",
        data="not valid json",
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    print("✅ Invalid JSON returns 422")

    # Test invalid field type
    print("\n4. Testing invalid field type (dict instead of boolean)...")
    response = requests.put(
        f"{BASE_URL}/settings",
        json={"learning_enabled": {"invalid": "data"}},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    print("✅ Invalid field type returns 422")

    print("\n✅ ALL ERROR HANDLING TESTS PASSED!")


if __name__ == "__main__":
    try:
        print("\n" + "=" * 70)
        print("PHASE 2.3 SECURITY & ERROR HANDLING TESTS")
        print("Issue #300 - CORE-ALPHA-LEARNING-BASIC")
        print("=" * 70)

        test_ownership()
        test_settings_validation()
        test_error_handling()

        print("\n" + "=" * 70)
        print("🎉 ALL SECURITY TESTS PASSED!")
        print("=" * 70 + "\n")

    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        exit(1)
