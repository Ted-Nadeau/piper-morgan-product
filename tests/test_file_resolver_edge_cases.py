import pytest
from datetime import datetime, timedelta
from services.domain.models import UploadedFile, Intent, IntentCategory
from services.file_context.file_resolver import FileResolver
from services.file_context.exceptions import AmbiguousFileReferenceError
from services.repositories.file_repository import FileRepository
from uuid import uuid4

class TestFileResolverEdgeCases:
    
    @pytest.mark.asyncio
    async def test_no_files_in_session(self, db_session):
        """Test when user references files but none uploaded"""
        resolver = FileResolver(FileRepository(db_session))
        
        intent = Intent(
            category=IntentCategory.ANALYSIS,
            action="analyze_document",
            context={"original_message": "analyze the report"}
        )
        
        # Should return None when no files exist
        file_id, confidence = await resolver.resolve_file_reference(
            intent, f"empty_session_{uuid4().hex}"
        )
        
        assert file_id is None
        assert confidence == 0.0
    
    @pytest.mark.asyncio
    async def test_very_old_file_scoring(self, db_session):
        """Test that very old files score lower than recent ones"""
        session_id = f"test_old_{uuid4().hex}"
        repo = FileRepository(db_session)
        
        # Create files with different ages
        old_file = UploadedFile(
            session_id=session_id,
            filename="old_report.pdf",
            file_type="application/pdf",
            file_size=1000,
            storage_path="/test/old_report.pdf",
            upload_time=datetime.now() - timedelta(days=7)  # 1 week old
        )
        recent_file = UploadedFile(
            session_id=session_id,
            filename="recent_report.pdf",
            file_type="application/pdf",
            file_size=1000,
            storage_path="/test/recent_report.pdf",
            upload_time=datetime.now() - timedelta(minutes=5)
        )
        
        await repo.save_file_metadata(old_file)
        await repo.save_file_metadata(recent_file)
        
        # Test resolution
        resolver = FileResolver(repo)
        intent = Intent(
            category=IntentCategory.ANALYSIS,
            action="analyze_report",
            context={"original_message": "analyze the report"}
        )
        
        file_id, confidence = await resolver.resolve_file_reference(intent, session_id)
        
        # Recent file should win
        assert file_id == recent_file.id
        assert confidence > 0.5
    
    @pytest.mark.asyncio
    async def test_identical_filenames_different_times(self, db_session):
        """Test handling multiple files with same name"""
        session_id = f"test_dup_{uuid4().hex}"
        repo = FileRepository(db_session)
        
        # Create files with same name but different upload times
        files = []
        for i in range(3):
            file = UploadedFile(
                session_id=session_id,
                filename="report.pdf",  # Same name
                file_type="application/pdf",
                file_size=1000,
                storage_path=f"/test/report_{i}.pdf",
                upload_time=datetime.now() - timedelta(hours=i)
            )
            saved = await repo.save_file_metadata(file)
            files.append(saved)
        
        resolver = FileResolver(repo)
        intent = Intent(
            category=IntentCategory.ANALYSIS,
            action="analyze_report",
            context={"original_message": "analyze the report"}
        )
        
        # Should resolve to most recent
        file_id, confidence = await resolver.resolve_file_reference(intent, session_id)
        assert file_id == files[0].id  # Most recent
    
    @pytest.mark.asyncio
    async def test_special_characters_in_filename(self, db_session):
        """Test files with spaces, unicode, special chars"""
        session_id = f"test_special_{uuid4().hex}"
        repo = FileRepository(db_session)
        
        # Create files with special characters
        test_files = [
            "résumé (final).pdf",
            "2024 Q3 Report - Sales & Marketing.pdf",
            "データ分析.xlsx",  # Japanese characters
            "report[v2](draft)_FINAL.docx"
        ]
        
        for filename in test_files:
            file = UploadedFile(
                session_id=session_id,
                filename=filename,
                file_type="application/pdf",
                file_size=1000,
                storage_path=f"/test/{filename}",
                upload_time=datetime.now()
            )
            await repo.save_file_metadata(file)
        
        # Test resolution with partial match
        resolver = FileResolver(repo)
        intent = Intent(
            category=IntentCategory.ANALYSIS,
            action="analyze_document",
            context={"original_message": "analyze the résumé"}
        )
        
        file_id, confidence = await resolver.resolve_file_reference(intent, session_id)
        assert file_id is not None  # Should find the résumé file
    
    @pytest.mark.asyncio
    async def test_performance_with_many_files(self, db_session):
        """Test resolution performance with many files"""
        import time
        
        session_id = f"test_perf_{uuid4().hex}"
        repo = FileRepository(db_session)
        
        # Create 100 files
        for i in range(100):
            file = UploadedFile(
                session_id=session_id,
                filename=f"document_{i}.pdf",
                file_type="application/pdf",
                file_size=1000,
                storage_path=f"/test/document_{i}.pdf",
                upload_time=datetime.now() - timedelta(minutes=i)
            )
            await repo.save_file_metadata(file)
        
        # Time the resolution
        resolver = FileResolver(repo)
        intent = Intent(
            category=IntentCategory.ANALYSIS,
            action="analyze_document",
            context={"original_message": "analyze document_50"}
        )
        
        start_time = time.time()
        file_id, confidence = await resolver.resolve_file_reference(intent, session_id)
        elapsed = (time.time() - start_time) * 1000  # Convert to ms
        
        # Should complete within 100ms
        assert elapsed < 100, f"Resolution took {elapsed:.2f}ms, should be <100ms"
        assert file_id is not None 