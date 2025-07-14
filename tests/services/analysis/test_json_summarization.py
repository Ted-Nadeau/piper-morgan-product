"""
TDD Tests for JSON Mode Document Summarization
Test-driven development for structured summary generation
"""

import json
from datetime import datetime

import pytest

from services.analysis.summary_parser import SummaryParser
from services.domain.models import DocumentSummary, SummarySection


class TestSummarySection:
    """Test SummarySection domain model"""

    def test_empty_section_to_markdown(self):
        """Empty section should generate proper markdown"""
        section = SummarySection(heading="Test Section")
        markdown = section.to_markdown()

        expected = "### Test Section\n\nNo items found.\n"
        assert markdown == expected

    def test_section_with_points_to_markdown(self):
        """Section with points should generate clean bullet list"""
        section = SummarySection(
            heading="Key Points", points=["First point", "Second point", "Third point"]
        )
        markdown = section.to_markdown()

        expected = "### Key Points\n\n- First point\n- Second point\n- Third point\n\n"
        assert markdown == expected

    def test_section_with_special_characters(self):
        """Section should handle special characters properly"""
        section = SummarySection(
            heading="Issues & Bugs",
            points=["API returns 500 error", "Database connection timeout"],
        )
        markdown = section.to_markdown()

        assert "### Issues & Bugs\n\n" in markdown
        assert "- API returns 500 error\n" in markdown
        assert "- Database connection timeout\n" in markdown


class TestDocumentSummary:
    """Test DocumentSummary domain model"""

    def test_minimal_summary_to_markdown(self):
        """Minimal summary should generate clean markdown"""
        summary = DocumentSummary(title="Test Document", document_type="Requirements")
        markdown = summary.to_markdown()

        expected = "# Test Document\n\n**Document Type:** Requirements\n\n"
        assert markdown == expected

    def test_summary_with_key_findings(self):
        """Summary with key findings should format properly"""
        summary = DocumentSummary(
            title="Project Analysis",
            document_type="Analysis Report",
            key_findings=["Critical bug found", "Performance issues identified"],
        )
        markdown = summary.to_markdown()

        assert "# Project Analysis\n\n" in markdown
        assert "**Document Type:** Analysis Report\n\n" in markdown
        assert "## Key Findings\n\n" in markdown
        assert "- Critical bug found\n" in markdown
        assert "- Performance issues identified\n" in markdown

    def test_summary_with_sections(self):
        """Summary with additional sections should format properly"""
        summary = DocumentSummary(
            title="API Documentation",
            document_type="Technical Spec",
            key_findings=["REST API documented"],
        )
        summary.add_section("Endpoints", ["GET /api/users", "POST /api/users"])
        summary.add_section("Authentication", ["Bearer token required"])

        markdown = summary.to_markdown()

        assert "# API Documentation\n\n" in markdown
        assert "## Key Findings\n\n" in markdown
        assert "- REST API documented\n" in markdown
        assert "### Endpoints\n\n" in markdown
        assert "- GET /api/users\n" in markdown
        assert "- POST /api/users\n" in markdown
        assert "### Authentication\n\n" in markdown
        assert "- Bearer token required\n" in markdown

    def test_get_section_by_heading(self):
        """Should be able to retrieve sections by heading"""
        summary = DocumentSummary(title="Test Doc", document_type="Test")
        summary.add_section("Features", ["Feature 1", "Feature 2"])

        section = summary.get_section("Features")
        assert section is not None
        assert section.heading == "Features"
        assert section.points == ["Feature 1", "Feature 2"]

        # Non-existent section should return None
        missing_section = summary.get_section("Non-existent")
        assert missing_section is None

    def test_clean_bullet_formatting_in_output(self):
        """Generated markdown should use clean ASCII hyphens for bullets"""
        summary = DocumentSummary(
            title="Test Document",
            document_type="Test",
            key_findings=["Finding with • bullet", "Another finding"],
        )
        summary.add_section("Issues", ["Issue with • character"])

        markdown = summary.to_markdown()

        # Should use ASCII hyphens for list bullets (markdown structure)
        assert "- Finding with • bullet\n" in markdown
        assert "- Another finding\n" in markdown
        assert "- Issue with • character\n" in markdown

        # Should not have malformed bullets like "• -"
        assert "• -" not in markdown


class TestSummaryParser:
    """Test SummaryParser service (TDD - these will fail initially)"""

    def test_parse_valid_json_to_summary(self):
        """Should parse valid JSON into DocumentSummary"""
        json_response = {
            "title": "Requirements Document",
            "document_type": "Product Requirements",
            "key_findings": [
                "User authentication required",
                "Database schema needs optimization",
            ],
            "sections": [
                {
                    "heading": "Features",
                    "points": ["User registration", "Password reset"],
                },
                {
                    "heading": "Technical Requirements",
                    "points": ["PostgreSQL database", "Redis cache"],
                },
            ],
        }

        parser = SummaryParser()
        summary = parser.parse_json(json.dumps(json_response))

        assert isinstance(summary, DocumentSummary)
        assert summary.title == "Requirements Document"
        assert summary.document_type == "Product Requirements"
        assert len(summary.key_findings) == 2
        assert "User authentication required" in summary.key_findings
        assert len(summary.sections) == 2

        features_section = summary.get_section("Features")
        assert features_section is not None
        assert "User registration" in features_section.points

    def test_parse_minimal_json(self):
        """Should handle minimal JSON with just title and document_type"""
        json_response = {"title": "Simple Doc", "document_type": "Note"}

        parser = SummaryParser()
        summary = parser.parse_json(json.dumps(json_response))

        assert summary.title == "Simple Doc"
        assert summary.document_type == "Note"
        assert len(summary.key_findings) == 0
        assert len(summary.sections) == 0

    def test_parse_invalid_json_returns_error_summary(self):
        """Should gracefully handle malformed JSON"""
        invalid_json = "{ invalid json structure"

        parser = SummaryParser()
        summary = parser.parse_json(invalid_json)

        assert isinstance(summary, DocumentSummary)
        assert "Error" in summary.title
        assert summary.document_type == "Error"
        assert len(summary.key_findings) > 0
        assert "JSON parsing failed" in summary.key_findings[0]

    def test_parse_json_missing_required_fields(self):
        """Should handle JSON missing required fields"""
        incomplete_json = {
            "title": "Test Doc"
            # Missing document_type
        }

        parser = SummaryParser()
        summary = parser.parse_json(json.dumps(incomplete_json))

        assert summary.title == "Test Doc"
        assert summary.document_type == "Unknown"  # Should default

    def test_parse_json_with_empty_sections(self):
        """Should handle sections with no points"""
        json_response = {
            "title": "Test Doc",
            "document_type": "Test",
            "sections": [{"heading": "Empty Section", "points": []}],
        }

        parser = SummaryParser()
        summary = parser.parse_json(json.dumps(json_response))

        section = summary.get_section("Empty Section")
        assert section is not None
        assert len(section.points) == 0

        # Should still generate valid markdown
        markdown = summary.to_markdown()
        assert "### Empty Section\n\nNo items found.\n" in markdown

    def test_parse_json_with_malformed_key_findings_string(self):
        """Should handle key_findings as a single string with Unicode bullets"""
        json_response = {
            "title": "Test Doc",
            "document_type": "Test",
            "key_findings": "• First finding • Second finding • Third finding",
        }

        parser = SummaryParser()
        summary = parser.parse_json(json.dumps(json_response))

        # Should split the string into individual findings
        assert len(summary.key_findings) == 3
        assert "First finding" in summary.key_findings
        assert "Second finding" in summary.key_findings
        assert "Third finding" in summary.key_findings

        # Should generate clean markdown
        markdown = summary.to_markdown()
        assert "- First finding\n" in markdown
        assert "- Second finding\n" in markdown
        assert "- Third finding\n" in markdown
        assert "•" not in markdown  # No Unicode bullets in output

    def test_parse_json_with_inline_bold_headings(self):
        """Should handle inline bold headings that lost line breaks"""
        json_response = {
            "title": "Test Doc",
            "document_type": "Test",
            "key_findings": "**Topic** details here and then **Another topic** more details **Final topic** end details",
        }

        parser = SummaryParser()
        summary = parser.parse_json(json.dumps(json_response))

        # Should split into separate items
        assert len(summary.key_findings) == 3
        assert "**Topic** details here and then" in summary.key_findings
        assert "**Another topic** more details" in summary.key_findings
        assert "**Final topic** end details" in summary.key_findings

        # Should generate clean markdown
        markdown = summary.to_markdown()
        assert "- **Topic** details here and then\n" in markdown
        assert "- **Another topic** more details\n" in markdown
        assert "- **Final topic** end details\n" in markdown

    def test_parse_json_with_numbered_lists(self):
        """Should handle numbered lists that lost line breaks"""
        json_response = {
            "title": "Test Doc",
            "document_type": "Test",
            "key_findings": "1. First item 2. Second item 3. Third item",
        }

        parser = SummaryParser()
        summary = parser.parse_json(json.dumps(json_response))

        # Should split into separate items
        assert len(summary.key_findings) == 3
        assert "First item" in summary.key_findings
        assert "Second item" in summary.key_findings
        assert "Third item" in summary.key_findings

    def test_parse_json_with_malformed_section_points(self):
        """Should handle section points as strings with formatting issues"""
        json_response = {
            "title": "Test Doc",
            "document_type": "Test",
            "sections": [
                {
                    "heading": "Features",
                    "points": "• Feature one • Feature two • Feature three",
                }
            ],
        }

        parser = SummaryParser()
        summary = parser.parse_json(json.dumps(json_response))

        # Should split the string into individual points
        section = summary.get_section("Features")
        assert section is not None
        assert len(section.points) == 3
        assert "Feature one" in section.points
        assert "Feature two" in section.points
        assert "Feature three" in section.points

        # Should generate clean markdown
        markdown = summary.to_markdown()
        assert "- Feature one\n" in markdown
        assert "- Feature two\n" in markdown
        assert "- Feature three\n" in markdown
        assert "•" not in markdown


class TestEndToEndMarkdownGeneration:
    """Test complete flow from JSON to clean markdown"""

    def test_complex_document_generates_clean_markdown(self):
        """Complex document should generate clean, readable markdown"""
        json_response = {
            "title": "Product Requirements Document",
            "document_type": "PRD",
            "key_findings": [
                "User story mapping completed",
                "Technical feasibility confirmed",
                "Resource allocation defined",
            ],
            "sections": [
                {
                    "heading": "Core Features",
                    "points": [
                        "User authentication system",
                        "Dashboard with analytics",
                        "Mobile-responsive design",
                    ],
                },
                {
                    "heading": "Technical Stack",
                    "points": [
                        "React frontend",
                        "Python backend",
                        "PostgreSQL database",
                    ],
                },
                {
                    "heading": "Success Metrics",
                    "points": [
                        "90% user satisfaction",
                        "< 2 second load time",
                        "99.9% uptime",
                    ],
                },
            ],
        }

        parser = SummaryParser()
        summary = parser.parse_json(json.dumps(json_response))
        markdown = summary.to_markdown()

        # Verify structure
        assert markdown.startswith("# Product Requirements Document\n\n")
        assert "**Document Type:** PRD\n\n" in markdown
        assert "## Key Findings\n\n" in markdown
        assert "### Core Features\n\n" in markdown
        assert "### Technical Stack\n\n" in markdown
        assert "### Success Metrics\n\n" in markdown

        # Verify clean formatting
        assert "• ##" not in markdown  # No malformed headers
        assert (
            markdown.count("- ") == 12
        )  # Correct number of bullet points (3 key findings + 9 section points)

        # Verify content
        assert "- User authentication system\n" in markdown
        assert "- Python backend\n" in markdown
        assert "- 99.9% uptime\n" in markdown

    def test_no_malformed_headers_in_output(self):
        """Should never generate malformed headers like '• ##'"""
        json_response = {
            "title": "Test Document",
            "document_type": "Test",
            "key_findings": ["Finding with • bullet"],
            "sections": [{"heading": "Section • with bullet", "points": ["Point with • bullet"]}],
        }

        parser = SummaryParser()
        summary = parser.parse_json(json.dumps(json_response))
        markdown = summary.to_markdown()

        # Should not contain malformed headers
        assert "• ##" not in markdown
        assert "• ###" not in markdown

        # Headers should be clean
        assert "### Section • with bullet\n\n" in markdown
        assert "- Point with • bullet\n" in markdown
