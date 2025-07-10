#!/usr/bin/env python3
"""Test the complete file disambiguation flow"""

import asyncio
from datetime import datetime

from services.domain.models import Intent, IntentCategory, UploadedFile
from services.repositories import DatabasePool
from services.repositories.file_repository import FileRepository
from services.session.session_manager import (ConversationSession,
                                              SessionManager)
from services.utils.serialization import serialize_dataclass


async def test_disambiguation_flow():
    """Test the complete file disambiguation flow"""
    print("Testing file disambiguation flow...")

    try:
        # Create session manager
        session_manager = SessionManager()
        session_id = "test_disambiguation_session"
        session = session_manager.get_or_create_session(session_id)

        # Create test files
        pool = await DatabasePool.get_pool()
        repo = FileRepository(pool)

        file1 = UploadedFile(
            session_id=session_id,
            filename="report_v1.pdf",
            file_type="application/pdf",
            file_size=1000,
            storage_path="/test/report_v1.pdf",
            upload_time=datetime.now(),
        )

        file2 = UploadedFile(
            session_id=session_id,
            filename="report_v2.pdf",
            file_type="application/pdf",
            file_size=1000,
            storage_path="/test/report_v2.pdf",
            upload_time=datetime.now(),
        )

        # Save files
        saved_file1 = await repo.save_file_metadata(file1)
        saved_file2 = await repo.save_file_metadata(file2)
        print(f"✅ Created test files: {saved_file1.filename}, {saved_file2.filename}")

        # Test 1: Set disambiguation state
        print("\n1. Testing disambiguation state setting...")
        original_intent = Intent(
            category=IntentCategory.ANALYSIS,
            action="analyze_report",
            context={"original_message": "analyze the report"},
        )

        ambiguous_files = [
            {
                "id": saved_file1.id,
                "filename": saved_file1.filename,
                "upload_time": saved_file1.upload_time.isoformat(),
            },
            {
                "id": saved_file2.id,
                "filename": saved_file2.filename,
                "upload_time": saved_file2.upload_time.isoformat(),
            },
        ]

        session.set_clarification(
            "file_disambiguation",
            {
                "ambiguous_files": ambiguous_files,
                "original_intent": serialize_dataclass(original_intent),
            },
        )

        print(f"   ✅ Set clarification state: {session.awaiting_clarification}")
        print(
            f"   ✅ Ambiguous files count: {len(session.get_clarification_context('ambiguous_files', []))}"
        )

        # Test 2: Simulate user selecting file 1
        print("\n2. Testing user selection (file 1)...")
        user_response = "1"

        # Check if this is a disambiguation response
        if session.awaiting_clarification == "file_disambiguation":
            print("   ✅ Detected disambiguation response")

            # Parse user choice
            if user_response.isdigit():
                choice = int(user_response) - 1
                ambiguous_files = session.get_clarification_context(
                    "ambiguous_files", []
                )

                if 0 <= choice < len(ambiguous_files):
                    selected_file = ambiguous_files[choice]
                    print(f"   ✅ User selected: {selected_file['filename']}")

                    # Get original intent
                    original_intent_data = session.get_clarification_context(
                        "original_intent"
                    )
                    if original_intent_data:
                        print("   ✅ Retrieved original intent data")

                        # Reconstruct intent with selected file
                        intent = Intent(
                            category=IntentCategory(original_intent_data["category"]),
                            action=original_intent_data["action"],
                            context={
                                **original_intent_data.get("context", {}),
                                "resolved_file_id": selected_file["id"],
                                "file_confidence": 1.0,
                            },
                        )

                        print(f"   ✅ Reconstructed intent: {intent.action}")
                        print(
                            f"   ✅ Resolved file ID: {intent.context.get('resolved_file_id')}"
                        )
                        print(
                            f"   ✅ File confidence: {intent.context.get('file_confidence')}"
                        )

                        # Clear disambiguation state
                        session.clear_clarification()
                        print("   ✅ Cleared clarification state")

                        # Test serialization
                        serialized = serialize_dataclass(intent)
                        print(f"   ✅ Serialized intent: {serialized['action']}")

        # Test 3: Verify state is cleared
        print("\n3. Testing state cleanup...")
        if session.awaiting_clarification is None:
            print("   ✅ Clarification state properly cleared")
        else:
            print("   ❌ Clarification state not cleared")

        # Cleanup
        print("\n4. Cleaning up...")
        await repo.delete_file(saved_file1.id)
        await repo.delete_file(saved_file2.id)
        print("   ✅ Cleanup completed")

        print("\n🎉 Disambiguation flow test completed successfully!")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
    finally:
        await pool.close()


if __name__ == "__main__":
    asyncio.run(test_disambiguation_flow())
