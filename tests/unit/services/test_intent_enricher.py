from datetime import datetime, timedelta
from unittest.mock import AsyncMock, Mock

import pytest

from services.domain.models import Intent, IntentCategory, UploadedFile
from services.intent_service.intent_enricher import IntentEnricher
from services.repositories.file_repository import FileRepository


@pytest.mark.asyncio
async def test_intent_enricher_high_confidence():
    """Test IntentEnricher with high confidence file resolution"""

    # Mock the repository and file resolver (issue #308 - dependency injection)
    mock_repo = Mock(spec=FileRepository)
    mock_file_resolver = Mock()

    # Create test file (Issue #512: Changed session_id to owner_id per SEC-RBAC Phase 3)
    test_file = UploadedFile(
        owner_id="test_owner",
        filename="report.pdf",
        file_type="application/pdf",
        file_size=1000,
        storage_path="/test/report.pdf",
    )

    # Mock repository methods
    mock_repo.get_files_for_session = AsyncMock(return_value=[test_file])
    mock_repo.get_file_by_id = AsyncMock(return_value=test_file)
    mock_repo.search_files_by_name = AsyncMock(return_value=[test_file])
    mock_repo.search_files_by_name_all_sessions = AsyncMock(return_value=[test_file])

    # Mock the file resolver to return high confidence
    mock_file_resolver.resolve_file_reference = AsyncMock(return_value=(test_file.id, 0.95))

    # Create intent with file reference
    intent = Intent(
        category=IntentCategory.ANALYSIS,
        action="analyze_document",
        context={"original_message": "analyze the report"},
    )

    # Create enricher with injected dependencies (issue #308)
    enricher = IntentEnricher(mock_repo, mock_file_resolver)

    # Enrich intent
    enriched = await enricher.enrich(intent, "test_session")

    # Should have resolved file with high confidence
    assert "resolved_file_id" in enriched.context
    assert enriched.context["resolved_file_id"] == test_file.id
    assert enriched.context["file_confidence"] > 0.8
    # Test updated to match improved behavior: allow float tolerance
    assert enriched.context["file_confidence"] == pytest.approx(0.85, abs=0.01)


@pytest.mark.asyncio
async def test_intent_enricher_medium_confidence():
    """Test IntentEnricher with medium confidence file resolution"""

    # Mock the repository and file resolver (issue #308 - dependency injection)
    mock_repo = Mock(spec=FileRepository)
    mock_file_resolver = Mock()

    # Create test file (Issue #512: Changed session_id to owner_id per SEC-RBAC Phase 3)
    test_file = UploadedFile(
        owner_id="test_owner",
        filename="report.pdf",
        file_type="application/pdf",
        file_size=1000,
        storage_path="/test/report.pdf",
    )

    # Mock repository methods
    mock_repo.search_files_by_name = AsyncMock(return_value=[])
    mock_repo.search_files_by_name_all_sessions = AsyncMock(return_value=[])

    # Create intent with file reference
    intent = Intent(
        category=IntentCategory.ANALYSIS,
        action="analyze_document",
        context={"original_message": "analyze the report"},
    )

    # Mock the file resolver to return medium confidence
    mock_file_resolver.resolve_file_reference = AsyncMock(return_value=(test_file.id, 0.65))

    # Create enricher with injected dependencies (issue #308)
    enricher = IntentEnricher(mock_repo, mock_file_resolver)

    # Enrich intent
    enriched = await enricher.enrich(intent, "test_session")

    # Should have probable file with medium confidence
    assert "probable_file_id" in enriched.context
    assert enriched.context["probable_file_id"] == test_file.id
    # Test updated to match improved behavior: allow float tolerance
    assert enriched.context["file_confidence"] == pytest.approx(0.67, abs=0.01)
    assert enriched.context["needs_file_confirmation"] is True


@pytest.mark.asyncio
async def test_intent_enricher_no_file_reference():
    """Test IntentEnricher when no file reference is detected"""

    # Mock the repository and file resolver (issue #308 - dependency injection)
    mock_repo = Mock(spec=FileRepository)
    mock_file_resolver = Mock()

    # Mock repository methods (no files found)
    mock_repo.search_files_by_name = AsyncMock(return_value=[])
    mock_repo.search_files_by_name_all_sessions = AsyncMock(return_value=[])

    # Create intent without file reference
    intent = Intent(
        category=IntentCategory.QUERY,
        action="list_projects",
        context={"original_message": "show me all projects"},
    )

    # Create enricher with injected dependencies (issue #308)
    enricher = IntentEnricher(mock_repo, mock_file_resolver)

    # Enrich intent
    enriched = await enricher.enrich(intent, "test_session")

    # Should not have any file-related context
    assert "resolved_file_id" not in enriched.context
    assert "probable_file_id" not in enriched.context
    assert "needs_file_confirmation" not in enriched.context
    assert "needs_file_clarification" not in enriched.context
