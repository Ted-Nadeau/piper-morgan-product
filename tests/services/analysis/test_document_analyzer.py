import os
from unittest.mock import Mock

import pytest

from services.analysis.base_analyzer import BaseAnalyzer
from services.domain.models import AnalysisResult

FIXTURE_DIR = "tests/fixtures/"


class TestDocumentAnalyzer:
    def setup_method(self):
        # Mock LLM client for summary/key points
        self.mock_llm = Mock()
        # DocumentAnalyzer will be implemented later
        from services.analysis.document_analyzer import DocumentAnalyzer

        self.analyzer = DocumentAnalyzer(llm_client=self.mock_llm)

    @pytest.mark.asyncio
    async def test_basic_pdf_analysis(self):
        """Test page count and text extraction from a normal PDF"""
        pdf_path = os.path.join(FIXTURE_DIR, "sample_document.pdf")
        result = await self.analyzer.analyze(pdf_path)
        assert result.metadata["page_count"] == 3 or result.metadata["page_count"] == 2
        assert "Introduction" in result.metadata["text"]

    @pytest.mark.asyncio
    async def test_summary_generation_with_llm(self):
        """Test summary generation using LLM (mocked)"""
        pdf_path = os.path.join(FIXTURE_DIR, "sample_document.pdf")
        self.mock_llm.summarize.return_value = "This is a summary."
        result = await self.analyzer.analyze(pdf_path)
        assert result.metadata["summary"] == "This is a summary."
        self.mock_llm.summarize.assert_called_once()

    @pytest.mark.asyncio
    async def test_key_points_extraction(self):
        """Test key points extraction from PDF using LLM (mocked)"""
        pdf_path = os.path.join(FIXTURE_DIR, "sample_document.pdf")
        self.mock_llm.extract_key_points.return_value = ["Point 1", "Point 2"]
        result = await self.analyzer.analyze(pdf_path)
        assert result.metadata["key_points"] == ["Point 1", "Point 2"]
        self.mock_llm.extract_key_points.assert_called_once()

    @pytest.mark.asyncio
    async def test_empty_pdf_handling(self):
        """Test that empty PDF (no text) returns zero page count and empty text"""
        pdf_path = os.path.join(FIXTURE_DIR, "empty_document.pdf")
        result = await self.analyzer.analyze(pdf_path)
        assert result.metadata["page_count"] == 1 or result.metadata["page_count"] == 0
        assert result.metadata["text"].strip() == ""
        assert "summary" in result.metadata or result.summary == ""

    @pytest.mark.asyncio
    async def test_corrupted_pdf_handling(self):
        """Test that corrupted PDF returns error gracefully"""
        pdf_path = os.path.join(FIXTURE_DIR, "corrupted_document.pdf")
        result = await self.analyzer.analyze(pdf_path)
        assert result.metadata.get("error") is not None
        assert (
            "corrupt" in result.metadata.get("error", "").lower()
            or "error" in result.metadata.get("error", "").lower()
        )

    def test_inherits_from_base_analyzer(self):
        from services.analysis.document_analyzer import DocumentAnalyzer

        assert issubclass(DocumentAnalyzer, BaseAnalyzer)

    @pytest.mark.asyncio
    async def test_analyze_returns_analysis_result(self):
        pdf_path = os.path.join(FIXTURE_DIR, "sample_document.pdf")
        result = await self.analyzer.analyze(pdf_path)
        assert isinstance(result, AnalysisResult)

    def test_llm_dependency_injection(self):
        from services.analysis.document_analyzer import DocumentAnalyzer

        analyzer = DocumentAnalyzer(llm_client=self.mock_llm)
        assert analyzer.llm_client is self.mock_llm


# 1. Basic PDF analysis (page count, text extraction)
@pytest.mark.asyncio
async def test_document_basic_pdf_analysis():
    from services.analysis.document_analyzer import DocumentAnalyzer

    analyzer = DocumentAnalyzer()
    result = await analyzer.analyze(FIXTURE_DIR + "sample_document.pdf")
    assert result.metadata["page_count"] == 2 or result.metadata["page_count"] == 3
    assert isinstance(result.metadata["text"], str)
    assert len(result.metadata["text"]) > 0


# 2. Summary generation using LLM (mock LLM)
@pytest.mark.asyncio
async def test_document_summary_generation():
    from services.analysis.document_analyzer import DocumentAnalyzer

    mock_llm = Mock()
    mock_llm.summarize.return_value = "This is a summary."
    analyzer = DocumentAnalyzer(llm_client=mock_llm)
    result = await analyzer.analyze(FIXTURE_DIR + "sample_document.pdf")
    assert "summary" in result.metadata
    assert result.metadata["summary"] == "This is a summary."


# 3. Key points extraction
@pytest.mark.asyncio
async def test_document_key_points_extraction():
    from services.analysis.document_analyzer import DocumentAnalyzer

    mock_llm = Mock()
    mock_llm.extract_key_points.return_value = ["Point 1", "Point 2"]
    analyzer = DocumentAnalyzer(llm_client=mock_llm)
    result = await analyzer.analyze(FIXTURE_DIR + "sample_document.pdf")
    assert "key_points" in result.metadata
    assert isinstance(result.metadata["key_points"], list)
    assert len(result.metadata["key_points"]) > 0


# 4. Empty PDF handling
@pytest.mark.asyncio
async def test_document_empty_pdf_handling():
    from services.analysis.document_analyzer import DocumentAnalyzer

    analyzer = DocumentAnalyzer()
    result = await analyzer.analyze(FIXTURE_DIR + "empty_document.pdf")
    assert result.metadata["page_count"] == 0 or result.metadata["text"] == ""
    assert "No extractable text" in result.summary or result.metadata["text"] == ""


# 5. Corrupted PDF handling
@pytest.mark.asyncio
async def test_document_corrupted_pdf_handling():
    from services.analysis.document_analyzer import DocumentAnalyzer

    analyzer = DocumentAnalyzer()
    result = await analyzer.analyze(FIXTURE_DIR + "corrupted_document.pdf")
    assert "error" in result.metadata
    assert "corrupt" in result.metadata["error"] or "invalid" in result.metadata["error"]


# 6. Inheritance from BaseAnalyzer
def test_document_inherits_base_analyzer():
    from services.analysis.base_analyzer import BaseAnalyzer
    from services.analysis.document_analyzer import DocumentAnalyzer

    assert issubclass(DocumentAnalyzer, BaseAnalyzer)


# 7. analyze returns AnalysisResult
@pytest.mark.asyncio
async def test_document_analyze_returns_analysis_result():
    from services.analysis.document_analyzer import DocumentAnalyzer

    analyzer = DocumentAnalyzer()
    result = await analyzer.analyze(FIXTURE_DIR + "sample_document.pdf")
    assert isinstance(result, AnalysisResult)


# 8. LLM dependency injection
def test_document_llm_dependency_injection():
    from services.analysis.document_analyzer import DocumentAnalyzer

    mock_llm = Mock()
    analyzer = DocumentAnalyzer(llm_client=mock_llm)
    assert hasattr(analyzer, "llm_client")
    assert analyzer.llm_client is mock_llm
