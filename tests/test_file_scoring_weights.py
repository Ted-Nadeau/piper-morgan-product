import asyncio
from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from services.domain.models import Intent, IntentCategory, UploadedFile
from services.file_context.file_resolver import FileResolver
from services.repositories.file_repository import FileRepository

# NOTE: Use db_session_factory for fresh sessions per operation (2025-07-14)
# This prevents asyncpg/SQLAlchemy concurrency errors. See conftest.py for details.


@pytest.mark.asyncio
async def test_scoring_weight_distribution(db_session_factory):
    """Validate that scoring weights produce good distribution"""
    session_id = f"test_weights_{uuid4().hex}"
    for_test_files = []
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
        async with await db_session_factory() as session:
            repo = FileRepository(session)
            await repo.save_file_metadata(file)
        await asyncio.sleep(0)  # Yield to event loop to avoid asyncpg connection reuse issues
    # Test with intent that matches "exact_match"
    intent = Intent(
        category=IntentCategory.ANALYSIS,
        action="analyze_report",
        context={"original_message": "analyze exact_match"},
    )
    async with await db_session_factory() as session:
        repo = FileRepository(session)
        files = await repo.get_files_for_session(session_id)
    resolver = FileResolver(repo)
    scores = []
    for file in files:
        score = resolver._calculate_score(file, intent)
        scores.append((file.filename, score))
        for test_name, _, _, expected in test_cases:
            if file.filename == test_name:
                assert (
                    expected[0] <= score <= expected[1]
                ), f"{test_name} score {score} not in range {expected}"
    score_values = [s[1] for s in scores]
    score_spread = max(score_values) - min(score_values)
    assert score_spread > 0.4, "Scores not well distributed"


@pytest.mark.asyncio
async def test_scoring_component_breakdown(db_session_factory):
    """Test individual scoring components work correctly"""
    session_id = f"test_components_{uuid4().hex}"
    file = UploadedFile(
        session_id=session_id,
        filename="test_report.pdf",
        file_type="application/pdf",
        file_size=1000,
        storage_path="/test/test_report.pdf",
        upload_time=datetime.now() - timedelta(minutes=10),
    )
    async with await db_session_factory() as session:
        repo = FileRepository(session)
        await repo.save_file_metadata(file)
    intent = Intent(
        category=IntentCategory.ANALYSIS,
        action="analyze_report",
        context={"original_message": "analyze the report"},
    )
    resolver = FileResolver(repo)
    recency_score = resolver._calculate_recency_score(file.upload_time)
    type_score = resolver._calculate_type_score(file.file_type, intent.action)
    name_score = resolver._calculate_name_score(file.filename, intent)
    usage_score = resolver._calculate_usage_score(file)
    assert 0.0 <= recency_score <= 1.0, f"Recency score {recency_score} out of range"
    assert 0.0 <= type_score <= 1.0, f"Type score {type_score} out of range"
    assert 0.0 <= name_score <= 1.0, f"Name score {name_score} out of range"
    assert 0.0 <= usage_score <= 1.0, f"Usage score {usage_score} out of range"
    assert recency_score > 0.5, f"Recent file should have high recency score, got {recency_score}"
    assert type_score > 0.5, f"PDF should have high type score for analysis, got {type_score}"


@pytest.mark.asyncio
async def test_scoring_with_different_intent_types(db_session_factory):
    """Test scoring varies appropriately with different intent types"""
    session_id = f"test_intents_{uuid4().hex}"
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
        async with await db_session_factory() as session:
            repo = FileRepository(session)
            await repo.save_file_metadata(file)
        await asyncio.sleep(0)
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
        async with await db_session_factory() as session:
            repo = FileRepository(session)
            file_scores = []
            for file in files:
                score = FileResolver(repo)._calculate_score(file, intent)
                file_scores.append((file.filename, score))
            best_file = max(file_scores, key=lambda x: x[1])
            assert (
                best_file[0] == expected_best_file
            ), f"{description}: expected {expected_best_file}, got {best_file[0]} with score {best_file[1]}"
        await asyncio.sleep(0)


@pytest.mark.asyncio
async def test_scoring_edge_cases(db_session_factory):
    """Test scoring handles edge cases gracefully"""
    session_id = f"test_edge_{uuid4().hex}"
    old_file = UploadedFile(
        session_id=session_id,
        filename="ancient.pdf",
        file_type="application/pdf",
        file_size=1000,
        storage_path="/test/ancient.pdf",
        upload_time=datetime.now() - timedelta(days=365),  # 1 year old
    )
    async with await db_session_factory() as session:
        repo = FileRepository(session)
        await repo.save_file_metadata(old_file)
    await asyncio.sleep(0)
    intent = Intent(
        category=IntentCategory.ANALYSIS,
        action="analyze_report",
        context={"original_message": "analyze the report"},
    )
    resolver = FileResolver(repo)
    score = resolver._calculate_score(old_file, intent)
    assert 0.0 <= score <= 1.0, f"Old file score {score} out of range"
    assert score < 0.5, f"Very old file should have low score, got {score}"
    unknown_file = UploadedFile(
        session_id=session_id,
        filename="unknown.xyz",
        file_type="application/unknown",
        file_size=1000,
        storage_path="/test/unknown.xyz",
        upload_time=datetime.now(),
    )
    async with await db_session_factory() as session:
        repo = FileRepository(session)
        await repo.save_file_metadata(unknown_file)
    await asyncio.sleep(0)
    score = resolver._calculate_score(unknown_file, intent)
    assert 0.0 <= score <= 1.0, f"Unknown file type score {score} out of range"


@pytest.mark.asyncio
async def test_minimal_file_repository_operations(db_session_factory):
    """Minimal test to isolate connection pool issue"""
    from services.domain.models import UploadedFile
    from services.repositories.file_repository import FileRepository

    # Operation 1
    async with await db_session_factory() as session:
        repo = FileRepository(session)
        file1 = UploadedFile(
            session_id="test_session",
            filename="test1.txt",
            file_type="text/plain",
            file_size=100,
            storage_path="/tmp/test1.txt",
        )
        await repo.save_file_metadata(file1)

    # Operation 2 - completely separate session
    async with await db_session_factory() as session:
        repo = FileRepository(session)
        file2 = UploadedFile(
            session_id="test_session",
            filename="test2.txt",
            file_type="text/plain",
            file_size=200,
            storage_path="/tmp/test2.txt",
        )
        await repo.save_file_metadata(file2)


@pytest.mark.asyncio
async def test_minimal_file_repository_loop(db_session_factory):
    """Test with loop to find error threshold"""
    from services.domain.models import UploadedFile
    from services.repositories.file_repository import FileRepository

    for i in range(5):
        async with await db_session_factory() as session:
            repo = FileRepository(session)
            file = UploadedFile(
                session_id=f"test_session_{i}",
                filename=f"test{i}.txt",
                file_type="text/plain",
                file_size=100 * (i + 1),
                storage_path=f"/tmp/test{i}.txt"
            )
            await repo.save_file_metadata(file)
