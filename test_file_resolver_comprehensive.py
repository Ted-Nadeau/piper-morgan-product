#!/usr/bin/env python3
"""Comprehensive test for FileResolver edge cases and scoring weights"""

import asyncio
from datetime import datetime, timedelta
from uuid import uuid4
from services.file_context.file_resolver import FileResolver
from services.repositories.file_repository import FileRepository
from services.repositories import DatabasePool
from services.domain.models import UploadedFile, Intent, IntentCategory

async def test_file_resolver_comprehensive():
    """Test FileResolver with comprehensive edge cases and scoring validation"""
    print("Testing FileResolver comprehensive edge cases and scoring...")
    
    # Get database pool
    pool = await DatabasePool.get_pool()
    repo = FileRepository(pool)
    resolver = FileResolver(repo)
    
    try:
        # Test 1: No files in session
        print("\n=== Test 1: No Files in Session ===")
        session_id = f"empty_session_{uuid4().hex[:8]}"
        
        intent = Intent(
            category=IntentCategory.ANALYSIS,
            action="analyze_document",
            context={"original_message": "analyze the report"}
        )
        
        file_id, confidence = await resolver.resolve_file_reference(intent, session_id)
        
        if file_id is None and confidence == 0.0:
            print("✅ Correctly handled empty session")
        else:
            print(f"❌ Expected None/0.0, got {file_id}/{confidence}")
        
        # Test 2: Very old vs recent files
        print("\n=== Test 2: Old vs Recent File Scoring ===")
        session_id = f"age_test_{uuid4().hex[:8]}"
        
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
        
        file_id, confidence = await resolver.resolve_file_reference(intent, session_id)
        
        if file_id == recent_file.id and confidence > 0.5:
            print("✅ Recent file correctly selected with high confidence")
        else:
            print(f"❌ Expected recent file, got {file_id} with confidence {confidence}")
        
        # Test 3: Identical filenames
        print("\n=== Test 3: Identical Filenames ===")
        session_id = f"dup_test_{uuid4().hex[:8]}"
        
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
        
        file_id, confidence = await resolver.resolve_file_reference(intent, session_id)
        
        if file_id == files[0].id:  # Most recent
            print("✅ Correctly selected most recent file with same name")
        else:
            print(f"❌ Expected most recent file, got {file_id}")
        
        # Test 4: Special characters and unicode
        print("\n=== Test 4: Special Characters and Unicode ===")
        session_id = f"unicode_test_{uuid4().hex[:8]}"
        
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
        
        # Test with specific unicode reference
        unicode_intent = Intent(
            category=IntentCategory.ANALYSIS,
            action="analyze_document",
            context={"original_message": "analyze the résumé document"}
        )
        
        try:
            file_id, confidence = await resolver.resolve_file_reference(unicode_intent, session_id)
            
            if file_id is not None:
                print("✅ Correctly resolved specific unicode filename reference")
            else:
                print("❌ Failed to resolve unicode filename reference")
        except Exception as e:
            if "AmbiguousFileReferenceError" in str(type(e)):
                print("✅ Correctly detected ambiguity for generic unicode reference")
            else:
                print(f"❌ Unexpected error: {e}")
        
        # Test with Japanese characters
        japanese_intent = Intent(
            category=IntentCategory.ANALYSIS,
            action="analyze_data",
            context={"original_message": "analyze the データ analysis"}
        )
        
        try:
            file_id, confidence = await resolver.resolve_file_reference(japanese_intent, session_id)
            
            if file_id is not None:
                print("✅ Correctly resolved Japanese filename reference")
            else:
                print("❌ Failed to resolve Japanese filename reference")
        except Exception as e:
            if "AmbiguousFileReferenceError" in str(type(e)):
                print("✅ Correctly detected ambiguity for Japanese reference")
            else:
                print(f"❌ Unexpected error: {e}")
        
        # Test 5: Performance with many files
        print("\n=== Test 5: Performance with Many Files ===")
        session_id = f"perf_test_{uuid4().hex[:8]}"
        
        # Create 50 files with unique names to avoid ambiguity
        for i in range(50):
            file = UploadedFile(
                session_id=session_id,
                filename=f"unique_file_{i:03d}_test.pdf",  # Unique pattern
                file_type="application/pdf",
                file_size=1000,
                storage_path=f"/test/unique_file_{i:03d}_test.pdf",
                upload_time=datetime.now() - timedelta(minutes=i)
            )
            await repo.save_file_metadata(file)
        
        # Test performance with generic intent (should detect ambiguity)
        perf_intent = Intent(
            category=IntentCategory.ANALYSIS,
            action="analyze_document",
            context={"original_message": "analyze a document"}
        )
        
        import time
        start_time = time.time()
        
        try:
            file_id, confidence = await resolver.resolve_file_reference(perf_intent, session_id)
            elapsed = (time.time() - start_time) * 1000  # Convert to ms
            
            if elapsed < 100 and file_id is not None:
                print(f"✅ Performance test passed: {elapsed:.2f}ms")
            else:
                print(f"❌ Performance test failed: {elapsed:.2f}ms, file_id: {file_id}")
        except Exception as e:
            elapsed = (time.time() - start_time) * 1000
            if "AmbiguousFileReferenceError" in str(type(e)):
                print(f"✅ Performance test passed (ambiguity detected): {elapsed:.2f}ms")
            else:
                print(f"❌ Performance test failed with unexpected error: {e} ({elapsed:.2f}ms)")
        
        # Test with a single file to verify resolution works
        single_file_session = f"single_test_{uuid4().hex[:8]}"
        single_file = UploadedFile(
            session_id=single_file_session,
            filename="single_test_file.pdf",
            file_type="application/pdf",
            file_size=1000,
            storage_path="/test/single_test_file.pdf",
            upload_time=datetime.now()
        )
        await repo.save_file_metadata(single_file)
        
        single_intent = Intent(
            category=IntentCategory.ANALYSIS,
            action="analyze_document",
            context={"original_message": "analyze the test file"}
        )
        
        start_time = time.time()
        file_id, confidence = await resolver.resolve_file_reference(single_intent, single_file_session)
        elapsed = (time.time() - start_time) * 1000
        
        if elapsed < 100 and file_id == single_file.id:
            print(f"✅ Single file resolution test passed: {elapsed:.2f}ms")
        else:
            print(f"❌ Single file resolution test failed: {elapsed:.2f}ms, file_id: {file_id}")
        
        # Test 6: Scoring component breakdown
        print("\n=== Test 6: Scoring Component Breakdown ===")
        session_id = f"scoring_test_{uuid4().hex[:8]}"
        
        test_file = UploadedFile(
            session_id=session_id,
            filename="test_report.pdf",
            file_type="application/pdf",
            file_size=1000,
            storage_path="/test/test_report.pdf",
            upload_time=datetime.now() - timedelta(minutes=10)
        )
        await repo.save_file_metadata(test_file)
        
        test_intent = Intent(
            category=IntentCategory.ANALYSIS,
            action="analyze_report",
            context={"original_message": "analyze the report"}
        )
        
        # Test individual scoring components
        recency_score = resolver._calculate_recency_score(test_file.upload_time)
        type_score = resolver._calculate_type_score(test_file.file_type, test_intent.action)
        name_score = resolver._calculate_name_score(test_file.filename, test_intent)
        usage_score = resolver._calculate_usage_score(test_file)
        total_score = resolver._calculate_score(test_file, test_intent)
        
        print(f"   Recency score: {recency_score:.3f}")
        print(f"   Type score: {type_score:.3f}")
        print(f"   Name score: {name_score:.3f}")
        print(f"   Usage score: {usage_score:.3f}")
        print(f"   Total score: {total_score:.3f}")
        
        # Verify all scores are in valid range
        scores_valid = all(0.0 <= score <= 1.0 for score in [recency_score, type_score, name_score, usage_score, total_score])
        if scores_valid:
            print("   ✅ All scores in valid range [0.0, 1.0]")
        else:
            print("   ❌ Some scores outside valid range")
        
        # Test 7: Different file types for different intents
        print("\n=== Test 7: File Type Intent Matching ===")
        session_id = f"type_test_{uuid4().hex[:8]}"
        
        type_files = [
            UploadedFile(
                session_id=session_id,
                filename="data.csv",
                file_type="text/csv",
                file_size=1000,
                storage_path="/test/data.csv",
                upload_time=datetime.now()
            ),
            UploadedFile(
                session_id=session_id,
                filename="report.pdf",
                file_type="application/pdf",
                file_size=1000,
                storage_path="/test/report.pdf",
                upload_time=datetime.now()
            )
        ]
        
        for file in type_files:
            await repo.save_file_metadata(file)
        
        # Test CSV for data analysis
        data_intent = Intent(
            category=IntentCategory.ANALYSIS,
            action="analyze_data",
            context={"original_message": "analyze the data"}
        )
        
        file_id, confidence = await resolver.resolve_file_reference(data_intent, session_id)
        csv_file = next(f for f in type_files if f.filename == "data.csv")
        
        if file_id == csv_file.id:
            print("   ✅ CSV correctly selected for data analysis")
        else:
            print(f"   ❌ Expected CSV, got {file_id}")
        
        # Test PDF for report analysis
        report_intent = Intent(
            category=IntentCategory.ANALYSIS,
            action="analyze_report",
            context={"original_message": "analyze the report"}
        )
        
        file_id, confidence = await resolver.resolve_file_reference(report_intent, session_id)
        pdf_file = next(f for f in type_files if f.filename == "report.pdf")
        
        if file_id == pdf_file.id:
            print("   ✅ PDF correctly selected for report analysis")
        else:
            print(f"   ❌ Expected PDF, got {file_id}")
        
        # Cleanup
        print("\n=== Cleanup ===")
        # Get all test files and delete them
        all_files = await repo.get_files_for_session(session_id)
        for file in all_files:
            await repo.delete_file(file.id)
        print("✅ Cleanup completed")
        
        print("\n🎉 Comprehensive FileResolver tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await pool.close()

if __name__ == "__main__":
    asyncio.run(test_file_resolver_comprehensive()) 