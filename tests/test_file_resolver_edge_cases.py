import asyncio
from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from services.domain.models import Intent, IntentCategory, UploadedFile
from services.file_context.exceptions import AmbiguousFileReferenceError
from services.file_context.file_resolver import FileResolver
from services.repositories.file_repository import FileRepository


# NOTE: Use db_session_factory for fresh sessions per operation (2025-07-14)
# This prevents asyncpg/SQLAlchemy concurrency errors. See conftest.py for details.
class TestFileResolverEdgeCases:

    @pytest.mark.asyncio
    async def test_no_files_in_session(self, db_session_factory):
        """Test when user references files but none uploaded"""
        async with await db_session_factory() as session:
            resolver = FileResolver(FileRepository(session))
            intent = Intent(
                category=IntentCategory.ANALYSIS,
                action="analyze_document",
                context={"original_message": "analyze the report"},
            )
            file_id, confidence = await resolver.resolve_file_reference(
                intent, f"empty_session_{uuid4().hex}"
            )
            assert file_id is None
            assert confidence == 0.0

    @pytest.mark.asyncio
    async def test_very_old_file_scoring(self, db_session_factory):
        """Test that very old files score lower than recent ones"""
        session_id = f"test_old_{uuid4().hex}"
        old_file = UploadedFile(
            session_id=session_id,
            filename="old_report.pdf",
            file_type="application/pdf",
            file_size=1000,
            storage_path="/test/old_report.pdf",
            upload_time=datetime.now() - timedelta(days=7),  # 1 week old
        )
        recent_file = UploadedFile(
            session_id=session_id,
            filename="recent_report.pdf",
            file_type="application/pdf",
            file_size=1000,
            storage_path="/test/recent_report.pdf",
            upload_time=datetime.now() - timedelta(minutes=5),
        )
        async with await db_session_factory() as session:
            repo = FileRepository(session)
            await repo.save_file_metadata(old_file)
            await repo.save_file_metadata(recent_file)
            resolver = FileResolver(repo)
            intent = Intent(
                category=IntentCategory.ANALYSIS,
                action="analyze_report",
                context={"original_message": "analyze the report"},
            )
            file_id, confidence = await resolver.resolve_file_reference(intent, session_id)
            assert file_id == recent_file.id
            assert confidence > 0.5
        await asyncio.sleep(0)

    @pytest.mark.asyncio
    async def test_identical_filenames_different_times(self, db_session_factory):
        """Test handling multiple files with same name"""
        session_id = f"test_dup_{uuid4().hex}"
        files = []
        async with await db_session_factory() as session:
            repo = FileRepository(session)
            for i in range(3):
                file = UploadedFile(
                    session_id=session_id,
                    filename="report.pdf",  # Same name
                    file_type="application/pdf",
                    file_size=1000,
                    storage_path=f"/test/report_{i}.pdf",
                    upload_time=datetime.now() - timedelta(hours=i),
                )
                saved = await repo.save_file_metadata(file)
                files.append(saved)
            resolver = FileResolver(repo)
            intent = Intent(
                category=IntentCategory.ANALYSIS,
                action="analyze_report",
                context={"original_message": "analyze the report"},
            )
            file_id, confidence = await resolver.resolve_file_reference(intent, session_id)
            assert file_id == files[0].id  # Most recent
        await asyncio.sleep(0)

    @pytest.mark.asyncio
    async def test_special_characters_in_filename(self, db_session_factory):
        """Test files with spaces, unicode, special chars"""
        session_id = f"test_special_{uuid4().hex}"
        test_files = [
            "résumé (final).pdf",
            "2024 Q3 Report - Sales & Marketing.pdf",
            "データ分析.xlsx",  # Japanese characters
            "report[v2](draft)_FINAL.docx",
        ]
        async with await db_session_factory() as session:
            repo = FileRepository(session)
            for filename in test_files:
                file = UploadedFile(
                    session_id=session_id,
                    filename=filename,
                    file_type="application/pdf",
                    file_size=1000,
                    storage_path=f"/test/{filename}",
                    upload_time=datetime.now(),
                )
                await repo.save_file_metadata(file)
            resolver = FileResolver(repo)
            intent = Intent(
                category=IntentCategory.ANALYSIS,
                action="analyze_document",
                context={"original_message": "analyze the résumé"},
            )
            file_id, confidence = await resolver.resolve_file_reference(intent, session_id)
            assert file_id is not None  # Should find the résumé file
        await asyncio.sleep(0)

    @pytest.mark.asyncio
    async def test_performance_with_many_files(self, db_session_factory):
        """Test resolution performance with many files"""
        import time

        session_id = f"test_perf_{uuid4().hex}"
        async with await db_session_factory() as session:
            repo = FileRepository(session)
            for i in range(100):
                file = UploadedFile(
                    session_id=session_id,
                    filename=f"document_{i}.pdf",
                    file_type="application/pdf",
                    file_size=1000,
                    storage_path=f"/test/document_{i}.pdf",
                    upload_time=datetime.now() - timedelta(minutes=i),
                )
                await repo.save_file_metadata(file)
            resolver = FileResolver(repo)
            intent = Intent(
                category=IntentCategory.ANALYSIS,
                action="analyze_document",
                context={"original_message": "analyze document_50"},
            )
            start_time = time.time()
            file_id, confidence = await resolver.resolve_file_reference(intent, session_id)
            elapsed = (time.time() - start_time) * 1000  # Convert to ms
            assert elapsed < 100, f"Resolution took {elapsed:.2f}ms, should be <100ms"
            assert file_id is not None
        await asyncio.sleep(0)
