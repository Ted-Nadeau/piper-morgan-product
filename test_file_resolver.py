#!/usr/bin/env python3
"""Comprehensive test for FileResolver scoring algorithm"""

import asyncio
from datetime import datetime, timedelta
from uuid import uuid4

from services.domain.models import Intent, IntentCategory, UploadedFile
from services.file_context.file_resolver import FileResolver
from services.repositories import DatabasePool
from services.repositories.file_repository import FileRepository


async def test_file_resolver():
    """Test FileResolver with various scenarios"""
    print("Testing FileResolver scoring algorithm...")

    # Get database pool
    pool = await DatabasePool.get_pool()
    repo = FileRepository(pool)
    resolver = FileResolver(repo)

    try:
        # Generate unique session ID for this test run to avoid conflicts
        session_id = f"test-resolver-session-{uuid4().hex[:8]}"
        print(f"Using unique session ID: {session_id}")

        # Create test files with different characteristics
        files = [
            # Recent PDF report (should score high for analyze_report)
            UploadedFile(
                session_id=session_id,
                filename="Q3_Sales_Report.pdf",
                file_type="application/pdf",
                file_size=1024000,
                storage_path="/tmp/Q3_Sales_Report.pdf",
                upload_time=datetime.now() - timedelta(minutes=2),  # Very recent
                reference_count=0,
            ),
            # Older CSV data (should score high for analyze_data)
            UploadedFile(
                session_id=session_id,
                filename="sales_data.csv",
                file_type="text/csv",
                file_size=512000,
                storage_path="/tmp/sales_data.csv",
                upload_time=datetime.now() - timedelta(hours=2),  # Older
                reference_count=3,  # Previously referenced
                last_referenced=datetime.now() - timedelta(hours=1),
            ),
            # Very old document (should score low)
            UploadedFile(
                session_id=session_id,
                filename="old_report.docx",
                file_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                file_size=2048000,
                storage_path="/tmp/old_report.docx",
                upload_time=datetime.now() - timedelta(days=5),  # Very old
                reference_count=1,
            ),
            # Recent spreadsheet (should score high for process_spreadsheet)
            UploadedFile(
                session_id=session_id,
                filename="Q3_Financials.xlsx",
                file_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                file_size=1536000,
                storage_path="/tmp/Q3_Financials.xlsx",
                upload_time=datetime.now() - timedelta(minutes=10),
                reference_count=0,
            ),
        ]

        # Save all files
        print("Creating test files...")
        for file in files:
            await repo.save_file_metadata(file)
            print(f"  - {file.filename} (ID: {file.id[:8]}...)")

        # Test 1: Analyze report intent (should prefer recent PDF)
        print("\n=== Test 1: Analyze Report Intent ===")
        analyze_report_intent = Intent(
            category=IntentCategory.EXECUTION,
            action="analyze_report",
            context={"keywords": ["sales", "report", "quarterly"]},
        )

        # Debug: Show all scores first
        print("Debug: All file scores for analyze_report intent:")
        all_files = await repo.get_files_for_session(session_id, limit=20)
        for file in all_files:
            score = resolver._calculate_score(file, analyze_report_intent)
            print(f"  {file.filename}: {score:.3f}")

        try:
            file_id, confidence = await resolver.resolve_file_reference(
                analyze_report_intent, session_id
            )
            resolved_file = await repo.get_file_by_id(file_id) if file_id else None

            print(f"Intent: {analyze_report_intent.action}")
            print(
                f"Resolved file: {resolved_file.filename if resolved_file else 'None'}"
            )
            print(f"Confidence: {confidence:.3f}")

            expected_file = "Q3_Sales_Report.pdf"
            if resolved_file and resolved_file.filename == expected_file:
                print("✅ Test 1 PASSED - Correctly resolved to recent PDF report")
            else:
                print(
                    f"❌ Test 1 FAILED - Expected {expected_file}, got {resolved_file.filename if resolved_file else 'None'}"
                )
        except Exception as e:
            print(f"Test 1 result: {e}")
            if "AmbiguousFileReferenceError" in str(type(e)):
                print("⚠️  Test 1: Ambiguity detected (this is expected behavior)")
            else:
                print(f"❌ Test 1 FAILED with unexpected error: {e}")

        # Test 2: Analyze data intent (should prefer CSV)
        print("\n=== Test 2: Analyze Data Intent ===")
        analyze_data_intent = Intent(
            category=IntentCategory.EXECUTION,
            action="analyze_data",
            context={"keywords": ["sales", "data", "analysis"]},
        )

        file_id, confidence = await resolver.resolve_file_reference(
            analyze_data_intent, session_id
        )
        resolved_file = await repo.get_file_by_id(file_id) if file_id else None

        print(f"Intent: {analyze_data_intent.action}")
        print(f"Resolved file: {resolved_file.filename if resolved_file else 'None'}")
        print(f"Confidence: {confidence:.3f}")

        expected_file = "sales_data.csv"
        if resolved_file and resolved_file.filename == expected_file:
            print("✅ Test 2 PASSED - Correctly resolved to CSV data file")
        else:
            print(
                f"❌ Test 2 FAILED - Expected {expected_file}, got {resolved_file.filename if resolved_file else 'None'}"
            )

        # Test 3: Process spreadsheet intent (should prefer Excel)
        print("\n=== Test 3: Process Spreadsheet Intent ===")
        process_spreadsheet_intent = Intent(
            category=IntentCategory.EXECUTION,
            action="process_spreadsheet",
            context={"keywords": ["financial", "quarterly"]},
        )

        file_id, confidence = await resolver.resolve_file_reference(
            process_spreadsheet_intent, session_id
        )
        resolved_file = await repo.get_file_by_id(file_id) if file_id else None

        print(f"Intent: {process_spreadsheet_intent.action}")
        print(f"Resolved file: {resolved_file.filename if resolved_file else 'None'}")
        print(f"Confidence: {confidence:.3f}")

        expected_file = "Q3_Financials.xlsx"
        if resolved_file and resolved_file.filename == expected_file:
            print("✅ Test 3 PASSED - Correctly resolved to Excel spreadsheet")
        else:
            print(
                f"❌ Test 3 FAILED - Expected {expected_file}, got {resolved_file.filename if resolved_file else 'None'}"
            )

        # Test 4: Generic intent (should prefer recent files)
        print("\n=== Test 4: Generic Intent ===")
        generic_intent = Intent(
            category=IntentCategory.EXECUTION,
            action="ingest_generic",
            context={"keywords": ["document", "file"]},
        )

        file_id, confidence = await resolver.resolve_file_reference(
            generic_intent, session_id
        )
        resolved_file = await repo.get_file_by_id(file_id) if file_id else None

        print(f"Intent: {generic_intent.action}")
        print(f"Resolved file: {resolved_file.filename if resolved_file else 'None'}")
        print(f"Confidence: {confidence:.3f}")

        # Should prefer recent files for generic intent
        if resolved_file and "Q3_Sales_Report.pdf" in resolved_file.filename:
            print("✅ Test 4 PASSED - Correctly resolved to most recent file")
        else:
            print(
                f"❌ Test 4 FAILED - Expected recent file, got {resolved_file.filename if resolved_file else 'None'}"
            )

        # Test 5: Scoring breakdown
        print("\n=== Test 5: Scoring Breakdown ===")
        test_file = files[0]  # Q3_Sales_Report.pdf
        test_intent = Intent(
            category=IntentCategory.EXECUTION,
            action="analyze_report",
            context={"keywords": ["sales", "report"]},
        )

        # Calculate individual scores
        recency_score = resolver._calculate_recency_score(test_file.upload_time)
        type_score = resolver._calculate_type_score(
            test_file.file_type, test_intent.action
        )
        name_score = resolver._calculate_name_score(test_file.filename, test_intent)
        usage_score = resolver._calculate_usage_score(test_file)
        total_score = resolver._calculate_score(test_file, test_intent)

        print(f"File: {test_file.filename}")
        print(f"Recency score: {recency_score:.3f}")
        print(f"Type score: {type_score:.3f}")
        print(f"Name score: {name_score:.3f}")
        print(f"Usage score: {usage_score:.3f}")
        print(f"Total score: {total_score:.3f}")

        if total_score > 0.5:
            print("✅ Test 5 PASSED - Scoring algorithm produces reasonable scores")
        else:
            print("❌ Test 5 FAILED - Scoring algorithm produced low score")

        # Test 6: Ambiguity detection
        print("\n=== Test 6: Ambiguity Detection ===")
        # Create two similar files with close scores
        similar_file1 = UploadedFile(
            session_id=session_id,
            filename="report_v1.pdf",
            file_type="application/pdf",
            file_size=1024000,
            storage_path="/tmp/report_v1.pdf",
            upload_time=datetime.now() - timedelta(minutes=1),
            reference_count=0,
        )
        similar_file2 = UploadedFile(
            session_id=session_id,
            filename="report_v2.pdf",
            file_type="application/pdf",
            file_size=1024000,
            storage_path="/tmp/report_v2.pdf",
            upload_time=datetime.now() - timedelta(minutes=2),
            reference_count=0,
        )

        await repo.save_file_metadata(similar_file1)
        await repo.save_file_metadata(similar_file2)

        ambiguous_intent = Intent(
            category=IntentCategory.EXECUTION,
            action="analyze_report",
            context={"keywords": ["report"]},
        )

        try:
            file_id, confidence = await resolver.resolve_file_reference(
                ambiguous_intent, session_id
            )
            print("❌ Test 6 FAILED - Should have detected ambiguity")
        except Exception as e:
            if "AmbiguousFileReferenceError" in str(type(e)):
                print("✅ Test 6 PASSED - Correctly detected ambiguous reference")
            else:
                print(f"❌ Test 6 FAILED - Unexpected error: {e}")

        # Clean up
        print("\nCleaning up test data...")
        for file in files + [similar_file1, similar_file2]:
            await repo.delete_file(file.id)
        print("✅ Cleanup completed")

    except Exception as e:
        print(f"❌ Test FAILED with error: {e}")
        import traceback

        traceback.print_exc()
    finally:
        await pool.close()


if __name__ == "__main__":
    asyncio.run(test_file_resolver())
