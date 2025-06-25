import os
import pytest
from unittest.mock import Mock
from services.analysis.base_analyzer import BaseAnalyzer
from services.domain.models import AnalysisResult

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), '../../fixtures')

class TestDocumentAnalyzer:
    def setup_method(self):
        # Mock LLM client for summary/key points
        self.mock_llm = Mock()
        # DocumentAnalyzer will be implemented later
        from services.analysis.document_analyzer import DocumentAnalyzer
        self.analyzer = DocumentAnalyzer(llm_client=self.mock_llm)

    def test_basic_pdf_analysis(self):
        """Test page count and text extraction from a normal PDF"""
        pdf_path = os.path.join(FIXTURE_DIR, 'sample_document.pdf')
        result = self.analyzer.analyze(pdf_path)
        assert result.metadata['page_count'] == 3
        assert 'Introduction' in result.metadata['text']

    def test_summary_generation_with_llm(self):
        """Test summary generation using LLM (mocked)"""
        pdf_path = os.path.join(FIXTURE_DIR, 'sample_document.pdf')
        self.mock_llm.summarize.return_value = "This is a summary."
        result = self.analyzer.analyze(pdf_path)
        assert result.metadata['summary'] == "This is a summary."
        self.mock_llm.summarize.assert_called_once()

    def test_key_points_extraction(self):
        """Test key points extraction from PDF using LLM (mocked)"""
        pdf_path = os.path.join(FIXTURE_DIR, 'sample_document.pdf')
        self.mock_llm.extract_key_points.return_value = ["Point 1", "Point 2"]
        result = self.analyzer.analyze(pdf_path)
        assert result.metadata['key_points'] == ["Point 1", "Point 2"]
        self.mock_llm.extract_key_points.assert_called_once()

    def test_empty_pdf_handling(self):
        """Test that empty PDF (no text) returns zero page count and empty text"""
        pdf_path = os.path.join(FIXTURE_DIR, 'empty_document.pdf')
        result = self.analyzer.analyze(pdf_path)
        assert result.metadata['page_count'] == 1
        assert result.metadata['text'].strip() == ''
        assert 'summary' in result.metadata  # Should still attempt summary

    def test_corrupted_pdf_handling(self):
        """Test that corrupted PDF returns error gracefully"""
        pdf_path = os.path.join(FIXTURE_DIR, 'corrupted_document.pdf')
        result = self.analyzer.analyze(pdf_path)
        assert result.metadata.get('error') is not None
        assert 'corrupt' in result.metadata.get('error', '').lower() or 'error' in result.metadata.get('error', '').lower()

    def test_inherits_from_base_analyzer(self):
        from services.analysis.document_analyzer import DocumentAnalyzer
        assert issubclass(DocumentAnalyzer, BaseAnalyzer)

    def test_analyze_returns_analysis_result(self):
        pdf_path = os.path.join(FIXTURE_DIR, 'sample_document.pdf')
        result = self.analyzer.analyze(pdf_path)
        assert isinstance(result, AnalysisResult)

    def test_llm_dependency_injection(self):
        from services.analysis.document_analyzer import DocumentAnalyzer
        analyzer = DocumentAnalyzer(llm_client=self.mock_llm)
        assert analyzer.llm_client is self.mock_llm 