import asyncio
from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from services.database.models import User
from services.database.session_factory import AsyncSessionFactory
from services.domain.models import Intent, IntentCategory, UploadedFile
from services.file_context.file_resolver import FileResolver
from services.repositories.file_repository import FileRepository


async def create_test_user(session, owner_id: str) -> User:
    """
    Create a test user for file resolver tests.
    Required for SEC-RBAC owner_id foreign key constraint.
    """
    user = User(
        id=owner_id,
        username=f"test_user_{owner_id[:8]}",
        email=f"test_{owner_id[:8]}@example.com",
        role="user",
        is_active=True,
        is_verified=True,
        is_alpha=True,
    )
    session.add(user)
    await session.flush()  # Ensure user exists before file creation
    return user


@pytest.mark.asyncio
async def test_scoring_weight_distribution():
    """Validate that scoring weights produce good distribution"""
    owner_id = str(uuid4())
    for_test_files = []
    # Create test scenarios
    test_cases = [
        # (filename, file_type, age_minutes, expected_score_range)
        ("exact_match.pdf", "application/pdf", 5, (0.7, 1.0)),  # High
        ("partial_match.pdf", "application/pdf", 30, (0.4, 0.7)),  # Medium
        ("no_match.xlsx", "application/vnd.ms-excel", 120, (0.0, 0.3)),  # Low
    ]
    # Create all test files in separate transactions to avoid session conflicts
    async with AsyncSessionFactory.session_scope() as session:
        # Create test user first (SEC-RBAC requires owner_id FK)
        await create_test_user(session, owner_id)
        repo = FileRepository(session)
        for filename, file_type, age_minutes, expected_range in test_cases:
            file = UploadedFile(
                owner_id=owner_id,
                filename=filename,
                file_type=file_type,
                file_size=1000,
                storage_path=f"/test/{filename}",
                upload_time=datetime.now() - timedelta(minutes=age_minutes),
            )
            await repo.save_file_metadata(file)
        # Commit all files in one transaction
        await session.commit()
    # Test with intent that matches "exact_match"
    intent = Intent(
        category=IntentCategory.ANALYSIS,
        action="analyze_report",
        context={"original_message": "analyze exact_match"},
    )
    # Get files and test scoring in a separate session
    async with AsyncSessionFactory.session_scope() as session:
        repo = FileRepository(session)
        files = await repo.get_files_for_session(owner_id)
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


@pytest.mark.asyncio
async def test_scoring_component_breakdown():
    """Test individual scoring components work correctly"""
    owner_id = str(uuid4())
    file = UploadedFile(
        owner_id=owner_id,
        filename="test_report.pdf",
        file_type="application/pdf",
        file_size=1000,
        storage_path="/test/test_report.pdf",
        upload_time=datetime.now() - timedelta(minutes=10),
    )
    async with AsyncSessionFactory.session_scope() as session:
        # Create test user first (SEC-RBAC requires owner_id FK)
        await create_test_user(session, owner_id)
        repo = FileRepository(session)
        await repo.save_file_metadata(file)
        await session.commit()

    intent = Intent(
        category=IntentCategory.ANALYSIS,
        action="analyze_report",
        context={"original_message": "analyze the report"},
    )

    # Test scoring components in a separate session
    async with AsyncSessionFactory.session_scope() as session:
        repo = FileRepository(session)
        resolver = FileResolver(repo)
        recency_score = resolver._calculate_recency_score(file.upload_time)
        type_score = resolver._calculate_type_score(file.file_type, intent.action)
        name_score = resolver._calculate_name_score(file.filename, intent)
        usage_score = resolver._calculate_usage_score(file)
        assert 0.0 <= recency_score <= 1.0, f"Recency score {recency_score} out of range"
        assert 0.0 <= type_score <= 1.0, f"Type score {type_score} out of range"
        assert 0.0 <= name_score <= 1.0, f"Name score {name_score} out of range"
        assert 0.0 <= usage_score <= 1.0, f"Usage score {usage_score} out of range"
        assert (
            recency_score > 0.5
        ), f"Recent file should have high recency score, got {recency_score}"
        assert type_score > 0.5, f"PDF should have high type score for analysis, got {type_score}"


@pytest.mark.asyncio
async def test_scoring_with_different_intent_types():
    """Test scoring varies appropriately with different intent types"""
    owner_id = str(uuid4())
    files = [
        UploadedFile(
            owner_id=owner_id,
            filename="data.csv",
            file_type="text/csv",
            file_size=1000,
            storage_path="/test/data.csv",
            upload_time=datetime.now(),
        ),
        UploadedFile(
            owner_id=owner_id,
            filename="report.pdf",
            file_type="application/pdf",
            file_size=1000,
            storage_path="/test/report.pdf",
            upload_time=datetime.now(),
        ),
        UploadedFile(
            owner_id=owner_id,
            filename="presentation.pptx",
            file_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            file_size=1000,
            storage_path="/test/presentation.pptx",
            upload_time=datetime.now(),
        ),
    ]
    # Save all files in one transaction
    async with AsyncSessionFactory.session_scope() as session:
        # Create test user first (SEC-RBAC requires owner_id FK)
        await create_test_user(session, owner_id)
        repo = FileRepository(session)
        for file in files:
            await repo.save_file_metadata(file)
        await session.commit()
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
        async with AsyncSessionFactory.session_scope() as session:
            repo = FileRepository(session)
            resolver = FileResolver(repo)
            file_scores = []
            for file in files:
                score = resolver._calculate_score(file, intent)
                file_scores.append((file.filename, score))
            best_file = max(file_scores, key=lambda x: x[1])
            assert (
                best_file[0] == expected_best_file
            ), f"{description}: expected {expected_best_file}, got {best_file[0]} with score {best_file[1]}"


@pytest.mark.asyncio
async def test_scoring_edge_cases():
    """Test scoring handles edge cases gracefully"""
    owner_id = str(uuid4())
    old_file = UploadedFile(
        owner_id=owner_id,
        filename="ancient.pdf",
        file_type="application/pdf",
        file_size=1000,
        storage_path="/test/ancient.pdf",
        upload_time=datetime.now() - timedelta(days=365),  # 1 year old
    )
    unknown_file = UploadedFile(
        owner_id=owner_id,
        filename="unknown.xyz",
        file_type="application/unknown",
        file_size=1000,
        storage_path="/test/unknown.xyz",
        upload_time=datetime.now(),
    )

    # Save both files in one transaction
    async with AsyncSessionFactory.session_scope() as session:
        # Create test user first (SEC-RBAC requires owner_id FK)
        await create_test_user(session, owner_id)
        repo = FileRepository(session)
        await repo.save_file_metadata(old_file)
        await repo.save_file_metadata(unknown_file)
        await session.commit()

    intent = Intent(
        category=IntentCategory.ANALYSIS,
        action="analyze_report",
        context={"original_message": "analyze the report"},
    )

    # Test scoring in separate session
    async with AsyncSessionFactory.session_scope() as session:
        repo = FileRepository(session)
        resolver = FileResolver(repo)

        # Test old file scoring
        old_score = resolver._calculate_score(old_file, intent)
        assert 0.0 <= old_score <= 1.0, f"Old file score {old_score} out of range"
        assert old_score < 0.5, f"Very old file should have low score, got {old_score}"

        # Test unknown file type scoring
        unknown_score = resolver._calculate_score(unknown_file, intent)
        assert 0.0 <= unknown_score <= 1.0, f"Unknown file type score {unknown_score} out of range"


@pytest.mark.asyncio
async def test_minimal_file_repository_operations():
    """Minimal test to isolate connection pool issue"""
    from services.domain.models import UploadedFile
    from services.repositories.file_repository import FileRepository

    owner_id = str(uuid4())
    # Test both operations in a single transaction
    async with AsyncSessionFactory.session_scope() as session:
        # Create test user first (SEC-RBAC requires owner_id FK)
        await create_test_user(session, owner_id)
        repo = FileRepository(session)
        file1 = UploadedFile(
            owner_id=owner_id,
            filename="test1.txt",
            file_type="text/plain",
            file_size=100,
            storage_path="/tmp/test1.txt",
        )
        file2 = UploadedFile(
            owner_id=owner_id,
            filename="test2.txt",
            file_type="text/plain",
            file_size=200,
            storage_path="/tmp/test2.txt",
        )
        await repo.save_file_metadata(file1)
        await repo.save_file_metadata(file2)
        await session.commit()


@pytest.mark.asyncio
async def test_minimal_file_repository_loop():
    """Test with loop to find error threshold"""
    from services.domain.models import UploadedFile
    from services.repositories.file_repository import FileRepository

    for i in range(20):
        owner_id = str(uuid4())
        async with AsyncSessionFactory.session_scope() as session:
            # Create test user first (SEC-RBAC requires owner_id FK)
            await create_test_user(session, owner_id)
            repo = FileRepository(session)
            file = UploadedFile(
                owner_id=owner_id,
                filename=f"test{i}.txt",
                file_type="text/plain",
                file_size=100 * (i + 1),
                storage_path=f"/tmp/test{i}.txt",
            )
            await repo.save_file_metadata(file)
