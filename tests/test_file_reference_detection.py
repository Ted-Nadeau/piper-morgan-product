from datetime import datetime

import pytest

from services.intent_service.classifier import IntentClassifier
from services.intent_service.pre_classifier import PreClassifier
from services.session.session_manager import SessionManager


class TestFileReferenceDetection:
    """Test file reference detection functionality"""

    @pytest.fixture
    def session_manager(self):
        """Create a fresh session manager for each test"""
        return SessionManager(ttl_minutes=30)

    @pytest.fixture
    def classifier(self):
        """Create a classifier instance"""
        return IntentClassifier()

    def test_file_reference_patterns(self):
        """Test that file reference patterns are correctly detected"""
        # Test various file reference patterns
        file_references = [
            "analyze the file I uploaded",
            "create a ticket from that document",
            "what's in the csv",
            "summarize the pdf",
            "the spreadsheet shows",
            "my report contains",
            "the data indicates",
            "that upload has",
            "the excel file shows",
        ]

        for message in file_references:
            assert PreClassifier.detect_file_reference(
                message
            ), f"Failed to detect file reference in: {message}"

    def test_non_file_references(self):
        """Test that non-file references are not detected"""
        # Test messages that should NOT be detected as file references
        non_file_references = [
            "hello there",
            "create a ticket",
            "list all projects",
            "how are you",
            "thanks for the help",
            "goodbye",
            "analyze the data",
            "the project is ready",
        ]

        for message in non_file_references:
            assert not PreClassifier.detect_file_reference(
                message
            ), f"Incorrectly detected file reference in: {message}"

    @pytest.mark.asyncio
    async def test_classification_with_file_context(self, session_manager, classifier):
        """Test that file context is included in classification"""
        session_id = "test_file_context"
        session = session_manager.get_or_create_session(session_id)

        # Add a file to the session
        session.add_uploaded_file(
            file_id="test_file_123",
            filename="data.csv",
            file_type="text/csv",
            upload_time=datetime.utcnow(),
        )

        # Test classification with file reference
        intent = await classifier.classify(
            message="analyze the file I uploaded", session=session
        )

        # Should be classified as analysis intent
        assert intent.category.value == "analysis"
        assert intent.action == "analyze_data"
        assert intent.confidence > 0.7

    @pytest.mark.asyncio
    async def test_classification_without_file_context(
        self, session_manager, classifier
    ):
        """Test that classification works without file context"""
        session_id = "test_no_file_context"
        session = session_manager.get_or_create_session(session_id)

        # Test classification without file reference
        intent = await classifier.classify(message="list all projects", session=session)

        # Should be classified as query intent
        assert intent.category.value == "query"
        assert intent.action == "list_projects"
        assert intent.confidence > 0.7

    @pytest.mark.asyncio
    async def test_file_reference_with_multiple_files(
        self, session_manager, classifier
    ):
        """Test file reference when multiple files are uploaded"""
        session_id = "test_multiple_files"
        session = session_manager.get_or_create_session(session_id)

        # Add multiple files
        session.add_uploaded_file(
            "file1", "report.pdf", "application/pdf", datetime.utcnow()
        )
        session.add_uploaded_file("file2", "data.csv", "text/csv", datetime.utcnow())

        # Test classification with ambiguous file reference
        intent = await classifier.classify(
            message="analyze the document", session=session
        )

        # Should still be classified as analysis, but may need clarification
        assert intent.category.value in ["analysis", "conversation"]
        if intent.category.value == "conversation":
            assert intent.action == "clarification_needed"

    def test_file_reference_edge_cases(self):
        """Test edge cases for file reference detection"""
        edge_cases = [
            ("THE FILE", True),  # Case insensitive
            ("that document!", True),  # With punctuation
            ("my file and stuff", True),  # With additional words
            ("file the report", False),  # Word order matters
            ("the file is ready", True),  # Complete sentence
            ("", False),  # Empty string
            ("   the file   ", True),  # With whitespace
        ]

        for message, expected in edge_cases:
            result = PreClassifier.detect_file_reference(message)
            assert (
                result == expected
            ), f"Expected {expected} for '{message}', got {result}"
