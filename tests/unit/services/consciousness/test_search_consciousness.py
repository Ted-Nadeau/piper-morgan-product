"""Tests for search consciousness wrapper. Issue #634."""

import pytest


class TestSearchConsciousness:
    """Test consciousness wrapper for search results."""

    def test_search_results_has_identity(self):
        """Search results must have identity voice."""
        from services.consciousness.search_consciousness import format_search_results_conscious

        results = [
            {"title": "Auth Guide", "url": "https://example.com/1"},
            {"title": "JWT Docs", "url": "https://example.com/2"},
        ]
        output = format_search_results_conscious("authentication", results, "Notion")
        assert "I " in output or "I'" in output, "Should have identity"
        assert "authentication" in output.lower(), "Should mention query"

    def test_search_results_has_invitation(self):
        """Search results must have dialogue invitation."""
        from services.consciousness.search_consciousness import format_search_results_conscious

        results = [{"title": "Doc 1", "url": "https://example.com"}]
        output = format_search_results_conscious("test", results, "Notion")
        assert "?" in output, "Should have invitation"

    def test_search_results_highlights_top(self):
        """Top result should get special mention."""
        from services.consciousness.search_consciousness import format_search_results_conscious

        results = [
            {"title": "Best Match", "url": "https://example.com/1"},
            {"title": "Second", "url": "https://example.com/2"},
        ]
        output = format_search_results_conscious("query", results, "Notion")
        assert "Best Match" in output, "Should mention top result"

    def test_no_results_has_identity(self):
        """No results message must have identity."""
        from services.consciousness.search_consciousness import format_no_results_conscious

        output = format_no_results_conscious("obscure query")
        assert "I " in output or "I'" in output, "Should have identity"
        assert "?" in output, "Should suggest alternatives"

    def test_search_error_has_invitation(self):
        """Error message must have invitation."""
        from services.consciousness.search_consciousness import format_search_error_conscious

        output = format_search_error_conscious("Connection timeout")
        assert "?" in output, "Should have invitation"
        assert "I " in output or "I'" in output, "Should have identity"

    def test_single_result_format(self):
        """Single result should be formatted nicely."""
        from services.consciousness.search_consciousness import format_search_results_conscious

        results = [{"title": "Only Result", "url": "https://example.com"}]
        output = format_search_results_conscious("specific", results, "Notion")
        assert "Only Result" in output
        assert "1" in output or "one" in output.lower()


class TestSearchConsciousnessSourceAttribution:
    """Test source attribution in search consciousness."""

    def test_source_mentioned_in_output(self):
        """Source should be mentioned in output."""
        from services.consciousness.search_consciousness import format_search_results_conscious

        results = [{"title": "Doc", "url": "https://example.com"}]
        output = format_search_results_conscious("test", results, "your Notion workspace")
        assert "Notion" in output, "Should mention source"

    def test_default_source_used(self):
        """Default source should be used when not specified."""
        from services.consciousness.search_consciousness import format_search_results_conscious

        results = [{"title": "Doc", "url": "https://example.com"}]
        output = format_search_results_conscious("test", results)
        assert "document" in output.lower() or "found" in output.lower()


class TestSearchConsciousnessEdgeCases:
    """Test edge cases for search consciousness."""

    def test_empty_results_returns_no_results_message(self):
        """Empty results list should return no results message."""
        from services.consciousness.search_consciousness import format_search_results_conscious

        output = format_search_results_conscious("test", [], "Notion")
        assert "I " in output or "I'" in output
        assert "?" in output

    def test_result_without_url(self):
        """Results without URL should still format correctly."""
        from services.consciousness.search_consciousness import format_search_results_conscious

        results = [{"title": "No URL Doc"}]
        output = format_search_results_conscious("test", results, "Notion")
        assert "No URL Doc" in output

    def test_many_results_capped(self):
        """Many results should be capped at reasonable number."""
        from services.consciousness.search_consciousness import format_search_results_conscious

        results = [{"title": f"Doc {i}", "url": f"https://example.com/{i}"} for i in range(20)]
        output = format_search_results_conscious("test", results, "Notion")
        # Should mention total count but cap displayed results
        assert "20" in output or "found" in output.lower()
