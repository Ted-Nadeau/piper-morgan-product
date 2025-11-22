#!/usr/bin/env python3
"""
Manual test script for SEC-RBAC Phase 2 role-based permissions.

Tests all 24 role × operation combinations:
- Owner: Full permissions (all operations succeed)
- Admin: Can share but can't delete
- Editor: Can modify but can't share/delete
- Viewer: Read-only (can't modify/delete/share)

Run: python tests/manual/manual_rbac_phase2_role_permissions.py

Note: Requires running server on localhost:8001 and test database setup.
"""

import asyncio
import json
import os
import uuid
from typing import Optional

import httpx
from dotenv import load_dotenv

BASE_URL = "http://localhost:8001"
TIMEOUT = 10.0

# Test user tokens (will be created during test)
test_users = {
    "owner": {"token": None, "user_id": None},
    "admin": {"token": None, "user_id": None},
    "editor": {"token": None, "user_id": None},
    "viewer": {"token": None, "user_id": None},
}

# Test results tracking
test_results = []


async def make_request(
    method: str,
    endpoint: str,
    token: str,
    json_data: dict = None,
    expected_status: int = None,
) -> dict:
    """Make HTTP request and return response"""
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    url = f"{BASE_URL}{endpoint}"

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            if method.upper() == "GET":
                response = await client.get(url, headers=headers)
            elif method.upper() == "POST":
                response = await client.post(url, headers=headers, json=json_data)
            elif method.upper() == "PUT":
                response = await client.put(url, headers=headers, json=json_data)
            elif method.upper() == "DELETE":
                response = await client.delete(url, headers=headers)
            else:
                raise ValueError(f"Unknown method: {method}")

            return {
                "status": response.status_code,
                "success": True,
                "data": response.json() if response.text else None,
            }
    except Exception as e:
        return {
            "status": None,
            "success": False,
            "error": str(e),
        }


async def create_test_list(
    role: str,
    list_name: str = None,
) -> Optional[str]:
    """Create a test list as the given role"""
    if list_name is None:
        list_name = f"Test List - {role.upper()} - {uuid.uuid4().hex[:8]}"

    token = test_users[role]["token"]

    response = await make_request(
        "POST",
        "/api/v1/lists",
        token,
        json_data={"name": list_name, "description": f"Test list for {role} role"},
    )

    if response["success"] and response["status"] == 200:
        list_id = response["data"].get("id")
        print(f"  ✓ Created list {list_id} as {role}")
        return list_id
    else:
        print(f"  ✗ Failed to create list as {role}: {response}")
        return None


async def share_list(
    list_id: str,
    share_with_role: str,
    share_with_user_id: str,
    assigned_role: str,
) -> bool:
    """Share a list with a user at specified role"""
    owner_token = test_users["owner"]["token"]

    response = await make_request(
        "POST",
        f"/api/v1/lists/{list_id}/share",
        owner_token,
        json_data={"user_id": share_with_user_id, "role": assigned_role},
    )

    if response["success"] and response["status"] == 200:
        return True
    else:
        print(f"  ✗ Failed to share list: {response}")
        return False


async def test_operation(
    role: str,
    operation: str,
    list_id: str,
    expected_status: int,
) -> bool:
    """Test a specific operation for a role"""
    token = test_users[role]["token"]

    if operation == "read":
        response = await make_request("GET", f"/api/v1/lists/{list_id}", token)
    elif operation == "update":
        response = await make_request(
            "PUT",
            f"/api/v1/lists/{list_id}",
            token,
            json_data={"name": f"Updated by {role}"},
        )
    elif operation == "delete":
        response = await make_request("DELETE", f"/api/v1/lists/{list_id}", token)
    elif operation == "share":
        new_user_id = str(uuid.uuid4())
        response = await make_request(
            "POST",
            f"/api/v1/lists/{list_id}/share",
            token,
            json_data={"user_id": new_user_id, "role": "viewer"},
        )
    elif operation == "unshare":
        # For unshare, we need to know who to unshare
        # In a real test, we'd track shared users
        other_role = "viewer" if role != "viewer" else "editor"
        other_user_id = test_users[other_role]["user_id"]
        response = await make_request(
            "DELETE",
            f"/api/v1/lists/{list_id}/share/{other_user_id}",
            token,
        )
    elif operation == "change_role":
        other_role = "viewer" if role != "viewer" else "editor"
        other_user_id = test_users[other_role]["user_id"]
        response = await make_request(
            "PUT",
            f"/api/v1/lists/{list_id}/share/{other_user_id}",
            token,
            json_data={"role": "admin"},
        )
    else:
        raise ValueError(f"Unknown operation: {operation}")

    actual_status = response["status"]
    passed = actual_status == expected_status

    status_symbol = "✅" if passed else "❌"
    print(f"    {status_symbol} {operation:12} → {actual_status} (expected {expected_status})")

    return passed


async def run_tests():
    """Run all 24 test cases (4 roles × 6 operations)"""
    print("\n" + "=" * 70)
    print("SEC-RBAC Phase 2: Role-Based Permissions Test")
    print("=" * 70)

    # Test matrix: Expected status codes for each role/operation combo
    # 200 = success, 404 = access denied (returns 404 not 403)
    test_matrix = {
        "owner": {
            "read": 200,
            "update": 200,
            "delete": 200,
            "share": 200,
            "unshare": 200,
            "change_role": 200,
        },
        "admin": {
            "read": 200,
            "update": 200,
            "delete": 404,  # Admin cannot delete
            "share": 200,
            "unshare": 200,
            "change_role": 200,
        },
        "editor": {
            "read": 200,
            "update": 200,
            "delete": 404,  # Editor cannot delete
            "share": 404,  # Editor cannot share
            "unshare": 404,  # Editor cannot unshare
            "change_role": 404,  # Editor cannot change roles
        },
        "viewer": {
            "read": 200,
            "update": 404,  # Viewer cannot update
            "delete": 404,  # Viewer cannot delete
            "share": 404,  # Viewer cannot share
            "unshare": 404,  # Viewer cannot unshare
            "change_role": 404,  # Viewer cannot change roles
        },
    }

    # Create test list (as owner)
    list_id = await create_test_list("owner", "Test List for RBAC Phase 2")
    if not list_id:
        print("✗ Failed to create test list")
        return 1

    # Share with other roles
    print("\nSharing test list with other roles...")
    await share_list(list_id, "admin", test_users["admin"]["user_id"], "admin")
    await share_list(list_id, "editor", test_users["editor"]["user_id"], "editor")
    await share_list(list_id, "viewer", test_users["viewer"]["user_id"], "viewer")

    # Run all 24 test cases
    print("\n" + "=" * 70)
    print("Testing Role-Based Permissions")
    print("=" * 70)

    total_tests = 0
    passed_tests = 0

    for role in ["owner", "admin", "editor", "viewer"]:
        print(f"\nTesting {role.upper()} Role (6 operations):")
        print("-" * 70)

        for operation in ["read", "update", "delete", "share", "unshare", "change_role"]:
            expected = test_matrix[role][operation]
            result = await test_operation(role, operation, list_id, expected)

            total_tests += 1
            if result:
                passed_tests += 1

    # Summary
    print("\n" + "=" * 70)
    print(f"RBAC Phase 2 Manual Test Results: {passed_tests}/{total_tests} passed")
    print("=" * 70)

    if passed_tests == total_tests:
        print("\n✅ ALL TESTS PASSED - Role-based permissions working correctly!")
        return 0
    else:
        failed = total_tests - passed_tests
        print(f"\n❌ {failed} TESTS FAILED - Review failures above")
        return 1


async def main():
    """Main entry point"""
    load_dotenv()

    print("Initializing test users...")
    print("NOTE: This test assumes test users can be created with Bearer tokens")
    print("or uses existing test credentials from .env file\n")

    # For this manual test, we'll use placeholder tokens
    # In a real scenario, these would be created via signup/login
    for role in ["owner", "admin", "editor", "viewer"]:
        test_users[role]["user_id"] = str(uuid.uuid4())
        test_users[role]["token"] = f"test-token-{role}"

    print(f"Owner ID:  {test_users['owner']['user_id']}")
    print(f"Admin ID:  {test_users['admin']['user_id']}")
    print(f"Editor ID: {test_users['editor']['user_id']}")
    print(f"Viewer ID: {test_users['viewer']['user_id']}\n")

    # Run the test suite
    exit_code = await run_tests()
    return exit_code


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
