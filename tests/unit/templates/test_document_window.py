"""
Unit tests for Document Window Component (#422 MUX-IMPLEMENT-DOCS-ACCESS)

Tests the document_window.html component following Place window pattern.
"""

from pathlib import Path

import pytest
from bs4 import BeautifulSoup


@pytest.fixture
def document_window_html():
    """Load the document window component HTML."""
    component_path = Path("templates/components/document_window.html")
    return component_path.read_text()


@pytest.fixture
def soup(document_window_html):
    """Parse the component HTML."""
    return BeautifulSoup(document_window_html, "html.parser")


class TestDocumentWindowTemplate:
    """Tests for the document window template structure."""

    def test_template_exists(self, soup):
        """Template element should exist with correct ID."""
        template = soup.find("template", id="document-window-template")
        assert template is not None, "Template element not found"

    def test_template_has_document_window_class(self, soup):
        """Template should contain element with document-window class."""
        template = soup.find("template", id="document-window-template")
        window = template.find("div", class_="document-window")
        assert window is not None, "document-window element not found in template"

    def test_data_attributes_present(self, soup):
        """Template should have all required data attributes."""
        template = soup.find("template", id="document-window-template")
        window = template.find("div", class_="document-window")

        required_attrs = [
            "data-document-id",
            "data-confidence",
            "data-hardness",
            "data-source-url",
            "data-min-stage",
        ]

        for attr in required_attrs:
            assert window.has_attr(attr), f"Missing data attribute: {attr}"

    def test_hardness_is_soft(self, soup):
        """Document hardness should be 2 (SOFT) for Stage 4+ visibility."""
        template = soup.find("template", id="document-window-template")
        window = template.find("div", class_="document-window")

        assert window["data-hardness"] == "2", "Hardness should be 2 (SOFT)"
        assert window["data-min-stage"] == "4", "Min stage should be 4"


class TestDocumentWindowAriaLabels:
    """Tests for accessibility attributes."""

    def test_window_has_role(self, soup):
        """Document window should have article role."""
        template = soup.find("template", id="document-window-template")
        window = template.find("div", class_="document-window")

        assert window.get("role") == "article", "Window should have role='article'"

    def test_window_has_aria_label(self, soup):
        """Document window should have aria-label attribute."""
        template = soup.find("template", id="document-window-template")
        window = template.find("div", class_="document-window")

        assert window.has_attr("aria-label"), "Window should have aria-label"

    def test_window_is_focusable(self, soup):
        """Document window should be keyboard focusable."""
        template = soup.find("template", id="document-window-template")
        window = template.find("div", class_="document-window")

        assert window.get("tabindex") == "0", "Window should have tabindex='0'"

    def test_icon_is_hidden_from_screen_readers(self, soup):
        """Icon should be hidden from screen readers."""
        template = soup.find("template", id="document-window-template")
        icon = template.find("svg", class_="document-window-icon")

        assert icon.get("aria-hidden") == "true", "Icon should be aria-hidden"


class TestDocumentWindowStyles:
    """Tests for Documentation atmosphere styling."""

    def test_documentation_gradient_style(self, document_window_html):
        """Should have documentation-type purple gradient."""
        # Check for purple gradient colors from Place window pattern
        assert "faf5fa" in document_window_html, "Missing light purple gradient start"
        assert "f0e8f5" in document_window_html, "Missing light purple gradient end"

    def test_documentation_border_color(self, document_window_html):
        """Should have purple left border matching documentation type."""
        assert "7d5a7d" in document_window_html, "Missing purple border color"

    def test_hover_shadow_style(self, document_window_html):
        """Should have purple-tinted hover shadow."""
        assert "box-shadow" in document_window_html, "Missing hover shadow"

    def test_focus_outline_style(self, document_window_html):
        """Should have visible focus outline for accessibility."""
        assert "outline" in document_window_html, "Missing focus outline style"


class TestDocumentWindowContent:
    """Tests for document window content elements."""

    def test_has_header_section(self, soup):
        """Should have header with icon and name."""
        template = soup.find("template", id="document-window-template")

        header = template.find("div", class_="document-window-header")
        assert header is not None, "Header section not found"

        icon = header.find("svg", class_="document-window-icon")
        assert icon is not None, "Icon not found in header"

        name = header.find("span", class_="document-window-name")
        assert name is not None, "Name not found in header"

    def test_has_summary_section(self, soup):
        """Should have summary section for Piper's perspective."""
        template = soup.find("template", id="document-window-template")

        summary = template.find("div", class_="document-window-summary")
        assert summary is not None, "Summary section not found"

    def test_has_metadata_section(self, soup):
        """Should have metadata section with size and date."""
        template = soup.find("template", id="document-window-template")

        meta = template.find("div", class_="document-window-meta")
        assert meta is not None, "Metadata section not found"

        size = template.find(class_="document-window-size")
        assert size is not None, "Size element not found"

        date = template.find(class_="document-window-date")
        assert date is not None, "Date element not found"

    def test_has_actions_section(self, soup):
        """Should have actions section with expand and download."""
        template = soup.find("template", id="document-window-template")

        actions = template.find("div", class_="document-window-actions")
        assert actions is not None, "Actions section not found"

        expand = template.find(class_="document-window-expand")
        assert expand is not None, "Expand button not found"

        download = template.find(class_="document-window-download")
        assert download is not None, "Download link not found"


class TestDocumentWindowTrustGating:
    """Tests for trust-gated visibility."""

    def test_trust_hidden_class_exists(self, document_window_html):
        """Should have trust-hidden CSS class for hiding."""
        assert "trust-hidden" in document_window_html
        assert "display: none" in document_window_html

    def test_trust_visible_class_exists(self, document_window_html):
        """Should have trust-visible CSS class for showing."""
        assert "trust-visible" in document_window_html
        assert "display: block" in document_window_html

    def test_min_stage_is_four(self, soup):
        """Default min stage should be 4 (Stage 4+)."""
        template = soup.find("template", id="document-window-template")
        window = template.find("div", class_="document-window")

        assert window["data-min-stage"] == "4"


class TestDocumentWindowConfidence:
    """Tests for confidence-based display."""

    def test_low_confidence_styling(self, document_window_html):
        """Low confidence documents should have distinct styling."""
        assert '[data-confidence="low"]' in document_window_html
        assert "opacity" in document_window_html
        assert "italic" in document_window_html

    def test_confidence_default_is_medium(self, soup):
        """Default confidence should be medium."""
        template = soup.find("template", id="document-window-template")
        window = template.find("div", class_="document-window")

        assert window["data-confidence"] == "medium"


class TestDocumentWindowJavaScript:
    """Tests for JavaScript API."""

    def test_document_window_namespace_created(self, document_window_html):
        """Should create DocumentWindow namespace."""
        assert "window.DocumentWindow" in document_window_html

    def test_create_function_exposed(self, document_window_html):
        """Should expose create function."""
        assert "create: createDocumentWindow" in document_window_html

    def test_render_function_exposed(self, document_window_html):
        """Should expose render function."""
        assert "render: renderDocuments" in document_window_html

    def test_apply_trust_visibility_exposed(self, document_window_html):
        """Should expose applyTrustVisibility function."""
        assert "applyTrustVisibility: applyTrustVisibility" in document_window_html

    def test_piper_voice_prefixes(self, document_window_html):
        """Should have Piper's voice prefixes for summaries."""
        assert "I see this document" in document_window_html
        assert "This contains information" in document_window_html
        assert "Looking at this" in document_window_html

    def test_default_summary_messages(self, document_window_html):
        """Should have friendly default summaries."""
        assert "I haven't had a chance to look through" in document_window_html
        assert "ask me anything about it" in document_window_html


class TestDocumentWindowIcon:
    """Tests for document icon SVG."""

    def test_icon_is_svg(self, soup):
        """Icon should be an SVG element."""
        template = soup.find("template", id="document-window-template")
        icon = template.find("svg", class_="document-window-icon")

        assert icon is not None
        assert icon.name == "svg"

    def test_icon_has_document_shape(self, soup):
        """Icon should represent a document (rectangle with lines)."""
        template = soup.find("template", id="document-window-template")
        icon = template.find("svg", class_="document-window-icon")

        # Should have a rect for document outline
        rect = icon.find("rect")
        assert rect is not None, "Document should have rect for outline"

        # Should have lines for text representation
        lines = icon.find_all("line")
        assert len(lines) >= 2, "Document should have lines representing text"
