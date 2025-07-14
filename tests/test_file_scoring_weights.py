from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from services.domain.models import Intent, IntentCategory, UploadedFile
from services.file_context.file_resolver import FileResolver
from services.repositories.file_repository import FileRepository


@pytest.mark.asyncio
async def test_scoring_weight_distribution(db_session):
    """Validate that scoring weights produce good distribution"""
    session_id = f"test_weights_{uuid4().hex}"
    repo = FileRepository(db_session)
    resolver = FileResolver(repo)

    # Create test scenarios
    test_cases = [
        # (filename, file_type, age_minutes, expected_score_range)
        ("exact_match.pdf", "application/pdf", 5, (0.7, 1.0)),  # High
        ("partial_match.pdf", "application/pdf", 30, (0.4, 0.7)),  # Medium
        ("no_match.xlsx", "application/vnd.ms-excel", 120, (0.0, 0.3)),  # Low
    ]

    for filename, file_type, age_minutes, expected_range in test_cases:
        file = UploadedFile(
            session_id=session_id,
            filename=filename,
            file_type=file_type,
            file_size=1000,
            storage_path=f"/test/{filename}",
            upload_time=datetime.now() - timedelta(minutes=age_minutes),
        )
        await repo.save_file_metadata(file)

    # Test with intent that matches "exact_match"
    intent = Intent(
        category=IntentCategory.ANALYSIS,
        action="analyze_report",
        context={"original_message": "analyze exact_match"},
    )

    # Get all files and their scores
    files = await repo.get_files_for_session(session_id)
    scores = []
    for file in files:
        score = resolver._calculate_score(file, intent)
        scores.append((file.filename, score))

        # Verify score is in expected range
        for test_name, _, _, expected in test_cases:
            if file.filename == test_name:
                assert (
                    expected[0] <= score <= expected[1]
                ), f"{test_name} score {score} not in range {expected}"

    # Verify good distribution (scores should be spread out)
    score_values = [s[1] for s in scores]
    score_spread = max(score_values) - min(score_values)
    assert score_spread > 0.4, "Scores not well distributed"


@pytest.mark.asyncio
async def test_scoring_component_breakdown(db_session):
    """Test individual scoring components work correctly"""
    session_id = f"test_components_{uuid4().hex}"
    repo = FileRepository(db_session)
    resolver = FileResolver(repo)

    # Create a test file
    file = UploadedFile(
        session_id=session_id,
        filename="test_report.pdf",
        file_type="application/pdf",
        file_size=1000,
        storage_path="/test/test_report.pdf",
        upload_time=datetime.now() - timedelta(minutes=10),
    )
    await repo.save_file_metadata(file)

    intent = Intent(
        category=IntentCategory.ANALYSIS,
        action="analyze_report",
        context={"original_message": "analyze the report"},
    )

    # Test individual scoring components
    recency_score = resolver._calculate_recency_score(file.upload_time)
    type_score = resolver._calculate_type_score(file.file_type, intent.action)
    name_score = resolver._calculate_name_score(file.filename, intent)
    usage_score = resolver._calculate_usage_score(file)

    # Verify each component produces reasonable scores
    assert 0.0 <= recency_score <= 1.0, f"Recency score {recency_score} out of range"
    assert 0.0 <= type_score <= 1.0, f"Type score {type_score} out of range"
    assert 0.0 <= name_score <= 1.0, f"Name score {name_score} out of range"
    assert 0.0 <= usage_score <= 1.0, f"Usage score {usage_score} out of range"

    # Verify recent files get higher recency scores
    assert recency_score > 0.5, f"Recent file should have high recency score, got {recency_score}"

    # Verify PDF files get higher type scores for analysis
    assert type_score > 0.5, f"PDF should have high type score for analysis, got {type_score}"


@pytest.mark.asyncio
async def test_scoring_with_different_intent_types(db_session):
    """Test scoring varies appropriately with different intent types"""
    session_id = f"test_intents_{uuid4().hex}"
    repo = FileRepository(db_session)
    resolver = FileResolver(repo)

    # Create files of different types
    files = [
        UploadedFile(
            session_id=session_id,
            filename="data.csv",
            file_type="text/csv",
            file_size=1000,
            storage_path="/test/data.csv",
            upload_time=datetime.now(),
        ),
        UploadedFile(
            session_id=session_id,
            filename="report.pdf",
            file_type="application/pdf",
            file_size=1000,
            storage_path="/test/report.pdf",
            upload_time=datetime.now(),
        ),
        UploadedFile(
            session_id=session_id,
            filename="presentation.pptx",
            file_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            file_size=1000,
            storage_path="/test/presentation.pptx",
            upload_time=datetime.now(),
        ),
    ]

    for file in files:
        await repo.save_file_metadata(file)

    # Test different intent types
    intent_types = [
        ("analyze_data", "data.csv", "CSV should score high for data analysis"),
        ("analyze_report", "report.pdf", "PDF should score high for report analysis"),
        (
            "create_presentation",
            "presentation.pptx",
            "PPTX should score high for presentation creation",
        ),
    ]

    for intent_action, expected_best_file, description in intent_types:
        intent = Intent(
            category=IntentCategory.ANALYSIS,
            action=intent_action,
            context={"original_message": f"perform {intent_action}"},
        )

        # Get scores for all files
        file_scores = []
        for file in files:
            score = resolver._calculate_score(file, intent)
            file_scores.append((file.filename, score))

        # Find the highest scoring file
        best_file = max(file_scores, key=lambda x: x[1])

        # Verify the expected file scores highest
        assert (
            best_file[0] == expected_best_file
        ), f"{description}: expected {expected_best_file}, got {best_file[0]} with score {best_file[1]}"


@pytest.mark.asyncio
async def test_scoring_edge_cases(db_session):
    """Test scoring handles edge cases gracefully"""
    session_id = f"test_edge_{uuid4().hex}"
    repo = FileRepository(db_session)
    resolver = FileResolver(repo)

    # Test with very old file
    old_file = UploadedFile(
        session_id=session_id,
        filename="ancient.pdf",
        file_type="application/pdf",
        file_size=1000,
        storage_path="/test/ancient.pdf",
        upload_time=datetime.now() - timedelta(days=365),  # 1 year old
    )
    await repo.save_file_metadata(old_file)

    intent = Intent(
        category=IntentCategory.ANALYSIS,
        action="analyze_report",
        context={"original_message": "analyze the report"},
    )

    # Very old file should have low recency score but not crash
    score = resolver._calculate_score(old_file, intent)
    assert 0.0 <= score <= 1.0, f"Old file score {score} out of range"
    assert score < 0.5, f"Very old file should have low score, got {score}"

    # Test with unknown file type
    unknown_file = UploadedFile(
        session_id=session_id,
        filename="unknown.xyz",
        file_type="application/unknown",
        file_size=1000,
        storage_path="/test/unknown.xyz",
        upload_time=datetime.now(),
    )
    await repo.save_file_metadata(unknown_file)

    # Unknown file type should not crash
    score = resolver._calculate_score(unknown_file, intent)
    assert 0.0 <= score <= 1.0, f"Unknown file type score {score} out of range"
