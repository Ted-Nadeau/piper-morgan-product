"""
AnalyzerFactory - Factory for creating file analyzers
"""
from typing import Optional, Dict, Any
from services.domain.models import AnalysisType
from services.analysis.csv_analyzer import CSVAnalyzer
from services.analysis.document_analyzer import DocumentAnalyzer
from services.analysis.text_analyzer import TextAnalyzer


class UnsupportedAnalysisTypeError(Exception):
    """Raised when an unsupported analysis type is requested"""
    def __init__(self, analysis_type: AnalysisType):
        self.analysis_type = analysis_type
        super().__init__(f"Unsupported analysis type: {analysis_type.value}")


class AnalyzerFactory:
    """Factory for creating file analyzers based on analysis type"""
    
    def __init__(self, 
                 llm_client: Optional[Any] = None,
                 file_storage: Optional[Any] = None,
                 knowledge_base: Optional[Any] = None):
        """
        Initialize factory with optional dependencies
        
        Args:
            llm_client: LLM client for document analysis
            file_storage: File storage service
            knowledge_base: Knowledge base service
        """
        self.llm_client = llm_client
        self.file_storage = file_storage
        self.knowledge_base = knowledge_base
        
        # Registry mapping analysis types to analyzer creation methods
        self.analyzer_registry = {
            AnalysisType.DATA: self._create_data_analyzer,
            AnalysisType.DOCUMENT: self._create_document_analyzer,
            AnalysisType.TEXT: self._create_text_analyzer,
        }
    
    def create_analyzer(self, analysis_type: AnalysisType) -> Any:
        """
        Create an analyzer for the given analysis type
        
        Args:
            analysis_type: Type of analysis to perform
            
        Returns:
            Analyzer instance
            
        Raises:
            UnsupportedAnalysisTypeError: If analysis type is not supported
        """
        if analysis_type not in self.analyzer_registry:
            raise UnsupportedAnalysisTypeError(analysis_type)
        
        return self.analyzer_registry[analysis_type]()
    
    def _create_data_analyzer(self) -> CSVAnalyzer:
        """Create a real CSVAnalyzer"""
        return CSVAnalyzer()
    
    def _create_document_analyzer(self) -> DocumentAnalyzer:
        """Create a real DocumentAnalyzer with llm_client dependency"""
        return DocumentAnalyzer(llm_client=self.llm_client)
    
    def _create_text_analyzer(self) -> TextAnalyzer:
        """Create a real TextAnalyzer"""
        return TextAnalyzer() 