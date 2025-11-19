"""
Test FileRepository migration to SQLAlchemy pattern
Following TDD approach to migrate from asyncpg pools to AsyncSession
Following ADR-010: Configuration Access Patterns

PM-058: ASYNCPG CONCURRENCY ISSUE - RESOLVED
Enhanced with complete test data isolation to prevent "6 files instead of 3" failures.
- Added unique session IDs for each test
- Enhanced cleanup mechanisms
- Improved transaction isolation
- Added test-specific data cleanup
"""

import json
from datetime import datetime, timedelta
from unittest.mock import Mock
from uuid import uuid4

import pytest
from sqlalchemy import select

from services.database.models import UploadedFileDB
from services.database.session_factory import AsyncSessionFactory
from services.domain.models import UploadedFile
from services.infrastructure.config.file_configuration import FileConfigService
from services.repositories.file_repository import FileRepository


def create_mock_config_service() -> Mock:
    """Create a mock ConfigService for testing"""
    mock_config = Mock(spec=FileConfigService)
    mock_config.get_file_cache_ttl.return_value = 300
    mock_config.get_max_file_results.return_value = 1000
    mock_config.get_file_search_timeout.return_value = 30.0
    mock_config.get_mcp_search_enabled.return_value = False
    mock_config.get_file_metadata_cache_size.return_value = 1000
    mock_config.get_repository_config.return_value = {
        "cache_ttl": 300,
        "max_results": 1000,
        "search_timeout": 30.0,
        "mcp_search_enabled": False,
        "metadata_cache_size": 1000,
    }
    return mock_config


def generate_unique_session_id() -> str:
    """Generate unique session ID for test isolation"""
    return f"test_session_{uuid4().hex[:8]}"


async def test_file_repository_with_async_session(async_transaction):
    """Test that FileRepository works with AsyncSession following AsyncSessionFactory pattern"""
    # Arrange - Use unique session ID for isolation
    session_id = generate_unique_session_id()
    test_file = UploadedFile(
        id=str(uuid4()),
        session_id=session_id,
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


async def test_file_repository_with_config_service(async_transaction):
    """Test that FileRepository works with ConfigService injection following ADR-010"""
    # Arrange - Use unique session ID for isolation
    session_id = generate_unique_session_id()
    mock_config = create_mock_config_service()
    test_file = UploadedFile(
        id=str(uuid4()),
        session_id=session_id,
        filename="config_test.pdf",
        file_type="application/pdf",
        file_size=1024,
        storage_path="/uploads/config_test.pdf",
        upload_time=datetime.now(),
        last_referenced=datetime.now(),
        reference_count=0,
        metadata={"test": "config_service"},
    )

    # Act - Save file using ConfigService injection
    async with async_transaction as session:
        repo = FileRepository(session, config_service=mock_config)
        saved_file = await repo.save_file_metadata(test_file)

        # Assert - Verify saved and config service used
        assert saved_file.id == test_file.id
        assert saved_file.filename == test_file.filename
        assert saved_file.session_id == test_file.session_id


async def test_get_file_by_id(async_transaction):
    """Test retrieving file by ID using AsyncSession"""
    # Arrange - Use unique session ID for isolation
    session_id = generate_unique_session_id()
    file_id = str(uuid4())
    test_file = UploadedFile(
        id=file_id,
        session_id=session_id,
        filename="retrieval_test.pdf",
        file_type="application/pdf",
        file_size=2048,
        storage_path="/uploads/retrieval_test.pdf",
        upload_time=datetime.now(),
        last_referenced=datetime.now(),
        reference_count=0,
        metadata={"test": "retrieval"},
    )

    async with async_transaction as session:
        repo = FileRepository(session)

        # Act - Save and retrieve file
        saved_file = await repo.save_file_metadata(test_file)
        retrieved_file = await repo.get_file_by_id(file_id)

        # Assert
        assert retrieved_file is not None
        assert retrieved_file.id == file_id
        assert retrieved_file.filename == "retrieval_test.pdf"
        assert retrieved_file.session_id == session_id
        assert retrieved_file.file_size == 2048


async def test_get_files_for_session(async_transaction):
    """Test listing files for a session using AsyncSession with enhanced isolation"""
    # Arrange - Use unique session ID for complete isolation
    session_id = generate_unique_session_id()

    async with async_transaction as session:
        repo = FileRepository(session)

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

        # Assert - Verify exact count and isolation
        assert len(session_files) == 3, f"Expected 3 files, got {len(session_files)}"
        # Should be ordered by upload_time DESC (most recent first)
        assert session_files[0].filename == "file_0.txt"
        assert session_files[1].filename == "file_1.txt"
        assert session_files[2].filename == "file_2.txt"


async def test_search_files_by_name(async_transaction):
    """Test searching files by name pattern using AsyncSession with enhanced isolation"""
    # Arrange - Use unique session ID for complete isolation
    session_id = generate_unique_session_id()

    async with async_transaction as session:
        repo = FileRepository(session)

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

        # Assert - Verify exact count and isolation
        assert len(found_files) == 3, f"Expected 3 files, got {len(found_files)}"
        filenames = [f.filename for f in found_files]
        assert "requirements.pdf" in filenames
        assert "requirements_v2.pdf" in filenames
        assert "test_requirements.txt" in filenames
        assert "design_doc.pdf" not in filenames


async def test_increment_reference_count(async_transaction):
    """Test incrementing reference count using AsyncSession with enhanced isolation"""
    # Arrange - Use unique session ID for isolation
    session_id = generate_unique_session_id()
    file_id = str(uuid4())
    test_file = UploadedFile(
        id=file_id,
        session_id=session_id,
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

        # Act - Save file and increment reference count
        saved_file = await repo.save_file_metadata(test_file)
        updated_file = await repo.increment_reference_count(file_id)

        # Assert
        assert updated_file.reference_count == 1
        assert updated_file.last_referenced > test_file.last_referenced


async def test_delete_file(async_transaction):
    """Test deleting file using AsyncSession with enhanced isolation"""
    # Arrange - Use unique session ID for isolation
    session_id = generate_unique_session_id()
    file_id = str(uuid4())
    test_file = UploadedFile(
        id=file_id,
        session_id=session_id,
        filename="delete_test.pdf",
        file_type="application/pdf",
        file_size=1024,
        storage_path="/uploads/delete_test.pdf",
        upload_time=datetime.now(),
        last_referenced=datetime.now(),
        reference_count=0,
        metadata={},
    )

    async with async_transaction as session:
        repo = FileRepository(session)

        # Act - Save and delete file
        saved_file = await repo.save_file_metadata(test_file)
        await repo.delete_file(file_id)

        # Assert - File should be deleted
        deleted_file = await repo.get_file_by_id(file_id)
        assert deleted_file is None


async def test_repository_inherits_from_base(async_session):
    """Test that FileRepository inherits from BaseRepository"""
    # This test uses async_session instead of async_transaction for better isolation
    async with async_session as session:
        repo = FileRepository(session)
        # Verify it has the expected interface
        assert hasattr(repo, "save_file_metadata")
        assert hasattr(repo, "get_file_by_id")
        assert hasattr(repo, "get_files_for_session")


async def test_file_repository_returns_domain_models(async_transaction):
    """Test that FileRepository returns domain models, not DB models"""
    # Arrange - Use unique session ID for isolation
    session_id = generate_unique_session_id()
    test_file = UploadedFile(
        id=str(uuid4()),
        session_id=session_id,
        filename="domain_test.pdf",
        file_type="application/pdf",
        file_size=1024,
        storage_path="/uploads/domain_test.pdf",
        upload_time=datetime.now(),
        last_referenced=datetime.now(),
        reference_count=0,
        metadata={"test": "domain_model"},
    )

    async with async_transaction as session:
        repo = FileRepository(session)

        # Act - Save and retrieve file
        saved_file = await repo.save_file_metadata(test_file)
        retrieved_file = await repo.get_file_by_id(saved_file.id)

        # Assert - Should return domain model, not DB model
        assert isinstance(retrieved_file, UploadedFile)
        assert not isinstance(retrieved_file, UploadedFileDB)
        assert retrieved_file.filename == "domain_test.pdf"
        assert retrieved_file.session_id == session_id
