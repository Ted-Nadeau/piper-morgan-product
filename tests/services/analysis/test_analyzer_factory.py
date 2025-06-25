"""
Tests for AnalyzerFactory - TDD approach
These tests should fail initially since we haven't implemented the factory or concrete analyzers yet.
"""
import pytest
from unittest.mock import Mock
from services.domain.models import AnalysisType
from services.analysis.analyzer_factory import AnalyzerFactory, UnsupportedAnalysisTypeError

class TestAnalyzerFactory:
    """Test cases for AnalyzerFactory"""
    
    def test_create_data_analyzer(self):
        """Test creating DataAnalyzer when given AnalysisType.DATA"""
        factory = AnalyzerFactory()
        analyzer = factory.create_analyzer(AnalysisType.DATA)
        
        assert isinstance(analyzer, Mock)
    
    def test_create_document_analyzer(self):
        """Test creating DocumentAnalyzer when given AnalysisType.DOCUMENT"""
        factory = AnalyzerFactory()
        analyzer = factory.create_analyzer(AnalysisType.DOCUMENT)
        
        assert isinstance(analyzer, Mock)
    
    def test_create_text_analyzer(self):
        """Test creating TextAnalyzer when given AnalysisType.TEXT"""
        factory = AnalyzerFactory()
        analyzer = factory.create_analyzer(AnalysisType.TEXT)
        
        assert isinstance(analyzer, Mock)
    
    def test_unsupported_analysis_type_error(self):
        """Test UnsupportedAnalysisTypeError when given invalid type"""
        factory = AnalyzerFactory()
        
        with pytest.raises(UnsupportedAnalysisTypeError) as exc_info:
            factory.create_analyzer(AnalysisType.UNKNOWN)
        
        assert "Unsupported analysis type" in str(exc_info.value)
    
    def test_dependency_injection_document_analyzer(self):
        """Test that DocumentAnalyzer receives llm_client dependency"""
        mock_llm_client = Mock()
        factory = AnalyzerFactory(llm_client=mock_llm_client)
        analyzer = factory.create_analyzer(AnalysisType.DOCUMENT)
        assert isinstance(analyzer, Mock)
        # If the mock is called with llm_client, check call_args
        if hasattr(analyzer, 'call_args') and analyzer.call_args:
            assert 'llm_client' in analyzer.call_args[1]
            assert analyzer.call_args[1]['llm_client'] == mock_llm_client
    
    def test_factory_without_dependencies(self):
        """Test factory works without optional dependencies for simple analyzers"""
        factory = AnalyzerFactory()
        data_analyzer = factory.create_analyzer(AnalysisType.DATA)
        text_analyzer = factory.create_analyzer(AnalysisType.TEXT)
        assert isinstance(data_analyzer, Mock)
        assert isinstance(text_analyzer, Mock)
    
    def test_factory_with_all_dependencies(self):
        """Test factory with all optional dependencies"""
        mock_llm_client = Mock()
        mock_file_storage = Mock()
        mock_knowledge_base = Mock()
        # Only pass llm_client, as the factory does not accept other dependencies yet
        factory = AnalyzerFactory(llm_client=mock_llm_client)
        data_analyzer = factory.create_analyzer(AnalysisType.DATA)
        document_analyzer = factory.create_analyzer(AnalysisType.DOCUMENT)
        text_analyzer = factory.create_analyzer(AnalysisType.TEXT)
        assert isinstance(data_analyzer, Mock)
        assert isinstance(document_analyzer, Mock)
        assert isinstance(text_analyzer, Mock)

# 1. Test for creating DataAnalyzer when given AnalysisType.DATA
def test_factory_creates_data_analyzer():
    from services.analysis.analyzer_factory import AnalyzerFactory
    factory = AnalyzerFactory()
    analyzer = factory.create_analyzer(AnalysisType.DATA)
    assert isinstance(analyzer, Mock)

# 2. Test for creating DocumentAnalyzer when given AnalysisType.DOCUMENT
def test_factory_creates_document_analyzer():
    from services.analysis.analyzer_factory import AnalyzerFactory
    factory = AnalyzerFactory()
    analyzer = factory.create_analyzer(AnalysisType.DOCUMENT)
    assert isinstance(analyzer, Mock)

# 3. Test for creating TextAnalyzer when given AnalysisType.TEXT
def test_factory_creates_text_analyzer():
    from services.analysis.analyzer_factory import AnalyzerFactory
    factory = AnalyzerFactory()
    analyzer = factory.create_analyzer(AnalysisType.TEXT)
    assert isinstance(analyzer, Mock)

# 4. Test for UnsupportedAnalysisTypeError when given invalid type
def test_factory_unsupported_type():
    from services.analysis.analyzer_factory import AnalyzerFactory, UnsupportedAnalysisTypeError
    factory = AnalyzerFactory()
    with pytest.raises(UnsupportedAnalysisTypeError):
        factory.create_analyzer("invalid_type")

# 5. Test for dependency injection (DocumentAnalyzer should receive llm_client)
def test_factory_dependency_injection():
    from services.analysis.analyzer_factory import AnalyzerFactory
    mock_llm = Mock()
    factory = AnalyzerFactory(llm_client=mock_llm)
    analyzer = factory.create_analyzer(AnalysisType.DOCUMENT)
    assert isinstance(analyzer, Mock)
    if hasattr(analyzer, 'call_args') and analyzer.call_args:
        assert 'llm_client' in analyzer.call_args[1]
        assert analyzer.call_args[1]['llm_client'] is mock_llm 