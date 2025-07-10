#!/usr/bin/env python3
"""
Test script for the updated API flow with clarification handling
"""
import asyncio
import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.conversation.conversation_handler import ConversationHandler
from services.intent_service import classifier
from services.session.session_manager import SessionManager
from services.shared_types import IntentCategory


async def test_api_flow():
    """Test the API flow with clarification handling"""

    print("Testing updated API flow with clarification...")
    print("=" * 60)

    # Initialize components
    session_manager = SessionManager(ttl_minutes=30)
    conversation_handler = ConversationHandler(session_manager=session_manager)
    session_id = "test_api_session"

    # Simulate API flow
    print("\n1. First request: Vague intent")
    vague_message = "Fix the bug"

    # Simulate the API call
    session = session_manager.get_or_create_session(session_id)
    intent = await classifier.classify(vague_message)

    print(f"   Input: '{vague_message}'")
    print(f"   Intent: {intent.category} / {intent.action}")

    if (
        intent.category == IntentCategory.CONVERSATION
        and intent.action == "clarification_needed"
    ):
        print("   ✅ Vague intent detected")

        # Simulate API response
        response = await conversation_handler.respond(intent, session_id)
        print(f"   API Response: {response['message']}")

        # Check if clarification is pending
        pending = session.get_pending_clarification()
        if pending:
            print("   ✅ Clarification state stored in session")
        else:
            print("   ❌ No clarification state stored")
            return
    else:
        print("   ❌ Vague intent not detected")
        return

    print("\n2. Second request: Clarification response")
    clarification_message = "The login button shows a 500 error on mobile devices"

    # Simulate the API call with pending clarification
    response2 = await conversation_handler.handle_clarification_response(
        clarification_message, session_id
    )

    print(f"   Input: '{clarification_message}'")
    print(f"   API Response: {response2['message']}")

    if response2.get("clarification_resolved"):
        print("   ✅ Clarification resolved")

        # Check if session state is cleared
        pending_after = session.get_pending_clarification()
        if not pending_after:
            print("   ✅ Session state cleared after resolution")
        else:
            print("   ❌ Session state not cleared")
    else:
        print("   ❌ Clarification not resolved")
        print(f"   Still needs: {response2.get('clarification_data', {})}")

    print("\n3. Third request: Normal request after clarification")
    normal_message = "List all projects"

    # Simulate normal API call
    intent3 = await classifier.classify(normal_message)
    print(f"   Input: '{normal_message}'")
    print(f"   Intent: {intent3.category} / {intent3.action}")

    if intent3.category == IntentCategory.QUERY:
        print("   ✅ Normal intent processed correctly")
    else:
        print("   ❌ Normal intent not processed correctly")

    print("\n" + "=" * 60)
    print("API flow test complete!")


if __name__ == "__main__":
    asyncio.run(test_api_flow())
