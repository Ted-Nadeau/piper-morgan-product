#!/usr/bin/env python3
"""Simple test for FileRepository"""

import asyncio
import os
from services.repositories.file_repository import FileRepository
from services.domain.models import UploadedFile
from services.repositories import DatabasePool

async def test_file_repository():
    """Test basic FileRepository functionality"""
    print("Testing FileRepository...")
    
    # Get database pool
    pool = await DatabasePool.get_pool()
    repo = FileRepository(pool)
    
    try:
        # Create a test file
        test_file = UploadedFile(
            session_id="test-session-123",
            filename="test_document.pdf",
            file_type="application/pdf",
            file_size=2048,
            storage_path="/tmp/test_document.pdf",
            metadata={"test": True, "version": "1.0"}
        )
        
        print(f"Created test file: {test_file.filename}")
        print(f"File ID: {test_file.id}")
        print(f"Session: {test_file.session_id}")
        
        # Save to database
        print("Saving file metadata...")
        saved_file = await repo.save_file_metadata(test_file)
        print(f"Saved file ID: {saved_file.id}")
        
        # Retrieve from database
        print("Retrieving file metadata...")
        retrieved_file = await repo.get_file_by_id(test_file.id)
        
        if retrieved_file:
            print(f"Retrieved file: {retrieved_file.filename}")
            print(f"File type: {retrieved_file.file_type}")
            print(f"File size: {retrieved_file.file_size}")
            print(f"Metadata: {retrieved_file.metadata}")
            print("✅ File save and retrieve test PASSED")
        else:
            print("❌ File retrieve test FAILED")
            
        # Test session files
        print("Testing session files retrieval...")
        session_files = await repo.get_files_for_session("test-session-123")
        print(f"Found {len(session_files)} files in session")
        
        if len(session_files) > 0:
            print("✅ Session files test PASSED")
        else:
            print("❌ Session files test FAILED")
            
        # Test search
        print("Testing file search...")
        search_results = await repo.search_files_by_name("test-session-123", "test")
        print(f"Search found {len(search_results)} files")
        
        if len(search_results) > 0:
            print("✅ File search test PASSED")
        else:
            print("❌ File search test FAILED")
            
        # Clean up
        print("Cleaning up test data...")
        await repo.delete_file(test_file.id)
        print("✅ Cleanup completed")
        
    except Exception as e:
        print(f"❌ Test FAILED with error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await pool.close()

if __name__ == "__main__":
    asyncio.run(test_file_repository()) 