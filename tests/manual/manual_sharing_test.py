"""
Manual testing script for SEC-RBAC Phase 1.4 - Shared Resource Access
Tests the sharing functionality for Lists and Todos with read-only access.

To run:
    PYTHONPATH=. python tests/manual/manual_sharing_test.py

Requirements:
- Server running on http://localhost:8001
- Two test users created in the system
- JWT tokens for both users
"""

import asyncio
import json
from datetime import datetime, timedelta

import httpx

# Configuration
API_BASE = "http://localhost:8001/api/v1"
USER_A_ID = "550e8400-e29b-41d4-a716-446655440000"  # Owner
USER_B_ID = "7c9e6679-7425-40de-944b-e07fc1f90ae7"  # Shared user

# Mock JWT tokens for testing (these should be real tokens in actual testing)
MOCK_TOKEN_A = "mock-token-a"
MOCK_TOKEN_B = "mock-token-b"

HEADERS_A = {
    "Authorization": f"Bearer {MOCK_TOKEN_A}",
    "Content-Type": "application/json",
}
HEADERS_B = {
    "Authorization": f"Bearer {MOCK_TOKEN_B}",
    "Content-Type": "application/json",
}


async def test_list_sharing():
    """Test list sharing functionality"""
    print("\n" + "=" * 70)
    print("Testing List Sharing (SEC-RBAC Phase 1.4)")
    print("=" * 70)

    async with httpx.AsyncClient() as client:
        # Step 1: User A creates a list
        print("\n[Step 1] User A creates a list...")
        create_response = await client.post(
            f"{API_BASE}/lists",
            json={"name": "Shared Test List", "description": "Testing sharing"},
            headers=HEADERS_A,
        )

        if create_response.status_code != 200:
            print(f"❌ Failed to create list: {create_response.status_code}")
            print(f"Response: {create_response.text}")
            return

        list_data = create_response.json()
        list_id = list_data.get("id")
        print(f"✅ List created with ID: {list_id}")

        # Step 2: User A shares the list with User B
        print(f"\n[Step 2] User A shares list {list_id} with User B...")
        share_response = await client.post(
            f"{API_BASE}/lists/{list_id}/share",
            json={"user_id": USER_B_ID},
            headers=HEADERS_A,
        )

        if share_response.status_code != 200:
            print(f"❌ Failed to share list: {share_response.status_code}")
            print(f"Response: {share_response.text}")
            return

        shared_list = share_response.json()
        print(f"✅ List shared! Shared with: {shared_list.get('shared_with')}")

        # Step 3: User B retrieves the shared list (should work - read access)
        print(f"\n[Step 3] User B retrieves the shared list (should succeed)...")
        read_response = await client.get(
            f"{API_BASE}/lists/{list_id}",
            headers=HEADERS_B,
        )

        if read_response.status_code == 200:
            print(f"✅ User B can read the shared list")
        else:
            print(f"❌ User B cannot read shared list: {read_response.status_code}")

        # Step 4: User B tries to update the list (should fail - 404 for no permission)
        print(f"\n[Step 4] User B tries to update the list (should fail with 404)...")
        update_response = await client.put(
            f"{API_BASE}/lists/{list_id}",
            json={"name": "Hacked List"},
            headers=HEADERS_B,
        )

        if update_response.status_code == 404:
            print(f"✅ User B blocked from updating (404 returned)")
        elif update_response.status_code == 403:
            print(f"✅ User B blocked from updating (403 Forbidden returned)")
        else:
            print(f"❌ Unexpected response: {update_response.status_code}")
            print(f"Response: {update_response.text}")

        # Step 5: User B tries to delete the list (should fail - 404 for no permission)
        print(f"\n[Step 5] User B tries to delete the list (should fail with 404)...")
        delete_response = await client.delete(
            f"{API_BASE}/lists/{list_id}",
            headers=HEADERS_B,
        )

        if delete_response.status_code == 404:
            print(f"✅ User B blocked from deleting (404 returned)")
        elif delete_response.status_code == 403:
            print(f"✅ User B blocked from deleting (403 Forbidden returned)")
        else:
            print(f"❌ Unexpected response: {delete_response.status_code}")

        # Step 6: User B tries to share the list further (should fail - 404)
        print(f"\n[Step 6] User B tries to share list with another user (should fail)...")
        share_again_response = await client.post(
            f"{API_BASE}/lists/{list_id}/share",
            json={"user_id": "ffffffff-ffff-ffff-ffff-ffffffffffff"},
            headers=HEADERS_B,
        )

        if share_again_response.status_code == 404:
            print(f"✅ User B blocked from sharing (404 returned)")
        elif share_again_response.status_code == 403:
            print(f"✅ User B blocked from sharing (403 Forbidden returned)")
        else:
            print(f"❌ Unexpected response: {share_again_response.status_code}")

        # Step 7: User A retrieves shared lists (List should appear)
        print(f"\n[Step 7] User B retrieves their shared lists...")
        shared_lists_response = await client.get(
            f"{API_BASE}/lists/shared-with-me",
            headers=HEADERS_B,
        )

        if shared_lists_response.status_code == 200:
            shared_data = shared_lists_response.json()
            count = shared_data.get("count", 0)
            if count > 0:
                print(f"✅ User B sees {count} shared list(s)")
            else:
                print(f"❌ User B doesn't see the shared list")
        else:
            print(f"❌ Failed to retrieve shared lists: {shared_lists_response.status_code}")

        # Step 8: User A unshares the list with User B
        print(f"\n[Step 8] User A unshares the list with User B...")
        unshare_response = await client.delete(
            f"{API_BASE}/lists/{list_id}/share/{USER_B_ID}",
            headers=HEADERS_A,
        )

        if unshare_response.status_code == 200:
            print(f"✅ List unshared successfully")
        else:
            print(f"❌ Failed to unshare: {unshare_response.status_code}")
            print(f"Response: {unshare_response.text}")

        # Step 9: User B tries to access the list again (should fail - 404)
        print(f"\n[Step 9] User B tries to access the unshared list (should fail)...")
        read_again_response = await client.get(
            f"{API_BASE}/lists/{list_id}",
            headers=HEADERS_B,
        )

        if read_again_response.status_code == 404:
            print(f"✅ User B cannot access unshared list (404 returned)")
        else:
            print(f"❌ User B still has access: {read_again_response.status_code}")


async def test_todo_sharing():
    """Test todo sharing functionality"""
    print("\n" + "=" * 70)
    print("Testing Todo Sharing (SEC-RBAC Phase 1.4)")
    print("=" * 70)

    async with httpx.AsyncClient() as client:
        # Step 1: User A creates a todo
        print("\n[Step 1] User A creates a todo...")
        create_response = await client.post(
            f"{API_BASE}/todos",
            json={
                "title": "Shared Test Todo",
                "description": "Testing todo sharing",
                "status": "pending",
            },
            headers=HEADERS_A,
        )

        if create_response.status_code != 200:
            print(f"❌ Failed to create todo: {create_response.status_code}")
            print(f"Response: {create_response.text}")
            return

        todo_data = create_response.json()
        todo_id = todo_data.get("id")
        print(f"✅ Todo created with ID: {todo_id}")

        # Step 2: User A shares the todo with User B
        print(f"\n[Step 2] User A shares todo {todo_id} with User B...")
        share_response = await client.post(
            f"{API_BASE}/todos/{todo_id}/share",
            json={"user_id": USER_B_ID},
            headers=HEADERS_A,
        )

        if share_response.status_code != 200:
            print(f"❌ Failed to share todo: {share_response.status_code}")
            print(f"Response: {share_response.text}")
            return

        shared_todo = share_response.json()
        print(f"✅ Todo shared! Shared with: {shared_todo.get('shared_with')}")

        # Step 3: User B retrieves the shared todo (should work - read access)
        print(f"\n[Step 3] User B retrieves the shared todo (should succeed)...")
        read_response = await client.get(
            f"{API_BASE}/todos/{todo_id}",
            headers=HEADERS_B,
        )

        if read_response.status_code == 200:
            print(f"✅ User B can read the shared todo")
        else:
            print(f"❌ User B cannot read shared todo: {read_response.status_code}")

        # Step 4: User B tries to update the todo (should fail - 404)
        print(f"\n[Step 4] User B tries to update the todo (should fail)...")
        update_response = await client.put(
            f"{API_BASE}/todos/{todo_id}",
            json={"status": "completed"},
            headers=HEADERS_B,
        )

        if update_response.status_code == 404:
            print(f"✅ User B blocked from updating (404 returned)")
        elif update_response.status_code == 403:
            print(f"✅ User B blocked from updating (403 Forbidden returned)")
        else:
            print(f"❌ Unexpected response: {update_response.status_code}")

        # Step 5: User B retrieves their shared todos
        print(f"\n[Step 5] User B retrieves their shared todos...")
        shared_todos_response = await client.get(
            f"{API_BASE}/todos/shared-with-me",
            headers=HEADERS_B,
        )

        if shared_todos_response.status_code == 200:
            shared_data = shared_todos_response.json()
            count = shared_data.get("count", 0)
            if count > 0:
                print(f"✅ User B sees {count} shared todo(s)")
            else:
                print(f"⚠️  User B doesn't see the shared todo (count: {count})")
        else:
            print(f"❌ Failed to retrieve shared todos: {shared_todos_response.status_code}")

        # Step 6: User A unshares the todo
        print(f"\n[Step 6] User A unshares the todo with User B...")
        unshare_response = await client.delete(
            f"{API_BASE}/todos/{todo_id}/share/{USER_B_ID}",
            headers=HEADERS_A,
        )

        if unshare_response.status_code == 200:
            print(f"✅ Todo unshared successfully")
        else:
            print(f"❌ Failed to unshare: {unshare_response.status_code}")

        # Step 7: User B tries to access the todo again (should fail - 404)
        print(f"\n[Step 7] User B tries to access the unshared todo (should fail)...")
        read_again_response = await client.get(
            f"{API_BASE}/todos/{todo_id}",
            headers=HEADERS_B,
        )

        if read_again_response.status_code == 404:
            print(f"✅ User B cannot access unshared todo (404 returned)")
        else:
            print(f"❌ User B still has access: {read_again_response.status_code}")


async def main():
    """Run all tests"""
    print("\n" + "█" * 70)
    print("SEC-RBAC Phase 1.4 - Manual Sharing Tests")
    print("█" * 70)
    print("\n⚠️  NOTE: These tests require a running server and actual JWT tokens.")
    print("Current configuration uses mock tokens - they will fail unless tokens are updated.")
    print(f"\nServer: {API_BASE}")
    print(f"User A (Owner): {USER_A_ID}")
    print(f"User B (Shared): {USER_B_ID}")

    try:
        await test_list_sharing()
        await test_todo_sharing()
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "█" * 70)
    print("Testing Complete")
    print("█" * 70)


if __name__ == "__main__":
    asyncio.run(main())
