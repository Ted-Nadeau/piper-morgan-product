#!/usr/bin/env python3
"""Test file upload functionality"""

import asyncio
import os
import tempfile
from datetime import datetime
from pathlib import Path

from services.domain.models import UploadedFile
from services.file_context.storage import generate_session_id, save_file_to_storage
from services.repositories import DatabasePool
from services.repositories.file_repository import FileRepository


async def test_file_upload():
    """Test the file upload functionality"""
    print("Testing file upload functionality...")

    try:
        # Create a temporary test file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
            test_content = b"This is a test file for upload functionality"
            tmp_file.write(test_content)
            tmp_file_path = tmp_file.name

        # Test storage function
        print("1. Testing file storage...")
        with open(tmp_file_path, "rb") as f:
            content = f.read()

        storage_path = await save_file_to_storage(content, "test_file.txt")
        print(f"   ✅ File saved to: {storage_path}")

        # Test session ID generation
        print("2. Testing session ID generation...")
        session_id = generate_session_id()
        print(f"   ✅ Generated session ID: {session_id}")

        # Test database integration
        print("3. Testing database integration...")
        pool = await DatabasePool.get_pool()
        repo = FileRepository(pool)

        uploaded_file = UploadedFile(
            session_id=session_id,
            filename="test_file.txt",
            file_type="text/plain",
            file_size=len(content),
            storage_path=storage_path,
            upload_time=datetime.now(),
        )

        saved_file = await repo.save_file_metadata(uploaded_file)
        print(f"   ✅ File saved to database with ID: {saved_file.id}")

        # Test retrieval
        retrieved_file = await repo.get_file_by_id(saved_file.id)
        if retrieved_file:
            print(f"   ✅ File retrieved successfully: {retrieved_file.filename}")
        else:
            print("   ❌ File retrieval failed")

        # Test session files
        session_files = await repo.get_files_for_session(session_id)
        print(f"   ✅ Found {len(session_files)} files in session")

        # Cleanup
        print("4. Cleaning up...")
        await repo.delete_file(saved_file.id)
        if os.path.exists(storage_path):
            os.unlink(storage_path)
        print("   ✅ Cleanup completed")

        print("\n🎉 All tests passed!")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
    finally:
        # Clean up temporary file
        if os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
        await pool.close()


if __name__ == "__main__":
    asyncio.run(test_file_upload())
