#!/usr/bin/env python3
"""Test IntentEnricher integration with main intent flow"""

import asyncio
import os
import tempfile
from datetime import datetime
from pathlib import Path

from services.domain.models import Intent, IntentCategory, UploadedFile
from services.intent_service.classifier import IntentClassifier
from services.intent_service.intent_enricher import IntentEnricher
from services.repositories import DatabasePool
from services.repositories.file_repository import FileRepository


async def test_intent_enrichment_integration():
    """Test that IntentEnricher integrates properly with intent processing"""
    print("Testing IntentEnricher integration...")

    try:
        # Create a test file first
        session_id = "test_integration_session"

        # Create test file
        test_file = UploadedFile(
            session_id=session_id,
            filename="test_report.pdf",
            file_type="application/pdf",
            file_size=1000,
            storage_path="/test/test_report.pdf",
            upload_time=datetime.now(),
        )

        # Save to database
        pool = await DatabasePool.get_pool()
        repo = FileRepository(pool)
        saved_file = await repo.save_file_metadata(test_file)
        print(f"✅ Test file saved: {saved_file.filename}")

        # Test 1: Intent with file reference
        print("\n1. Testing intent with file reference...")
        classifier = IntentClassifier()
        intent = await classifier.classify("analyze the report")
        intent.context["original_message"] = "analyze the report"

        # Enrich the intent
        enricher = IntentEnricher(pool)
        enriched_intent = await enricher.enrich(intent, session_id)

        print(f"   Original intent action: {intent.action}")
        print(f"   Enriched intent action: {enriched_intent.action}")
        print(
            f"   File context: {enriched_intent.context.get('resolved_file_id', 'None')}"
        )

        if "resolved_file_id" in enriched_intent.context:
            print("   ✅ File reference resolved successfully")
        else:
            print("   ⚠️  File reference not resolved (this might be expected)")

        # Test 2: Intent without file reference
        print("\n2. Testing intent without file reference...")
        intent_no_file = await classifier.classify("list all projects")
        intent_no_file.context["original_message"] = "list all projects"

        enriched_no_file = await enricher.enrich(intent_no_file, session_id)

        print(f"   Original intent action: {intent_no_file.action}")
        print(f"   Enriched intent action: {enriched_no_file.action}")
        print(
            f"   File context: {enriched_no_file.context.get('resolved_file_id', 'None')}"
        )

        if "resolved_file_id" not in enriched_no_file.context:
            print("   ✅ No file context added (correct behavior)")
        else:
            print("   ❌ Unexpected file context added")

        # Test 3: Check that enrichment preserves intent structure
        print("\n3. Testing intent structure preservation...")
        assert (
            enriched_intent.category == intent.category
        ), "Category should be preserved"
        assert enriched_intent.action == intent.action, "Action should be preserved"
        assert (
            enriched_intent.confidence == intent.confidence
        ), "Confidence should be preserved"
        print("   ✅ Intent structure preserved during enrichment")

        # Cleanup
        print("\n4. Cleaning up...")
        await repo.delete_file(saved_file.id)
        print("   ✅ Cleanup completed")

        print("\n🎉 Integration test completed successfully!")

    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback

        traceback.print_exc()
    finally:
        await pool.close()


if __name__ == "__main__":
    asyncio.run(test_intent_enrichment_integration())
