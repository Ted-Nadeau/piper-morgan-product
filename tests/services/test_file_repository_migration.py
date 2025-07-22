"""
Test FileRepository migration to SQLAlchemy pattern
Following TDD approach to migrate from asyncpg pools to AsyncSession

TODO PM-058: ASYNCPG CONCURRENCY ISSUE
Tests using async_transaction fixture fail when run in batch due to AsyncPG
connection pool contention. Individual tests pass. Current status:
- Tests with async_session fixture: WORKING
- Tests with async_transaction fixture: FAIL in batch, PASS individually
- Error: "cannot perform operation: another operation is in progress"

Workaround: Use async_session instead of async_transaction for non-rollback tests.
"""

import json
from datetime import datetime, timedelta
from uuid import uuid4

import pytest
from sqlalchemy import select

from services.database.models import UploadedFileDB
from services.database.session_factory import AsyncSessionFactory
from services.domain.models import UploadedFile
from services.repositories.file_repository import FileRepository


async def test_file_repository_with_async_session(async_transaction):
    """Test that FileRepository works with AsyncSession following AsyncSessionFactory pattern"""
    # Arrange
    test_file = UploadedFile(
        id=str(uuid4()),
        session_id="test_session_123",
        filename="test_document.pdf",
        file_type="application/pdf",
        file_size=1024,
        storage_path="/uploads/test_document.pdf",
        upload_time=datetime.now(),
        last_referenced=datetime.now(),
        reference_count=0,
        metadata={"test": "data"},
    )

    # Act - Save file using AsyncSessionFactory pattern
    async with async_transaction as session:
        repo = FileRepository(session)
        saved_file = await repo.save_file_metadata(test_file)

        # Assert - Verify saved
        assert saved_file.id == test_file.id
        assert saved_file.filename == test_file.filename
        assert saved_file.session_id == test_file.session_id


async def test_get_file_by_id(async_transaction):
    """Test retrieving file by ID using AsyncSession"""
    # Arrange
    file_id = str(uuid4())
    test_file = UploadedFile(
        id=file_id,
        session_id="test_session_456",
        filename="report.xlsx",
        file_type="application/vnd.ms-excel",
        file_size=2048,
        storage_path="/uploads/report.xlsx",
        upload_time=datetime.now(),
        last_referenced=datetime.now(),
        reference_count=0,
        metadata={},
    )

    async with async_transaction as session:
        repo = FileRepository(session)
        # Save file first
        await repo.save_file_metadata(test_file)

        # Act - Retrieve file
        retrieved_file = await repo.get_file_by_id(file_id)

        # Assert
        assert retrieved_file is not None
        assert retrieved_file.id == file_id
        assert retrieved_file.filename == "report.xlsx"
        assert retrieved_file.file_type == "application/vnd.ms-excel"
        assert retrieved_file.file_size == 2048


async def test_get_files_for_session(async_transaction):
    """Test listing files for a session using AsyncSession"""
    async with async_transaction as session:
        repo = FileRepository(session)

        # Arrange
        session_id = "test_session_789"

        # Create multiple files for the session
        files = []
        for i in range(3):
            file = UploadedFile(
                id=str(uuid4()),
                session_id=session_id,
                filename=f"file_{i}.txt",
                file_type="text/plain",
                file_size=100 * (i + 1),
                storage_path=f"/uploads/file_{i}.txt",
                upload_time=datetime.now() - timedelta(minutes=i),
                last_referenced=datetime.now(),
                reference_count=0,
                metadata={},
            )
            files.append(file)
            await repo.save_file_metadata(file)

        # Act - Get files for session
        session_files = await repo.get_files_for_session(session_id, limit=10)

        # Assert
        assert len(session_files) == 3
        # Should be ordered by upload_time DESC (most recent first)
        assert session_files[0].filename == "file_0.txt"
        assert session_files[1].filename == "file_1.txt"
        assert session_files[2].filename == "file_2.txt"


async def test_search_files_by_name(async_transaction):
    """Test searching files by name pattern using AsyncSession"""
    async with async_transaction as session:
        repo = FileRepository(session)

        # Arrange
        session_id = "test_search_session"

        # Create files with different names
        test_files = [
            ("requirements.pdf", "application/pdf"),
            ("requirements_v2.pdf", "application/pdf"),
            ("design_doc.pdf", "application/pdf"),
            ("test_requirements.txt", "text/plain"),
        ]

        # Save files
        for filename, file_type in test_files:
            file = UploadedFile(
                id=str(uuid4()),
                session_id=session_id,
                filename=filename,
                file_type=file_type,
                file_size=1000,
                storage_path=f"/uploads/{filename}",
                upload_time=datetime.now(),
                last_referenced=datetime.now(),
                reference_count=0,
                metadata={},
            )
            await repo.save_file_metadata(file)

        # Act - Search for files containing "requirements"
        found_files = await repo.search_files_by_name(session_id, "requirements")

        # Assert
        assert len(found_files) == 3
        filenames = [f.filename for f in found_files]
        assert "requirements.pdf" in filenames
        assert "requirements_v2.pdf" in filenames
        assert "test_requirements.txt" in filenames
        assert "design_doc.pdf" not in filenames


async def test_increment_reference_count(async_transaction):
    """Test incrementing reference count using AsyncSession"""
    # Arrange
    file_id = str(uuid4())
    test_file = UploadedFile(
        id=file_id,
        session_id="ref_count_session",
        filename="important.doc",
        file_type="application/msword",
        file_size=5000,
        storage_path="/uploads/important.doc",
        upload_time=datetime.now() - timedelta(hours=1),
        last_referenced=datetime.now() - timedelta(hours=1),
        reference_count=0,
        metadata={},
    )

    async with async_transaction as session:
        repo = FileRepository(session)

        # Save the file first
        await repo.save_file_metadata(test_file)

        # Act - Increment reference count
        await repo.increment_reference_count(file_id)

        # Assert
        updated_file = await repo.get_file_by_id(file_id)
        assert updated_file.reference_count == 1
        assert updated_file.last_referenced > test_file.last_referenced


async def test_delete_file(async_transaction):
    """Test deleting file using AsyncSession"""
    # Arrange
    file_id = str(uuid4())
    test_file = UploadedFile(
        id=file_id,
        session_id="delete_test_session",
        filename="to_delete.tmp",
        file_type="application/octet-stream",
        file_size=100,
        storage_path="/uploads/to_delete.tmp",
        upload_time=datetime.now(),
        last_referenced=datetime.now(),
        reference_count=0,
        metadata={},
    )

    async with async_transaction as session:
        repo = FileRepository(session)

        # Save the file first
        await repo.save_file_metadata(test_file)

        # Verify file exists
        assert await repo.get_file_by_id(file_id) is not None

        # Act - Delete file
        deleted = await repo.delete_file(file_id)

        # Assert
        assert deleted is True
        assert await repo.get_file_by_id(file_id) is None


async def test_repository_inherits_from_base(async_session):
    """Test that FileRepository follows BaseRepository pattern"""
    from services.database.repositories import BaseRepository

    # Assert FileRepository inherits from BaseRepository
    async with async_session as session:
        repo = FileRepository(session)
        assert isinstance(repo, BaseRepository)
        assert hasattr(repo, "session")
        assert repo.session == session


async def test_file_repository_returns_domain_models(async_transaction):
    """Test that all repository methods return domain models, not DB models"""
    # Arrange
    test_file = UploadedFile(
        id=str(uuid4()),
        session_id="domain_test_session",
        filename="domain_test.pdf",
        file_type="application/pdf",
        file_size=1024,
        storage_path="/uploads/domain_test.pdf",
        upload_time=datetime.now(),
        last_referenced=datetime.now(),
        reference_count=0,
        metadata={"key": "value"},
    )

    # Act & Assert - All methods should return domain models
    async with async_transaction as session:
        repo = FileRepository(session)

        saved = await repo.save_file_metadata(test_file)
        assert isinstance(saved, UploadedFile)
        assert not isinstance(saved, UploadedFileDB)

        retrieved = await repo.get_file_by_id(test_file.id)
        assert isinstance(retrieved, UploadedFile)
        assert not isinstance(retrieved, UploadedFileDB)

        session_files = await repo.get_files_for_session(test_file.session_id)
        for file in session_files:
            assert isinstance(file, UploadedFile)
            assert not isinstance(file, UploadedFileDB)
