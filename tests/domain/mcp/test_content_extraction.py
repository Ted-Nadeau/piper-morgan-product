"""
Test-Driven Development for Content Extraction Domain Service
Following RED-GREEN-REFACTOR methodology.
"""

from pathlib import Path
from unittest.mock import Mock

import pytest

# These imports WILL FAIL initially - that's the point of TDD!
from services.domain.mcp.content_extraction import ContentExtractor
from services.domain.mcp.value_objects import ContentExtract, ContentMatch, RelevanceScore


class TestContentExtractor:
    """Test suite for ContentExtractor domain service."""

    def test_content_extractor_initialization(self):
        """Test that ContentExtractor can be initialized."""
        extractor = ContentExtractor()
        assert extractor is not None

    def test_extract_text_from_string_content(self):
        """Test extracting text content from a string."""
        extractor = ContentExtractor()
        content = "This is a test document with important content."

        result = extractor.extract_text_content(content, "test.txt")

        assert isinstance(result, ContentExtract)
        assert result.text == content
        assert result.file_type == "text/plain"
        assert result.extraction_method == "direct"

    def test_extract_text_from_markdown(self):
        """Test extracting text from markdown content."""
        extractor = ContentExtractor()
        markdown_content = """# Test Document

This is **bold** text and *italic* text.

## Section
- List item 1
- List item 2
"""

        result = extractor.extract_text_content(markdown_content, "test.md")

        assert isinstance(result, ContentExtract)
        assert "Test Document" in result.text
        assert "bold" in result.text
        assert result.file_type == "text/markdown"

    def test_extract_text_handles_empty_content(self):
        """Test that empty content is handled gracefully."""
        extractor = ContentExtractor()

        result = extractor.extract_text_content("", "empty.txt")

        assert isinstance(result, ContentExtract)
        assert result.text == ""
        assert result.word_count == 0

    def test_extract_text_calculates_word_count(self):
        """Test that word count is calculated correctly."""
        extractor = ContentExtractor()
        content = "One two three four five words exactly."

        result = extractor.extract_text_content(content, "test.txt")

        assert result.word_count == 7  # Including "exactly"

    def test_extract_text_handles_large_content(self):
        """Test extraction with content size limits."""
        extractor = ContentExtractor()
        large_content = "word " * 10000  # 10k words

        result = extractor.extract_text_content(large_content, "large.txt")

        assert isinstance(result, ContentExtract)
        assert result.word_count <= 10000  # Should not exceed reasonable limits

    def test_calculate_relevance_score_exact_match(self):
        """Test relevance scoring for exact query matches."""
        extractor = ContentExtractor()
        content = "This document contains project timeline information."
        query = "project timeline"

        score = extractor.calculate_relevance_score(content, query)

        assert isinstance(score, RelevanceScore)
        assert score.value > 0.8  # High relevance for exact match
        assert "project" in score.matched_terms
        assert "timeline" in score.matched_terms

    def test_calculate_relevance_score_partial_match(self):
        """Test relevance scoring for partial query matches."""
        extractor = ContentExtractor()
        content = "This document contains project information."
        query = "project timeline"

        score = extractor.calculate_relevance_score(content, query)

        assert isinstance(score, RelevanceScore)
        assert 0.3 < score.value < 0.7  # Medium relevance for partial match
        assert "project" in score.matched_terms
        assert "timeline" not in score.matched_terms

    def test_calculate_relevance_score_no_match(self):
        """Test relevance scoring when no terms match."""
        extractor = ContentExtractor()
        content = "This document is about cats and dogs."
        query = "project timeline"

        score = extractor.calculate_relevance_score(content, query)

        assert isinstance(score, RelevanceScore)
        assert score.value < 0.1  # Very low relevance for no match
        assert len(score.matched_terms) == 0

    def test_calculate_relevance_score_case_insensitive(self):
        """Test that relevance scoring is case insensitive."""
        extractor = ContentExtractor()
        content = "This document contains PROJECT TIMELINE information."
        query = "project timeline"

        score = extractor.calculate_relevance_score(content, query)

        assert score.value > 0.8
        assert "project" in score.matched_terms
        assert "timeline" in score.matched_terms

    def test_find_content_matches_simple(self):
        """Test finding content matches in text."""
        extractor = ContentExtractor()
        content = "The project timeline shows important milestones. Project planning is crucial."
        query = "project timeline"

        matches = extractor.find_content_matches(content, query)

        assert len(matches) >= 1
        assert isinstance(matches[0], ContentMatch)
        assert "project timeline" in matches[0].snippet.lower()

    def test_find_content_matches_with_context(self):
        """Test that content matches include surrounding context."""
        extractor = ContentExtractor()
        content = "Before text. The project timeline shows important milestones. After text."
        query = "project timeline"

        matches = extractor.find_content_matches(content, query)

        assert len(matches) >= 1
        match = matches[0]
        assert "Before text" in match.snippet or "After text" in match.snippet
        assert match.start_position >= 0
        assert match.end_position > match.start_position

    def test_extract_keywords_from_content(self):
        """Test keyword extraction from content."""
        extractor = ContentExtractor()
        content = (
            "This project timeline document contains important milestone information for planning."
        )

        keywords = extractor.extract_keywords(content, max_keywords=5)

        assert len(keywords) <= 5
        assert "project" in keywords or "timeline" in keywords or "milestone" in keywords
        # Common stop words should be excluded
        assert "this" not in keywords
        assert "for" not in keywords


class TestContentExtractionErrorHandling:
    """Test error handling scenarios for content extraction."""

    def test_extract_handles_none_content(self):
        """Test that None content is handled gracefully."""
        extractor = ContentExtractor()

        with pytest.raises(ValueError, match="Content cannot be None"):
            extractor.extract_text_content(None, "test.txt")

    def test_extract_handles_invalid_filename(self):
        """Test that invalid filenames are handled."""
        extractor = ContentExtractor()

        with pytest.raises(ValueError, match="Filename cannot be empty"):
            extractor.extract_text_content("content", "")

    def test_calculate_relevance_handles_empty_query(self):
        """Test relevance calculation with empty query."""
        extractor = ContentExtractor()

        with pytest.raises(ValueError, match="Query cannot be empty"):
            extractor.calculate_relevance_score("content", "")

    def test_find_matches_handles_empty_inputs(self):
        """Test match finding with empty inputs."""
        extractor = ContentExtractor()

        matches = extractor.find_content_matches("", "query")
        assert len(matches) == 0

        matches = extractor.find_content_matches("content", "")
        assert len(matches) == 0


class TestContentExtractionConfiguration:
    """Test configuration and customization of content extraction."""

    def test_extractor_with_custom_config(self):
        """Test ContentExtractor with custom configuration."""
        config = {"max_content_length": 1000, "include_metadata": True, "snippet_length": 150}

        extractor = ContentExtractor(config=config)

        assert extractor.config["max_content_length"] == 1000
        assert extractor.config["include_metadata"] is True

    def test_extractor_uses_default_config(self):
        """Test that default configuration is applied."""
        extractor = ContentExtractor()

        assert hasattr(extractor, "config")
        assert extractor.config["max_content_length"] > 0
        assert extractor.config["snippet_length"] > 0
