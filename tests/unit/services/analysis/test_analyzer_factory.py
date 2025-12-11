"""
Tests for AnalyzerFactory - TDD approach
These tests should fail initially since we haven't implemented the factory or concrete analyzers yet.
"""

from unittest.mock import Mock

import pytest

from services.analysis.analyzer_factory import AnalyzerFactory, UnsupportedAnalysisTypeError
from services.analysis.csv_analyzer import CSVAnalyzer
from services.analysis.document_analyzer import DocumentAnalyzer
from services.analysis.text_analyzer import TextAnalyzer
from services.domain.models import AnalysisType


class TestAnalyzerFactory:
    """Test cases for AnalyzerFactory"""

    @pytest.mark.smoke
    def test_create_data_analyzer(self):
        """Test creating DataAnalyzer when given AnalysisType.DATA"""
        factory = AnalyzerFactory()
        analyzer = factory.create_analyzer(AnalysisType.DATA)
        assert isinstance(analyzer, CSVAnalyzer)

    @pytest.mark.smoke
    def test_create_document_analyzer(self):
        """Test creating DocumentAnalyzer when given AnalysisType.DOCUMENT"""
        factory = AnalyzerFactory()
        analyzer = factory.create_analyzer(AnalysisType.DOCUMENT)
        assert isinstance(analyzer, DocumentAnalyzer)

    @pytest.mark.smoke
    def test_create_text_analyzer(self):
        """Test creating TextAnalyzer when given AnalysisType.TEXT"""
        factory = AnalyzerFactory()
        analyzer = factory.create_analyzer(AnalysisType.TEXT)
        assert isinstance(analyzer, TextAnalyzer)

    @pytest.mark.smoke
    def test_unsupported_analysis_type_error(self):
        """Test UnsupportedAnalysisTypeError when given invalid type"""
        factory = AnalyzerFactory()
        with pytest.raises(UnsupportedAnalysisTypeError) as exc_info:
            factory.create_analyzer(AnalysisType.UNKNOWN)
        assert "Unsupported analysis type" in str(exc_info.value)

    @pytest.mark.smoke
    def test_dependency_injection_document_analyzer(self):
        """Test that DocumentAnalyzer receives llm_client dependency"""
        mock_llm_client = Mock()
        factory = AnalyzerFactory(llm_client=mock_llm_client)
        analyzer = factory.create_analyzer(AnalysisType.DOCUMENT)
        assert isinstance(analyzer, DocumentAnalyzer)
        assert getattr(analyzer, "llm_client", None) is mock_llm_client

    @pytest.mark.smoke
    def test_factory_without_dependencies(self):
        """Test factory works without optional dependencies for simple analyzers"""
        factory = AnalyzerFactory()
        data_analyzer = factory.create_analyzer(AnalysisType.DATA)
        text_analyzer = factory.create_analyzer(AnalysisType.TEXT)
        assert isinstance(data_analyzer, CSVAnalyzer)
        assert isinstance(text_analyzer, TextAnalyzer)

    @pytest.mark.smoke
    def test_factory_with_all_dependencies(self):
        """Test factory with all optional dependencies"""
        mock_llm_client = Mock()
        mock_file_storage = Mock()
        mock_knowledge_base = Mock()
        factory = AnalyzerFactory(llm_client=mock_llm_client)
        data_analyzer = factory.create_analyzer(AnalysisType.DATA)
        document_analyzer = factory.create_analyzer(AnalysisType.DOCUMENT)
        text_analyzer = factory.create_analyzer(AnalysisType.TEXT)
        assert isinstance(data_analyzer, CSVAnalyzer)
        assert isinstance(document_analyzer, DocumentAnalyzer)
        assert isinstance(text_analyzer, TextAnalyzer)
        assert getattr(document_analyzer, "llm_client", None) is mock_llm_client


@pytest.mark.smoke
def test_factory_creates_data_analyzer():
    from services.analysis.analyzer_factory import AnalyzerFactory
    from services.analysis.csv_analyzer import CSVAnalyzer

    factory = AnalyzerFactory()
    analyzer = factory.create_analyzer(AnalysisType.DATA)
    assert isinstance(analyzer, CSVAnalyzer)


@pytest.mark.smoke
def test_factory_creates_document_analyzer():
    from services.analysis.analyzer_factory import AnalyzerFactory
    from services.analysis.document_analyzer import DocumentAnalyzer

    factory = AnalyzerFactory()
    analyzer = factory.create_analyzer(AnalysisType.DOCUMENT)
    assert isinstance(analyzer, DocumentAnalyzer)


@pytest.mark.smoke
def test_factory_creates_text_analyzer():
    from services.analysis.analyzer_factory import AnalyzerFactory
    from services.analysis.text_analyzer import TextAnalyzer

    factory = AnalyzerFactory()
    analyzer = factory.create_analyzer(AnalysisType.TEXT)
    assert isinstance(analyzer, TextAnalyzer)


@pytest.mark.smoke
def test_factory_unsupported_type():
    from services.analysis.analyzer_factory import AnalyzerFactory, UnsupportedAnalysisTypeError

    factory = AnalyzerFactory()
    with pytest.raises(UnsupportedAnalysisTypeError):
        factory.create_analyzer("invalid_type")


@pytest.mark.smoke
def test_factory_dependency_injection():
    from services.analysis.analyzer_factory import AnalyzerFactory
    from services.analysis.document_analyzer import DocumentAnalyzer

    mock_llm = Mock()
    factory = AnalyzerFactory(llm_client=mock_llm)
    analyzer = factory.create_analyzer(AnalysisType.DOCUMENT)
    assert isinstance(analyzer, DocumentAnalyzer)
    assert getattr(analyzer, "llm_client", None) is mock_llm
