"""
Test-Driven Development for MCP Value Objects
Testing ContentMatch, RelevanceScore, and ContentExtract value objects.
"""

from datetime import datetime

import pytest

# These imports WILL FAIL initially - that's the point of TDD!
from services.domain.mcp.value_objects import (
    ContentExtract,
    ContentMatch,
    ContentSearchResult,
    RelevanceScore,
    SearchQuery,
)


class TestContentMatch:
    """Test suite for ContentMatch value object."""

    def test_content_match_creation(self):
        """Test creating a ContentMatch with all required fields."""
        match = ContentMatch(
            snippet="This is a project timeline document",
            start_position=10,
            end_position=35,
            matched_terms=["project", "timeline"],
            relevance_score=0.85,
        )

        assert match.snippet == "This is a project timeline document"
        assert match.start_position == 10
        assert match.end_position == 35
        assert match.matched_terms == ["project", "timeline"]
        assert match.relevance_score == 0.85

    def test_content_match_validation(self):
        """Test that ContentMatch validates its inputs."""
        # Test invalid position range
        with pytest.raises(ValueError, match="end_position must be greater than start_position"):
            ContentMatch(
                snippet="test",
                start_position=10,
                end_position=5,  # Invalid: end < start
                matched_terms=["test"],
                relevance_score=0.5,
            )

        # Test invalid relevance score
        with pytest.raises(ValueError, match="relevance_score must be between 0 and 1"):
            ContentMatch(
                snippet="test",
                start_position=0,
                end_position=4,
                matched_terms=["test"],
                relevance_score=1.5,  # Invalid: > 1
            )

    def test_content_match_equality(self):
        """Test ContentMatch equality comparison."""
        match1 = ContentMatch(
            snippet="test snippet",
            start_position=0,
            end_position=4,
            matched_terms=["test"],
            relevance_score=0.5,
        )

        match2 = ContentMatch(
            snippet="test snippet",
            start_position=0,
            end_position=4,
            matched_terms=["test"],
            relevance_score=0.5,
        )

        match3 = ContentMatch(
            snippet="different snippet",
            start_position=0,
            end_position=9,
            matched_terms=["different"],
            relevance_score=0.5,
        )

        assert match1 == match2
        assert match1 != match3

    def test_content_match_length_property(self):
        """Test that ContentMatch calculates snippet length correctly."""
        match = ContentMatch(
            snippet="project timeline",
            start_position=0,
            end_position=16,
            matched_terms=["project", "timeline"],
            relevance_score=0.8,
        )

        assert match.length == 16  # end_position - start_position


class TestRelevanceScore:
    """Test suite for RelevanceScore value object."""

    def test_relevance_score_creation(self):
        """Test creating a RelevanceScore with all fields."""
        score = RelevanceScore(
            value=0.75,
            matched_terms=["project", "timeline"],
            total_terms=3,
            scoring_method="tf_idf",
        )

        assert score.value == 0.75
        assert score.matched_terms == ["project", "timeline"]
        assert score.total_terms == 3
        assert score.scoring_method == "tf_idf"

    def test_relevance_score_validation(self):
        """Test RelevanceScore input validation."""
        # Test invalid score value
        with pytest.raises(ValueError, match="Score value must be between 0 and 1"):
            RelevanceScore(
                value=-0.1,  # Invalid: negative
                matched_terms=["test"],
                total_terms=1,
                scoring_method="test",
            )

        with pytest.raises(ValueError, match="Score value must be between 0 and 1"):
            RelevanceScore(
                value=1.1,  # Invalid: > 1
                matched_terms=["test"],
                total_terms=1,
                scoring_method="test",
            )

        # Test invalid total_terms
        with pytest.raises(ValueError, match="total_terms must be positive"):
            RelevanceScore(
                value=0.5,
                matched_terms=["test"],
                total_terms=0,  # Invalid: zero
                scoring_method="test",
            )

    def test_relevance_score_match_ratio(self):
        """Test that RelevanceScore calculates match ratio correctly."""
        score = RelevanceScore(
            value=0.8,
            matched_terms=["project", "timeline"],
            total_terms=4,  # 2 out of 4 terms matched
            scoring_method="simple",
        )

        assert score.match_ratio == 0.5  # 2/4 = 0.5

    def test_relevance_score_is_significant(self):
        """Test significance threshold checking."""
        high_score = RelevanceScore(
            value=0.8, matched_terms=["project"], total_terms=1, scoring_method="test"
        )

        low_score = RelevanceScore(
            value=0.1, matched_terms=[], total_terms=3, scoring_method="test"
        )

        assert high_score.is_significant() is True
        assert low_score.is_significant() is False

    def test_relevance_score_comparison(self):
        """Test RelevanceScore comparison operations."""
        score1 = RelevanceScore(
            value=0.8, matched_terms=["test"], total_terms=1, scoring_method="test"
        )

        score2 = RelevanceScore(
            value=0.6, matched_terms=["test"], total_terms=1, scoring_method="test"
        )

        assert score1 > score2
        assert score2 < score1
        assert score1 != score2


class TestContentExtract:
    """Test suite for ContentExtract value object."""

    def test_content_extract_creation(self):
        """Test creating a ContentExtract with all fields."""
        extract = ContentExtract(
            text="This is the extracted text content",
            file_type="text/plain",
            extraction_method="direct",
            word_count=6,
            metadata={"encoding": "utf-8"},
        )

        assert extract.text == "This is the extracted text content"
        assert extract.file_type == "text/plain"
        assert extract.extraction_method == "direct"
        assert extract.word_count == 6
        assert extract.metadata["encoding"] == "utf-8"

    def test_content_extract_validation(self):
        """Test ContentExtract input validation."""
        # Test None text
        with pytest.raises(ValueError, match="Text cannot be None"):
            ContentExtract(
                text=None, file_type="text/plain", extraction_method="direct", word_count=0
            )

        # Test negative word count
        with pytest.raises(ValueError, match="word_count cannot be negative"):
            ContentExtract(
                text="test", file_type="text/plain", extraction_method="direct", word_count=-1
            )

    def test_content_extract_auto_word_count(self):
        """Test that ContentExtract can auto-calculate word count."""
        extract = ContentExtract(
            text="This is a test with five words",
            file_type="text/plain",
            extraction_method="direct",
            # word_count not provided
        )

        assert extract.word_count == 7  # Should auto-calculate

    def test_content_extract_is_empty(self):
        """Test empty content detection."""
        empty_extract = ContentExtract(
            text="", file_type="text/plain", extraction_method="direct", word_count=0
        )

        non_empty_extract = ContentExtract(
            text="content", file_type="text/plain", extraction_method="direct", word_count=1
        )

        assert empty_extract.is_empty() is True
        assert non_empty_extract.is_empty() is False

    def test_content_extract_has_metadata(self):
        """Test metadata presence checking."""
        with_metadata = ContentExtract(
            text="test",
            file_type="text/plain",
            extraction_method="direct",
            word_count=1,
            metadata={"key": "value"},
        )

        without_metadata = ContentExtract(
            text="test", file_type="text/plain", extraction_method="direct", word_count=1
        )

        assert with_metadata.has_metadata() is True
        assert without_metadata.has_metadata() is False


class TestSearchQuery:
    """Test suite for SearchQuery value object."""

    def test_search_query_creation(self):
        """Test creating a SearchQuery with required fields."""
        query = SearchQuery(
            text="project timeline", session_id="session-123", search_type="content", max_results=10
        )

        assert query.text == "project timeline"
        assert query.session_id == "session-123"
        assert query.search_type == "content"
        assert query.max_results == 10

    def test_search_query_validation(self):
        """Test SearchQuery input validation."""
        # Test empty query text
        with pytest.raises(ValueError, match="Query text cannot be empty"):
            SearchQuery(text="", session_id="session-123", search_type="content")

        # Test invalid max_results
        with pytest.raises(ValueError, match="max_results must be positive"):
            SearchQuery(text="test", session_id="session-123", search_type="content", max_results=0)

    def test_search_query_terms_property(self):
        """Test that SearchQuery extracts terms correctly."""
        query = SearchQuery(
            text="project timeline management", session_id="session-123", search_type="content"
        )

        terms = query.terms
        assert "project" in terms
        assert "timeline" in terms
        assert "management" in terms
        assert len(terms) == 3

    def test_search_query_is_valid(self):
        """Test query validation method."""
        valid_query = SearchQuery(
            text="project timeline", session_id="session-123", search_type="content"
        )

        assert valid_query.is_valid() is True


class TestContentSearchResult:
    """Test suite for ContentSearchResult value object."""

    def test_content_search_result_creation(self):
        """Test creating a ContentSearchResult."""
        relevance_score = RelevanceScore(
            value=0.8, matched_terms=["project"], total_terms=2, scoring_method="tf_idf"
        )

        content_matches = [
            ContentMatch(
                snippet="project timeline",
                start_position=0,
                end_position=16,
                matched_terms=["project"],
                relevance_score=0.8,
            )
        ]

        result = ContentSearchResult(
            file_id="file-123",
            filename="project_doc.txt",
            file_type="text/plain",
            relevance_score=relevance_score,
            content_matches=content_matches,
            search_source="content",
        )

        assert result.file_id == "file-123"
        assert result.filename == "project_doc.txt"
        assert result.file_type == "text/plain"
        assert result.relevance_score == relevance_score
        assert len(result.content_matches) == 1
        assert result.search_source == "content"

    def test_content_search_result_validation(self):
        """Test ContentSearchResult validation."""
        with pytest.raises(ValueError, match="file_id cannot be empty"):
            ContentSearchResult(
                file_id="",
                filename="test.txt",
                file_type="text/plain",
                relevance_score=RelevanceScore(
                    value=0.5, matched_terms=[], total_terms=1, scoring_method="test"
                ),
                content_matches=[],
                search_source="content",
            )

    def test_content_search_result_has_matches(self):
        """Test content matches detection."""
        result_with_matches = ContentSearchResult(
            file_id="file-123",
            filename="test.txt",
            file_type="text/plain",
            relevance_score=RelevanceScore(
                value=0.8, matched_terms=["test"], total_terms=1, scoring_method="test"
            ),
            content_matches=[
                ContentMatch(
                    snippet="test content",
                    start_position=0,
                    end_position=12,
                    matched_terms=["test"],
                    relevance_score=0.8,
                )
            ],
            search_source="content",
        )

        result_without_matches = ContentSearchResult(
            file_id="file-456",
            filename="empty.txt",
            file_type="text/plain",
            relevance_score=RelevanceScore(
                value=0.1, matched_terms=[], total_terms=1, scoring_method="test"
            ),
            content_matches=[],
            search_source="filename",
        )

        assert result_with_matches.has_content_matches() is True
        assert result_without_matches.has_content_matches() is False

    def test_content_search_result_comparison(self):
        """Test ContentSearchResult sorting by relevance."""
        high_relevance = ContentSearchResult(
            file_id="file-1",
            filename="high.txt",
            file_type="text/plain",
            relevance_score=RelevanceScore(
                value=0.9, matched_terms=["test"], total_terms=1, scoring_method="test"
            ),
            content_matches=[],
            search_source="content",
        )

        low_relevance = ContentSearchResult(
            file_id="file-2",
            filename="low.txt",
            file_type="text/plain",
            relevance_score=RelevanceScore(
                value=0.3, matched_terms=["test"], total_terms=1, scoring_method="test"
            ),
            content_matches=[],
            search_source="content",
        )

        assert high_relevance > low_relevance
        assert low_relevance < high_relevance

        # Test sorting
        results = [low_relevance, high_relevance]
        sorted_results = sorted(results, reverse=True)
        assert sorted_results[0] == high_relevance
        assert sorted_results[1] == low_relevance
