#!/usr/bin/env python3
"""
TDD Tests for PM-039: Intent Classification Coverage Improvements
Testing new search patterns and variations - focusing on fallback classification
"""

import pytest

from services.domain.models import Intent, IntentCategory
from services.intent_service.classifier import IntentClassifier


@pytest.fixture
def classifier():
    """Fixture to create an IntentClassifier for testing fallback patterns."""
    return IntentClassifier()


class TestFallbackSearchPatterns:
    """Test new search patterns using fallback classification"""

    @pytest.mark.smoke
    def test_find_technical_specifications_pattern(self, classifier):
        """Test 'find technical specifications' pattern"""
        message = "find technical specifications"

        # Test the fallback classification directly
        result_intent = classifier._fallback_classify(message)

        assert result_intent.category == IntentCategory.QUERY
        assert result_intent.action == "search_documents"
        assert "search_query" in result_intent.context
        assert "technical specifications" in result_intent.context["search_query"]

    @pytest.mark.smoke
    def test_search_for_type_files_pattern(self, classifier):
        """Test 'search for [type] files' pattern variations"""
        test_cases = [
            ("search for PDF files", "PDF files"),
            ("search for markdown files", "markdown files"),
            ("search for config files", "config files"),
            ("search for documentation files", "documentation files"),
        ]

        for message, expected_content in test_cases:
            result_intent = classifier._fallback_classify(message)

            assert result_intent.category == IntentCategory.QUERY
            assert result_intent.action == "search_files"
            assert "search_query" in result_intent.context
            assert any(
                word in result_intent.context["search_query"].lower()
                for word in expected_content.lower().split()
            )

    @pytest.mark.smoke
    def test_locate_files_patterns(self, classifier):
        """Test 'locate files' patterns"""
        message = "locate files with MCP integration"

        result_intent = classifier._fallback_classify(message)

        assert result_intent.category == IntentCategory.QUERY
        assert result_intent.action == "find_documents"
        assert "search_query" in result_intent.context
        assert "MCP integration".lower() in result_intent.context["search_query"].lower()

    @pytest.mark.smoke
    def test_look_for_files_patterns(self, classifier):
        """Test 'look for files' patterns"""
        message = "look for files about deployment"

        result_intent = classifier._fallback_classify(message)

        assert result_intent.category == IntentCategory.QUERY
        assert result_intent.action == "find_documents"
        assert "search_query" in result_intent.context

    @pytest.mark.smoke
    def test_files_containing_patterns(self, classifier):
        """Test 'files containing' patterns"""
        message = "find files containing API endpoints"

        result_intent = classifier._fallback_classify(message)

        assert result_intent.category == IntentCategory.QUERY
        assert result_intent.action == "search_content"
        assert "search_query" in result_intent.context
        assert "API endpoints".lower() in result_intent.context["search_query"].lower()

    @pytest.mark.smoke
    def test_show_me_patterns(self, classifier):
        """Test 'show me' patterns"""
        test_cases = [
            "show me files about database",
            "show me documents related to testing",
        ]

        for message in test_cases:
            result_intent = classifier._fallback_classify(message)

            assert result_intent.category == IntentCategory.QUERY
            assert result_intent.action == "search_files"
            assert "search_query" in result_intent.context


class TestQueryExtractionMethods:
    """Test query extraction methods for new patterns"""

    @pytest.mark.smoke
    def test_extract_search_query_with_new_patterns(self, classifier):
        """Test query extraction with new trigger phrases"""
        test_cases = [
            ("find technical specifications", ["find technical specifications"]),
            ("search for PDF files", ["search for"]),
            ("look for files about deployment", ["look for files"]),
            ("locate files with MCP", ["locate files"]),
        ]

        for message, trigger_phrases in test_cases:
            result = classifier._extract_search_query(message, trigger_phrases)
            # Should extract some meaningful query content
            assert len(result.strip()) > 0

    @pytest.mark.smoke
    def test_extract_search_query_about_patterns(self, classifier):
        """Test extraction of 'about' patterns"""
        test_cases = [
            ("find documents about project timeline", "project timeline"),
            ("search files about API design", "API design"),
            ("locate files about database schema", "database schema"),
        ]

        for message, expected_query in test_cases:
            result = classifier._extract_search_query_about(message)
            assert expected_query.lower() in result.lower()

    @pytest.mark.smoke
    def test_extract_search_query_show_me(self, classifier):
        """Test extraction of 'show me' patterns"""
        test_cases = [
            ("show me files about database", "database"),
            ("show me documents related to testing", "testing"),
        ]

        for message, expected_content in test_cases:
            result = classifier._extract_search_query_show_me(message)
            assert expected_content.lower() in result.lower()


class TestErrorPatternElimination:
    """Test that new patterns eliminate 'Unknown query action' errors"""

    @pytest.mark.smoke
    def test_no_learning_fallback_for_target_phrases(self, classifier):
        """Test that target phrases don't fall back to learning actions"""
        target_phrases = [
            "find technical specifications",
            "search for PDF files",
            "look for files containing requirements",
            "locate files with deployment info",
            "find files containing API endpoints",
        ]

        for phrase in target_phrases:
            result_intent = classifier._fallback_classify(phrase)

            # Should not result in learning actions (which is the default fallback)
            assert result_intent.action != "learn_pattern"
            # Should be a valid query action
            assert result_intent.action in [
                "find_documents",
                "search_files",
                "search_content",
                "search_documents",
                "list_items",
                "get_project",
                "count_projects",
            ]
